# Humanize examples

Word lists and before/after examples for the rules in [SKILL.md](SKILL.md), moved here unchanged and grouped under the same headings.

## Use plain language

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

## Avoid inflated wording

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

## Avoid poetic language by default

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

Instead of:

> This architecture serves as the foundation upon which the entire application experience is built.

Write:

> The rest of the app depends on this architecture.

## Prefer simple verbs

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

Instead of:

> The dashboard serves as the central interface for managing deployments.

Prefer:

> The dashboard is the main interface for managing deployments.

Instead of:

> The application boasts an extensive collection of customization options.

Prefer:

> The application has many customization options.

## Cut filler

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

## Avoid cutoff disclaimers

Avoid phrases such as:

- "While specific details are limited..."
- "Although information is scarce..."
- "Based on the available information..."
- "Without more context..."
- "It is difficult to say for certain..."
- "There is limited public information..."
- "Details remain unclear..."

Instead of:

> While specific details are limited, the migration appears to have improved performance.

Prefer:

> The team reports faster startup times, but no benchmark numbers were published.

## Avoid formulaic contrast

Avoid constructions such as:

> It's not X. It's Y.

> This isn't about X. It's about Y.

> Not only X, but also Y.

> It's less about X and more about Y.

## Avoid formulaic concession sentences

Be suspicious of structures such as:

> Despite these challenges, the company continues to thrive.

> Despite its limitations, the framework remains a powerful choice.

> While there are some drawbacks, the overall experience is positive.

> Although the implementation is complex, it offers significant benefits.

Instead of:

> Despite its limitations, the library remains a powerful tool for developers.

Prefer:

> The library lacks offline support, but its API is simple and well documented.

## Do not force groups of three

Avoid patterns such as:

> Faster. Smarter. Better.

> Build faster, collaborate better, and ship confidently.

## Avoid repetitive parallelism

For example, avoid:

> You need clarity. You need discipline. You need focus. You need consistency.

## Avoid rhetorical fragment questions

Do not use fragments such as:

> The problem? Latency.

> The result? A slower application.

> The reason? Poor caching.

Write:

> The problem is latency.

or restructure the paragraph naturally.

## Avoid false ranges

Avoid:

> From React performance to company culture, the conference covered everything developers need.

> From authentication to AI agents, the platform handles modern development workflows.

> From small startups to global enterprises, the solution works for everyone.

Prefer:

> The conference covered React performance, company culture, and several other developer topics.

or:

> The platform includes authentication and AI agent tooling.

Use `from X to Y` when the range is real:

> The migration reduced startup time from 3.2 seconds to 1.8 seconds.

> The SDK supports Android versions from API 26 to API 36.

## Avoid AI vocabulary

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

## Prefer concrete statements

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

## Use the project-specific prose test

Examples of weak generic prose:

> The framework provides a flexible and intuitive developer experience.

> The architecture is designed with scalability and maintainability in mind.

> This solution enables teams to build better software more efficiently.

Prefer:

> The framework generates typed API clients from the GraphQL schema.

> Each feature owns its routes, state, and API calls.

> Builds are cached by workspace, so unchanged packages are not rebuilt.

## Avoid name-dropping without substance

Avoid:

> The project has been featured by Forbes, Bloomberg, TechCrunch, Wired, and The Verge.

> Companies such as Google, Meta, Netflix, and Amazon use similar approaches.

> Experts including X, Y, and Z have discussed this idea.

Prefer:

> Bloomberg reported that the company had 4 million subscribers in March.

or:

> Netflix described a similar caching strategy in its engineering blog.

## Avoid vague attribution

Avoid:

- experts say
- research shows
- critics argue
- industry reports suggest
- many developers believe
- it is widely considered

## Remove empty promotional language

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

## Avoid excessive short sentences

Avoid:

> The API is simple. It is fast. It is flexible. It works everywhere.

Prefer something like:

> The API is simple and works across platforms. It also avoids much of the setup required by the previous approach.

## Sentence structure

Instead of:

> The configuration is loaded by the server.

Write:

> The server loads the configuration.

## Avoid weak filler clauses

Examples:

> The cache stores the response, improving the overall user experience.

> The change reduces startup work, ensuring better performance.

## Avoid excessive hedging

Avoid:

> It could potentially perhaps cause...

Use:

> It may cause...

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

## Semicolons

Instead of:

> The API is stable; however, the documentation is incomplete.

Prefer:

> The API is stable, but the documentation is incomplete.

Instead of:

> The migration reduced complexity; it also removed two runtime dependencies.

Prefer:

> The migration reduced complexity and removed two runtime dependencies.

## Headings

Prefer:

> How the cache works

Not:

> How The Cache Works

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

## Conclusions

Avoid generic endings such as:

> Ultimately, the future looks promising.

> Only time will tell.

> This represents an exciting step forward.

## Technical writing

Do not turn:

> React reconciles the component tree after the state update.

into:

> React looks through everything and figures out what changed.

The first version may be more precise for the intended reader.
