---
name: test-audit
description: >
  Audit tests in a module for meaningful signal quality. Identifies tests that
  break on correct refactors, only cover happy paths, assert on implementation
  details instead of behavior, or give false confidence. Two workflows: unit
  tests and integration tests. Trigger when the user says "test-audit",
  "audit tests", "audit my tests", "check test quality", or asks whether
  their tests are actually catching real bugs. Also trigger when the user
  asks about test fragility, flaky tests that aren't timing-related, or
  tests that need constant updating after harmless changes.
---

# Test Audit

The goal: every test should produce a meaningful signal. When a test fails, it should mean the code is wrong — not that someone forgot to update a hardcoded value in a test fixture. Tests that meet this bar rarely need changing, and when they do break, it's worth paying attention.

## Smell Categories

Both workflows use the same classification system. Scan for these when surveying tests:

**Tautological tests** — Asserts a constant equals itself, or that a constructor returns non-null. Can never fail because it tests no real behavior.

**Hardcoded-value fragility** — Asserts against magic numbers, specific string literals, exact timestamps, or snapshot-style output. Breaks when you change a label or reword a message even though behavior is correct.

**Happy-path-only coverage** — The function under test has error conditions, edge cases, or branching logic, but the test only covers the golden path. Read the source to identify untested branches.

**Implementation coupling** — Asserts on internal state, private method calls, exact call counts, or specific middleware/hook invocation order. Breaks when you refactor internals without changing behavior.

**Redundant or overlapping tests** — Multiple tests that exercise the exact same code path with trivially different inputs and no distinct edge case.

**Weak assertions** — Runs code but asserts almost nothing (e.g., "does not throw", `expect(result).toBeTruthy()` when result is always truthy). Doesn't verify the interesting part of the behavior.

**Missing domain-critical tests** — Important behavior with zero test coverage. Focus on error handling, boundary conditions, and state transitions — not exhaustive line coverage.

## Routing

Determine which workflow applies and read the corresponding reference file.

### Unit Tests
**When:** The target module's tests are unit tests — testing individual functions, methods, classes, or modules in isolation. Mocks/stubs may be present. No real databases, network calls, or multi-service interaction.
**Read:** `references/unit-tests.md`

### Integration Tests
**When:** The target module's tests exercise interactions between components — real database queries, HTTP calls to running services, multi-step workflows, end-to-end pipelines, or API contract tests.
**Read:** `references/integration-tests.md`

If the module has both, run each workflow on the relevant subset. Start with whichever set is larger.

## Constraints (both workflows)

- Do not propose tests for trivial getters, simple data containers, or pure configuration.
- Do not inflate test count for its own sake. Fewer, stronger tests beat many weak ones.
- Prefer testing observable behavior over internal mechanics.
- Property-based / generative tests are fair game where the domain fits (numeric ranges, parsing, serialization round-trips).

## What This Skill Is NOT

- Not a test coverage tool. Line coverage percentage is not the metric.
- Not a style guide. Test naming conventions and file organization are out of scope.
- Not a performance audit. Slow tests aren't inherently bad signal.
- Not for flaky tests caused by timing/concurrency. Those are infrastructure problems, not signal problems.
