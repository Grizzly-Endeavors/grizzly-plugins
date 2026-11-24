---
name: tweaks
description: Batch-tweak session for a run of small, unrelated changes (QoL touches, minor bugs, housekeeping, copy fixes) on one branch and one PR — commits each tweak as it lands and wraps up when the user says done. User-invoked ("/tweaks").
disable-model-invocation: true
---

# Tweaks

A lightweight session lane for knocking out a batch of small, unrelated changes on one branch and one PR.

## Session Flow

1. **Open or rejoin one batch branch.** Check the current branch and `git branch` for an unmerged `chore/tweaks-*` (or themed batch branch) first — a batch may span multiple sessions. Rejoin it if present; otherwise branch off the default branch as `chore/tweaks-<slug>`. If you start on an unrelated non-default branch or dirty tree, flag it before branching.
2. **Work batch by batch at full quality.** Small means small in scope, not sloppy — follow the repo's conventions (`AGENTS.md`/`CLAUDE.md`) and apply `Making Calls` (decide routine details yourself; ask only when a call passes the ask test).
3. **Commit each tweak separately.** One logical tweak, one conventional commit (`fix:`, `docs:`, `chore:`, `feat:`) before starting the next tweak so history stays clean and hooks don't tangle unrelated edits.
4. **Don't nag for exit.** After committing a tweak, report what landed and wait for the next item. Do not ask "anything else?" or "ready to merge?" — wait until the user signals done ("that's it", "ship it", "we're done").
5. **Wrap up on the user's word.** Ensure the tree is clean, push the branch (letting the repo's pre-push hook and remote CI run the full gate rather than duplicating a manual full-CI run beforehand; only run the suite manually if the repo has neither), open a PR listing the tweaks (with `closes #N` as needed), and merge end-to-end.

## When a Tweak Isn't a Tweak

If a request turns out to need a real refactor, new module, migration, or design work, pause before implementing it, name why it's larger than a tweak, and offer to file a `gh` issue so the batch stays lightweight.
