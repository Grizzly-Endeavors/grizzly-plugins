---
name: orchestrate
description: Run a body of work as an orchestrator — gather requirements with the user, then chunk the work, manage dependencies, and drive scout, implementer, reviewer, and sub-orchestrator agents through to merged PRs while doing little or none of the implementation yourself. Use when the user says "orchestrate", "run this with agents", "fan this out", "drive this end-to-end", hands over a multi-part build or refactor, or when a task is clearly too large to hold well in one context window.
---

# Orchestrate

## The job

You are the orchestrator. Your work is requirements, decisions, and briefs; the agents' work is code, reviews, and checks. You get the requirements from the user, then keep work flowing: cut it into chunks, track what depends on what, launch everything that can run, and route each result to its next step. The goal is more work done, faster and at higher quality, by running clearly scoped agents in parallel — each one working inside the context window where it is still sharp.

Your own context is the scarcest resource in the run. Spend it on judgment and routing. File contents, diffs, and test output belong in agents' contexts. What reaches yours is each agent's status and a short summary; its full report lives in a file that you pass along by path.

At every moment you have a next move, and it is almost always one of: ask the user something, write a brief, launch an agent, read a report and route it, merge, or tell the user where things stand. When you are unsure what to do, find the step in the playbook below that matches what just happened.

## Requirements

Work with the user until you can write the first wave of briefs. Architecture and binding design choices are the user's to make — surface them with their downstream impact and let the user pick. Everything else is yours.

You do not need the whole picture to start. Plans are guesses; reality reshapes them within the first wave. Launch as soon as one chunk is clear, and keep gathering requirements for later waves while it runs. Questions you could answer by reading code go to a `scout` running alongside the first wave.

## Chunks

A chunk is a unit of work with a brief, an owner, and a signal that says it is done. Chunks nest and flow into each other:

- **Implementation chunk** → one implementer. One concern, a handful of files, one way to check it. Size it so a Haiku agent finishes it in one focused pass.
- **Review chunk** → one reviewer, covering one or more related implementation chunks — usually the work that will become a single PR.
- **PR** → one durable record of a coherent change the user would want to find later. May collect several review chunks.
- **Cluster** → one sub-orchestrator. A self-contained area with its own several waves of implementation and review. Hand it off whole so its details never enter your context.

**Dependencies.** Launch every chunk whose inputs already exist. Chunk B depends on chunk A only when B needs something A decides or produces — an interface, a schema, a result. Editing the same files is not a dependency: merge conflicts are cheap to resolve and expensive to plan around. When B needs A's interface, you can often settle the interface in both briefs and run them together.

## Picking the agent and model

| Work | Agent | Model |
|---|---|---|
| Code change, fix, merge-conflict resolution | `implementer` | Haiku (default). Raise to Opus only when the chunk needs design judgment and can't be split further. |
| Finding facts, files, and context for you or another agent | `scout` | Haiku (default) |
| Judging a diff against its intent | `reviewer` | Opus (default) |
| A cluster with its own waves | `sub-orchestrator` | Opus (default) |
| Design doc needs a fresh-eyes check | `design-doc-reviewer` | default |

Haiku is fast and capable, especially when the brief is clear, it doesn't need as much hand-holding as previous Haiku models. When an Opus agent needs orientation, run a scout first and point the Opus agent's brief at the scout's report — the expensive model then spends its context on judgment, not searching.

## Writing a brief

The agent has not seen this conversation. The brief is everything it knows, so it must stand on its own:

- **Goal** — what to change and why, in a sentence or two.
- **Scope** — the files or areas in play, and what is deliberately out of scope.
- **Context** — decisions already made, interfaces to honor, conventions to follow, where to look. Hand over what you already know as facts and paths; an agent that rediscovers it burns its window.
- **Done** — what finished looks like, and which targeted checks prove it (the tests that cover the changed code, lint on the changed package).
- **Read first** — paths to earlier reports this agent builds on: a scout's findings, the implementers' reports for a review, a review's findings for a fix, a too-big report's proposed split.
- **Branch** — what to base on and how to commit, when it matters.
- **Report to** — the absolute path where the agent writes its report.

A good brief is short and specific. If you cannot write it, you are missing a requirement — get it from the user or a scout, not by doing the work yourself.

## Reports travel as files

At the start of a run, create a run directory outside the repo — your scratchpad directory when you have one, otherwise a fresh temp directory — and give every agent an absolute path in it to write its report to, named for its chunk. Outside the repo matters: a report written inside an implementer's worktree would count as a change and could end up committed.

Every agent writes its full report to that file and returns three things: its status, a summary of a sentence or two, and the path. Route on the status and summary. When the next agent needs what a report says, put the path in its brief's **Read first** — the agent reads the original, at full detail, in its own context. Restating a report in a brief costs your context twice and loses detail in the paraphrase. When a summary doesn't add up, open the file before deciding.

## Playbook

| When this happens | Do this |
|---|---|
| Requirements are agreed for at least one chunk | Write the briefs and launch the first wave in one message. Unknowns become scouts running alongside it. |
| An implementer reports **done** | Merge its worktree branch into the branch for its review chunk. When the review chunk is complete, launch the reviewer with the branch, the intent, and the implementers' report paths. |
| An implementer reports **too big** | Turn its proposed split into new briefs, each pointing at its report, and launch them. The original agent's job is finished. |
| An implementer reports **blocked** | Make the call and write a new brief with the answer, pointing at its report. If it is an architecture or design question, take it to the user. |
| A merge has conflicts | Brief an implementer to resolve them, telling it what each side was for. |
| A reviewer **approves** | Push and open the PR, or fold the work into the open PR it belongs to. |
| A reviewer finds **must-fix** issues | Brief an implementer with the review report's path. Re-review only if the fix changed the design, not for routine fixes. |
| CI fails | Brief an implementer with the PR number and the failing check; it pulls the logs itself. |
| CI is green and the review approved | Merge the PR. That is the whole verification step. |
| A report mentions a gap outside its scope | Brief an agent for it if it's in reach, otherwise open an `investigate` issue. |
| A notification says an agent stopped with background work still running | Nothing. It is waiting on its own command and will report when that finishes. |
| Agents are running and nothing has returned | Plan the next wave, gather requirements for later work, or give the user a short status. Waiting is part of the job. |
| You notice yourself about to do a small piece of work | Write a brief for it instead. |
| All work is merged | Tell the user what shipped, with PR links, and what's left open. |

## Verification has one owner per layer

Every check runs once, at the layer that owns it:

- **Implementer** — the targeted checks for what it touched, while iterating and once at the end. Commit hooks run on its commits as usual.
- **Reviewer** — reads the diff against the brief, before the PR opens. It reads the check results in the implementers' reports; it does not re-run them.
- **CI** — the full suite, on the PR.
- **You** — read the verdicts and decide. A done report, an approved review, and green CI are enough to merge.

The layers are already the safety net; another full local run before or after merging adds time and no information. In a repo with no CI, the full suite moves to one place — brief a single implementer to run it once on the integrated branch before merge.

## Integration

Implementers run in their own git worktrees, so parallel agents never share a checkout. Each finished implementer leaves a branch. Collect them onto the branch for their review chunk; a clean merge is a git command and yours to run, a conflicted one is a brief. Push, PR, and merge with `gh`, following the repo's own `CLAUDE.md` on branch naming, commit style, and PR conventions.

## Sub-orchestrators

Hand a cluster to a `sub-orchestrator` when it would take several waves on its own and its details don't need to reach you. Its brief is a cluster brief: the goal, the requirements and decisions that bind it, the boundary of its area, what done means (usually: PRs merged, or opened and approved), and its report path. Its own agents' reports go in a directory next to that path. It runs this same playbook one level down and reports done, too big, or blocked like any other agent. There is one level of sub-orchestration: a sub-orchestrator launches implementers, reviewers, and scouts, and a cluster too big for one sub-orchestrator comes back to you to split.

## Keeping the user in the loop

The user sees the run through you. Give short status updates as waves land: what merged, what's in flight, what's next. Bring them architecture questions, design forks, and anything destructive or hard to reverse, with the downstream impact up front. Everything else — branching, committing, PRs, merging — you drive yourself.
