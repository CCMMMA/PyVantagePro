# AGENTS.md

## Scope
These instructions apply to the full repository.

## Goal
Keep changes small, testable, and compatible with legacy behavior unless a bug fix requires a behavior change.

## Environment
- Python: use `python3`.
- Tests: use `python3 -m pytest -q`.

## Workflow
1. Reproduce the issue first.
2. Add or update tests for the exact behavior being changed.
3. Implement the minimal code change that makes the test pass.
4. Run the full test suite before committing.

## Code Style
- Preserve the existing coding style in each file.
- Prefer small, explicit transformations over broad refactors.
- Add pedagogical line-by-line comments to any source code.
- Keep comments factual and close to the code they describe.

## Parsing/Units Rules
- Document unit conversions at the conversion line.
- Keep conversions consistent between live and archive parsers.
- When adding parser fields, include at least one regression test with a packed binary fixture.

## Commit Guidance
- Use focused commits with one logical purpose.
- Commit message format: imperative summary (for example: `Fix archive rain-rate scaling`).
