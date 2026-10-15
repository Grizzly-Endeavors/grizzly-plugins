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
- **Review chunk** → one reviewer, covering one or more related implementation chunks that land together. When those chunks are build-heavy, one verifier builds and checks the review chunk before the reviewer reads it.
- **PR** → one batch: a whole wave or a coherent body of work, usually several review chunks. Each review chunk is reviewed before it joins the PR branch; the PR opens when the batch is done. See "Batching PRs" for how to draw the batches.
- **Cluster** → one sub-orchestrator. A self-contained area with its own several waves of implementation and review. Hand it off whole so its details never enter your context.

**Dependencies.** Launch every chunk whose inputs already exist. Chunk B depends on chunk A only when B needs something A decides or produces — an interface, a schema, a result. Editing the same files is not a dependency: merge conflicts are cheap to resolve and expensive to plan around. When B needs A's interface, you can often settle the interface in both briefs and run them together.

**Machine load.** A build in a fresh worktree starts cold, so on a compiled codebase the build, not the change, takes most of an implementer's time. Build once per review chunk instead: implementers on build-heavy chunks make the change and commit without building, and the review chunk's verifier is the agent that builds (see "Verification has one owner per layer"). Across the whole run, sub-orchestrators included, keep at most as many verifiers running at once as the repo's `CLAUDE.md` allows builds, or about one per four CPU cores (`nproc`) when it says nothing. Launch the next as one returns, and give each sub-orchestrator its share in its cluster brief. Implementers, and chunks that only touch docs, config, interpreted code, or scripts, run alongside freely.

## Picking the agent and model

| Work | Agent | Model |
|---|---|---|
| Code change, fix, merge-conflict resolution | `implementer` | Haiku (default). Raise to Opus only when the chunk needs design judgment and can't be split further. |
| Finding facts, files, and context for you or another agent | `scout` | Haiku (default) |
| Verifying a build-heavy review chunk: building it, running lint and tests, fixing mechanical failures | `crank-turner` | Haiku (default) |
| Judging a diff against its intent | `reviewer` | Opus (default) |
| A cluster with its own waves | `sub-orchestrator` | Opus (default) |
| Design doc needs a fresh-eyes check | `design-doc-reviewer` | default |

Haiku is fast and capable, especially when the brief is clear. When an Opus agent needs orientation, run a scout first and point the Opus agent's brief at the scout's report — the expensive model then spends its context on judgment, not searching.

## Writing a brief

The agent has not seen this conversation. The brief is everything it knows, so it must stand on its own:

- **Goal** — what to change and why, in a sentence or two.
- **Scope** — the files or areas in play, and what is deliberately out of scope.
- **Context** — decisions already made, interfaces to honor, conventions to follow, where to look. Hand over what you already know as facts and paths; an agent that rediscovers it burns its window.
- **Done** — what finished looks like, and which checks prove it. A cheap chunk names the targeted checks the implementer runs (the tests that cover the changed code, lint on the changed package, with the repo's documented iteration commands). A build-heavy chunk says to commit without building; its verifier runs the checks.
- **Read first** — paths to earlier reports this agent builds on: a scout's findings, the implementers' reports for a review, a review's findings for a fix, a too-big report's proposed split.
- **Branch** — what to base on and how to commit, when it matters.
- **Report to** — the absolute path where the agent writes its report.

A good brief is short and specific. If you cannot write it, you are missing a requirement — get it from the user or a scout, not by doing the work yourself.

## Reports travel as files

At the start of a run, create a run directory outside the repo — your scratchpad directory when you have one, otherwise a fresh temp directory — and give every agent an absolute path in it to write its report to, named for its chunk. Outside the repo matters: a report written inside an implementer's worktree would count as a change and could end up committed.

Every agent writes its full report to that file and returns three things: its status, a summary of a sentence or two, and the path. Route on the status and summary. When the next agent needs what a report says, put the path in its brief's **Read first** — the agent reads the original, at full detail, in its own context. Restating a report in a brief costs your context twice and loses detail in the paraphrase. When a summary doesn't add up, open the file before deciding.

## Batching PRs

CI is usually the slowest loop in a run, so spend it once per batch, not once per change.

- **Batch by what the change triggers.** Before drawing batches, find out which paths start which CI jobs and hooks: from the repo's `CLAUDE.md` when it documents them, otherwise from a `scout` that maps them from the workflow and hook config. Put the changes that start the same expensive pipeline — dependency manifests that trigger cross-platform builds, workflow files that trigger every suite — in one PR, and keep those paths out of the other batches, so that pipeline runs once.
- **Cheapen the loop first.** Land changes that make every later PR cheaper — hooks, CI config, build settings — in an early batch, ahead of the work that leans on the pipeline, and build later batches on it while it is still open (see "Stack instead of waiting for main"). A branch opened before a CI change merged still runs the old CI: merge `main` into it before it enters a merge queue whose required check only the new CI produces, or it never reports that check.
- **Hand off, don't wait.** When a batch's PR opens, hand it to the repo's merge path straight away: when the repo's `CLAUDE.md` says to use auto-merge or a merge queue, run `gh pr merge <n> --auto`, adding the merge strategy flag it names; a merge queue sets its own strategy, so there `--auto` alone is enough. Then start one wait per open PR with `run_in_background` and a `timeout` of up to 7200000, and keep working:

  ```
  until s=$(gh pr view <n> --json state,autoMergeRequest,statusCheckRollup -q 'if .state != "OPEN" then .state elif any(.statusCheckRollup[]; (.conclusion // .state) | IN("FAILURE","ERROR","CANCELLED","TIMED_OUT","ACTION_REQUIRED","STARTUP_FAILURE")) then "FAILED" elif .autoMergeRequest == null then "LEFT_MERGE_PATH" else "" end') && [ -n "$s" ]; do sleep 60; done; echo "$s"
  ```

  It prints `MERGED`, `CLOSED`, `FAILED` (a check failed), or `LEFT_MERGE_PATH` (auto-merge was cleared while the PR is still open, as when the queue ejects it). Without auto-merge or a queue, the wait is `gh pr checks <n> --watch --fail-fast >/dev/null 2>&1; echo "exit $?"`, and you merge when it exits 0.
- **Stack instead of waiting for main.** Work that depends on an open PR builds on that PR's branch, and its batch is assembled there while the PR below is in flight. Open the stacked PR, or hand it to the merge path, only after the PR below has merged (its wait prints `MERGED`, or you merged it yourself): then update its branch onto `main` (when the repo squash-merges, `git rebase --onto main <the branch below>`, so the lower PR's original commits drop out), open it against `main`, and hand it off.

## Playbook

| When this happens | Do this |
|---|---|
| Requirements are agreed for at least one chunk | Write the briefs and launch the first wave in one message. Unknowns become scouts running alongside it. |
| An implementer reports **done** | Merge its worktree branch into the branch for its review chunk. When the review chunk is complete and build-heavy, launch its verifier (see "Verify worktrees"). Otherwise launch the reviewer with the branch, the base to diff it against (what the review chunk was branched from), the intent, and the implementers' report paths. |
| A verifier reports **done** | Launch the reviewer as for a cheap review chunk, adding the verifier's report path. |
| A verifier reports **blocked** | A failure needs a decision. Make the call, or take an architecture or design question to the user, then brief an implementer with **Branch** set to the review chunk's branch, pointing at the verifier's report. Merge its branch in the verify worktree and relaunch the verifier. |
| An implementer reports **too big** | Turn its proposed split into new briefs, each pointing at its report, and launch them. The original agent's job is finished. |
| An implementer reports **blocked** | Make the call and write a new brief with the answer, pointing at its report. If it is an architecture or design question, take it to the user. |
| A merge has conflicts | Brief an implementer to resolve them, telling it what each side was for. |
| A reviewer **approves** | Merge the review chunk into its batch's PR branch. When the batch is complete, push from a warm checkout (see "Verify worktrees"), open the PR, and hand it off (see "Batching PRs"); a stacked batch waits for the PR below it to merge first. |
| A reviewer finds **must-fix** issues | Brief an implementer with the review report's path. Re-review only if the fix changed the design, not for routine fixes. |
| CI fails (the wait prints `FAILED` or exits non-zero) | Brief an implementer with the PR number, the failing check, and **Branch** set to the PR's branch; it pulls the logs itself. Merge its branch into the PR branch and push, then start a new wait for it (see "Batching PRs"). Work stacked on that PR keeps going. |
| A PR leaves the merge path without merging (the wait prints `LEFT_MERGE_PATH`) | Read why from the PR — failed checks or a conflict with main — and brief an implementer to fix it with **Branch** set to the PR's branch. Merge its branch into the PR branch, push, hand the PR back to the merge path, then start a new wait for it (see "Batching PRs"). |
| CI is green and the review approved | Auto-merge or the queue merges it; without either, merge it yourself. That is the whole verification step. |
| A report mentions a gap outside its scope | Brief an agent for it if it's in reach, otherwise open an `investigate` issue. |
| A notification says an agent stopped with background work still running | Nothing. It is waiting on its own command and will report when that finishes. |
| Agents are running and nothing has returned | Plan the next wave, gather requirements for later work, or give the user a short status. Waiting is part of the job. |
| You notice yourself about to do a small piece of work | Write a brief for it instead. |
| All work is merged | Tell the user what shipped, with PR links, and what's left open. |

