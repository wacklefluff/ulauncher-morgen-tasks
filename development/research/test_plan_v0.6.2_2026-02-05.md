# Test Plan (v0.6.2) — One‑Shot Refresh

**Date**: 2026-02-05  
**Version under test**: v0.6.2  
**Goal**: Ensure `mg refresh` / `mg !` only refresh once, and typing afterwards does not repeatedly hit the API.

Report failures by **test ID** (e.g. `R05`).

---

## Setup

- **R01** — Restart Ulauncher: `pkill ulauncher && ulauncher -v`.
- **R02** — Ensure API key is set and `mg` lists tasks.

---

## One‑Shot `mg refresh`

- **R03** — Type `mg refresh` and pause (don’t type anything else for ~1s).
  - Expected: refresh occurs once (header shows refreshed/fresh).
- **R04** — Continue typing immediately after: `mg refresh test` (keep typing a few extra letters).
  - Expected: it behaves like a normal search for `test` and shows a notice that refresh is one-shot.
  - Expected: it does **not** keep refreshing on every keystroke.

---

## One‑Shot `mg !`

- **R05** — Type `mg !` and pause (~1s).
  - Expected: refresh occurs once.
- **R06** — Continue typing: `mg ! test` (keep typing a few extra letters).
  - Expected: normal search for `test` + one-shot notice.
  - Expected: it does **not** refresh repeatedly.

---

## Regression Smoke

- **R07** — Verify search still works: `mg <query>` returns filtered results.
- **R08** — Verify help still works: `mg help` shows help view; `mg help regression` performs search.

