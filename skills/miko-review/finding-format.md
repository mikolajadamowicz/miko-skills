# Finding format

Every review lens returns its findings in this format, so the `miko-review` skill can merge them. Put the `Extensions` and `Conflicts` lines from [extensions.md](extensions.md) first.

```
- file: <path>:<line or line range>
  lens: <the value your lens's SKILL.md gives>
  check: <the check's name from the lens>
  severity: <Block | Fix | Ask>
  confidence: <0-100>
  problem: <what is wrong, with the concrete scenario that triggers it>
  fix: <the change that would satisfy the check, at the site that owns the rule>
```

## Severity

- **Block**: merging this causes a bug, a security problem, data loss, a lie to the user, or a wrong comment that will mislead the next edit.
- **Fix**: should change before merge, but nothing breaks today: drift risk, a stale doc, an asymmetric branch, a leaky interface.
- **Ask**: a judgement call or convention question. Phrase it as a question.

## Confidence

How sure you are that the problem is real, not how bad it is.

- **90-100**: you read the code path and can name the input that breaks it, or you ran it.
- **70-89**: the problem follows from code you read, but depends on a caller or config you did not fully trace.
- **Below 70**: a hunch. Report it only if the prompt or the user asks for every finding.

## Rules

- Cite a real `file:line` from the current head. No finding without a location.
- Describe the scenario, not the category. "A tip with `../` reaches `join(dir, name)` at `fetch.ts:42`", not "possible path traversal".
- When a problem shows up at several call sites, report one finding at the owner, listing the sites.
- Return at most 12 findings, unless the prompt or the user asks for every finding. Keep every Block, then the highest-confidence Fix and Ask findings, and add one line saying how many you left out.
- Skip what a linter or formatter would catch, and style preferences with no scenario where they cause harm.
- A rule in `REVIEW.md` or a repo rule file (listed under "Repo rule files" in the `miko-review` skill) that the diff breaks is a finding. Name the file and rule in `check`, for example `check: CONTRIBUTING.md: resolve paths before fs calls`.
- If you found nothing, return `No findings.` and the checks you ran.
