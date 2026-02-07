# Development Log

## 2026-02-07 (Session 39)

**Goals**:
- Add temporary manual list name-map settings (5 slots)

**Accomplished**:
- Added manual mapping preferences in `extension/manifest.json`:
  - `manual_list_name_1..5`
  - `manual_list_id_1..5`
- Implemented manual map ingestion and merge:
  - `extension/src/task_lists.py`: `build_manual_list_name_maps()`
  - `extension/main.py`: merges cache/API maps with manual maps for runtime resolution
  - Manual list mappings override cache/API names for matching ids
- Updated tests:
  - `extension/tests/test_task_lists.py` (manual map builder coverage)
- Updated docs/tracking:
  - `extension/README.md`
  - `CHANGELOG.md`
  - `TODO.md` (temporary workaround noted under v1.2.0 roadmap)

**Automated Tests**:
- `python -m py_compile extension/main.py extension/src/task_lists.py extension/tests/test_task_lists.py`: PASS
- `nix-shell --run "pytest -q"`: PASS (57 tests)

---

## 2026-02-07 (Session 38)

**Goals**:
- Replace overdue title prefix text with warning symbol

**Accomplished**:
- Updated task display formatting:
  - `extension/src/formatter.py`
  - Overdue title prefix changed from `OVERDUE` to `⚠`
- Updated tests/docs:
  - `extension/tests/test_formatter.py`
  - `extension/README.md`
  - `CHANGELOG.md`

**Automated Tests**:
- `python -m py_compile extension/src/formatter.py extension/tests/test_formatter.py`: PASS
- `nix-shell --run "pytest -q"`: PASS (56 tests)

---

## 2026-02-07 (Session 37)

**Goals**:
- Add `--` low-priority shortcut in create flow

**Accomplished**:
- Updated create parser in `extension/main.py`:
  - `--` token now maps to low priority (`9`)
  - Works alongside existing priority tokens (`!`, `!!`, `!1-!9`, named `!high/!medium/!low`)
- Updated docs/tracking:
  - `extension/README.md`
  - `CHANGELOG.md`

**Manual Tests**:
- LP01 PENDING (`mg new <title> --` creates low-priority task)

**Automated Tests**:
- `python -m py_compile extension/main.py`: PASS
- `nix-shell --run "pytest -q"`: PASS (56 tests)

---

## 2026-02-07 (Session 36)

**Goals**:
- Verify and implement query-rewrite behavior for `due:` autocomplete suggestions

**Accomplished**:
- Confirmed Ulauncher exposes query-rewrite action for extension items:
  - `SetUserQueryAction` available in installed Ulauncher API (v5.15.7 path inspection).
- Implemented `due:` suggestion Enter behavior to rewrite query input:
  - `extension/main.py`
  - Suggestion items now use `SetUserQueryAction` when available (fallback to `HideWindowAction`).
  - Rewritten query preserves existing argument text and replaces active `due`/`due:<fragment>` token.
- Added helper for query token rewrite:
  - `extension/src/task_filters.py` (`rewrite_due_filter_query`)
- Added unit coverage:
  - `extension/tests/test_task_filters.py` (rewrite helper tests)
- Updated manual test plan:
  - `development/research/test_plan_v1.2.0_due_autocomplete_2026-02-07.md` (added `DA08`)

**Manual Tests**:
- DA08 PASS

**Automated Tests**:
- `python -m py_compile extension/main.py extension/src/task_filters.py extension/tests/test_task_filters.py`: PASS
- `nix-shell --run "pytest -q"`: PASS (56 tests)

---

## 2026-02-07 (Session 35)

**Goals**:
- Commit completed v1.2.0 work
- Add `next-month` due autocomplete support
- Add autocomplete suggestions for `due:` filter typing

**Accomplished**:
- Committed completed v1.2.0 due-autocomplete + task-filter work:
  - Commit: `fbfd3f7`
  - Message: `feat: add due autocomplete and task filters`
- Added `next-month` support in due parsing/autocomplete:
  - `extension/src/date_parser.py`
  - `extension/main.py` due suggestion catalog/help examples
- Added `due:` filter autocomplete suggestions in search flow:
  - `extension/src/task_filters.py` (fragment extraction + suggestion helper)
  - `extension/main.py` suggestion section for partial `due` / `due:<fragment>` input
- Extended due filter support:
  - Added `due:next-month` matching in `extension/src/task_filters.py`
- Added/updated tests:
  - `extension/tests/test_date_parser.py` (next-month parse test)
  - `extension/tests/test_task_filters.py` (next-month + due-filter autocomplete helper coverage)
- Updated docs/tracking:
  - `development/research/test_plan_v1.2.0_due_autocomplete_2026-02-07.md` (added `DA06`, `DA07`)
  - `development/research/feature_tracker_due_date_autocomplete_v1.2.0_2026-02-07.md`
  - `extension/README.md`
  - `CHANGELOG.md`
  - `TODO.md`

