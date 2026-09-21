# /// script
# requires-python = ">=3.12"
# dependencies = ["laya==0.3.4", "torch==2.14.0", "transformers==5.17.0", "huggingface-hub==1.32.0", "safetensors==0.8.0", "numpy==2.5.3"]
# ///
"""Fit Laya temperatures on labeled data and report held-out accuracy / ECE before and after.

    uv run laya_calibrate.py --checkpoint typed-decisions --data labeled.jsonl --out calibration.json

Half the data fits temperatures and the other half scores them; the written calibration.json is then refit
on all rows. Load it with laya_load.load(checkpoint, calibration="calibration.json").
"""
import argparse
import json
import random
import sys

import numpy as np

import laya_load

MIN_BUCKET = 20
GRID = np.exp(np.linspace(np.log(0.05), np.log(20.0), 400))


def fit_temperature(samples):
    """Temperature minimising mean NLL of the gold label; samples = [(logits, gold_index)]."""
    nll = np.zeros(len(GRID))
    for z, y in samples:
        zs = z[None, :] / GRID[:, None]
        m = zs.max(1, keepdims=True)
        nll += (m[:, 0] + np.log(np.exp(zs - m).sum(1))) - zs[:, y]
    return float(GRID[int(nll.argmin())])


def fit(samples):
    """Per-(type, option-count) temperatures with a per-type fallback; samples = [(qtype, bucket, logits, y)]."""
    temperature = []
    for qt in range(3):
        sel = [(z, y) for t, _, z, y in samples if t == qt]
        temperature.append(fit_temperature(sel) if len(sel) >= MIN_BUCKET else 1.0)
    by_options = {}
    for bucket in sorted({b for _, b, _, _ in samples}):
        sel = [(z, y) for _, b, z, y in samples if b == bucket]
        if len(sel) >= MIN_BUCKET:
            by_options[bucket] = fit_temperature(sel)
    return temperature, by_options


def score(samples, temperature, by_options):
    """Accuracy, mean NLL and 15-bin ECE of top-1 confidence under the given temperatures."""
    from laya.common import ece_score
    conf, correct, nll = [], [], []
    for qt, bucket, z, y in samples:
        p = laya_load.softmax(z / by_options.get(bucket, temperature[qt]))
        conf.append(p.max())
        correct.append(float(p.argmax() == y))
        nll.append(-np.log(max(p[y], 1e-12)))
    return {"accuracy": round(float(np.mean(correct)), 4), "nll": round(float(np.mean(nll)), 4),
            "ece": round(ece_score(np.array(conf), np.array(correct)), 4)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checkpoint", default="typed-decisions", help="english | typed-decisions | multilingual | local dir")
    ap.add_argument("--data", required=True, help="labeled JSONL (see laya_load.read_jsonl)")
    ap.add_argument("--out", required=True, help="calibration.json to write")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    from laya.common import temp_bucket
    rows = laya_load.read_jsonl(args.data)
    agent = laya_load.load(args.checkpoint)
    samples = []
    for row in rows:
        for qid, (qt, z) in laya_load.raw_logits(agent, row["state"], {q: row["questions"][q] for q in row["labels"]}).items():
            y = laya_load.label_index(row["questions"][qid], row["labels"][qid])
            samples.append((qt, temp_bucket(qt, len(z)), z, y))
    shipped = (list(agent.temperature), dict(agent.temperature_by_options))
    laya_load.free(agent)
    if len(samples) < 2 * MIN_BUCKET:
        sys.exit("only %d labeled decisions; need at least %d to fit and evaluate" % (len(samples), 2 * MIN_BUCKET))

    random.Random(args.seed).shuffle(samples)
    half = len(samples) // 2
    fitted = fit(samples[:half])
    report = {"decisions": len(samples), "heldout": len(samples) - half,
              "shipped_temperatures": score(samples[half:], *shipped),
              "fitted_temperatures": score(samples[half:], *fitted)}
    temperature, by_options = fit(samples)
    with open(args.out, "w") as f:
        json.dump({"checkpoint": args.checkpoint, "revision": laya_load.REVISION, "decisions": len(samples),
                   "temperature": temperature, "temperature_by_options": by_options, "heldout_report": report}, f, indent=2)
    print(json.dumps(report, indent=2))
    print("wrote", args.out)


if __name__ == "__main__":
    main()
