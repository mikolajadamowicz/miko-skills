---
name: simple-explain
description: >-
  Explain a concept, code, a review finding, or a design decision in plain
  words with one concrete example. Use when the user invokes /simple-explain,
  asks to explain something simply or "like I'm new to this", or has asked
  more than once for a simpler answer.
---

# Simple explain

Explain one thing so the user understands it on the first read. Answer in the language the user writes in.

## Modes

| Mode | Length | When |
| --- | --- | --- |
| `short` | 60-120 words | Default |
| `normal` | 120-250 words | The user asks for `normal` or "a bit more" |
| `deep` | As long as it needs | The user asks for `deep` or "everything" |

## Steps

1. **Find the thing to explain.** Use what the user named. If they named nothing, take the last term, finding, or decision in the conversation that they reacted to. If two things fit, ask which one in one line.
2. **Check the facts.** If it is about code in this repo, read the code first. Explain what the code does, not what the name suggests.
3. **Write three parts, in this order:**
   - **What it means.** One or two sentences in everyday words. Define any term you cannot avoid the first time you use it.
   - **Example.** One concrete case: real code from the repo, real values, or an everyday situation that has the same shape. Show the input and what happens. In `short` mode, one example only.
   - **Why it matters.** What goes wrong without it, or what the user should do with this.
4. **Stop.** No summary, no list of related topics. In `deep` mode, add steps, edge cases, or a second example only where the user needs them.

## Rules

- Use short sentences and common words. Keep exact names for code, commands, and files.
- One idea per paragraph. Use numbered steps only when order matters.
- Do not talk down. Simple words, not baby words.
- Do not drop facts to make it simpler. If something stays hard, say which part is hard and explain that part.
- Do not run this on every answer. Use it when asked, or after the user has asked more than once to make something simpler.

## Example

User: `/simple-explain race condition`

> **What it means.** Two pieces of code use the same data at the same time, and the result depends on which one finishes first.
>
> **Example.** You click "log out" while the app is refreshing your login token. Logout clears the token. A moment later the refresh finishes and saves a new token. You are logged out on screen but still logged in underneath.
>
> **Why it matters.** It breaks only sometimes, so tests often miss it. The fix is to make the second step check that nothing changed before it writes.
