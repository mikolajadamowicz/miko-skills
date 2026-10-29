---
name: review-deep-modules
description: >-
  Review lens based on John Ousterhout's "A Philosophy of Software Design":
  flags shallow modules, information leakage, pass-through methods and
  variables, temporal decomposition, complexity pushed up to callers, errors
  that could be defined out of existence, and special-purpose interfaces. Run
  by the review skill, or on its own when the user asks for a deep-modules or
  design-complexity review.
---

# Review lens: deep modules

A module is deep when a simple interface hides a lot of functionality. Complexity is what makes code hard to understand and change; it shows up as change amplification (one change touches many places), cognitive load (how much you must know to make a change), and unknown unknowns (not knowing what you must know). Judge every new or changed module, class, and function by whether it reduces those.

## Setup

- If the `review` skill started you, it gave you the repo, base ref, and paths to `finding-format.md` and maybe `REVIEW.md`.
- If you run on your own, get the diff with `git diff $(git merge-base origin/HEAD HEAD)...HEAD` plus `git diff HEAD`, read `REVIEW.md` at the repo root if it exists, and use the finding format in `finding-format.md` inside the sibling `review` skill directory.
- Read only. Do not edit files.

## How

1. List every module, class, exported function, and interface the diff adds or changes.
2. For each one, read its callers and its implementation. You cannot judge depth from the signature alone.
3. Run the checks below. A finding must name the module, what leaks or what is shallow, and the deeper shape.

## Checks

### 1. Shallow module

The interface costs about as much to learn as the implementation it hides. Signs:

- a wrapper whose body is one call to another function with the same arguments
- a class with many small methods that each do one line
- callers must call several methods in a fixed order to do one thing
- an options object with many flags that each switch a small branch

Fix: merge into the caller or the callee, or widen the module so it does the whole job behind one call.

### 2. Information leakage

The same design decision (a file format, a protocol detail, an ordering rule, a data shape) is known by more than one module. Changing it would mean editing all of them.

Fix: put the knowledge in one module and give the others an interface that does not expose it.

### 3. Temporal decomposition

Code is split by the order things happen (read, then parse, then write) rather than by what each piece knows. The result is that the read and write modules both know the format.

Fix: split by knowledge. One module owns the format and does both directions.

### 4. Pass-through methods and variables

- A method that only forwards to another method with the same signature adds an interface without adding function.
- A parameter threaded through several layers that do not use it, only to reach one deep function.

Fix: remove the layer, or give it real work. For pass-through variables, use a context object or move the use closer to the source.

### 5. Pull complexity downward

The module pushes decisions onto its callers: config knobs nobody can choose well, exceptions every caller handles the same way, return values every caller post-processes the same way.

Fix: make the decision inside the module with a sensible default. A module has fewer developers than users, so complexity is cheaper inside it.

### 6. Define errors out of existence

An error or special case that callers must handle, but which the module could make impossible or harmless: deleting something that is already gone, a substring past the end, an empty input that could return an empty result.

Fix: change the semantics so the case is normal, mask it inside the module, or aggregate many handlers into one. Do not apply this to errors the caller genuinely must know about.

### 7. Somewhat general-purpose interfaces

An interface shaped exactly around today's one caller (`deleteSelectedTextInEditorForBackspace`) instead of the general operation (`delete(range)`). Special-purpose interfaces multiply and leak caller knowledge into the module.

The opposite is also a finding: an interface generalized for callers that do not exist. Generality should simplify today's callers, not add parameters for imagined ones.

### 8. Different layer, different abstraction

Adjacent layers that expose the same abstraction (a `TextDocument` class whose methods mirror the `Buffer` class beneath it) add a layer without adding a concept.

### 9. Interface comments describe the abstraction

The interface comment (or the name and types, if there is no comment) should tell a caller what the module does and what they must know to use it, without reading the body. If you had to read the implementation to call it correctly, the interface is incomplete. Comments that repeat the code are not the fix; a clearer abstraction is.

### 10. Names and obviousness

A name that is vague (`data`, `handle`, `manager`, `process`) or that could fit several things usually means the module has no single clear job. Code is obvious when a reader's first guess about what it does is right.

## Severity guide

- **Block**: rarely. Only when the leak or shallow split will cause a real bug, such as two modules that must agree on a format and already disagree.
- **Fix**: information leakage, temporal decomposition, pass-through layers, errors pushed to every caller.
- **Ask**: shallow but small helpers, generality trade-offs, naming.

Return findings with `lens: deep-modules` and `check:` set to the check name above. In `fix`, describe the deeper shape concretely: which modules merge, where the knowledge moves, and what the new interface is.
