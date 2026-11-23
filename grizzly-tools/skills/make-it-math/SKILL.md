---
name: make-it-math
description: Turn a recurring frustration or vague preference into a single equation that makes your tradeoffs legible to agents. Use when prompting in plain English keeps failing to produce the behavior you want.
---

# Make it Math

Help the user turn a recurring annoyance into a fitness function: one clear equation that combines what can be objectively measured with what the user actually cares about.

The goal is not to build a dashboard or a perfect mathematical model. The goal is an equation that communicates the user's tradeoffs clearly enough that an agent with no extra context derives the right behavior just by reading it.

## How to Work With the User

The user is half of the equation. Your job is to help them surface preferences they have not yet put into numbers, without dumping algebra or a wall of questions on them.

* **Move one decision at a time.** Keep each turn short, focused, and in plain language so the user can skim, gut-check, and reply in a sentence or two.

* **Give them anchors to react to.** People freeze on blank-page math questions ("what is a minor glitch worth to you?"). Offer a rough starting point or concrete tradeoff ("would you trade 5 minutes of waiting to avoid a minor glitch, or is that way off?") so they can steer by reacting.

* **Actively ask for pushback, including nitpicks.** A formula that feels "mostly fine" usually hides an unstated value and will steer an agent toward the wrong outcome. Explicitly invite the user to call out anything that feels slightly off, overcomplicated, or weirdly phrased. Treat every rejection as progress.

* **Translate math back into English.** Whenever you propose an operator, cap, or weight, state the value judgment it encodes in plain words ("multiplying by this means if it happens too late, the whole run is worth zero to you. Is that true?") so the user can shape the equation without thinking in algebra.

* **Hold off on solving.** Resist the urge to propose a full formula on turn one. If you invent the user's values for them, the formula will look neat and miss what they actually care about.

## The Process

Work through these phases in order, skipping anything the user has already made clear and looping back whenever a hidden value surfaces.

### 1. Name the Problem and the Blind Spot

Get a clear picture of what is happening, what it feels like from the user's seat, and what they wish the end state looked like. Help them name what agents currently optimize for and what cost or reality the agents are blind to.

### 2. Check Reality and Pick One Currency

Before theorizing, look at what can actually be measured. If you have access to the repo, logs, history, or tooling, inspect them to see what real signals exist rather than guessing in the abstract.

Then help the user choose **one shared unit** (such as minutes, dollars, tokens, or lines). Both the value side and the cost side have to end up in the same currency so they can be weighed against each other.

### 3. Set Exchange Rates and Price Your Values

This step has two separate jobs:

* **Convert measured signals into the shared currency.** Objective data points rarely arrive in the same unit. Work with the user to set the exchange rates that convert what you can measure (CPU usage, tokens, lines, wait time, etc.) into the chosen currency.

* **Turn personal values into numbers, tiers, or modifiers.** Some things that matter cannot be measured directly, like how severe a failure is, how much one area of the system matters compared to another, or whether a result arrived in time to be useful. Translate those preferences into rough prices, scales, caps, or binary modifiers (`1` or `0`) that can sit inside the equation.

Remind the user if they hesitate: these numbers are not physics, they are declared preferences. Order-of-magnitude honest is plenty. Offer concrete anchors for them to push back on rather than asking them to invent numbers from scratch.

### 4. Cut What Pulls the Wrong Way

Look over the candidate variables and ask which ones would steer an optimizer toward vanity metrics or punish something the user actually wants to keep. Exclude those on purpose, and note why.

### 5. Shape the Formula

Combine the measured terms and declared values into a single, readable equation. Keep these structural instincts in mind:

* **Anchor zero at break-even.** Structure the score as `Expected Value - Actual Cost` (or equivalent) so a negative number literally means net waste in the shared unit.

* **Multiply dependencies, add independent costs.** If a piece of work becomes worthless when a condition is false, multiply by that condition so the value term collapses to zero automatically.

* **Keep it simple.** If a sub-formula starts nesting calculations, check whether a simple tier or cap captures the same value judgment more clearly.

Present the draft formula with short, one-line definitions for each term, translate what its shape implies in plain English, and explicitly ask the user to nitpick it.

### 6. Run a Blind Dry-Run

The real test of the formula is whether an agent with *zero* background context derives the behavior the user wants just from reading it.

Do not run this test yourself inside the current conversation; you already know what the user complained about and will accidentally bias the result.

* **If you can spawn a fresh subagent or clean context:** Pass it *only* the formula, the short term definitions, and any pricing table. Ask it to summarize the priorities and desired shape of a system/workflow optimized for that formula.

* **If you cannot spawn a clean context:** Give the user a clean, self-contained copy-paste prompt containing only the formula, term definitions, and that question, and ask them to paste back the response from a fresh chat.

Review the blind result together. Ask the user what looks right and what makes them cringe, even slightly. Any cringe or nitpick means a value is missing, mispriced, or shaped wrong. Loop back through Phases 2 to 5 until the blind run lands where they want it.

## Done (and Coming Back Later)

You are done when the user approves the blind dry-run result.

When they do, output a clean, portable summary they can drop into docs, prompts, or tooling:

1. The final formula.

2. Short definitions for each term (noting which are measured and which are declared).

3. Any exchange-rate or pricing tables.

4. Variables explicitly excluded and why.

5. The approved blind dry-run behavior.

Treat this as a living artifact. If the user comes back later after trying to apply the formula in practice, skip the intro, ask what felt off when they used it, and jump straight into adjusting terms, exclusions, or shape, followed by a fresh blind dry-run.