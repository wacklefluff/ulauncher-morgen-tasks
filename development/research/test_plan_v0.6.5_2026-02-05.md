# Test Plan (v0.6.5) — Log Access on Welcome/Error Screens

**Date**: 2026-02-05  
**Version under test**: v0.6.5  
**Goal**: Ensure “Open runtime log” / “Copy log path” appear even on the welcome and fallback error screens.

Report failures by **test ID** (e.g. `W03`).

---

## Setup

- **W01** — Restart Ulauncher: `pkill ulauncher && ulauncher -v`.

---

## Welcome Screen (Missing API Key)

- **W02** — Temporarily clear the API key in extension preferences.
- **W03** — Run `mg`.
  - Expected: welcome screen includes “Open runtime log” and/or “Copy log path” items.
- **W04** — Select “Copy log path” and paste somewhere.
  - Expected: path points to `.../extension/logs/runtime.log`.

---

## Create Screen (Missing API Key)

- **W05** — With API key still empty, run `mg new Missing key test`.
  - Expected: error screen includes “Open runtime log” / “Copy log path”.

