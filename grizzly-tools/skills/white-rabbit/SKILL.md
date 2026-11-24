---
name: white-rabbit
description: Anti-tunnel-vision diagnostic protocol for debugging when fixes aren't landing, something doesn't make sense, or a previously fixed bug resurfaces. User-invoked (e.g. "/white-rabbit", "chasing the rabbit", "step back and diagnose").
disable-model-invocation: true
---

# White Rabbit

Premature convergence happens when the first plausible cause (the white rabbit) pulls you down a tunnel: fixes fail, get rationalized, and the search space narrows instead of widening. Step back and eliminate systematically before editing anything else.

## Core Principles

- **Diagnose before treating:** stop making speculative edits after two failed attempts on the same hypothesis.
- **Elimination over confirmation:** prefer the fastest probe that permanently rules out a whole class of causes, not evidence that supports a favorite theory.
- **Separate observation from interpretation:** raw logs, error messages, and timings are facts; explanations are hypotheses.
- **Anomalies are signal:** anything that doesn't fit the current mental model is the best lead.
- **One variable per probe:** change or isolate one thing at a time, and batch any questions about inaccessible logs/environment into a single ask instead of drip-feeding.

## Protocol

1. **Inventory:** list only *observed* facts — exact errors, logs, timing, what was tried, and what actually happened. Keep interpretations out of this list.
2. **Suspect List:** cast the net wide across layers (code, config, state, cache, environment, dependencies, network, concurrency). Include the unlikely candidates.
3. **Eliminations:** for each suspect, name the fastest test that rules it in or out. Rank by speed and how much of the remaining search space it cuts in half.
4. **Next Probe:** propose or run the single highest-information probe (not a fix). State what result confirms or eliminates the suspect, then loop: update the inventory, cross off eliminated suspects, and pick the next probe until the root cause is verified.

If a previously fixed bug resurfaces, explicitly re-test the assumptions behind the prior fix — it likely patched a symptom rather than the cause. If elimination keeps pointing at structural friction rather than a defect, stop debugging and simplify (`hammer-time`).