## Verification has one owner per layer

Every check runs once, at the layer that owns it:

- **Implementer** — on a cheap chunk (docs, config, interpreted code, scripts), the targeted checks for what it touched, with the repo's documented iteration commands, while iterating and once at the end. On a build-heavy chunk, it makes the change and commits without building; its commit hook still runs. It never waits on CI unless its brief says so.
- **Verifier** — one per build-heavy review chunk, once its implementers' branches are merged. It builds the integrated branch once in the review chunk's verify worktree, runs lint and the tests that cover the changed code, fixes mechanical failures (lint, compile errors from moved code, unfulfilled lint expectations) and commits the fixes, and reports anything that needs a decision as **blocked**.
- **Hooks** — commit hooks run on every commit; pre-push hooks run on whoever pushes, so push from a warm checkout. When a pre-push hook is slow, run your push as a background wait like any other. A pre-push failure on your push routes to a fix brief.
- **Reviewer** — reads the diff against the brief, before the work joins its PR branch. It reads the check results in the verifier's report, or in the implementers' reports for a cheap review chunk; it does not re-run them.
- **CI** — the full suite, once per batch, on the PR.
- **You** — read the verdicts and decide. A done report, an approved review, and green CI are enough to merge.

The layers are already the safety net; another full local run before or after merging adds time and no information. In a repo with no CI, the full suite moves to one place — brief one verifier to run it once, in a verify worktree, on the integrated PR branch before merge.

## Integration

Implementers run in their own git worktrees, so parallel agents never share a checkout. Each finished implementer leaves a branch. Collect them onto the branch for their review chunk, and approved review chunks onto their batch's PR branch; a clean merge is a git command and yours to run, a conflicted one is a brief. Push, PR, and merge with `gh`, following the repo's own `CLAUDE.md` on branch naming, commit style, and PR conventions.

### Verify worktrees

A verifier needs a persistent checkout, and `implementer` can't use one: it runs isolated, and the harness refuses its git operations anywhere but its own fresh worktree. So the verifier is a `crank-turner`, which runs without isolation, working in a verify worktree you set up:

- **Create one per review chunk under verification**, at a gitignored path, starting the review chunk's branch in it: `git worktree add -b <branch> <repo>/.claude/verify-<n> <base>`. When every existing one is busy, create another, so a chunk's verification never waits for another's worktree; the "Machine load" cap is the only limit on how many run at once.
- **Keep them between runs**, and reuse an idle one with `git switch -c <branch> <base>` in it. A build at a stable path stays warm and hits its caches next run.
- **Prepare it before the first build.** Symlink dependency directories such as `node_modules` from the main checkout, and copy in the build outputs the build needs. `cp -r src dst` nests `src` inside `dst` when `dst` exists; copy `src/.` instead.
- **Assemble the review chunk there.** Merge its implementers' branches in the verify worktree, then brief the verifier with the worktree path, the branch and its base, the repo's build, lint, and test commands, and the implementers' report paths.
- **Push from a warm checkout:** a verify worktree that has built the branch, or another checkout that has. A pre-push hook that builds runs cold from a fresh agent worktree, many times slower.

## Sub-orchestrators

Hand a cluster to a `sub-orchestrator` when it would take several waves on its own and its details don't need to reach you. Its brief is a cluster brief: the goal, the requirements and decisions that bind it, the boundary of its area, its share of the verifiers (see "Machine load"), what done means (usually: PRs merged, or opened and approved), and its report path. Its own agents' reports go in a directory next to that path. It runs this same playbook one level down and reports done, too big, or blocked like any other agent. There is one level of sub-orchestration: a sub-orchestrator launches implementers, verifiers, reviewers, and scouts, and a cluster too big for one sub-orchestrator comes back to you to split.

## Keeping the user in the loop

The user sees the run through you. Give short status updates as waves land: what merged, what's in flight, what's next. Bring them architecture questions, design forks, and anything destructive or hard to reverse, with the downstream impact up front. Everything else — branching, committing, PRs, merging — you drive yourself.
