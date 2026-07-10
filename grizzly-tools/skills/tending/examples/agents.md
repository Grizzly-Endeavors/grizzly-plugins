# Agents — shapes cared-for *for the AI agent*

Concrete shapes that make a codebase cared-for for the AI agents that work in it, and that make the tools you build *for* agents worth using. An agent arrives with no memory of this repo and a finite context budget; everything it must carry to be useful competes for that budget. Care, here, is spending that budget honestly — giving an agent the context it needs, findable, and nothing it doesn't.

Two audiences hide in here: the agent working *in* your repo (which reads your agent files and indexes), and the agent consuming tools you *expose* (MCP servers, CLIs). Both entries below are marked accordingly. Use this alongside `code.md` whenever a repo is worked on by agents or ships agent-facing tools.

Note the through-line with the other lenses: this is the same instinct as `code.md`'s "imagine the next reader" and `interfaces.md`'s discoverability — an agent is just a reader with no memory and a hard budget, so the care that helps it usually helps humans too.

---

## 1. The root agent file holds only what *always* applies · (working in the repo)

The root agent file — `CLAUDE.md`, `AGENTS.md`, a rules file, whatever the tool reads first — is loaded on *every* task. Every line is paid for every time. So it should contain only what is true across the whole repo and stable over time: durable conventions, the shape of the project, how to build and test, the handful of rules that always hold.

What does *not* belong there: transient state ("we're mid-migration to X"), a deep dive on one module, today's TODOs, anything that will be false next month. Those crowd out the signal and rot in place, and a rotting instruction is worse than a missing one because the agent trusts it.

```
# less cared-for CLAUDE.md
- 900 lines, including three paragraphs on the billing module's
  internals and a note that "we're currently refactoring auth (as of March)"

# more cared-for
- the conventions that always hold, the build/test commands,
  a map of where things live, and pointers to deeper docs
- module specifics live next to the module; transient notes live
  in the tracker, not here
```

## 2. Keep current in-repo indexes for code and docs · (working in the repo)

A fresh agent has no mental map. Give it one it can actually reach: a maintained index of the codebase (where things live, what each area does, the entry points) and an index of the docs. Then finding the right context is one hop, not a blind grep across the tree.

This is `interfaces.md`'s discoverability and `code.md`'s guessable names, aimed at an agent. The same caveat as tests and docs applies with force: a *stale* index is worse than none, because it sends the agent confidently to the wrong place. If you move or rename something (a Sweep), the index is part of what the sweep must update.

## 3. Put context where it applies, at the layer it applies · (working in the repo)

Progressive disclosure for agents. Root-level files carry always-true things; module-specific guidance lives *next to the module* (a local agent file or doc), reached only when the agent works there. This keeps the always-loaded surface small and lets depth exist without taxing every task — the same principle this very skill is built on.

An agent working in one module shouldn't have to load prose about five others to get started, and shouldn't have to guess which root-level rules actually apply to its corner.

## 4. Tools built for agents earn their tokens · (building for agents)

Every tool description, parameter, and result is context an agent must carry. A tool that dumps 500 lines of boilerplate when 5 matter is not neutral — it is actively harmful, burning budget and burying the signal the agent needed. Return what's needed, in a form that's cheap to read, with a way to ask for more.

```
# less cared-for tool result
a 400-line dump: every field, internal ids, timestamps, null-heavy
metadata, repeated for all 50 items

# more cared-for
the handful of fields the caller asked about — as a plain sentence, or
tight YAML if structure helps — plus a cursor or id to fetch detail on demand
```

The tool's *description* earns its tokens too: say exactly what it does and when to reach for it, in as few words as carry the meaning. No marketing, no restating the obvious, no essay.

## 5. Don't frontload unnecessary context · (both)

Loading everything "just in case" — every doc, every schema, the whole map — before the work begins is the opposite of care. It spends the budget before the task starts and dilutes the agent's attention across things it may never touch. Prefer giving the agent the *map* and letting it pull what it needs, when it needs it. Retrieval over recitation.

## 6. One instruction, one source of truth — no conflicts · (both)

