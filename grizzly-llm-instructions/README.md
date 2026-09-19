# grizzly-llm-instructions

`skill-lint` lints agent skills (`SKILL.md`). It combines two engines:

- **Vale** reports line-level findings for fixed wording: prohibitions and fences, history narration, emphasis words, padding, formatting counts, and the mechanical rules of ASD-STE100 (sentence length, passive voice, paragraph length).
- **Jev** (TypeSafe's System One model) scores each heading-delimited section, the skill body as a whole, and the frontmatter description.

The linter only reports. Fixing the findings is the author's job.

## Requirements

- [uv](https://docs.astral.sh/uv/). The CLI is a uv script and installs its own Python dependencies.
- [Vale](https://vale.sh/docs/install) 3.x on `PATH`.
- `TYPESAFE_API_KEY` in the environment. Create a key at [console.typesafe.ai](https://console.typesafe.ai/).

## Usage

```sh
grizzly-llm-instructions/bin/skill-lint path/to/SKILL.md
grizzly-llm-instructions/bin/skill-lint skills/          # every SKILL.md below a directory
grizzly-llm-instructions/bin/skill-lint --json skills/   # full report as JSON
```

Exit codes: `0` pass, `1` a finding failed the gate, `2` a usage or environment error.

## What fails the gate

- Frontmatter an agent cannot load: missing, not closed, invalid YAML, or without a `name` and `description`. The file gets no other checks until this is fixed.
- A Vale alert at `error` level (prohibitions, attached fences, shouted negations, history).
- A section whose body is shorter than `min_section_chars`: it does not deserve its own section.
- A section whose score is below the pass grade (0.60).
- A skill-level check past its limit (`skill-formatting`, `description-trigger`).

Vale warnings and suggestions are reported but do not fail the gate. The overall score (0–100) is a tracking number and does not fail the gate.

## Scoring

Each section is scored from the section checks in `lint/checks/`:

```
quality = (sum(weight × positive) − sum(weight × negative)) / sum(positive weights)
score   = quality / max(1, chars / size_unit_chars) ^ size_exponent
```

The reported section score rescales this raw score linearly: `pass_raw_score` reads as 0.60 (pass) and a raw 1.0 reads as 1.0, clamped to 0–1. Grades: below 0.60 fails, 0.60 passes, 0.80 is good, 0.90–1.00 is perfect. The JSON report carries the raw score too.

Every check value is 0–1: a Noul's probability, or a Score's level divided by its highest level. `chars` is the section body length, so a long section needs more quality to pass than a short one. The parameters live in `lint/scoring.yml`, including the pinned Jev model.

## Pre-commit hook

Reference the hook from this repository:

```yaml
repos:
  - repo: https://github.com/Grizzly-Endeavors/grizzly-plugins
    rev: <tag or commit>
    hooks:
      - id: skill-lint
```

Or point a local hook at a checkout:

```yaml
repos:
  - repo: local
    hooks:
      - id: skill-lint
        name: skill-lint
        entry: /path/to/grizzly-plugins/grizzly-llm-instructions/bin/skill-lint
        language: system
        files: (^|/)SKILL\.md$
```

Both forms run on staged `SKILL.md` files. `uv`, `vale` and `TYPESAFE_API_KEY` must be available in the shell that runs `git commit`.

## Adding or tuning checks

- **Vale rules** are standard Vale YAML in `lint/styles/SkillLint/`. A rule's `level` decides whether it gates.
- **Jev checks** are YAML files in `lint/checks/`, one per check. The file name is the check id.

```yaml
slice: section          # section | skill | description
direction: negative     # positive adds to the section score, negative subtracts
weight: 3               # section checks: weight in the section score
fail_above: 0.5         # skill and description checks: gate limit (or fail_below)
question:               # passed to Jev as-is: type noul or score, instructions, criteria
  type: score
  instructions: How much of `section.text` ...
  criteria: ["None: ...", "Some: ...", "Much: ..."]
```

Questions reference the state by path: `section.text` and `section.heading` for section checks, `skill.text` for skill checks, and `description` for description checks. Section state also carries `skill_purpose`, the skill's description.
