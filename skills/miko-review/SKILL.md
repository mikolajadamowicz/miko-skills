---
name: miko-review
description: >-
  Multi-lens code review of a branch or diff. Runs the review-truth,
  review-deep-modules, review-senior, review-minimal and review-verify skills as
  parallel subagents, merges and filters their findings, and reports in chat.
  Use only when the user names miko-review or invokes /miko-review. A generic
  request to review code, a PR, or a diff does not start this skill.
---

# Review

You coordinate the review. You do not review code yourself: each lens runs in its own subagent with a fresh context, and you merge what they return.

## Lenses

The lenses are sibling skills, installed next to this one. Their `SKILL.md` files are in the directories beside this skill's directory.

Each lens may also be installed as a custom subagent (Cursor or Claude Code), which wraps the same skill and adds a model and read-only tools. Installed as a plugin, the subagent type carries the plugin prefix, such as `miko-skills:truth-reviewer`.

| Skill | Subagent | Question it answers | Runs when |
| --- | --- | --- | --- |
| `review-truth` | `truth-reviewer` | Is everything the diff says true, and does every fact have one owner? | Always |
| `review-deep-modules` | `deep-modules-reviewer` | Do the modules hide complexity behind simple interfaces? | The diff adds or changes code, not only docs or config |
| `review-senior` | `senior-reviewer` | Will this scale, stay maintainable, and read clearly? | The diff adds or changes code |
| `review-minimal` | `minimal-reviewer` | Is this the smallest change, and does it reuse what exists? | The diff adds or changes code |
| `review-verify` | `verify-reviewer` | Does the new or changed behaviour actually work when run? | The diff adds or changes behaviour (see below) |

Behaviour changes are code that can be executed: a function, command, endpoint, UI, script, CI job, or a config that changes what runs. Docs, comments, formatting, and test-only changes are not. When unsure, run `review-verify`; it reports "nothing to run" cheaply.

## Steps

1. **Find the diff.**
   - Default: `git diff $(git merge-base origin/HEAD HEAD)...HEAD` plus uncommitted changes (`git diff HEAD`). Fall back to `origin/main` or `main` if `origin/HEAD` is not set.
   - If the user names a PR, use `gh pr diff <n>` and `gh pr view <n>`.
   - If the diff is empty, say so and stop.
2. **Read repo context.** If the repo has a `REVIEW.md` at its root, read it. It lists helpers to reuse, module owners, repo rules, and how to run things. Pass its path to every lens. [review-context-template.md](review-context-template.md) shows the shape.
3. **Pick lenses** with the table above. Tell the user in one line which lenses run and why any are skipped.
4. **Start one subagent per lens, all in the same turn so they run in parallel.**
   - If the lens's subagent from the table is available as a subagent type, start that type.
   - Otherwise start a general-purpose subagent.

   Each prompt contains:
   - the absolute path to the lens's `SKILL.md`, with the instruction to read it in full first and follow it
   - the absolute path to [finding-format.md](finding-format.md)
   - the repo path, the base ref, and how to get the diff (do not paste a large diff; let the lens run git)
   - the `REVIEW.md` path, if there is one
   - any focus the user asked for

   The four reading lenses only read; tell them not to edit files. `review-verify` may run commands but must not edit tracked files, commit, or push.
5. **Merge.**
   - Drop findings with confidence below 70.
   - Merge findings that point at the same `file:line` and the same underlying problem. Keep the clearer wording and list every lens that raised it.
   - When two lenses disagree (one says add a guard, another says remove it), keep both and say they conflict.
   - Check every Block finding yourself by opening the cited lines. Downgrade or drop it if the code does not show the problem.
6. **Report** in chat using the layout below. Never post to GitHub.

## Report

```
Review of <branch or PR> against <base> — <N> files, +<added>/-<removed>
Lenses: truth, deep-modules, senior, minimal, verify (<skipped lens: reason>)

Block
- `<file>:<line>` [<lens>] <what is wrong and when it breaks>. Fix: <concrete change at the owning site>.

Fix
- ...

Ask
- ...

Verified
- <behaviour>: <command run> → <observed result>. <works | broken | could not run: why>
```

- Sort each section by confidence, highest first.
- Omit empty sections. If nothing survives the filter, say so in one line.
- Keep each finding to one or two sentences. The user can ask for detail.
