 # Manual Test Plan — v1.2.0 Task Filters (Priority + Due)

**Date**: 2026-02-07  
**Scope**: Validate search/list filtering by `p:`/`priority:` and `due:` query tokens.

## Preconditions

- Restart Ulauncher in verbose mode:
  - `pkill ulauncher && ulauncher -v`
- Extension enabled
- Morgen API key configured
- Have a mix of tasks with different priorities and due states

## Tests

- **TF01** — Due filter: today
  1. Type: `mg due:today`
  - **Expected**:
    - Results include only tasks due today
    - No crash or malformed UI
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **TF02** — Priority filter: high
  1. Type: `mg p:high`
  - **Expected**:
    - Results include only high-priority tasks (`priority=1`)
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**: should also work `!` and `!!`

- **TF03** — Combined filters
  1. Type: `mg due:today p:high`
  - **Expected**:
    - Results satisfy both due and priority filters
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **TF04** — Text + filter composition
  1. Type: `mg report due:week`
  - **Expected**:
    - Results match text query and due filter together
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **TF05** — Unknown filter values degrade safely
  1. Type: `mg due:later p:urgent`
  - **Expected**:
    - No crash
    - Unknown filter tokens are treated as plain text search terms
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

- **TF06** — Existing plain search remains unchanged
  1. Type: `mg <known keyword>`
  - **Expected**:
    - Normal search behavior unchanged from before
  - **Result**: [X] PASS  [ ] FAIL  [ ] SKIP
  - **Notes**:

