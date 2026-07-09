# Stuck — Mid-Debug Course Correction

## Purpose

The rabbit hole is already deep. Effort has been invested, fixes have been tried, and nothing's working. Maybe each fix reveals a new wrinkle. Maybe there's a growing suspicion the problem isn't what it seemed, but the momentum of the current approach keeps pulling things deeper.

This is the hardest mode to execute because it requires fighting inertia. A mental model of what's wrong has been built, time has been spent on that model, and now it might need to be set aside entirely. The rabbit looked convincing at the start. That doesn't mean it was right.

## Workflow

### Step 1: Full Stop

Stop fixing. Stop changing code. Stop running tests. The next action should produce *information*, not *changes*.

If there are uncommitted changes, stash or note them — they represent the current theory's footprint and are useful context, but they shouldn't stay in play while diagnosing.

### Step 2: Build the Inventory

Write out everything that's actually known. Be ruthless about the distinction between observation and interpretation.

**Observations** are things that can be pointed to: error messages (exact text), log output, stack traces, behavior ("the request returns 500"), timing ("it fails after exactly 30 seconds"), environmental facts ("this works in dev but not staging").

**Interpretations** are conclusions drawn from observations: "the database connection is timing out," "the cache is stale," "there's a race condition." These go in a separate bucket — they're hypotheses, not facts. Label them as such.

Also inventory what's been tried and what happened:
- What was the hypothesis behind each attempted fix?
- What *should* have happened if the hypothesis were correct?
- What *actually* happened?

This last part is gold. A fix that "should have worked" but didn't isn't a failure — it's a data point that the model is wrong. It's the clearest sign that the rabbit was the wrong one.

### Step 3: Generate the Suspect List

With the inventory laid out, brainstorm causes. Go wider than feels comfortable:

- **The obvious.** The first thing anyone would check. If it hasn't been checked yet, check it. If it has, note what was found.
- **The assumed.** Things being taken for granted. "The config is correct." "The service is running." "The input is well-formed." Assumptions are the most common hiding place for bugs — and the most common reason the rabbit looked plausible in the first place.
- **The upstream.** Could the real problem be earlier in the pipeline? Is the data wrong before it reaches the code being stared at?
- **The environmental.** Permissions, versions, networking, DNS, disk space, resource limits. The boring stuff that doesn't show up in code review.
- **The interaction.** A timing issue? Concurrency? Does it only happen under certain conditions or a different ordering of events?
- **The "no way."** The thing that feels too unlikely to check. Check it anyway — especially when nothing else is panning out. When every reasonable suspect has been eliminated, the unreasonable ones deserve their turn.

### Step 4: Prioritize Eliminations

For each suspect, two questions:
1. How fast can this be tested? (Seconds? Minutes? Requires a deploy?)
2. How much search space does it eliminate? (One narrow possibility, or a whole category off the board?)

The best probes are fast and broad. "Add a log line at the entry point to confirm the request even reaches this service" takes thirty seconds and eliminates an entire class of networking/routing problems.

Rank the suspects and pick the top probe. Write down the expected result and what it means if the result differs. Then run *just that one probe*.

### Step 5: Update and Repeat

After each probe, update the inventory with the new observation. Cross off eliminated suspects. Pick the next probe. Continue until the cause is identified through elimination — not intuition.

Only then apply a fix. And verify that the fix addresses the *confirmed cause*, not just the symptom.

## The Sunk Cost Trap

"An hour has already been spent looking at the database layer" is not a reason to keep looking there. The inventory makes visible how much effort has gone into a theory that isn't producing results. If three tests haven't confirmed the hypothesis, it's time to test a different one — regardless of how deep the current hole is.

Letting go of the rabbit isn't admitting defeat. It's the move that gets to the actual answer.

## Things to Watch For

- **The false positive fix.** A change was made and the problem seems gone, but the *why* isn't clear. If the causal chain from change to resolution can't be traced, the symptom may have been masked or a different code path triggered. Test the explanation, not just the outcome.
- **The environment trap.** "It works on my machine" is a clue, not a dismissal. If it works somewhere and fails somewhere else, the difference between those environments *is* the debugging surface. Enumerate the differences.
- **The cascade.** One bug is found, fixed, and a different failure appears. This often means the first bug was hiding the second, but it can also mean the fix introduced a new problem. Check both before chasing the new failure.
- **The version phantom.** Dependency versions, API versions, schema versions. Something changed somewhere and nobody mentioned it. When the timeline matters ("this worked yesterday"), start with what changed between then and now.
- **The architectural root cause.** If the suspect list keeps pointing at structural friction — wrong abstraction boundaries, old patterns fighting new features, every fix requiring changes across too many modules — the problem may not be a bug at all. That's a signal to stop debugging and transition to Hammer Time. The system needs simplifying, not fixing.
