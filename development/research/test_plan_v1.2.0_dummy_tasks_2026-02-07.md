# Manual Test Plan — v1.2.0 Dummy Task Seeding

**Date**: 2026-02-07  
**Scope**: Validate bulk creation of real Morgen test tasks via both CLI script and Ulauncher command.

## Preconditions

- Extension enabled with valid API key
- Restart Ulauncher in verbose mode:
  - `pkill ulauncher && ulauncher -v`
- Optional: clear existing dummy tasks in Morgen first

## Tests

- **DD01** — Script dry-run preview
  1. Run: `python development/tools/create_dummy_morgen_tasks.py --dry-run --count 90`
  - **Expected**: Prints preview lines and exits without creating tasks.
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: Dry-run preview printed payload summaries with no writes.

- **DD02** — Script creates 90 tasks with required prefix
  1. Run: `python development/tools/create_dummy_morgen_tasks.py --count 90 --prefix "#dev Testing "`
  2. Refresh in extension: `mg refresh`
  3. Search: `mg #dev Testing`
  - **Expected**:
    - Script summary shows mostly/all created tasks
    - Search returns many tasks with titles starting `#dev Testing `
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: Tasks created and visible under `mg #dev Testing`.

- **DD03** — Ulauncher command creates dummy tasks
  1. Type: `mg dev dummy-tasks`
  2. Press Enter on `Dev: Create 90 dummy tasks in Morgen`
  3. Run: `mg refresh`
  4. Search: `mg #dev Testing`
  - **Expected**:
    - Completion summary shows created/failed counts
    - Added tasks are visible after refresh
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: Completion summary shown; tasks visible after refresh.

- **DD04** — Seeded data has variety (priority/due)
  1. Search seeded tasks: `mg #dev Testing`
  2. Inspect multiple results/subtitles
  - **Expected**:
    - Mix of priorities appears (e.g., high/medium/low/normal markers)
    - Mix of due states appears (future/overdue/no due)
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: Priority and due-state variety confirmed.

- **DD05** — Missing API key path is graceful
  1. Temporarily remove API key in extension preferences
  2. Type: `mg dev dummy-tasks`
  3. Press Enter on create item
  - **Expected**:
    - No crash
    - Clear missing-API-key error shown
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: Missing-key path stayed stable and showed expected guidance.

- **DD06** — Ulauncher command marks dummy tasks as complete
  1. Ensure at least one open dummy task exists (`mg #dev Testing`)
  2. Type: `mg dev dummy-tasks`
  3. Press Enter on `Mark dummy tasks complete`
  4. Run: `mg refresh`
  5. Search: `mg #dev Testing`
  - **Expected**:
    - Completion summary shows `Closed` count
    - Matching dummy tasks are reduced/removed from active list
    - If many tasks exist, optional warning may appear about possible remaining tasks due to 100-task batch limit
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: Complete action reduced/cleared matching open dummy tasks.
