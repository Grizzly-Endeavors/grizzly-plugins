---
name: hammer-time
description: A simplicity-first reasoning lens for cutting through overcomplicated designs, plans, and systems. User-invoked (e.g. "/hammer-time", "hammer time", "just use a hammer", "this is overcomplicated").
disable-model-invocation: true
---

# Hammer Time

Complexity accumulates without earning its place — scope creep in brainstorming, fighting the architecture mid-build, or layers of compatibility shims in an existing system. A hammer is boring, obvious, and actually solves the core need.

## Rules

- **Solve the real need.** A hammer that doesn't work is a cop-out, not simplicity. Name the core need first, then pick the simplest path that genuinely meets it.
- **Complexity carries the burden of proof.** Ask "why not just use the hammer?" If the answer is "this is cleaner/cooler/more extensible", that's not justification.
- **Name what you're cutting.** Explicitly listing what you are choosing *not* to do turns vague scope into concrete decisions.
- **Match the moment:**
  - *Starting fresh (Define):* strip requirements to the minimum that solves the core problem and propose one boring default.
  - *Mid-discussion spiral (Simplify):* pause the branching options, identify where the solution outgrew the problem, and pull back to one path.
  - *Existing system (Audit):* inspect what actually exists and identify what earns its keep vs what can be deleted or collapsed.
  - *Stuck mid-build (Redirect):* decide plainly whether to push through, back out, or pivot to a simpler approach.

## Output

1. **Statement:** one short declarative sentence — the hammer, no hedging or "you could also".
2. **Explanation:** why it works, what is dropped and why that's fine, and where the unnecessary complexity was hiding.
3. **Handoff:** check if the user wants to adjust, then move into action.
