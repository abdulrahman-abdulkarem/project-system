# CLAUDE.md Template

```markdown
# Project: [Project Name]

## Summary
One paragraph: what this project does, who it's for, and why it exists.

## Tech Stack
- Language/Framework: 
- Database: 
- Hosting/Infra: 
- Key libraries: 

## Architecture
Brief overview of how the project is structured. Mention key folders and what lives where.

Example:
- `/src/components` — UI components
- `/src/lib` — shared utilities, API clients
- `/src/app` — routes/pages
- `/supabase` — DB schema, migrations, RLS policies

## Key Decisions
Running list of important choices and the reasoning behind them — saves re-litigating old debates.

- **[Decision]**: [Why it was made, what alternative was rejected and why]
- Example: "Auth uses Supabase RLS instead of API-level checks — simpler to maintain and matches our other projects."

## Conventions
- Naming conventions (files, components, variables)
- Code style preferences (e.g. functional components only, no default exports, etc.)
- Patterns to follow / patterns to avoid
- Testing approach (if any)

## Environment Setup
Non-secret setup notes — what's needed to run the project locally.
- Node version / runtime requirements
- Install command
- Copy `.env.example` to `.env` and fill in values
- Any local services needed (e.g. local Supabase, Docker, etc.)

## Things Claude Code Should Know
Anything project-specific that would otherwise need re-explaining every session:
- Quirks in the codebase
- Things that look wrong but are intentional
- Areas that are fragile / need extra care when editing
```

---

# PROGRESS.md Template

```markdown
# Progress Log

## Open / Next up
- [ ] [Task description]
- [ ] [Task description]
- [ ] Blocked: [what's blocking, what's needed to unblock]

---

## YYYY-MM-DD (Device: PC/Laptop)
- [What was done]
- [What was fixed]
- Notes: [any reasoning worth remembering, e.g. why an approach was chosen or rejected]

## YYYY-MM-DD (Device: PC/Laptop)
- [What was done]
- ...
```

---

## Notes on usage
- **CLAUDE.md** = mostly static — update when architecture/decisions/conventions change.
- **PROGRESS.md** = update at the *end of every session*, newest entry on top. Ask Claude Code directly: "update PROGRESS.md with what we did today and commit it."
- Both files live in the repo root and get committed/pushed — that's what makes them sync across devices.
- Keep the "Open / Next up" checklist as the first thing you (or Claude Code) check at the start of a session.
