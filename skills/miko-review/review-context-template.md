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

## How to run things

- Install: `pnpm install`
- Unit tests: `pnpm test -- <file>`
- CLI: `pnpm cli <command>`
- Dev server: `pnpm dev` (port 3000)
- Needs: `.env` with `API_KEY`; a booted iOS simulator for device tests.
- Never run: `pnpm deploy`, anything against production.
```
