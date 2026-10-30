---
name: humanize
description: Make prose sound natural, clear, direct, and human in technical and professional contexts — PR descriptions, code comments, documentation, technical explanations, work reports. Remove AI writing patterns, inflated language, unnecessary formality, poetic wording, and unnatural punctuation while preserving meaning and technical accuracy. Use this for technical/professional writing; for casual or social writing (emails, Twitter/X threads, Slack messages), use the unslop skill instead.
---

# Humanize

Write like a thoughtful person, not a language model.

The goal is not to make writing casual, quirky, or artificially imperfect. The goal is to make it clear, natural, specific, and appropriate for the situation.

Apply these rules whenever producing or rewriting prose.

Do not apply stylistic rewriting to code, commands, identifiers, file paths, URLs, logs, error messages, quotations, or other text that must remain exact.

## Priorities

When editing or generating text, optimize in this order:

1. Preserve meaning and accuracy.
2. Use clear, everyday language.
3. Remove obvious AI writing patterns.
4. Keep the tone appropriate for the audience.
5. Make the text easy to read.
6. Keep useful detail.
7. Cut anything that adds words without adding meaning.

Never make the text more "human" by changing facts or inventing personality.

## Preserve the source

Keep all important:

- facts
- names
- numbers
- dates
- technical terms
- commands
- identifiers
- filenames
- file paths
- URLs
- API names
- library names
- quoted output
- error messages
- code

Do not simplify a precise technical term into a less accurate everyday word.

Simplify the explanation around the technical term instead.

Do not invent:

- opinions
- emotions
- personal experiences
- anecdotes
- certainty
- claims
- sources
- motivations

If the original writer has a clear opinion or personality, preserve it.

Do not manufacture one merely to make the text sound human.

## Use plain language

Prefer words people actually use in conversation and normal professional writing.

Choose the simplest natural word that keeps the intended meaning.

Prefer:

- use instead of utilize or leverage
- help instead of facilitate
- improve instead of enhance
- show instead of showcase
- start instead of initiate
- many instead of numerous
- enough instead of sufficient when appropriate
- if instead of in the event that
- because instead of due to the fact that
- to instead of in order to

Do not mechanically replace words. Context still matters.

### Avoid inflated wording

Claude and other LLMs often make ordinary ideas sound grander than they are.

Remove unnecessary words such as:

- crucial
- pivotal
- profound
- compelling
- intricate
- nuanced
- transformative
- groundbreaking
- remarkable
- robust
- seamless
- comprehensive
- holistic
- multifaceted
- sophisticated
- powerful
- elegant

These words are allowed when they communicate something specific and justified.

Do not use them as decoration.

### Avoid poetic language by default

Do not turn normal explanations into prose such as:

- "sits at the heart of"
- "opens the door to"
- "paves the way for"
- "serves as a bridge"
- "the foundation upon which"
- "the broader landscape"
- "at the intersection of"
- "a testament to"
- "a delicate balance"
- "a rich tapestry"
- "embarks on a journey"

Say what actually happens.

Instead of:

> This architecture serves as the foundation upon which the entire application experience is built.

Write:

> The rest of the app depends on this architecture.

## Prefer simple verbs

Do not replace simple verbs such as `is`, `has`, `uses`, or `does` with grander alternatives simply to make the sentence sound more polished.

Be suspicious of constructions such as:

- serves as
- stands as
- acts as
- functions as
- represents
- constitutes
- boasts
- features
- offers
- provides

Use them when they describe a real distinction.

If the sentence simply means `is`, `has`, or `uses`, say that.

Instead of:

> The dashboard serves as the central interface for managing deployments.

Prefer:

> The dashboard is the main interface for managing deployments.

Instead of:

> The application boasts an extensive collection of customization options.

Prefer:

> The application has many customization options.

## Cut filler

Delete introductions that delay the actual point.

Avoid openings such as:

