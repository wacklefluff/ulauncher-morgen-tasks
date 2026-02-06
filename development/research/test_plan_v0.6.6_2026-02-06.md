# Test Plan (v0.6.6) — Priority Icons & Overdue Highlighting

**Date**: 2026-02-06
**Version under test**: v0.6.6
**Goal**: Verify improved priority icons, human-readable priority labels, overdue highlighting, and relative due date display.

Report failures by **test ID** (e.g. `P03`).

---

## Setup

- **P01** — Restart Ulauncher:
  ```bash
  pkill ulauncher && ulauncher -v
  ```
- **P02** — Verify API key is configured: run `mg` and confirm tasks load.

---

## Create Test Tasks

Run these commands to create test tasks (press Enter to confirm each):

```
mg new Test High Priority !1
mg new Test Medium Priority !5
mg new Test Low Priority !9
mg new Test Normal Priority
mg new Test Overdue Yesterday @2026-02-05 !1
mg new Test Due Today @today
mg new Test Due Tomorrow @tomorrow !5
mg new Test Due Future @2026-02-10
```

After creating, run `mg !` to refresh the cache.

---

## Priority Icons in Title

Run: `mg` (list all tasks)

Morgen normalizes priorities: High→1, Medium→5, Low→9, Normal→None.

- **P03** — Find "Test High Priority"
  - Expected title: `!! Test High Priority`
- **P04** — Find "Test Medium Priority"
  - Expected title: `! Test Medium Priority`
- **P05** — Find "Test Low Priority"
  - Expected title: `Test Low Priority` (no icon)
- **P06** — Find "Test Normal Priority"
  - Expected title: `Test Normal Priority` (no icon)

---

## Priority Labels in Subtitle

Run: `mg` (list all tasks)

- **P07** — Find "Test High Priority"
  - Expected subtitle contains: `Priority: High`
- **P08** — Find "Test Medium Priority"
  - Expected subtitle contains: `Priority: Medium`
- **P09** — Find "Test Low Priority"
  - Expected subtitle contains: `Priority: Low`
- **P10** — Find "Test Normal Priority"
  - Expected subtitle contains: `Priority: Normal`

---

## Overdue Highlighting

Run: `mg` (list all tasks)

- **O01** — Find "Test Overdue Yesterday"
  - Expected title: `OVERDUE !! Test Overdue Yesterday`
  - Expected subtitle contains: `(overdue!)`
- **O02** — Find "Test Due Future"
  - Expected: No "OVERDUE" prefix, no "(overdue!)" in subtitle
- **O03** — Find "Test Normal Priority" (no due date)
  - Expected subtitle: `Due: No due date`
  - Expected: No "OVERDUE" prefix

---

## Relative Due Dates

Run: `mg` (list all tasks)

- **D01** — Find "Test Due Today"
  - Expected subtitle contains: `Due: Today` followed by time
- **D02** — Find "Test Due Tomorrow"
  - Expected subtitle contains: `Due: Tomorrow` followed by time
- **D03** — Find "Test Due Future"
  - Expected subtitle contains: `Due: 2026-02-10` (full date format)

---

## Combination Tests

Run: `mg` (list all tasks)

- **C01** — Find "Test Overdue Yesterday" (overdue + high priority)
  - Expected title: `OVERDUE !! Test Overdue Yesterday`
  - Expected subtitle: `Due: ... (overdue!) | Priority: High`
- **C02** — Find "Test Due Tomorrow" (tomorrow + medium priority)
  - Expected title: `! Test Due Tomorrow`
  - Expected subtitle: `Due: Tomorrow ... | Priority: Medium`

---

## Regression Tests

- **R01** — Run `mg` with no query
  - Expected: All tasks display correctly with new formatting
- **R02** — Run `mg Test`
  - Expected: Filtered tasks display with correct formatting
- **R03** — Run `mg !`
  - Expected: "Refreshing..." then tasks display correctly
- **R04** — Run `mg help`
  - Expected: Help screen displays (unaffected by formatter changes)

---

## Cleanup

After testing, delete the test tasks from Morgen app/web, then run `mg !` to refresh.

---

## Results

| Test ID | Status | Notes |
|---------|--------|-------|
| P01     |        |       |
| P02     |        |       |
| P03     |        |       |
| P04     |        |       |
| P05     |        |       |
| P06     |        |       |
| P07     |        |       |
| P08     |        |       |
| P09     |        |       |
| P10     |        |       |
| O01     |        |       |
| O02     |        |       |
| O03     |        |       |
| D01     |        |       |
| D02     |        |       |
| D03     |        |       |
| C01     |        |       |
| C02     |        |       |
| R01     |        |       |
| R02     |        |       |
| R03     |        |       |
| R04     |        |       |
