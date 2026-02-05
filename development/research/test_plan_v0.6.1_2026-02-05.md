# Test Plan (v0.6.1) — Runtime Log File

**Date**: 2026-02-05  
**Version under test**: v0.6.1  
**Goal**: Verify the extension writes runtime logs to `extension/logs/runtime.log`.

Report failures by **test ID** (e.g. `L04`).

---

## Setup

- **L01** — Restart Ulauncher in verbose mode: `pkill ulauncher && ulauncher -v`.
- **L02** — Clear any old runtime log (optional):
  - `rm -f /home/user/Documents/AI/Morgen-Tasks/extension/logs/runtime.log`

---

## Log File Creation

- **L03** — Trigger the extension: run `mg`.
  - Expected: file exists at `extension/logs/runtime.log`.
- **L04** — Open the file and confirm it contains at least one line mentioning file logging enabled.
  - Expected: a line like `File logging enabled: .../extension/logs/runtime.log`.

---

## Log Content (Smoke)

- **L05** — Run `mg help` and then check `runtime.log`.
  - Expected: at least one log line with `Keyword triggered with query: 'help'` (or similar).
- **L06** — Run `mg refresh` and then check `runtime.log`.
  - Expected: logs indicating cache invalidation and API fetch attempt.
- **L07** — Run `mg new Runtime log test`.
  - Expected: logs for create flow and task creation (or a clear error if API rejects).

---

## Rotation (Optional)

- **L08** — Fill the log close to 1MB using the helper script, then trigger one more log line:
  1) Run: `python development/tools/fill_runtime_log.py --target-kib 990 --truncate`  
  2) Trigger the extension once (e.g. run `mg`) to write a new log entry.  
  - Expected: rotated files appear (e.g. `extension/logs/runtime.log.1`) and the extension still works.
