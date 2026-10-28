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

A check earns its CPU time by catching a defect the change could have introduced, at the earliest stage where it can. Every other run of it is waste. Build the setup so a one-line docs change lands in seconds and a code change runs each relevant check once.

## 1. Inventory every place a check runs

Before adding or changing anything, build a table with one row per check (format, lint, typecheck, unit tests, e2e, build, audit, perf, link check) and one column per stage. Fill it from all of these:

- Git hooks (`.githooks/`, `.husky/`, `lefthook.yml`, `.pre-commit-config.yaml`) and the recipes they call (`justfile`, `Makefile`, `package.json` scripts). Follow each recipe down to the commands it runs, since `ci` recipes often contain `lint` again.
- Remote CI (`.github/workflows/`, `.gitlab-ci.yml`, etc.) for PR, push to main, merge queue, tag, deploy and schedule triggers.
- Deploy pipelines and scripts (Flux, Argo, Dockerfiles that run tests in a build stage).
- Agent instructions: `CLAUDE.md` and `AGENTS.md` at every level, project skills and commands (`.claude/skills/`, `.claude/commands/`), agent definitions, and plugin skills the project's agents load. Search them for `test`, `lint`, `check`, `ci`, `build`, `clippy`, `tsc`, `just`, `npm run`.
- Claude Code hooks in `.claude/settings.json` and `settings.local.json` (a `PostToolUse` hook that runs tests after every edit counts as a stage).
- Orchestration workflows where an implementer, a verifier and a reviewer each run the suite.

Mark each cell with what it runs on: staged files, the affected projects, or everything.

## 2. Give each check one home

Each check blocks at exactly one stage: the earliest one where its input exists and it runs fast enough.

| Stage | Runs | Budget |
|---|---|---|
| Claude Code edit hooks | At most a formatter or linter on the edited file | About a second |
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
- **Failures in code the change didn't touch:** call a failure pre-existing only after reproducing it on the base commit. Then fix it, or file an `investigate` issue with the full output, and scope the check to the change.
- **Advisory output** (dependency updates, complexity metrics): report it in a scheduled run.

A test that fails intermittently is a broken test, not a non-blocking one. It blocks until it's fixed with test-reliability. Never retry, skip or reclassify it.

A change that adds or tightens a rule fixes every existing violation in the same change, so scoping lint to staged files never hides old violations of a new rule.

Agents ignore warnings, so warnings that print and pass aren't a third option. Every check either blocks or routes its findings to an issue or report someone reads.

Removing a duplicate run of a check on the same input needs no approval. Moving a check off its blocking stage, or deleting a check, relaxes the project's guardrails: propose it with the numbers from §6 and wait for the user's answer.

## 5. Keep the machine usable and the output complete

- Build once and reuse the output across the checks that need it (e2e and perf on the same production build).
- Run builds one at a time rather than several at once, and size test workers per test-reliability's runner settings.
- Run every selected check to the end, even after one fails, then print a summary of each check's result, so one push shows every failure.

### Hook correctness

- Start each git hook with `unset $(git rev-parse --local-env-vars)`, since in a linked worktree git's hook variables change what nested git calls see.
- Install hooks as small dispatchers that run `$(git rev-parse --show-toplevel)/<hook source dir>/<hook>`. The hooks directory is shared by every worktree, so a symlink would run one checkout's copy.
- Judge the commit being pushed: refuse when the pushed sha isn't HEAD or tracked files have uncommitted changes, or check the pushed commit out in a temporary `git worktree`.

## 6. Prove the setup

After building or changing checks, measure them and put the numbers in the PR:

1. **Time three changes end to end**, from commit to the gate passing: a docs-only change, a one-file change in a leaf project, and a change to a shared dependency. The docs-only change must run no test suite and finish in seconds. The leaf change must not run other projects' suites.
2. **Time pre-commit on a typical commit** against its ~15 s budget, and confirm the machine stays responsive (a browser and editor still usable) while the gate runs.
3. **Count runs per check** for one change from commit to deploy, including what the agent instructions tell agents to run. Any check that runs twice on the same input is a finding to fix.
4. **Touch a path the mapping doesn't know** and confirm every check runs.
5. **Make one check fail on purpose** and confirm the others still run and the summary names the failure.
6. **Run the hooks from a linked worktree** and confirm a nested `git log` shows that worktree's history.
