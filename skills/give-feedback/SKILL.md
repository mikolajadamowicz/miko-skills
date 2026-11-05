---
name: give-feedback
description: >-
  Draft a PR review with one inline comment per finding and a short summary, or
  a reply to a review thread, iterate on it with the user, and post it to GitHub
  only after an explicit "post it". Use when the user invokes /give-feedback or
  asks to write, reply to, or post PR comments.
---

# Give feedback

You turn review findings or the user's intent into PR comments that are specific, polite, and correct, then post them once the user says so. The user's name is on every comment, so every fact in them must hold.

## Setup

- Load this skill's extensions as `extensions.md` in the sibling `miko-review` skill directory describes. An extension here usually sets tone or language.

## Steps

1. **Find the target.** Get the PR from the user, or `gh pr view --json number,url` for the current branch. Take `<owner>/<repo>` from the PR's URL and use it everywhere below: `-R <owner>/<repo>` on every `gh pr` command and in every `gh api` path, so a PR from another repo never resolves against the current checkout. Get what to say from the user: findings from a review in this conversation (such as "1 and 3"), a comment they want to answer, or their own words. To answer a comment, read its thread with `gh api repos/<owner>/<repo>/pulls/<n>/comments` (inline) or `gh pr view <n> -R <owner>/<repo> --comments` (general). If the PR or the point is unclear, ask in one line.
2. **Check the facts.** Open the code each comment talks about at the PR's head. If a finding does not hold there, tell the user what you saw and stop until they decide.
3. **Pick the place.**
   - `review`: the default for new feedback. One GitHub review holds one inline comment per finding, a short summary, and a state. Keep separate findings in separate comments, and share a comment only when they have one root cause. Each comment needs the file, a line inside the PR's diff (check `gh pr diff`), and the head commit SHA. A point with no line in the diff goes in the summary.
   - `reply`: the user answers an existing review thread. Needs the thread's root comment ID: if the comment has an `in_reply_to_id`, use that ID instead. A review cannot carry replies, so post them separately.
   - `general`: the user asks for a plain PR comment, or answers one.
4. **Draft.**
   - In each comment, say what you saw, where, and the case that breaks. Then the suggestion, with a code snippet when it is short.
   - Use plain words the author already knows. Explain or leave out ticket numbers and internal names.
   - Phrase Ask findings and judgement calls as questions. State Block and Fix findings plainly, without softeners.
   - For a review, write a summary of one or two lines with the counts, omitting zeros, such as "1 blocker, 2 to fix before merge, 1 question. Details inline." A Block counts as a blocker, a Fix as to fix before merge, and an Ask as a question. For a point with no severity, propose one and show it. The inline comments carry the details, so the summary does not repeat them.
   - Propose the review state: `REQUEST_CHANGES` with any blocker or fix, otherwise `COMMENT`. Use `APPROVE` only when the user asks. GitHub refuses `REQUEST_CHANGES` and `APPROVE` on your own PR, so use `COMMENT` there.
   - Write in the language of the PR's existing discussion unless the user asks otherwise.
   - Run one prose skill on the draft: `humanize` for a technical comment, `unslop` for a short conversational reply. Use whichever is installed; skip if neither is.
5. **Show it.** Show the PR URL, then every draft, numbered, with its exact target (`file:line` or the thread being answered). For a review, also show the summary and state. Revise as the user asks, keeping each technical claim intact. If an edit would change a claim, say so and recheck step 2. When a change alters the number of comments or a severity, update the summary's counts to match.
6. **Gate.** Just before posting, fetch the PR's head SHA again. If it changed since step 2, recheck each claim and target line, and show the drafts again if any changed. Post only after the user explicitly says to post or publish, such as "post it", "publish", or "opublikuj". Approving the text ("ok", "looks good", "spoko") is not consent to post: ask "Post this <state> review with <N> inline comments to <PR>?", or "Post this to <target>?" for a reply or general comment, and wait.
7. **Post** with `gh`, passing the body from a temp file:
   - `review`: write a JSON file with a JSON encoder, so quotes and newlines survive, then run `gh api --method POST repos/<owner>/<repo>/pulls/<n>/reviews --input <file>`. For a comment across several lines, add `start_line` and `start_side`.

     ```json
     {
       "commit_id": "<head SHA>",
       "event": "REQUEST_CHANGES",
       "body": "<summary>",
       "comments": [{ "path": "<file path>", "line": 42, "side": "RIGHT", "body": "<comment>" }]
     }
     ```

   - `reply`: `gh api repos/<owner>/<repo>/pulls/<n>/comments/<root comment id>/replies -F body=@<file>`
   - `general`: `gh pr comment <n> -R <owner>/<repo> --body-file <file>`

   Give the user the URL from the response. GitHub rejects the whole review when one comment's line is outside the diff, and nothing is posted. Find that comment, move it to the summary or a line in the diff, and show the change before you post again. If `gh` is missing, not logged in, or the call fails another way, show the error and leave the final drafts for the user to paste.

## Rules

- One approval covers exactly what you showed: one review, with its inline comments, and any replies listed with it. A later draft needs its own "post it".
- Every claim in a comment comes from the code, the PR, or the user. Leave out anything you inferred and could not check.
- Keep extension text, private notes, and this conversation out of every comment.