**Manual Tests**:
- DA06 PENDING
- DA07 PENDING

**Automated Tests**:
- `python -m py_compile extension/main.py extension/src/date_parser.py extension/src/task_filters.py extension/tests/test_date_parser.py extension/tests/test_task_filters.py`: PASS
- `nix-shell --run "pytest -q"`: PASS (55 tests)

---

## 2026-02-07 (Session 34)

**Goals**:
- Implement task filtering by priority/due date for v1.2.0

**Accomplished**:
- Added filter parsing/matching module:
  - `extension/src/task_filters.py`
  - Supports:
    - `p:<value>` / `priority:<value>` (`high`, `medium`, `low`, `normal`, `1-9`)
    - `due:<value>` (`today`, `tomorrow`, `overdue`, `future`, `week`, `nodue`)
- Integrated filter flow in `extension/main.py`:
  - Parses filter tokens from query
  - Applies filters plus normal text search together
  - Applies same filtering in cached fallback mode (network/rate-limit errors)
  - Added filter examples to `mg help`
- Added unit tests:
  - `extension/tests/test_task_filters.py`
- Added manual test plan:
  - `development/research/test_plan_v1.2.0_task_filters_2026-02-07.md` (`TF01`-`TF06`)
- Added feature tracker:
  - `development/research/feature_tracker_task_filters_v1.2.0_2026-02-07.md`
- Updated docs/tracking:
  - `extension/README.md`
  - `CHANGELOG.md`
  - `TODO.md` (task filter roadmap item marked complete)

**Manual Tests**:
- TF01 PASS
- TF02 PASS
- TF03 PASS
- TF04 PASS
- TF05 PASS
- TF06 PASS
  - Note: consider adding `!` / `!!` aliases for priority filtering in a future enhancement.

**Automated Tests**:
- `python -m py_compile extension/main.py extension/src/task_filters.py`: PASS
- `nix-shell --run "pytest -q"`: PASS (50 tests)

---

## 2026-02-07 (Session 33)

**Goals**:
- Implement due-date autocomplete suggestions in create flow for v1.2.0
- Keep implementation structured for future parser-state refactor path

**Accomplished**:
- Implemented due-autocomplete flow in `extension/main.py`:
  - Added due suggestion catalog and deterministic matcher
  - Added helper to detect active due token context
  - Added suggestion rendering for partial due input (`@`, `@to`, etc.)
  - Added actionable suggestion items (`Use due @...`) that create task directly on Enter
  - Updated create parser behavior so partial due input shows guidance instead of only hard errors
- Added tracking and planning artifacts:
  - `development/research/feature_tracker_due_date_autocomplete_v1.2.0_2026-02-07.md`
  - `development/research/due_date_autocomplete_plan_2026-02-07.md`
  - `development/research/test_plan_v1.2.0_due_autocomplete_2026-02-07.md`
  - `development/research/due_date_autocomplete_approach_1_actionable_items_2026-02-07.md`
  - `development/research/due_date_autocomplete_approach_2_parser_state_model_2026-02-07.md`
  - `development/research/due_date_autocomplete_approach_3_tab_fill_concept_2026-02-07.md`
- Updated docs/tracking:
  - `extension/README.md`
  - `CHANGELOG.md`
  - `TODO.md` (due-autocomplete roadmap item marked complete)

**Manual Tests**:
- DA01 PASS
- DA02 PASS
- DA03 PASS
- DA04 PASS
- DA05 PASS
  - Note: consider adding an explicit "next month" suggestion in a follow-up enhancement.

**Automated Tests**:
- `python -m py_compile extension/main.py`: PASS
- `nix-shell --run "pytest -q"`: PASS (42 tests)

---

## 2026-02-07 (Session 32)

**Goals**:
- Complete and record manual v1.2.0 verification
- Refresh roadmap focus after verification pass

**Accomplished**:
- Recorded manual test outcomes as PASS in:
  - `development/research/test_plan_v1.2.0_dummy_tasks_2026-02-07.md` (`DD01`-`DD06`)
  - `development/research/test_plan_v1.2.0_api_limit_notice_2026-02-07.md` (`LIM01`-`LIM03`)
  - `development/research/test_plan_v1.2.0_dev_tools_ui_2026-02-07.md` (`DT01`-`DT05`)
- Updated `TODO.md` Immediate Next Steps to focus on deciding whether to include or defer remaining v1.2.0 roadmap candidates before release.

**Manual Tests**:
- DD01 PASS
- DD02 PASS
- DD03 PASS
- DD04 PASS
- DD05 PASS
- DD06 PASS
- LIM01 PASS
- LIM02 PASS
- LIM03 PASS
- DT01 PASS
- DT02 PASS
- DT03 PASS
- DT04 PASS
- DT05 PASS

