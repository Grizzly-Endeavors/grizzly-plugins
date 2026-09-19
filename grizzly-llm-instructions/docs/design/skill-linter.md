# Skill linter design

A catch-only linter for agent-written skills. It combines Vale (fixed-wording rules, line-level findings) with Jev (semantic judgments, section- and skill-level scores). It ships as a CLI with instructions for running it as a pre-commit hook. A companion rubric skill tells the fixing agent what a passing skill looks like; the linter itself never rewrites.

## Scope

- Lints `SKILL.md` only. Reference files under `references/` are out of scope.
- Skills first, to set the pattern. Other LLM instructions (CLAUDE.md, agents, tool descriptions) come later.
- Catch only. Findings name the problem and location; fixing is the rubric skill's job.

## Core failure mode: "don't" bloat

Agents fix unwanted behavior by adding a prohibition. The result is a skill that spends its words fencing the negative space instead of describing the target, which caps how good the skill can be. No prohibition is treated as legitimate: each one is better framed positively or enforced by the environment instead of prose.

- Explicit negations and attached fences ("Not light gray.", `❌`, "NO triangles") are Vale rules.
- "only" constructions ("This is the only supported path") are a low-severity guarding rule; keep or drop it based on noise during calibration.
- Positive statements that happen to rule something out ("Save them for title/closing") are fine.

## Checks are data

Every check is a data file, like a Vale rule. Adding or tuning a check never touches code. Code owns only the slices, section roles, and the scoring formula.

Jev check fields: slice, applies_to (section roles), direction (positive / negative), weight, curve, question (type, instructions, criteria), and fail_above / fail_below for skill-level checks that gate on their own.

### Slices

- **section:** state is the heading-delimited section plus the skill's description as its purpose.
- **skill:** state is the whole `SKILL.md` body.
- **description:** state is the frontmatter description.

Line-level findings belong to Vale. Jev findings point at a section, the skill, or the description.

The state is billed once per request; each extra question costs only its own text (~28 tokens bare, ~65 with criteria, measured). Ask every check for a slice in one request, including speculative ones, and let code consume the answers that apply.

### Section roles

- **instruction:** the default. Guides a part of the work.
- **route:** says when a case applies and sends the reader to a file for that case's instructions. A section is a route candidate when it links to a file inside the skill; Jev confirms the role with the question in `lint/route.yml`. Routing detail into reference files is a valid way to shorten a skill.
- **container:** a heading with at most a short lead-in above its subsections. Not scored.

An instruction section below the minimum size is a finding: "this doesn't deserve a section." It is not scored, so splitting into more headings cannot dodge the composite. Routes have no size minimum.

## Scoring

### Section composite

Instruction sections, positive checks:

- **goal:** states the outcome the work produces for the people it serves. Naming an aim for the work itself is only partial.
- **reasons:** says why this part of the work matters to those people. Consequences attached to single instructions do not count.
- specificity, bounded choices, and measurable (a rubric that separates good results from poor ones).

Route sections, positive checks: route-condition (the reader can tell whether this case is theirs) and route-distinct (only one sibling route fits a given situation).

Negative checks, weighted much more heavily than the positives:

- prohibitions (commands to refrain from an action; describing a problem, symptom, or smell is not a prohibition), with a curve that forgives a trace and charges a pervasive problem in full
- history (past versions, removals, deprecations, provenance)
- formatting
- value-pile (lookup values that belong in a reference file)
- sentence-complexity and relevance

Composite = (weighted positives − weighted negatives) / positive weight, divided by a size factor for instruction sections. Reported on a scale where 0.60 passes, 0.80 is good, and 0.90 is perfect.

### Skill-level

- **Formatting** (skill slice) and **description decides when to trigger** (description slice) are standalone pass/fail findings.
- **Overall skill score** is the size-weighted average of section scores, with too-short sections counted as 0, multiplied by a length factor against a reference length. It is a tracking number across iterations, not a gate.

### Gate

The pre-commit hook fails on any individual finding: unloadable frontmatter, a Vale error, a section below the minimum size, a section below the pass grade, a broken link to a file inside the skill, or a failed skill-level check.

## Vale rules

- Negations and fences, including inside ASCII diagrams.
- History phrases about the instructions' own past ("previously offered", "a prior version", "DEPRECATED"). Past events in the task domain do not match.
- Formatting counts (bold density, `---` dividers, heading density).
- Padding phrases ("It's important to note that", "In order to").
- ASD-STE100 mechanical rules: sentence length (20 words procedural, 25 descriptive), active voice, one instruction per sentence, short paragraphs. The STE dictionary is not enforced.

The plugin ships its own Vale style and `.vale.ini`; the CLI passes that config explicitly so a repo's own Vale setup does not interfere.

## Rubric skill

Hand-written guidance for the fixing agent, written from the skills that pass. It covers:

- goal as the outcome for the people served, and why it matters, as the checks define them
- positive framing, ASD-STE100 without the dictionary
- deleting and merging sections, dropping niche edge cases, and routing detail into reference files as valid fixes

A fixer given only the scoring mechanics finds the linter and iterates against it. Without the rubric it bolts reasons and bounds onto sections and splits sentences until they read choppily; the rubric exists to steer that loop toward better skills, not higher numbers.

`grizzly-tools:working-with-llms` predates these rules (it teaches earned negatives) and scores 32. The rubric skill supersedes it.

## Calibration (prerequisite to shipping)

No existing skill is a trusted "good" reference, so thresholds come from iteration:

1. Build the machinery with provisional weights.
2. Rewrite a few skills until Bear is happy with them, and record Bear's score for each.
3. Eval each rewrite against its previous version: same prompts, compare model behavior. Only a rewrite that wins the eval becomes a reference point.
4. Tune checks and weights so every original/rewrite pair ranks correctly and the anchored skills land on Bear's scores.

Anchors so far: digi-pptx v5 at 75 and troubleshooting v1 at 69, both reproduced by the current settings. Neither rewrite has been through the eval step yet. Bear's read of the full grizzly-tools ranking agrees with the linter's.

A form linter cannot see lost content: a rewrite can score higher by dropping instructions. The eval step is what catches that.

Test adversarial content early: skill text is itself instructions, and emphatic lines may steer Jev's judgment of them.

## Implementation

- Python, run with `uv` (inline script dependencies), using the official `typesafe_sdk`.
- Model pinned to `jev-1.13.0`: thresholds are calibrated against a specific version, and the tracking number must not drift when the alias moves.
- API key from the `TYPESAFE_API_KEY` environment variable.
- `vale` must be on PATH; the CLI exits with install instructions when it is missing.
- Human-readable report by default, `--json` for tooling; non-zero exit when the gate fails.
