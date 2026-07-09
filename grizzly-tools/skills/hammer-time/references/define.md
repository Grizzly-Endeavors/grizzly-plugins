# Define — New Problem, Starting Fresh

## Purpose

Ground a new design conversation in reality before solutions start flying. The goal is to collect the concrete facts that make the hammer solution obvious — so that when ideas start getting complex, there's a clear baseline to measure against.

## Workflow

### Step 1: Define the Problem

Don't jump to solutions. Ask questions that surface the real shape of the problem:

- **What specifically needs to happen?** Not what the system should look like — what does it need to *do*? What's the actual verb?
- **What are the real requirements?** How much data? How many users? How often does it change? What's the actual scale?
- **What does minimum success look like?** What's the threshold where this is done and working, in practice? If you could only ship one thing, what would it be?
- **What are the actual usage patterns?** Is this used daily or monthly? By one person or a thousand? Read-heavy or write-heavy? Interactive or batch?
- **What already exists?** Is this greenfield or does it need to integrate with something? What constraints are real vs. assumed?

Push for specifics. "A lot of data" isn't a requirement — "~10,000 rows updated daily" is. The more concrete the answers, the more obvious the hammer becomes.

### Step 2: Drop the Hammer

Once the problem is grounded, deliver the hammer solution following the output contract:

**Statement** → **Explanation** → **Handoff**

Connect the solution directly to the facts gathered in Step 1. Show why it works by pointing at the actual numbers, patterns, and constraints.

## Example

**User:** "I want to build a system to track which books I've read, want to read, and my ratings."

**Good questions to ask:**
- How many books are we talking about? Dozens? Thousands?
- Is this just for you or shared with others?
- Do you need search, or is browsing fine?
- Where do you want to access it — phone, desktop, both?
- Do you need it to pull data from anywhere (Goodreads, etc.) or is manual entry fine?

**If the answers are:** ~200 books, just me, browsing is fine, mostly desktop, manual entry is fine:

> **Use a spreadsheet.** You've got ~200 books for one person with no sharing or integration requirements. A Google Sheet gives you sorting, filtering, access from anywhere, and zero setup. If you want it prettier later you can always export the CSV into something else, but the data model is trivially simple and the usage pattern doesn't demand anything more.
>
> Want to tweak that, or should we set it up?
