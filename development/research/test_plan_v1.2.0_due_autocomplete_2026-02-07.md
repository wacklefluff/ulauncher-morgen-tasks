# Manual Test Plan — v1.2.0 Due-Date Autocomplete

**Date**: 2026-02-07  
**Scope**: Validate due-date suggestions in create flow for partial `@...` input.

## Preconditions

- Restart Ulauncher in verbose mode:
  - `pkill ulauncher && ulauncher -v`
- Extension enabled
- Morgen API key configured

## Tests

- **DA01** — Bare `@` shows due suggestions
  1. Type: `mg new Planning @`
  - **Expected**:
    - A due-suggestion section appears
    - Suggestions include common values like `@today` and `@tomorrow`
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: Also add next month

- **DA02** — Partial token narrows suggestions
  1. Type: `mg new Planning @to`
  - **Expected**:
    - Suggestions are narrowed (for example `@today`, `@tomorrow`)
    - No crash or unexpected fallback
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **DA03** — Enter on suggestion creates task with due date
  1. Type: `mg new Planning @to`
  2. Press Enter on one suggestion item (e.g. `Use due @today`)
  3. Run: `mg refresh`
  4. Search for created task title
  - **Expected**:
    - Task is created
    - Due date is set and displayed in subtitle
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **DA04** — Works with quick-create keyword too
  1. Type: `<new task keyword> Planning @to` (default keyword is `mgn`)
  2. Press Enter on a due suggestion
  - **Expected**:
    - Same due-suggestion behavior as `mg new ...`
    - Task creation works with selected due
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **DA05** — Invalid full due token still returns clear error
  1. Type: `mg new Planning @notadate`
  - **Expected**:
    - Create flow shows clear invalid-date message
    - No task is created
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **DA06** — `@next-month` appears and creates correctly
  1. Type: `mg new Planning @next-`
  2. Confirm `@next-month` appears in suggestions
  3. Press Enter on `Use due @next-month`
  - **Expected**:
    - Suggestion appears in the autocomplete list
    - Created task has due date in next calendar month
  - **Result**: [ ] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **DA07** — `due:` filter suggestions appear in search flow
  1. Type: `mg due`
  2. Type: `mg due:to`
  - **Expected**:
    - A due-filter suggestion section appears
    - Suggested values appear (for example `due:today`, `due:tomorrow`)
    - No crash or blocking behavior
  - **Result**: [ ] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:
