# Manual Test Plan — v1.2.0 Dev Tools UI Tidy

**Date**: 2026-02-07  
**Scope**: Validate dev-tools visibility toggle and 30-per-run dummy completion behavior.

## Preconditions

- Restart Ulauncher in verbose mode:
  - `pkill ulauncher && ulauncher -v`
- Extension enabled
- Morgen API key configured

## Tests

- **DT01** — Dummy completion closes at most 30 per run
  1. Ensure >30 open dummy tasks exist (`#dev Testing ` prefix)
  2. Type: `mg dev dummy-tasks`
  3. Press Enter on `Mark dummy tasks complete`
  - **Expected**:
    - Summary shows `Closed` count
    - `Closed` is `<= 30`
  - **Result**: [ ] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **DT02** — Re-run closes additional batches
  1. Run `Mark dummy tasks complete` repeatedly
  - **Expected**:
    - Each run closes up to 30 more matching tasks
    - Optional warning appears when more tasks may remain
  - **Result**: [ ] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **DT03** — Toggle off hides dev tools
  1. In extension preferences set `Dev Tools Enabled (1/0)` to `0`
  2. Type: `mg dev dummy-tasks`
  - **Expected**:
    - No dev action list
    - Message indicates dev tools are disabled
  - **Result**: [ ] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **DT04** — Toggle on restores dev tools
  1. Set `Dev Tools Enabled (1/0)` to `1`
  2. Type: `mg dev dummy-tasks`
  - **Expected**:
    - Dev tools menu appears (create 10/50/90 + mark complete)
  - **Result**: [ ] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **DT05** — Invalid toggle value falls back to enabled
  1. Set `Dev Tools Enabled (1/0)` to `abc`
  2. Type: `mg dev dummy-tasks`
  - **Expected**:
    - Dev tools menu appears (safe fallback to enabled)
  - **Result**: [ ] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:
