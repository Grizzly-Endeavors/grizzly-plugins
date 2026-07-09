# Redirect — Mid-Implementation Course Correction

## Purpose

The user is partway through building something and hit a wall. Maybe the change touches way more systems than expected. Maybe they're knee-deep in a rabbit hole of edge cases that keep multiplying. Maybe what they're building is fighting the existing architecture at every step. The design might have been fine — the reality of implementing it is the problem.

This is different from Simplify, which course-corrects a *design*. Redirect course-corrects an *implementation in progress*, where the user has partially-built work and forward momentum pulling them deeper.

## Workflow

### Step 1: Assess the Situation

If you have access to the codebase or work-in-progress, look at it. Check what's been changed so far — diffs, new files, modified configs. Understand the current state:

- How much has actually been built? Is this 10% done or 80% done?
- What's the nature of the blocker? Is it unexpected complexity, a conflict with existing patterns, a scope revelation, or something else?
- How deep are the tendrils? Does the change touch two files or twenty? Is it isolated or has it started threading through the system?

If you don't have access, ask the user to describe where they are, what they've changed so far, and what they're running into.

### Step 2: Identify the Real Options

This is the core of Redirect and where it diverges from the other modes. There are usually three paths, and the job is to honestly evaluate each:

**Push through.** Is the remaining complexity bounded? Can you see the end from here, or does every fix reveal two more problems? If the blockers are tedious but finite, sometimes the hammer is to just grind through them. But if every step uncovers more unknowns, that's a signal to stop.

**Back out.** Can you cleanly revert to where you started? How much of what you've done is salvageable in a different approach? The sunk cost doesn't matter — what matters is whether the path forward from here is shorter than the path forward from a clean slate.

**Pivot.** Is there a simpler approach that gets to the same goal, and can it reuse some of what's already been built? This is often the actual hammer — not the original plan and not a full retreat, but a third path that sidesteps the complexity you've uncovered.

### Step 3: Drop the Hammer

Deliver the recommendation following the output contract:

**Statement** → **Explanation** → **Handoff**

The statement might look different from the other modes. It could be:

- "Stop. Back out the changes and do X instead."
- "Finish what you have but drop Y and Z — they're where all the complexity is hiding."
- "You're 80% through the hard part. Push through the last bit, it's bounded."
- "Pivot: keep the work on A, throw away B, and connect A to the existing C instead of building D."

Be specific about what to do with the existing work — keep it, revert it, or extract parts of it.

## The Sunk Cost Trap

The biggest danger in mid-implementation is the pull of work already done. "I've already spent three hours on this" is not a reason to spend three more. The only question that matters is: *from where I am right now, what's the shortest path to done?*

Call this out explicitly when the honest answer is to back out. Naming the sunk cost makes it easier to let go of.

## Things to Watch For

- **Cascading changes** — one modification requiring changes in five other places, each of which requires its own changes. This is the system telling you the approach doesn't fit the architecture.
- **Fighting the framework** — when you're working around the tools instead of with them. If the existing patterns, conventions, or architecture resist what you're doing at every turn, the approach is probably wrong for the codebase, even if it's correct in theory.
- **Scope revelation** — you thought this was a small change but it's actually a big change. The original estimate was wrong. Recalibrate from reality, not from the plan.
- **The "almost done" loop** — feeling like you're almost done, repeatedly, for an extended period. Each remaining task reveals one more task. If "almost done" has been true three times, you're not almost done.
