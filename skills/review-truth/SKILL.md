---
name: review-truth
description: >-
  Review lens that checks whether a diff tells the truth and keeps one owner
  per fact: comments verified against source, preexisting bugs in touched
  hunks, copied values that can drift, user-facing text that names the real
  source, symmetric branches, stale references to old values, untrusted input
  parsed before use. Run by the review skill, or on its own when the user asks
  to fact-check a diff or hunt for drift.
---

# Review lens: truth and ownership

You are not looking for style. You are looking for comments that lie, values that live in two places, messages that name the wrong source, branches that disagree, and untrusted strings that become paths.

## Setup

- If the `review` skill started you, it gave you the repo, base ref, and paths to `finding-format.md` and maybe `REVIEW.md`.
- If you run on your own, get the diff with `git diff $(git merge-base origin/HEAD HEAD)...HEAD` plus `git diff HEAD`, read `REVIEW.md` at the repo root if it exists, and use the finding format in `finding-format.md` inside the sibling `review` skill directory.
- Read only. Do not edit files.

## How

1. Read every touched hunk in full: the whole function, not only the changed line.
2. Run the checks below on each hunk.
3. After the hunks, grep the repo for every old value, name, and path the diff replaced.

## Checks

### 1. Comments must be true

A comment that justifies a change gets verified against the current source, docs, or tool behaviour. Open the code it describes. A wrong comment is worse than none: it talks the next editor into deleting the wrong thing.

Includes docstrings, commit-message claims repeated in code, and comments on unchanged lines whose meaning the diff changed.

### 2. You own the hunk

Touching a line makes the surrounding function yours. Preexisting bugs in it are in scope: the error string with the wrong filename, the other branch of the `if`, the unhandled failure path. The review tool attaches comments to the lines you edited, so that is where they get found.

### 3. One fact, one owner

A value that appears in more than one place (a version, URL, field id, limit, label, sort key, list of allowed names) must either:

- have two clearly different jobs, named as such (an exact pin versus a minimum floor), or
- have a test or codegen step that fails when the copies drift.

Otherwise it gets one owner and every other site reads from it. A sort key counts as a fact too: `name-<semver>-<id>` sorts by semver, then id, not by the trailing number.

Repo-specific values (URLs, ids, labels) belong in config or adapters, not in shared core code. If `REVIEW.md` names owners, enforce them.

### 4. User-facing text cites the real source

Error messages, logs, CLI help, doctor or diagnostic output, and API responses must name the file or setting that actually supplied the value. Do not say "required by X" when the value comes from Y.

- A flag or field that is accepted must change the result or be rejected. Accepted and silently ignored is a lie.
- Commands shown in usage text or docs must run on a fresh clone.

### 5. Symmetric branches

If the success path strips a prefix, normalizes a path, redacts a field, or maps an error, the failure path does the same. Feed the realistic input shape (`v22.1.0`, a leading slash, an id with a prefix) through both branches.

Same check for: `--flag=value` versus `--flag value`, interactive versus non-interactive input, every request to the same host handling the same status code the same way, and a local write error not being reported as a network error.

### 6. Do not drop a guard other readers still use

Before accepting a deleted config key, step, field, or function, find every reader. Other tools, older versions, docs, and other packages may still look there.

The inverse is also a finding: a function whose only caller is its own test is dead. Delete both.

### 7. Grep the old value

For a rename, version bump, moved file, or rewritten CI step, search for the old string in tests, fixtures, README, docs, ADRs, comments, and scripts. Every hit is either updated or deliberately kept with a reason.

Install and run commands must resolve to the version you mean: `npm i -g tool` installs `latest`, not the version you pinned.

### 8. Write down the defaults you rely on

If the change depends on a default (timeout, retry count, model name, install behaviour, a tool's major-version behaviour), the default should be written in repo config with a note that it is the default and why it is pinned. The next upgrade must not flip it silently.

### 9. Parse, then trust

Untrusted input (CLI args, request fields, URLs, file contents, LLM output) becomes a path, filename, URL, command, or identifier only after a parse that rejects traversal, empty values, and the wrong shape. Downstream code uses only the parsed value.

Computing `parsed.folder` and then interpolating the raw `folder` is this check. So is `name: ../../tmp/x` reaching `join(dir, name)`.

### 10. Families are not a default member

A type or parameter that stands for a family (platform, device kind, provider) must not silently pick one member. Handle every variant or require the caller to choose. `tv` hardcoded to one TV platform makes the others unreachable.

### 11. Governance is literal

Ticket references must be real. A placeholder like `PROJ-TBD` is a placeholder, not done. No secrets, tokens, or personal data in code, fixtures, logs, or evidence.

## Severity guide

- **Block**: a wrong comment that will cause a bad delete; a user-facing lie; untrusted input reaching a path or command; a missing redaction; a secret; an invented ticket presented as real.
- **Fix**: drift risk, a stale fixture or doc, an asymmetric branch.
- **Ask**: a convention question where the repo is already inconsistent.

Return findings with `lens: truth` and `check:` set to the check name above.
