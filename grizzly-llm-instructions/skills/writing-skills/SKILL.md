---
name: writing-skills
description: "Write, revise, or fix an agent skill (SKILL.md) so a model using it does good work, including in cases the skill does not spell out. Use when creating a new skill, rewriting or tightening an existing one, or fixing findings from skill-lint. Trigger on requests like 'write a skill for', 'improve this skill', 'this skill is too long', 'clean up this SKILL.md', or 'skill-lint failed'."
---

# Writing Skills

A good skill gives a model a clear picture of what good work looks like and why it matters. With that picture, the model handles the cases its author did not foresee. Rules and values reach as far as the cases they name. Every added rule also costs context the model reads on every use.

Aim for a skill a new reader could follow on first read. Each section names its target, says why it matters, and shows how to check the result.

## Give each section a goal and a reason

Open each section with the outcome its work produces for the people it serves: the viewer, the user, the maintainer. "Each slide builds around one visual so viewers keep their attention" is a goal. "Fix the root cause" names an aim for the work, but it does not say what anyone gains.

Then say why that outcome matters to those people. "Walls of text lose viewers even for engaging speakers" explains the stakes for the whole section. The model uses that reason to decide cases the section does not list.

Add a reason to a single instruction when the instruction would look arbitrary without it. A reason earns its place when it tells the reader something the instruction did not already say.

A section passes when a reader can answer two questions from it. Who benefits when this part goes well? What do they lose when it goes badly?

## Describe the target

The model does its best work when every sentence points at the result you want. A prohibition marks one place the result is not, and the model still has to guess where it is. So each fence you add leaves the target as vague as before and costs the reader context.

State the behavior you want. Rewrite each `don't`, `never`, `avoid`, `X, not Y`, `instead of`, and `rather than` as that behavior. A consequence written to forbid something counts too. "Shrinking type breaks the hierarchy" really says `don't shrink type`, so write "split long lists across two slides".

Describing a problem the reader must recognize is different. A catalog of code smells, a symptom list, or the conditions that call for the skill all describe the problem. Keep those.

Enforce a hard limit in the environment with a script, a hook, or a check. Prose is the weakest place to hold one.

A section passes when every instruction in it names something to do.

## Give the work a rubric

A model that can judge its own result fixes its mistakes before anyone sees them. The person relying on the skill then gets finished work, and fewer rounds of review.

End each instructional section with the criteria that separate a good result from a poor one. "A fix is ready to ship once the original symptom cannot reproduce" lets the model check its own work. A list of values tells the model what to apply; a rubric tells it how to judge the outcome.

Bound a choice when the bound shapes the work, such as "build each slide around one visual". A number placed on a list the reader follows anyway adds words and no guidance.

## Keep SKILL.md lean

The model reads every line of SKILL.md on every use, so each section spends the reader's attention. A lean skill keeps that attention on the cases that come up.

Delete or merge a weak section; that is often the best fix. Two sections that make the same argument belong together. A section that restates another can go.

Drop niche edge cases. A rule for a rare situation costs context on every run and pulls attention from the common ones.

Move lookup values into a reference file: colors, sizes, geometry, format strings, and file indexes. Keep in SKILL.md what those values are for and how to judge them. Link the file where the model needs it.

Route detailed workflows to reference files. A route section says when its case applies and which file to read. Give each route a condition the reader can recognize. Make sibling routes distinct, so each situation fits one of them:

```markdown
### Unit tests
**When:** the tests exercise functions or classes in isolation, with mocks at most.
**Read:** `references/unit-tests.md`
```

## Write plainly

Plain sentences carry one meaning to every model that reads them. Tangled sentences leave room for a reading the author did not intend.

Write in ASD-STE100 style without its dictionary. Keep procedure sentences to 20 words and descriptions to 25. Use active voice, one instruction per sentence, and paragraphs of six sentences or fewer.

Shorten by cutting filler words first. Split a long sentence at a real break in meaning, so each half still reads naturally.

Use headings for real sections and bold for the few terms a reader needs to catch. Horizontal rules, emoji, and ASCII art cost tokens and carry no instruction.

Describe the skill as it is now. The model acts on the current instructions, so every sentence should be one it can act on today. Change records belong in git or an ADR.

## Write the description for triggering

An agent reads the frontmatter description to decide whether to load the skill. A description full of details that matter after loading leaves the agent guessing when to use it.

Fill the description with the tasks, requests, situations, and trigger phrases that should load the skill. Move values and steps into the body.

Quote the description when it contains a colon followed by a space. Unquoted, YAML reads that colon as a new key, and the skill fails to load.

## Check the work with skill-lint

Run the linter on the skill after each revision. It lives in this plugin's `bin/` directory, two levels above this skill:

```sh
<this skill's directory>/../../bin/skill-lint path/to/SKILL.md
```

It needs `uv`, `vale`, and `TYPESAFE_API_KEY`. Vale reports line-level findings. Jev scores each section from 0 to 1, where 0.60 passes, 0.80 is good, and 0.90 is perfect.

Read each finding as a question about the skill, and fix the skill. A reason bolted on to lift a score, or a sentence split mid-thought to meet a length limit, raises the number and weakens the skill.

The linter measures form and cannot see lost content. After a rewrite, run the same prompts with the new skill and the previous version. Keep the rewrite when a model using it does better work.