Conflicting guidance makes an agent guess, and it will guess inconsistently. When the root file says one thing and a module doc says the opposite, or a tool's description contradicts its actual behavior, that contradiction is a bug — resolve it, don't let the agent arbitrate. Name each convention once, the same way everywhere, and let the other places point at that one statement rather than restating (and eventually contradicting) it.

## 7. Shape output for whoever actually reads it · (building for agents)

Parseable is not the same as good-for-an-agent, and JSON is not the default a tool should reach for. An LLM reads plain prose perfectly well — often more easily than JSON, whose brackets, quotes, and commas are pure syntactic noise it pays for in tokens and attention without gaining meaning. Match the format to the reader:

- **When an agent reads the result directly, default to prose.** A short, plain sentence stating what happened is usually the best tool output there is. Say the thing; don't wrap it in ceremony.
- **When structure genuinely helps** — several records, nested fields, something awkward to say in a sentence — reach for **YAML**, not JSON. It carries the same structure with far less punctuation, keeping the signal-to-syntax ratio high for a model that's reading, not parsing.
- **Reserve JSON for scripts and automation.** In a CLI meant to be piped into `jq` or consumed by a program, JSON behind a `--json` flag is exactly right: a rigid, machine-parseable contract with meaningful exit codes. That reader wants the brackets; an agent reading prose does not.

And cut the decoration. Pretty markdown tables, box-drawing, ASCII dividers, restated headers, "Here are your results:" preambles — none of it adds information, and all of it spends the budget entry 4 is about protecting. If a token isn't carrying meaning, it's noise, whoever the reader is.

```
# less cared-for for an agent: a decorative table spending tokens on
# borders and repetition that carry no information
┌───────────┬───────┐
│ metric    │ value │
├───────────┼───────┤
│ processed │ 12    │
│ skipped   │ 2     │
└───────────┴───────┘

# more cared-for for an agent: plain prose, or tight YAML when structure helps
Processed 12 of 14; skipped 2 (missing checksum).

processed: 12
skipped: 2   # missing checksum
total: 14

# more cared-for for a script: JSON behind --json, a stable parseable contract
{"processed":12,"skipped":2,"total":14}
```

Whatever form you choose, keep the contract stable, so today's reader — agent or script — still works tomorrow.

## 8. Errors and results say what to do next · (building for agents)

The agent-facing sibling of the 3am-debugger and the user-facing error entries. A tool or CLI error an agent receives should carry what failed *and* an actionable next step, in a form the agent can act on — a named cause and a suggested remedy, not an opaque code or a stack trace. The agent can only recover as well as the error lets it.

## 9. Encode conventions mechanically where you can · (working in the repo)

A convention an agent can apply *without judgment* — a fixed file layout, a uniform test-placement rule, a naming pattern with no exceptions — gets applied consistently, because there is no taste to get wrong. Conventions that require reading the room get applied unevenly by humans and agents alike. Where a rule can be made mechanical and uniform, that is a gift to every future agent (and reviewer): it turns "use good judgment" into "follow the pattern."

This is not a call to bureaucratize everything — some things genuinely need judgment. But where a convention *can* be uniform, making it uniform is an act of care aimed squarely at whoever, or whatever, applies it next.

## 10. Don't make agents re-derive what could be written down · (both)

If every fresh agent has to rediscover the same thing — how to run the tests, where the entry point is, the one non-obvious gotcha that wastes an hour — that rediscovery is a toll paid over and over. Write it down once, in the index or the agent file, and the toll is paid once. This is `Fix What Trips You` in its agent form: the friction you just hit is friction the next agent will hit too, so leave the answer behind you.

---

## Care that adds

Each shape above can exist in rough form — refine it — or not exist at all — add it. For agents the absent case is the common one: most repos have never been given these, and every fresh agent pays for the gap. Small, self-contained additions:

- a seed in-repo index — even ten lines of "where things live" beats a blind grep
- the gotcha an agent (or you) just rediscovered, written into the agent file
- a module-local note beside the one genuinely tricky module
- build/test/run commands in the root agent file, if an agent would otherwise have to guess
- a `--json` flag on the CLI output that scripts are currently parsing by regex
