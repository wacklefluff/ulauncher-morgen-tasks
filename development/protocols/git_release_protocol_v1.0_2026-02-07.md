# Git Release Protocol

**Version**: 1.0
**Project**: Ulauncher Morgen Tasks Extension
**Date**: 2026-02-07
**Related**: `git_maintenance_protocol_2026-02-07.md` (Section 5)

## Overview

This protocol documents the exact steps to release `develop` to `main` for this project. The two branches have **different directory structures**:

- `develop`: extension code lives inside `extension/`, plus dev-only files (`CLAUDE.md`, `TODO.md`, `development/`, `shell.nix`, etc.)
- `main`: extension files at repo root (flat layout required by Ulauncher's extension installer)

Because of this structural difference, releases are **not a merge** — they are a rebuild of `main` from `develop`'s `extension/` directory.

---

## Pre-Release (on `develop`)

### 1. Finalize CHANGELOG

Change `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD`:

```markdown
## [1.1.0] - 2026-02-07    ← was: ## [Unreleased]
```

Review entries — remove any that belong to a previous release.

### 2. Update TODO.md

- Update version/status line
- Mark roadmap items as complete
- Add release to Release History

### 3. Update extension/README.md

- **Version**: Update the "Current Version" line to the new version
- **Roadmap**: Ensure a "Roadmap" section exists listing planned/upcoming features
- **Features**: Add any new features to the Features list if not already there

### 4. Commit and push

```bash
git add CHANGELOG.md TODO.md extension/README.md
git commit -m "docs: finalize CHANGELOG and README for vX.Y.Z release"
git push origin develop
```

Ensure the working tree is **completely clean** before proceeding — `git checkout main` will fail otherwise.

---

## Release Build (on `main`)

### 5. Switch to main

```bash
git checkout main
```

### 6. Clear all tracked files

```bash
git rm -r .
```

This removes everything from `main`'s working tree and index. The `.git/` directory is preserved.

### 7. Copy extension directory from develop

```bash
git checkout develop -- extension/
```

### 8. Remove files that must not be committed

```bash
rm -rf extension/__pycache__
rm -rf extension/src/__pycache__
rm -rf extension/tests/__pycache__
rm -f  extension/logs/runtime.log
```

### 9. Move extension files to repo root

The flat layout is required by Ulauncher's installer (expects `manifest.json` at root).

```bash
# Move .gitignore first (hidden file)
git mv extension/.gitignore . 2>/dev/null

# Move all visible files/dirs
for item in extension/*; do
    git mv "$item" .
done

# Clean up empty directory
rmdir extension
```

**Pitfall**: If a directory already exists at root (from a previous partial move or stale state), `git mv` will fail with "destination already exists". Fix by removing the stale root copy first:

```bash
rm -rf ./src  # remove stale copy
git mv extension/src .  # now works
```

### 10. Restore .gitignore (if missing)

Step 6 (`git rm -r .`) deletes the `.gitignore`. If step 9 didn't restore it (e.g., `.gitignore` wasn't in `extension/`), recreate it:

```bash
git show develop:.gitignore > .gitignore
# or: git show develop:extension/.gitignore > .gitignore
```

### 11. Remove dev-only directories

These exist on `develop` but should not ship on `main`:

```bash
rm -rf development/
```

### 12. Fix `extension/` path references

Several files contain paths like `extension/logs/runtime.log` that are valid on `develop` but wrong on `main` (where it's just `logs/runtime.log`).

**Files to check and fix**:

| File | What to change |
|------|---------------|
| `main.py` | `_RUNTIME_LOG_HINT` variable |
| `README.md` | Log location references |
| `docs/USER_GUIDE.md` | Log location references |
| `docs/API_REFERENCE.md` | Log location + architecture tree |

Search command:
```bash
grep -r "extension/" --include="*.py" --include="*.md" .
```

**Exception**: `logs/dev_log.md` contains historical references to `extension/` paths — leave these as-is (they document the develop branch structure).

### 13. Verify staging area

```bash
git add -A
git status
```

**Checklist** — verify there are:
- No `__pycache__/` files staged
- No `runtime.log` staged
- No `development/` directory
- No `CLAUDE.md`, `TODO.md`, `shell.nix`, `AGENTS.md` (dev-only files)
- `.gitignore` is present
- `manifest.json` is at root (not inside `extension/`)

---

## Tag and Push

### 14. Commit the release

```bash
git commit -m "$(cat <<'EOF'
release: vX.Y.Z

Short summary of what's in this release.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

### 15. Create annotated tag

```bash
git tag -a vX.Y.Z -m "$(cat <<'EOF'
vX.Y.Z

- Feature 1
- Feature 2
- Fix 1
EOF
)"
```

### 16. Push main and tag

```bash
git push origin main --tags
```

---

## GitHub Release

### 17. Create GitHub Release

```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes "$(cat <<'EOF'
### Added
- Feature descriptions from CHANGELOG

### Changed
- Change descriptions from CHANGELOG

### Fixed
- Fix descriptions from CHANGELOG
EOF
)"
```

This creates a release page at `https://github.com/<owner>/<repo>/releases/tag/vX.Y.Z`.

---

## Post-Release

### 18. Switch back to develop

```bash
git checkout develop
```

### 19. Update TODO.md on develop

- Add new version to Release History
- Update "Current Version" line
- Clear or update "Immediate Next Steps"

### 20. Commit post-release updates

```bash
git add TODO.md
git commit -m "docs: post-release updates for vX.Y.Z"
git push origin develop
```

---

## Known Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `git checkout main` fails | Uncommitted changes on develop | Commit or stash first |
| `git mv` "destination exists" | Partial move left stale dirs at root | `rm -rf ./dir` then retry |
| `__pycache__` in staging | Copied from `extension/` | `git rm -r --cached **/__pycache__` |
| `runtime.log` in staging | Copied from `extension/logs/` | `git rm --cached logs/runtime.log` |
| `.gitignore` missing | Deleted by `git rm -r .` | Restore from develop |
| `extension/` paths in docs | Develop uses `extension/` prefix | Grep and fix (see step 12) |
| Interactive `mv` prompt | System `mv` asks about overwrite | Use `git mv` or `mv -f` |
| README shows old version | Forgot to update before release | Update in step 3 (pre-release) |
| README missing roadmap | Not added before release | Add roadmap section in step 3 |

---

## Quick Reference

```bash
# Full release sequence (after pre-release commits on develop)
git checkout main
git rm -r .
git checkout develop -- extension/
rm -rf extension/__pycache__ extension/src/__pycache__ extension/tests/__pycache__
rm -f extension/logs/runtime.log
git mv extension/.gitignore . 2>/dev/null
for item in extension/*; do git mv "$item" .; done
rmdir extension
rm -rf development
# Fix extension/ path references in main.py, README.md, docs/
git add -A
git status  # verify clean
git commit -m "release: vX.Y.Z"
git tag -a vX.Y.Z -m "vX.Y.Z — summary"
git push origin main --tags
gh release create vX.Y.Z --title "vX.Y.Z" --notes "release notes"
git checkout develop
```
