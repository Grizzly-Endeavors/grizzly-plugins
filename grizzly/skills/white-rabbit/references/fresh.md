# Fresh — Disciplined Start on a New Problem

## Purpose

A new problem has arrived. Something's broken, behaving unexpectedly, or failing silently. Debugging hasn't started yet — or has barely started — and the white rabbit is already there: that first plausible-looking cause, beckoning.

This is where the discipline pays off the most. The first five minutes of debugging set the trajectory. Starting with a broad inventory and a suspect list converges on the right answer faster than diving straight after the rabbit and making changes.

The investment is small — a few minutes of structured observation before touching anything. The payoff is avoiding the thirty-minute rabbit hole that would otherwise need climbing back out of.

## Workflow

### Step 1: Observe Before Acting

Gather information. Don't change anything yet. The goal is the most complete picture of the failure with the least effort.

**Reproduce first.** Can the problem happen again? Reliably? If it's intermittent, what conditions seem to correlate? Reproduction is the foundation — without it, the target is a ghost.

**Read the actual error.** The full error message, stack trace, or log output often contains more information than gets extracted on first read. Read the whole thing. Note the exact error type, location, and any context provided. Save timestamps, request IDs, and correlation IDs.

**Check the perimeter.** Before diving into code, check the things around the code:
- Is the service/process running?
- Are there resource constraints (CPU, memory, disk, connections)?
- Did anything change recently? (Deploys, config changes, dependency updates, infra changes)
- Is this happening everywhere or in a specific environment?
- Is this happening to all inputs or specific ones?

These questions take two minutes and can save hours.

### Step 2: Build the Inventory

Write out the observations. Be specific:

- **What's happening:** Exact error messages, exact behavior, exact output.
- **What should be happening:** The expected behavior. Sometimes the "bug" is actually correct behavior that wasn't expected, or the expectation itself is wrong.
- **When it started:** If known. "This worked yesterday" is a valuable constraint.
- **What changed:** Recent deploys, config changes, upstream service changes, data changes.
- **What's been observed but not explained:** Anything weird, even if seemingly unrelated.

### Step 3: Generate Hypotheses (Plural)

Based on the inventory, generate at least three possible causes. Not one — three. The discipline of generating multiple hypotheses is specifically what prevents chasing the first rabbit in sight.

For each hypothesis:
- What specific observations does it explain?
- What specific observations does it *not* explain? (An incomplete explanation is an incomplete hypothesis.)
- What would be expected that hasn't been looked for yet? (This becomes the test.)

If only one hypothesis comes to mind, the problem hasn't been viewed from enough angles. Revisit the categories from the Stuck workflow: the obvious, the assumed, the upstream, the environmental, the interaction, the "no way."

### Step 4: Triage and Probe

Pick the hypothesis that's fastest to test — not the one that seems most likely. The goal is maximum information per minute.

Design a probe that distinguishes between hypotheses. The best probe is one where hypothesis A predicts one outcome and hypothesis B predicts a different outcome. A single test, two suspects addressed.

State predictions before running the test. "If it's a connection timeout, [X] will appear in the logs. If it's an auth failure, [Y]. If it's neither, [Z]." This prevents after-the-fact rationalization of ambiguous results.

### Step 5: Proceed or Recurse

If the probe identifies the cause clearly: confirm with one more piece of evidence if practical, then fix.

If the probe narrows but doesn't resolve: update the inventory, refine hypotheses, probe again.

If the probe reveals something unexpected: good. That's the landscape showing something the rabbit would have hidden. Update the suspect list and reprioritize.

## The "Quick Check" Exemption

Not every bug needs the full protocol. A `FileNotFoundError` pointing at a specific path just needs a check whether the file exists. If the error message is unambiguous and the fix is obvious, just do it.

The protocol is for when the cause isn't obvious, when multiple systems are involved, or when the error message could mean several things. Err toward the protocol when unsure. A two-minute inventory that turns out to be unnecessary costs almost nothing. A thirty-minute rabbit hole costs real time.

## Things to Watch For

- **The assumption cascade.** The input is assumed valid. The service is assumed reachable. The config is assumed to match prod. Each assumption is an untested hypothesis. When nothing makes sense, walk backward through the assumptions.
- **The red herring log line.** Not every error in the logs is *the* error. Logs are noisy. Match timestamps and request contexts carefully. A `WARN` from an unrelated module at the wrong timestamp can lead down the wrong hole for hours.
- **The "I've seen this before" trap.** Pattern matching is powerful, but it can be its own rabbit. When symptoms look familiar, the pull to chase that theory is even stronger. If the experience-based fix doesn't work on the first try, immediately broaden — don't double down on the pattern match.
