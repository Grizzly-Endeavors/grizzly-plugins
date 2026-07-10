---
name: tending
description: >
  Four modes for making a codebase feel cared-for, loved, and actively
  maintained — qualities that live in the code itself (beyond "clean") and
  extend to the people and agents who use and work on it. Use whenever the user
  wants to give a project attention: tend small rough edges (Rounds), carry one
  well-defined change across many files like a rename or module reorg (Sweep),
  refactor a system that outgrew its shape (Distill), or consolidate scattered
  logic into one home (Gather). Also covers care for the end user's experience
  (UI, CLI, API, docs) and for AI agents in the repo (agent files like
  CLAUDE.md, in-repo indexes, MCP/tool output). Trigger on phrases like "make
  this feel maintained", "give this some love", "tend to this", "rename this
  everywhere", "reorganize these modules", "distill this down", "clean up our
  CLAUDE.md", or "clean this up" in the caring rather than cosmetic sense — or
  when you notice a codebase would benefit and want to offer it. Also runs
  unattended (Garden): when invoked under /loop, on a schedule, or with phrases
  like "keep tending", "tend continuously", or "let it run", orchestrate scout
  and fixer agents instead of walking the code yourself. Any language or stack.
---

# Tending

## Why This Exists

Loved code looks *lived in* rather than pristine. Pristine often just means untouched — nobody has had to go in and fix anything because nobody has run it against the world. Code that feels cared for has a kind of scar tissue: you can see the places where reality bit someone and they came back and dealt with it.

Two kinds of evidence give it away. Someone imagined a reader who wasn't them. And the thing has been run hard enough to hurt, and then returned to.

This skill is a way to be that someone, and to do the returning on purpose. Not a linter pass, not a rewrite, not cleanup for the sake of a tidier diff. Attention. The four modes below are shapes that attention can take, depending on what the code in front of you actually needs.

## What Cared-For Looks Like

These are things to recognize, not yet a list of things to do. The doing lives in the mode references.

Cared-for code deletes. A codebase nobody loves only ever grows; a loved one shrinks sometimes. It handles edge cases on purpose — the empty collection, the flaky network, the timezone that only breaks for someone in Auckland. Its errors are written for the human debugging at 3am, carrying context about what was being attempted and with what inputs. It uses the type system to make illegal states unrepresentable. Its names can be guessed, because the same concept is called the same word everywhere and units live in the names. Its boundaries sit where the domain has joints, not wherever a file got too long. And it takes care of the unglamorous parts — logging, config validation, graceful shutdown — because that is exactly where corners get cut when nobody is watching.

And care has an audience. The paragraph above is care for the *next maintainer*, but the same instinct — imagine someone who arrives without your context — points two other directions: toward the *end user* who operates the thing across whatever surface it presents (a UI, a CLI, an API, the docs), and toward the *AI agent* that will work in the repo with no memory of it, or consume the tools it exposes. A thing can be cared-for for one audience and neglected for another.

It is almost never one grand gesture. It is the accumulation of a hundred small alignments all pointing the same way. The concrete shapes these take — across all three audiences — live in `examples/`, indexed in `examples/INDEX.md`, and are usable from inside any mode.

## The Disposition

Hold this stance in every mode. It matters more than any individual technique.

**Preserve behavior.** Care is not a license to change what the thing does. If a behavior turns out to be a bug, that is worth fixing — but say so out loud and treat it as its own decision, never as a quiet side effect of tidying.

**Imagine the next reader.** Every change is a note left for whoever comes after, which very often means your future self. Write the note you would want to find.

**Leave it coherent.** A change that improves one line but muddies the pattern around it is a net loss. The surrounding code should feel *more* consistent when you step away, not less.

**Practice restraint.** Knowing when to stop, refusing to gold-plate, declining to manufacture work — these are part of the craft, not a failure of ambition.

**One concern at a time.** If a unit of work were a commit, its message should be a single clean sentence. Keep passes reviewable in isolation.

**Know when it's already loved.** Sometimes the most honest and useful thing you can do is notice that the code is fine, say so plainly, and leave it be.

## Fix What Trips You

