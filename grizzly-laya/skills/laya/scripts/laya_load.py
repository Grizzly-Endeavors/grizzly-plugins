"""Load a pinned Laya checkpoint with calibration applied, and expose raw logits for fitting.

Copy this file into a project that uses Laya. Pin `laya==0.3.4` alongside it: the checkpoint revision
below was reviewed against that package version.
"""
import json
import os

import numpy as np
import torch

REPO = "convaiinnovations/laya"
REVISION = "1c5edc17a7acd8701df6fc341c0d179f1c62c982"
CHECKPOINTS = {"english": None, "typed-decisions": "typed-decisions", "multilingual": "multilingual"}


def checkpoint_dir(checkpoint):
    """Resolve a checkpoint name (see CHECKPOINTS) or a local directory to a local directory."""
    if os.path.isdir(checkpoint):
        return checkpoint
    if checkpoint not in CHECKPOINTS:
        raise ValueError("unknown checkpoint %r: use one of %s or a local directory" % (checkpoint, sorted(CHECKPOINTS)))
    from huggingface_hub import snapshot_download
    sub = CHECKPOINTS[checkpoint]
    patterns = ["%s/*" % sub] if sub else ["model.safetensors", "rl_agent_config.json", "encoder/*", "tokenizer/*"]
    root = snapshot_download(REPO, revision=REVISION, allow_patterns=patterns)
    return os.path.join(root, sub) if sub else root


def apply_calibration(agent, path):
    """Replace the checkpoint's shipped temperatures with ones fitted by laya_calibrate.py."""
    with open(path) as f:
        cal = json.load(f)
    agent.temperature = cal["temperature"]
    agent.temperature_by_options = cal["temperature_by_options"]


def load(checkpoint="typed-decisions", calibration=None, device=None):
    """Return a laya.Agent. `calibration` is a calibration.json path; without one the shipped temperatures are used."""
    import laya
    agent = laya.load(checkpoint_dir(checkpoint), device=device)
    if agent.device.type != "cuda" and (device or "cuda") == "cuda" and torch.cuda.is_available():
        raise RuntimeError("Laya fell back to %s although CUDA is available; see the warning above" % agent.device)
    if calibration:
        apply_calibration(agent, calibration)
    return agent


def free(agent):
    """Release the agent's GPU memory in a process that keeps running afterwards."""
    agent.model.to("cpu")
    del agent.model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


@torch.no_grad()
def raw_logits(agent, state, questions):
    """Uncalibrated per-option logits: {qid: (qtype_index, np.ndarray)} for one state and its questions."""
    from laya.common import QTYPES, build_sequence, collate_items, render_options
    ids, items = list(questions), []
    for qid in ids:
        q = agent._to_internal(questions[qid])
        seq, markers = build_sequence(agent.tok, state, q, agent.cfg["max_len"], agent.cfg["head_max_len"])
        if len(markers) != len(render_options(q)):
            raise ValueError("question %r: options do not fit in head_max_len=%d" % (qid, agent.cfg["head_max_len"]))
        items.append({"ids": seq, "markers": markers, "qtype": QTYPES[q["t"]]})
    b = collate_items([items], agent.tok.pad_token_id)
    with torch.autocast(device_type=agent.device.type, dtype=agent.dtype, enabled=agent.device.type == "cuda"):
        logits, _ = agent.model(*(b[k].to(agent.device) for k in ("input_ids", "attention_mask", "marker_pos", "marker_mask", "qtype")))
    logits = logits.float().cpu().numpy()
    return {qid: (items[r]["qtype"], logits[r, :len(items[r]["markers"])]) for r, qid in enumerate(ids)}


def label_index(qdef, label):
    """Index of a gold label in the question's option order (choice key, noul bool, score level int)."""
    if qdef["type"] == "choice":
        keys = list(qdef["criteria"]) if isinstance(qdef["criteria"], dict) else list(qdef["criteria"])
        return keys.index(label)
    if qdef["type"] == "noul":
        if not isinstance(label, bool):
            raise ValueError("noul label must be true/false, got %r" % (label,))
        return int(label)
    level = int(label)
    if not 0 <= level < len(qdef["criteria"]):
        raise ValueError("score label %r outside 0..%d" % (label, len(qdef["criteria"]) - 1))
    return level


def read_jsonl(path):
    """Labeled examples: one {"state": ..., "questions": {...}, "labels": {qid: label}} per line."""
    rows = []
    with open(path) as f:
        for n, line in enumerate(f, 1):
            if line.strip():
                row = json.loads(line)
                missing = set(row["labels"]) - set(row["questions"])
                if missing:
                    raise ValueError("%s:%d: labels for undefined questions %s" % (path, n, sorted(missing)))
                rows.append(row)
    return rows


def softmax(z):
    p = np.exp(z - z.max())
    return p / p.sum()
