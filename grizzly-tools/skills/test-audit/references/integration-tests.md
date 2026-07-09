# Integration Test Audit Workflow

## Phase 1: Survey

Read every integration test file for the module. Classify against the smell categories in SKILL.md, plus these integration-specific patterns:

### Environment bleeding
- Tests that depend on state left by previous tests (database rows, files on disk, cache entries).
- Tests that pass in isolation but fail when run with the suite, or vice versa.
- Missing setup/teardown that makes the test implicitly rely on execution order.

### Asserting on transport instead of contract
- Tests that assert on HTTP status codes, header values, or response shapes that are framework defaults rather than application-defined behavior.
- Verifying that a 200 was returned instead of verifying the response body contains the correct data.
- Asserting on exact JSON structure when only a few fields carry the actual business meaning.

### Test-doubles at the wrong boundary
- Mocking out the component the integration test exists to exercise. If the database is mocked in a database-integration test, it's a unit test wearing a disguise.
- Stubbing external services when a test container or fixture would give real signal.

### Scenario bloat
- Single test functions that set up a long multi-step scenario and assert at every intermediate step. When it fails, you can't tell which step broke without reading the whole test.
- These should typically be split into focused tests that each set up their own preconditions.

### Missing failure-mode coverage
- Integration tests that only cover the success path through the system.
- No tests for: partial failures (one service down, others up), invalid input at the boundary, timeout/retry behavior, concurrent access, rollback on error.
- Check what the system does when a dependency returns an error — is that tested?

### Brittle ordering / timing
- Tests that depend on events arriving in a specific order when the system doesn't guarantee ordering.
- Assertions on exact timing (`sleep(2)` then check) instead of polling or event-based verification.
- Note: pure flakiness from race conditions is out of scope. The concern here is tests that encode timing assumptions as assertions.

Read the source code alongside the tests. Integration tests need the source to understand what boundaries are being exercised and whether the test is actually crossing them.

## Phase 2: Report

Present findings organized by severity:

### High — Tests that actively hurt
Tests that encode false contracts, mask real integration failures behind mocks, or break on any deployment change. Rewrite or remove.

### Medium — Tests that don't pull their weight
Success-path-only integration tests, tests asserting on transport details instead of business outcomes, scenario bloat. Strengthen or split.

### Low — Gaps worth filling
Untested failure modes, missing rollback/retry verification, boundary conditions between components.

For each finding:
- Name the test (file + test name/description).
- State the smell category.
- Explain concretely why it's a problem — what real integration failure would slip past it, or what correct deployment change would break it.
- Propose a fix: rewrite, delete, split, or new test. Enough detail for intent, no full test code yet.

## Phase 3: Apply Changes

1. **Fix environment isolation first** — ensure every test creates its own preconditions and cleans up after itself. If tests share a database, each test should use transactions or dedicated test data that doesn't collide.
2. **Remove wrong-boundary mocks** — if a test mocks the component it's supposed to integrate with, either convert it to a real integration (test container, fixture, in-memory implementation) or move it to the unit test suite where it belongs.
3. **Assert on business outcomes** — replace transport-level assertions with domain-level ones. Instead of `expect(status).toBe(200)`, assert on the state change: the record exists, the balance changed, the event was published.
4. **Split bloated scenarios** — break multi-step tests into focused tests with their own setup. Each test should have one clear reason to fail.
5. **Add failure-mode tests** — exercise the system's behavior when dependencies fail, input is invalid, or operations need to roll back.
6. **Replace timing assertions** — swap `sleep` + assert with polling, retry-with-timeout, or event-based verification patterns.

For each changed test, verify:
- It fails when the integration it guards is broken (mentally: what would happen if the schema changed, the service was down, or the contract shifted?).
- It passes without depending on test execution order or leftover state from other tests.

## Phase 4: Verify

1. Run the full integration test suite. All tests must pass.
2. If possible, run the suite twice in succession to catch state-leaking tests.
3. If linters/formatters are configured, run them on changed test files.
4. If the project has a build step, confirm it succeeds.

Fix any failures before finishing.

## Phase 5: Summary

```
# Integration Test Audit: [module path]

## Changes
- Tests deleted: X (wrong-boundary mocks/redundant)
- Tests rewritten: X (transport assertions → business outcomes, environment isolation)
- Tests split: X (scenario bloat → focused tests)
- Tests added: X (failure-mode coverage)

## Before → After
- Total test count: X → Y
- Smell categories addressed: [list]

## Key improvements
- [Brief description of the most impactful changes]

## Verification
- Tests: pass/fail
- Build: pass/fail/skipped
- Lint: pass/fail/skipped
- Double-run (state leak check): pass/fail/skipped
```
