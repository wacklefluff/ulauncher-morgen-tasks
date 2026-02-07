# AI Agent Handoff Protocol

Protocol for writing, consuming, and archiving AI handoff files for this repository.

## When to Write a Handoff

Write a handoff file at natural break points:
- After completing a sub-task (e.g., finished one file, moving to next)
- Before starting a large/risky change
- When user says `pause`, `stop`, or `switch agents`
- When user says `handoff session` (explicit trigger)
- If you receive a rate limit error
- Before context compaction/conversation restart

## Ask User to Check Rate Limits

At natural break points, ask:
- `Should I continue or would you like to check rate limits first?`

How users check rate limits:
- Claude Code: run `/status` or check `Account and usage...` in settings
- Codex CLI: run `codex --usage` or check OpenAI dashboard
- Gemini CLI: check Google AI Studio usage dashboard
- GitHub Copilot: GitHub settings -> Copilot -> Usage

## Handoff File Format

Create:
- `development/handoff/handoff_YYYY-MM-DD_HHmm.md`

Template:

```markdown
# AI Agent Handoff

**Agent**: [Model name]
**Timestamp**: YYYY-MM-DD HH:mm
**Reason**: [Natural break / User request / Rate limit / Context limit]

## Current Task
[What you were working on]

## Progress Made
- [Completed items]

## Next Steps
1. [Immediate next action]
2. [Following actions]

## Files Modified (uncommitted)
- [List any uncommitted changes]

## Notes for Next Agent
[Context, gotchas, important information]
```

## For Continuing Agents

1. Check `development/handoff/` for recent handoff files
2. Read the most recent handoff to understand context
3. Continue from where previous agent stopped
4. Archive completed handoff file to `development/handoff/archive/`
