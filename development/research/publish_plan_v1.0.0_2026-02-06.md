# Publish Plan — v1.0.0 (Ulauncher Morgen Tasks)

**Date**: 2026-02-06  
**Goal**: Publish the extension so it can be installed from GitHub and (optionally) listed on the Ulauncher extensions directory.

---

## Assumptions / Current State

- Release tag exists locally: `v1.0.0`
- `extension/versions.json` points to `v1.0.0`
- Your icon file is available at: `morgen_icon.png` (repo root)

---

## P01 — Repo Metadata (before creating GitHub repo)

1. Decide the GitHub repo name (recommended): `ulauncher-morgen-tasks`
2. Update `extension/manifest.json`:
   - Set `developer_url` to the final GitHub URL (currently a placeholder).
   - (Optional) Update `developer_name` to your name/GitHub handle.
3. (Optional) Add topics later on GitHub:
   - `ulauncher`, `ulauncher-extension`, `morgen`, `tasks`, `productivity`

---

## P02 — Icon + Screenshots

1. Set the extension icon used by Ulauncher:
   - Replace `extension/images/icon.png` with `morgen_icon.png` (rename/copy).
2. Create a screenshots folder:
   - `extension/images/screenshots/`
3. Capture 2–4 screenshots (recommended set):
   - List view (normal): `mg ` (space) with ≤5 results
   - List view (condensed): query that yields >5 results
   - Create preview: `mg new Test task @tomorrow !high`
   - Help screen: `mg help`
4. Add screenshots to `extension/README.md` (and optionally root `README.md`) using relative paths:
   - Example: `images/screenshots/list.png`

---

## P03 — Branch/Tag Compatibility for Ulauncher Install

Ulauncher installs from a GitHub repo using `versions.json`. Use `main` as the default branch.

1. Ensure `main` contains `extension/versions.json`
2. `extension/versions.json` should reference the release tag `v1.0.0`
3. Keep `develop` for ongoing work

Recommended branch model:
- `main` = install/release branch (stable)
- `develop` = ongoing development (contains `development/`)
- `vX.Y.Z` tags = releases (the extension installer pins to tags via `versions.json`)

Policy:
- Only merge `develop` → `main` for releases.
- Avoid merging `main` → `develop` (because `main` does not contain `development/`).

---

## P04 — Create GitHub Repo + Push

1. Create an **empty** GitHub repo (don’t add README/license via GitHub).
2. Add remote:
   - `git remote add origin <YOUR_GITHUB_REPO_URL>`
3. Push branches (choose which you want public):
   - `git push -u origin main`
   - `git push -u origin develop`
4. Push tags:
   - `git push origin --tags`
5. On GitHub, set the default branch to `main`.

---

## P05 — Verify Install From GitHub URL

1. Open Ulauncher → Preferences → Extensions → “Add extension”
2. Paste the GitHub repo URL: `https://github.com/<you>/<repo>`
3. Restart Ulauncher:
   - `pkill ulauncher && ulauncher -v`
4. Smoke-test:
   - `mg ` (space): list tasks
   - `mg refresh`: refresh one-shot
   - `mg new Test task @tomorrow !high`: create preview + create
   - Confirm the icon appears in the extension list

---

## P06 — Submit to the Ulauncher Extensions Directory (Optional)

The submission process may change over time, so verify the current method used by Ulauncher to list new extensions.

Checklist to have ready:
- GitHub repo URL (public)
- Short description (1–2 sentences)
- Keywords/category
- 1–2 screenshots
- Icon (already in repo)
- Confirmed install steps (P05)

Then submit via the official directory method (ext.ulauncher.io) or the currently recommended workflow.

---

## P07 — Post-Publish Cleanup (Optional)

1. Remove or hide dev-only preference from docs (keep it available, but avoid confusing users).
2. Add a short “Troubleshooting” section to `extension/README.md`:
   - missing API key
   - rate-limit + cache behavior
   - runtime log location

---

## Notes / Decisions Needed

- **GitHub URL**: needed to finalize `developer_url` in `extension/manifest.json`
- **Default branch**: use `main` (GitHub standard)
