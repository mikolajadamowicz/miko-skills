#!/usr/bin/env python3
"""Read Claude Code, Cursor, and OpenCode chat history and find how skills were used.

Without --skill, prints how many chats used each skill. With --skill, also writes one
Markdown file per chat that used it, starting at the first use, to a new private temp
directory. Reads history only. Uses only the standard library.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sqlite3
import tempfile
from collections import Counter

STRIP_TAGS = (
    "system_reminder|system-reminder|attached_files|open_and_recently_viewed_files|"
    "user_info|git_status|timestamp|local-command-caveat|local-command-stdout|"
    "command-message|task-notification"
)
SKILL_BODY = re.compile(r"^(?:Base directory for this skill: \S*/([a-z0-9-]+)|<skill_content name=\"([a-z0-9-]+)\")")
SKILL_FILE = re.compile(r"/([a-z0-9][a-z0-9-]*)/SKILL\.md")
SLASH = re.compile(r"(?<![\w/.:<-])/([a-z0-9][a-z0-9:-]*)(?![\w/.-])")
INJECTED = "Briefly inform the user about the task result"


class Chat:
    def __init__(self, harness, chat_id, where, updated):
        self.harness = harness
        self.chat_id = chat_id
        self.where = where
        self.updated = updated
        # Each message is (role, text, skills it names or uses).
        self.messages = []
        # Names a tool call, an attached skill, or a loaded skill body proves were used in
        # this chat. A slash name alone may be a built-in command or a passing mention.
        self.confirmed = set()

    def add(self, role, text, skills=()):
        self.messages.append((role, text, set(skills)))

    def first_use(self):
        """Index of the first message that names or uses each confirmed skill."""
        first = {}
        for index, (_, _, skills) in enumerate(self.messages):
            for skill in skills & self.confirmed:
                first.setdefault(skill, index)
        return first


def bare(skill):
    return skill.split(":")[-1]


def clean_user_text(text):
    attached = re.findall(r"^Skill Name: ([a-z0-9-]+)$", text, flags=re.M)
    text = re.sub(r"<manually_attached_skills>.*?</manually_attached_skills>", "", text, flags=re.S)
    text = re.sub(rf"<({STRIP_TAGS})\b[^>]*>.*?</\1>", "", text, flags=re.S)
    query = re.search(r"<user_query>(.*?)</user_query>", text, flags=re.S)
    if query:
        text = query.group(1)
    command = re.search(r"<command-name>(.*?)</command-name>", text, flags=re.S)
    if command:
        args = re.search(r"<command-args>(.*?)</command-args>", text, flags=re.S)
        text = f"{command.group(1)} {args.group(1) if args else ''}"
    text = text.strip()
    return text, {bare(s) for s in SLASH.findall(text)}, set(attached)


def skills_in_tool_input(tool_input):
    return set(SKILL_FILE.findall(json.dumps(tool_input)))


def read_jsonl(path):
    with open(path, errors="replace") as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def read_blocks(chat, role, content, tool_skills):
    """Add one message from Anthropic-style content, which Claude Code and Cursor share."""
    blocks = [{"type": "text", "text": content}] if isinstance(content, str) else content or []
    text = "\n".join(b.get("text", "") for b in blocks if b.get("type") == "text").strip()
    skills = set()
    for block in blocks:
        if block.get("type") == "tool_use":
            skills |= tool_skills(block)
    chat.confirmed |= skills
    if role == "user":
        body = SKILL_BODY.match(text)
        if body:
            name = body.group(1) or body.group(2)
            chat.confirmed.add(name)
            chat.add(role, f"[skill {name} loaded]", {name})
            return
        if not text or text.startswith(INJECTED):
            return
        text, named, attached = clean_user_text(text)
        chat.confirmed |= attached
        skills |= named | attached
        if not text:
            return
    if text or skills:
        chat.add(role, text, skills)


def claude_chats():
    root = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")

    def tool_skills(block):
        input_ = block.get("input", {})
        if block.get("name") == "Skill":
            return {bare(input_.get("skill", ""))} - {""}
        return skills_in_tool_input(input_)

    # Subagent transcripts sit one level deeper, so this reads only the user's own chats.
    for path in glob.glob(os.path.join(glob.escape(root), "projects", "*", "*.jsonl")):
        name = os.path.basename(path)[:-len(".jsonl")]
        chat = Chat("claude-code", name, os.path.basename(os.path.dirname(path)), os.path.getmtime(path))
        for entry in read_jsonl(path):
            if entry.get("cwd"):
                chat.where = entry["cwd"]
            role = entry.get("type")
            if role in ("user", "assistant") and not entry.get("isMeta") and not entry.get("isSidechain"):
                read_blocks(chat, role, entry.get("message", {}).get("content"), tool_skills)
        yield chat


def cursor_chats():
    root = os.path.expanduser("~/.cursor/projects")
    pattern = os.path.join(glob.escape(root), "*", "agent-transcripts", "*", "*.jsonl")

    def tool_skills(block):
        return skills_in_tool_input(block.get("input", {}))

    for path in glob.glob(pattern):
        name = os.path.basename(path)[:-len(".jsonl")]
        project = path.split(os.sep)[-4]
        chat = Chat("cursor", name, project, os.path.getmtime(path))
        for entry in read_jsonl(path):
            role = entry.get("role")
            if role in ("user", "assistant"):
                read_blocks(chat, role, entry.get("message", {}).get("content"), tool_skills)
        yield chat


def opencode_chats():
    data = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    path = os.path.join(data, "opencode", "opencode.db")
    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        tables = {row[0] for row in db.execute("select name from sqlite_master where type='table'")}
        if not {"session_v2", "session_message"} <= tables:
            raise RuntimeError("the database has no session_v2 and session_message tables")
        sessions = db.execute(
            "select id, directory, time_updated from session_v2 where parent_id is null"
        ).fetchall()
        for session_id, directory, updated in sessions:
            chat = Chat("opencode", session_id, directory, updated / 1000)
            rows = db.execute(
                "select type, data from session_message where session_id = ? order by seq",
                (session_id,),
            )
            for kind, raw in rows:
                message = json.loads(raw)
                if kind == "user":
                    text, named, attached = clean_user_text(message.get("text", ""))
                    chat.confirmed |= attached
                    if text:
                        chat.add("user", text, named | attached)
                elif kind == "assistant":
                    parts, skills = [], set()
                    for block in message.get("content", []):
                        if block.get("type") == "text":
                            parts.append(block.get("text", ""))
                        elif block.get("type") == "tool":
                            input_ = block.get("state", {}).get("input", {})
                            if block.get("name") == "skill":
                                skills |= {bare(input_.get("id") or input_.get("name") or "")} - {""}
                            else:
                                skills |= skills_in_tool_input(input_)
                    chat.confirmed |= skills
                    text = "\n".join(parts).strip()
                    if text or skills:
                        chat.add("assistant", text, skills)
            yield chat
    finally:
        db.close()


SOURCES = {
    "claude-code": (claude_chats, lambda: os.path.isdir(
        os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude"), "projects"))),
    "cursor": (cursor_chats, lambda: os.path.isdir(os.path.expanduser("~/.cursor/projects"))),
    "opencode": (opencode_chats, lambda: os.path.isfile(os.path.join(
        os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share"), "opencode", "opencode.db"))),
}


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def write_chat(chat, skill_start, skills, out_dir, max_chars):
    start = min(skill_start[s] for s in skills)
    # The user's message that asked for the skill may come just before the tool call.
    if chat.messages[start][0] != "user" and start and chat.messages[start - 1][0] == "user":
        start -= 1
    follow_ups = sum(
        1 for role, text, _ in chat.messages[start + 1:]
        if role == "user" and not re.fullmatch(r"\[skill [a-z0-9-]+ loaded\]", text)
    )
    date = datetime.date.fromtimestamp(chat.updated).isoformat()
    lines = [
        f"# {chat.harness} {chat.chat_id}",
        f"where: {chat.where}",
        f"last active: {date}",
        f"skills: {', '.join(sorted(skills))}",
        f"user messages after the first use: {follow_ups}",
    ]
    for index, (role, text, used) in enumerate(chat.messages[start:], start):
        cut = len(text) - max_chars
        body = text if cut <= 0 else f"{text[:max_chars]}\n[cut {cut} characters]"
        tag = f" uses {', '.join(sorted(used))}" if used else ""
        lines.append(f"\n### {role.upper()} [{index}]{tag}\n{body}")
    name = f"{chat.harness}_{re.sub(r'[^A-Za-z0-9._-]', '-', chat.chat_id)}.md"
    with open(os.path.join(out_dir, name), "w") as f:
        f.write("\n".join(lines) + "\n")
    return follow_ups


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", action="append", default=[], help="skill to extract; repeat for several")
    parser.add_argument("--repo", help="keep chats whose directory contains this text, such as a repo name")
    parser.add_argument("--since", help="keep chats active on or after this date, YYYY-MM-DD")
    parser.add_argument("--max-chars", type=int, default=12000, help="cut longer messages at this length")
    args = parser.parse_args()

    since = datetime.datetime.fromisoformat(args.since).timestamp() if args.since else 0
    wanted = {bare(s) for s in args.skill}
    repo = slug(args.repo) if args.repo else None
    out_dir = tempfile.mkdtemp(prefix="improve-skills-") if wanted else None

    uses = Counter()
    scanned = Counter()
    written = Counter()
    follow_ups = 0
    problems = []
    for harness, (read, installed) in SOURCES.items():
        if not installed():
            problems.append(f"{harness}: no history on this machine")
            continue
        try:
            for chat in read():
                if chat.updated < since or (repo and repo not in slug(chat.where)):
                    continue
                scanned[harness] += 1
                first = chat.first_use()
                uses.update((harness, skill) for skill in first)
                matched = wanted & first.keys()
                if matched:
                    follow_ups += 1 if write_chat(chat, first, matched, out_dir, args.max_chars) else 0
                    written[harness] += 1
        except (OSError, RuntimeError, sqlite3.Error, ValueError) as error:
            problems.append(f"{harness}: could not read all history: {error}")

    for harness in SOURCES:
        print(f"{harness}: {scanned[harness]} chats scanned")
    for problem in problems:
        print(problem)
    if wanted:
        print(f"extracted {sum(written.values())} chats to {out_dir}: {dict(written)}")
        print(f"chats with user messages after the first use: {follow_ups}")
    else:
        totals = Counter()
        for (_, skill), count in uses.items():
            totals[skill] += count
        print("chats per skill (includes chats that edit the skill):")
        for skill, count in totals.most_common():
            per = {h: uses[(h, skill)] for h in SOURCES if uses[(h, skill)]}
            print(f"  {skill}: {count} {per}")


if __name__ == "__main__":
    main()