**Automated Tests**:
- Not re-run in this logging-only session.

---

## 2026-02-07 (Session 31)

**Goals**:
- Execute dev-tools UI tidy plan (`DEV-03`, `DEV-04`)

**Accomplished**:
- Updated dummy completion behavior in `extension/main.py`:
  - `Mark dummy tasks complete` now closes up to 30 tasks per run
  - Updated completion notice text to explain 30-per-run behavior
- Added dev-tools visibility toggle support:
  - New manifest preference in `extension/manifest.json`:
    - `dev_tools_enabled` (default `"1"`)
  - `mg dev dummy-tasks` now shows:
    - disabled message when toggle is `0`
    - full dev menu when toggle is `1` (or invalid value)
- Updated docs/tracking:
  - `TODO.md` (`DEV-03` and `DEV-04` checked off)
  - `CHANGELOG.md`
  - `extension/README.md`
- Added manual test plan:
  - `development/research/test_plan_v1.2.0_dev_tools_ui_2026-02-07.md` (`DT01`–`DT05`)

**Manual Tests**:
- DT01 PENDING
- DT02 PENDING
- DT03 PENDING
- DT04 PENDING
- DT05 PENDING

**Automated Tests**:
- `python -m py_compile extension/main.py`: PASS
- `nix-shell --run "pytest -q"`: PASS (42 tests)

---

## 2026-02-07 (Session 30)

**Goals**:
- Plan dev-tools UI tidy-up for v1.2.0

**Accomplished**:
- Added implementation plan:
  - `development/research/dev_tools_ui_tidy_plan_2026-02-07.md`
- Updated roadmap in `TODO.md`:
  - Added `DEV-03`: complete dummy tasks in 30-task runs
  - Added `DEV-04`: dev-tools visibility toggle in extension settings (default enabled)
- Updated `Immediate Next Steps` in `TODO.md` to execute this plan next

---

## 2026-02-07 (Session 29)

**Goals**:
- Add a dummy-task bulk-complete option under `mg dev dummy-tasks`

**Accomplished**:
- Updated dev menu in `extension/main.py`:
  - Added `Mark dummy tasks complete` action under `mg dev dummy-tasks`
  - Updated header text to "Dev: Dummy task tools"
- Added new custom action flow: `complete_dummy_tasks`
  - Fetches tasks in repeated 100-task batches
  - Closes tasks whose title starts with `#dev Testing `
  - Stops safely on API/network/rate-limit errors
  - Shows summary with closed/failed counts and a possible-remaining warning when API cap may hide more tasks
- Updated docs/tracking:
  - `extension/README.md`
  - `CHANGELOG.md`
  - `TODO.md`
  - `development/research/test_plan_v1.2.0_dummy_tasks_2026-02-07.md` (added DD06)

**Manual Tests**:
- DD06 PENDING

**Automated Tests**:
- `python -m py_compile extension/main.py`: PASS
- `nix-shell --run "pytest -q"`: PASS (42 tests)

---

## 2026-02-07 (Session 28)

**Goals**:
- Remove search-index optimization and surface API list cap in UI

**Accomplished**:
- Removed search-index code path from:
  - `extension/src/cache.py`
  - `extension/main.py` filtering flow
- Added UI notice when loaded task count is exactly 100:
  - `API list limit reached (100 tasks)`
  - Shown in normal and cached-fallback result flows
- Updated large-dataset test coverage to match non-indexed behavior:
  - `extension/tests/test_perf.py`
- Updated roadmap/release docs:
  - `CHANGELOG.md`
  - `TODO.md` (added **Currently not Possible** section for >100 task fetch limitation)

**Manual Tests**:
- LIM01 PENDING
- LIM02 PENDING
- LIM03 PENDING

**Automated Tests**:
- `python -m py_compile extension/main.py extension/src/cache.py extension/tests/test_perf.py`: PASS
- `nix-shell --run "pytest -q"`: PASS (42 tests)

---

## 2026-02-07 (Session 27)

**Goals**:
- Add multiple batch-size options to `mg dev dummy-tasks`

**Accomplished**:
- Updated `extension/main.py` dev flow UI to provide three explicit actions:
  - Create 10 dummy tasks
  - Create 50 dummy tasks
  - Create 90 dummy tasks
- Updated `extension/README.md` utility command description to reflect 10/50/90 options

**Automated Tests**:
- `python -m py_compile extension/main.py`: PASS
- `nix-shell --run "pytest -q"`: PASS (43 tests)

---

## 2026-02-07 (Session 26)

**Goals**:
- Add real dummy-task seeding for performance/testing workflows

**Accomplished**:
- Added shared dummy-task generator module:
  - `extension/src/dev_dummy_tasks.py`
- Added Ulauncher dev command:
  - `mg dev dummy-tasks` (creates 90 real tasks with `#dev Testing ` prefix)
  - Added confirmation UI and bulk-create action handling in `extension/main.py`
- Added CLI seeding script:
  - `development/tools/create_dummy_morgen_tasks.py`
  - Supports `--count`, `--prefix`, `--api-key`/`MORGEN_API_KEY`, and `--dry-run`
- Added unit tests:
  - `extension/tests/test_dev_dummy_tasks.py`
- Updated docs/tracking:
  - `extension/README.md` command table
  - `CHANGELOG.md` (Unreleased)
  - `TODO.md` roadmap/context
- Added manual test plan:
  - `development/research/test_plan_v1.2.0_dummy_tasks_2026-02-07.md`

**Manual Tests**:
- DD01 PENDING
- DD02 PENDING
- DD03 PENDING
- DD04 PENDING
- DD05 PENDING

**Automated Tests**:
- `nix-shell --run "pytest -q"`: PASS (43 tests)

---

## 2026-02-07 (Session 25)

**Goals**:
- Implement SUG-03 search optimization threshold behavior

**Accomplished**:
- Updated `extension/src/cache.py` to only build the precomputed search index when task count is >= 200
- Added debug logging for threshold skip/build decisions
- Updated `extension/tests/test_perf.py`:
  - Adjusted index-building test to use 250 tasks
  - Added coverage for below-threshold behavior (no index for 100 tasks)
- Added manual test plan for this change:
  - `development/research/test_plan_v1.2.0_sug03_2026-02-07.md`
- Updated release tracking docs:
  - `CHANGELOG.md` (Unreleased)
  - `TODO.md` (SUG-03 marked complete for v1.2.0)

**Manual Tests**:
- S01 PENDING
- S02 PENDING
- S03 PENDING

**Automated Tests**:
- `nix-shell --run "pytest -q"`: PASS (41 tests)

---

## 2026-02-07 (Session 24)

**Goals**:
- Complete documentation protocol housekeeping and end session

**Accomplished**:
- Created dedicated handoff protocol file:
  - `development/protocols/ai_agent_handoff_protocol_2026-02-07.md`
- Updated `AGENTS.md` to point handoff rules to the dedicated protocol file
- Added explicit trigger phrase support in protocol/docs:
  - `handoff session`
- Added protocol pointers in core docs:
  - `README.md`
  - `AGENTS.md`
  - `CLAUDE.md`
- Verified current changes and committed documentation updates

**Notes**:
- Handoff and git-maintenance protocols now both live under `development/protocols/`.

---

## 2026-02-07 (Session 23)

**Goals**:
- Remove "Task Open URL Template" from Ulauncher extension settings

**Accomplished**:
- Removed `task_open_url_template` preference from `extension/manifest.json`
- Updated `extension/main.py` to always open `https://web.morgen.so` on task Enter
- Removed stale docs references in:
  - `extension/README.md`
  - `CHANGELOG.md`
  - `TODO.md`
- Updated normal-mode task Enter behavior to no-op (`HideWindowAction`) while keeping done-mode Enter and Alt+Enter copy behavior

**Automated Tests**:
- `nix-shell --run "pytest -q"`: PASS (40 tests)

---

## 2026-02-07 (Session 22)

**Goals**:
- Add explicit container commands so each API field path can be tested independently (`listId`/`projectId`/`spaceId`)

**Accomplished**:
- Updated list/container UX in `extension/main.py`:
  - Added kind-specific browse commands: `mg list`, `mg project`, `mg space`
  - Added kind-specific filter commands: `mg list <name> [query]`, `mg project <name> [query]`, `mg space <name> [query]`
  - Kept existing commands: `mg lists`/`mg ls` and `mg in <list> [query]`
  - Added container-kind aware labels in headers/subtitles
- Expanded manual test plan:
  - `development/research/test_plan_v1.1.0_task_lists_2026-02-07.md` now includes L01-L11 to validate each container path and debug field-dump checks
- Updated docs/changelog:
  - `extension/README.md` command table
  - `CHANGELOG.md` (Unreleased)
  - `TODO.md` task-list implementation notes
- Added explicit unit coverage for reference-field extraction:
  - `projectId` + optional `projectName`
  - `spaceId` + optional `spaceName`
  - File: `extension/tests/test_task_lists.py`
- Added compatibility for Morgen payloads that use `taskListId`/`taskListName`:
  - `extension/src/task_lists.py` now extracts list refs from `taskListId`
  - Container name maps also ingest `data.taskLists` / `data.tasklists` when present
- Added unit tests for `taskListId` extraction and map-based name resolution
- Added `integrationId` fallback support in list extraction for payloads without explicit list/project/space keys
- Added unit tests validating `integrationId` fallback and precedence rules
- Made container-id matching case-insensitive in list filters and list selection actions
- Enhanced `mg debug` dump to log sample `taskListId` and `integrationId` values
- Clarified manual test L10 pass criteria for accounts without projects/spaces
- Simplified list field support based on real payloads:
  - Removed `listId` / `projectId` / `spaceId` extraction paths
  - Kept `taskListId` / `taskListName` + `integrationId` fallback
  - Updated unit tests accordingly

