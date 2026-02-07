# Implementation Plan — Task List Metadata Enrichment (v1.2.0)

**Date**: 2026-02-07  
**Scope**: Improve list/project/space labels when task payload only includes ids.

## Goal

Show user-friendly container names in UI whenever possible, even when tasks only expose id fields (for example `taskListId`, `integrationId`).

## Current State

- Container grouping/filtering exists.
- Name resolution depends on available maps and fallbacks.
- Some accounts still show id-like labels due to incomplete metadata resolution.

## Plan

### P1 — Normalize Metadata Inputs

1. Audit all container-like metadata sources currently captured from API payload and cache.
2. Build a single normalized name-map shape:
   - keyed by container kind (`list`, `project`, `space`, `integration`)
   - value: `{id -> display_name}`
3. Ensure id normalization is consistent (trim + case-insensitive matching).

### P2 — Improve Resolution Priority

1. Update `get_task_list_ref` resolution order:
   - explicit task name field (if present)
   - normalized map lookup by id
   - integration fallback map
   - id-only fallback label
2. Preserve current behavior for unknown/unavailable metadata (no crashes, clear fallback).

### P3 — Enrich Cache Metadata Lifecycle

1. Verify cache persists normalized name maps with tasks.
2. Confirm refresh/invalidate paths keep maps in sync with latest payload.
3. Ensure fallback-to-cache mode still resolves names with cached maps.

### P4 — UX and Debug Improvements

1. In list screens and task subtitles, prefer resolved names over raw ids.
2. Add/adjust `mg debug` field dump to include:
   - sample unresolved ids
   - map-hit/miss counts for troubleshooting.

### P5 — Testing

1. Unit tests:
   - id-to-name resolution precedence
   - case-insensitive id matching
   - integration fallback correctness
   - cache load/store map integrity
2. Manual tests (`ME01-ME06`):
   - list view shows names (not ids) when metadata exists
   - filtered commands (`mg in`, `mg list`, `mg project`, `mg space`) use enriched names
   - cached fallback keeps enriched naming
   - graceful fallback remains when no metadata exists

## Deliverables

- Code updates in:
  - `extension/src/task_lists.py`
  - `extension/src/cache.py` (if map storage changes)
  - `extension/main.py` (render/debug use of enriched names)
- New manual test plan:
  - `development/research/test_plan_v1.2.0_metadata_enrichment_2026-02-07.md`
- Tracking updates:
  - `TODO.md`
  - `CHANGELOG.md`
  - `extension/logs/dev_log.md`

## Risks / Notes

- API may not always provide authoritative names for every id.
- Some ids may remain unresolved; fallback labels must stay clear and stable.
- Keep change conservative to avoid regressing existing list filtering behavior.

## Suggested Execution Order

1. Implement resolver + map normalization (`task_lists.py`).
2. Add/adjust unit tests.
3. Wire display/debug usage in `main.py`.
4. Run automated checks.
5. Execute manual metadata enrichment test plan.
6. Update docs/logs and ship.