The friction you hit while working is not a distraction from the work — it *is* the work. It is the highest-signal thing this skill exists to find, because reality just handed it to you for free.

So: if you trip over something, uncover an existing warning or bug, meet ergonomics that are bad for something that has to happen often, or have to invent a workaround for something that should have simply worked — **fix it, right then.** Don't route around it, don't file it for later, don't leave it for the next person who will pay the same toll you just paid. These are not sidetracks. They are exactly the things this skill exists to find and fix.

This is not limited to application code. A broken or fiddly dev script, a stale doc or README, a misleading comment, an out-of-date sibling skill, an awkward local environment, a build step that fails confusingly, a test that only runs with some magic incantation — all of it is in scope. If it made working in this codebase harder, the caring move is to leave it fixed behind you.

The one guard is that this is friction you *actually encountered*, not a license to wander off inventing improvements — that is the manufactured work the disposition warns against. The line is simple: you didn't go looking for this; it got in your way. Fix it with the same care as anything else — understand it first, keep the fix coherent and reviewable, and if it changes behavior because the old behavior was a bug, name that as you go rather than folding it in silently. Then return to what you were doing, on a path that is now clear for whoever comes next.

## The Modes

Identify what the code needs, then read the matching reference before acting.

Every mode also leans on the concrete shapes in `examples/`, and reaching for them is **not optional** — a scan run from your own general sense of "cared for" is exactly what comes out generic. Before you survey or build, open the relevant lens and make it the checklist you actually work against: always `code.md`, plus `interfaces.md` for anything with a user surface (UI, CLI, API, docs) and `agents.md` for a repo that agents work in or that ships tools for them (`examples/INDEX.md` routes this). Each mode reference marks the point to read them; treat that as a step, not a suggestion.

### Rounds — continuous small care
The loop. Find one small thing that could use attention, give it real care, finish it, then go looking for the next. Aimed deliberately at the little things. Use this when there is no single large target — just a place that would feel more tended after an unhurried walk through it.
**Read:** `references/rounds.md`

### Sweep — one change carried completely across many places
A change you've already decided on, but whose reach is wide: a semantic rename that touches dozens of files, a module move, a convention propagated to every call site, a directory reorganized. The decision is small and clear; the care is in applying it uniformly and *completely*, behavior held constant, with nothing left half-changed.
**Read:** `references/sweep.md`

### Distill — a system that outgrew its purpose
A single system has accreted responsibilities, or been evolved several times until its core is buried in noise. Find the actual job it does, design something that does just that and does it well, and send the rest of the logic home or delete it.
**Read:** `references/distill.md`

### Gather — scattered logic serving one need
The same need is met in several places, each a little differently. Recognize the shared shape and build one well-made home for it — one that makes the modules it serves easier to understand, or that will clearly be reached for again and again.
**Read:** `references/gather.md`

### Garden — the four modes, run unattended
Not a fifth kind of care but a way of running the others without supervision. When tending is invoked under `/loop`, on a schedule, or told to keep going on its own, the main thread becomes an orchestrator: it dispatches scout agents (armed with the example lenses) to survey, routes small findings to fixer agents and large ones to a dedicated agent on a worktree, then verifies and commits centrally. It never surveys or edits the code itself, and it never trusts "I already looked there."
**Read:** `references/garden.md`

Roughly by scope: **Rounds** is many small, independent cares; **Sweep** is one change applied across many places; **Distill** and **Gather** each reshape a single concern — Distill by subtracting from something overgrown, Gather by collecting something scattered. When torn between Sweep and the deeper two, ask whether you already know the change (Sweep) or are still deciding the right shape (Distill or Gather — decide there first, then a Sweep may be how you roll the decision out). And whenever tending runs unattended — a loop, a schedule, no one steering — the mode question answers itself: it's **Garden**, and the other four become the work it dispatches.

## What This Is Not

- **Not a formatter or linter.** Those are cosmetic. This is about care, which the tooling can't see.
- **Not a rewrite.** The goal is almost always *less*, with behavior held constant.
- **Not cleanup for its own sake.** Every change should leave a real reader measurably better off. If you can't name that reader, don't make the change.
- **Not a judgment on whoever wrote it.** Code accretes; that is normal and expected. This is tending, not blame.
