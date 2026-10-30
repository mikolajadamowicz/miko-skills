# miko-skills

Code review, skill-authoring, and prose-cleanup skills, plus review subagents, for Cursor, Claude Code, and OpenCode.

Run `/miko-review` on a branch. It starts one subagent per lens in parallel, merges their findings, and reports in chat.

| Skill | Checks |
| --- | --- |
| `miko-review` | Picks the lenses, runs them, merges and filters findings |
| `review-truth` | Comments that lie, values copied into two places, asymmetric branches, stale references, untrusted input used as a path |
| `review-deep-modules` | Shallow modules, information leakage, and pass-through layers, from Ousterhout's *A Philosophy of Software Design* |
| `review-senior` | Scalability, maintainability, readability |
| `review-minimal` | Whether the change could be smaller, reinvented helpers, unneeded guards, tests that would pass without the change |
| `review-verify` | Runs new or changed behaviour and reports what happened |

To give the lenses repo-specific context (helpers to reuse, owners, rules, how to run things), add a `REVIEW.md` at the repo root. See the [template](skills/miko-review/review-context-template.md).

The other skills are not part of review:

| Skill | Use it for |
| --- | --- |
| `skill-examples` | Indexes six public skill repos (Matt Pocock's skills, Superpowers, pstack, gstack, ECC, Callstack's software factory). The agent reads and cites them when searching for an existing skill, writing a new one, or reviewing one. |
| `humanize` | Removes AI writing patterns from technical prose: PR descriptions, docs, code comments, reports |
| `unslop` | Removes AI writing patterns from casual prose: chat, Slack, email, social posts |

## Install

Install all the skills together, since the review skills read each other's files. Use one route per harness, or the skills load twice.

| Harness | Skills and agents |
| --- | --- |
| Claude Code | `/plugin marketplace add mikolajadamowicz/miko-skills`, then `/plugin install miko-skills@miko-skills` |
| Cursor | Copy the repo into `~/.cursor/plugins/local/miko-skills` and reload the window. Cursor ignores symlinks there. |
| OpenCode | `npx skills add mikolajadamowicz/miko-skills -g -a opencode`, then `scripts/install-agents.sh --opencode` from a clone |

For skills only in any harness, run `npx skills add mikolajadamowicz/miko-skills -g`. `miko-review` then uses general-purpose subagents that read the same skills. To add the agents later, run the script from a clone:

```bash
scripts/install-agents.sh                      # ~/.claude/agents (Claude Code, and Cursor reads it too)
scripts/install-agents.sh --cursor             # ~/.cursor/agents
scripts/install-agents.sh --opencode           # ~/.config/opencode/agents
scripts/install-agents.sh --all path/to/repo   # all three, inside a project
```

Re-run it after pulling changes to `agents/`.

### Upgrading from 0.2

Version 0.3 renamed the `review` skill to `miko-review`. Updating does not delete the old `review/` directory, and it keeps answering `/review` and generic review requests. Remove it:

- `npx skills` installs: `npx skills remove -g review`
- Cursor local plugin: delete `~/.cursor/plugins/local/miko-skills/skills/review`, or replace the whole folder with a fresh copy

The Claude Code plugin installs each version into its own directory, so it needs no cleanup.

## Models

Agents use the parent chat's model. To pin one, set `model:` in the installed agent file. Each harness has its own format:

- Cursor: `claude-opus-5[effort=high]`
- Claude Code: `opus`, `sonnet`, `haiku`, or a full model ID
- OpenCode: `anthropic/claude-opus-5`

## Read-only reviewers

Four of the lenses only read code. Cursor enforces that with `readonly`, and OpenCode with `permission: edit: deny`. In Claude Code they have no edit or write tools, but Bash can still write files, so permission prompts are the real guard.

## Contributing

[AGENTS.md](AGENTS.md) has the rules for keeping all three harnesses working and the checks to run before committing.
