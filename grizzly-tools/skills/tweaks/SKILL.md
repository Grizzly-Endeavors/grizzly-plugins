---
name: tweaks
description: Batch-tweak session for this project — a lightweight lane for a run of small, unrelated changes (minor QoL, small bug fixes, repo housekeeping, copy fixes, tuning) that don't each deserve their own plan/implement/verify/commit/PR cycle. Branches once (or rejoins an in-progress batch branch, possibly across several sessions), then takes tweaks batch-by-batch — implementing and committing each — and stays in that mode until you say you're done, at which point it pushes, opens a PR, and merges.
disable-model-invocation: true
---

# Tweaks

A session mode for the small stuff. The user has a handful of little changes — a
QoL touch here, a one-line bug there, some repo housekeeping — and doesn't want
the ceremony of a full plan/PR flow for each one. `/tweaks` collapses all of that
into a single branch and a single PR, while you knock the changes out one at a
time.

This skill is user-invoked only (`disable-model-invocation` in the frontmatter) —
it loads solely when the user types `/tweaks`, never on its own. It's for a *run*
of small changes the user wants to batch; a lone request still goes through the
normal flow.

## The shape of a session

1. **Open the branch once — or rejoin it.** A batch lives on a single feature
   branch. **The user may spread one batch across several Claude sessions on that
   same branch, so before you create anything, check whether a batch branch is
   already in progress** — look at the current branch and `git branch` for an
   unmerged `chore/tweaks-*` (or a differently-themed batch branch). If one exists,
   check it out and pick up where it left off; do **not** open a second branch. Only
   when there's no batch branch yet do you cut one off the default branch: default
   the prefix to `chore/` with a short descriptive slug — `chore/tweaks-<slug>` —
   unless the user's first message makes a better theme obvious (e.g. all typo
   fixes). One branch holds the whole batch across every session; don't spin up a
   new branch per tweak or per session.

2. **Take tweaks batch by batch — and slow down.** The user hands you one or a few
   changes at a time. These small touches are *the* things that make a project feel
   cared for, so treat them that way — don't rush them out. Take the time to do each
   one right and hold the same quality bar the rest of the repo does (see the
   project's `CLAUDE.md` and any local conventions): no cruft, elegant over fast,
   visible failures, tests for pure logic that lands. Small means small in scope,
   never quick-and-sloppy. **If anything about a request is ambiguous, ask before
   implementing** instead of guessing — a wrong guess costs far more than the
   question, and getting these right is the whole point.

3. **Commit each change as you finish it.** One logical tweak, one commit, with its
   own appropriate conventional prefix — a bug fix is `fix:`, a copy change is
   `docs:` or `chore:`, a small feature is `feat:`. Don't let several unrelated
   tweaks pile into one commit. Commit the finished tweak *before* starting the
   next one — if a pre-commit hook runs `git add -u`, anything tracked and modified
   rides along on the next commit whether you meant it to or not. Staging and
   committing one tweak at a time keeps the history honest.

4. **Keep going without nagging.** After a tweak lands, do **not** ask "anything
   else?" or "should I merge now?" or otherwise fish for the exit. Assume there's
   more coming. Just report what you did, that it's committed, and wait for the
   next one. The user will tell you plainly when the session is over — phrases like
   "that's it", "we're done", "ship it", "let's merge". Only then do you move to
   wrapup.

5. **Wrap up on the user's word.** When the user signals done:
   - Make sure everything is committed and the tree is clean.
   - Run the project's full CI / verification gate (the static gates + smoke — e.g.
     whatever `just ci-full`, `make check`, or the project's equivalent is) so the
     branch is green before it goes up; a per-commit pre-commit hook usually only
     runs a lighter gate.
   - Push the branch, open a PR, and merge it. Drive this end-to-end without
     pausing for permission on the git mechanics — branching, pushing, and merging
     aren't approval points here (see the "Driving Work End-to-End" and Git
     Workflow guidance in the project's `CLAUDE.md`).
   - The PR body is the record of the batch: a short bullet list of the tweaks that
     landed. Reference any issues the tweaks close with `closes #N`.

## When a "tweak" isn't a tweak

Some requests look small but aren't — they'd need a real refactor, a new module, a
migration, or a chunk of design work. Those don't belong in a tweak session:
they'd bloat the batch, they deserve their own plan and PR, and they're exactly the
kind of thing the user tracks as issues.

When you spot one, **stop before implementing it** and say so plainly: name what
makes it bigger than a tweak (the surface it touches, the design decision it
forces), and offer to open a GitHub issue capturing it instead — so it's not lost
and the tweak session stays lightweight. Only open the issue if the user agrees; if
they'd rather just do it now, follow their lead, but let them make that call
knowingly. Keep taking the rest of the batch either way.

## Notes

- **Never `--no-verify`.** If a pre-commit hook fails, fix the underlying issue —
  that's the whole point of the hook. Same for CI at wrapup.
- **Commit style:** `git commit -m "message"` only (no HEREDOC/`$()`), first line
  ≤72 chars, lowercase, imperative, no trailing period, plain `git` (never
  `git -C`) — per the project conventions.
- If the user starts `/tweaks` on a non-default branch that **isn't** the batch
  branch, or with an unexpected dirty tree, surface that before branching — they may
  want those changes folded in or set aside first, rather than have the batch branch
  off an unexpected base. (Landing on the batch branch itself is the normal
  multi-session case — just continue on it, per step 1.)
