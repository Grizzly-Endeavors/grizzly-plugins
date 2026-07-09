# Unit Test Audit Workflow

## Phase 1: Survey

Read every unit test file for the module. For each test, classify it against the smell categories defined in SKILL.md.

Unit-test-specific patterns to watch for:

### Over-mocking
- Tests where the mock setup is longer than the test logic. The test is mostly verifying that the mocks were wired up correctly, not that the code works.
- Mocking the thing you're testing instead of its dependencies.
- Mocking concrete implementations that could just be used directly (e.g., mocking a pure function, mocking a simple data class constructor).

### Snapshot over-reliance
- Tests that snapshot an entire output structure when only a few fields matter. Any structural change — even adding a new field — breaks the test.
- Snapshots of error messages, log output, or serialized objects where the content is incidental to the behavior being tested.

### Test-per-method mirroring
- One test per method that just calls the method and checks the return type exists. The test suite mirrors the class structure rather than the behavior surface.
- These tests add maintenance cost without catching real bugs because they assert on structure, not semantics.

### Fixture coupling
- Tests that share mutable fixtures or depend on setup from other tests.
- Test data that's defined far from where it's used, making it hard to see what's actually being tested.

Read the source code alongside the tests. The source is needed to identify happy-path-only coverage and missing domain-critical tests.

## Phase 2: Report

Present findings organized by severity:

### High — Tests that actively hurt
Tests that break on correct refactors, require constant babysitting, or give false confidence. Rewrite or remove.

### Medium — Tests that don't pull their weight
Happy-path-only, weak assertions, tautologies. Strengthen or replace.

### Low — Gaps worth filling
Important behavior with zero coverage. New tests to write.

For each finding:
- Name the test (file + test name/description).
- State the smell category.
- Explain concretely why it's a problem — what correct change would break this test, or what bug would slip past it.
- Propose a fix: rewrite, delete, or new test. Enough detail that the intent is clear, but no full test code yet.

## Phase 3: Apply Changes

1. **Delete or gut first** — remove tautological and redundant tests before writing new ones.
2. **Rewrite fragile tests** — replace hardcoded assertions with:
   - Computed expected values derived from the same inputs.
   - Structural assertions (shape, type, invariant) instead of exact-value matching.
   - Assertions on behavior ("returns an error when input is empty") not on specific error message text.
3. **Reduce mock surface** — if a test over-mocks, replace mocks with real implementations where feasible. Only mock at true boundaries (network, filesystem, clock).
4. **Strengthen weak tests** — add meaningful assertions that would catch real bugs.
5. **Fill coverage gaps** — write new tests for the high-value missing cases.
6. **Add edge case and failure tests** — exercise error paths and boundary conditions.

For each changed test, verify:
- It fails when the behavior it guards is broken (mentally: what source mutation would make this fail?).
- It passes without depending on test execution order, external state, or timing.

## Phase 4: Verify

1. Run the full test suite for the module. All tests must pass.
2. If linters/formatters are configured, run them on changed test files.
3. If the project has a build step, confirm it succeeds.

Fix any failures before finishing.

## Phase 5: Summary

```
# Unit Test Audit: [module path]

## Changes
- Tests deleted: X (tautological/redundant)
- Tests rewritten: X (fragile/weak → behavior-focused)
- Tests added: X (coverage gaps filled)

## Before → After
- Total test count: X → Y
- Smell categories addressed: [list]

## Key improvements
- [Brief description of the most impactful changes]

## Verification
- Tests: pass/fail
- Build: pass/fail/skipped
- Lint: pass/fail/skipped
```
