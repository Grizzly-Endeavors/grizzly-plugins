---
name: visible-failures
description: >
  Enforces the "every failure must be visible" discipline when writing error
  paths, catch/except blocks, Result-matching, ? operators, `.context()`
  chains, `.unwrap_or()` fallbacks, `.map_err()` conversions, log statements,
  or any code that handles a potentially-failing operation. Trigger when the
  user says things like "handle this error", "what if this fails", "catch
  this", "what happens when X errors", "is this the right error handling",
  "add logging here", or when you're about to write `try { ... } catch`,
  `if err != nil`, `match result`, `.map_err(|_| ...)`, `let _ = ...` on a
  Result, or any log/trace call in an error path. Also trigger during code
  review when you spot silent error swallowing, bare catch blocks, raw
  exceptions bubbling to users, or log spam on retry loops.
---

# Visible Failures

## What this enforces

**Every failure must be visible.** Silent failures — swallowed errors, empty catch blocks, `let _ = result`, logs that never fire, retries that hide the underlying problem — are non-negotiable violations of how this codebase operates.

Failures have two audiences. Both matter, and they're different.

## Two audiences, two styles

### User-facing: plain language, actionable

End users are not expected to read stack traces. Translate failures into language they can act on:

- Good: `"Couldn't connect to the server. Check your internet connection and try again."`
- Bad: `"TCP connection refused on port 443"`
- Good: `"Couldn't save your changes — the file 'notes.md' is open in another program. Close it and retry."`
- Bad: `"IOError: [Errno 32] Broken pipe"`

Never show raw error types, module paths, stack traces, or internal identifiers to end users. If the failure has no user impact, it still needs a log (see below) — it doesn't need a user message.

**Partial failures get dedicated treatment**: if 2 of 3 items synced, tell the user which succeeded, which failed, and whether they need to act. "Synced 2 of 3 items. Failed: 'report.pdf' (file too large). You can retry by..."

### Developer-facing: rich, structured diagnostics

Every error path produces a log entry with enough context to diagnose without reproducing. This means:

- **Structured fields, not string interpolation**:
  - Good: `error!(error = %e, path = %path, user_id = %uid, "failed to read config")`
  - Bad: `error!("failed to read config at {} for user {}: {}", path, uid, e)`
- **Chain context at every layer** so the log shows the full causal chain:
  - Rust: `.context("failed to load user settings")`
  - Go: `fmt.Errorf("loading settings: %w", err)`
  - Python: `raise ConfigError("loading settings") from err`
- **Pick the right level**:
  - `error` — an operation failed (config parse error, save failed)
  - `warn` — recoverable, degraded behavior (reconnecting, skipping malformed event)
  - `info` — major lifecycle events (server started, migration complete)
  - `debug` — internal state transitions
  - `trace` — payloads, per-tick timing

## Things to actively refuse

### Silent swallowing

```rust
let _ = some_operation();        // denied — Result must be handled
result.map_err(|_| MyError)?;    // denied — original error context lost
```

```python
try:
    do_thing()
except Exception:
    pass    # denied — silent failure
```

```go
value, _ := operation()  // denied for errors — the _ discards information
```

If an error is genuinely safe to ignore, log it at `debug` or `trace` with a reason, or use an explicit suppression with a comment explaining why.

### Log spam on retries

A retry loop that logs every attempt is noise. The pattern:

- Log once at `warn` when retries start: `warn!(attempt = 1, max = 5, "transient failure, retrying")`
- Log once at `warn` or `error` when retries resolve or exhaust: `error!(attempts = 5, "giving up after 5 attempts")`
- Individual retries log at `debug` at most.

### Routine success logs

Do not log "heartbeat ok", "connection alive", "widget still rendering". Absence of errors *is* the success signal. Anything that would fire on every frame/tick/poll under normal conditions belongs at `trace` at most.

### Raw errors to users

`eprintln!("{:?}", err)` on a user-facing CLI exposes debug formatting with Rust paths and types. Use `eprintln!("{err:#}")` for user-friendly display (still shows context chain but not debug noise), or better, match on the error type and emit a hand-authored user message.

## Checklist when writing an error path

Ask these in order:

1. **What's the user impact?** If zero: log only. If non-zero: user message + log.
2. **Can this recover?** If yes: log at `warn`, take the recovery path. If no: log at `error`, propagate with `.context()` / `fmt.Errorf(...: %w, ...)`.
3. **Does the log have enough structured fields to diagnose this without reproducing?** (What failed, where, for whom, with what input.)
4. **If this is in a loop or retry, am I about to create log spam?** Use the once-on-start / once-on-resolution pattern instead.
5. **If partial success is possible, does the user message distinguish succeeded from failed?**

If any answer is "no," fix it before moving on.

## How to steer when asked about error handling

When the user asks "how should I handle this error" or "what should I do if this fails," your response should:

1. Identify whether the failure has user impact.
2. Propose a user-facing message (if applicable) that is actionable and in plain language.
3. Propose a structured log call with specific fields relevant to diagnosis.
4. Propose the right log level based on recoverability.
5. Point out any retry / loop context that needs spam-avoidance.

Do not accept "just bubble it up with `?`" as a complete answer when the failure crosses a user boundary. Do not accept a logger call that's just the error message string with no fields. Do not accept a catch block without a log.
