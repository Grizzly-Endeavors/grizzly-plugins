# /// script
# requires-python = ">=3.12"
# dependencies = ["laya==0.3.4", "torch==2.14.0", "transformers==5.17.0", "huggingface-hub==1.32.0", "safetensors==0.8.0", "numpy==2.5.3"]
# ///
"""Fine-tune a Laya checkpoint on labeled JSONL with upstream's RLCD recipe, on one GPU.

    uv run laya_finetune.py --checkpoint typed-decisions --data labeled.jsonl --out ./laya-finetuned

Holds out --val-frac of the rows (whole rows, so no state leaks into validation), prints validation accuracy
before and after training, fits temperatures on the held-out rows, and writes a checkpoint directory that
laya_load.load("./laya-finetuned") accepts.
"""
import argparse
import json
import math
import os
import random
import time

import numpy as np
import torch

import laya_calibrate
import laya_load

LR_ENCODER, LR_HEAD = 2.5e-5, 1.0e-4
GROUP_SIZE, SIGMA_START, SIGMA_END = 4, 0.4, 0.1


def encode(agent, rows):
    from laya.common import build_sequence, render_options
    items = []
    for row in rows:
        for qid, label in row["labels"].items():
            qdef = row["questions"][qid]
            q = agent._to_internal(qdef)
            seq, markers = build_sequence(agent.tok, row["state"], q, agent.cfg["max_len"], agent.cfg["head_max_len"])
            k = len(render_options(q))
            if len(markers) != k:
                raise ValueError("question %r: options do not fit in head_max_len=%d" % (qid, agent.cfg["head_max_len"]))
            y = laya_load.label_index(qdef, label)
            items.append({"ids": seq, "markers": markers, "qtype": q["t"], "target": [float(i == y) for i in range(k)]})
    return items


def collate(items, pad_id):
    from laya.common import QTYPES
    n, L, kmax = len(items), max(len(it["ids"]) for it in items), max(len(it["markers"]) for it in items)
    b = {"input_ids": torch.full((n, L), pad_id, dtype=torch.long), "attention_mask": torch.zeros((n, L), dtype=torch.long),
         "marker_pos": torch.zeros((n, kmax), dtype=torch.long), "marker_mask": torch.zeros((n, kmax), dtype=torch.bool),
         "target": torch.zeros((n, kmax)), "qtype": torch.tensor([QTYPES[it["qtype"]] for it in items])}
    for i, it in enumerate(items):
        k = len(it["markers"])
        b["input_ids"][i, :len(it["ids"])] = torch.tensor(it["ids"])
        b["attention_mask"][i, :len(it["ids"])] = 1
        b["marker_pos"][i, :k] = torch.tensor(it["markers"])
        b["marker_mask"][i, :k] = True
        b["target"][i, :k] = torch.tensor(it["target"])
    return b


def validation_samples(agent, rows):
    from laya.common import temp_bucket
    agent.model.eval()
    out = []
    for row in rows:
        for qid, (qt, z) in laya_load.raw_logits(agent, row["state"], {q: row["questions"][q] for q in row["labels"]}).items():
            out.append((qt, temp_bucket(qt, len(z)), z, laya_load.label_index(row["questions"][qid], row["labels"][qid])))
    return out


