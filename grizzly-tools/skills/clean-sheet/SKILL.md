---
name: clean-sheet
description: Step back from what currently exists and plan what should exist — a Socratic interview about goals, a clean-sheet design of what you would build today, then the current system mined for knowledge rather than treated as constraints, priced by what actually costs effort when AI writes the code. User-invoked during planning or scoping, e.g. "/clean-sheet".
disable-model-invocation: true
---

# Clean Sheet

The user invoked this because plans have been coming back as small tweaks to what already exists. For the rest of this planning discussion, treat the current code, architecture, language, libraries, and docs as evidence about the problem, not as the frame for the answer. Every option is on the table, including rewriting from scratch, changing language or framework, building in place of a dependency, removing a library, merging or splitting projects, and deleting the feature.

The only constraints are the ones the user states. Treat everything the existing system implies as open.

## What costs effort now

An agent writes the code, so a rewrite, a port, or replacing a library with your own code is hours to days of agent time. Price options by what still costs real effort:

- **Data:** migrating or risking loss of stored state.
- **Contracts:** APIs, file formats, and behavior that other systems or people rely on.
- **Behavior parity:** proving the new thing does everything the old one did that matters.
- **Deployed state:** live infrastructure, running users, and cutover.
- **The user's attention:** what they must review, verify, learn, or decide.
- **Operational risk:** what breaks in production and how fast you would know.

## Workflow

### 1. Interview the user

Interview the user Socratically about purpose and outcomes, not the implementation: what this is for, who or what depends on it, what hurts today, what great would look like, and what is fixed. Skip what the conversation already answers. When you can state the goals in one short paragraph, read it back and get the user's confirmation.

### 2. Design from a clean sheet

Write what you would build today to meet the goals if nothing existed: language, architecture, data model, dependencies, what you would build yourself, and what you would leave out. Read no more code before writing it.

If you have already seen the code or an earlier plan, check each choice that matches the current system: name the goal that requires it, or change it.

### 3. Mine the existing work

Read the current system and sort what you find into two lists:

- **Knowledge to carry forward:** edge cases it handles, requirements the interview missed, hard-won fixes, real data and contracts in use.
- **Accidental structure:** how it happens to be organized.

Revise the design to absorb the knowledge, and leave the structure behind. Take any finding that changes the goals back to the user.

### 4. Lay out the options

Draft options from the most contained change that meets the goals to the clean-sheet design, each with what it achieves and its cost in the terms above, and pick one to recommend. Before presenting, check them:

- For each part an option keeps, find the reason. If the reason is that it exists, already works, or keeps the change small, justify it from the goals or replace it.
- Remove any cost based on how much code must be written.
- If you recommend a contained change, state what the clean-sheet design would gain and why that gain is not worth its real cost.

### 5. Record the direction

Once the user picks a direction, write it to the project's design-doc location, or `docs/design/<topic>.md` if it has none: the goals, the chosen design, the knowledge carried forward, and the rejected options with one line each on why.
