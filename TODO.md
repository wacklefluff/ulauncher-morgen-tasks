# TODO - Ulauncher Morgen Tasks Extension

Current task list and development roadmap.

**Last Updated**: 2026-02-07
**Current Version**: v1.1.0 (Released)
**Current Branch**: `develop` (up to date with origin)

## Release Checklist (Repeat Every Feature/Fix)

Use this checklist **every time** you implement a feature or fix (not just once per phase).

- [ ] Update `CHANGELOG.md` (add/move items into the correct version section)
- [ ] Update `extension/logs/dev_log.md` (include test IDs + PASS/FAIL)
- [ ] Update `TODO.md` context
  - [ ] Check off completed tasks
  - [ ] Refresh current roadmap to reflect what's next
- [ ] Write/update a numbered manual test plan: `development/research/test_plan_vX.Y.Z_YYYY-MM-DD.md`
- [ ] Run manual tests and record results by test ID
- [ ] Commit (and include the version in the commit message when appropriate)

**Version tags**: When marking a task done, append the version it shipped in, e.g. `(+v1.2.0)`.

## Immediate Next Steps

1. Run manual v1.2.0 tests and record PASS/FAIL by test ID (`DD01-DD06`, `LIM01-LIM03`)
2. Pick any remaining v1.2.0 scope items from the roadmap below
3. Release v1.2.0

## Release History

- v1.1.0 — task completion, task lists, debug command, shortcut keywords
- v1.0.0 — published to GitHub + Ulauncher directory
- v0.6.6 — better priority icons + overdue highlighting
- v0.6.5 — show log access on welcome/error fallbacks
- v0.6.4 — open/copy runtime log from UI
- v0.6.3 — improved errors + runtime logging tips
- v0.6.2 — one-shot refresh
- v0.6.1 — file-based runtime logging
- v0.6.0 — help + clear cache commands
- v0.5.0 — disk-persistent cache
- v0.4.0 — create tasks + due parsing
- v0.3.0 — list/search/refresh tasks

---

## v1.2.0 Roadmap

Candidates — pick items to commit to this release:

### From Backlog
- [x] **DEV-01**: Add dummy task seeding tools (`mg dev dummy-tasks` + CLI script) (+v1.2.0)
- [x] **DEV-02**: Add dummy-task bulk-complete action in `mg dev dummy-tasks` (+v1.2.0)
- [x] **LIM-01**: Warn in UI when task list response hits API cap (100 tasks) (+v1.2.0)

### From Future Enhancements (High)
- [ ] Filter tasks by priority/due date
- [ ] Task list metadata enrichment (resolve user-friendly names when API only returns ids)
- [x] Make first dropdown item the actionable "Create" option so Enter creates the task immediately (+v1.2.0)
- [ ] Due-date autocomplete: typing `@` shows a dropdown with date suggestions (e.g. `@to` suggests "today", "tomorrow")


---

## Backlog

Items not yet scheduled. May be promoted to a version roadmap.

- [x] **SUG-01** (T02): Fix welcome screen when typing `mg` with no space — **won't fix** (Ulauncher limitation)
- [ ] **VIM-like mode**: Alt+J/K navigation — not natively supported by Ulauncher v5 (requires system-level key remap)
- [ ] Lazy load task details
- [ ] Pagination for large result sets (Ulauncher lacks native scroll)
- [ ] Open log file button in Ulauncher settings (blocked: preferences don't support buttons)

---

## Currently not Possible

- [ ] Load full task history when account has more than 100 tasks. Current `GET /v3/tasks/list` usage is capped at 100 and no pagination/cursor flow is implemented.

---

## Future Enhancements

See `extension/logs/improvements.md` for detailed ideas.

### High Priority
- [ ] Filter tasks by priority/due date
- [ ] Task list metadata enrichment (resolve user-friendly names when API only returns ids)


### Medium Priority
- [ ] Subtask creation
- [ ] Recurring tasks support
- [ ] Progress status indicator (add an emoji before task title)
- [ ] Better keyboard shortcuts (Alt+Enter actions)
- [ ] Desktop notifications for upcoming tasks
- [ ] Parse `#<tag>` for tags
- [ ] autocomplete words for dates (e.g. @tomorrow)


### Low Priority / Nice-to-Have
- [ ] when showing a lot of results, next page option could be on top message
- [ ] Integration with system notifications
- [ ] Quick scheduling (time blocking)
- [ ] Task templates
- [ ] Bulk operations
- [ ] Update task details (title, due date, priority)
- [ ] Shorter dates, writting DD-MM should be enough, it assumes first time that date occurs. so if it is may and i say 13-02 then it stores for next year
- [ ] Background refresh (refresh cache in background without blocking UI). Is it really needed?
---

## Completed Releases

### v1.1.0 (2026-02-07)
Debug command, task completion, task lists, shortcut keywords, protocol docs.
See [GitHub Release](https://github.com/wacklefluff/ulauncher-morgen-tasks/releases/tag/v1.1.0).

### v1.0.0 (2026-02-06)
First public release — list/search/create, caching, help, tests, published to GitHub + Ulauncher directory.
See [GitHub Release](https://github.com/wacklefluff/ulauncher-morgen-tasks/releases/tag/v1.0.0).

### v0.1.0–v0.6.x (2026-02-05 – 2026-02-06)
Phases 0–6: project setup, basic extension, API integration, list/search, create tasks, caching, polish.
See [CHANGELOG.md](CHANGELOG.md) for full details.

---

## Notes

- Remember to update `extension/logs/dev_log.md` during each session
- Log issues in `extension/logs/issues.md` as they arise
- Log improvement ideas in `extension/logs/improvements.md`
- Protocols live in `development/protocols/` (handoff, git maintenance, release)
- Make small, frequent git commits
- Test after each feature implementation

## Reminders

- **P07** Post-publish cleanup (ongoing, not version-tied)
  - Keep troubleshooting accurate (API key, rate limit, runtime log)
  - Use GitHub Releases for binaries/archives (avoid committing zips into repo)

## Quick Commands

```bash
# Start development session
cd /home/user/Documents/AI/Morgen-Tasks/
git checkout develop

# Test extension
pkill ulauncher && ulauncher -v

# Commit changes
git add -A
git commit -m "feat: description"

# View logs
cat extension/logs/dev_log.md
```
