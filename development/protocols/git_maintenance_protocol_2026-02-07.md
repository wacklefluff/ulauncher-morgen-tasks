# Git Structure, Branches, Tags, and Maintenance Protocol

**Project**: Ulauncher Morgen Tasks Extension  
**Date**: 2026-02-07  
**Canonical remote**: `origin`

## 1. Repository Structure (Git Perspective)

- `main`
  - Stable, release-ready branch.
  - Should contain only what users/installers need for release.
- `develop`
  - Active development branch.
  - Can include development notes, plans, experiments, and in-progress features.
- Tags
  - Semantic version tags (example currently in repo: `v1.0.0`).
  - Tags mark immutable release points.

Current observed state pattern:
- Local feature work -> `develop`
- Release snapshots -> tags like `vX.Y.Z`
- Stable channel -> `main`

## 2. Branch Rules

- Do all normal feature/fix/docs work on `develop`.
- Keep `main` clean and stable; do not commit experimental work there.
- Never force-push shared branches (`main`, `develop`) unless explicitly coordinated.
- Keep commit messages consistent: `type: description`.

Suggested commit types:
- `feat` new functionality
- `fix` bug fix
- `docs` documentation-only changes
- `refactor` internal restructuring without behavior change
- `test` tests added/updated
- `chore` maintenance
- `perf` performance improvements
- `release` release-specific commits

## 3. Tagging Rules

- Use Semantic Versioning tags: `vMAJOR.MINOR.PATCH`.
- Create tags only after:
  - tests pass,
  - docs/changelog/todo are updated,
  - release branch content is correct.
- Use annotated tags for release notes context.

Commands:
```bash
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
```

Or push all local tags:
```bash
git push origin --tags
```

## 4. Daily Maintenance Protocol

### Session Start

```bash
git checkout develop
git pull origin develop
git status
git log --oneline -5
```

Then read current context files:
- `TODO.md`
- `extension/logs/dev_log.md`
- active test plan(s) in `development/research/`

### During Work

- Make small, focused commits.
- Run tests before commit.
- Update these in the same change set:
  - `CHANGELOG.md` (Unreleased section)
  - `extension/logs/dev_log.md`
  - `TODO.md` roadmap/context
  - test plan files when manual tests are involved

### Before Commit

```bash
git status
nix-shell --run "pytest -q"
```

### Commit

```bash
git add -A
git commit -m "type: short description"
```

### Push

```bash
git push origin develop
```

## 5. Release Protocol (`develop` -> `main` + tag)

Use this only when releasing a stable version.

1. Ensure `develop` is green and updated.
2. Prepare release notes in `CHANGELOG.md`.
3. Move release content to `main` per project packaging policy.
4. Commit release on `main`.
5. Tag release.
6. Push `main` and tags.
7. Return to `develop`.

Reference commands:
```bash
# from a clean tree
git checkout main
git pull origin main
# (apply project-specific release layout update here)
git add -A
git commit -m "release: vX.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin main
git push origin vX.Y.Z
git checkout develop
```

## 6. Hotfix Protocol

For urgent production fixes:

1. Branch from `main`:
```bash
git checkout main
git pull origin main
git checkout -b hotfix/vX.Y.Z+1
```
2. Apply fix + tests.
3. Commit.
4. Merge into `main` and tag patch release.
5. Back-merge same fix into `develop`.

## 7. Rollback Protocol

If a release is bad:

- Preferred: create a forward-fix patch release.
- If immediate rollback needed, redeploy previous tag and communicate clearly.

Identify previous stable tag:
```bash
git tag --sort=-v:refname
```

Inspect tag commit:
```bash
git show v1.0.0 --no-patch
```

## 8. Hygiene Checklist (Per Feature/Fix)

- [ ] Code implemented and tested
- [ ] Manual tests run and recorded by ID (if applicable)
- [ ] `CHANGELOG.md` updated
- [ ] `extension/logs/dev_log.md` updated
- [ ] `TODO.md` updated (including roadmap status)
- [ ] Commit created with proper `type:` prefix
- [ ] Pushed to `origin/develop`

## 9. Safety Rules

- Do not rewrite shared history casually.
- Do not use destructive commands (`reset --hard`, force-push) unless explicitly approved.
- Keep commits focused; avoid bundling unrelated work.
- Prefer reverting bad commits over rewriting public history.

## 10. Useful Quick Commands

```bash
# status + branch
git status -sb

# recent commits
git log --oneline -10

# inspect changed files
git diff --stat

# show local-only commits
git log origin/develop..develop --oneline

# sync develop
git checkout develop && git pull origin develop
```

## 11. Project-Specific Notes

- Active branches currently present: `main`, `develop`.
- Current known release tag in repo: `v1.0.0`.
- This project uses Nix; run tests via:
```bash
nix-shell --run "pytest -q"
```
