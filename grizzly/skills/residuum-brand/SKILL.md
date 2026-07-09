---
name: residuum-brand
description: >
  Residuum's brand identity, voice, aesthetic, messaging, and project philosophy.
  Trigger this skill whenever working on anything that touches Residuum's
  public-facing surfaces — landing page copy, README text, social posts,
  documentation tone, UI styling, component design, color choices, typography,
  motion/animation decisions, marketing language, or any creative asset for the
  project. Also trigger when reviewing or critiquing existing Residuum
  copy/design for brand consistency, when naming features or writing feature
  descriptions, or when making any aesthetic decision in Residuum's codebase
  (CSS, Tailwind config, design tokens, etc.). Additionally, trigger when
  evaluating whether a feature, pattern, or dependency belongs in Residuum —
  scope decisions, architectural direction, what to add, what to cut, what
  constitutes "done." If the work involves Residuum and a human will read or
  see the output, or if the decision shapes what Residuum becomes, this skill
  probably applies.
---

# Residuum Brand

This skill contains the brand system and project philosophy for Residuum — identity, voice, aesthetic, messaging, and the thinking behind decisions. These docs work together: identity defines *what* Residuum is, messaging defines *how to talk about it*, aesthetic defines *how it looks and moves*, and philosophy defines *how to decide what belongs*.

## Quick Reference

Before diving into the reference files, here are the non-negotiable principles that apply across all surfaces:

**Voice:** Quiet confidence. Warm through competence, not friendliness. Direct without being cold. The voice of something that's been doing this long enough that it doesn't need to explain itself — but will, clearly, if you ask.

**Framing pattern:** Subtractive headline → positive description. The headline strips something away (the frustration, the complexity). The description says what remains.

**Core palette:** Near-black stone backgrounds (`#0e0e10`), blue energy veins (`#3b8bdb`), moss green accents (`#6b7a4a`). Everything else is grey stone tones.

**Typography:** Cinzel (display headings), Literata 300 (body), JetBrains Mono (code/labels).

**Motion:** Slow and geological. Fade up from below, staggered 120ms between siblings, ease-out. Nothing snaps.

**The construct:** A colossal stone golem, mid-stride. Weathered, cracked, unhurried. Blue energy in the seams. Moss and vines in the still places. It represents Residuum as infrastructure — carrying agents and users on its shoulders. It doesn't serve — it sustains. It was moving before you arrived.

## Routing

Read the reference file(s) that match the work being done. Often more than one will apply. **POSITIONING.md takes precedence** over other references where they conflict — it defines the product framing that all other docs serve.

### Positioning — how Residuum is *framed as a product*
**When:** Any user-facing copy, messaging decisions, audience questions, feature naming, landing page work, README writing, or decisions about what language to use or avoid. Also when evaluating whether something belongs on a public surface vs. developer docs.
**Read:** `references/POSITIONING.md`

### Identity — what Residuum *is*
**When:** Naming things. Writing "about" content. Making decisions about what the product should feel like. Evaluating whether something is on-brand. Any work where the question is "does this feel like Residuum?"
**Read:** `references/IDENTITY.md`

### Messaging — how to *talk about* Residuum
**When:** Writing copy for any surface — landing page, README, social, docs, feature descriptions, changelogs, release notes. Also when reviewing existing copy for brand consistency.
**Read:** `references/MESSAGING.md`

### Aesthetic — how Residuum *looks and moves*
**When:** Making visual or interaction design decisions. Writing CSS, choosing colors, setting up animations, designing components, building UI. Any work where the output is something a user will see rendered on screen.
**Read:** `references/AESTHETIC.md`

### Philosophy — how to *decide what belongs*
**When:** Evaluating whether a feature, dependency, or pattern should exist in Residuum. Scoping work. Deciding what to cut. Determining when something is done. Any contribution where the question is "should this be here?" or "is this the right shape?"
**Read:** `references/PHILOSOPHY.md`

## Anti-Patterns

These are the ways brand work most commonly goes wrong for Residuum:

- **Hype language.** "Powerful," "advanced," "cutting-edge," "revolutionary." Let the capability speak. If you catch yourself reaching for a superlative, the sentence probably needs to be rewritten, not amplified.
- **Technical jargon in messaging surfaces.** "RAG," "context window," "orchestration," "multi-channel gateway." These belong in documentation, not in anything a non-technical user might read first.
- **Comparison framing.** "Unlike X," "better than Y." Residuum doesn't define itself against others. Describe what it does, full stop.
- **Startup energy.** Exclamation points, urgency, "get started now," bright gradients, bouncy animations. The construct doesn't rush. Neither does the brand.
- **Over-explaining.** The brand voice trusts the reader. One idea per block. Short sentences. Let them breathe.
- **Positioning Residuum as the assistant.** Residuum is the substrate, not the agent. Users talk to their agents, not to Residuum. Copy should describe what agents do, not what Residuum does.
- **Leading with philosophy before utility.** The positioning ladder is: category → capability → differentiator → philosophy. Never reverse this for a new audience.
- **Infrastructure/hosting language on user surfaces.** "Self-host," "deploy," "instance," "server" — none of these exist on user-facing surfaces. Residuum is software you download.
- **Assuming the reader is technical.** The primary audience doesn't know what GitHub is. If jargon is needed, it belongs on a separate developer surface that is hard to stumble into.
