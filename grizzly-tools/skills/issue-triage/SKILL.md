---
name: issue-triage
description: >
  For triaging GitHub issues before work on them begins. Use when the user asks to triage issues, go through issues, pull down the issues about some area, or pick up, plan or start work from one or more gh issues, even when they don't say "triage".
---

# Issue Triage

Treat each issue as an unverified claim. Assume the filer, person or agent, did not read the code closely: paths drift, the stated cause may be a guess, the proposal may duplicate an existing mechanism or cut against the project's patterns, and the listed questions may already be answered in the code or docs.

## Workflow

### 1. Collect

- Fetch the issues the user named with `gh issue view <n> --comments`, or the matching ones from `gh issue list`. If the scope is unclear, list the open issues and ask which to triage. Read every body and comment.
- Look up every `#N` an issue references (`gh issue view` / `gh pr view`) and note its type and state. Drop merged PRs and closed issues from the open work.
- Group issues that touch the same area.

### 2. Classify each issue

- **Clear-cut bug**: a concrete observed behavior that is wrong (an error, a crash, a visibly wrong result). The symptom is what to verify; the stated cause and fix are hypotheses.
- **Everything else** (features, refactors, design proposals, vague complaints, bugs with no concrete symptom): write a draft need in one sentence, independent of the proposed solution: who is hurt, by what, in what situation. Example: "Move the inbox into one shared folder" becomes "agents can't see items other agents already filed, so they file duplicates." From here on, the issue's proposal is one candidate for meeting the need, not the plan.

### 3. Gather facts with Explore agents

Launch one `Explore` agent (thoroughness "very thorough") per issue or group, all in one message so they run in parallel. Their job is to report what the code and docs contain, with `file:line` citations. They do not judge whether a claim is right or a proposal is good; you make those calls. Give each agent the issue text and ask it to report:

1. For each path, symbol, constant and behavior the issue mentions (list them as a numbered checklist): where it lives now and what the code there does.
2. The code that handles the area the need is about: the existing mechanisms, helpers and modules that touch it, and how comparable features in the codebase are built.
3. For each open question the issue lists, what the code, the docs (READMEs, design docs, systems docs, CLAUDE.md / AGENTS.md, CONTRIBUTING) or existing conventions say on the subject, quoted with the source.
4. For a bug: the code path from the reported symptom back to where it originates.

Tell the agent to say "not found" rather than guess.

### 4. Make the verdicts

For each issue, read the cited code yourself wherever a verdict depends on it, then settle:

- **Claims**: list every claim that is wrong or stale, and state whether it changes the cause, the scope, or whether the problem still exists.
- **Need**: re-read the draft need against the facts. Rewrite it if it rested on a wrong claim or an existing mechanism already meets it.
- **Cause** (bugs): trace the symptom yourself from the agent's code path and name the cause.
- **Approach** (everything else): set the issue's proposal beside at least one other way to meet the need. Compare them on whether they reuse what exists, whether they follow the patterns the codebase uses for similar features, and their long-term cost. Recommend one.
- **Open questions**: mark a question answered only when the code settles it, or when a doc settles it and the code agrees with the doc. A question about intended behavior or product direction is not settled by what the current code happens to do; give it a recommended answer in step 5.

When a fact a verdict depends on is missing, read the code yourself or send a follow-up to the same agent.

### 5. Report to the user

Open with the list of issues and a one-line verdict on each. Then, per issue:

- **Need**: the need (for bugs, the verified symptom and cause).
- **Corrections**: wrong or stale claims and the true state, with `file:line`.
- **Approach**: the options compared and your recommendation, with the reason.
- **Already answered**: each settled question with its answer and source, one line each.
- **Recommended answers**: for each open question, your answer and the reason in one line. Mark a question **needs you** only when it is hard to undo (it loses or migrates data, fixes a schema or public API other work builds on, spends money, touches security or legal exposure, or sends something outside the platform), decides how a main flow or the architecture works in a way most users would notice, or contradicts something the user said or decided. For those, add who runs into it, how often, and what changing it later costs; your answer is the default if the user doesn't reply. Before reporting, recheck each **needs you** mark against this test, and remove the ones that fail.

Close with how the issues relate: overlaps, which to settle first because others depend on it, and any that look fixed or duplicated.

### 6. Update the issues, with approval

Offer to record the outcome on each issue: the corrections, the need, the decisions made and the answered questions. Show the exact text, and any issues you propose to close, and change nothing on GitHub until the user approves. Post the outcome as a comment rather than rewriting the filer's body.
