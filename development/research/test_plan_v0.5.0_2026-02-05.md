# Test Plan (v0.5.0) — Disk-Persistent Cache

**Date**: 2026-02-05  
**Version under test**: v0.5.0 (Phase 5 started)  
**Goal**: Confirm the task cache persists across Ulauncher restarts and is invalidated appropriately.

Report failures by **test ID** (e.g. `C07`).

---

## Setup

- **C01** — Restart Ulauncher in verbose mode: `pkill ulauncher && ulauncher -v`.
- **C02** — Ensure API key is set and tasks load via `mg`.

---

## Baseline Cache Behavior

- **C03** — Run `mg` twice within cache TTL.
  - Expected: second run shows cached status (e.g. `Cache: cached …`).

---

## Disk Persistence

- **C04** — Warm the cache: run `mg` once and confirm tasks show.
  - Expected: tasks listed successfully.
- **C05** — Restart Ulauncher (`pkill ulauncher && ulauncher -v`) and immediately run `mg`.
  - Expected: tasks list appears quickly and shows cached status (loaded from disk).

---

## Invalidation

- **C06** — Run `mg refresh` (or `mg !`).
  - Expected: cache is invalidated, tasks are fetched again, header shows refreshed/fresh status.
- **C07** — Restart Ulauncher and run `mg` again.
  - Expected: cached status reflects the new cache; no stale data reappears.

---

## Create-Task Integration

- **C08** — Create a task: `mg new Cache invalidate test`.
  - Expected: “Task created”.
- **C09** — Immediately run `mg Cache invalidate test`.
  - Expected: new task is found without manual refresh (cache invalidated on create).

---

## Optional Failure Modes

- **C10** — If you can simulate a network failure: go offline, restart Ulauncher, run `mg`.
  - Expected: cached tasks still show (loaded from disk), or a clear error if no cache exists.

