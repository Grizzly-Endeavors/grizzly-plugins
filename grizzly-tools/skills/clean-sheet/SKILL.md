---
name: clean-sheet
description: Step back from what currently exists and plan what should exist — a Socratic interview about goals, a clean-sheet design of what you would build today with no existing code, then the current system mined for knowledge rather than treated as constraints, priced by what actually costs effort when AI writes the code. User-invoked during planning or scoping, e.g. "/clean-sheet".
disable-model-invocation: true
---

# Clean Sheet

The user invoked this because plans have been coming back as small tweaks to what already exists. For the rest of this planning discussion, treat the current code, architecture, language, libraries, and docs as evidence about the problem, not as the frame for the answer. Every option is on the table, including rewriting from scratch, changing language or framework, building in place of a dependency, removing a library, merging or splitting projects, and deleting the feature. A contained change is still a valid answer when the goals justify it.

## What costs effort now

Price options as if an agent writes the code: a rewrite, a port to another language, or replacing a library with your own code is agent time measured in hours to days. Leave typing effort and lines changed out of every estimate.

Price options by what still costs real effort:

- **Data:** migrating, transforming, or risking loss of stored state.
- **Contracts:** APIs, file formats, and behavior that other systems or people rely on.
- **Behavior parity:** proving the new thing does everything the old one did that matters, and the tests or verification that show it.
- **Deployed state:** live infrastructure, running users, and cutover.
- **The user's attention:** what they must review, verify, learn, or decide.
- **Operational risk:** what breaks in production and how fast you would know.

## Workflow

### 1. Interview the user

Ask about purpose and outcomes, not the implementation. Cover:

- What this is for, and who or what depends on it.
- What hurts today, in concrete cases.
- What great would look like if effort were no object.
- What is truly fixed.

If the conversation already answers some of these, draft from it and ask only about the gaps. Ask one or two questions at a time and build each question on the last answer. When the user states a constraint, ask whether it is a requirement or a fact about how things are built now. Ask why behind answers until you reach a goal the user would defend on its own terms. Continue until you can state the goals in one short paragraph, then read it back and get the user's confirmation before moving on.

### 2. Design from a clean sheet

Write what you would build today to meet the confirmed goals if nothing existed: language, architecture, data model, dependencies, what you would build yourself, and what you would leave out. Read no more code before writing it.

If you have already seen the code or an earlier plan, write the design anyway, then check it: for each choice that matches the current system, write the goal that requires it. Change any choice no goal requires, or mark it open for step 3.

### 3. Mine the existing work

Now read the parts of the current system that hold knowledge relevant to the goals: storage schemas and real data, public interfaces, tests, and fix history. Sort what you find into two lists:

- **Knowledge to carry forward:** edge cases it handles, requirements it reveals that the interview missed, hard-won fixes, real data and contracts in use.
- **Accidental structure:** how it happens to be organized, chosen for reasons that no longer apply or were never deliberate.

Revise the clean-sheet design to absorb the knowledge. Keep a piece of structure only when you can justify it from the goals, as in step 5. When a finding changes the goals, take it back to the user.

### 4. Draft the options

Draft the most contained change that meets the goals and the clean-sheet design, plus a middle option when one is meaningfully different. If the contained change and the clean-sheet design turn out the same, say so and draft one. For each, write what it achieves against the goals and its cost in the terms from "What costs effort now", then pick a recommendation.

### 5. Check, then present

Reread every option and the recommendation:

- For each part an option keeps, find the reason. If the reason is that it exists, already works, or keeps the change small, justify it from the goals or replace it.
- For each cost, confirm it names data, contracts, behavior parity, deployed state, the user's attention, or operational risk. Remove any cost based on how much code must be written.
- If you recommend a contained change, state what the clean-sheet design would gain and why that gain is not worth its real cost.
- If you recommend a larger change, name the goal the contained change fails to meet and the case from the interview that shows it.

Fix what the check finds, then present the options and the recommendation with its reason in one or two lines.

### 6. Record the direction

Once the user picks a direction, write it to the project's design-doc location, or `docs/design/<topic>.md` if it has none: the confirmed goals, the chosen design, the knowledge carried forward, and the rejected options with one line each on why. Before proposing a later change to this area, reread the doc and say whether the proposal departs from it.
