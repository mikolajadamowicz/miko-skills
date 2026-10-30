---
name: review-minimal
description: >-
  Review lens that asks whether the diff is the smallest change that does the
  job: speculative branches and options, ride-along work, reinvented helpers,
  duplicated rules across layers, defensive guards the call site does not need,
  and tests that would not fail if the change were reverted. Run by the review
  skill, or on its own when the user asks whether a change could be smaller or
  reuse more.
---

# Review lens: minimal change and reuse

Less code, one owner per rule, reuse what exists, delete what the change supersedes. Most findings in this lens come from knowing what already exists next to the change, so open the callers, siblings, and shared utilities of every hunk before judging it.

## Setup

- If the `miko-review` skill started you, it gave you the repo, base ref, and paths to `finding-format.md` and maybe `REVIEW.md`.
- If you run on your own, get the diff with `git diff $(git merge-base origin/HEAD HEAD)...HEAD` plus `git diff HEAD`, read `REVIEW.md` at the repo root if it exists, and use the finding format in `finding-format.md` inside the sibling `miko-review` skill directory.
- Read only. Do not edit files.

## Checks

### 1. Smallest change

Count the lines that implement the behaviour against the total diff. If the core is a small fraction, propose the smaller shape with a target size.

- **Speculative branches**: code for situations nobody has run or asked for. Prefer reading live state over guessing which stored value applies.
- **Speculative options**: new env vars, config knobs, opt-outs, or compatibility fallbacks nobody requested.
- **Ride-along work**: renames, moves, and cleanups unrelated to the change.
- **Unpaid seams**: a new abstraction, wrapper, type, option, export, or dependency with no reader, or with a path production never reaches.
- **Missing deletions**: the code this change supersedes is still there.

### 2. Reuse before you write

For every new utility, grep for an existing one first: wait and poll loops, subprocess wrappers, HTTP helpers, path and string helpers, error types, parsers, constants. If `REVIEW.md` lists helpers, check each new function against it.

- Two functions doing the same job become one.
- A private wrapper around a shared helper should call the shared one directly or extend it.
- A new shared helper waits for a third call site.
- One value read twice (a presence check and then an inspect of the same thing) should be one read.
- A copy of a shared module is a fork. Restore the shared one.

### 3. One owner per rule

State the rule the diff enforces, then find the one place that should enforce it.

- The same check in two layers (the CLI and the server both refuse the same input) is one too many. Keep it at the owner.
- Hand-maintained lists of names that mirror a registry should be derived from the registry.
- Every entry point obeys the rule: direct calls, batch or replayed calls, fallback routes, and overrides.

### 4. Guards the call site does not need

- `try/catch` that swallows, an empty `catch {}`, `?? fallback` for a value that is always set, `if (!x) return` for an impossible state.
- Unchecked casts (`as X`) instead of a narrowing check that throws.
- Branching on `error.message` text instead of a typed code.
- A guard that exists must fail closed: refuse, keep state, redact.

### 5. Tests that discriminate

- Each new test must fail if the production change were reverted. Name the line whose revert breaks it.
- Tests of the platform or library instead of your code do not count.
- Near-identical tests should be one table-driven test.
- Fakes should fail the way production fails. Asserting "not called" needs the fake's call log checked.
- Junk: rejects-assertions with no predicate, mocks asserting their own inputs, expectations computed by the helper under test.

## Severity guide

- **Block**: a duplicated source of truth that already disagrees; a guard that fails open; a branch nobody can reach that hides a bug.
- **Fix**: reinvented helpers, duplicate enforcement, unpaid seams, non-discriminating tests.
- **Ask**: "could this be smaller?" proposals. Phrase them as questions.

Return findings with `lens: minimal` and `check:` set to the check name above. For check 1, include a summary line even with no other findings: either the proposed cut with core lines versus total, or "I looked for a smaller design and found none."
