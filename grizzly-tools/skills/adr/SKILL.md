---
name: adr
description: Create or update Architecture Decision Records in docs/decisions/. Use only when a named person makes a hard-to-reverse decision, when an external/infrastructure constraint forces a non-obvious architecture, or when the user explicitly invokes /adr. Do not write ADRs for routine implementation choices or agent defaults.
---

# Architectural Decision Records

ADRs capture consequential, hard-to-reverse decisions that cannot be read out of the code. They live in `docs/decisions/` and are numbered sequentially.

## When to Write an ADR

An ADR must clear **at least one** of these two bars:

- **A named person made a consequential, hard-to-reverse decision** (product/business boundary, security/legal posture, public schema/API commitment, or an explicit preference that future sessions must not overturn).
- **An outside system you do not control forced a non-obvious constraint** (hardware quirk, network topology, vendor limit, OS/protocol behavior — common in infrastructure repos like `grizzly-platform`).

**Do NOT write an ADR for:**

- **Agent defaults or routine implementation choices** (UI layout, component wiring, internal module shape, local abstractions, reversible code structure). If an agent chose it without the user explicitly deciding it, it does not get an ADR.
- **Reverting an unnecessary or unattributed ADR.** Delete the old ADR instead — git holds history. Never write a new ADR whose main purpose is undoing an earlier ADR that didn't need to exist.

## Format

File naming: `NNNN-short-title.md` (e.g., `0001-mergerfs-over-zfs-for-storage.md`). To determine the next number, list existing files in `docs/decisions/`.

```markdown
# NNNN: Short Decision Title

**Date:** YYYY-MM-DD
**Status:** accepted | superseded by NNNN | deprecated
**Decided by:** a person's name (required for decision ADRs; omit only for pure external-constraint records)

## What they said

Present whenever a person decided. Quote what they said, verbatim, from the session. Do not paraphrase or tidy it. A later reader gets their words, not an interpretation of them.

## Context

What situation, external constraint, or problem prompted this decision? Keep it to 2-4 sentences. Name the specific machines, services, or external limits involved.

## Decision

What was decided? Be specific — name the tool, config, topology, or boundary. 1-3 sentences.

## Alternatives Considered

- **Alternative A** — Why it was rejected (1 sentence)
- **Alternative B** — Why it was rejected (1 sentence)

Only include alternatives that were genuinely considered. Skip this section if an external constraint left only one viable option.

## Consequences

- What gets easier or better
- What gets harder or is now a limitation
- What future decisions this constrains or enables
```

## Authority

Only a record that names a person (`Decided by: Bear`) or documents a verifiable external constraint carries authority for later work. Do not write `Decided by: agent` ADRs. When encountering an older unattributed ADR in a repo, treat it as an unverified guess a prior agent made — never cite it as a veto against the user or a reviewer's finding, and delete it if the code moves on.

## Process

1. Check `docs/decisions/` for existing ADRs — avoid duplicates, and check whether an existing unattributed ADR should simply be deleted instead of superseded.
2. Determine the next number.
3. Write the ADR using the format above. Keep it readable in under 60 seconds.
4. Only use `superseded by NNNN` when replacing a genuinely consequential `Decided by: <person>` or external-constraint ADR whose premises changed. Otherwise delete the obsolete ADR.
