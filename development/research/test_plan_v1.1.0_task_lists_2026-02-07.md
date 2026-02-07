# Manual Test Plan — v1.1.0 Task Lists

**Date**: 2026-02-07  
**Scope**: Container browsing/filtering and payload-shape verification for `taskListId` and `integrationId`.

## Preconditions

- Restart Ulauncher in verbose mode:
  - `pkill ulauncher && ulauncher -v`
- Extension enabled
- Morgen API key set
- Run `mg !` once before starting tests (refresh cache from API)

## Suggested Run Order

1. Run **L11** first to see what payload fields are present.
2. Run view tests (**L01-L05**).
3. Run filtering tests (**L06-L09**).
4. Run fallback checks (**L10**, and **L12** if needed).

## Tests

### Payload Inspection

- **L11** — Inspect cached payload field shape via debug dump
  1. Type: `mg debug`
  2. Press Enter on **Dump cached task fields**
  3. Check `extension/logs/runtime.log`
  - **Expected**: Log includes:
    - `DEBUG cached task list-like keys: ...`
    - `DEBUG container maps sizes: lists=... projects=... spaces=...`
  - **Expected for your account (current hypothesis)**:
    - list-like keys include `taskListId`
    - container maps may still be empty (`lists=0 projects=0 spaces=0`)
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: I would like to also dump taskListId and integrationId avaialable that way I can diagnose the full names of the outputs

### Lists/Container Views

- **L01** — `mg lists` shows grouped containers
  1. Type: `mg lists`
  - **Expected**: Shows “Morgen Task Lists” and container entries grouped by detected container id/name.
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: expect the taskListId Inbox, the rest shows like this `6e7c93f8-e0fe-45ed-8...098cbb@morgen.so (3)` this looks like the account id

- **L02** — Enter on a container opens tasks for that container
  1. Type: `mg lists`
  2. Press Enter on any container item
  - **Expected**: Shows `Morgen Tasks — <container> (...)` with matching tasks.
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **L03** — `mg list` shows only list-kind containers
  1. Type: `mg list`
  - **Expected**: Shows “Morgen Lists” and only list-kind entries.
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **L04** — `mg project` shows project-kind containers
  1. Type: `mg project`
  - **Expected**: Shows “Morgen Projects”, or “No project metadata found” if unavailable.
  - **Result**: [ ] PASS  [X] FAIL  [ ] SKIP
  - **Notes**: i think this variable is not visible check morgen documentaion. if not present remove it

- **L05** — `mg space` shows space-kind containers
  1. Type: `mg space`
  - **Expected**: Shows “Morgen Spaces”, or “No space metadata found” if unavailable.
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: does this variable exist?

### Filtering Commands

- **L06** — `mg in <container>` filters tasks
  1. Type: `mg in <known-container-name-or-id>`
  - **Expected**: Shows only matching tasks (kind-agnostic).
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: it is case sensitive, worked `inbox` but not `Inbox`. it would be nice for the future to add a easy completion
      - FIXED

- **L07** — `mg project <name>` filters project tasks
  1. Type: `mg project <known-project-name>`
  - **Expected**: Shows only matching project tasks, or a clear unavailable/no-match message.
  - **Result**: [ ] PASS  [X] FAIL  [ ] SKIP
  - **Notes**: i think this variable is not visible check morgen documentaion. if not present remove it

- **L08** — `mg space <name>` filters space tasks
  1. Type: `mg space <known-space-name>`
  - **Expected**: Shows only matching space tasks, or a clear unavailable/no-match message.
  - **Result**: [ ] PASS  [X] FAIL  [ ] SKIP
  - **Notes**: i think this variable is not visible check morgen documentaion. if not present remove it

- **L09** — `mg list <name> <query>` filters within list-kind container
  1. Type: `mg list <known-list-name-or-id> <query>`
  - **Expected**: Shows matching tasks inside that list container.
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

### Fallback / Error Handling

- **L10** — Graceful fallback message when metadata is unavailable
  1. Type: `mg project` (or `mg space`) on an account with no such metadata
  - **Expected**: No crash; shows “No ... metadata found” with guidance.
  - **PASS Criteria**: Mark PASS when this message appears and the extension stays responsive, even if you do not have any projects/spaces configured in Morgen.
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: i think this is the case for all, but I also think I do not have any project or space setup

- **L12** — `integrationId` fallback grouping (only if no explicit list field is available)
  1. Confirm via **L11** whether explicit list keys are absent.
  2. Type: `mg lists`
  - **Expected**: Tasks still group into containers using `integrationId` fallback ids.
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:



Log Cache Dump
```
2026-02-07 12:17:30,406 INFO __main__: DEBUG cached task keys: ['@type', 'created', 'due', 'estimatedDuration', 'id', 'integrationId', 'position', 'priority', 'progress', 'tags', 'taskListId', 'title', 'updated']
2026-02-07 12:17:30,406 INFO __main__: DEBUG cached task list-like keys: ['taskListId']
2026-02-07 12:17:30,407 INFO __main__: DEBUG sample taskListId values: ['a8557182-960b-49d8-ba6e-4f1aeb3f07a0@morgen.so', 'inbox', '6e7c93f8-e0fe-45ed-824b-ba94bb098cbb@morgen.so']
2026-02-07 12:17:30,408 INFO __main__: DEBUG sample integrationId values: ['morgen']
2026-02-07 12:17:30,409 INFO __main__: DEBUG cached data keys: ['labelDefs', 'spaces', 'tasks']
2026-02-07 12:17:30,409 INFO __main__: DEBUG container maps sizes: lists=0 projects=0 spaces=0
```