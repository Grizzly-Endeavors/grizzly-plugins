# grizzly-plugins

A personal [Claude Code](https://claude.com/claude-code) plugin marketplace for the Grizzly Endeavors project family. It exists so a single set of skills, agents, and commands stays in sync across every machine I work on — install once per machine, update from git, never copy files by hand again.

Right now it ships one plugin, `grizzly`, containing everything. It may get split into themed bundles later; for now, one plugin keeps sync friction at zero.

## Install

```
/plugin marketplace add Grizzly-Endeavors/grizzly-plugins
/plugin install grizzly@grizzly-plugins
```

Update later with `/plugin marketplace update grizzly-plugins`.

## What's inside

### Skills

- **grug** — the grug-brained developer persona; anti-complexity lens, user-invoked.
- **hammer-time** — simplicity-first reasoning lens for cutting through overcomplicated designs.
- **white-rabbit** — prevents premature convergence on a single hypothesis while debugging.
- **wonk-check** — finds technically-correct-but-weird, needlessly-complicated, or pointless code.
- **troubleshooting** — a robust framework for anything that isn't working.
- **visible-failures** — enforces the "every failure must be visible" discipline in error paths.
- **tending** — four modes (Rounds, Sweep, Distill, Gather) for making a codebase feel cared-for.
- **test-audit** — audits tests for real signal vs. false confidence.
- **working-with-llms** — the workflow for creating any LLM-facing content (prompts, skills, tool descriptions).
- **review-ready-writing** — tightens materials meant for someone else to review.
- **adr** — create or update Architectural Decision Records that capture the *why* behind non-obvious decisions.
- **tweaks** — a batch-tweak session lane for a run of small changes on one branch/PR, user-invoked.
- **bevy-ui** — building and debugging UI in Bevy 0.18.
- **pinchtab** — token-efficient browser automation via PinchTab.
- **jules-delegation** — delegate coding tasks to Google's Jules async agent.
- **homelab-deploy** — deploy apps to the Grizzly Endeavors homelab Kubernetes cluster.
- **residuum-brand** — Residuum's brand identity, voice, and aesthetic.

### Agents

- **library-research-specialist** — deep documentation research for unfamiliar libraries/APIs.
- **module-doc-writer** — generates a README for a code module.
- **quick-fix-handler** — handles small, non-blocking issues without interrupting the main task.
- **tlc-craftsmanship-reviewer** — elevates working code from "done" to "finished" before others build on it.

### Commands

- **/clean** — per-module code organization and cleanup.

## License

MIT
