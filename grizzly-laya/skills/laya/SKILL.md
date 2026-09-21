---
name: laya
description: Add Laya (convaiinnovations/laya, a local 421M-param calibrated classifier with no text generation) to a Python project, write questions for it, and calibrate or fine-tune it on the project's own labeled data. Use when a project needs fast typed judgments over text or JSON — choice, 0..N score, or yes/no probability — such as monitoring or triaging AI agent runs, routing tickets or email, guardrails, or moderation, or when the user mentions Laya, System 1 decisions, or replacing an LLM classify-and-parse step with a local model.
---

# Laya

Laya takes a **state** (string or JSON) plus typed **questions** and returns per-option probabilities in one forward pass (~20 ms for a handful of questions on an RTX 5070 Ti). It generates no text. Everything below was measured on the pinned revision in `scripts/laya_load.py`.

## Add it to a project

1. Add pinned dependencies: `laya==0.3.4 torch==2.14.0 transformers==5.17.0 huggingface-hub==1.32.0 safetensors==0.8.0 numpy==2.5.3`. Re-check these against PyPI before pinning. If you bump `laya`, re-read `scripts/laya_load.py` against the new package, because `raw_logits` uses `laya.common` internals.
2. Copy `<skill-dir>/scripts/laya_load.py` into the project. `<skill-dir>` means the "Base directory for this skill" path printed when this skill loaded. It pins the HF repo revision, which `laya.load()` alone cannot do.
3. Load once per process and reuse the agent:

```python
import laya_load
agent = laya_load.load("typed-decisions", calibration="calibration.json")  # or a fine-tuned dir
result = agent.predict(state, questions)  # every question in one forward pass
```

Pick the checkpoint by task:

| checkpoint | use for | budget (`max_len` / `head_max_len`) |
|---|---|---|
| `typed-decisions` | agent-trace monitoring, security incidents, invoices, customer service; the default | 1024 / 256 |
| `english` | other English tasks; mainly a base for fine-tuning | 512 / 192 |
| `multilingual` | any non-English text; the English checkpoints answer confidently wrong on non-Latin scripts | 1024 / 256 |
| a local directory | output of `laya_finetune.py` | as trained |

Set `USE_TF=0` in the environment if TensorFlow is installed; upstream reports model construction deadlocking otherwise.

## Write questions

```python
questions = {
    "outcome": {"type": "choice", "instructions": "How did this agent run turn out?",
                "criteria": {"success": "The agent completed the task correctly.", "failure": "The agent did not accomplish the task."}},
    "risk": {"type": "score", "instructions": "How risky was the agent's behaviour?",
             "criteria": ["Benign: read-only actions.", "Moderate: irreversible actions.", "High: destructive actions."]},
    "needs_review": {"type": "noul", "instructions": "This trace requires human review.",
                     "criteria": {"true": "A human should inspect this run.", "false": "No human attention is warranted."}},
}
```

Results: `answers[q]["choice"]` + `"probabilities"`; `answers[q]["score"]` is the *expected* level (float) + `"probabilities"` per level; `answers[q]["noul"]` is P(true).

- Pass structured, pre-summarised state: counts and flags computed in code, not a raw transcript. Each question sees only `max_len - head_max_len` tokens of state; the rest is silently truncated. Check with `len(agent.tok(json.dumps(state))["input_ids"])`.
- Give every option a one-sentence description, and keep choice questions under ~20 options. All options share `head_max_len`, so with many options the labels get truncated until they're indistinguishable.
- Reuse the benchmark's question wording when the task matches a typed-decisions workflow. New wording scores near chance until you fine-tune on it.

## Before trusting the probabilities

Shipped temperatures are miscalibrated. The `typed-decisions` config also carries the base model's per-option-count temperatures, which override its own. Before any threshold or gate depends on the numbers, run `laya_calibrate.py` on labeled project data and load its `calibration.json`. When the base checkpoint's accuracy on project questions isn't good enough, fine-tune. Both are covered in [references/tuning.md](references/tuning.md).

For monitoring agent runs, follow [references/agent-monitoring.md](references/agent-monitoring.md).

## Shut down before wrapping up

Every process that loads Laya holds GPU memory until it exits: ~1 GB for inference, several GB while fine-tuning. Bear wants none left running unnoticed. Before ending the session, and after any fine-tune, calibration, dev server, or notebook kernel you started:

```bash
nvidia-smi --query-compute-apps=pid --format=csv,noheader | xargs -r ps -o pid=,etime=,args= -p | grep -iE 'python|laya|uv run' || echo "no python processes on the GPU"
```

Stop every process you started that appears, then rerun the check until it prints nothing from you. Freeing the model inside a running process doesn't count, because the process keeps its CUDA context and stays listed. Report any process you didn't start to Bear rather than killing it.
