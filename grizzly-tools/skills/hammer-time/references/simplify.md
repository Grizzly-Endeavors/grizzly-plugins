# Simplify — Mid-Conversation Course Correction

## Purpose

The design discussion has gone somewhere impractical. Maybe it happened gradually — one "and we could also" at a time — or maybe it's a sudden realization that the solution has become a loose collection of cool ideas rather than a coherent thing that solves the original problem. Time to find the hammer.

## Workflow

### Step 1: Recover the Original Problem

Before simplifying, re-establish what this was supposed to do. Conversations drift, and by this point the original ask might be buried under layers of iteration. Go back to it explicitly:

- What was the user actually trying to accomplish when this started?
- What were the real constraints and requirements?
- Have any of those changed, or did the solution just outgrow them?

If the original requirements were never concretely defined (common — the brainstorm may have started without grounding), do that now. Ask the questions from the Define workflow to establish the facts.

### Step 2: Identify the Bloat

Look at the current design and name specifically where complexity crept in. Common patterns:

- **Feature stacking:** "Since we're already building X, we might as well add Y." Y was never a requirement.
- **Premature abstraction:** Building for flexibility or scale that hasn't been established as necessary.
- **Frankensteining:** Two different good ideas got merged instead of choosing between them.
- **Cool-driven development:** Something got included because it's an interesting technical challenge, not because the problem demands it.
- **Edge case inflation:** Designing for edge cases that might never happen, at the cost of core simplicity.

### Step 3: Drop the Hammer

Deliver the simplified solution following the output contract:

**Statement** → **Explanation** → **Handoff**

Walk through what was cut and why each cut is fine. Be specific — "we don't need the event bus because the data changes once a week and there's one consumer" is useful. "We simplified the architecture" is not.

Don't apologize for the ideas that got cut. They weren't bad ideas — they just weren't earning their complexity. Name them, acknowledge why they were appealing, and explain why the problem doesn't need them.

## Example

**Context:** A conversation about a personal blog has evolved into a design involving a custom CMS, a headless API layer, a React frontend with SSR, a comment system with moderation, and an analytics pipeline.

> **Use a static site generator with markdown files.** The original goal was a personal blog — one author, public posts, maybe a few pages. We've accumulated a CMS (but there's one author), an API layer (but nothing consumes it except one frontend), server-side rendering (but the content is static text), a comment system (which wasn't in the original ask), and analytics (which any free third-party tool handles).
>
> A tool like Hugo or Astro turns a folder of markdown files into a site. Writing happens in a text editor, publishing is a git push, hosting is free on any static host. Everything else we discussed solves problems this setup doesn't have.
>
> Does that feel right, or is there something in there you actually want to keep?
