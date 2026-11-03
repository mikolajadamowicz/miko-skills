# miko-skills

Code review, skill-authoring, and prose-cleanup skills, plus review subagents, for Cursor, Claude Code, and OpenCode.

Run `/miko-review` on a branch. It starts one subagent per lens in parallel, merges their findings, and reports in chat. The report opens with a verdict and shows every Block finding, the top 8 Fix findings, and the top 5 Ask findings. When findings are left out, the last line counts them, and "show all" lists the hidden findings along with the ones it filtered as low confidence or minor.

| Skill | Checks |
| --- | --- |
| `miko-review` | Picks the lenses, runs them, merges and filters findings |
| `review-truth` | Comments that lie, values copied into two places, asymmetric branches, stale references, untrusted input used as a path |
| `review-deep-modules` | Shallow modules, information leakage, and pass-through layers, from Ousterhout's *A Philosophy of Software Design* |
| `review-senior` | Scalability, maintainability, readability |
| `review-minimal` | Whether the change could be smaller, reinvented helpers, unneeded guards, tests that would pass without the change |
| `review-experience` | Options with no reason to exist, failures that leave the consumer stuck, actions with no feedback, work pushed onto the consumer |
| `review-verify` | Runs new or changed behaviour and reports what happened |

To give the lenses repo-specific context (helpers to reuse, owners, rules, how to run things), add a `REVIEW.md` at the repo root. See the [template](skills/miko-review/review-context-template.md).

To add your own instructions to one review skill without forking it, write an extension file named after the skill, such as `review-senior.md`. Extensions add checks and context. They cannot skip steps or relax rules, and the report lists every extension applied and every conflict.

| Layer | Path |
| --- | --- |
| Private, all your repos | `~/.config/miko-skills/<skill>.md` (symlink the directory to a private repo clone) |
| Project, committed | `.miko-skills/<skill>.md` |
| Local, this machine | `.miko-skills/local/<skill>.md` (keep it out of git with the command in [extensions.md](skills/miko-review/extensions.md)) |

[extensions.md](skills/miko-review/extensions.md) has the full rules and an example.

The other skills are not part of review:

| Skill | Use it for |
| --- | --- |
| `skill-examples` | Indexes six public skill repos (Matt Pocock's skills, Superpowers, pstack, gstack, ECC, Callstack's software factory). The agent reads and cites them when searching for an existing skill, writing a new one, or reviewing one. |
| `humanize` | Removes AI writing patterns from technical prose: PR descriptions, docs, code comments, reports |
| `unslop` | Removes AI writing patterns from casual prose: chat, Slack, email, social posts |
| `benchmark-reviewers` | Runs `miko-review` and other reviewers (CodeRabbit, Cursor, Claude Code, OpenCode) on the same PR, has a blinded judge check every finding against the code, and proposes rule changes for what `miko-review` missed. Run `/benchmark-reviewers <PR>`. |
| `give-feedback` | Drafts a PR comment or thread reply from a finding, revises it with you, and posts it with `gh` only after you say "post it". |
| `simple-explain` | Explains a concept, code, a review finding, or a decision in plain words with one example. Run `/simple-explain <topic>`, optionally with `normal` or `deep` for more detail. |

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

Every lens except `review-verify` only reads code. Cursor enforces that with `readonly`, and OpenCode with `permission: edit: deny`. In Claude Code they have no edit or write tools, but Bash can still write files, so permission prompts are the real guard.

## Contributing

[AGENTS.md](AGENTS.md) has the rules for keeping all three harnesses working and the checks to run before committing.
