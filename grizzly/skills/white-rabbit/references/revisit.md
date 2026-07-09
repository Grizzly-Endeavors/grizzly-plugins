# Revisit — The Zombie That Won't Stay Dead

## Purpose

It was fixed. It was tested. It was moved past. And now it's back — or something suspiciously similar is back — or the fix for the first thing broke a second thing.

A returning problem is strong evidence that the original diagnosis was incomplete. Either the rabbit that was chased last time led to a symptom instead of the root cause, or it was the wrong rabbit entirely and the real cause was somewhere nobody looked. Either way, the previous mental model had a gap. This time the goal is to find it.

## Workflow

### Step 1: Establish What's Actually Happening

Before assuming "the bug is back," verify:

- **Is this the same problem?** Same error, same behavior, same conditions? Or similar but subtly different? The distinction matters enormously. Same problem = the fix didn't work. Similar problem = possibly a different manifestation of a deeper issue, or a separate bug that happens to look alike.
- **Is the fix still in place?** Was the change deployed? Did it get reverted or merged over? Is the correct code actually running in the environment where the problem appears? This is the most common reason a fix "didn't work" — it isn't actually running.
- **What changed since the fix?** Anything deployed, configured, or updated between when it was working and when it stopped? This narrows the timeline and points at potential interactions.

### Step 2: Audit the Original Diagnosis

Go back to the original fix and reconstruct the reasoning:

- **What was the diagnosed cause?** State it explicitly.
- **What evidence supported that diagnosis?** Was it confirmed through elimination, or was it the first plausible rabbit that happened to produce a fix?
- **How was the fix verified?** Was the specific cause tested as resolved, or was the symptom tested as gone? These are not the same thing. A symptom can disappear temporarily for unrelated reasons — a different code path, a timing shift, a cache refresh.

This audit often reveals the gap. Common patterns:

- **Symptom-level fix.** The fix suppressed the symptom (caught an exception, added a retry, defaulted a null) without addressing why the symptom was occurring. The underlying cause persists, now manifesting differently.
- **Coincidental fix.** The fix changed something that happened to make the problem go away, but not for the assumed reason. Maybe restarting the service cleared a stale connection, and the credit went to the config change made before the restart.
- **Partial fix.** The cause was correct but there were multiple triggers. The fix addressed one. The remaining triggers still produce the failure, just less frequently.
- **Fix-induced bug.** The fix introduced a new issue. The original problem is genuinely resolved, but the fix has a side effect creating different symptoms that look similar.

### Step 3: Broaden the Search

With the original diagnosis under scrutiny, build a new suspect list including causes the first round may have missed:

- **Suspects not fully eliminated last time.** If suspects were dismissed on intuition rather than evidence, they're back in play. These are the paths not taken when the rabbit was chosen.
- **Interaction effects.** Could the fix be interacting with something else? Could the original cause be interacting with the fix? Systems have memory — changes ripple.
- **Deeper layers.** If the diagnosed cause was "the cache returns stale data," the revisit question is *why* the cache returns stale data. Go one level deeper than the previous investigation.
- **The timing dimension.** Zombies often have a temporal component. They resurface under load, after a certain interval, when a cron job runs, or when a connection pool cycles. Look for periodicity.

### Step 4: Probe with Prejudice

Probes in Revisit mode carry an additional constraint: they need to distinguish between "same cause, fix didn't work" and "different cause, similar symptoms."

Design probes that specifically test this:
- Reproduce with the fix explicitly reverted. If the problem is identical with and without the fix, the fix was never addressing the real cause.
- Reproduce under the exact same conditions as the original failure. If the conditions can't be matched, the trigger has changed even if the symptom looks the same.
- Compare failure signatures (error type, location, stack trace). Subtle differences point toward a different cause.

### Step 5: Fix and Verify Differently

When the real cause is identified, don't just apply a fix and test the symptom again. That's what happened last time.

- **Verify the cause directly.** Demonstrate that the identified cause *produces* the symptom. Not just that fixing it removes the symptom — prove the causal chain.
- **Negative test.** After the fix, try to trigger the symptom through a different path. If it's still reachable, there are multiple causes.
- **Time-delay test.** If the zombie had a temporal component, don't declare victory immediately. Check again after the relevant interval.

## The Confidence Trap

A returning bug erodes confidence, and the natural response is to compensate with certainty. "This time it's *definitely* the cache." The appropriate response to a zombie is *increased skepticism*, not increased conviction. One rabbit was chased last time and it didn't lead to the answer. The instinct to grab the next rabbit harder is strong, but wrong. Widen the net instead.

## Things to Watch For

- **The whack-a-mole.** Fix one thing, another breaks. Fix that, a third breaks. This signals a systemic issue, not a localized bug. Stop fixing individual symptoms and look for the common thread. If the common thread turns out to be architectural — accumulated complexity, patterns that don't fit together, old code resisting new features — that's a Hammer Time problem. The system needs simplifying, not more targeted fixes.
- **The phantom fix.** The problem went away on its own and the credit went to a change. When a fix "works," check whether the timeline actually proves causation. Did it stop failing because of the change, or because of someone else's deploy, or because the queue drained, or because the Tuesday spike subsided?
- **The regression test gap.** If the problem returned because the fix was lost (overwritten, reverted, not deployed), that's a process problem, not a diagnosis problem. Note it, add a test, move on.
