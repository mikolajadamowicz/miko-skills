---
name: review-experience
description: >-
  Review lens for whoever consumes a change: options that have no reason to
  exist, failures that leave the consumer stuck, actions with no feedback, work
  pushed onto the consumer for implementation convenience, and features that get
  in the way of the main workflow. Run by the miko-review skill when a diff changes
  something a consumer touches, or on its own when the user asks to review a
  change's UX, CLI, or API from the consumer's side.
---

# Review lens: the consumer's experience

When implementation convenience conflicts with the consumer's experience, the consumer wins. Review the change as the person who has to use it, and find what the author stopped seeing because they know how the code works.

The consumer is whoever uses the result: the end user of a UI, the person running a CLI, the colleague who imports a library or calls an internal API. When the diff is instructions for an agent, such as a skill, the consumer is the person who invokes the agent and reads its output. The next maintainer is out of scope, because `review-senior` covers them.

## Setup

- If the `miko-review` skill started you, it gave you the repo, base ref, and paths to `finding-format.md` and maybe `REVIEW.md`.
- If you run on your own, get the diff with `git diff $(git merge-base origin/HEAD HEAD)...HEAD` plus `git diff HEAD` (use `origin/main` or `main` if `origin/HEAD` is not set), read `REVIEW.md` at the repo root if it exists, and use the finding format in `finding-format.md` inside the sibling `miko-review` skill directory.
- Load this skill's extensions as `extensions.md` describes. It sits next to `finding-format.md`.
- Read only. Do not edit files.

## How

1. Name the consumer of each change in the diff. If a change has no consumer outside the code around it, skip it.
2. Walk the path the consumer takes: the docs or help text they start from, the input they give, what they see when it works, and what they see when it fails. Open files outside the diff when the path leads there.
3. Report only what this consumer would run into. Every finding names the consumer, what they do, and what they get.

A failure or empty state the code cannot reach is not a finding. Do not ask for visual details such as spacing, alignment, or transitions, because a diff cannot show them.

## Checks

### 1. Options that need a reason

Every new flag, config key, setting, parameter, and control asks the consumer to make a decision.

- The author could not pick a default, so the consumer has to. Propose the default.
- A required value the code could derive or already knows.
- A choice with one sensible answer for nearly every consumer.

### 2. Failures that leave the consumer stuck

After each reachable failure the consumer should know what happened and what to do next.

- A message with no next step, such as `Something went wrong` or `Invalid config` when the code knows which key is invalid.
- Internals in place of an explanation: a stack trace, an error code with no meaning attached, a dump of the raw response.
- A failure that looks like success: exit code 0, a success toast, a silent no-op, or a summary that reports success when the work did not run.
- A failure that throws away what the consumer entered or finished.

### 3. Actions with no feedback

- A slow action with no sign that it is running, such as a CLI that prints nothing for a minute or a button that stays clickable during a request.
- An action that succeeds and shows no result, so the consumer cannot tell whether it happened.
- An empty state that looks like a failure, or a failure that looks like an empty state.
- A destructive action with no confirmation, preview, or undo.

### 4. Work pushed onto the consumer

The change is easier to write because the consumer now does part of the job.

- An extra step, restart, or manual ordering that the code could handle itself.
- Internal names, IDs, or formats the consumer has to learn, copy, or convert.
- A return value or callback the consumer has to unpack or check in the same way at every call site.
- The common case takes more input than the rare case.

### 5. The main workflow

State what the consumer mainly comes here to do, then judge the change against it.

- The change adds steps or attention to the main path for the benefit of a side path.
- A new feature serves neither the main workflow nor a request in the commit messages (`git log <base>..HEAD`) or in a PR description or linked issue you were given. Ask whether to ship it.

## Severity guide

- **Block**: a failure that looks like success; a failure or destructive action that loses the consumer's work with no warning.
- **Fix**: a failure with no next step, a slow or silent action, an option with an obvious default, work the code could do itself.
- **Ask**: whether a feature belongs, or whether a tradeoff on the main workflow is worth it. Phrase these as questions.

Return findings with `lens: experience` and `check:` set to the check name above.