**Manual Tests**:
- L11 PASS (payload keys include `taskListId`; maps may be empty)
- L01 PASS
- L02 PASS
- L03 PASS
- L04 SKIP (no project metadata available in current account payload)
- L05 PASS
- L06 PASS
- L07 SKIP (no project metadata available in current account payload)
- L08 SKIP (no matching space metadata for filter in current account payload)
- L09 PASS
- L10 PASS (unavailable metadata fallback message verified)
- L12 PASS (`integrationId` fallback grouping confirmed)

**Automated Tests**:
- `nix-shell --run "pytest -q"`: PASS (40 tests)

---

## 2026-02-07 (Session 21)

**Goals**:
- Add task list support (Inbox/Work/etc): list and filter

**Accomplished**:
- Added task list extraction/grouping helpers (`extension/src/task_lists.py`)
- Added `mg lists` / `mg ls` view and `mg in <list> [query]` filtering
- List name now shows in task subtitle when available
- Added debug helper: "Dump cached task fields" in `mg debug`
- Added manual test plan: `development/research/test_plan_v1.1.0_task_lists_2026-02-07.md`

**Manual Tests**:
- L01 PENDING
- L02 PENDING
- L03 PENDING
- L04 PENDING
- L05 PENDING

---

## 2026-02-07 (Session 20)

**Goals**:
- Add an optional shortcut keyword to create new tasks

**Accomplished**:
- Added `mg_new_keyword` manifest preference (default: `mgn`) to trigger quick-create flow
- Updated help screen to show configured keyword(s) and the shortcut example when enabled
- Updated docs and changelog
- Created manual test plan: `development/research/test_plan_v1.1.0_2026-02-07.md`

**Manual Tests**:
- N01 PASS
- N02 PASS
- N03 PASS
- N04 PASS

**Notes**:
- Ulauncher extension preferences don't support clickable "buttons"; runtime log access remains available via `mg debug`.

---

## 2026-02-06 (Session 19)

**Goals**:
- Make opening Morgen the default task action on Enter

**Accomplished**:
- Default task Enter now opens Morgen using the "Task Open URL Template" preference
- Added Alt+Enter copy-task-id action when supported by Ulauncher
- Updated docs and manual test plan (`development/research/test_plan_v1.1.0_2026-02-06.md` O02)
- Removed `{id}` substitution from the open URL (Morgen has no official per-task deep link support)

**Manual Tests**:
- O02 PASS

---

## 2026-02-06 (Session 18)

**Goals**:
- Add `mg d <query>` flow to mark tasks as done (close via API)

**Accomplished**:
- Added `MorgenAPIClient.close_task()` and made `_make_request()` handle empty (204) responses
- Implemented `mg d` / `mg done` mode: lists/searches tasks but Enter marks done
- Extended unit tests for close-task behavior
- Updated manual test plan: `development/research/test_plan_v1.1.0_2026-02-06.md` (D01–D06)

**Manual Tests**:
- D01 PASS
- D02 PASS
- D03 PASS
- D04 PASS
- D05 PASS
- D06 PASS

---

## 2026-02-06 (Session 17)

**Goals**:
- Implement SUG-04: show creation date when no due date is available

**Accomplished**:
- Updated `TaskFormatter.format_subtitle()` to show `Created: YYYY-MM-DD` for tasks without `due`
- Added unit test coverage for the created-date fallback
- Created manual test plan: `development/research/test_plan_v1.1.0_2026-02-06.md`

**Manual Tests**:
- S04-01 PASS
- S04-02 PASS
- S04-03 SKIP (no task missing `created` found)

---

## 2026-02-06 (Session 16)

**Goals**:
- Remove dev-only empty-task simulation toggle

**Accomplished**:
- Removed `dev_empty_tasks` preference from `extension/manifest.json`
- Removed dev-empty bypass logic from `extension/main.py`
- Updated `CHANGELOG.md` (Unreleased) to note removal

---

## 2026-02-06 (Session 12)

**Goals**:
- Close remaining manual test gap for empty task list UX

**Accomplished**:
- Added dev preference `dev_empty_tasks` to simulate a 0-task account (no API calls)
- Updated empty-state UI message to explain dev-empty behavior when enabled
- Added manual test plan for the empty-task-list scenario: `development/research/test_plan_v1.0.0_empty_tasks_2026-02-06.md`
- Manual empty-task-list tests: PASS (E01–E03)

**Files Changed**:
- `extension/manifest.json` - add dev empty-task-list preference
- `extension/main.py` - bypass API/cache when dev-empty is enabled
- `development/research/test_plan_v1.0.0_empty_tasks_2026-02-06.md` - new empty-list test plan
- `TODO.md` - link to the new empty-list test plan