- "In today's world..."
- "In the rapidly evolving..."
- "When it comes to..."
- "It's important to note that..."
- "It is worth mentioning..."
- "At the end of the day..."
- "As we have seen..."
- "Needless to say..."
- "The reality is that..."
- "There is no doubt that..."

Start with the useful information.

Avoid unnecessary transitions between paragraphs.

Do not add "Furthermore", "Moreover", "Additionally", or "That said" just because a new paragraph begins.

Use a transition only when the relationship between ideas would otherwise be unclear.

## Avoid cutoff disclaimers

Do not add vague disclaimers that announce missing information without helping the reader.

Avoid phrases such as:

- "While specific details are limited..."
- "Although information is scarce..."
- "Based on the available information..."
- "Without more context..."
- "It is difficult to say for certain..."
- "There is limited public information..."
- "Details remain unclear..."

Use these only when the limitation genuinely matters to the answer.

When possible:

1. State what is actually known.
2. State the specific missing information if it affects the conclusion.
3. Explain how that uncertainty changes the answer.

Do not use a generic disclaimer as filler.

Instead of:

> While specific details are limited, the migration appears to have improved performance.

Prefer:

> The team reports faster startup times, but no benchmark numbers were published.

## Remove AI rhetorical patterns

### Avoid formulaic contrast

Avoid constructions such as:

> It's not X. It's Y.

> This isn't about X. It's about Y.

> Not only X, but also Y.

> It's less about X and more about Y.

Use them only when the contrast itself is genuinely important.

Usually, state the actual point directly.

### Avoid formulaic concession sentences

LLMs often create artificial balance by beginning with a generic limitation and following it with a positive conclusion.

Be suspicious of structures such as:

> Despite these challenges, the company continues to thrive.

> Despite its limitations, the framework remains a powerful choice.

> While there are some drawbacks, the overall experience is positive.

> Although the implementation is complex, it offers significant benefits.

Do not automatically add a drawback before a positive statement.

Mention the limitation only if it is relevant.

State the specific tradeoff instead of using a generic concession.

Instead of:

> Despite its limitations, the library remains a powerful tool for developers.

Prefer:

> The library lacks offline support, but its API is simple and well documented.

If the limitation does not matter, remove the concession entirely.

### Do not force groups of three

Do not automatically package ideas into three items because three sounds rhetorically neat.

Avoid patterns such as:

> Faster. Smarter. Better.

> Build faster, collaborate better, and ship confidently.

Use however many points the idea actually requires.

### Avoid repetitive parallelism

Do not make several consecutive sentences follow the same grammatical shape merely for effect.

For example, avoid:

> You need clarity. You need discipline. You need focus. You need consistency.

Rewrite it as normal prose.

### Avoid rhetorical fragment questions

Do not use fragments such as:

> The problem? Latency.

> The result? A slower application.

> The reason? Poor caching.

Write:

> The problem is latency.

or restructure the paragraph naturally.

Normal questions are fine when the text genuinely asks a question.

### Avoid fake suspense

Do not write:

> Here's the catch.

> But here's where things get interesting.

> And the best part?

> The surprising part is...

unless there is a real reason to create suspense.

Just state the information.

## Avoid false ranges

Do not use `from X to Y` unless X and Y are meaningful endpoints of a real range, progression, or scope.

LLMs often use this structure to connect unrelated topics.

Avoid:

> From React performance to company culture, the conference covered everything developers need.

> From authentication to AI agents, the platform handles modern development workflows.

> From small startups to global enterprises, the solution works for everyone.

Use a normal list or state the actual scope.

Prefer:

> The conference covered React performance, company culture, and several other developer topics.

or:

> The platform includes authentication and AI agent tooling.

Use `from X to Y` when the range is real:

> The migration reduced startup time from 3.2 seconds to 1.8 seconds.

> The SDK supports Android versions from API 26 to API 36.

## Avoid AI vocabulary

Be suspicious of words and phrases commonly used to make simple ideas sound analytical or impressive.

Examples include:

