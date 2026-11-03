# Public review datasets

Open datasets of PRs with known findings ("golden" findings). Use them to measure how many real issues `miko-review` finds (recall) and how much noise it adds (precision), instead of only comparing it with other reviewers. Checked 2026-11-03.

All three are MIT-licensed. Their PRs come from public projects that may be in a model's training data, so a high score on a well-known PR can be memory. Prefer recent PRs and treat a single run as a signal.

| Dataset | Size | Golden findings | Best for |
| --- | --- | --- | --- |
| [GitHub ReviewBench](https://github.com/review-bench/ReviewBench) | 25-PR test set, 219 PRs in full | Human-reviewed, with file, line range, severity, and category | Default choice: many languages and repos, exact SHAs |
| [Martian Code Review Bench](https://github.com/withmartian/code-review-benchmark) (offline) | 50 PRs from 5 large repos | 173 human-verified comments with severity and category, no line numbers | Large codebases where reuse and ownership are hard to see |
| [KyleSau/reviewbench](https://github.com/KyleSau/reviewbench) | 25 small diffs, 6 of them clean | 21 seeded bugs with file and line | False positives on clean PRs |

## GitHub ReviewBench

- Each file in `golden/` is one PR: `pr.repo`, `pr.pr_number`, `pr.base`, `pr.head`, and `findings[]` with `file`, `start_line`, `end_line`, `message`, `severity`, `category`, and `tp_fp`. Only findings with `tp_fp: "tp"` count as real issues.
- The test set is listed in `corpus/test/test.json`. The full set is `corpus/manifest.json`.
- Clone the repo from `pr.repo`, or from its mirror `review-bench/<owner>_<repo>` if the original is gone. Both hold the base and head commits.
- The repo's own judge (`npm run judge`) scores findings in its JSON format. The format is in `AGENT_CONTRACT.md`.

## Martian Code Review Bench

- Golden comments live in `offline/golden_comments/<repo>.json`, one file per project (`sentry`, `grafana`, `keycloak`, `discourse`, `cal_dot_com`). Each entry has `pr_title`, `url`, and `comments[]` with `comment`, `severity`, and `category`.
- `url` points to the PR in a fork under `ai-code-review-evaluation`. Get base and head from `gh pr view <url> --json baseRefOid,headRefOid`.
- Comments have no file or line, so the judge matches on the described problem.
- Score with the `core` categories (bug, security, concurrency, data, api, perf, test_gap, doc_defect). The `style` and `speculative` comments are sparse.

## KyleSau/reviewbench

- Cases are unified diffs in `datasets/v1/cases`, not repos. Lenses that read callers or run code (`review-verify`, most of `review-minimal` and `review-deep-modules`) have nothing to work with, so use it mainly to count findings on the 6 clean PRs.
- Its CLI (`reviewbench run`, `reviewbench gate`) runs its own reviewers. Running `miko-review` means applying each diff to an empty git repo first.

## Not included

- Factory's `droid-code-review-evals/review-droid-benchmark` has a validated v3 golden set for the same 50 PRs as Martian, but the repo has no license.
- [AACR-Bench](https://github.com/alibaba/aacr-bench) (Apache-2.0, 200 PRs) is open, but most of its golden comments are LLM-generated and then checked by engineers.
- hyperneolabs/review-bench has no data yet.
