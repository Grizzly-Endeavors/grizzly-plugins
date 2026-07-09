# Residuum — Philosophy

This doc captures how decisions get made on this project. Not what to build — that changes. How to think about what to build, what to cut, and when something is done. If you're contributing to Residuum and aren't sure whether something belongs, start here.

---

## Simple things that compose

The unit of good work in Residuum is a thing that is simple and reliable on its own, but designed to connect. A feature should be useful without knowing about every other integration point in the system. If you *do* know, you can compose simple pieces into something powerful — but that power comes from the composition, not from any single piece trying to be powerful by itself.

Simple and clear systems that compose to meet complex needs. Not complex systems that try to meet every need up front.

This applies at every level — a function, a feature, an agent capability, a CLI command. Each one should be easy to understand in isolation. The complexity budget is spent at the seams, not inside the parts.

---

## The obvious test

The best contributions feel obvious in hindsight. Either they add something that should have been there from the start, or they cut something that wasn't pulling its weight. Both should make someone look at the result and think "right, of course."

If a change needs a paragraph to justify its existence, it's worth questioning whether it belongs. This doesn't mean all good work is small — some things are large and obvious. But the *reason* it belongs should be immediately legible.

---

## When to say no

A few recurring patterns that signal something doesn't belong:

**It has to hook into too many things to work.** If a feature requires touching five systems to function, it's either the wrong feature or the wrong shape. Good additions land cleanly. If the codebase is resisting the change, listen to it.

**It makes an existing system's purpose less clear.** Extensions are good when they make something more complete. They're bad when they blur what the thing was for. If adding a capability to a module means you'd need to rewrite its description to explain what it does now, that's a signal.

**It's cool but doesn't make the existing experience more complete.** This is the biggest one. New capabilities that don't deepen what's already there usually mean Residuum is trying to do another tool's job. The question isn't "could Residuum do this?" — it's "does this make Residuum more itself?"

---

## When something is done

A feature is complete when it works in all the obvious ways. You don't need to research it. You don't dig through docs to figure out the right incantation. You pick it up and know what to do with it.

This is a high bar, but it's a specific one. It doesn't mean every edge case is handled. It doesn't mean the implementation is elegant. It means the *experience* is self-evident. If someone has to ask how to use it, it's not done yet.

Conversely — something can be rough, early, and incomplete as long as it's honest about that. An unfinished feature with clear boundaries is fine. A finished-looking feature that's confusing is not.

---

## Depth over breadth

Every other agent project is competing on surface area — more integrations, more models, more tools, more features. Residuum competes on depth. Memory that actually works. An experience that improves the longer someone uses it. A foundation that knows you.

When choosing between making one thing excellent and making two things adequate, make one thing excellent. When a feature is good enough and the temptation is to add the next thing, spend the time making the existing thing complete instead. The product earns trust by doing fewer things well, not more things passably.

---

## Frictionless by default

The measure of success isn't who *can* use Residuum — it's whether anyone has to fight it. Every surface, from install to daily use to extension, should just work. If someone has to read a guide to get started, the onboarding isn't done. If an integration requires boilerplate, the extension point isn't done. If an error message requires context the user doesn't have, the error handling isn't done.

This isn't about targeting a specific audience. It's about removing friction until the audience question answers itself.

---

## What remains

The AI agent space moves fast and burns through ideas faster. New protocols, new frameworks, new patterns — most of them won't matter in a year. Residuum is a foundation, and a foundation doesn't chase every new thing. It waits, and it picks up what's still standing after the hype clears.

This isn't resistance to change. It's patience. When a pattern proves itself — when it survives contact with real use and real users — Residuum adopts it. But it adopts the *essential* version, not the trendy one. The thing that remains after everything else is removed.

This applies to dependencies, protocols, integrations, and architectural patterns. The question isn't "is this new and promising?" It's "is this going to matter in two years?" If the answer isn't clear yet, wait. The construct is patient.

---

## Residuum is invisible when it's working

The best infrastructure disappears. Users should think about their agents, not about Residuum. If a user is thinking about Residuum, something went wrong — either the setup demanded attention, or the coordination between agents became visible, or the system's limitations surfaced during normal use.

Every decision should push Residuum further into the background. The product succeeds when users describe what their agents do for them without mentioning Residuum at all.

---

## Extension should be invisible

The power of AI agents comes from hooking them into existing systems. Residuum's job is to make that effortless. Every extension point — adding a tool, connecting a service, building a new agent — should be frictionless and self-evident. If someone needs to study the internals to extend the system, the extension surface isn't done.

The same "pick it up and know what to do with it" bar that applies to features applies to integration. A well-designed extension point teaches you how to use it by being obvious. The best ones feel like they were always there.

---

## Principles for contributors

These aren't rules. They're the patterns behind the decisions that have worked.

1. **Make it work without context.** Your addition should be understandable and useful to someone who only knows about the part they're touching.
2. **Design the seams.** Think about where your work connects to other pieces, even if those connections aren't built yet. Clean interfaces now enable composition later.
3. **Cut what isn't earning its place.** Removing something that isn't pulling its weight is as valuable as adding something that is.
4. **Don't build for the demo.** Build for the person who's been using it for three months. First impressions matter less than the twentieth time.
5. **When in doubt, do less.** A smaller, complete thing is worth more than a larger, partial one. Ship the hammer. The toolbox comes later.