---

## 2026-02-06 (Session 13)

**Goals**:
- Add unit test coverage for key helpers

**Accomplished**:
- Added unit tests for `DateParser` (today/tomorrow/yesterday, weekday parsing, time-only rollover, ISO datetime, invalid inputs)
- Added unit tests for `TaskFormatter` (priority mapping, overdue handling, subtitle truncation)

**Files Changed**:
- `extension/tests/test_date_parser.py` (new)
- `extension/tests/test_formatter.py` (new)
- `TODO.md` - check off unit test items

---

## 2026-02-06 (Session 14)

**Goals**:
- Add mock API unit tests (no network)

**Accomplished**:
- Added unit tests for `MorgenAPIClient` with mocked `urllib.request.urlopen`:
  - Success JSON parsing
  - HTTP error mapping (401/429/400/500)
  - Network error mapping (URLError)
  - Invalid JSON response handling
  - `list_tasks()` limit capping to 100
  - `create_task()` validation (priority range, due format)

**Files Changed**:
- `extension/tests/test_morgen_api.py` (new)
- `TODO.md` - check off mock API test item

---

## 2026-02-06 (Session 15)

**Goals**:
- Finalize v1.0.0 release artifacts

**Accomplished**:
- Recorded empty-task-list manual test results: PASS (E01–E03)
- Updated README version references to v1.0.0 and clarified Python requirement (3.10+)
- Created `main` branch and tagged release `v1.0.0`

---

## 2026-02-06 (Session 11)

**Goals**:
- Performance profiling and search optimization

**Accomplished**:
- Added `_timed()` context manager for profiling key operations (cache lookup, API calls, search, formatting)
- Implemented pre-computed lowercase search index in `cache.py`:
  - `_build_search_index()` creates `{task_id: (title_lower, desc_lower)}` on cache store/load
  - `get_search_index()` returns the index for fast lookups
  - Index rebuilt automatically when loading from disk
- Updated `_filter_tasks()` in `main.py` to use the search index
- Created performance test (`tests/test_perf.py`)
- Added result limit (`_MAX_DISPLAY_RESULTS = 7`) to prevent UI lag with large task lists
- Shows "... and X more" when results are truncated

**Performance Results**:
- Search with 500 tasks, 1000 iterations:
  - Without index: 217.89ms
  - With index: 162.33ms
  - **Improvement: 25.5%**
- Real-world timing (500 tasks):
  - cache_lookup: ~0.3ms
  - filter_tasks: ~0.3ms
  - format_7_tasks: ~1ms (vs 40ms for 500 tasks)

**Files Changed**:
- `extension/main.py` - Added timing, search index, result limit
- `extension/src/cache.py` - Added search index
- `extension/tests/test_perf.py` - Performance test (new)
- `extension/tests/__init__.py` - Test package (new)

**Notes**:
- Ulauncher doesn't support native scrolling (hard-coded 9-17 item limit)
- Pagination could be added as future enhancement

---

## 2026-02-06 (Session 10)

**Goals**:
- Phase 6 documentation

**Accomplished**:
- Updated `extension/README.md` with current features (v0.6.6)
- Created `extension/docs/USER_GUIDE.md` - complete usage guide
- Created `extension/docs/API_REFERENCE.md` - technical reference for developers

---

## 2026-02-06 (Session 9)

**Goals**:
- Phase 6 UI polish: better priority icons and overdue highlighting

**Accomplished**:
- Updated `extension/src/formatter.py`:
  - Added `is_overdue()` function to detect past-due tasks
  - Priority icons: `!!` (high/1), `!` (medium/5), none for low/normal
  - Added `get_priority_label()` for human-readable subtitle text (High, Medium, Low, Normal)
  - Overdue tasks show "OVERDUE" prefix in title and "(overdue!)" in subtitle
  - Due dates show relative labels ("Today 14:00", "Tomorrow 09:00")
- Updated priority logic to match Morgen's normalized values (High→1, Medium→5, Low→9)
- Updated `CHANGELOG.md` for v0.6.6
- Created test plan: `development/research/test_plan_v0.6.6_2026-02-06.md`

**Test Results**: All PASS (P01-P10, O01-O03, D01-D03, C01-C02, R01-R04)

---

## 2026-02-05 (Session 5)

**Goals**:
- Housekeeping after Phase 3

**Accomplished**:
- Archived completed AI handoff to `development/handoff/archive/`
- Synced `TODO.md` to reflect Phase 3 commit completion

**Notes**:
- Manual Ulauncher testing still recommended (`pkill ulauncher && ulauncher -v`)

---

## 2026-02-05 (Session 6)

**Goals**:
- Implement Phase 4: create tasks

**Accomplished**:
- Added `extension/src/date_parser.py` (`DateParser`) for due parsing
- Updated `extension/main.py` with create flow:
  - `mg new <title> [@due] [!priority]` (preview + confirmation)
  - Handles custom action via `ItemEnterEvent`
  - Invalidates cache after successful creation
