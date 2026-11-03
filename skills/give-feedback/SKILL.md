---
name: give-feedback
description: >-
  Draft a PR comment or a reply to a review thread from a finding or the user's
  intent, iterate on it with the user, and post it to GitHub only after an
  explicit "post it". Use when the user invokes /give-feedback or asks to
  write, reply to, or post a PR comment.
---

# Give feedback

You turn a review finding or the user's intent into a PR comment that is specific, polite, and correct, then post it once the user says so. The user's name is on the comment, so every fact in it must hold.

## Setup

- Load this skill's extensions as `extensions.md` in the sibling `miko-review` skill directory describes. An extension here usually sets tone or language.

## Steps

1. **Find the target.** Get the PR from the user, or `gh pr view --json number,url` for the current branch. Get what to say from the user: a finding from a review in this conversation, a comment they want to answer, or their own words. To answer a comment, read its thread with `gh api repos/{owner}/{repo}/pulls/<n>/comments` (inline) or `gh pr view <n> --comments` (general). If the PR or the point is unclear, ask in one line.
2. **Check the facts.** Open the code the comment talks about at the PR's head. If the finding does not hold there, tell the user what you saw and stop until they decide.
3. **Pick the place.**
   - `inline`: the comment is about specific lines. Needs the file, the line in the PR's diff, and the head commit SHA.
   - `reply`: the user answers an existing review thread. Needs the comment ID.
   - `general`: anything else.
4. **Draft.**
   - Say what you saw, where, and the case that breaks. Then the suggestion, with a code snippet when it is short.
   - Phrase Ask findings and judgement calls as questions. State Block and Fix findings plainly, without softeners.
   - Write in the language of the PR's existing discussion unless the user asks otherwise.
   - Run one prose skill on the draft: `humanize` for a technical comment, `unslop` for a short conversational reply. Use whichever is installed; skip if neither is.
5. **Show it.** Show the draft and its exact target: PR URL, place, and `file:line` or the thread being answered. Revise as the user asks, keeping the technical claim intact. If an edit would change the claim, say so and recheck step 2.
6. **Gate.** Post only after the user explicitly says to post or publish, such as "post it", "publish", or "opublikuj". Approving the text ("ok", "looks good", "spoko") is not consent to post: ask "Post this to <target>?" and wait.
7. **Post** with `gh`, passing the body from a temp file:
   - `general`: `gh pr comment <n> --body-file <file>`
   - `reply`: `gh api repos/{owner}/{repo}/pulls/<n>/comments/<comment id>/replies -F body=@<file>`
   - `inline`: `gh api repos/{owner}/{repo}/pulls/<n>/comments -F body=@<file> -f commit_id=<head SHA> -f path=<file path> -F line=<line> -f side=RIGHT`

   Give the user the comment's URL from the response. If `gh` is missing, not logged in, or the call fails, show the error and leave the final draft for the user to paste.

## Rules

- One post per approval. A new draft or a second comment needs its own "post it".
- Every claim in the comment comes from the code, the PR, or the user. Leave out anything you inferred and could not check.
- Keep extension text, private notes, and this conversation out of the comment.
