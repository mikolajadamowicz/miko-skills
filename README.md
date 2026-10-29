# miko-skills

Agent skills for code review.

| Skill | What it does |
| --- | --- |
| `review` | Runs the lenses below as parallel subagents, merges their findings, reports in chat |
| `review-truth` | True comments, one owner per fact, symmetric branches, stale references, untrusted input |
| `review-deep-modules` | Ousterhout's *A Philosophy of Software Design*: shallow modules, leakage, pass-throughs |
| `review-senior` | Scalability, maintainability, readability |
| `review-minimal` | Smallest change, reuse existing helpers, no unneeded guards, discriminating tests |
| `review-verify` | Runs new or changed behaviour and reports the observed output |

Install all of them together; `review` and the lenses read each other's files.

## Install

The rules live only in `skills/`. The subagents in `agents/` are thin wrappers that load the matching skill and add a model and read-only tools. One agent file serves both harnesses: Cursor reads `readonly`, Claude Code reads `tools` and preloads the skill through `skills`. Without the agents, `review` starts general-purpose subagents that read the same skills.

Pick one route per harness. Installing the same skills twice (plugin plus `npx skills`) loads them twice.

**Any agent, skills only** (Vercel `skills` CLI):

```bash
npx skills add mikolajadamowicz/miko-skills -g                  # agents it detects
npx skills add mikolajadamowicz/miko-skills -g -a claude-code   # or name one
```

**Claude Code plugin** (skills and agents):

```
/plugin marketplace add mikolajadamowicz/miko-skills
/plugin install miko-skills@miko-skills
```

For local development: `claude --plugin-dir path/to/miko-skills`.

**Cursor plugin** (skills and agents): copy the repo into `~/.cursor/plugins/local/miko-skills` (Cursor skips symlinks there) and reload the window.

**Skills CLI plus agents from a clone:**

```bash
scripts/install-agents.sh                      # ~/.claude/agents: Claude Code, and Cursor through its .claude/agents support
scripts/install-agents.sh --cursor             # ~/.cursor/agents
scripts/install-agents.sh --all path/to/repo   # both, inside a project
```

Re-run the script after pulling changes to `agents/`.

### Models

Every agent uses `model: inherit`. To pin one, edit `model:` in the installed copy. The values differ by harness: Cursor takes a model ID with options (`claude-opus-5[effort=high]`), Claude Code takes `opus`, `sonnet`, `haiku`, or a full model ID.

### Read-only in Claude Code

The four reading agents get `Read, Grep, Glob, Bash`. Without `Edit` and `Write` they cannot edit files directly, but Bash can still write. The skills tell them not to; Claude Code's permission prompts are the enforcement.

Add a `REVIEW.md` to a repo to give the lenses its helpers, owners, rules, and run commands. See [skills/review/review-context-template.md](skills/review/review-context-template.md).
