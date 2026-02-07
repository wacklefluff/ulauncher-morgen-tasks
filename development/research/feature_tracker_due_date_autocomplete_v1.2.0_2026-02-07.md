# Feature Tracker - Due-Date Autocomplete (v1.2.0)

**Created**: 2026-02-07  
**Owner**: AI agent + user  
**Status**: In Progress (follow-up enhancements in progress)  
**Primary Strategy**: Approach 1 (actionable suggestions) with code seams for future Approach 2 parser-state model.

## Objective

Add due-date autocomplete guidance in create flow (`mg new`, `mg add`, quick-create keyword) using suggestion items, while keeping architecture ready for future parser-state refactor and possible in-place completion exploration later.

## Scope

### In Scope (v1.2.0)

- Show due suggestions for partial due tokens (`@`, `@to`, `@next-...`) in create flow.
- Allow Enter on suggestion to create task using selected due value.
- Preserve existing title/priority parsing behavior.
- Improve partial due UX so incomplete due typing is guided, not blocked.

### Out of Scope (deferred)

- True in-place query text completion.
- Tab key interception/rewrite behavior.
- Full parser-state refactor across create flow.

## Subtasks

- [x] `DA-01` Define due suggestion catalog and ordering
- [x] `DA-02` Implement due context detection helper for create input
- [x] `DA-03` Implement fragment matcher for suggestions
- [x] `DA-04` Render due suggestion items in create flow UI
- [x] `DA-05` Wire suggestion Enter actions to `create_task` payload
- [x] `DA-06` Adjust partial due behavior (`@`, `@to`) to show guidance instead of only hard error
- [x] `DA-07` Create manual test plan file with `DA01-DA05`
- [x] `DA-08` Run/record manual test outcomes (PASS/FAIL)
- [x] `DA-09` Update docs (`extension/README.md`)
- [x] `DA-10` Update release tracking (`CHANGELOG.md`, `TODO.md`, `extension/logs/dev_log.md`)
- [x] `DA-11` Add `next-month` due suggestion support
- [x] `DA-12` Add `due:` filter autocomplete suggestions in search flow
- [ ] `DA-13` Run/record follow-up manual outcomes (`DA06`, `DA07`)

## Progress Log

- 2026-02-07: Feature tracker created. Strategy confirmed:
  - Prioritize speed and reliable v1.2.0 delivery.
  - Keep implementation shape compatible with future parser-state migration.
  - Defer Tab/in-place completion pending feasibility.
- 2026-02-07: Implemented due suggestion flow in `extension/main.py`:
  - Added due suggestion catalog + fragment matcher.
  - Added active due-fragment detection helper.
  - Added actionable "Use due @..." create items for partial due input.
  - Added manual test plan file:
    - `development/research/test_plan_v1.2.0_due_autocomplete_2026-02-07.md`
  - Automated checks:
    - `python -m py_compile extension/main.py`: PASS
    - `nix-shell --run "pytest -q"`: PASS (42 tests)
- 2026-02-07: Manual verification completed:
  - `DA01` PASS
  - `DA02` PASS
  - `DA03` PASS
  - `DA04` PASS
  - `DA05` PASS
  - Note captured from DA01: consider adding explicit "next month" due suggestion in a future iteration.
- 2026-02-07: Follow-up enhancement implemented:
  - Added `next-month` support for due parsing/autocomplete.
  - Added due-filter autocomplete suggestions for partial `due` / `due:<fragment>` search input.
  - Added follow-up manual tests in:
    - `development/research/test_plan_v1.2.0_due_autocomplete_2026-02-07.md` (`DA06`, `DA07`)

## Design Notes

- Keep suggestion logic isolated in helper functions to avoid deep coupling in `_build_create_flow_items`.
- Keep parser contract backward-compatible where possible; avoid broad refactor in v1.2.0.
- Deterministic suggestion order should favor most common inputs (`today`, `tomorrow`) first.

## Risk Checklist

- [x] No regression in existing create behavior without `@` token
- [x] No regression in quick-create keyword flow
- [x] No regression in non-create commands
- [x] Due values sent to API remain exactly `YYYY-MM-DDTHH:mm:ss`

## Validation Map

- `DA01`: `mg new Task @` shows due suggestions
- `DA02`: `mg new Task @to` narrows suggestions
- `DA03`: Enter on suggestion creates task with expected due
- `DA04`: Works for quick-create keyword too
- `DA05`: Invalid complete token still returns clear error
