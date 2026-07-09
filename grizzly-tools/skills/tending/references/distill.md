# Distill

One system has outgrown what it was originally for. It started with a clear job, then absorbed responsibilities one reasonable decision at a time, or was reshaped through several evolutions until its core is hard to see under everything that grew around it. Each addition made sense on the day it was made. The sum no longer does.

The work here is to find the actual job the system does, design something that does just that job well, and send everything else home or delete it. The result is smaller than what you started with — and, done right, the code *around* it gets simpler too, because responsibilities that never belonged here go back where they do.

This is the mode most able to break things. Behavior preservation is not a nicety in it; it is the whole discipline. Move in reviewable steps, under a safety net, and never let a cleanup silently change what the system does.

## Recognizing the Candidate

Signs that a system wants distilling:

- You cannot describe what it does without the word "and." "It parses the config *and* validates it *and* caches it *and* notifies on change."
- Its name no longer matches its contents, or you struggle to name it at all.
- A change in one corner ripples to unrelated corners. The parts are entangled rather than merely adjacent.
- The core operation is buried — most of the code is scaffolding, special cases, and things bolted on for one caller that never got removed.
- Reading it, you can feel the geological layers: an original clean idea, then three eras of "just add a flag for this."

## The Work

Before the steps below, open the relevant example lens — `examples/code.md`, plus `interfaces.md` or `agents.md` if this system has a user or agent surface. It does double duty in this mode: the shapes give you concrete language for what "buried" and "tangled" actually look like as you inventory, and they are the target you design toward in step 3. Skipping it is how a distillation ends up merely rearranged rather than genuinely better — the structure moves but none of the shapes that make code cared-for get applied.

### 1. Observe what it actually does now

Not what it was meant to do, not what its name or docs claim — what it does today, in reality. Inventory its responsibilities honestly and specifically. List the distinct jobs it performs, the things that call it, and what each caller actually needs from it. This map is the ground truth everything else rests on; resist the urge to start editing before you have it.

### 2. Find the core

Among those responsibilities, which one is the essential job — the thing that, if you kept only it and threw everything else away, would still justify the system's existence? Separate essential complexity (inherent to the problem) from accidental complexity (an artifact of how it grew). The core is usually smaller than it looks from inside the current code, because so much of what is there is accident.

State the core in one sentence with no "and." If you can't, you may be looking at two systems wearing one name — which is itself the finding, and splits this into two distillations.

### 3. Design the thing that does just the core

Design the interface someone would *wish* existed for this job — the shape you would want to reach for if you were a caller who knew nothing of the history. Make it do the core well and completely. Lean on the shapes in `examples/code.md`: make illegal states unrepresentable, give it errors a tired human can use, name it so a stranger could guess it. If the distilled thing has a user surface or is consumed by agents, bring in `examples/interfaces.md` or `examples/agents.md` too. The goal is a thing small enough to hold in your head at once.

Design *less*, not a more elaborate replacement. Distilling that produces a fancier, more general, more configurable system than the original has failed — you have added complexity while claiming to remove it. If the new design is bigger than the old core, stop and find the core again.

### 4. Relocate and delete

This is the step people skip, and it is where most of the value is. Every responsibility that is not the core has to go somewhere honest:

- **Belongs to a caller** → push it out to that caller, or to a place they can share.
- **Belongs to a different system** → move it there.
- **Belonged to a need that no longer exists** → delete it, without ceremony.

Do not leave orphaned logic parked "just in case." The reason the surrounding code gets simpler after a good distillation is precisely that these displaced responsibilities land where they actually belong, instead of hiding in a system that was pretending to be about something else.

### 5. Migrate under a safety net

Behavior must be preserved through the change. Before altering anything:

- **If tests exist**, make sure they cover the behavior you're about to move around. Run them; they are your net.
- **If they don't**, write characterization tests first — tests that pin down what the system currently does, quirks and all, so that "unchanged" has a definition you can check against. This is not optional busywork; without it, "I preserved behavior" is a hope, not a claim.

Then migrate in the smallest reviewable steps you can — introduce the distilled core alongside the old system, move callers over one at a time, verify at each step, and remove the old shape only once nothing depends on it. Each step should be independently sound.

If, along the way, you discover a genuine bug — a behavior that is simply wrong, not just ugly — do not silently fix it inside the refactor. Surface it, name it, and let correcting it be its own decision. A refactor that also quietly changes behavior is the exact thing that makes people afraid to refactor.

## Guardrails

- **Behavior is sacred; the shape is not.** Preserve the former ruthlessly while you change the latter.
- **Smaller is the whole point.** If the result isn't simpler to hold in your head than the original core, reconsider.
- **No gold-plating.** Do not add generality, configurability, or features "while you're in there." Distilling is subtraction.
- **Reversible steps.** Prefer a sequence where any single step could be reviewed and reverted alone over one heroic all-at-once rewrite.

## Done When

The system does one nameable job, you can hold it in your head at once, and the code around it reads more simply than before because the responsibilities that drifted in have gone home. A reader who arrives fresh can guess what it does from its name and interface, and be right.
