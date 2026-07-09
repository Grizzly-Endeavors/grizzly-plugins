# Sweep

One well-defined change, carried completely across every place it touches. A semantic rename that reaches forty files. Moving a module and updating everything that pointed at it. Propagating a convention to every call site. Reorganizing a directory so the structure matches how the code is actually used now.

The distinguishing quality is a mismatch between decision and reach: the *decision* is small and clear — you already know what the change is — but the *reach* is wide. That is what makes Sweep its own mode. It is too big for Rounds, which keeps each pass small and independent; but it isn't Distill or Gather, because you are not rethinking a system's core or designing a new home — you are applying a decision you've already made, everywhere it belongs, without dropping a stitch.

Where the other modes are mostly about judgment, Sweep is mostly about *thoroughness*. The care is almost entirely in completeness and consistency: leaving nothing half-changed, and leaving behavior exactly as it was.

## Is It a Sweep?

- **Rounds** — many small, unrelated cares, each self-contained. Small decision, small reach.
- **Sweep** — one change, made once, applied uniformly across many places. Small decision, wide reach.
- **Distill** — rethinking one overgrown system down to its core. Big decision, one system.
- **Gather** — designing one home for scattered logic. Big decision, cross-cutting.

If you're applying a decision you've already made to many places, it's a Sweep. If you're still deciding *what the right shape is*, it's probably Distill or Gather — decide there first, then a Sweep may be how you roll the decision out.

## The One Discipline: Completeness

A half-finished sweep is worse than never starting. Rename a concept in thirty places and miss ten, and now the codebase has two names for one thing and no signal about which is right — you've *added* the exact confusion this mode exists to remove. The same is true of a module move that leaves dangling references, or a convention applied to most call sites but not all. Partial is not "progress"; it's a new inconsistency wearing the costume of an improvement.

So a sweep is not done when it's mostly done. It's done when the old shape is *gone* — every reference, in every kind of file — or when what remains is deliberate and named as such.

## What Counts as "Every Place"

The most common way a sweep fails is by only updating the obvious surface — the code — and forgetting everywhere else the old shape lived. Before you call it complete, account for:

- **Code:** every call site, import, and reference, in every language in the repo.
- **Tests:** including fixtures, snapshots, and test names that mention the old thing.
- **Docs and comments:** READMEs, guides, inline comments, docstrings, changelogs.
- **Config and scripts:** build files, CI, deploy scripts, environment templates, Makefiles.
- **Strings and identifiers:** log messages, error text, serialized keys, API field names, database identifiers — with care, since some of these are contracts (see guardrails).
- **Agent-facing context:** the root agent file, in-repo indexes, and any `agents.md`-style pointers that name the thing you moved or renamed. A rename that leaves the code map pointing at the old path has left the sweep unfinished.

The tool that finds the stragglers is your friend here: a repo-wide search for the old name at the end, expecting zero unaccounted-for hits, is how you *know* rather than hope.

Sweep is mostly mechanical, so it leans on the example lenses less than the other modes — but if the change passes through a user- or agent-facing surface (a renamed CLI flag, a moved tool, a restructured doc), open `examples/interfaces.md` or `examples/agents.md` and make sure you carry the change through in a way that keeps those shapes intact rather than quietly degrading them.

## The Work

### 1. Pin down the change precisely

Write the transformation as a single, unambiguous rule before touching anything: "`OldName` becomes `NewName` everywhere it refers to the billing concept" or "everything under `utils/net/` moves to `network/` and imports update accordingly." The sharper the rule, the more mechanically you can apply it and the easier it is to verify. If you can't state it in a sentence, you may still be deciding — step back to Distill or Gather.

### 2. Find the full blast radius

Search the whole repo for every place the old shape appears, across all the categories above — not just the first file type that comes to mind. Know the true count before you start, so you can tell when you've reached zero.

Watch for **false matches** (the same string meaning something unrelated) and **false misses** (the same concept under a different spelling — `old_name`, `OldName`, `OLD_NAME`, `old-name`). A semantic rename follows meaning, not text; a blind find-and-replace is how sweeps introduce bugs.

### 3. Apply it uniformly

Make the *same* change the same way everywhere. The value of a sweep is its uniformity — that a reviewer can understand one instance and trust the other thirty-nine are identical in spirit. Resist improving the things you pass through. That function you're renaming also has a swallowed error? That's a Round, noted separately — folding it in breaks the "one change, applied uniformly" contract and makes the sweep unreviewable.

### 4. Preserve behavior, and verify it

A rename, a move, a reorganization must not change what the program *does*. Lean on the mechanical safety nets: the compiler or type checker for a typed language, the test suite, the linter. Run them. For contracts that reach outside the code — a serialized key, an API field, a database column, a public CLI flag — renaming the internal symbol is safe, but renaming the *external name* is a breaking change, not a sweep; treat it as its own decision with migration and compatibility, never as tidying.

### 5. Confirm completeness

Search again for the old shape. Every remaining hit is either something you missed — finish it — or something intentionally left, which you should be able to name and justify. Zero unexplained hits is the bar. Then confirm the safety nets are still green.

## Guardrails

- **All or clearly nothing.** Finish the sweep or scope it down to a subset you *can* finish completely. Never leave the repo in a half-migrated state with no marker of which shape won.
- **One change, uniformly.** No riders. Improvements you notice along the way are Rounds, tracked and done separately, so the sweep stays a single reviewable motion.
- **Behavior is held constant.** Internal renames and moves are safe; changing an external contract is a different, heavier task. Know which one you're doing.
- **Mechanical, but not blind.** Follow meaning, not raw text. Verify with the compiler and tests, not by eye.

## Done When

The old shape is gone from every kind of file — code, tests, docs, config, strings, and agent-facing context — a repo-wide search for it comes back clean, and the safety nets are green. A reviewer can read one instance of the change and trust the rest, because every instance is the same change made the same way. The codebase now speaks with one voice about the thing you swept, where before it spoke with two.
