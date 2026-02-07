# Feature Tracker - Task Filters (Priority + Due) (v1.2.0)

**Created**: 2026-02-07  
**Owner**: AI agent + user  
**Status**: Completed (manual tests passed)

## Objective

Add query-time filtering for tasks by priority and due status/date windows, while preserving existing free-text search behavior.

## Scope

### In Scope

- Query tokens for priority filters:
  - `p:<value>` or `priority:<value>`
  - Values: `high`, `medium`, `low`, `normal`, or numeric `1`-`9`
- Query tokens for due filters:
  - `due:<value>`
  - Values: `today`, `tomorrow`, `overdue`, `future`, `week`, `nodue`
- Combine filters with normal text search.

### Out of Scope

- UI dropdown for filters.
- Filter presets in preferences.
- Advanced relative date grammar (e.g. `due:next-month`) in this iteration.

## Subtasks

- [x] `TF-01` Implement filter token parser in a dedicated module
- [x] `TF-02` Implement task matching logic for priority filter values
- [x] `TF-03` Implement task matching logic for due filter values
- [x] `TF-04` Wire parser/filtering into `extension/main.py` search flow
- [x] `TF-05` Add unit tests for parser and matching logic
- [x] `TF-06` Create manual test plan (`TF01-TF06`)
- [x] `TF-07` Update docs (`extension/README.md`)
- [x] `TF-08` Update tracking (`CHANGELOG.md`, `TODO.md`, `extension/logs/dev_log.md`)
- [x] `TF-09` Run/record manual outcomes

## Validation Map

- `TF01`: `mg due:today` only shows tasks due today
- `TF02`: `mg p:high` only shows high-priority tasks
- `TF03`: Combined filters work (`mg due:today p:high`)
- `TF04`: Text query + filters both apply (`mg report due:week`)
- `TF05`: Unknown filter values are ignored as plain text (no crash)
- `TF06`: Existing search without filters remains unchanged

## Progress Log

- 2026-02-07: Implemented filter engine and integration:
  - Added `extension/src/task_filters.py` (filter token parsing + matching).
  - Wired filter parsing into `extension/main.py` query flow.
  - Applied filters in normal API and cached-fallback paths.
  - Added help examples for due/priority filters.
  - Added tests: `extension/tests/test_task_filters.py`.
  - Added manual test plan:
    - `development/research/test_plan_v1.2.0_task_filters_2026-02-07.md`
  - Automated checks:
    - `python -m py_compile extension/main.py extension/src/task_filters.py`: PASS
    - `nix-shell --run "pytest -q"`: PASS (50 tests)
- 2026-02-07: Manual verification completed:
  - `TF01` PASS
  - `TF02` PASS
  - `TF03` PASS
  - `TF04` PASS
  - `TF05` PASS
  - `TF06` PASS
  - Follow-up note: consider `!` / `!!` alias support for priority filtering in a future iteration.
