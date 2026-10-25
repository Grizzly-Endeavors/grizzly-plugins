# grizzly-plugins

A personal [Claude Code](https://claude.com/claude-code) plugin marketplace for the Grizzly Endeavors project family. It exists so a single set of skills, agents, and commands stays in sync across every machine I work on — install once per machine, update from git, never copy files by hand again.

It ships six plugins so you only install what a given machine actually needs:

- **`grizzly-tools`** — the general-purpose toolkit: reasoning lenses, debugging discipline, code craftsmanship, planning/process, LLM-content authoring, plus supporting agents and the `/clean` command. Useful on any project.
- **`grizzly-misc`** — hyper-specific skills bound to a particular tool, engine, project, or environment. Only worth installing where that context applies.
- **`grizzly-mail`** — an MCP server giving Claude its own mailbox (`claude@grizzly-endeavors.com`) for end-to-end mail testing. Only works on machines holding the 1Password operator token.
- **`grizzly-tasks`** — a skill for managing tasks in the self-hosted Vikunja from the terminal with the `vja` CLI, including first-time setup on a new machine. Only useful where a Vikunja API token can be set up.
- **`grizzly-laya`** — a skill for adding the Laya local decision model to Python projects, with bundled calibrate and fine-tune scripts. Only useful where the project can run a local GPU model.
- **`rust-build`** — Rust build speed for parallel agent worktrees: a cargo wrapper backed by a warm target-dir pool, plus worktree pruning hooks and two skills. Only useful on machines that build Rust. Its source lives in the rust-toolkit repo.

## Install

```
/plugin marketplace add Grizzly-Endeavors/grizzly-plugins
/plugin install grizzly-tools@grizzly-plugins
/plugin install grizzly-misc@grizzly-plugins    # optional, context-specific
/plugin install grizzly-mail@grizzly-plugins    # optional, Grizzly machines only
/plugin install grizzly-tasks@grizzly-plugins   # optional, machines where you manage Vikunja tasks
/plugin install grizzly-laya@grizzly-plugins    # optional, machines with a CUDA GPU
/plugin install rust-build@grizzly-plugins      # optional, machines that build Rust
```

Update later with `/plugin marketplace update grizzly-plugins`.

## grizzly-tools

### Skills

**Reasoning lenses**

- **grug** — the grug-brained developer persona; anti-complexity lens, user-invoked.
- **hammer-time** — simplicity-first reasoning lens for cutting through overcomplicated designs.
- **pull-focus** — periodic step during iterative refinement that rebuilds each area of work around one focal point, dropping stale framing and moving tangents into their own shots.

**Debugging & diagnostics**

- **troubleshooting** — a robust framework for anything that isn't working.
- **white-rabbit** — prevents premature convergence on a single hypothesis while debugging.

**Code quality & review**

- **wonk-check** — finds technically-correct-but-weird, needlessly-complicated, or pointless code.
- **visible-failures** — enforces the "every failure must be visible" discipline in error paths.
- **tending** — four modes (Rounds, Sweep, Distill, Gather) for making a codebase feel cared-for.
- **test-audit** — audits tests for real signal vs. false confidence.

**Planning & process**

- **issue-triage** — triages GitHub issues skeptically: verifies their claims against the code and docs, pulls out the need behind non-bug issues, and brings the user only the decisions the codebase can't settle.
- **orchestrate** — run a body of work as an orchestrator: gather requirements, chunk the work, and drive scout, implementer, reviewer, and sub-orchestrator agents through to merged PRs.
- **workbench** — build an interactive diagram or browser tool as a self-contained HTML bundle in the personal workbench server.
- **adr** — create or update Architectural Decision Records that capture the *why* behind non-obvious decisions.
- **tweaks** — a batch-tweak session lane for a run of small changes on one branch/PR, user-invoked.

**Writing & LLM content**

- **working-with-llms** — the workflow for creating any LLM-facing content (prompts, skills, tool descriptions).
- **review-ready-writing** — tightens materials meant for someone else to review.

### Agents

- **library-research-specialist** — deep documentation research for unfamiliar libraries/APIs.
- **module-doc-writer** — generates a README for a code module.
- **quick-fix-handler** — handles small, non-blocking issues without interrupting the main task.
- **tlc-craftsmanship-reviewer** — elevates working code from "done" to "finished" before others build on it.
- **crank-turner** — works through well-defined, mechanical, repetitive changes (migrations, mass renames) verifiable by tests/linters; also the orchestrate skill's verifier for build-heavy review chunks.
- **design-doc-reviewer** — reviews a systems-level design doc for ambiguities and missing detail before implementation.
- **scout** — answers an orchestrator's questions about a codebase and writes the findings to a report file for the next agent.
- **implementer** — implements one scoped chunk from an orchestrator's brief in its own worktree and reports done, too big, or blocked.
- **reviewer** — reviews an orchestrated chunk's diff against its intent and returns approve or changes-needed.
- **sub-orchestrator** — runs the orchestrate playbook for one cluster on behalf of a parent orchestrator.
- **ux-nitpicker** — creates, refines, or audits UI/UX work for usability and accessibility.
- **grug-code-reviewer** — reviews diffs/PRs through the grug-brained lens, flagging premature abstraction and complexity smells.
- **web-research-analyst** — fetches accurate, up-to-date information from the web and verifies facts against current sources.

### Commands

- **/clean** — per-module code organization and cleanup.

## grizzly-misc

Context-specific skills — install only where the context applies.

- **bevy-ui** — building and debugging UI in Bevy 0.18.
- **pinchtab** — token-efficient browser automation via PinchTab.
- **jules-delegation** — delegate coding tasks to Google's Jules async agent.
- **homelab-deploy** — deploy apps to the Grizzly Endeavors homelab Kubernetes cluster.
- **residuum-brand** — Residuum's brand identity, voice, and aesthetic.

## grizzly-mail

An MCP server (single-file stdlib Python, no dependencies) bundling five tools — `send_mail`, `list_messages`, `read_message`, `delete_message`, `wait_for_message` — plus a skill carrying the usage conventions (self-round-trip testing, cleanup, the never-retry-auth rule). The launcher reads the mailbox password from 1Password once per session via the operator service-account token at `~/.config/op-tokens/operator`; see [grizzly-mail/README.md](grizzly-mail/README.md).

## grizzly-tasks

- **vja** — manage tasks in the self-hosted Vikunja (todo.grizzly-endeavors.com) with the `vja` CLI: find, add, edit, complete, defer, relate and delete tasks, plus projects and labels. Its `references/first-time-setup.md` installs and configures vja on a new machine; the API token comes from your Vikunja account settings.

## grizzly-laya

- **laya** — add [Laya](https://huggingface.co/convaiinnovations/laya) (a 421M-param local classifier returning calibrated probabilities for choice, score, and yes/no questions; no text generation) to a Python project at a pinned revision. Covers question design, monitoring AI agent runs with the `typed-decisions` checkpoint, and bundled `uv run` scripts to calibrate temperatures and fine-tune on a project's own labeled JSONL. The skill requires shutting down every process holding the model on the GPU before a session ends.

## rust-build

The plugin's source lives in the [rust-toolkit](https://github.com/Grizzly-Endeavors/rust-toolkit) repo under `plugin/`; the marketplace entry points there and tracks its default branch.

- **cargo wrapper** — on each build-type cargo run, leases a warm target directory from a per-repo pool, so parallel agent sessions in separate worktrees stop paying for cold builds.
- **SessionStart hooks** — put the plugin's `bin/` first on `PATH`, and prune `target/` directories of idle agent worktrees.
- **cargo-workspace-split** — skill for splitting a Cargo workspace into member crates.
- **rust-build-speed** — skill for diagnosing and speeding up Rust builds.

## License

MIT
