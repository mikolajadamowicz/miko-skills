---
name: miko-review
description: >-
  Multi-lens code review of a branch or diff. Runs the review-truth,
  review-deep-modules, review-senior, review-minimal, review-experience and
  review-verify skills as parallel subagents, merges and filters their findings,
  and reports in chat.
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
| `review-experience` | `experience-reviewer` | Is this change good for the person who has to use it? | The diff changes code a consumer touches: a UI, CLI, user-facing message, or public or shared API |
| `review-verify` | `verify-reviewer` | Does the new or changed behaviour actually work when run? | The diff adds or changes behaviour (see below) |

Behaviour changes are code that can be executed: a function, command, endpoint, UI, script, CI job, or a config that changes what runs. Docs, comments, formatting, and test-only changes are not. When unsure, run `review-verify`; it reports "nothing to run" cheaply.

## Steps

1. **Find the diff.**
   - Default: `git diff $(git merge-base origin/HEAD HEAD)...HEAD` plus uncommitted changes (`git diff HEAD`). Fall back to `origin/main` or `main` if `origin/HEAD` is not set.
   - If the user names a PR, use `gh pr diff <n>` and `gh pr view <n>`.
   - If the diff is empty, say so and stop.
2. **Read repo context.** If the repo has a `REVIEW.md` at its root, read it. It lists helpers to reuse, module owners, repo rules, and how to run things. Pass its path to every lens. [review-context-template.md](review-context-template.md) shows the shape. Then load this skill's own extensions as [extensions.md](extensions.md) describes. Each lens loads its own.
3. **Pick lenses** with the table above. Tell the user in one line which lenses run and why any are skipped.
4. **Start one subagent per lens, all in the same turn so they run in parallel.**
   - If the lens's subagent from the table is available as a subagent type, start that type.
   - Otherwise start a general-purpose subagent.

   Each prompt contains:
   - the absolute path to the lens's `SKILL.md`, with the instruction to read it in full first and follow it
   - the absolute paths to [finding-format.md](finding-format.md) and [extensions.md](extensions.md)
   - the repo path, the base ref, and how to get the diff (do not paste a large diff; let the lens run git)
   - the `REVIEW.md` path, if there is one
   - any focus the user asked for

   The five reading lenses only read; tell them not to edit files. `review-verify` may run commands but must not edit tracked files, commit, or push.
5. **Merge.**
   - Set aside findings with confidence below 70.
   - Merge findings that point at the same `file:line` and the same underlying problem. Keep the clearer wording and list every lens that raised it.
   - When two lenses disagree (one says add a guard, another says remove it), keep both and say they conflict.
   - Check every Block finding yourself by opening the cited lines. Downgrade or drop it if the code does not show the problem.
   - Collect the `Extensions` and `Conflicts` lines from every lens, plus your own.
   - Add up the findings each lens says it left out at its limit.
   - Keep every entry from the `review-verify` report for the Verified section.
   - Record any lens that failed or returned nothing. It did not pass.
6. **Gate.** Show the user only what matters most.
   - Group findings with the same root cause into one, listing every site.
   - Set aside findings with no concrete scenario where something breaks or drifts, style preferences, and anything a linter or formatter would catch.
   - Sort by severity, then by confidence.
   - Show every Block, the top 8 Fix, and the top 5 Ask. Hide the rest. If the user asks to see everything, list every hidden and set-aside finding in the same layout, and say how many the lenses left out. Getting those means running the lens again with a focus on what it left out.
   - Pick the verdict: `Blocked` when any Block is left, `Fix first` when any Fix is left, `Not verified` when a lens failed or `review-verify` has any `could not run` entry, otherwise `Ship it`.
7. **Report** in chat using the layout below. Never post to GitHub.

## Report

```
<Blocked | Fix first | Not verified | Ship it>: <one sentence on the main reason>
<branch or PR> vs <base> · <N> files, +<added>/-<removed> · lenses: <lenses run> (<skipped or failed lens: reason>)
Extensions: <each file applied, with the skills that used it, or "none">

Conflicts
- `<extension file>:<line>` wants <what>; kept <the skill rule>. <or: local extension is tracked by git>

Block
1. `<file>:<line>` <what is wrong and when it breaks>. Fix: <concrete change at the owning site>. [<lenses>]

Fix
1. ...

Ask
1. <question> [<lenses>]

Verified
- <behaviour>: <command run> → <observed result>. <works | broken | could not run: why>

<N> Fix and <M> Ask findings hidden, <K> set aside as low confidence or minor, <L> left out by lenses. Ask "show all" to see them.
```

- Number findings within each section so the user can answer "fix Block 1 and Fix 3".
- Omit empty sections, zero counts in the hidden line, and the whole line when all its counts are zero. If no findings survive the gate and there are no Verified entries, give the verdict line and the hidden line, if any, and stop.
- Keep each finding to one or two sentences. The user can ask for detail.
