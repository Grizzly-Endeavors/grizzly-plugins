# Calibrating and fine-tuning Laya

Both scripts live in `<skill-dir>/scripts/` (`<skill-dir>` is the "Base directory for this skill" path printed when the skill loaded) and carry pinned inline dependencies, so `uv run <script>` works from anywhere. They need `laya_load.py` beside them; run them in place rather than copying them.

## Labeled data (JSONL)

One example per line; `labels` may cover a subset of `questions`:

```json
{"state": {...}, "questions": {"outcome": {"type": "choice", ...}, "needs_review": {"type": "noul", ...}, "risk": {"type": "score", ...}}, "labels": {"outcome": "partial", "needs_review": true, "risk": 2}}
```

Label types: choice → one of the question's `criteria` keys; noul → JSON `true`/`false`; score → a 0-based level index. The scripts reject anything else.

Keep a test file of examples that never go into fine-tuning. Split by run, not by question, so no state appears on both sides.

## Calibrate (minutes; any checkpoint)

```bash
uv run <skill-dir>/scripts/laya_calibrate.py --checkpoint typed-decisions --data test.jsonl --out calibration.json
```

It fits temperatures on half the decisions and reports accuracy, NLL and ECE on the other half for the shipped and fitted temperatures, then refits on everything and writes `calibration.json`. You need at least 40 labeled decisions; aim for 200+. Use the fitted file if its held-out ECE is lower. Accuracy doesn't change, since calibration only rescales the probabilities.

## Fine-tune (about a minute per 1,500 decisions on an RTX 5070 Ti)

```bash
uv run <skill-dir>/scripts/laya_finetune.py --checkpoint typed-decisions --data train.jsonl --out ./laya-finetuned
```

It holds out 15% of the rows, prints validation accuracy before and after, fits temperatures on that held-out split, and writes a checkpoint directory for `laya_load.load("./laya-finetuned")`. Defaults follow upstream's recipe (4 epochs, encoder LR 2.5e-5, head LR 1e-4, effective batch 64). Pass `--max-len` / `--head-max-len` to raise the token budget (up to 8192 total; train and infer with the same values).

Then run `laya_calibrate.py --checkpoint ./laya-finetuned --data test.jsonl` for an unbiased score. The fine-tune's own "validation_after" ECE uses temperatures fit on that same split, so it reads optimistically.

Run jobs expected to take over ~2 minutes in the background. Watch them until the process exits, then run the GPU check from SKILL.md.

## Ship the result

Commit `calibration.json` to the project. Store the fine-tuned directory (~800 MB) outside git: point `laya_load.load()` at its path, and record in the project's docs where it lives and which data trained it.
