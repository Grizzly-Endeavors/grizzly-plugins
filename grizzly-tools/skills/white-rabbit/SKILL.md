---
name: white-rabbit
description: >
  A diagnostic discipline skill that prevents premature convergence on a single
  hypothesis during debugging and troubleshooting. Trigger this skill when the
  same class of fix has been attempted more than twice without progress, when a
  fix "should have worked" but didn't, when the observed behavior doesn't fully
  match the hypothesis being chased, when something "doesn't make sense"
  mid-debug, or when a previously fixed issue resurfaces. Those are signs you're chasing the rabbit. Applies
  to code, infrastructure, configuration, networking, system design — any domain
  where the instinct is to chase the first plausible cause.
---

# White Rabbit

## The Problem This Solves

There's a specific failure mode in debugging that's easy to fall into and hard to notice from inside: a plausible cause appears — the white rabbit — and the chase begins. Down the hole, through the tunnel, deeper and deeper. Every failed fix gets rationalized ("maybe this also needs to change"), and the search space narrows to a single thread instead of broadening to where the real problem might be.

This is premature convergence. It feels productive because things are happening. Changes are being made, tests are running, logs are being read. But nothing is being *learned*. The same hypothesis is getting tried in variations instead of being questioned.

The white rabbit is the first plausible-looking cause. It's compelling, it makes sense on the surface, and chasing it feels like progress. But the deeper the pursuit goes, the harder it is to climb back out and see the bigger picture. This skill is about recognizing the rabbit before chasing it too far — and having the discipline to let it go, step back, and survey the full landscape before committing to a direction.

## Core Principles

**Diagnose before treating.** The urge to fix something immediately is strong and almost always counterproductive when the problem is non-obvious. Every minute spent understanding the problem saves ten minutes chasing the wrong fix.

**Elimination over confirmation.** Don't look for evidence that supports a theory. Look for the fastest way to *rule things out*. A negative result ("it's definitely not the cache") is more valuable than a positive hunch ("it might be the cache") because it permanently shrinks the search space.

**Symptoms are not causes.** The visible behavior is a symptom. There may be multiple layers between the symptom and the root cause. Fixing a symptom without finding the cause means it will come back, probably wearing a different hat.

**Anomalies are gifts.** When something doesn't match the mental model, that's not noise — that's signal. The instinct is to dismiss what doesn't fit. The anomaly is often the thread that leads to the real answer.

**One variable at a time.** When probing, change one thing per test. Changing three things at once and seeing the problem disappear doesn't reveal which one mattered — and might introduce a new problem masked by the others.

## Output Contract

White Rabbit interventions follow a consistent structure:

1. **Inventory.** What is actually known? Not suspected — *observed*. Concrete facts: error messages, log output, behavior, timing, what's been tried, what happened when it was tried. Observation and interpretation stay in separate buckets.

2. **Suspect List.** What are the possible causes? Cast the net wide. Include the obvious, the unlikely, and the "no way, but..." options. The full landscape should be visible before choosing where to dig.

3. **Eliminations.** For each suspect, what's the fastest way to rule it in or out? Prioritize by: (a) how quickly it can be tested, and (b) how much of the search space it eliminates. The ideal probe is fast to run and splits the remaining possibilities roughly in half.

4. **Next Probe.** The single most informative thing to do next. Not a fix — a test. Something that will produce new information regardless of outcome. State the expected result if the hypothesis is correct, and what it means if the result differs.

After each probe, loop: update the inventory, cross off eliminated suspects, pick the next probe. Repeat until the cause is identified with confidence, *then* fix it.

## Routing

This skill has three modes. Identify which one applies and read the corresponding reference file.

### 1. Stuck — Mid-debug course correction
**When:** Progress has stalled. Fixes aren't working, the same files keep getting touched, or the approach has shifted more than twice without resolution. The rabbit hole is deep and getting deeper.
**Read:** `references/stuck.md`

### 2. Fresh — Disciplined start on a new problem
**When:** A new bug, failure, or unexpected behavior has appeared and the cause isn't immediately obvious. Multiple systems could be involved. The white rabbit is right there looking plausible. Don't chase it yet.
**Read:** `references/fresh.md`

### 3. Revisit — The zombie that won't stay dead
**When:** A problem that was previously "fixed" has returned, or a fix for one thing has revealed or caused another. The previous diagnosis was probably incomplete — the rabbit led to a symptom last time, not the root.
**Read:** `references/revisit.md`

## When the Problem Isn't a Bug

Sometimes the White Rabbit protocol reveals that the root cause isn't a defect — it's the system itself. The architecture is fighting the change. Old patterns and new features are pulling in opposite directions. Every fix requires touching five files because the abstraction boundaries are wrong. If elimination keeps pointing at structural friction rather than a specific fault, the right move is to stop debugging and start simplifying. That's a Hammer Time problem, not a White Rabbit problem. Transition accordingly.

## What This Skill Is NOT

- It's not "never trust instincts." Sometimes the first guess is right. The discipline is in *verifying* before committing, not in ignoring intuition.
- It's not an excuse to over-analyze simple problems. If the error says "file not found" and the file is missing, a suspect list isn't needed.
- It's not a replacement for domain knowledge. Understanding how a system works is the foundation — this skill is about using that knowledge systematically instead of reactively.
- It's not about going slow. It's about going in the right direction. The protocol often resolves problems *faster* than chasing, because dead ends get skipped instead of explored.
