# Project System

A reusable setup-and-rules system for building software with Claude Code. Arabic/RTL-first, validated on a real project rather than assembled from theory.

## Start here

Beginning a new project? Pick the prompt that matches your situation from `prompts/` and paste the whole code block into Claude Code as your first message:

| Situation | Prompt |
|---|---|
| New project | `prompts/new-project-kickoff-prompt.md` |
| Project already underway | `prompts/existing-project-setup-prompt.md` |
| Setup got interrupted or half-finished | `prompts/repair-setup-prompt.md` |

Each one sets up CLAUDE.md, PROGRESS.md, README.md, DESIGN.md and CHECKPOINTS.md, embeds the rules so they load every session, and ends with "Setup complete — the shortcuts are active."

## The one rule for this repo

**Never edit anything in `prompts/`.** Everything in there is generated. Edit the masters, then regenerate:

```bash
python3 build-prompts.py
```

Hand-editing a generated prompt is how these files silently drifted apart the first time — one of them lost its entire design section and most of its security section, and nobody noticed for weeks.

## Layout

```
masters/          Edit these. The single source of truth.
  project-rules.md          Always-on rules → embedded in CLAUDE.md
  project-checkpoints.md    On-demand procedures → written to CHECKPOINTS.md

prompts/          GENERATED — never edit by hand
  new-project-kickoff-prompt.md
  existing-project-setup-prompt.md
  repair-setup-prompt.md
  CHECKPOINTS.md            standalone copy, droppable into a project

guides/           Reference, read as needed
  project-lifecycle-playbook.md      phase-by-phase map, Kickoff → Run/handover
  project-startup-plan-and-toolkit.md startup sequence, design workflow, tool menu
  claude-code-templates.md            CLAUDE.md / PROGRESS.md templates

taste-library/    Design reference bank — the part that has to be yours
  taste-library.md          four-session build guide + entries
  screenshots/

arabgo/           Sandbox notes from the project used to validate all of this
build-prompts.py  Regenerates prompts/ from masters/
```

## The architecture

Rules split two ways, and the test is simple:

- **Always-on** (`masters/project-rules.md` → CLAUDE.md) — rules that stop you writing something wrong *at the moment you write it*. "Never hardcode secrets." "Animate transform and opacity only." These must be in context before the mistake happens.
- **On-demand** (`masters/project-checkpoints.md` → CHECKPOINTS.md) — *procedures run at a specific moment*: the review pass, testing standards, the data-model check, the language/accessibility audit, the performance pass, motion, ship. Useless as ambient context, expensive as always-on text. A shortcut loads them when the moment arrives.

The split is what allows seven full procedures to cost ~25 lines of session context instead of ~200.

## Shortcuts

Typed as ordinary messages in the Claude Code chat, not in a terminal.

**Every session:** `wrap up` (updates docs) · `commit` (reviews staged files, then commits and pushes)

**While working:** `plan` (approach + rejected alternative, then waits) · `Q&A` / `Q&A short` / `Q&A history` (consult mode, logs to QA.md)

**Checkpoints** — each loads its procedure and reports without fixing:
`review` · `test check` · `schema check` · `lang check` / `rtl check` / `a11y check` · `perf pass` · `motion check` · `ship check`

## Status

Validated end-to-end against a live Next.js/Prisma/Supabase project in August 2026. That run produced eight fixes to this system, including one silent failure worth knowing about: a clean git merge that quietly discarded the entire contents of a branch, because the target branch contained a revert of a shared commit.

The design and UI half is well exercised. The security and backend half is not — the validation run was UI work throughout. Treat those rules as sound but unproven.

Full log: `arabgo/arabgo-validation-run.md`.
