---
name: write-pr
description: >-
  Write a pull request title and description that follows the target repo's PR
  template, or a What and Why when it has none, each opening with a plain
  bird's-eye summary a person gets on the first read. Use when the user invokes
  /write-pr or asks to write, draft, or update a PR description.
---

# Write PR

Write the title and description for a pull request. A reviewer reads the first two sentences and knows what changed and why; the rest is there for when they want the detail.

## Setup

- Load this skill's extensions as `extensions.md` in the sibling `miko-review` skill directory describes. An extension here usually sets language, title format, or ticket links.

## Steps

1. **Gather the change.** Find the base branch: the one the user names, the existing PR's base (`gh pr view --json baseRefName,number,url`), or the repo's default branch (`gh repo view --json defaultBranchRef`, or `git symbolic-ref refs/remotes/origin/HEAD`). Read `git log <base>..HEAD`, `git diff <base>...HEAD`, the linked issue or ticket (from the branch name, commits, or the user), and what this conversation says about the work. Done when every change in the diff is either placed under a point you will write or set aside as noise (lockfile churn, formatting).
2. **Find the reason.** Take the why from the issue, the commits, or the conversation. When none of them says why, ask the user in one line and wait. Every claim in the description comes from the diff, the issue, or the user.
3. **Find the template** in the repo the PR targets. Check, case-insensitively: `.github/pull_request_template.md`, `pull_request_template.md` at the root, `docs/pull_request_template.md`, and the files in `.github/PULL_REQUEST_TEMPLATE/`. With several templates, pick the one whose name fits the change (bugfix, feature, release); if none clearly fits, list them and ask. For a PR into another repo, such as a fork's upstream, read the template from that repo with `gh api repos/<owner>/<repo>/contents/<path>`.
4. **Write the overviews.** Two pairs of sentences, each written bird's-eye: for a teammate who has never opened this code, in everyday words, about what changes for the people or systems involved.
   - **What overview**, 1–2 sentences: the essence of the change.
   - **Why overview**, 1–2 sentences: the problem or need behind it, and who it affects.
   - Keep file names, function names, versions, and jargon for the details below them. Test: a product manager reads the four sentences and can explain the PR to someone else.
5. **Write the body.**
   - **With a template:** keep its headings, order, and checklists. Open the section that describes the change (Summary, Description, What, Changes) with the What overview, and the section that explains motivation (Why, Context, Motivation) with the Why overview. When the template has no motivation section, put the Why overview right after the What overview. Fill every other section from what you gathered, and write "N/A" in a section that does not apply. Follow the template's HTML comments, then delete them. Tick a checkbox only for something you checked.
   - **Without a template:** use this shape.

     ```markdown
     ## What

     <What overview>

     - <one concrete change per bullet: "Bumped X from 1.2 to 1.4", "Moved retry logic from A to B">

     ## Why

     <Why overview>

     <the details: root cause, constraints, trade-offs, options you ruled out, links>
     ```

   - Bullets under What carry the technical detail: names, files, old → new values. One change per bullet, in the order a reviewer should read them.
   - Leave out sections the template does not ask for, such as a testing section, unless the user wants one.
6. **Write the title.** Follow the convention in the repo's recent PR titles or commits (Conventional Commits, ticket prefix); otherwise a short plain sentence in the imperative, under 70 characters, that says what the PR does.
7. **Polish.** Run `humanize` on the prose if it is installed. Write in the language of the repo's existing PRs unless the user asks otherwise.
8. **Show it.** Show the title and the body in one Markdown block the user can copy. Revise as the user asks. Create or update the PR on GitHub only when the user says so: `gh pr create --title <title> --body-file <file>` or `gh pr edit <n> --body-file <file>`, with the body in a temp file, then give the user the URL.
