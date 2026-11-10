---
name: simple-explain
description: >-
  Explain something in plain words with a concrete example: a concept, code, a
  review finding, a design decision, the last agent message, the flow of the
  feature being built, or someone else's PR. Use when the user invokes
  /simple-explain, asks to explain something simply or "like I'm new to this",
  asks how a feature or PR works step by step, says they do not understand the
  last message, or has asked more than once for a simpler answer.
---

# Simple explain

Explain one thing so the user understands it on the first read. Answer in the language the user writes in.

## Modes

| Mode | Length | When |
| --- | --- | --- |
| `short` | 60-120 words for an idea, 120-250 for a flow | Default |
| `normal` | 120-250 words for an idea, 250-400 for a flow | The user asks for `normal` or "a bit more" |
| `deep` | As long as it needs | The user asks for `deep` or "everything" |

## Steps

1. **Find the thing to explain.**
   - The user named it: use that.
   - The user says they do not get the last message, or names nothing right after a long agent message: explain that whole message, not one term from it.
   - The user asks how the current feature or work works: take the flow being built in this conversation. Read the branch diff (`git diff` against the base branch, plus uncommitted changes), the untracked files that `git status --short` lists, and the files touched in the conversation.
   - The user gives a PR number or link: run `gh pr view <pr>` and `gh pr diff <pr>`. To read the PR's version of a file without switching the user's branch, run `git fetch origin pull/<pr>/head` and then `git show FETCH_HEAD:<path>`. If the fetch fails, say so and explain from the diff alone.
   - The user names nothing else: take the last term, finding, or decision they reacted to.
   - If two things fit, ask which one in one line.
2. **Check the facts.** If it is about code, read the code first. Explain what the code does, not what the name suggests. For a feature or PR, read the callers and callees of the changed code too, because a flow often runs through lines the diff does not show.
3. **Pick the shape.** A single concept, finding, or decision is an idea. Something that happens in order, such as a request, a user action, a job, or a feature or PR, is a flow. A last message is an idea when it makes one point and a flow when it describes a sequence.
4. **Write the parts for that shape**, in order.

   For an idea:
   - **What it means.** One or two sentences in everyday words. Define any term you cannot avoid the first time you use it.
   - **Example.** One concrete case: real code from the repo, real values, or an everyday situation that has the same shape. Show the input and what happens. In `short` mode, one example only.
   - **Why it matters.** What goes wrong without it, or what the user should do with this.

   For a flow:
   - **What it does.** One or two sentences: who starts it and what they get at the end.
   - **The flow.** Numbered steps, one action per step, with the real function and file names (`saveOrder` in `orders.ts`). For a PR, or when the user asks what changed, mark each step as new, changed, or unchanged, and say in one line what the step did before.
   - **Example run.** One concrete input followed through the steps, with real values: "the user submits quantity 0, step 2 rejects it, the form shows the error".
   - **Watch out.** Only when there is something: a step that can fail, a case the code does not handle, or work that is not finished yet.
5. **Stop.** No summary, no list of related topics. In `deep` mode, add edge cases or a second example only where the user needs them.

## Rules

- Use short sentences and common words. Keep exact names for code, commands, and files.
- One idea per paragraph. Use numbered steps only when order matters.
- Do not talk down. Simple words, not baby words.
- Do not drop facts to make it simpler. If something stays hard, say which part is hard and explain that part.
- Explain what the code or PR does, not whether it is right. Point to `miko-review` if the user wants a review.
- Do not run this on every answer. Use it when asked, or after the user has asked more than once to make something simpler.

## Examples

User: `/simple-explain race condition`

> **What it means.** Two pieces of code use the same data at the same time, and the result depends on which one finishes first.
>
> **Example.** You click "log out" while the app is refreshing your login token. Logout clears the token. A moment later the refresh finishes and saves a new token. You are logged out on screen but still logged in underneath.
>
> **Why it matters.** It breaks only sometimes, so tests often miss it. The fix is to make the second step check that nothing changed before it writes.

User: `/simple-explain what changed in the checkout flow on this branch`

> **What it does.** When the user clicks "Pay", the app checks the cart, charges the card, and saves the order.
>
> **The flow.**
> 1. `onPay` in `Checkout.tsx` sends the cart to `POST /orders`. *(unchanged)*
> 2. `createOrder` in `orders.ts` checks that every item is in stock. *(new: before, stock was checked only after payment)*
> 3. `charge` in `payments.ts` charges the card.
> 4. `createOrder` saves the order and returns its id.
>
> **Example run.** The cart has 2 mugs, but only 1 is left. Step 2 stops with "Only 1 mug left", so the card is never charged.
>
> **Watch out.** Two people can still pass step 2 for the last mug at the same time, because nothing reserves the stock between steps 2 and 4.
