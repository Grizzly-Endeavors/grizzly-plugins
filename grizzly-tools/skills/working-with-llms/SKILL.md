---
name: working-with-llms
description: Guidelines for writing and revising LLM-facing content — prompts, skills, tool descriptions, agent presets, or system instructions. Use when authoring or editing instructions that will be sent to an LLM repeatedly.
---

# Working with LLMs

Write instructions for what the model actually needs, not what looks thorough to a human reader.

## Principles

- **Lead with the objective:** know the one concrete behavior change the instruction exists to produce; cut everything that doesn't serve it.
- **Outcomes over habit corrections:** describe the target result and stopping point rather than layering rules against a specific model's quirks. Re-test old workarounds on newer models by deleting them and watching.
- **Imperative and actionable:** tell the model what to do ("check X before Y") rather than stating abstract values ("X is important").
- **Earned negatives only:** add a "don't" only after observing the unwanted behavior; speculative prohibitions waste tokens and crowd out real signal.
- **Targets with stopping points:** replace unbounded absolutes ("always", "never", "every") with a closed done condition unless the invariant is genuinely absolute (such as secrets or irreversible data loss).
- **Token cost is real:** every extra paragraph competes for attention in a shared context window. Prefer concise checklists and concrete examples over prose essays.
- **Verification over hoping:** when a recurring defect matters, pair the instruction with an explicit check or mechanical guardrail rather than stronger wording.

## Self-Check Before Finishing

Re-read the draft and cut any line that fails: *"Would a frontier model behave meaningfully worse if I deleted this sentence?"*