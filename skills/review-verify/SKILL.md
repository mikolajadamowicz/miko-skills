---
name: review-verify
description: >-
  Review lens that runs new or changed behaviour and reports what actually
  happened: finds what the diff makes executable, works out how to exercise it,
  runs it, and cites the output as evidence. Run by the review skill whenever
  the diff adds or changes behaviour, or on its own when the user asks to check
  that a change actually works.
---

# Review lens: verify by running

Reading code tells you what it should do. This lens finds out what it does. A claim is verified only by output you observed on the current head.

## Setup

- If the `review` skill started you, it gave you the repo, base ref, and paths to `finding-format.md` and maybe `REVIEW.md`.
- If you run on your own, get the diff with `git diff $(git merge-base origin/HEAD HEAD)...HEAD` plus `git diff HEAD`, read `REVIEW.md` at the repo root if it exists, and use the finding format in `finding-format.md` inside the sibling `review` skill directory.

## Safety

- Do not edit tracked files, commit, push, or change git state. Scratch files go in a temp directory and are deleted at the end.
- Do not run anything `REVIEW.md` lists under "never run", anything that deploys, publishes, or migrates, or anything that sends messages or touches production data.
- Do not invent credentials. If a run needs a secret or device that is missing, report "could not run" and what is missing.
- Bound every command with a timeout. Stop background processes (dev servers, watchers) you started before you finish.

## How

1. **List the behaviour.** From the diff, list each new or changed behaviour a user or caller can trigger: a command or flag, a function's new result, an endpoint, a UI state, a script, a CI step. Skip pure refactors unless the diff claims they preserve behaviour; then verify that claim.
2. **Find how to run it.** In order: `REVIEW.md` "how to run things", `package.json` scripts / `Makefile` / `justfile` / `pyproject.toml`, the README, CI config, existing tests that already exercise the area.
3. **Plan the smallest run that reaches the changed branch.** Prefer, in order:
   - an existing test that covers the branch (run only that file or case)
   - the real entry point: the CLI command, the script, a request to a locally started server
   - a throwaway script in a temp directory that imports the changed function and calls it
   
   For each run, name the changed line it is meant to reach. A run that never reaches the changed code verifies nothing.
4. **Run the happy path and at least one edge.** The edge comes from the diff: the new error branch, the empty input, the flag in its other form, the boundary value.
5. **Compare with what the diff claims.** The PR description, commit messages, docs, help text, and comments say what should happen. Note any mismatch.
6. **If an existing test suite covers the area,** run that suite's affected files too and report failures.

## Report

Return one entry per behaviour:

```
- behaviour: <what was checked>
  reaches: <file>:<line> of the changed code
  command: <exact command>
  result: works | broken | could not run
  evidence: <the relevant lines of output, trimmed>
```

Then return findings in the shared finding format for every `broken` result and every mismatch between claimed and observed behaviour, with `lens: verify`. Confidence is 90 or higher only when you observed the failure yourself. A `could not run` is not a finding unless the diff has no way to be run at all, which is an Ask.

If the diff has no behaviour to run, return `Nothing to run:` and one line saying why.
