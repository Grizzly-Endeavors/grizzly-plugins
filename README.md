# grizzly-plugins

A personal [Claude Code](https://claude.com/claude-code) plugin marketplace for the Grizzly Endeavors project family. It exists so a single set of skills and agents stays in sync across every machine I work on — install once per machine, update from git, never copy files by hand again.

It ships five plugins so you only install what a given machine actually needs:

- **`grizzly-tools`** — the general-purpose toolkit: reasoning lenses, debugging discipline, code craftsmanship, test and CI discipline, planning/process, and LLM-content authoring, plus supporting agents. Useful on any project.
- **`grizzly-mail`** — an MCP server giving agents access to `claude@grizzly-endeavors.com` (mail testing), `billing@` / `admin@grizzly-endeavors.com` (company mail), and `support@goalaxi.com` (Goalaxi support mail). Only works on machines holding the 1Password operator token.
- **`grizzly-tasks`** — a skill for managing tasks in the self-hosted Vikunja from the terminal with the `vja` CLI, including first-time setup on a new machine. Only useful where a Vikunja API token can be set up.
- **`grizzly-laya`** — a skill for adding the Laya local decision model to Python projects, with bundled calibrate and fine-tune scripts. Only useful where the project can run a local GPU model.
- **`rust-build`** — Rust build speed for parallel agent worktrees: a cargo wrapper backed by a warm target-dir pool, plus worktree pruning hooks and two skills. Only useful on machines that build Rust. Its source lives in the `rust-toolkit` repo.

## Install

```
/plugin marketplace add Grizzly-Endeavors/grizzly-plugins
/plugin install grizzly-tools@grizzly-plugins
/plugin install grizzly-mail@grizzly-plugins    # optional, Grizzly machines only
/plugin install grizzly-tasks@grizzly-plugins   # optional, machines where you manage Vikunja tasks
/plugin install grizzly-laya@grizzly-plugins    # optional, machines with a CUDA GPU
/plugin install rust-build@grizzly-plugins      # optional, machines that build Rust
```

Update later with `/plugin marketplace update grizzly-plugins`.

## grizzly-tools

### Skills

**Reasoning lenses**

- **hammer-time** — simplicity-first reasoning lens for cutting through overcomplicated designs; user-invoked.
- **clean-sheet** — planning lens that designs what should exist rather than tweaking what does: Socratic goals interview, clean-sheet design, existing work mined as evidence, options priced by AI-era costs; user-invoked.
- **make-it-math** — turns a recurring frustration or vague preference into a single fitness-function equation that makes tradeoffs legible to agents, validated with a blind dry-run.
- **pull-focus** — periodic step during iterative refinement that rebuilds each area of work around one focal point, dropping stale framing and moving tangents into their own shots.

**Debugging, testing & CI**

- **white-rabbit** — anti-tunnel-vision diagnostic protocol that prevents premature convergence on a single hypothesis while debugging; user-invoked.
- **test-reliability** — patterns for making tests wait on real events instead of sleeps, raised timeouts, or retries, plus load-stress recipes for fixing flakes.
- **test-audit** — audits unit and integration tests for real behavioral signal vs fragile or over-mocked tests; user-invoked.
- **lean-ci** — designs and audits hooks, gates, CI pipelines, and agent check instructions so each check runs once at the earliest stage where it matters.

**Code quality & planning**

- **tending** — five modes (Rounds, Sweep, Distill, Gather, and unattended Garden) for making a codebase feel cared-for across code, user surfaces, and agent files; user-invoked.
- **issue-triage** — triages GitHub issues skeptically: verifies claims against code and docs, pulls out the underlying need, and brings the user only the decisions the codebase can't settle.
- **orchestrate** — Claude Code orchestration playbook: gather requirements, chunk work, and drive `scout`, `implementer`, verifier (`crank-turner`), and `reviewer` agents through to merged PRs.
- **workbench** — build an interactive diagram or browser tool as a self-contained HTML bundle in the personal workbench server (`~/workbench/tools/`).
- **adr** — create or update Architectural Decision Records in `docs/decisions/` that capture the *why* behind non-obvious decisions.
- **tweaks** — batch-tweak session lane for a run of small, unrelated changes on one branch and one PR; user-invoked.
- **working-with-llms** — concise principles for authoring and revising prompts, skills, tool descriptions, and agent instructions.

### Agents

- **scout** — answers an orchestrator's questions about a codebase and writes findings to a report file for the next agent.
- **implementer** — implements one scoped chunk from an orchestrator's brief in its own worktree and reports done, too big, or blocked.
- **crank-turner** — executes well-defined, mechanical, repetitive changes verifiable by tests/linters; also `orchestrate`'s verifier for build-heavy review chunks.
- **reviewer** — reviews an orchestrated chunk's diff against its intent and returns approve or changes-needed.
- **design-doc-reviewer** — reviews a systems-level design doc for ambiguities and missing contracts before implementation.
- **grug-code-reviewer** — reviews diffs and PRs through the anti-complexity lens of grugbrain.dev.
- **ux-nitpicker** — reviews, fixes, or designs UI/UX work for usability and WCAG 2.1 AA accessibility.
- **web-research-analyst** — verifies facts, docs, versions, and pricing against current primary web sources.

## grizzly-mail

An MCP server (single-file stdlib Python, no dependencies) bundling eight tools — `send_mail`, `list_messages`, `read_message`, `save_attachment`, `delete_message`, `move_message`, `list_folders`, `wait_for_message`, each taking an optional `mailbox` (`claude` by default, `billing`, or `support`) — plus a skill carrying the usage conventions (self-round-trip testing, cleanup, company and support mailbox handling, and the never-retry-auth rule). See [grizzly-mail/README.md](grizzly-mail/README.md).

## grizzly-tasks

- **vja** — manage tasks in the self-hosted Vikunja (todo.grizzly-endeavors.com) with the `vja` CLI: find, add, edit, complete, defer, relate, and delete tasks, plus projects and labels. Its `references/first-time-setup.md` installs and configures `vja` on a new machine.

## grizzly-laya

- **laya** — add [Laya](https://huggingface.co/convaiinnovations/laya) (a 421M-param local classifier returning calibrated probabilities for choice, score, and yes/no questions; no text generation) to a Python project at a pinned revision, with bundled `uv run` scripts to calibrate and fine-tune on labeled JSONL.

## rust-build

The plugin's source lives in the [rust-toolkit](https://github.com/Grizzly-Endeavors/rust-toolkit) repo under `plugin/`; the marketplace entry points there and tracks its default branch.

- **cargo wrapper** — on each build-type cargo run, leases a warm target directory from a per-repo pool so parallel agent worktrees stop paying for cold builds.
- **SessionStart hooks** — put the plugin's `bin/` first on `PATH` and prune `target/` directories of idle agent worktrees (Claude Code).
- **cargo-workspace-split** — skill for splitting a Cargo workspace into member crates.
- **rust-build-speed** — skill for diagnosing and speeding up Rust builds.

## License

MIT