- Updated docs for v0.4.0 (`CHANGELOG.md`, `README.md`, `extension/README.md`, `TODO.md`)

**Notes**:
- Manual testing needed in Ulauncher:
  - `mg new Test task`
  - `mg new Test @tomorrow`
  - `mg new Test @next-mon !3`

---

## 2026-02-05 (Session 7)

**Goals**:
- Phase 6 polish: fix help/search edge case

**Accomplished**:
- Fixed `mg help <query>` so it searches instead of opening help (help now triggers only on `mg help`, `mg ?`, or `mg h`)
- Updated `development/research/test_plan_v0.6.0_2026-02-05.md` with regression test `H10`
- Verified `H10` manually (PASS)

---

## 2026-02-05 (Session 8)

**Goals**:
- Phase 6 polish: add file-based runtime logging

**Accomplished**:
- Added rotating file logging to `extension/logs/runtime.log`

**Notes**:
- Add a numbered manual test plan for v0.6.1 to verify runtime log creation and content.

---

## 2026-02-05 (Session 9)

**Goals**:
- Prevent accidental rate limiting when using `mg refresh` / `mg !`

**Accomplished**:
- Made force refresh one-shot: only exact `mg refresh` or `mg !` triggers refresh
- Added a UI notice when the refresh prefix is detected with extra text (to clarify behavior)

**Notes**:
- Add a numbered test plan for v0.6.2 that covers one-shot refresh while typing.

---

## 2026-02-05 (Session 10)

**Goals**:
- Verify v0.6.1 and v0.6.2 manual test plans

**Accomplished**:
- v0.6.1 manual tests: PASS (`L01`–`L08`)
- v0.6.2 manual tests: PASS (`R01`–`R08`)

---

## 2026-02-05 (Session 11)

**Goals**:
- Phase 6 polish: improve error messages and runtime logging

**Accomplished**:
- Added more actionable UI error messages (auth/network/rate limit/unexpected) with tips and a pointer to `extension/logs/runtime.log`
- Added additional runtime log lines around cache/API actions and create-task outcomes

---

## 2026-02-05 (Session 12)

**Goals**:
- Phase 6 polish: quick access to runtime logs

**Accomplished**:
- Added UI items to open/copy the runtime log path from help and error screens

**Notes**:
- Add a numbered test plan for v0.6.4 to verify OpenAction/CopyToClipboardAction availability in the user environment.

---

## 2026-02-05 (Session 13)

**Goals**:
- Fix missing log access actions on certain screens

**Accomplished**:
- Added “Open runtime log” / “Copy log path” items to the welcome (missing API key) screen
- Added log access items to no-cache fallback error screen and create-task missing-API-key screen

---

## 2026-02-05 (Session 14)

**Goals**:
- Verify v0.6.5 manual test plan

**Accomplished**:
- v0.6.5 manual tests: PASS (`W01`–`W05`)

---

## 2026-02-05 (Session 4)

**Goals**:
- Implement Phase 3: list/search tasks UX
- Add force refresh command to bypass cache

**Accomplished**:
- Created `extension/src/formatter.py`
  - Added `TaskFormatter` with `format_for_display()` and `format_subtitle()`
  - Added `get_priority_icon()` helper
- Updated `extension/main.py` (Phase 3)
  - Lists all tasks when no query is provided
  - Filters tasks by query (title/description)
  - Force refresh via `mg refresh` or `mg !` (supports `!<query>` and `refresh <query>`)
  - Handles empty result sets gracefully
  - Shows cache status in header item
  - Enter on a task copies its ID when supported (fallbacks to close)
  - Improved fallback behavior to show cached tasks on rate-limit/network errors
- Updated `TODO.md` and `CHANGELOG.md` for v0.3.0

**Notes**:
- Manual testing still needed in Ulauncher (`pkill ulauncher && ulauncher -v`)

---

## 2026-02-05 (Session 3)

**Goals**:
- Test Phase 1 extension in Ulauncher
- Implement Phase 2: Morgen API integration

**Accomplished**:
- Phase 1 testing: PASSED
  - Extension loads in Ulauncher without errors
  - Keyword `mg` triggers correctly
  - Welcome message displays when no API key set
  - "Morgen Tasks is working!" displays when API key configured
  - Cache TTL preference shown correctly
- Phase 1 officially verified and complete

