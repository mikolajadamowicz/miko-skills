# miko-skills

Code review, skill-authoring, and prose-cleanup skills, plus review subagents, that must work in three harnesses: **Cursor**, **Claude Code**, and **OpenCode**. Every change keeps all three working. If a change can only work in one, stop and ask.

## Layout

| Path | Owns | Read by |
| --- | --- | --- |
| `skills/<name>/SKILL.md` | All rules and steps | All three, and the Vercel `skills` CLI |
| `agents/*.md` | Subagent wrappers: frontmatter plus a pointer to one skill | Cursor and Claude Code as is; OpenCode after `scripts/install-agents.sh --opencode` converts them |
| `.cursor-plugin/plugin.json` | Cursor plugin manifest | Cursor |
| `.claude-plugin/plugin.json`, `marketplace.json` | Claude Code plugin and marketplace | Claude Code |
| `scripts/install-agents.sh` | Installing agents per harness, including the OpenCode conversion | Users |
| `scripts/check.sh` | Drift checks for every rule below that a script can check | You, before every commit |

## Rules

### Skills are the single source

- Every review rule lives in a skill. Agent bodies only say which skill to follow and where to find it. A rule written in an agent body is missing from the fallback path, where `review` starts general-purpose subagents that read only the skills.
- Write skills in harness-neutral words: "start a subagent", "general-purpose subagent", "read the file". Name a harness's tool or path only in a table that covers all three.
- Skill `name` matches its directory, lowercase with hyphens. OpenCode rejects a mismatch.
- Skills reference each other through the sibling directory (`finding-format.md` in the sibling `review` skill directory), never by absolute or harness-specific path. Installed skills always sit side by side.

### Agent frontmatter is the intersection

Each harness reads different keys from the same file:

| Key | Cursor | Claude Code | OpenCode (after conversion) |
| --- | --- | --- | --- |
| `name` | identifier | identifier | dropped; filename is the name |
| `description` | delegation hint | delegation hint | kept |
| `model: inherit` | parent model | parent model | dropped; subagents inherit by default |
| `readonly: true` | blocks edits | ignored | becomes `permission: edit: deny` |
| `tools` | not documented | tool allowlist | dropped |
| `skills` | not documented | preloads skill text | dropped |
| — | — | — | `mode: subagent` added |

- `name` equals the filename without `.md`.
- `description` is one line. The OpenCode conversion reads only the first line.
- `model` stays `inherit`. Model IDs differ per harness (`claude-opus-5[effort=high]`, `opus`, `anthropic/claude-opus-5`), so a pinned value breaks the other two. Users pin in their installed copy.
- Reading lenses set `readonly: true` and `tools: Read, Grep, Glob, Bash`. Lenses that run things omit both.
- `skills` lists both `<skill>` and `miko-skills:<skill>`. Claude Code prefixes plugin skills and skips the name that does not exist.
- Any new key: check what each harness does with it. OpenCode passes unknown keys to the model provider, so the converter in `scripts/install-agents.sh` writes only `description`, `mode`, and `permission`. Extend the converter when a key needs an OpenCode equivalent.

### Agent bodies list every skill location

The body's skill search list covers project and user skill directories for all three harnesses, plus the plugin's `skills/` directory. It is identical in every agent. When a harness adds a location, update every agent in the same commit.

### Adding a lens

One commit adds all of:

1. `skills/review-<lens>/SKILL.md`, with the Setup section the other lenses use and findings in `finding-format.md`.
2. `agents/<lens>-reviewer.md`, copied from an existing agent of the same kind (reading or running).
3. A row in the lens table in `skills/review/SKILL.md`.
4. A row in the README skill table.

### Plugin manifests agree

`name`, `version`, and `description` are equal in `.cursor-plugin/plugin.json` and `.claude-plugin/plugin.json`. Bump `version` in both when skills or agents change.

## Before committing

Run each and fix every failure:

```bash
scripts/check.sh
claude plugin validate .
npx skills add . --list            # lists every skill under skills/
T=$(mktemp -d) && git -C "$T" init -q && scripts/install-agents.sh --all "$T" \
  && (cd "$T" && opencode debug agents --standalone | rg '"id": ".*-reviewer"')
```

The last command must print every agent. When a tool is not installed, say which check you skipped.
