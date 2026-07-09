---
name: phase-plan
description: >
  Decompose a large refactor or implementation into a systems-level design doc
  and a sequence of self-contained, individually-verifiable implementation
  phases. Trigger when the user wants to plan a big build — a refactor or
  feature too large to hold in one session — or says "phase-plan", "break this
  down into phases", "make a design doc and phases", "decompose this refactor",
  or similar. The skill produces two standalone artifacts (design.md, phases.md);
  the user orchestrates the per-phase implementation separately in dedicated
  sessions.
created_by: Bear
---

# Phase-Plan

## What this solves

Large refactors and implementations fail in a predictable way: a single session tries to hold the whole thing at once, assumptions compound, and by the end the work has drifted from the original intent. The fix is altitude separation and fresh context. You design at the systems level, you slice into module-level phases, and then each phase gets implemented in its own session that knows nothing about the design conversation — only what the artifacts say. That last part is the whole point: **the artifacts must stand on their own.** If implementing a phase requires assumptions that only exist in the design session's chat history, the decomposition has failed.

This skill covers the design-and-phasing work (Steps 1–2), which is what you do here, in this session. Steps 3–4 (implementation and final verification) are orchestrated by the user in separate sessions — they're described below as context, because you cannot write artifacts that survive a fresh context window unless you understand how they'll be consumed.

## The altitude rule

Each step operates at exactly one altitude. Do not bleed downward.

- **Design doc** — systems level. Shape, reasoning, integration. Never names files or lines.
- **Phase outline** — module level. What each phase must produce and what "done" means. Never names files or lines.
- **Per-phase planning** (Step 3, user-run) — file/line level. This is where specifics get mapped, in a dedicated session, in plan mode.

Pushing file/line detail up into the design or phases is the most common failure. It bloats the artifacts, couples them to a code layout that may change, and robs the per-phase session of the focused mapping work it exists to do.

## Step 1 — Design doc (`design.md`)

Operate exclusively at the systems level. The design doc defines:

- **Shape** — the structure being introduced or changed: the major components, their responsibilities, and the boundaries between them.
- **Reasoning** — why this change, why this shape over alternatives considered. Capture the tradeoffs so a reader who wasn't in the room understands the decision, not just the outcome.
- **Touchpoints with external systems** — every place this work meets something outside its own boundary: APIs, databases, queues, other services, shared libraries. Name the contract at each touchpoint.
- **Integration / composition with existing implementations** — how the new shape sits alongside what's already there. What it replaces, what it wraps, what it leaves untouched, and how old and new coexist during the transition.

Start from `references/design-template.md`. This is iterative — expect multiple revisions. Push on the reasoning, not just the shape. When the shape feels settled, pressure-test it against the touchpoints and the existing system before calling it done.

**Review (required at least once before finalizing).** Before treating the design as final, hand it to the `design-doc-reviewer` subagent (via the Agent tool). It reads the doc with a fresh context window — deliberately good at catching what you've quietly assumed and can no longer see — and reports ambiguities, unstated assumptions, and underspecified contracts without proposing a different design. Run it whenever the user asks, and at least once on the near-final draft. Feed the findings back into a revision and rerun as the design warrants. The bar to clear: **an implementer with only this document and the codebase could build it without guessing.**

## Step 2 — Phase outline (`phases.md`)

Once the design is final, slice it into implementation phases, starting from `references/phases-template.md`. Each phase:

- **Operates at the module level** — it names what modules/components it touches and what they should do when the phase is complete. Never file or line.
- **Is self-contained** — it can be implemented and reasoned about on its own. Order phases so each depends only on phases before it. State each phase's preconditions (what earlier phases must have delivered) explicitly.
- **Is individually verifiable** — it defines what "done" looks like in concrete, checkable terms: what should exist, what should behave differently, how someone confirms the phase landed without waiting for the whole project.
- **Defines only shape and done-criteria** — what must be true at the end, not how to get there. The how is mapped in the phase's own session (Step 3).

A good phase is a coherent unit of progress that leaves the system in a consistent state. Resist phases that are "do half of module X" or that can't be verified until a later phase exists.

## Steps 3–4 — How the artifacts get consumed (context, user-orchestrated)

You do not run these. They're described so you design artifacts that work under these conditions.

**Step 3 — per-phase implementation, one dedicated session each.** For each phase, the user opens a fresh session, enters plan mode, and has Claude map the file/line-level changes for that phase and then implement. Each phase gets its own session so Claude applies full focus to just that phase and assumptions don't compound across phases. Critically, **that session does not have the design conversation** — it has `design.md`, `phases.md`, and the codebase. This is why both artifacts must be self-contained: every term defined, every contract specified, every precondition stated. If a phase session would have to guess at intent, the gap is yours to close now, in the artifacts.

**Step 4 — end-to-end verification.** After all phases are complete, the full implementation is verified against the original design intent — not just "each phase passed" but "the assembled whole does what the design set out to do." Phrase the design's reasoning and the phases' done-criteria so this final check has something concrete to verify against.

## Artifacts

Two standalone files, each at the altitude described above. Scaffold them from the reference templates and keep them in the repo (or wherever the team keeps design docs):

- `design.md` → `references/design-template.md`
- `phases.md` → `references/phases-template.md`

## Output contract

When you finish a design-and-phasing pass, hand off cleanly: state where `design.md` and `phases.md` live, confirm the `design-doc-reviewer` ran at least once and what it surfaced, and remind the user that each phase is implemented in its own fresh session (Step 3) with end-to-end verification at the end (Step 4).
