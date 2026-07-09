# Example Shapes — Index

Concrete, language-agnostic shapes that "cared-for" tends to take. The mode references (`references/*.md`) tell you *how* to move; these tell you *what good looks like* once you get there. Use them two ways: as recognition (their absence marks a candidate) and as target (build toward them).

The shapes are split by **who** the care is for, because a thing can be cared-for for one audience and neglected for another. Consult whichever lenses match what you are tending — often more than one.

## The three lenses

- **`code.md` — for the next maintainer.** The person who reads and changes this code later (often future-you). Always relevant, because every mode leaves code behind. Illegal states made unrepresentable, errors for the 3am debugger, guessable names, boundaries at the domain's joints, care for the unglamorous operational edges.

- **`interfaces.md` — for the end user.** Whoever *uses* the thing across whatever surface it presents: a web UI, a CLI, an API, a set of docs. Relevant whenever what you are tending has a surface someone else operates. Discoverability, navigation that matches a mental model, state that survives, help at the point of need, feedback for every action, errors that tell the user what to do next.

- **`agents.md` — for the AI agent.** The agent that will work *in* this repo with no memory of it, and the agent that will consume tools you build *for* it. Relevant whenever the codebase is worked on by agents, or exposes tools (MCP servers, CLIs) meant for them. Lean root agent files, current in-repo indexes, context placed where it applies, tools that earn their tokens.

## Choosing lenses

- Tending internal library code with no user surface → `code.md`.
- Tending a CLI, web app, API, or the docs → `code.md` + `interfaces.md`.
- Tending a repo that agents work in, or building an MCP server / agent-facing CLI → `code.md` + `agents.md`.
- A tool that both humans and agents use → all three.

When in doubt, `code.md` is never wrong; add the others as the surface demands.
