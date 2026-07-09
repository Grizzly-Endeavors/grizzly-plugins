---
name: jules-delegation
description: >
  Delegate coding tasks to Google's Jules async coding agent via the Jules Tools
  CLI and Jules REST API. Use this skill whenever the user mentions Jules, wants
  to offload coding work to a background agent, asks about batch task assignment,
  wants to script TODO or GitHub issue processing into Jules sessions, or wants
  to integrate Jules into CI/CD pipelines (e.g. GitHub Actions). Also trigger
  when the user says "send this to Jules", "have Jules handle it", "delegate to
  Jules", "queue this for Jules", or references jules remote, Jules sessions, or
  the Jules API. If the user is building automation around an async coding agent
  and mentions Google or Jules by name, use this skill.
---

# Jules Delegation

Jules is an asynchronous coding agent. It runs tasks in remote cloud VMs against
GitHub repositories. You describe a task, Jules plans and executes in a VM, and
delivers results as code changes or pull requests. It is fire-and-forget — not
an interactive pair-programmer.

## Routing

Figure out what the user needs and read the right reference file.

### 1. Delegate — Run a task now
**When:** The user wants to send one or more tasks to Jules from the terminal.
Anything from "have Jules write tests for this" to "send my whole TODO list."
**Read:** `references/delegate.md`

### 2. Build — Create automation around Jules
**When:** The user wants to wire Jules into CI/CD, GitHub Actions, webhooks,
Slack bots, cron jobs, or any system that triggers Jules sessions
programmatically.
**Read:** `references/build.md`

## Writing Jules Prompts

When constructing a session prompt — whether for a single task or a batch —
write it as a bounded, concrete instruction. Jules thinks in code changes.

1. **State the goal concretely.** "Write unit tests for the auth module using
   pytest" not "improve test coverage."
2. **Scope the work.** Reference specific files, directories, or modules.
3. **Include constraints.** Framework, style guide, language version, conventions.
4. **No open-ended exploration.** Give it a task, not a question.

Bad: "Look at the codebase and see what could be improved"
Good: "Refactor src/utils/parser.ts to use the visitor pattern. Keep the public API identical. Add tests."

When the user gives a vague description, rewrite it into a Jules-ready prompt
before dispatching.
