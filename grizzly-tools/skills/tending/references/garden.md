# Garden

The unattended mode. The other four assume someone is present to steer; Garden is for when tending runs as a standing loop — `/loop /tending`, a scheduled session, "keep tending until I say stop" — and the user has walked away. The main thread becomes the gardener: it decides where attention goes, sends scouts to look, sends fixers to tend, verifies and commits their work. It does not kneel in the beds itself.

Garden is not a fifth kind of care. It is the other four modes run continuously by an orchestrator: scouts surface candidates, small ones become Rounds, large ones become a Sweep, Distill, or Gather carried out by a dedicated agent. Everything in `SKILL.md` — the disposition, behavior preservation, one concern at a time — binds every agent working under it.

## The Two Rules

**1. Orchestrate; never wander.** The orchestrator does not survey the codebase and does not edit code. When the main thread walks the code itself, it fixes whatever it happens to notice, its context fills with one narrow walk's worth of impressions, and soon everything *looks* tended because nothing outside that walk was ever seen. Every survey goes to a scout; every fix goes to a fixer; the orchestrator's context stays clear for judgment, routing, and verification. This includes *Fix What Trips You*: friction the orchestrator itself hits — a broken dev script, a failing verification tool, a misleading doc — still gets fixed right then, but by an immediately dispatched fixer, never by the orchestrator's own hands and never by filing it for later.

**2. Distrust "already looked."** A scout that finds nothing has told you about that one pass — one area, one lens, one walk, one moment — not about the area. Re-scout old ground in later cycles with a different lens or a different walk, deliberately and without apology. Keep no list of "clean" areas and never skip an assignment because it was covered before: sessions that concluded "all tended" have repeatedly been followed by fresh sessions finding days of real work. Fresh eyes on old ground is the mechanism, not a waste.

## The Cycle

```
assign → scout (parallel) → triage → dispatch → verify → commit → report → next
```

Each `/loop` firing re-enters this skill mid-garden. Start every firing by collecting what's already in flight — read the results of scouts and fixers that returned while you were away, and check the status of any background large-item agent — then resume the cycle where it stands rather than restarting blind. A background agent that finished is a result to verify and merge *this* firing, not eventually.

### 1. Assign

Pick 2–3 scout assignments. An assignment is **area × lens × walk**:

- **Area** — a module or directory, a surface (the CLI, the docs, the API, CI), or a slice that cuts across the repo (error paths, config handling, test health).
- **Lens** — the example file(s) the scout must read: always `examples/code.md`, plus `examples/interfaces.md` or `examples/agents.md` as `examples/INDEX.md` routes.
- **Walk** — the reader the scout impersonates:
  - the **new contributor**: can I orient, build, and find things?
  - the **3am debugger**: when this fails, what does it actually tell me?
  - the **first-time user**: can I succeed on this surface without being told the secret?
  - the **fresh agent**: do the agent files, indexes, and tool outputs earn their tokens?
  - the **operator**: config, logging, shutdown, deploys — what breaks at the edges?
  - the **deleter**: what here no longer earns its place?
  - the **adder**: what small kindness is missing — the help example, the empty state, the progress line, the test that would have caught the last bug?

Vary at least one axis from recent cycles. Revisiting an area is expected — change the lens or the walk, not the target. The walks are the anti-staleness device: the same directory read as the 3am debugger and read as the first-time user yields different findings, and neither pass exhausts it.

### 2. Scout

Launch the scouts in parallel as read-only exploration subagents (e.g. `Explore` in Claude Code or `research` in Antigravity). Give each the assignment and the lens, not a checklist of specific things to confirm — the lens *is* the checklist, and a scout free to notice will find what a scripted one walks past.

When filling the templates below, substitute **absolute paths** to this skill's own lens and reference files (the directory this file lives in). Spawned agents start in the tended repo, where `examples/code.md` and `references/sweep.md` resolve to nothing — a scout whose lens fails to load will quietly survey from its own general taste, which is exactly the failure the lens exists to prevent. The scout template:

> Survey `[area]` of this repo through a specific lens. First read `[absolute lens file paths]` in full — they define what "cared-for" means for this pass; do not survey from your own general sense of good code. Then walk the area as `[walk description]`. Report the 3–5 most valuable acts of care the area could receive, each with: file:line, the lens entry it falls under (by number or heading), what is missing or wrong, why a real reader/user/agent would feel it, and a size call — **small** (a self-contained fix or addition, minutes to an hour) or **large** (a rename or convention reaching many files; a system that outgrew its job; the same logic scattered across sites needing one home). A finding you cannot place under a lens entry is suspect — say so explicitly if you keep it. Additions count as much as corrections — something missing entirely is as real a finding as something done poorly. Rank by value to the reader, not by ease. If you find nothing, say exactly what you checked so the emptiness means something. Do not fix anything; do not run tests, linters, or formatters.

At triage, a report whose findings cite no lens entries is the signature of a scout that skipped its reading — discount it and reassign the ground with a fresh scout.

### 3. Triage

Hold each candidate against the disposition in `SKILL.md`: is the reader real, is behavior preserved, is it care rather than churn? Drop what fails; keep the rest. Dedupe only against work currently in flight — never against past cycles or a mental map of what's been visited.

### 4. Dispatch

**Small findings** → fixer agents, in parallel, on disjoint files (findings that touch the same files go to one fixer, or wait a cycle). The template:

> Tend one thing in this repo: `[finding, with file:line and why it matters]`. First read `[lens file path]`, especially the entry this finding falls under — it defines the target shape. Make the smallest change that fully addresses it, matching the module's local grain and preserving behavior exactly. Do NOT run tests, linting, or formatting checks. Do NOT commit. When done, report what you changed and why in two sentences.

**Large findings** (a Sweep, Distill, or Gather candidate) → dispatch **now**, to an agent, not to a backlog. Do not defer it, do not park it in a report for the user to triage, do not shrink it into a nitpick-sized version of itself. Spawn a capable agent in an isolated worktree (e.g. `isolation: "worktree"` in Claude Code) running in the background so scout cycles keep moving while it works. Prompt it to read the matching mode reference (absolute path to `references/sweep.md`, `references/distill.md`, or `references/gather.md`) plus the relevant lenses, then plan and carry the change end-to-end in its worktree — committing incrementally there, one reviewable step per commit as the mode reference prescribes — and report the shape of what it did and where the worktree lives. One large item in flight at a time is plenty. If a second large candidate appears meanwhile, name it in your cycle report and dispatch it the moment the in-flight item is verified and merged — it is next, not optional.

### 5. Verify and commit — centrally

Verification belongs to the orchestrator alone; that is why fixers are told not to run it. After fixers land, run only the narrow checks covering the files that changed (leaving full suites to the PR/CI gate per `lean-ci`), and commit per unit of care with a one-sentence message. For a returned worktree: review its commits, verify the affected scope *in the worktree*, then bring it home (merge or PR per the tended repo's convention). If verification fails, send the failure back to a fixer with the output — don't absorb the debugging into the orchestrator.

The tended repo's own `AGENTS.md`/`CLAUDE.md` outranks this file on process — commit style, PR-vs-direct, branch policy. Follow it.

### 6. Report and stopping point

One short paragraph per cycle: what was tended (with the *why*, not just the diff), what's in flight, what the next cycle will walk. After two consecutive quiet cycles across genuinely varied areas, lenses, and walks (and once any in-flight large item lands), summarize what shipped and stop rather than burning cycles indefinitely.