- delve
- landscape
- ecosystem when "system" or a specific group would work
- interplay
- tapestry
- paradigm
- pivotal
- underscore
- foster
- harness
- leverage
- navigate
- elevate
- unlock
- empower
- streamline
- augment
- showcase
- realm
- journey
- lens
- cornerstone
- north star
- flywheel
- nexus
- substrate
- scaffolding when used metaphorically
- surface when used as an abstract metaphor

These words are not banned.

Use them only when they are genuinely the clearest word.

Prefer concrete descriptions.

## Prefer concrete statements

Avoid sentences that sound meaningful but provide little information.

Instead of:

> The API provides a seamless developer experience.

Explain why:

> The API requires one function call and returns typed results.

Instead of:

> This creates a more robust architecture.

Explain what changes:

> Each module owns its state, so changing one feature does not require updating the others.

Instead of:

> This significantly improves performance.

Give the result if known:

> Startup time dropped from 2.4 seconds to 1.7 seconds.

If no measurement exists, do not imply one.

## Use the project-specific prose test

For technical writing, documentation, product descriptions, and project explanations, ask:

> Could this sentence appear unchanged in the documentation for dozens of unrelated projects?

If yes, it is probably too generic.

Examples of weak generic prose:

> The framework provides a flexible and intuitive developer experience.

> The architecture is designed with scalability and maintainability in mind.

> This solution enables teams to build better software more efficiently.

These statements could describe almost anything.

Replace them with information specific to the actual project.

Prefer:

> The framework generates typed API clients from the GraphQL schema.

> Each feature owns its routes, state, and API calls.

> Builds are cached by workspace, so unchanged packages are not rebuilt.

Project-specific prose should tell the reader something they could not learn from a generic software landing page.

## Avoid name-dropping without substance

Do not list companies, publications, researchers, products, or public figures merely to create authority or importance.

Avoid:

> The project has been featured by Forbes, Bloomberg, TechCrunch, Wired, and The Verge.

> Companies such as Google, Meta, Netflix, and Amazon use similar approaches.

> Experts including X, Y, and Z have discussed this idea.

If the name matters, explain why.

Prefer:

> Bloomberg reported that the company had 4 million subscribers in March.

or:

> Netflix described a similar caching strategy in its engineering blog.

Do not include a name simply because recognition makes the sentence sound more credible.

If several sources say the same thing, keep all sources when the document's citation requirements or the user's intent call for them; otherwise, prefer the strongest or most relevant source.

## Avoid vague attribution

Avoid:

- experts say
- research shows
- critics argue
- industry reports suggest
- many developers believe
- it is widely considered

Name the source when it matters.

If there is no source and the attribution adds nothing, remove it.

## Remove empty promotional language

Avoid promotional adjectives unless the user explicitly wants marketing copy.

Examples:

- stunning
- breathtaking
- world-class
- cutting-edge
- revolutionary
- best-in-class
- must-have
- must-visit
- game-changing
- unparalleled

Describe the actual quality instead.

## Sentence rhythm

Natural writing does not use one sentence length repeatedly.

Mix shorter and longer sentences where appropriate.

Do not deliberately alternate sentence lengths according to a pattern.

### Avoid excessive short sentences

Short sentences can add clarity or emphasis.

Several short sentences in a row often sound generated.

Avoid:

> The API is simple. It is fast. It is flexible. It works everywhere.

Prefer something like:

> The API is simple and works across platforms. It also avoids much of the setup required by the previous approach.

### Avoid overly dense sentences

If a sentence contains several independent ideas, split it.

The reader should not need to reread a sentence to understand its structure.

But do not enforce "one tiny sentence per idea" so aggressively that the prose becomes choppy.

The goal is natural rhythm.

## Sentence structure

Prefer active voice when the actor matters.

Instead of:

> The configuration is loaded by the server.

Write:

> The server loads the configuration.

Passive voice is fine when:

- the actor is unknown
- the actor does not matter
- the passive form is more natural in context

Do not rewrite a natural sentence merely to satisfy a grammar rule.