- Phase 2 implementation: COMPLETE
  - Updated `CLAUDE.md` with NixOS package management section and plans location
  - Updated `AGENTS.md` with NixOS section and updated plan references
  - Created `shell.nix` for NixOS development environment (Python 3 + dev tools)
  - Created `src/__init__.py` (package marker)
  - Created `src/morgen_api.py`:
    - Custom exceptions: `MorgenAPIError`, `MorgenAuthError`, `MorgenRateLimitError`, `MorgenValidationError`, `MorgenNetworkError`
    - `MorgenAPIClient` class with `list_tasks()` and `create_task()` methods
    - Full error handling for network, auth, rate limit, and validation errors
    - Uses `urllib.request` (stdlib) — no external dependencies
  - Created `src/cache.py`:
    - `TaskCache` class with TTL-based expiration (default 10 min)
    - Methods: `get_tasks()`, `set_tasks()`, `invalidate()`, `is_fresh()`, `get_age_display()`
    - Tracks `last_updated` for future incremental updates
  - Updated `main.py`:
    - Integrated API client and cache
    - Cache-first strategy (check cache before API call)
    - Lazy initialization (re-create client if API key changes)
    - Shows task count + first 5 tasks
    - Comprehensive error handling with fallback to cached data
  - Tested with real Morgen account — tasks load correctly, cache works

**Issues**:
- None

**Next Steps**:
- Phase 3: Task formatting and search
  - Create `src/formatter.py`
  - Implement search filtering
  - Better task display

---

## 2026-02-05 (Session 2)

**Goals**:
- Create comprehensive documentation for the repository
- Add guides for AI agents
- Create TODO list

**Accomplished**:
- Created `/home/user/Documents/AI/Morgen-Tasks/README.md`:
  - Complete project overview
  - Repository structure explanation
  - Installation and usage instructions
  - Technology stack and important notes
- Created `/home/user/Documents/AI/Morgen-Tasks/TODO.md`:
  - Detailed task list for all 7 phases
  - Immediate next steps (Phase 2)
  - Completed tasks checklist
  - Quick command reference
- Created `/home/user/Documents/AI/Morgen-Tasks/CLAUDE.md`:
  - Comprehensive guide for AI agents
  - Development workflow
  - File locations and purposes
  - Technical details (Morgen API, Ulauncher API)
  - Testing guidelines
  - Git workflow
  - Common commands
- Created `/home/user/Documents/AI/Morgen-Tasks/AGENTS.md`:
  - Quick reference card for AI agents
  - TL;DR section with essential info
  - Phase 2 checklist
  - Common issues and solutions
- Committed all documentation files (commit a1a9eaa)

**Issues**:
- None

**Next Steps**:
- User to test Phase 1 extension in Ulauncher
- Begin Phase 2: API integration
  - Create src/morgen_api.py
  - Create src/cache.py
  - Update main.py

**Notes**:
- Documentation is now comprehensive for any developer or AI agent
- Log files in `extension/logs/` were created earlier (dev_log.md, issues.md, improvements.md)
- All essential project information is now documented

---

## 2026-02-05 (Session 1)

**Goals**:
- Initialize project structure (Phase 0)
- Create basic Ulauncher extension (Phase 1)
- Test extension loads in Ulauncher

**Accomplished**:
- Created git repository in `/home/user/Documents/AI/Morgen-Tasks/`
- Initialized with main branch
- Created `.gitignore` for Python, logs, and sensitive data
- Created directory structure:
  - `extension/` - holds extension code
  - `development/` - research, prototypes, scratch work
  - Subdirectories: src, images, logs, tests, docs
- Created CHANGELOG.md with v0.1.0 entry
- Created this development log

**Issues**:
- None yet

**Next Steps**:
- ~~Create logs/issues.md and logs/improvements.md~~ ✓
- ~~Set up Ulauncher extension directory~~ ✓
- ~~Create placeholder icon~~ ✓
- ~~Create manifest.json with preferences~~ ✓
- ~~Create main.py with basic Extension class~~ ✓
- Test extension in Ulauncher (user needs to restart Ulauncher)
- Phase 2: API integration with Morgen

**Completed**:
- Phase 0 complete - Project structure established
- Phase 1 complete - Basic extension created
- Git commits made:
  - fa54568: Phase 0 - project structure
  - 2d44fb7: Phase 1 - basic extension
  - 731644d: Documentation updates

**Notes**:
- Using semantic versioning (0.x.y for pre-release)
- Morgen API list endpoint costs 10 points - caching is critical!
- Due dates must be exactly 19 characters: YYYY-MM-DDTHH:mm:ss
- Extension symlinked to: ~/.local/share/ulauncher/extensions/ulauncher-morgen-tasks/

## Testing Instructions

To test the extension:

1. Restart Ulauncher in verbose mode:
   ```bash
   pkill ulauncher
   ulauncher -v
   ```

2. Type `mg` (or your configured keyword) to trigger the extension

3. You should see:
   - "Welcome to Morgen Tasks!" if no API key configured
   - "Morgen Tasks is working!" if API key is configured

4. Configure API key:
   - Open Ulauncher preferences (Ctrl+,)
   - Go to Extensions tab
   - Find "Morgen Tasks"
   - Add your Morgen API key from platform.morgen.so
