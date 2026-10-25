---
name: pull-focus
description: >
  A distillation and separation-of-concerns step during iterative, AI-assisted
  refinement of any work — documents, plans, outlines, prototypes, code, ideas.
  Rebuilds each area of the work around one clear focal point: superseded framing
  is deleted, and tangents move into their own homes. Reorganizes without cutting
  scope (cutting scope is hammer-time). Trigger immediately when the user says
  "pull focus", "this has gotten muddy", "untangle this", "split this out", or
  similar. Also trigger when you notice, after three or more rounds of revision
  on the same work, that corrections sit beside what they corrected, early-draft
  structure still steers later content, or side topics have leaked into the main
  piece — in these cases, ask if it's time to pull focus before proceeding, and
  don't ask again for the same work after the user declines.
---

# Pull Focus

Rebuild the work so each area is a distinct shot: one focal point, holding only what the user means now. Keep everything the user still holds; change only where it lives and how it reads. When content the user still holds looks unnecessary to the work, keep it and offer hammer-time at the end.

A **shot** is one unit a reader takes in as a whole: a section of a document, a module or file of code, a slide in a deck, a step of a plan.

## Workflow

### 1. Recover current intent

Treat the conversation as the source of truth. Where the artifact disagrees with it, the artifact is wrong. Walk the session from the start and write down, as working notes:

- Each correction or elaboration the user made, stated as what they mean now.
- Each framing those corrections superseded, named concretely: the terms, structures, assumptions, examples, or (in code) names, branches, and shims it left behind. Step 5 searches for these.
- Each tangent that came up: where it belongs, or that the user dropped it.

If the early session has been compacted, work from the summary and tell the user the record is partial.

### 2. Map the shots

List every area of work touched in the session. For each, write its focal point as one sentence in the user's current terms. Add a new shot for each live tangent with no proper home.

Sort every passage in those shots into one bucket:

- **In focus**: serves this shot's focal point. Keep it. Passages from before the session that the conversation never addressed are in focus unless they carry a superseded framing from step 1.
- **Belongs elsewhere**: serves another shot's focal point. Name the destination.
- **Out of focus**: superseded framing, dropped tangents, or text that reconciles old with new ("Note:", "Update:", "actually…", parentheticals squaring a correction with the original). Delete it.

Mark any in-focus passage that the user still holds but the work may not need as a hammer-time candidate.

### 3. Get sign-off on the shot list

Present the map before changing anything:

```
**<shot>**: <focal point>
  moving in: <content> (from <shot>)
  moving out: <content> → <shot>
  dropping: <superseded framing>
  hammer-time candidate: <content>
**<new shot>**: <focal point>
  ...
```

Leave out shots with nothing moving, dropping, or flagged, and list them by name on one line. Wait for the user to confirm or adjust. Re-present only if their adjustments change the shot list itself.

### 4. Rewrite each changed shot from its focal point

For each shot with content moving in or out, or dropping, in the map, write it fresh, starting from the focal point and its in-focus and incoming content. Do not edit the existing text in place. Editing keeps the earlier draft's structure, and that structure is where stale framing hides. Create new shots in the same form as the existing work (a new section, file, or module). Leave shots with no changes untouched.

Delete out-of-focus content outright and leave no notes about what changed. Where a reader of the source shot needs to find moved content, leave a plain pointer to the destination. In code, update imports, call sites, and references.

### 5. Verify

Check each item and fix what fails before handing back:

- For each rewritten shot, state its focal point, then re-read it and confirm every passage serves that point.
- Search all shots for the superseded terms from step 1. Each hit is residue: rewrite or delete it. A hit in a shot step 4 left untouched adds that shot to the rewrite; tell the user if the change is more than a small fix.
- Search the rewritten shots for change notes and reconciling text ("Note:", "Update:", "previously", "now", "actually", "instead of"). Remove any that narrate the revision history.
- Confirm each moved item exists in its destination and appears in its source only as a pointer, if at all.
- Confirm each in-focus item from the signed-off map survived the rewrite.
- For code, build and run the tests. Behavior changes only where the user asked for them. If there is no build or tests, say so in the hand-back.

### 6. Hand back

Tell the user in a few lines which shots exist now, which are new, and anything verification caught. If the map marked hammer-time candidates, offer hammer-time on them.
