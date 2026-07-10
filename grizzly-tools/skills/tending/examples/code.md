# Code Craft — shapes cared-for *for the next maintainer*

Concrete shapes that make code feel cared-for to the person who reads and changes it next. These are language-agnostic — the sketches are pseudocode meant to show the *shape* of the thing, not a specific syntax. Translate the shape into whatever the code in front of you is written in, using that project's own conventions.

This is one of three lenses (see `INDEX.md`). It is the one that always applies, because every mode leaves code behind. The other two — `interfaces.md` and `agents.md` — apply when the thing you are tending is also *used* by an end user or by an AI agent.

Use this index two ways. As **recognition**: when surveying code (especially in Rounds), these are the shapes whose *absence* marks a candidate for attention. As **target**: when building or reworking something (in Distill, Gather, or Sweep), these are the shapes to build toward.

None of these is a rule to apply everywhere. Each is a form that care tends to take. Reach for the one the situation is asking for.

---

## 1. Make illegal states unrepresentable

Let the type system carry invariants so that whole classes of bug simply cannot be written. A stranger reading the signature learns what is and isn't possible without reading the body.

```
# less cared-for: nothing stops a caller from passing a status
# string that no branch handles, or a raw id that means nothing
process(order_id: string, status: string)

# more cared-for: the set of valid states is closed and visible;
# an OrderId can't be confused with any other string
enum Status { Pending, Paid, Shipped, Cancelled }
process(order_id: OrderId, status: Status)
```

Parse, don't validate: turn loose input into a precise type *once*, at the boundary, and let everything downstream work with the guaranteed-valid form.

## 2. Errors written for the 3am debugger

An error is a message to an exhausted human who has lost context. Say what was being attempted, with what inputs, and ideally what to do about it — not just that something, somewhere, went wrong.

```
# less cared-for
throw Error("invalid input")
value.unwrap()   # panics with no story

# more cared-for
throw ConfigError(
  "loading config from {path}: missing required key 'database.url'"
)
```

One good error can save an hour. A wall of anonymous `unwrap`/`!`/`panic` on genuinely reachable failures is a debt the next person pays at the worst possible time.

## 3. Names you can guess

The same concept should be called the same word everywhere, so a reader can predict a function's name before finding it. Put units and meaning into names so the type isn't the only place the truth lives.

```
# less cared-for: three names for one idea; a bare number of... seconds? ms?
getUserData(), fetch_account(), loadProfile()
sleep(timeout)

# more cared-for: one vocabulary; the unit is impossible to misread
loadUser(), loadAccount(), loadProfile()
sleep(timeout_ms)
```

## 4. Edge cases handled on purpose

Deliberately account for the empty, the absent, the boundary, the concurrent, and the time-dependent — the cases that only bite in production. Their presence is evidence someone has actually operated the thing.

```
# less cared-for: assumes there is always at least one, and that
# "now" is timezone-free
average = sum(items) / len(items)

# more cared-for: the empty case is a named, intended outcome
if items is empty: return NoData
average = sum(items) / len(items)
```

Handling the empty list on purpose says more about care than any amount of happy-path polish.

## 5. Delete with intent

A loved codebase shrinks sometimes. Removing dead code, a concluded experiment, or a retired flag is an act of care, not destruction — it lowers the weight everyone after you has to carry.

```
# the caring change is often a deletion:
#   - the function nothing calls
#   - the branch that can't be reached
#   - the feature flag whose rollout finished two quarters ago
#   - the "temporary" compatibility shim for a thing long gone
```

If you hesitate to delete because something *might* need it, that is what version control is for. The code that stays should be code that earns its place.

## 6. Abstractions earned, not anticipated

The best helpers are born from real, repeated pain — extracted at the moment duplication actually hurts, not speculatively up front for a future that may never arrive.

```
# less cared-for: a configurable, generic framework built for one caller
#                 and a hypothetical second one
GenericProcessor(strategy, options, hooks, adapters...)

# more cared-for: three real duplications, then one small helper that
#                 fits all three exactly
retry(times, operation)
```

You can feel the difference between a helper that answers three concrete needs and one that answers an imagined one. (See Gather for how to tell them apart.)

## 7. Boundaries at the domain's joints

Modules should divide where the problem itself divides, so that a change to one concern touches one place. Then you can understand a piece without holding the whole system in your head.

```
# less cared-for: a boundary drawn because a file got too long
utils.x   # a grab-bag of unrelated helpers

# more cared-for: boundaries that match how the domain actually thinks
billing.x, notifications.x, scheduling.x
```

The tell is locality of change: when the boundaries are right, most changes stay inside one of them.

## 8. Fail loud, fail early

Validate at the edge and refuse to start in a bad state, rather than limping halfway into a run before falling over somewhere far from the cause. Encode the invariants you rely on so they are checked, not merely hoped.

```
# less cared-for: a missing setting surfaces as a mysterious crash
#                 deep in the middle of doing real work
run()   # ...500 lines later: null reference on config.timeout

# more cared-for: the program won't start in an invalid state
config = validate(load_config())   # fails here, loudly, with a reason
assert invariant_holds   # the assumption is written down and checked
```

Early, loud failure with a clear reason is a kindness. A silent bad state that corrupts a run is the opposite.

## 9. Local reasoning

Code you can understand by reading it — without chasing hidden state changed somewhere far away. Minimize reliance on global mutable state and action-at-a-distance, so a function does what it says and nothing surprising.

```
# less cared-for: the result depends on global state some other
#                 module may have quietly changed
CONFIG.mode = "fast"
result = process()          # reads CONFIG.mode from who-knows-where

# more cared-for: everything the function depends on is in front of you
result = process(input, mode = Fast)
```

The measure is whether a reader can predict what a function does from its inputs alone.

## 10. Tests as living specification

Tests that read like statements of behavior someone cares about, and that are *alive* — run, trusted, and kept honest. A graveyard of skipped or commented-out tests is worse than none, because people learn to ignore the signal entirely.

```
# less cared-for
test("it works", ...)
xit("handles retries", ...)     # skipped so long nobody remembers why

# more cared-for: the name states the behavior; nothing here is ignored
test("retries three times, then surfaces the last error", ...)
```

A good test suite is documentation that cannot go stale, because it fails when it lies.

## 11. Care for the unglamorous

The operational edges — logging, shutdown, migrations, config — are where corners get cut when nobody is watching, which is exactly why tending them signals care so strongly.

```
# the quiet marks of an operator who came back:
#   - logs that are actually useful when something is on fire
#   - graceful shutdown that finishes in-flight work and lets go cleanly
#   - migrations that are reversible, and have been run backward at least once
#   - config validated at startup, not discovered wrong mid-run
```

Nobody demos these. Their presence means someone imagined the 3am on-call reader and left them something to stand on.

---

## Care that adds

Every shape above can fall short in two ways: present but done poorly — refine it — or absent entirely — add it. Surveys reliably catch the first and walk straight past the second, because a gap has no line number to snag on. So scan for these deliberately; each is a small, self-contained *addition* the next maintainer would thank you for:

- the test that pins the behavior you just had to read the implementation to learn
- the assertion that writes down the invariant everything nearby silently assumes
- the doc comment on a module's entry point saying what it's for and who calls it
- the log line at the spot where, today, an operator watching a failure would be blind
- the startup validation for the config value that currently fails mid-run
- the named constant for the literal whose meaning you had to go ask about
