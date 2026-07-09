---
name: review-ready-writing
description: >
  Create or refine materials meant for someone else to review — proposals,
  design docs, status updates, PR/MR descriptions, emails, RFCs, decision docs,
  or Teams/Slack messages — so they are focused, plainly written, and purposeful,
  and don't dump review load on the reader. Use this skill proactively whenever
  the user is drafting or producing anything that will be sent to a colleague,
  manager, or team for review or sign-off, and whenever the user pastes a draft
  and asks to tighten, shorten, clarify, cut the fluff, or "make it land." Also
  trigger when the user asks for a "proposal", "writeup", "doc", or "formal"
  version of something — that is exactly when to check whether a lighter format
  would do. Do not trigger for the user's own private notes, scratch work, or
  anything not bound for another reader.
last_updated: 2026-06-03
created_by: Bear
---

# Review-Ready Writing

AI makes it cheap to produce long, polished-sounding documents fast. The cost
lands on the reader, who then has to dig the actual point out of a wall of
confident prose. This skill does the opposite: produce the smallest thing that
does the job, written plainly, with a clear ask. Respecting the reviewer's
attention is the whole point — everything below serves that.

Apply this whether writing from scratch or refining a draft the user already
wrote. When refining, default to cutting. The reviewer's time is the scarce
resource, not the word count.

---

## Step 1 — Right-size the format before writing

The most expensive mistake is building a big artifact for a small decision.
Before writing anything, decide what the situation actually needs.

Rough guide:

- **A one-line message** (Teams/Slack) — a small, reversible, or low-stakes
  call. "Thinking of moving the cron from hourly to every 15m — any objection?"
  does not need a document.
- **A short message or email** — a decision with a couple of tradeoffs, or an
  update a few people need. A handful of sentences, maybe a short list.
- **A doc** — genuinely multi-part work: several options to compare, a design
  with real surface area, something people will reference later.
- **A formal proposal** — high-stakes, hard to reverse, needs a paper trail or
  sign-off from people who weren't in the room.

If the user asks for a heavier format than the situation warrants, say so and
offer the lighter version. For example, if the user says "write a formal
proposal to switch our error tracking to X" and it reads like a small reversible
call, push back: draft the three-line Teams message first, and mention the full
proposal is there if anyone asks for it. The user can always escalate; almost
nobody wants to un-send an essay.

This is a suggestion, not a veto. If the user has a reason for the heavier
format — an exec wants it in writing, it is politically load-bearing — go
with it.

---

## Step 2 — Give it a goal

The worst thing to receive is a 40-page proposal. The second worst is anything
with the message "Thoughts?" — it shoves the work of figuring out what is even
being asked onto the reader.

Every review-bound item should answer three questions up front, before the body.
Lead with a short framing block:

> **What this is:** [the objective, in one line]
> **My calls:** [what the sender personally wrote, decided, or verified — anything not listed here may be AI-generated and could contain unverified assumptions]
> **What I need from you:** [the specific question(s), and what the answer unblocks]

Why each one earns its place:

- **What this is** sets the lens. The reader knows what they are looking at and
  why before they spend any attention on it.
- **My calls** tells the reader what the sender actually owns and has verified.
  This matters especially because AI can produce confident-sounding content with
  wrong assumptions or unverified details baked in. Without this, the reviewer
  has no way to know which parts have been personally stood behind and which are
  AI extrapolation that warrants scrutiny. It shifts the burden of that judgment
  from the reviewer back to the sender, where it belongs.
- **What I need from you** is the gap between "review this" and "tell me whether
  the rollback plan in section 3 is safe enough to ship Friday." The second gets
  a fast, useful answer. Tie the ask to a consequence — the decision or action
  the feedback feeds — so the reviewer knows why their five minutes matters.

If you cannot answer "what do I need and what will it do," that is a signal the
thing may not be ready to send, or does not need to be sent at all. Say so,
rather than wrapping an aimless draft in a tidy framing block.

---

## Step 3 — Say it plainly

AI defaults to sounding impressive. Strip that out. The reader wants to know what
is true and what matters, not to be sold.

- Cut hype and intensifiers — "groundbreaking," "revolutionary," "unprecedented,"
  "game-changing," "seamlessly," "robust," "leverage," "unlock." State the
  concrete thing instead.
- Lead with the conclusion, then support it. Do not build up to the point.
- Prefer specific over grand. Numbers, names, and dates beat adjectives.
- Write like a competent colleague talking, not a press release.

**Hype → plain:**
Before: "This groundbreaking initiative will revolutionize our data
infrastructure and unlock unprecedented efficiency gains across the org."
After: "This cuts the nightly batch job from ~4h to ~40m."

**Buildup → conclusion-first:**
Before: "After evaluating several approaches and weighing the tradeoffs of each,
considering both short- and long-term implications, we arrived at a
recommendation."
After: "Recommendation: token-bucket rate limiting. Reasons below."

---

## Step 4 — Keep it short

Aim for high information density — more meaning per word. Length is a cost the
reader pays, so every part of the document has to earn its place.

- Leave out "just in case" context. If the reader probably already knows it, or
  probably will not need it, cut it. Inviting a question beats forcing everyone
  through background they did not need: "Happy to share the migration history if
  useful" beats three paragraphs of it.
- One point per sentence. Delete sentences that only restate the one before.
- Drop preamble ("I wanted to reach out about...") and throat-clearing.
- Five tight bullets can beat three dense paragraphs for scanning — but do not
  pad to fill bullets either.

The test for any sentence: if deleting it would not change what the reader
decides or does, delete it.

**Just-in-case → ask-instead:**
Before: [four paragraphs recapping how the current system evolved, the vendor
relationship history, and three alternatives already ruled out]
After: "We're switching X to Y to fix the timeout issue — background in the
linked thread if you want it. One open question for you below."

---

## When you are the one missing information

These principles cut both ways. If you have not given enough to write the thing
well, Claude will ask for the specific missing piece rather than padding the
draft with generic filler or hedged guesses. A short, precise question to you
now produces a tighter result than noise the reviewer has to wade through later.
Asking for specifics is better than manufacturing context.

---

## Quick self-check before it goes out

- Is this the lightest format that does the job?
- Does it answer: what this is / my calls / what I need from you?
- Could a reader find the ask in about five seconds?
- Is there a sentence, paragraph, or section that could be cut without losing
  anything the reader acts on? If yes, cut it.
- Did any hype words sneak back in?
