---
name: test-audit
description: Audit a module's unit or integration tests for signal quality — identifying tests that break on harmless refactors, only cover happy paths, over-mock internals, or give false confidence. User-invoked (e.g. "/test-audit", "audit my tests"). For flaky/timing tests, use test-reliability.
disable-model-invocation: true
---

# Test Audit

Every test should produce a meaningful signal: when it fails, the code is wrong — not a hardcoded label or internal call count. Line coverage percentage is not the metric; fewer, stronger behavioral tests beat many fragile ones.

## Smells to Check

- **Tautologies:** asserting constants, trivial constructors, or mock return values you just set up.
- **Hardcoded-value fragility:** exact error strings, timestamps, or snapshots that break on harmless copy changes.
- **Happy-path-only:** branching logic, error handling, boundary values, or state transitions with zero tests.
- **Implementation coupling & over-mocking:** asserting on private helpers, internal state, call counts, or mocking types the repo owns instead of using real objects or in-memory fakes.
- **Redundant tests:** multiple cases exercising the exact same code path with no distinct edge case.
- **Weak assertions:** checking only "does not throw" or truthiness without verifying the actual outcome.
- **Wrong boundary (integration):** mocking away the real DB, HTTP layer, or contract the integration test exists to prove, or bloating one scenario with unrelated assertions.

## Workflow

1. **Read the module and its tests together.** Map what the module actually guarantees (contracts, invariants, failure modes) against what the tests currently verify.
2. **Classify findings concisely:** list tests to delete (tautological/redundant), rewrite (fragile/over-mocked), and add (missing domain-critical edge cases or error paths). Skip trivial getters, data containers, and pure config.
3. **Apply agreed changes:** rewrite tests to assert observable behavior and real contracts; use property-based tests where the domain fits (parsers, serialization round-trips, numeric bounds).
4. **Verify once** using the narrow test command for the audited module (let hooks and CI cover the full suite per `lean-ci`). Do not fix timing flakes with retries or sleeps — use `test-reliability` for timing/concurrency defects.
