# AI Agent Guide - Morgen Tasks Extension

Primary guide for AI agents working in this repository.
`AGENTS.md` intentionally redirects to this file.

## Project Snapshot

- Project: Ulauncher extension for managing Morgen tasks
- Path: `/home/user/Documents/AI/Morgen-Tasks/`
- Working branch: `develop`
- Current released version: `v1.1.0`
- Current roadmap target: `v1.2.0` (manual verification + release prep)

Source of truth for status:
- `TODO.md`
- `CHANGELOG.md`
- `extension/logs/dev_log.md`

## Start-of-Session Checklist

1. Read current context:
   - `README.md`
   - `TODO.md`
   - `extension/logs/dev_log.md`
2. Check repo state:
   - `git status`
   - `git log --oneline -5`
3. Check active plans/tests:
   - `ls development/research/`

## Handoff Protocol (Required)

Use:
- `development/protocols/ai_agent_handoff_protocol_2026-02-07.md`

Write a handoff at natural break points, including when user says:
- `pause`
- `stop`
- `switch agents`
- `handoff session` (explicit trigger)

Handoff path format:
- `development/handoff/handoff_YYYY-MM-DD_HHmm.md`

At natural break points, ask:
- `Should I continue or would you like to check rate limits first?`

## Development Workflow

### During Work

- Make small, focused changes.
- Keep behavior changes and docs/log updates in the same logical change set.
- Prefer reliability and traceability over large refactors.

### Testing

Core local checks:

```bash
python -m py_compile extension/main.py
nix-shell --run "pytest -q"
pkill ulauncher && ulauncher -v
```

Manual test request format is mandatory:
1. Provide numbered test cases with stable IDs (`T01`, `T02`, ...).
2. Save a test plan file in:
   - `development/research/test_plan_<version>_<YYYY-MM-DD>.md`
3. Record/report outcomes by test ID (PASS/FAIL).

### End of Session / Feature Completion

Update all of the following:
- `CHANGELOG.md`
- `extension/logs/dev_log.md` (include test IDs + PASS/FAIL)
- `TODO.md` (tasks + context, not just checkboxes)

Then commit:

```bash
git add -A
git commit -m "type: short description"
```

Allowed commit types:
- `feat`
- `fix`
- `docs`
- `refactor`
- `test`
- `chore`
- `perf`
- `release`

## TODO.md Update Rules

Whenever `TODO.md` is edited:
1. Check off completed tasks.
2. Refresh **Immediate Next Steps** so they reflect what is actually next.
3. Keep status/version metadata accurate.
4. Use the Release Checklist for each feature/fix cycle.
5. Add shipped version tags on completed tasks when relevant (example: `(+v1.2.0)`).

## Git and Release Protocol

Use:
- `development/protocols/git_maintenance_protocol_2026-02-07.md`

Key rules:
- Do normal work on `develop`.
- Keep `main` stable and release-oriented.
- Do not force-push shared branches.
- Use semver tags for releases (`vX.Y.Z`).

## Repository Map

Core code:
- `extension/main.py`
- `extension/manifest.json`
- `extension/src/`
- `extension/tests/`

Tracking/docs:
- `TODO.md`
- `CHANGELOG.md`
- `extension/logs/dev_log.md`
- `extension/logs/issues.md`
- `extension/logs/improvements.md`
- `development/research/`
- `development/protocols/`

## NixOS Rules

- Use `shell.nix` / `nix-shell` for dependencies.
- Do not use `pip install` for project dependency management.
- Python dependencies belong in `shell.nix` (`python3Packages.*`).

## API and Product Constraints (Important)

- Morgen API base URL: `https://api.morgen.so/v3`
- Auth header: `Authorization: ApiKey <API_KEY>`
- Task list endpoint consumes points; cache usage is required.
- Due date format for writes: `YYYY-MM-DDTHH:mm:ss` (19 chars, no timezone suffix).

## Current Priority Focus

From current `TODO.md`:
1. Run and record manual `v1.2.0` test suites by test ID.
2. Verify dev-tools toggle behavior across fresh restart (`0` hides, `1` shows).
3. Prepare/release `v1.2.0` once verification is complete.

## Practical Reminders

- Update logs every session.
- Keep manual tests reproducible and file-backed.
- Prefer small commits with clear intent.
- If uncertain about current direction, re-check `TODO.md` first.
