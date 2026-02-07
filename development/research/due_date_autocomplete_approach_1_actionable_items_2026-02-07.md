# Due Autocomplete Approach 1 - Actionable Suggestion Items

**Date**: 2026-02-07  
**Strategy**: Keep Ulauncher interaction simple by showing clickable/enter-able due suggestions that directly create the task.

## Steps

1. Detect due-entry context in create flow.
   - In `extension/main.py`, identify when the last token is `@` or starts with `@`.
   - Extract the typed fragment (`@to` -> `to`).

2. Build a suggestion catalog and prefix matcher.
   - Add ordered candidates (`today`, `tomorrow`, weekdays, `next-...`, time examples).
   - Filter by fragment prefix and cap to a small result count.

3. Render a "Due suggestions" section under create flow.
   - Keep existing `Create: <title>` first item unchanged.
   - Add suggestion rows such as `Use due: @today`, `Use due: @tomorrow`.

4. Make each suggestion row actionable.
   - On Enter, fire `ExtensionCustomAction({"action": "create_task", ...})` with resolved due.
   - Use `DateParser` for canonical due string (`YYYY-MM-DDTHH:mm:ss`).

5. Handle partial input gracefully.
   - For bare/partial due (`@`, `@to`), show suggestions instead of hard invalid-date errors.
   - Keep strict errors for truly invalid complete tokens.

## Pros

- Lowest-risk change, minimal architecture impact.
- Works with existing Ulauncher behaviors.
- Fast to ship and easy to test.

## Cons

- Does not insert text into query; it is "select to create" rather than "autocomplete in-place".

