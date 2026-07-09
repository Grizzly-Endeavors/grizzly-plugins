# 🔨 Hammer Time

A Claude skill for cutting through overcomplicated designs, plans, and systems.

## What Is This?

When you brainstorm with AI, conversations tend to snowball. One cool idea leads to another, someone says "you could do both," and before you know it you're designing a spaceship when you needed a bicycle.

**Hammer Time** is a skill that teaches Claude to ask: *"What if we just used a hammer?"* — meaning the most boring, obvious, proven solution that actually works. Not the clever one. Not the elegant one. The one that gets the job done.

## Installing

1. Download the `hammer-time.skill` file
2. In Claude.ai, go to **Settings** → **Skills**
3. Upload the `.skill` file
4. Done — Claude now knows about hammers

## How to Use It

### Say "It's hammer time"

When a conversation has gotten too complicated and you want to cut through the noise, just tell Claude:

- *"It's hammer time"*
- *"This is overcomplicated"*
- *"What's the hammer solution?"*
- *"Just use a hammer"*

Claude will respond with a short, direct statement of the simplest solution that works, followed by an explanation of what's being cut and why, and then ask if you want to adjust or move to an action plan.

### Claude will also check in on its own

If Claude notices a design conversation getting bloated — too many components, too many "and we could also" moments — it'll ask if it's hammer time before things get out of hand.

### Three modes

The skill works in four situations, and Claude will figure out which one applies:

1. **New problem** — You're starting from scratch. Claude will ask grounding questions first (how much data? how many users? what does success actually look like?) to find the hammer before the brainstorm spirals.

2. **Mid-conversation reset** — The design has gotten away from you. Claude recovers the original problem, identifies where the complexity crept in, and proposes the simple version.

3. **Auditing something that exists** — You've got a system, codebase, or process that's become fragile and overcomplicated. Claude explores what's actually there, clarifies what it actually does vs. what it was built for, and identifies what can be cut.

4. **Mid-implementation redirect** — You're partway through building something and you've hit a wall. Unexpected complexity, cascading changes, or the architecture is fighting you. Claude assesses where you are and whether to push through, back out, or pivot to a simpler approach.

### The output is always the same

1. **The hammer** — a short, declarative statement of the solution
2. **The explanation** — why it works and what's being cut
3. **The handoff** — *"Any adjustments? Or should we make an action plan?"*

The hammer lands just before planning starts, so you go from "what do we actually need?" straight into "okay, let's do it."

## Tips

- **Be specific when answering Claude's questions.** "A lot of users" doesn't help. "About 50 people, mostly on Mondays" does. The more concrete the facts, the better the hammer.
- **The hammer isn't always the final answer.** Sometimes after seeing the simple version, you'll decide some of the complexity was actually worth it. That's fine — at least now it's a deliberate choice.
- **You can always ignore it.** If the hammer feels too simple, say so. Claude will work with you from there.
