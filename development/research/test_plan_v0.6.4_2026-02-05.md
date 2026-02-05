# Test Plan (v0.6.4) — Open/Copy Runtime Logs

**Date**: 2026-02-05  
**Version under test**: v0.6.4  
**Goal**: Ensure users can quickly access `extension/logs/runtime.log` from the UI.

Report failures by **test ID** (e.g. `O03`).

---

## Setup

- **O01** — Restart Ulauncher: `pkill ulauncher && ulauncher -v`.

---

## Help Screen Access

- **O02** — Run `mg help`.
  - Expected: help view includes items:
    - “Open runtime log” (if `OpenAction` is supported)
    - “Copy log path” (if `CopyToClipboardAction` is supported)
- **O03** — Select “Open runtime log”.
  - Expected: the log file opens in your default app/editor.
- **O04** — Select “Copy log path” and paste somewhere.
  - Expected: pasted path points to `.../extension/logs/runtime.log`.

---

## Error Screen Access (Optional / Requires Simulation)

- **O05** — Trigger a known error screen (e.g. temporarily remove API key and run `mg`).
  - Expected: error/welcome screen includes “Open runtime log” / “Copy log path” items.

