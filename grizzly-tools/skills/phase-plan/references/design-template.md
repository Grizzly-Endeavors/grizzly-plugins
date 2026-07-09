# <Title> — Design

> Systems level only. No file or line references. This document must stand on its own: it will be implemented later in fresh sessions that have only this doc, phases.md, and the codebase — not the conversation that produced it.

## Goal & context

What we're building or changing, and why now. The problem in one or two paragraphs.

## Shape

The major components, their responsibilities, and the boundaries between them.

## Reasoning & alternatives

Why this shape. What else was considered and why it lost. Tradeoffs accepted, so a reader who wasn't in the room understands the decision and not just the outcome.

## External touchpoints

Every place this work meets something outside its own boundary — APIs, databases, queues, other services, shared libraries. Name the contract at each touchpoint: inputs, outputs, error modes, ordering, idempotency, auth.

## Integration with existing system

How the new shape sits alongside what's already there. What it replaces, what it wraps, what it leaves untouched, and how old and new coexist during the transition.

## Open questions

Anything unresolved. Drive these to zero before finalizing.
