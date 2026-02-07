# Due Autocomplete Approach 3 - Tab-to-Fill Concept

**Date**: 2026-02-07  
**Strategy**: Aim for shell-like Tab completion of `@...` fragments, with graceful fallback if Ulauncher cannot capture Tab for extension-level text mutation.

## Steps

1. Validate Ulauncher key handling capabilities.
   - Confirm whether extension APIs can intercept Tab and replace current query text.
   - If unsupported, explicitly fall back to Enter-based suggestion actions.

2. If Tab interception is supported, implement query rewrite flow.
   - On Tab while in create flow and on partial `@...`, choose top suggestion.
   - Rewrite query text from e.g. `mg new Task @to` to `mg new Task @today`.

3. Add visible ranking and hinting.
   - Show top suggestion first and a hint line:
     - `Tab: fill @today`
   - Keep additional alternatives below.

4. Add Enter fallback behavior.
   - Enter on suggestion should still work and create task.
   - This ensures behavior remains functional even if Tab is unavailable on some systems.

5. Add compatibility guardrails.
   - Feature flag this path (`tab_due_autocomplete=1/0`) if needed.
   - Default to OFF until verified on target Ulauncher versions.

## Pros

- Best UX if technically feasible (fast in-place completion).
- Familiar behavior for keyboard-heavy users.

## Cons

- High feasibility risk: Ulauncher extension APIs commonly do not support direct Tab-query mutation.
- More cross-version/platform uncertainty.
- Requires fallback path anyway, increasing complexity.

## Recommendation

- Prototype feasibility first.
- If Tab rewrite is not reliably supported, ship Approach 1 and keep this as a future enhancement.

