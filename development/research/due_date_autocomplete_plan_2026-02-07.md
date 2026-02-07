# Due-Date Autocomplete Plan — v1.2.0

**Date**: 2026-02-07  
**Scope**: Add due-date autocomplete suggestions while typing create commands (`mg new ...`, `mg add ...`, and shortcut create keyword).

## Goal

When the user types a due marker (`@...`) in create flow, show suggestion items for supported due formats (for example `@today`, `@tomorrow`, `@next-mon`) and let Enter create using that suggestion.

## Current Behavior (Baseline)

- Create flow parsing is handled in `extension/main.py`:
  - `_maybe_build_create_flow()`
  - `_build_create_flow_items()`
  - `_parse_create_args()`
- Due parsing currently requires a complete date token; partial tokens like `@to` return an invalid-date error and no guidance list.
- A bare `@` is currently treated as title text instead of due context.

## Implementation Plan

### P1 — Add Due Suggestion Catalog + Matcher

- Add helper(s) in `extension/main.py` to produce due suggestions from a typed fragment:
  - Input fragment examples: `""` (for `@`), `"to"` (for `@to`), `"next-"`.
  - Suggested canonical values should map to `DateParser`-supported input:
    - `today`, `tomorrow`, `yesterday`
    - weekdays (`mon`..`sun`)
    - `next-mon`..`next-sun`
    - `next-week`
    - time examples (`09:00`, `15:30`, `3pm`, `noon`, `midnight`)
    - date format hints (`2026-02-10`, `2026-02-10T15:30`)
- Matching rule:
  - Prefix match against normalized fragment.
  - Keep deterministic ordering (most common first: `today`, `tomorrow`, weekdays, etc.).

### P2 — Detect Active Due-Token Context in Create Input

- Add helper to inspect raw create text (`rest`) and detect whether user is typing a due token:
  - Active when last token starts with `@` (including bare `@`).
  - Capture typed fragment (text after `@`) for filtering suggestions.
- Keep parser behavior stable for non-autocomplete paths.

### P3 — Render Autocomplete Items in Create Flow

- Update `_build_create_flow_items()`:
  - Keep existing primary create/cancel UX.
  - When due autocomplete context is active, append a "Due suggestions" section.
  - Add actionable suggestion items that create the same task title/priority but with selected due.
- Each suggestion item should:
  - Pre-parse selected due token via `DateParser`.
  - Show display date/time in subtitle.
  - Use `ExtensionCustomAction({"action": "create_task", ...})` so Enter on suggestion creates immediately.

### P4 — Graceful Incomplete-Due UX

- Prevent confusing hard-fail when user is clearly mid-typing a due token:
  - For bare `@` or partial `@to`, show suggestion items instead of only invalid-date error.
  - Keep validation strict for non-partial invalid values (e.g., `@notadate` after user stops on full token).
- Ensure `@` is not silently added to title in create flow.

### P5 — Docs + Tracking

- Update:
  - `extension/README.md` with autocomplete examples.
  - `CHANGELOG.md` (`Unreleased`).
  - `TODO.md` roadmap checkbox for due-date autocomplete once shipped.
  - `extension/logs/dev_log.md` with test IDs and PASS/FAIL.

## Manual Test Plan (to create during implementation)

Create file:
- `development/research/test_plan_v1.2.0_due_autocomplete_2026-02-07.md`

Suggested IDs:
- `DA01` Typing `mg new Task @` shows due suggestions.
- `DA02` Typing `mg new Task @to` narrows to `today`/`tomorrow`.
- `DA03` Enter on suggestion creates task with expected due.
- `DA04` Works with quick-create keyword as well as `mg new`.
- `DA05` Invalid complete token still shows clear validation message.

## Acceptance Criteria

1. Typing `@` inside create flow surfaces due suggestions immediately.
2. Typing partial fragments (for example `@to`) narrows suggestions.
3. Enter on a due suggestion creates the task with correct due datetime format (`YYYY-MM-DDTHH:mm:ss`).
4. Existing create behavior (priority parsing, title parsing, cancel flow) remains unchanged.
5. No regression in non-create commands.

## Risks / Notes

- Ulauncher does not provide direct query-text replacement in this flow; suggestions are implemented as actionable create items rather than text insertion.
- `DateParser` resolves weekday/time against current local time; test notes should account for date rollovers.
