---
name: ci-audit
description: Deep, empirical audit of a repository's CI, git hooks, check scripts, test suites, build tooling, and agent check instructions against lean-ci — exposing cost/risk inversions, zero-catch paranoia machinery, and speed-first structural refactors, then turning the user's choices into a parallel orchestration plan. User-invoked (e.g. "/ci-audit", "audit my CI"). For designing checks from scratch or incremental tweaks, use lean-ci; for unit/integration test signal quality, use test-audit.
disable-model-invocation: true
---

# CI Audit

Audit the whole automated-check stack with real numbers, not assumptions. Modern agents obsessively self-validate and mirror whatever check patterns exist in a repo — left unchecked, repos accumulate slow blocking suites and thousands of lines of custom check/routing machinery that guard cosmetics while missing irreversible failures. Your goal is to expose that inversion, cut ruthlessly before adding cleverness, and leave the user with a clear direction and (once they choose) a speed-first execution plan.

Load `lean-ci` first for the check-cost formula, damage levels (`0`–`4`), and stage budgets. Stay in discussion/audit mode until the user chooses what to cut and refactor.

## 1. Gather Evidence in Parallel

Fan out read-only exploration before forming opinions. Collect facts from all four surfaces:

- **Hooks, task runners, manifests, and deploys:** every git hook (installed `.git/hooks/` vs tracked source), `justfile`/`Makefile`/`package.json` recipes (expand `ci` recipes down to leaf commands), Dockerfiles, deploy scripts, and cross-directory compile-time includes (`include_str!`, codegen, shared schemas).
- **Check scripts, path mapping, and runner configs:** all bespoke lint/check/selection scripts (count their lines of code!), test-selection/reach algorithms, linter/formatter/typechecker configs, Playwright/Vitest/Cargo/pytest runner configs, and ignore lists.
- **Agent instructions and automation:** every `AGENTS.md`, `CLAUDE.md`, project skill/command, `.claude/settings*.json` hooks, and CI-related ADRs. Search them for manual check commands (`test`, `lint`, `check`, `ci`, `build`, `just`, `npm run`, `cargo`) and compare against what hooks actually run.
- **Empirical runtime and catch data:** local `check-run` telemetry (`${XDG_STATE_HOME:-~/.local/state}/check-runs/<project>.jsonl`) if present, recent CI workflow run/step durations (`gh run list` / `gh run view`), branch protection / runner constraints, git log of recent CI/flake churn, open flake/CI issues, test counts per subproject, and host build setup (linkers like `mold`/`lld`, `sccache`, `nextest`, orphaned build dirs).

Summarize the raw findings in two tables: a **Check × Stage inventory** (`lean-ci` §1, marking `staged` / `affected` / `all` and flagging duplicates) and an **Empirical Cost vs. Catch table** (runs, failures, fail %, median/P90/max wall time, total wall time).

## 2. Interrogate Six Failure Modes

Inspect the evidence explicitly for each of these patterns:

1. **Cost/risk inversion:** checks burning blocking wait time on Level 0–1 cosmetic/internal/tooling concerns (especially 0%-failure checks!) while Level 3–4 paths (secret scanning at `pre-commit`, production auth/billing/backup/deploy workers, real cross-boundary integration tests, clean-branch deploy guards) go unchecked.
2. **Stage duplication and budget blowouts:** identical checks running across commit, push, CI, deploy, and agent instructions; `pre-commit` blowing its ~15s budget; missing fail-fast between cheap static checks and slow suites; missing gate log files (causing lost failure output on truncation); hooks mutating unstaged working-tree edits; missing failure traces/artifacts.
3. **Selection and reach illusions:** custom test-selection or path-mapping scripts that silently escalate to full suites on routine edits (measure the actual escalation rate!), miss transitive dependencies or orphan specs, or pull unrelated upstream `main` commits into a branch's push gate when `remote_sha..HEAD` isn't intersected with `origin/main..HEAD`.
4. **Paranoia monuments and meta-machinery:** bespoke AST/regex policy linters, meta-tests, reach graphs, sharding, and lock queues that only exist because suites grew slow — plus bloated test templates (e.g. full-browser state-matrix specs or hundreds of inline accessibility scans) that agents keep copying instead of writing fast unit tests.
5. **Build and runner waste:** redundant installs or builds across CI jobs (e.g. reinstalling browsers or rebuilding artifacts per shard), unpinned toolchains causing double downloads, missing fast linkers/caches (`mold`/`lld`, `sccache`, `nextest`), or monolithic crates/packages forcing full rebuilds.
6. **Agent instruction drift:** skills or `AGENTS.md` instructing agents to manually duplicate hook checks, contradicting actual hooks/workflows, or keeping stale ADRs that anchor agents to obsolete guardrails.

## 3. Apply the Four-Bucket Cut (Subtract Before Optimizing)

Before proposing new caching or routing machinery to cope with slow checks, sort every check into four buckets:

- **Delete outright:** zero-catch bespoke policy checkers, duplicate linters, meta-tests, and selection/locking plumbing that evaporates once blocking suites are small.
- **Demote to on-demand agent CLI tools:** scoped single-file, single-asset, or single-route checks an agent invokes while actively authoring that surface, instead of blocking every commit or push.
- **Keep in the fast blocking critical gate:** Level 2–4 defects only — fast `pre-commit` (secret scan + format wholly-staged files only, ~seconds) and a single fail-fast gate covering affected-project lint/typecheck/unit/build plus curated critical user journeys.
- **Move off the critical path (scheduled/nightly):** broad regression suites, full accessibility/perf sweeps, dependency/advisory audits, and external/networked checks — especially when an automated issue or remediation workflow catches escapes.

Flag **anti-paranoia steering** too: the codebase itself is the strongest steering for future agents. Deleting bloated check/test templates and stating concise test-boundary rules in `AGENTS.md` prevents agents from rebuilding the labyrinth.

## 4. Price Structural ("Boil the Ocean") Refactors by Agent-Era Cost

Do not hold back big structural refactors that agents can execute quickly and that permanently improve every future iteration (splitting monolithic crates/packages, pre-baking CI runner images, build-once artifact fan-out in CI, decoupling slow assertions like accessibility scans from functional e2e specs, adding deterministic stubs so real cross-service integration tests can run in the gate).

Filter every structural proposal against Step 3: **explicitly drop** clever infrastructure (such as bespoke content-addressed caches or complex reach graphs) that radical subtraction already makes unnecessary.

## 5. Present Calls First; Produce a Speed-First Plan When Ready

Deliver the audit report concisely and surface at most 3 high-stakes architectural decisions (e.g., what moves from blocking to scheduled, how aggressively to prune vs. demote suites, which structural refactors to include). Do not edit repo files during the audit.

Once the user confirms direction and asks for an execution plan (especially for handoff to `/orchestrate` or another agent session), structure the plan to avoid common agent execution traps:

- **Put `Decided by: <user>` bindings at the top** listing every check authorized for deletion or demotion, so executing agents do not hesitate to remove checks or keep them "just in case."
- **Make Wave 0 unblock speed first:** land host build speedups and the fast critical gate to `main` *before* starting cleanup or refactor PRs, so every follow-on PR lands in seconds instead of waiting on the old slow gate.
- **Organize remaining work as a parallel DAG (Waves), not a serial checklist:** group independent chunks across disjoint directories or repos to run concurrently in separate worktrees.
- **Ban meta-guardrails and over-verification:** forbid adding "checks against new checks" or running full suites manually; specify the single narrow verification command for each chunk and end with `lean-ci` §6 spot-checks.
- **Place multi-repo plans outside the product repos** (uncommitted) when the work spans application repos, infrastructure/runner repos, and host setup.