def train(agent, items, epochs, micro_batch, grad_accum, seed):
    from laya.common import proper_reward
    model, device = agent.model, agent.device
    model.encoder.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.head_checkpointing = True
    model.float().train()
    enc = [p for n, p in model.named_parameters() if n.startswith("encoder.")]
    head = [p for n, p in model.named_parameters() if not n.startswith("encoder.")]
    opt = torch.optim.AdamW([{"params": enc, "lr": LR_ENCODER}, {"params": head, "lr": LR_HEAD}], weight_decay=0.01)
    updates = max(1, math.ceil(len(items) / (micro_batch * grad_accum)) * epochs)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=updates, eta_min=1e-6)
    dtype = torch.bfloat16 if torch.cuda.get_device_capability(device)[0] >= 8 else torch.float16
    scaler = torch.amp.GradScaler("cuda", enabled=dtype == torch.float16)
    rng, t0, step = random.Random(seed), time.time(), 0
    for epoch in range(epochs):
        rng.shuffle(items)
        sigma = SIGMA_START + (SIGMA_END - SIGMA_START) * epoch / max(1, epochs - 1)
        total, batches = 0.0, 0
        for start in range(0, len(items), micro_batch):
            b = {k: v.to(device) for k, v in collate(items[start:start + micro_batch], agent.tok.pad_token_id).items()}
            with torch.autocast("cuda", dtype=dtype):
                logits, act = model(b["input_ids"], b["attention_mask"], b["marker_pos"], b["marker_mask"], b["qtype"])
            logits, mask, target = logits.float(), b["marker_mask"], b["target"]
            k = mask.sum(-1, keepdim=True).float()
            eps = torch.randn((GROUP_SIZE,) + logits.shape, device=device) * sigma * mask
            eps = (eps - eps.sum(-1, keepdim=True) / k) * mask
            z = logits.detach().unsqueeze(0) + eps
            with torch.no_grad():
                r = proper_reward(torch.softmax(z.masked_fill(~mask, -1e4), -1), target.unsqueeze(0), b["qtype"], mask, w_sph=0.75, w_rps=1.0)
                adv = (r - r.mean(0, keepdim=True)) / ((r - r.mean(0, keepdim=True)).std() + 1e-6)
            logp = -(((z - logits.unsqueeze(0)) ** 2) * mask).sum(-1) / (2 * sigma ** 2)
            loss_ce = -(target * torch.log_softmax(logits.masked_fill(~mask, -1e4), -1)).sum(-1).mean()
            loss = (-(adv * logp).mean() + loss_ce) / grad_accum + 0.0 * act.sum()
            scaler.scale(loss).backward()
            batches += 1
            total += loss.item() * grad_accum
            if batches % grad_accum == 0 or start + micro_batch >= len(items):
                scaler.unscale_(opt)
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                scaler.step(opt)
                scaler.update()
                sched.step()
                opt.zero_grad(set_to_none=True)
                step += 1
        print("epoch %d/%d  loss %.4f  updates %d/%d  %.0fs" % (epoch + 1, epochs, total / batches, step, updates, time.time() - t0), flush=True)
    del opt, scaler
    model.encoder.gradient_checkpointing_disable()
    model.head_checkpointing = False


def save(agent, out, temperature, by_options, meta):
    from safetensors.torch import save_file
    os.makedirs(out, exist_ok=True)
    save_file({k: v.half().contiguous().cpu() for k, v in agent.model.state_dict().items()}, os.path.join(out, "model.safetensors"))
    agent.model.encoder.config.save_pretrained(os.path.join(out, "encoder"))
    agent.tok.save_pretrained(os.path.join(out, "tokenizer"))
    cfg = dict(agent.cfg, temperature=temperature, temperature_by_options=by_options, fine_tuned=True, finetune=meta)
    with open(os.path.join(out, "rl_agent_config.json"), "w") as f:
        json.dump(cfg, f, indent=2)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checkpoint", default="typed-decisions", help="english | typed-decisions | multilingual | local dir")
    ap.add_argument("--data", required=True, help="labeled JSONL (see laya_load.read_jsonl)")
    ap.add_argument("--out", required=True, help="output checkpoint directory")
    ap.add_argument("--epochs", type=int, default=4)
    ap.add_argument("--val-frac", type=float, default=0.15)
    ap.add_argument("--micro-batch", type=int, default=8)
    ap.add_argument("--grad-accum", type=int, default=8)
    ap.add_argument("--max-len", type=int, help="token budget per question (default: checkpoint's)")
    ap.add_argument("--head-max-len", type=int, help="budget for question + options (default: checkpoint's)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    if not torch.cuda.is_available():
        raise SystemExit("fine-tuning needs a CUDA GPU")

    rows = laya_load.read_jsonl(args.data)
    random.Random(args.seed).shuffle(rows)
    n_val = max(1, int(len(rows) * args.val_frac))
    val_rows, train_rows = rows[:n_val], rows[n_val:]
    torch.manual_seed(args.seed)
    agent = laya_load.load(args.checkpoint)
    for key, value in (("max_len", args.max_len), ("head_max_len", args.head_max_len)):
        if value:
            agent.cfg[key] = value
    items = encode(agent, train_rows)
    before = validation_samples(agent, val_rows)
    print("train %d decisions (%d rows) | validation %d decisions (%d rows)" % (len(items), len(train_rows), len(before), len(val_rows)), flush=True)

    train(agent, items, args.epochs, args.micro_batch, args.grad_accum, args.seed)
    after = validation_samples(agent, val_rows)
    temperature, by_options = laya_calibrate.fit(after)
    report = {"validation_before": laya_calibrate.score(before, list(agent.temperature), dict(agent.temperature_by_options)),
              "validation_after": laya_calibrate.score(after, temperature, by_options)}
    save(agent, args.out, temperature, by_options,
         {"base": args.checkpoint, "base_revision": laya_load.REVISION, "rows": len(rows), "epochs": args.epochs, "report": report})
    laya_load.free(agent)
    print(json.dumps(report, indent=2))
    print("wrote", args.out)


if __name__ == "__main__":
    main()
