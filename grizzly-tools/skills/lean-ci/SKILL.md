---
name: lean-ci
description: >
  Use when setting up, designing, adding to, changing or auditing a project's
  automated checks: git hooks, pre-commit and pre-push gates, CI pipelines, PR,
  merge and deploy checks, scheduled runs, and the agent instructions, skills,
  Claude Code hooks and agent workflows that tell agents to run tests, lint or
  builds. Also use when CI is slow, when there are too many checks, when a small
  or docs-only change takes a long time to land, when a commit or push bogs
  down the machine, when the same check seems to run at several stages, or
  when a check blocks on failures the change didn't cause. For making
  individual tests reliable (flakes, waits, timeouts, runner settings), use
  test-reliability.
---

# Lean CI

A check earns its wait and machine time by catching a defect the change could have introduced, at the earliest stage where it can. Every other run of it is waste. Build the setup so a one-line docs change lands in seconds and a code change runs each relevant check once.

Every check run is judged by one tradeoff:

```
score = (unchecked change × issue rate × damage × in time) − (wait time + machine time)
```

- **Unchecked change:** lines the check can see that it hasn't already passed on.
- **Issue rate:** real defects this kind of check finds per line it sees.
- **Damage & in time:** minutes of waiting worth trading to stop one defect reaching users, and whether the check catches it in time (1 if it blocks release or runs within the level's tolerance window, else 0):

| Level | Worst outcome if a defect slips through | Worth | Tolerance |
|---|---|---|---|
| 0 | Cosmetic or internal only (docs, tests, tooling) | <1 min | Blocking only |
| 1 | Visible glitch, nothing lost | 5 min | 3 days |
| 2 | Users blocked until fixed | 1 hour | Must block release |
| 3 | Costs real money or users | 1 day | Must block release |
| 4 | Irreversible (lost data, wrong charges, leaked secrets) | 1 week | Must block release |

- **Wait time + machine time:** wall-clock minutes anything waits on the result, plus core-minutes divided by machine cores (including follow-on work thrown away when a cheap check fails after expensive work started).

Running a 10-minute suite on a 3-line or docs-only change, or repeating a check on content it already passed on, is negative score — waste.

## 1. Inventory every place a check runs

Before adding or changing anything, build a table with one row per check (format, lint, typecheck, unit tests, e2e, build, audit, perf, link check) and one column per stage. Fill it from all of these:

- Git hooks (`.githooks/`, `.husky/`, `lefthook.yml`, `.pre-commit-config.yaml`) and the recipes they call (`justfile`, `Makefile`, `package.json` scripts). Follow each recipe down to the commands it runs, since `ci` recipes often contain `lint` again.
- Remote CI (`.github/workflows/`, `.gitlab-ci.yml`, etc.) for PR, push to main, merge queue, tag, deploy and schedule triggers.
- Deploy pipelines and scripts (Flux, Argo, Dockerfiles that run tests in a build stage).
- Agent instructions: `CLAUDE.md` and `AGENTS.md` at every level, project skills and commands (`.claude/skills/`, `.claude/commands/`), agent definitions, and plugin skills the project's agents load. Search them for `test`, `lint`, `check`, `ci`, `build`, `clippy`, `tsc`, `just`, `npm run`.
- Agent edit hooks (e.g. Claude Code `PostToolUse` hooks in `.claude/settings.json` — a hook running tests after every edit counts as a stage).
- Orchestration workflows where an implementer, a verifier and a reviewer each run the suite.

Mark each cell with what it runs on: staged files, the affected projects, or everything.

## 2. Give each check one home

Each check blocks at exactly one stage: the earliest one where its input exists and it runs fast enough.

| Stage | Runs | Budget |
|---|---|---|
| Agent edit hooks | At most a formatter or linter on the edited file | About a second |
| Agent iterating | The narrowest test for the code being changed (one file, one test name, one crate) | Seconds |
| Pre-commit | Lint and secret scan on the staged files; typecheck of the projects they belong to if it fits the budget, else at the gate. Formatters fix and re-stage only through a tool that stashes unstaged changes first (lint-staged, pre-commit); otherwise fail and print the fix command | Under ~15 s |
| The gate: PR when the repo has remote CI with a required status check, otherwise pre-push, never both | The tests and builds of the projects the change affects, plus the projects that depend on them | A few minutes |
| Merge | Nothing, when the landed tree equals the gated tree (fast-forward, rebase then gate, merge queue). Require the branch to be up to date, or use a merge queue, rather than rerunning after merge | None |
| Deploy | Build the artifact once and deploy that artifact. Run only deploy-level checks (smoke test, health check, migration dry run) | Minutes |
| Scheduled | The broad, slow or networked checks: full cross-project suites, stress runs, dependency audits, external link checks, full perf runs | Off the critical path |

For each check that appears in more than one cell, keep one and delete the rest, unless its input differs between those stages: a merge onto a main that changed underneath it, a platform the project ships to, or the built artifact rather than the source. Write that difference down next to the check.

Rewrite agent instructions to match the table. Tell agents which hook or CI job already runs the full check, and to run only the narrow test for what they're iterating on. Replace "run `just ci` before committing" with what the hooks run and the narrow command to use while iterating. After a hook or CI job passes, agents don't rerun it to confirm. When an orchestration has a verifier, implementers and reviewers read its results instead of rerunning them.

## 3. Run only what the change can affect

- Map changed paths to the checks of the projects they belong to and of the projects that import them.
- Map docs, prose and agent-instruction paths to their own checks only (prose lint, link check), or to none. A path counts as docs only if no build or test reads it (`include_str!`, doctests, MDX, copy files), so grep for it before mapping it narrowly.
- Map lockfiles, toolchain files, shared lint config, and the hook and CI files themselves to every check that reads them.
- Send a path the mapping doesn't know to every check, so a mapping gap makes the gate check more, never less.
- Give the mapping its own test cases, and keep the full run available as one command.
- Use the tools' own change detection where it's reliable (`cargo test -p`, `vitest --changed`, `nx affected`).
- To skip a check whose input hasn't changed since it passed, key the cache on a content hash of the inputs, the tool config and the lockfile, never on timestamps.

## 4. Decide what blocks

Block on a failure when all three hold:

1. The change could have caused it: it's in the code the change touches or in code that depends on it.
2. It's deterministic: the same commit fails every time.
3. It means something is broken: the build fails, a test fails, the types don't check, a secret is committed, or a lint rule the project chose to deny fires.

Don't block on these. Send each one somewhere it gets acted on instead:

- **Network, third-party services, or shared-machine timing** (external link checks, registry lookups, perf budgets and scores measured on a busy machine): move it to a scheduled run that files or updates an issue when it fails.
- **Failures in code the change didn't touch:** don't spend another full run reproducing them on the base commit — record the failure (file an `investigate` issue with the output if not already tracked), scope the check to the change when feasible, and carry on.
- **Advisory output** (dependency updates, complexity metrics): report it in a scheduled run.

A flaky test in the code you changed is a defect to fix with `test-reliability` (never mask it with retries or sleeps). A pre-existing intermittent flake in untouched code should be filed as an issue rather than holding up unrelated changes indefinitely.

A change that adds or tightens a rule fixes every existing violation in the same change, so scoping lint to staged files never hides old violations of a new rule.

Agents ignore warnings, so warnings that print and pass aren't a third option. Every check either blocks or routes its findings to an issue or report someone reads.

**Treat adding and removing recurring check cost symmetrically.** Removing a duplicate run on the same input needs no approval. Adding a new recurring check — or deleting / moving an existing blocking check off the critical path — both change the project's cost/safety tradeoff and should be justified by how often the defect occurs and what it costs if it slips through.

## 5. Keep the machine usable and the output complete

- Build once and reuse the output across the checks that need it (e2e and perf on the same production build).
- Run builds one at a time rather than several at once, and size test workers per `test-reliability`'s runner settings.
- Write full gate output to a log file and print the path so agents never re-run a slow gate just to read truncated output.
- Fail fast when a cheap check fails before starting an expensive downstream check on a tree that is about to change.

### Hook correctness

- Start each git hook with `unset $(git rev-parse --local-env-vars)`, since in a linked worktree git's hook variables change what nested git calls see.
- Install hooks as small dispatchers that run `$(git rev-parse --show-toplevel)/<hook source dir>/<hook>`. The hooks directory is shared by every worktree, so a symlink would run one checkout's copy.
- Judge the commit being pushed: refuse when the pushed sha isn't HEAD or tracked files have uncommitted changes, or check the pushed commit out in a temporary `git worktree`.

## 6. Spot-check the setup

After changing hooks or CI, confirm the invariants that matter most without turning verification into a multi-hour ritual:

1. A docs-only change runs no test suite and finishes in seconds; a leaf change does not run unrelated suites.
2. Pre-commit stays within its ~15 s budget and leaves the machine responsive.
3. No check runs twice on the same input across commit, push, CI, and agent instructions.
4. Hooks invoked from a linked worktree resolve that worktree's repo and history cleanly.
