# Dev Tools UI Tidy Plan — v1.2.0

**Date**: 2026-02-07  
**Scope**: Improve dev-tools UX under `mg dev dummy-tasks`.

## Requested Changes

1. Bulk completion should process **30 dummy tasks per run** (not 100).
2. Add extension preference toggle for dev tools visibility:
   - `1` = show dev tools (default)
   - `0` = hide dev tools

## Implementation Plan

### P1 — Bulk Complete Batch Size (30)

- Update dummy-complete flow in `extension/main.py`:
  - Introduce constant for completion batch cap: `30`.
  - In `complete_dummy_tasks`, close at most 30 matching tasks per run.
  - Keep current summary item (`Closed`, `Failed`) and warning for possible remaining tasks.
- Keep API list fetch limit unchanged (`100`) for discovery, but stop closes at 30.

**Acceptance Criteria**
- Running `mg dev dummy-tasks` -> `Mark dummy tasks complete` closes no more than 30 tasks in one run.
- Summary text clearly reflects count closed in that run.
- If more tasks remain, warning hints to run again.

### P2 — Dev Tools Toggle Preference

- Update `extension/manifest.json`:
  - Add preference (string) `dev_tools_enabled` default `"1"`.
  - Label: "Dev Tools Enabled (1/0)".
- Update `extension/main.py`:
  - Add helper to parse toggle safely (`"1"` enabled, `"0"` disabled; invalid -> enabled).
  - In query flow, hide `mg dev dummy-tasks` when disabled.
  - If user types `mg dev dummy-tasks` while disabled, show a non-destructive message:
    - "Dev tools are disabled in extension settings."

**Acceptance Criteria**
- Default fresh install shows dev tools.
- Setting toggle to `0` hides/dev-blocks the dev command.
- Setting toggle back to `1` immediately restores command availability.

## Manual Test Plan to Add (next step)

- Create `development/research/test_plan_v1.2.0_dev_tools_ui_2026-02-07.md` with:
  - `DT01` Bulk-complete closes max 30
  - `DT02` Re-running closes additional dummy tasks in 30-task chunks
  - `DT03` Toggle `0` disables dev command
  - `DT04` Toggle `1` re-enables dev command
  - `DT05` Invalid toggle value falls back to enabled

## Risks / Notes

- Because `tasks/list` is capped at 100, "mark all" remains best-effort and iterative.
- The toggle must be explicit in help/docs so users know why command is hidden.
