# grizzly-plugins

A personal [Claude Code](https://claude.com/claude-code) plugin marketplace for the Grizzly Endeavors project family. It exists so a single set of skills, agents, and commands stays in sync across every machine I work on — install once per machine, update from git, never copy files by hand again.

It ships two plugins so you only install what a given machine actually needs:

- **`grizzly-tools`** — the general-purpose toolkit: reasoning lenses, debugging discipline, code craftsmanship, planning/process, LLM-content authoring, plus supporting agents and the `/clean` command. Useful on any project.
- **`grizzly-misc`** — hyper-specific skills bound to a particular tool, engine, project, or environment. Only worth installing where that context applies.

## Install

```
/plugin marketplace add Grizzly-Endeavors/grizzly-plugins
/plugin install grizzly-tools@grizzly-plugins
/plugin install grizzly-misc@grizzly-plugins   # optional, context-specific
```

Update later with `/plugin marketplace update grizzly-plugins`.

## grizzly-tools

### Skills

**Reasoning lenses**

- **grug** — the grug-brained developer persona; anti-complexity lens, user-invoked.
- **hammer-time** — simplicity-first reasoning lens for cutting through overcomplicated designs.

**Debugging & diagnostics**

- **troubleshooting** — a robust framework for anything that isn't working.
- **white-rabbit** — prevents premature convergence on a single hypothesis while debugging.

**Code quality & review**

- **wonk-check** — finds technically-correct-but-weird, needlessly-complicated, or pointless code.
- **visible-failures** — enforces the "every failure must be visible" discipline in error paths.
- **tending** — four modes (Rounds, Sweep, Distill, Gather) for making a codebase feel cared-for.
- **test-audit** — audits tests for real signal vs. false confidence.

**Planning & process**

- **phase-plan** — decompose a large refactor into a systems-level design doc and a sequence of self-contained, individually-verifiable phases.
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
- **crank-turner** — works through well-defined, mechanical, repetitive changes (migrations, mass renames) verifiable by tests/linters.
- **design-doc-reviewer** — reviews a systems-level design doc for ambiguities and missing detail before implementation; pairs with phase-plan.
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

## License

MIT