## Avoid synonym cycling

Do not repeatedly rename the same thing to avoid repetition.

If something is called "the server", keep calling it "the server" unless another term has a different meaning.

Do not cycle through:

> the application
> the platform
> the solution
> the product
> the system

when all five mean the same thing.

Repetition is often clearer than forced variety.

## Avoid weak filler clauses

Watch for unnecessary clauses ending in `-ing`, especially when they merely restate the previous sentence.

Examples:

> The cache stores the response, improving the overall user experience.

> The change reduces startup work, ensuring better performance.

Ask what the second clause actually tells the reader.

If it adds no concrete information, remove it.

## Avoid excessive hedging

Do not stack uncertainty.

Avoid:

> It could potentially perhaps cause...

Use:

> It may cause...

Keep hedging when uncertainty is real.

Do not make uncertain claims sound certain just to make the sentence shorter.

## Avoid unnecessary adverbs

Be suspicious of words such as:

- significantly
- greatly
- dramatically
- effectively
- efficiently
- seamlessly
- incredibly
- extremely
- highly

Use them when they carry real information.

Otherwise, remove them or replace the sentence with a concrete fact.

## Punctuation

Use punctuation normally.

Do not use punctuation as a writing gimmick.

### Em dashes

Do not use em dashes in generated or rewritten prose.

This is a hard rule.

Rewrite the sentence using:

- a period
- a comma
- a conjunction
- parentheses when the information is genuinely secondary
- a colon when it has a normal grammatical purpose
- a different sentence structure

Do not mechanically replace every em dash with the same punctuation mark.

Never introduce an em dash for emphasis, interruption, contrast, explanation, or rhythm.

Do not replace an em dash with a semicolon.

This rule does not require changing exact source material such as:

- code
- quoted text
- logs
- error messages
- filenames
- commands
- identifiers

unless the user explicitly asks to rewrite that exact text.

### Semicolons

Avoid semicolons in prose.

They are not completely forbidden, but they should be rare.

Prefer:

- a period
- a comma with a conjunction
- two naturally connected sentences
- a simpler sentence structure

Do not use a semicolon merely to make a sentence look polished or literary.

Do not use semicolons as a replacement for em dashes.

Do not chain several related thoughts with semicolons.

Use one only when it is clearly more natural and precise than the simpler alternatives.

Instead of:

> The API is stable; however, the documentation is incomplete.

Prefer:

> The API is stable, but the documentation is incomplete.

Instead of:

> The migration reduced complexity; it also removed two runtime dependencies.

Prefer:

> The migration reduced complexity and removed two runtime dependencies.

### Colons

Use colons when they have a real grammatical purpose, especially before:

- a list
- an explanation
- an example

Do not repeatedly use colons as dramatic connectors.

### Parentheses

Use parentheses when the information is genuinely secondary.

Do not push half the paragraph into parentheses to avoid rewriting it properly.

## Formatting

Formatting should help the reader understand the content.

It should not make ordinary prose look more important.

### Bold and italics

Use bold or italics sparingly.

Good reasons include:

- a filename
- a command
- an important warning
- a term being defined
- a genuinely important distinction

Do not bold every keyword, product name, number, or conclusion.

Do not use bold as a substitute for clear writing.

### Headings

Use sentence case.

Prefer:

> How the cache works

Not:

> How The Cache Works

Do not create headings for tiny sections that would read better as normal paragraphs.

### Lists

Use a list when the content is naturally a list.

Do not turn ordinary prose into a list merely because lists are easy to generate.

Avoid repetitive list items with bold labels followed by colons:

> **Performance:** Performance improves because...

When the content is short, write a normal sentence instead.

### Emoji

Do not use decorative emoji in headings or bullet lists unless:

- the user asks for them
- the established format uses them
- the context genuinely benefits from them

## Chatbot language

Avoid generic assistant phrases such as:

