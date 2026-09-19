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

Every check is a data file, like a Vale rule. Adding or tuning a check never touches code. Code owns only the slice types and the scoring formula.

Jev check fields: engine, slice, direction (positive / negative), weight, question, criteria, and threshold where it gates on its own.

### Slices

- **line-in-section:** state is the heading-delimited section; one question per line, referenced by path (`lines[i]`). Gives section context and line numbers. The section is billed once per request; each extra question costs only its own text (~28 tokens bare, ~65 with criteria, measured).
- **section:** state is the heading-delimited section; one question per section.
- **skill:** state is the whole `SKILL.md` body.
- **description:** state is the frontmatter description.

When line numbers are available, findings use them.

Sections below a minimum size (in characters) fold into their parent heading for scoring, so splitting into more headings cannot dodge the score.

## Scoring

### Section composite

Positive checks (Jev, section slice):

- Clearly stated goal(s)
- Specificity
- Bounded choices
- Measurable criteria where possible
- Reasons attached to instructions (the why sharpens the instruction)

Negative checks, weighted much more heavily than the positives:

- Prohibitions and fences
- Irrelevant history (past versions, removals, deprecations)
- Excessive decoration and formatting
- Verbosity ("could this be shorter?"); repetition across sections is expected to drop as a side effect, so there is no separate cross-section check

Composite = (weighted positives − weighted negatives), normalized by section size in characters. A section below the minimum composite is a finding: "this section is not pulling its weight."

### Skill-level

- **Formatting** (skill slice) and **description decides when to trigger** (description slice) are standalone pass/fail findings.
- **Overall skill score** combines every section composite with the two skill-level results. It is a tracking number across iterations, not a gate.

### Gate

The pre-commit hook fails on any individual finding: a Vale error, a section below the minimum composite, or a failed skill-level check.

## Vale rules

- Negations and fences, including inside ASCII diagrams.
- History phrases ("previously", "was removed", "no longer", "DEPRECATED", "prior version").
- Formatting counts (bold density, `---` dividers, heading density).
- Padding phrases ("It's important to note that", "In order to").
- ASD-STE100 mechanical rules: sentence length (20 words procedural, 25 descriptive), active voice, one instruction per sentence, short paragraphs. The STE dictionary is not enforced.

The plugin ships its own Vale style and `.vale.ini`; the CLI passes that config explicitly so a repo's own Vale setup does not interfere.

## Rubric skill

Hand-written guidance for the fixing agent: specificity, bounded choices, measurable criteria, stated goals, reasons attached to instructions, positive framing, and ASD-STE100 without the dictionary. Written after calibration, from the skills that pass.

## Calibration (prerequisite to shipping)

No existing skill is a trusted "good" reference, so thresholds come from iteration:

1. Build the machinery with provisional weights.
2. Rewrite a few skills (starting with `digi-pptx`) until Bear is happy with them.
3. Eval each rewrite against its previous version: same prompts, compare model behavior. Only a rewrite that wins the eval becomes a reference point.
4. Tune weights so every original/rewrite pair ranks correctly, then set the minimum composite and size floor from where the reference skills land.

Test adversarial content early: skill text is itself instructions, and emphatic lines may steer Jev's judgment of them.

## Implementation

- Python, run with `uv` (inline script dependencies), using the official `typesafe_sdk`.
- Model pinned to `jev-1.13.0`: thresholds are calibrated against a specific version, and the tracking number must not drift when the alias moves.
- API key from the `TYPESAFE_API_KEY` environment variable.
- `vale` must be on PATH; the CLI exits with install instructions when it is missing.
- Human-readable report by default, `--json` for tooling; non-zero exit when the gate fails.
