# AI Agent Handoff Directory

This directory contains handoff files for seamless work transfer between AI agents.

## When to Create Handoffs

AI agents write handoff files at **natural break points**:
- After completing a sub-task
- Before large/risky changes
- On user request ("pause", "stop", "switch agents")
- On rate limit errors
- Before context compaction

## For Users: Checking Rate Limits

- **Claude Code**: Run `/status` or "Account and usage..." in settings
- **Codex CLI**: Run `codex --usage` or check OpenAI dashboard
- **Gemini CLI**: Check Google AI Studio usage dashboard
- **GitHub Copilot**: GitHub settings → Copilot → Usage

## For Agents

### Creating Handoffs
1. Create `handoff_YYYY-MM-DD_HHmm.md` with current state
2. Commit uncommitted work if possible
3. Notify user

### Continuing from Handoffs
1. Check this directory for recent files
2. Read the most recent for context
3. Continue where previous agent stopped
4. Move completed files to `archive/`

## File Format

See `CLAUDE.md` or `AGENTS.md` for the template.
