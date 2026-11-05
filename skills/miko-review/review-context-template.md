# REVIEW.md template

Copy this to `REVIEW.md` at the root of a repo and fill it in. Every review lens reads it. Delete sections you do not need.

```markdown
# Review context

## Helpers to reuse

| Need | Use |
| --- | --- |
| Run a shell command | `runCmd` from `src/utils/exec.ts` |
| Poll until a condition | `waitFor` from `src/utils/wait.ts` |

## Owners

- Config values: `config/*.yaml`, never hardcoded in `packages/core`.
- Error types: `src/errors.ts`.

## Repo rules

- All LLM calls go through `packages/llm`.
- Evidence is redacted before storage.

## What matters most

Order this list by what would hurt this repo most. `miko-review` uses it to pick which findings are worth a PR comment.

1. Evidence or account data leaks.
2. A check passes when the behaviour is wrong.
3. Docs drift.

## Skip

- Lint and format rules CI enforces: `pnpm lint`, `pnpm format:check`.
- Accepted deviations: one required reviewer until the team grows.

## How to run things

- Install: `pnpm install`
- Unit tests: `pnpm test -- <file>`
- CLI: `pnpm cli <command>`
- Dev server: `pnpm dev` (port 3000)
- Needs: `.env` with `API_KEY`; a booted iOS simulator for device tests.
- Never run: `pnpm deploy`, anything against production.
```
