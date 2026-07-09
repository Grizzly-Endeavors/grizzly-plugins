# Gather

The same need is being met in several places, each a little differently. Three functions that each parse a date their own way. Retry logic reimplemented at every call site. The same request shape rebuilt from scratch in five files, drifting slightly apart as each one gets patched in isolation. No single system here has grown too big — instead, a real, coherent need has never been given a home, so it lives scattered.

The work is to recognize the shared shape, build one well-made thing that fills the need, and move the scattered sites onto it — deleting the copies as you go. Like Distill, this ends at one thing that does one job well; unlike Distill, it gets there by collecting rather than subtracting.

## First, the Warning

Read this before you gather anything. Consolidation done wrong is worse than the duplication it replaces.

**The wrong abstraction is more expensive than duplication.** When you force together things that only *look* alike, every future change has to thread through a shared piece that fits none of its callers well, and the thing sprouts flags and special cases until it is harder to understand than the copies ever were. Duplication is cheap to fix later; the wrong abstraction is sticky and spreads.

So, before building:

- **Confirm it is genuinely one need**, not a superficial resemblance. Two blocks of code can look identical today and be destined to diverge tomorrow because they answer to different masters. If a change to one would *not* imply the same change to the others, they are not the same thing — leave them apart.
- **Prefer real instances over anticipated ones.** The rule of three is a good default: wait until the same need has actually appeared three times before giving it a home. Two might be a coincidence.
- **Distinguish "will be needed again and again" from "might be."** A home is justified when it clearly makes the call sites easier to understand *now*, or when the need is plainly recurring. Building for a future that only might arrive is how speculative abstractions are born — the opposite of care.

If, after this, it is not clearly one need, the caring move is to *not* gather. Say so and stop.

## Recognizing the Candidate

- The same small algorithm, copy-pasted and lightly edited, appears in several files.
- A cross-cutting concern — retries, pagination, auth headers, error mapping — is hand-rolled at each call site.
- You fix a bug in one place and get an uneasy feeling there are four more copies with the same bug. (There usually are.)
- Reviewers keep saying "didn't we already write this somewhere?"

## The Work

Before the steps below, open the relevant example lens — `examples/code.md`, plus `interfaces.md` or `agents.md` if the home you're building is a user-facing surface or an agent-facing tool. The shapes are what you hold the new home to; without them you tend to reproduce the scattered logic in one place rather than making it genuinely better than the copies it replaces.

### 1. Find every instance

Locate all the sites serving this need, not just the two that prompted you. Gathering three of five copies into a shared home while two stragglers stay behind leaves the codebase *more* confusing, not less — now there are two ways to do the thing and no obvious winner. Know the full set before you design.

### 2. Separate the shared core from the per-site variation

Look at the instances side by side. What is truly identical across all of them — that is the core. What differs from site to site — that is variation the home must accommodate. Design the seam so that variation enters as a parameter, a small injected hook, or a caller-supplied value — never as an internal `if this caller, do that` fork. A consolidated thing that has to know about its individual callers is the wrong abstraction wearing a helpful disguise.

If, when you lay them out, the variation dwarfs the shared part — if the sites agree on very little — then this is not one need after all. Abandon the gather. That is a successful outcome: you learned the duplication was superficial before you cemented it.

### 3. Build the home

Create one well-made thing that fills the need, and make it the obvious thing to reach for — clearly named, clearly the right tool, easy to find. Apply the shapes in `examples/code.md`: give it a guessable name, errors written for the debugger, a shape that makes illegal use hard. If the home you're building is a user-facing surface or an agent-facing tool, bring in `examples/interfaces.md` or `examples/agents.md` too. Hold it to a real bar: it should either make each call site visibly simpler to read, or be something the codebase will genuinely reach for again and again. If it does neither, you have added an indirection for nothing.

### 4. Migrate and delete

Move the call sites onto the new home **one at a time**, verifying at each step that behavior is preserved — the site should do exactly what it did before, now by a shorter path. As each site moves over, delete the old copy it replaced. Do not leave the scattered originals lying around next to the new home; the whole point is that the need now has one place to live, and leftover copies reintroduce the confusion you set out to remove.

## Guardrails

- **Behavior preserved at every site.** Each migrated caller must do exactly what it did before. If moving one reveals it was subtly different, that difference is either variation the home must handle or a bug to surface openly — never something to quietly flatten.
- **One home, one name, one place to change.** After gathering, a future change to this need should happen in exactly one spot. If it wouldn't, you haven't finished — or you gathered things that shouldn't have been together.
- **Delete as you go.** A gather that adds a shared thing without removing the copies has made the codebase larger and more confusing, not less.
- **Willing to walk away.** If the sites turn out not to share a real core, stopping is the right call, not a wasted effort.

## Done When

The need has exactly one home, the call sites are shorter and clearer for using it, and a future change to how the need is met happens in one place instead of many. Someone new to the code would find the home first and never be tempted to hand-roll the thing again.
