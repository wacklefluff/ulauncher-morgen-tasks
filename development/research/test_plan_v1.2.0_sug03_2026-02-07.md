# Manual Test Plan — v1.2.0 SUG-03 Search Threshold

**Date**: 2026-02-07  
**Scope**: Verify search behavior remains correct after enabling search index only for task sets with >=200 tasks.

## Preconditions

- Restart Ulauncher in verbose mode:
  - `pkill ulauncher && ulauncher -v`
- Extension enabled
- Morgen API key set
- Ensure cache can be refreshed (`mg !`)

## Tests

- **S01** — Normal search still works for typical/small task sets
  1. Type: `mg !` (one-shot refresh)
  2. Type: `mg <known keyword from an existing task>`
  3. Repeat with two-word query in swapped order
  - **Expected**:
    - Matching tasks appear
    - Search remains word-order independent
    - No UI regressions or crashes
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **S02** — Refresh + search flow remains stable
  1. Type: `mg refresh`
  2. Type: `mg refresh <query>`
  3. Type: `mg !<query>`
  - **Expected**:
    - Exact `mg refresh` triggers refresh
    - `mg refresh <query>` and `mg !<query>` do not force-refresh each keystroke; they behave like normal search with notice
  - **Result**: [ ] PASS  [ ] FAIL  [X] SKIP
  - **Notes**: I am using cached example

- **S03** — Runtime log indicates threshold path (optional inspection)
  1. Run a search after refresh
  2. Inspect `extension/logs/runtime.log`
  - **Expected**:
    - No errors
    - If debug logging is enabled in your environment, you may see either index skip/build messages depending on task count
  - **Result**: [ ] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:
