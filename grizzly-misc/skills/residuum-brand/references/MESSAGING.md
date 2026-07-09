# Residuum — Messaging Guide

## Elevator Pitch

Residuum is personal AI infrastructure — the substrate that makes Jarvis-like agents possible without writing code. Create an agent, tell it what you need, and Residuum handles everything underneath. Memory, coordination, complexity — it all just works.

## Message Hierarchy

Lead with these in order. Every surface (landing page, README, social, docs) should prioritize accordingly.

### 1. Create an agent. Tell it what you need.

The first thing anyone should feel is that creating an AI agent is as simple as having a conversation. No code, no templates, no configuration wizards. A minimal agent is created and it asks what you want. The entire "build" process is talking.

- **Subtractive**: No coding. No setup. No complexity.
- **Positive**: Create an agent. Talk to it. That's it.

### 2. It handles the rest.

The second thing is that Residuum is invisible. Memory, coordination, multi-agent management — the user never thinks about what's running underneath. The agents just work, and Residuum is the reason why.

- **Subtractive**: No managing infrastructure. No wiring things together.
- **Positive**: Your agents remember you, work together, and get things done.

### 3. They grow with you.

The third thing is that agents are shaped by ongoing conversation. Over time, users build a personal team of agents, each one knowing them better than the last. Residuum coordinates them all.

- **Subtractive**: No ceiling. No outgrowing it.
- **Positive**: Start with one agent. Build a team. They learn as you go.

## How to Talk About Features

Every feature should be described through what the user's agents do, not what Residuum does underneath. If someone needs to understand the architecture to appreciate the feature, the messaging has failed. The question is always: what do my agents do for me? Start there.

### Memory / Continuity

**Say**: "Your agents remember you." "Come back after a week — they know what you were working on." "The conversation never stopped."

**Don't say**: "Observational memory system." "Two-tier compression." "Context window management."

### Multi-Channel (desktop, phone, web, etc.)

**Say**: "Talk to your agents from anywhere." "Start a thought on your computer, finish it on your phone."

**Don't say**: "Multi-channel gateway." "Channel normalization." "WebSocket relay."

### Multi-Agent

**Say**: "Build a team of agents, each one shaped for a different part of your life." "Your agents, your way."

This is now a core part of the product story — agents are the primary unit users interact with. Frame it as natural and simple, not as a power feature.

### Proactive Behavior (Pulses)

**Say**: "Your agents check on things for you." "Morning briefings, reminders, keeping track of what matters — they handle the routine."

**Don't say**: "YAML-defined pulse scheduling." "Structured heartbeat system."

### Background Tasks

**Say**: "Hand something to your agent and walk away. It'll be done when you get back."

**Don't say**: "Sub-agent delegation with model tiering."

### Residuum Cloud

**Framing: "Connect your agents to the world."**

Residuum Cloud is the infrastructure layer that extends what agents can reach. Tunnel service, automatic backups, eventually fully hosted instances.

**Say**: "Connect your agents to the world." "Access your agents from anywhere." "Your agents, always on."

**Don't say**: "Cloud hosting." "Managed infrastructure." "SaaS tier."

**Positioning rules:**
- Free while in alpha, paid later as a natural upgrade
- Core product features are free forever — Cloud is about reach, not paywalled features
- Should feel like expanding what your agents can do, not unlocking what was locked
- Never position Cloud against the downloaded product — they're the same thing, Cloud just extends the reach

## Voice Rules

### Tone

Quiet confidence. Warm through competence, not friendliness. The voice of something that's been doing this long enough that it doesn't need to explain itself. But will, clearly, if you ask.

The voice belongs to the Residuum brand — product chrome, marketing, the "about" layer. Agents that users create have their own voices.

### Vocabulary

Write for someone who has never opened a terminal. If a sentence requires technical knowledge to parse, rewrite it. The tone stays the same — direct, understated, matter-of-fact — but the words are plain.

- "Create an agent" not "configure an agent instance"
- "Your agents remember you" not "persistent context window"
- "Talk to them from anywhere" not "multi-channel support"
- "They check on things" not "proactive pulse scheduling"
- "Download Residuum" not "self-host Residuum"

Technical depth belongs in developer documentation, which should be hard to stumble into from the primary surfaces.

### Cadence

Short sentences. Let them breathe. The landing page copy should feel like it's being said slowly, with pauses, matching the geological motion language of the UI.

Don't stack features. One idea per block. Let each one land before moving to the next.

## Framing Pattern

**Subtractive headline → positive description.**

The headline strips something away (the frustration, the complexity, the broken promise). The description underneath says what remains — what your agents actually do for you.

| Headline (subtractive) | Description (positive) |
|---|---|
| No more re-explaining yourself | Your agents remember everything. Pick up right where you left off. |
| No more starting over | Come back after a week. They know what you were working on. |
| No more juggling apps | Talk to your agents from anywhere. It's all the same conversation. |
| No more busywork | They check on the routine stuff so you don't have to. |
| No coding required | Create an agent and tell it what you need. That's the whole process. |

## Language to Avoid

| Avoid | Why | Use instead |
|---|---|---|
| "Framework" | Developer concept, not a product | "Residuum" or skip it |
| "Self-hosted" | Implies technical setup | "Download" or just skip it |
| "Platform" | Too abstract, too enterprise | Avoid entirely on user surfaces |
| "Orchestration" | Developer jargon | Don't use on user surfaces |
| "Deploy" / "instance" | Infrastructure language | "Download" / "your agents" |
| "RAG" / "embeddings" / "context window" | Technical implementation details | "Your agents remember" covers all of this |
| "Powerful" / "advanced" / "cutting-edge" | Hype words that violate the brand voice | Let the capability speak for itself |
| "vs. X" / "unlike X" / "better than X" | Residuum doesn't define itself against others | Describe what agents do, not what competitors don't |
| "Infrastructure" (user-facing) | Users shouldn't think about infrastructure | Skip it — Residuum handles this invisibly |
| "MCP" / "tokens" / "multi-channel" | Technical jargon | Plain language equivalents |

## Surface-Specific Notes

### Landing Page

The primary audience is non-technical. Lead with the promise (create agents through conversation), move to what agents do (outcome scenarios), then Residuum Cloud, then download/get started. Design principles and technical philosophy belong in docs, not here. The golem imagery and geological aesthetic communicate depth — the copy stays simple.

### README (GitHub)

Two-track approach. The primary README mirrors the landing page tone — plain language, outcome-focused, download-oriented. A separate developer README (or CONTRIBUTING.md) holds architecture, design philosophy, technical detail. The primary README links to the developer surface, but doesn't inline it.

### Social / Short-Form

One sentence, one idea. Pull from the positive descriptions, not the subtractive headlines — negation doesn't land in isolation.

- Good: "Your agents remember everything. Come back after a week — they know what you were working on."
- Bad: "No more re-explaining yourself." (needs context to land)

Frame around what agents do, not what Residuum is.

### Documentation

Matter-of-fact, thorough, assumes the reader wants to understand. This is where technical vocabulary lives. The voice here is competent, anticipates questions, doesn't waste words. This is the only surface where terms like MCP, context window, and architecture details belong.
