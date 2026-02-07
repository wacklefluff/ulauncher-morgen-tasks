# Manual Test Plan — v1.2.0 API Limit Notice

**Date**: 2026-02-07  
**Scope**: Verify UI warning behavior for Morgen task-list endpoint cap (`limit=100`) and ensure search still works without index optimization.

## Preconditions

- Restart Ulauncher in verbose mode:
  - `pkill ulauncher && ulauncher -v`
- Extension enabled
- Morgen API key configured

## Tests

- **LIM01** — Warning appears when exactly 100 tasks are loaded
  1. Ensure cache/API response yields exactly 100 tasks (real account or seeded test set)
  2. Type: `mg`
  - **Expected**:
    - Header appears normally
    - Additional item appears: `API list limit reached (100 tasks)`
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: API cap notice rendered as expected at 100 tasks.

- **LIM02** — Warning appears in cached fallback flow
  1. Load tasks once (`mg refresh`) so cache is populated with 100 tasks
  2. Simulate network/API failure (offline or temporary block)
  3. Type: `mg`
  - **Expected**:
    - Fallback banner (`showing cached data`) appears
    - `API list limit reached (100 tasks)` item is also shown
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: Cached fallback banner and cap warning both appeared.

- **LIM03** — Search still works correctly without index path
  1. Type: `mg <known keyword>`
  2. Type same words in different order
  - **Expected**:
    - Matching results appear in both cases
    - No regression in normal search behavior
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: Search behavior remained correct and word-order independent.
