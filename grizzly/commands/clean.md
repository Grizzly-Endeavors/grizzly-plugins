---
description: Per-module code organization and cleanup
argument-hint: <path-to-module>
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Task", "Write", "Edit", "EnterPlanMode", "ExitPlanMode"]
---

# Module Cleanup: $ARGUMENTS

Organize and clean up the target module.

## Phase 0: Validate Target

1. Parse `$ARGUMENTS` to get the module path. If empty, stop and ask the user which module to clean.
2. Verify the path exists and is a directory (or a single large file to be broken up).
3. Identify the project root (nearest git root or directory with package.json/Cargo.toml/pyproject.toml/go.mod).

## Phase 1: Clarify Scope and Survey the Module

Begin by clarifying with the user how much they're willing to change. Are they just looking to tidy up the module itself? Or would they be open to a large refactor if the codebase would benefit from it?

Thoroughly explore the target module:

1. **Inventory**: List all files, their sizes, and line counts. Note any files over 300 lines.
2. **Internal structure**: Map the module's own imports/exports and internal dependency graph.
3. **External integration**: Identify every other module that imports from this one, and every external module this one imports from. Use Grep across the project.
4. **Public API surface**: Catalog the module's exports that other modules depend on.
5. **Project conventions**: Note what's laid out in CLAUDE.md, linters, formatters, etc. and implied conventions from the code itself. 

## Phase 2: Build the Cleanup Plan

Enter plan mode. Design a cleanup plan covering these areas (skip any that don't apply):

### File decomposition
- Identify monolithic files (300+ lines of logic) that mix unrelated concerns.
- Propose how to split them: by domain concept, by layer (types/logic/handlers), or by responsibility.
- Consider sub-modules for large sections of code with shared responsibilities.

### Internal duplication
- Find repeated patterns, copy-pasted blocks, or near-duplicate functions within the module.
- Propose shared internal helpers or consolidation.

### Cross-module shared utilities
- If this module contains generic utilities used by (or useful to) other modules, propose extracting them to a shared/common location.
- If such a shared location already exists, prefer moving code there over creating a new one.

### Structural clarity
- Ensure clear separation of concerns (types, constants, business logic, I/O, handlers).
- Propose an `index`/`mod`/`__init__` barrel file if the module lacks a clean entry point.
- Remove dead code, unused imports, and orphaned files.

### Naming and conventions
- Flag files, functions, or types with unclear or inconsistent names.
- Align with project conventions.

### Plan constraints
- **Every external import path must keep working.** If a file moves, re-export from the original location or update all importers.
- List every file outside the module that will need an import path update.

Present the plan and wait for user approval before proceeding.

## Phase 3: Apply Cleanup

After the plan is approved, execute it step by step:

1. **Work in dependency order** — move/create leaf files first, then update files that depend on them.
2. **After each logical step** (file split, extraction, rename), verify:
   - No broken imports within the module.
   - All external import paths still resolve (update importers or add re-exports).
3. **Extract shared utilities** to the agreed-upon shared location. Update all consumers.
4. **Remove dead code** and clean up any barrel/index files.

## Phase 4: Verify

1. If the project has a build step, run it and confirm zero errors.
2. If the project has tests, run them and confirm they pass.
3. If linters/formatters are configured, run them on changed files.
4. Do a final Grep for any broken imports referencing old paths.

Report results. If anything fails, fix it before finishing.

## Phase 5: Summary

Present a concise summary:

```
# Module Cleanup: [module path]

## Changes Made
- Files created: X
- Files modified: X
- Files deleted: X
- Shared utilities extracted: [list]

## Structure (after)
[tree view of the cleaned module]

## Import Updates
- Files outside module updated: X [list them]

## Verification
- Build: pass/fail/skipped
- Tests: pass/fail/skipped
- Lint: pass/fail/skipped
```

The session is complete after the summary.
