---
name: review-senior
description: >-
  Review lens for scalability, maintainability, and readability, with concrete
  checks for each: growth and concurrency behaviour, coupling, testability,
  error handling, naming, comment density, and control flow. Run by the review
  skill, or on its own when the user asks for a senior-dev review of
  scalability, maintainability, or readability.
---

# Review lens: scalability, maintainability, readability

Review as a senior engineer who will own this code for the next two years. Every finding must point at a line and name a concrete cost: what breaks at what size, what change becomes expensive, or what a reader will misread. "Could be cleaner" is not a finding.

## Setup

- If the `miko-review` skill started you, it gave you the repo, base ref, and paths to `finding-format.md` and maybe `REVIEW.md`.
- If you run on your own, get the diff with `git diff $(git merge-base origin/HEAD HEAD)...HEAD` plus `git diff HEAD`, read `REVIEW.md` at the repo root if it exists, and use the finding format in `finding-format.md` inside the sibling `miko-review` skill directory.
- Read only. Do not edit files.

## How

Read every touched hunk and its callers. For scalability, estimate the realistic size of the inputs from how the code is called (one config file, a page of results, every row in a table, every device in a fleet) and judge against that, not against infinity.

## Scalability

1. **Work that grows with input.** Nested loops over the same collection, repeated `find`/`includes` inside a loop, sorting inside a loop, re-reading a file or re-parsing per item. Name the input that makes it slow.
2. **N+1 calls.** A network, database, subprocess, or filesystem call inside a loop that could be one batched call.
3. **Unbounded growth.** Lists, caches, maps, logs, or buffers that only grow; reading a whole file or response into memory when it can be large; pagination that is ignored.
4. **Missing limits on external calls.** No timeout, no retry limit, retries without backoff, polling without a deadline, no cancellation.
5. **Concurrency.** Shared mutable state across async tasks, check-then-act races on files or records, unbounded `Promise.all` over a large list, missing locks or idempotency where two runs can overlap.
6. **Blocking the hot path.** Synchronous filesystem or CPU-heavy work in a request handler, event loop, or UI thread.

## Maintainability

7. **Coupling.** A module that reaches into another's internals, imports across a layer boundary, or depends on a concrete implementation where the rest of the codebase uses an interface.
8. **Change amplification.** A likely future change (a new platform, a new field, a new command) would need edits in several places. Name the change and the places.
9. **Testability.** Logic that cannot be tested without the network, the clock, the filesystem, or a global, when it could take them as arguments. Hidden dependencies through module-level singletons.
10. **Error handling.** Swallowed errors, `catch` that logs and continues when the caller needed to know, errors that lose their cause or context, string matching on error messages instead of typed codes.
11. **Consistency with the codebase.** The diff solves a problem differently from how the surrounding code solves the same problem (a different HTTP client, logger, config loader, error type). Check `REVIEW.md` and neighbouring files.
12. **Dead and duplicate code.** Unused exports, parameters, branches, and feature flags; code copied from elsewhere instead of shared.

## Readability

13. **Names.** A name that says what it is for, at the level of the domain. Booleans read as questions (`isReady`). No abbreviations the codebase does not already use. One name per concept across the diff.
14. **Function size and nesting.** A function that does several jobs, or nests more than about three levels. Suggest the split by job, not by line count.
15. **Control flow.** Early returns over deep `else` chains; no flag variables that steer a later branch; no clever one-liners that need a second read.
16. **Comments.** Comments should state constraints the code cannot show. Flag comments that narrate the next line, restate the signature, or describe review history. Flag a diff where a large share of new lines are comments.
17. **Magic values.** Unnamed numbers and strings whose meaning is not obvious from context.

## Severity guide

- **Block**: a scalability or concurrency problem that will fail at the input sizes the code already sees; a swallowed error that hides a failure from the user.
- **Fix**: coupling, change amplification, untestable logic, missing timeouts, inconsistent patterns, dead code.
- **Ask**: naming, function size, and readability preferences.

Return findings with `lens: senior` and `check:` set to the check name above (for example `N+1 calls`, `Coupling`, `Names`).
