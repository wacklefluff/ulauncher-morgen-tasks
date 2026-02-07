# Due Autocomplete Approach 2 - Parser State Model

**Date**: 2026-02-07  
**Strategy**: Refactor create parsing into explicit states (`valid`, `incomplete_due`, `invalid`) and drive UI from parser output.

## Steps

1. Introduce structured parse output.
   - Replace loose dict parsing with a typed parse result object, for example:
     - `status`: `valid` | `incomplete_due` | `invalid`
     - `title`, `priority`, `due`, `due_fragment`, `error`

2. Split due parsing into two phases.
   - Phase A: lexical parse (`@...` token extraction, detect incompletes).
   - Phase B: semantic parse with `DateParser` only when token is complete enough.

3. Centralize suggestion generation from parser state.
   - If state is `incomplete_due`, generate candidate suggestions from fragment.
   - If state is `valid`, show normal create/cancel items.
   - If state is `invalid`, show error item plus recovery suggestions.

4. Reuse parser state for all create entry points.
   - `mg new ...`
   - `mg add ...`
   - shortcut create keyword

5. Add tests around parser states.
   - Unit tests for each status transition and edge cases.
   - UI behavior tests for result composition based on parse status.

## Pros

- Most maintainable long-term.
- Clear behavior for ambiguous input and fewer regressions later.
- Easier to extend for future autocomplete types (priority, list tags).

## Cons

- Higher implementation cost than direct UI patching.
- Requires broader refactor in `extension/main.py`.

