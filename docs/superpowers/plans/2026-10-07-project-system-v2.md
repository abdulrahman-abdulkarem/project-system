# Project System v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deliver Project System v2 in `/home/abdulrahman_abdulkarem/dev/project-system/v2/`, featuring modular `brain/` architecture, standardized IEEE SRS documentation for PDF export, cross-machine sync engine, and 3 streamlined prompts.

**Architecture:** Create modular, self-contained templates in `v2/templates/` (`CLAUDE.md`, `state.md`, `progress.md`, `sync.md`, `rules.md`, `SRS.md`) and 3 lightweight markdown prompts in `v2/prompts/` that embed these templates cleanly without bloating token budgets. Provide a top-level `v2/README.md` guide explaining usage.

**Tech Stack:** Markdown, Bash, Claude Code CLI conventions, ISO/IEC/IEEE 29148 documentation standards.

**Spec:** `docs/superpowers/specs/2026-10-07-project-system-v2-design.md`

## Global Constraints
- All v2 files must reside inside `/home/abdulrahman_abdulkarem/dev/project-system/v2/` without mutating existing v1 master files or prompts.
- Setup prompts must remain lean and self-contained (< 10 KB per prompt).
- Shortcuts must be exactly preserved: `wrap-up` (or `wrap up`), `catch-me-up`, `commit`, `plan`.
- Target projects must use a clean root (minimal 15-line `CLAUDE.md` pointer) and store internal context in `brain/`.
- SRS documentation must be a single file (`brain/documentation/SRS.md`) ready for one-step PDF conversion.

## Review Focus
1. Prompt isolation: Ensure prompts contain full instructions and templates without requiring access to `project-system` repo during runtime.
2. Shortcut exactness: Ensure `wrap-up`, `catch-me-up`, and `commit` behaviors match user requirements across all prompts.
3. Multi-device sync: Verify that `sync.md` handles branch tracking, `.env` additions, dependency installs, and database migrations properly.
4. Clean architecture rules: Verify rules strictly forbid premature abstractions, dead code, and direct database queries from UI.
5. Markdown formatting: Ensure SRS template uses clean GitHub Flavored Markdown suitable for direct pandoc/typst/AI PDF export.

---

### Task 1: Directory Setup & Root Pointer Template
- [ ] Create directory structure `v2/`, `v2/templates/`, `v2/prompts/`.
- [ ] Create `v2/templates/CLAUDE.md.template` (the minimal 15-line root pointer).
- [ ] Create `v2/templates/state.md.template` (frozen working memory snapshot for `catch-me-up`).
- [ ] Create `v2/templates/progress.md.template` (dated chronological changelog).

### Task 2: Sync Engine & Clean Architecture Rules Templates
- [ ] Create `v2/templates/sync.md.template` (cross-device handover tracking branch, `.env` variables, dependencies, migrations).
- [ ] Create `v2/templates/rules.md.template` (Hard security rules, feature-based clean architecture guidelines, and shortcuts: `catch-me-up`, `wrap-up`, `commit`, `plan`).

### Task 3: Professional SRS Documentation Template
- [ ] Create `v2/templates/SRS.md.template` (ISO/IEEE 29148 compliant System Requirements Specification with Executive Summary, Tech Matrix, Functional Modules, Data Dictionary, API Contracts, Security, and Deployment Guide).

### Task 4: Prompt 1 — Greenfield New Project Kickoff
- [ ] Create `v2/prompts/01-new-project-prompt.md`:
  - Interactive scope interview & stack recommendation.
  - Scaffolding of project structure & `.gitignore`.
  - Creation of root `CLAUDE.md` and public `README.md`.
  - Scaffolding of `brain/` (`state.md`, `progress.md`, `rules.md`, `sync.md`, `documentation/SRS.md`).
  - Active shortcut activation and final confirmation.

### Task 5: Prompt 2 — Brownfield Existing Project Adoption
- [ ] Create `v2/prompts/02-existing-project-prompt.md`:
  - Non-destructive codebase audit (detecting stack, conventions, existing docs).
  - Setup of root `CLAUDE.md` pointer.
  - Population of `brain/state.md` and initial reverse-engineered `brain/documentation/SRS.md`.
  - Hygiene verification (`.gitignore`, `.env.example`).
  - Active shortcut activation and final confirmation.

### Task 6: Prompt 3 — Multi-Device Sync & Machine Handover
- [ ] Create `v2/prompts/03-multidevice-sync-prompt.md`:
  - Dual-mode operation (Onboarding new machine vs. Resuming a switched session).
  - Environment reconciliation (checking `.env` diffs recorded in `sync.md`).
  - Automated dependency and migration checks.
  - Automated `catch-me-up` briefing.

### Task 7: V2 System Guide & Verification
- [ ] Create `v2/README.md` with a clean guide explaining when and how to copy-paste each prompt, how `catch-me-up` and `wrap-up` work, and how to export `SRS.md` to PDF.
- [ ] Review all prompts and templates for syntax, completeness, and consistency.
- [ ] Commit all v2 files to git.
