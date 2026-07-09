---
name: hammer-time
description: >
  A simplicity-first reasoning lens for cutting through overcomplicated designs,
  plans, and systems. Trigger immediately when the user says "hammer time",
  "it's hammer time", "just use a hammer", "this is overcomplicated", or
  similar. Also trigger when you detect that a situation, plan, or system has
  become overcomplicated, or when the user seems overwhelmed or lost in a
  design discussion — in these cases, ask if it's "hammer time" before
  proceeding. Applies to anything: software, writing, projects, workflows,
  life decisions.
---

# Hammer Time

## The Problem This Solves

Things get overcomplicated. It happens at every stage — during brainstorming when ideas compound faster than they get evaluated, during implementation when a "small change" turns out to touch everything, and in the systems we inherit or let grow unchecked over time. The patterns look different but the underlying dynamic is the same: complexity accumulates without earning its place.

In brainstorming, it's wow factor scope creep and "you could do both"-isms — cool ideas stacking up until the design is a loose collection of features rather than a coherent solution. In implementation, it's the realization that the approach is fighting the architecture, or that every fix reveals two more problems. In existing systems, it's the slow accretion of abstractions, compatibility layers, and features that made sense once but now just add weight.

The hammer solution is the antidote. A hammer is boring. A hammer is obvious. A hammer works.

## Core Principles

**The hammer solution must actually work.** This isn't about being reductive or dismissive. A hammer solution that doesn't solve the real problem isn't a hammer — it's a cop-out. Identify the actual core need first, then find the simplest path that genuinely meets it.

**Complexity needs to justify itself against the hammer, not the other way around.** The burden of proof is on the clever solution. "Why not just use the hammer?" is always a valid question. If the answer is "well, the hammer would be fine but this is cooler," that's not justification.

**Name what you're cutting.** Half the value of the hammer is making explicit what you're choosing NOT to do. This turns vague scope into concrete decisions.

**The hammer can change.** As understanding of the problem deepens, what counts as the simplest viable solution might shift. That's fine. The hammer is a tool for thinking, not a commitment.

## Output Contract

All four workflows end the same way:

1. **Statement.** A single short declarative sentence. The hammer. No hedging, no "you could also." Examples: "Just use a JSON file." / "Keep the API, drop everything else." / "Back out and use the existing queue."
2. **Explanation.** Why this works. What's being dropped and why that's fine. Where the complexity was hiding and why it wasn't earning its keep.
3. **Handoff.** Check if the user wants to adjust, and if not, move into action planning. Keep this natural — don't use the same phrasing every time.

## Routing

This skill has four modes. Identify which one applies and read the corresponding reference file.

### 1. Define — New problem, starting fresh
**When:** The conversation is entering design or planning territory and no solution exists yet.
**Read:** `references/define.md`

### 2. Simplify — Mid-conversation course correction
**When:** A design discussion has spiraled. The solution has outgrown the problem. The user asks for the hammer, or you detect that the conversation needs one.
**Read:** `references/simplify.md`

### 3. Audit — Evaluating an existing system
**When:** The user points the hammer at something already built. A codebase, a workflow, an infrastructure setup, a process. They want to know what it actually needs and what can be cut.
**Read:** `references/audit.md`

### 4. Redirect — Mid-implementation course correction
**When:** The user is partway through building something and has hit a wall. Unexpected complexity, cascading changes, conflicts with existing architecture, or a scope revelation. They need to decide whether to push through, back out, or pivot.
**Read:** `references/redirect.md`

## What This Skill Is NOT

- It's not "always do the simplest thing." Sometimes the complex solution is correct.
- It's not an excuse to be dismissive of ideas. Every idea in a brainstorm had a reason.
- It's not a replacement for design thinking. It's a complementary lens.
- It's not about speed over quality. The hammer should be high-quality — just not over-engineered.
