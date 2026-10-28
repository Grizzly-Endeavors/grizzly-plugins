---
name: test-reliability
description: >
  Use when writing or fixing any test (unit, integration, end-to-end); when a
  test is flaky, times out, or fails only sometimes or under load; when a gate
  or CI run fails on code the change didn't touch; when creating or changing a
  test runner's timeouts, retries or workers; and before writing `sleep`,
  `waitForTimeout`, `setTimeout`, `test.slow()`, a `timeout:` option, a retry
  or a longer deadline in test code. For tests that break on harmless
  refactors, use test-audit. For deciding which checks run where and when
  (hooks, gates, CI stages), use lean-ci.
---

# Test Reliability

Make every wait end on the event it waits for. A longer guess only moves the failure to a busier day.

## Writing a test

1. **Name the event each step depends on, and wait on it.**

   | The step needs | Wait with |
   |---|---|
   | Something to appear or change on a page (Playwright) | A web-first assertion (`toBeVisible`, `toHaveText`, `toHaveCount(0)`) |
   | A measurement to settle, like a rect or scroll (Playwright) | `expect.poll` on the measurement |
   | A request to finish (Playwright) | `waitForResponse` registered before the action that sends it |
   | A condition in a unit test | The project's wait helper (a `waitFor` under the project's hang guard). `vi.waitFor` alone gives up after one second |
   | A message, value or state in async code | The channel, watch or callback that delivers it |
   | Background work to have finished | The signal the code gives for it; add one if there is none (step 4) |
   | A timed behavior (debounce, grace period, toast dismissal) | A controlled clock: Playwright's `page.clock`, `vi.useFakeTimers` with `vi.advanceTimersByTimeAsync`, `#[tokio::test(start_paused = true)]` with `tokio::time::advance` |
   | A state to stay put while the test looks (loading, mid-stream) | Hold it open with a gate or mock control the test releases, never a delay the test races |

2. **Assert that something didn't happen only after a later event.** First wait for something that happens after it would have (a later message, a barrier, the component stopping, a pending count reaching zero), then check it's absent.

3. **Use the project's deadlines as they are.** Use its wait helpers and hang guards (runner config, a `guard` or `testing` module) before writing a wait of your own. Don't add, raise or lower a timeout, retry or `slow` mark. A wait that ends on its condition never reaches a hang guard. A raised per-test timeout someone added earlier comes out only in the same change that makes its test wait on events, proven by step 5.

4. **When nothing observable marks the event, add the signal to the code under test**: a `data-` attribute set once an animation or placement settles, a status field, a ready or done event, a mock control.

5. **Prove it under load before you push**, for each test you added or changed that involves time, async work, I/O, processes or a browser. Run the project's stress recipe (`just <app> stress`, `just stress <filter>`, or whatever `just --list` or the docs name); every repeat must pass. With no recipe, run the test 5 times under load and require 5 passes:
   - **Playwright:** `--repeat-each=5 --workers=2`, with CDP `Emulation.setCPUThrottlingRate` at 4 set in a temporary fixture (Chromium only).
   - **Anything else:** beside a bounded burner that leaves half the cores free, `stress-ng --cpu $(( $(nproc) / 2 )) --timeout 5m`. Confirm no burner is left running afterwards.
   - **Reading a failure:** one that shows only under load means the test assumes timing or ordering, so find the assumption. A port or temp-file collision between parallel runs is a bug too: fix it.

6. **Scan your diff before committing.** Run the project's wait scan if it has one (goalaxi: `just <app> check-waits`). Otherwise grep the lines you added (`git diff -U0 | grep '^+'`) for `sleep`, `waitForTimeout`, `setTimeout(` with a delay, `.slow(`, `timeout:` and `retries`. Replace each hit with a wait from step 1, unless it's the project's own hang guard or a fake-timer advance.

## Fixing a flaky or failing test

1. **Reproduce it under load** (step 5 above) instead of rerunning it until it passes. If it doesn't fail under load, you haven't found the guess yet: read for the step that assumes something has happened by now, and raise the repeat count.
2. **Make that step wait on the event** (step 1), adding the signal when there is none (step 4). If the test needs a moment held open, hold it. Don't add a sleep, a longer timeout, `test.slow()`, a retry or a skip.
3. **Prove the fix** with the same stress run, all repeats passing, and say in the commit what the test now waits on.
4. **A failure in code your change didn't touch is still yours:** fix it, or file an `investigate` issue with the full output.

## Test runner settings and wait scans

- **When creating a runner config, size it for a shared machine:** cap workers (one per two CPUs, at most six), set retries to 0, and set each timeout as a hang guard at least 10x the slowest passing run under the stress recipe. Leave an existing config's timeouts as they are (step 3).
- **When you remove a pattern agents keep reintroducing** (sleeps in tests, raised timeouts), add a scan or lint rule that fails on it, exempting the project's own hang guards. Run it in pre-commit on staged test files, and give it test cases.