- "Great question!"
- "Absolutely!"
- "Certainly!"
- "Of course!"
- "You're absolutely right."
- "I hope this helps."
- "Let me know if you have any questions."
- "Feel free to ask..."
- "Happy to help!"
- "Here's the exciting part..."

Respond to the substance instead.

Politeness is fine. Generic assistant padding is not.

## Conclusions

Do not add a conclusion simply because the text feels like it should have one.

Avoid generic endings such as:

> Ultimately, the future looks promising.

> Only time will tell.

> This represents an exciting step forward.

End when the useful information is finished.

If a conclusion is needed, summarize the actual decision, implication, or next step.

## Match the context

Do not force every piece of writing into the same casual style.

Technical documentation should still sound like technical documentation.

A business email should still sound professional.

A Slack message can be conversational.

An essay may use richer language than an API reference.

A marketing page may intentionally use persuasive language.

Humanizing means removing unnatural AI habits, not flattening every voice into the same style.

## Technical writing

For technical explanations:

- keep accepted technical terminology
- simplify the prose around it
- preserve code exactly unless asked to edit the code
- preserve commands exactly
- preserve identifiers exactly
- preserve filenames and paths exactly
- preserve API names and library names
- preserve error messages and logs
- avoid explaining basic terms when the intended reader already knows them
- do not use metaphors when a direct technical explanation is clearer

Do not turn:

> React reconciles the component tree after the state update.

into:

> React looks through everything and figures out what changed.

The first version may be more precise for the intended reader.

Plain language should not reduce technical accuracy.

## Length

Prefer concise writing, but do not optimize blindly for minimum word count.

Cut:

- repeated explanations
- repeated conclusions
- filler
- unnecessary setup
- redundant caveats
- decorative language

Keep:

- important reasoning
- useful examples
- necessary caveats
- technical constraints
- information the reader needs to act

Shorter is better only when nothing useful is lost.

## Human voice

Human writing may contain:

- contractions
- occasional fragments when natural
- simple words
- uneven paragraph lengths
- varied sentence structure
- direct opinions when the author actually holds them
- small stylistic quirks appropriate to the writer

Do not artificially introduce mistakes, slang, fragments, opinions, jokes, or emotional reactions to simulate humanity.

Natural writing comes from clarity and context, not manufactured imperfection.

## Final self-check

Before returning prose, silently check:

1. Did I preserve the meaning?
2. Did I preserve facts, names, numbers, code, commands, identifiers, and paths?
3. Is there any unnecessarily formal, poetic, or inflated wording?
4. Could any phrase be replaced with a simpler everyday expression?
5. Did I use filler transitions or generic cutoff disclaimers?
6. Did I use an "it's not X, it's Y" construction?
7. Did I use a formulaic "despite X, Y" or similar concession?
8. Did I force a group of three?
9. Did I use repetitive parallel sentence structures?
10. Did I use rhetorical fragments such as "The problem? X"?
11. Did I use fake suspense?
12. Did I create a false `from X to Y` range?
13. Did I use a fancy alternative to `is` or `has` without a good reason?
14. Did I overuse short sentences?
15. Did I use any em dashes in generated or rewritten prose?
16. Did I use a semicolon where a simpler sentence would sound more natural?
17. Did I overuse colons, parentheses, bold, italics, headings, or lists?
18. Did I use vague buzzwords instead of saying what actually happens?
19. Did I cycle through unnecessary synonyms?
20. Did I add generic chatbot politeness?
21. Did I invent opinions, feelings, experiences, sources, or certainty?
22. Did I name-drop people, companies, or publications without explaining why they matter?
23. Does any sentence sound impressive while saying very little?
24. Could any project-specific sentence appear unchanged in dozens of unrelated projects?
25. Would a normal person writing for this audience phrase it more simply?

If an em dash appears in generated or rewritten prose, rewrite that sentence before returning the final text.

If a semicolon appears, check whether a period, conjunction, or simpler sentence structure would sound more natural. Keep the semicolon only when it clearly improves the sentence.

Fix any other problems before returning the final text.
