# Rounds

Making the rounds. This is the caretaker's mode — an unhurried walk through the code, noticing what could use attention, and giving it. Nothing dramatic happens here. The point is a place that is visibly, consistently attended to, which is a quality that comes from many small acts rather than one large one.

Reach for this when there is no single big target, just a general sense that a corner of the codebase would feel more cared-for after some attention — and when someone is present to steer. If tending is running unattended (`/loop`, a schedule, "keep going on your own"), do not walk the rounds yourself: that is Garden's job — read `references/garden.md` and orchestrate scouts instead. A main thread making rounds alone sees only its own narrow walk, and after a few loops mistakes that walk for the whole garden.

## The Loop

```
survey  →  choose one  →  understand it fully  →  tend it  →  verify  →  move on
   ↑                                                                        │
   └────────────────────────────────────────────────────────────────────────┘
```

Survey the area against the lens, not from memory — see *What's Worth a Round* below for which index to load and how to scan with it. Choose exactly one thing. Understand it well enough that you are certain what "better" means here. Make the change. Verify that behavior is preserved and the surrounding pattern is intact. Then go back to surveying.

The loop ends when a survey turns up nothing worth doing — not when you run out of energy to keep going. If the area is already tended, that is a finding, not a failure. Say so and stop.

## The One Discipline: Small

Everything in this mode depends on keeping each thing small. A round is a two-minute-to-an-hour act of care, self-contained, obviously correct when you're done. The moment a change starts to sprawl — touching many files, requiring a design decision, asking you to hold the whole system in your head — it has stopped being a round. That is not a problem; it is a signal. Note the larger thing and hand it off (see below). Do not let one round quietly metastasize into an afternoon-long refactor; that abandons the discipline that makes this mode safe and reviewable.

## What's Worth a Round

**Before surveying, open the relevant example lens** — `examples/code.md` always, plus `examples/interfaces.md` or `examples/agents.md` if this code has a user or agent surface. Then survey for the *absence* of the shapes it describes. This is the whole difference between a specific search and a vague look-around: you are not scanning from memory for "anything that seems off," you are scanning for these particular things not being true. Do not skip this because you feel you already know what cared-for code looks like — that feeling is precisely what produces a generic scan.

The catalog below is the round-sized subset of those shapes, gathered here for convenience. Any one of these, done well and in isolation, is a complete round.

- **A name that misleads or makes you guess.** Rename to the word the concept is already called elsewhere. Put the unit in the name (`timeout_ms`, not `timeout`).
- **A swallowed error.** A bare catch-and-ignore, a generic bubbled-up string, an `unwrap`/`!`/`panic` where the failure is actually reachable. Give it context a tired human could use at 3am.
- **A missing edge case that's cheap to handle.** The empty list, the null, the zero, the off-by-one boundary — where the fix is small and the omission is real.
- **A magic number or literal** that should be a named constant with a reason attached to the name.
- **A `TODO` that is actually a two-minute fix.** Do it, delete the comment. (A `TODO` that is a real project belongs in your tracker, not the code — that is also a valid round: relocate it and remove the litter.)
- **A local inconsistency.** One function in a module that does the same thing a different way than its neighbors. Bring it in line with the established pattern.
- **A test that has quietly died** — `#[ignore]`, `skip`, `xit`, a commented-out assertion. Either revive it or delete it honestly. A test everyone has learned to distrust is worse than no test.
- **Dead code.** An unused function, an unreferenced branch, a flag whose experiment concluded long ago. Remove it. The willingness to delete is one of the clearest signs of an active caretaker.
- **A small, real duplication** — two or three lines repeated verbatim nearby, with no variation. Fold them together in place. (If it is scattered widely or varies between sites, that is Gather's job, not a round.)
- **A missing small kindness.** The empty state that could teach the first action, the `--help` with no worked example, the slow path that runs silent, the config value that fails mid-run instead of at startup, the invariant everyone assumes but nothing asserts. Tending adds as often as it corrects — each lens ends with a *Care that adds* list of round-sized additions; survey for those gaps too, not only for flaws in what exists.

## How to Tend a Single Thing

1. **Understand before touching.** Read enough of the surrounding code to know why it is the way it is. The odd-looking line is sometimes load-bearing. Care includes not breaking things you didn't understand.
2. **Make the smallest change that fully addresses it.** Not the change that also improves three adjacent things you happened to notice — those are their own rounds.
3. **Match the local grain.** Use the conventions already present in this module, even if you would have chosen differently on a blank page. Consistency within a boundary is worth more than your personal preference.
4. **Verify behavior is unchanged.** Run the relevant tests. If the thing you touched had no test and easily could, adding one is itself a fine round — but keep that as a separate pass.
5. **Confirm you left it coherent.** Step back. Does the module read as *more* consistent now, or did you introduce a new one-off? If the latter, reconsider.

## When It Won't Stay Small

If a candidate turns out to be bigger than a round — the visible tip of something structural, or a small change whose reach is actually wide — stop. Do not pull the thread here. Name the larger shape plainly for the user and point at the right mode:

- A clear change that would touch many places at once (a rename, a move, a convention to propagate) → **Sweep** (`references/sweep.md`)
- One system that has grown beyond its job → **Distill** (`references/distill.md`)
- The same logic scattered across many sites → **Gather** (`references/gather.md`)

Leaving the small version untouched and naming the real problem is better care than a half-done large change wedged into a small one. (The exception is friction you actually tripped over — see *Fix What Trips You* in `SKILL.md` — which you fix on the spot even when it's a little bigger than a round, because reality handed it to you rather than you going looking.)

## Leaving a Clean Trail

Keep each round independently reviewable. If you are making commits, one round is one commit with a one-sentence message. If you are working through several rounds in a sitting, keep them mentally (and ideally literally) separated, so that any one could be understood, kept, or reverted on its own. A tidy trail is part of the care — it is a note to the next reader about exactly what changed and why.

## When to Stop

Stop when a survey of the area turns up nothing that clears the bar. Resist the pull to manufacture work — inventing churn to feel productive is the opposite of care, and it erodes the trust that a clean history earns. When you stop, tell the user what you tended and, honestly, that the rest looked well kept. "This corner is in good shape" is a real and useful result.
