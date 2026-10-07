# Project System v2 — Modular Brain & Multi-Device Prompts

**Date:** 2026-10-07  
**Status:** In Review  
**Target Directory:** `/home/abdulrahman_abdulkarem/dev/project-system/v2/`

---

## 1. Executive Summary & Problem Statement

### The Problem in v1
The current prompt system in `/home/abdulrahman_abdulkarem/dev/project-system` compiled master files (`project-rules.md`, `project-checkpoints.md`, `rtl-guide.md`) into massive monolithic prompt files exceeding **87 KB (~1,100+ lines)**. Pasting this into Claude Code leads to:
1. **Context Exhaustion**: Upfront token flooding dilutes instructions, causing Claude to skip setup steps.
2. **Root Pollution**: 6+ tracking files dumped directly in the project root (`CLAUDE.md`, `PROGRESS.md`, `README.md`, `DESIGN.md`, `CHECKPOINTS.md`, `QA.md`).
3. **No Stakeholder Documentation**: Lack of a standardized, executive-ready specification (SRS) that can be shared with clients or converted into a PDF.
4. **Context Amnesia**: Developers returning to a project after weeks have to re-read everything from scratch because logs only capture past history rather than active mental state.
5. **Multi-Device Friction**: Switching between two development machines leads to environment drift (missing `.env` variables, pending migrations, uninstalled packages).

### The Solution in v2
Project System v2 re-architects the workflow into:
* **Lean Prompts (< 8 KB each)**: Highly targeted instructions without dumping encyclopedic checklists.
* **The `brain/` Directory**: All operational memory, rules, logs, and sync states are encapsulated inside `brain/`. The root contains only production code, a public `README.md`, and a minimal 15-line `CLAUDE.md` pointer.
* **Professional SRS (`brain/documentation/SRS.md`)**: An ISO/IEEE-aligned Software Requirements Specification formatted in clean Markdown, ready to be converted into an executive PDF by an AI agent anytime.
* **Active Working Memory (`brain/state.md`) & `catch-me-up`**: A frozen working snapshot that gives a 30-second briefing when returning after weeks.
* **Cross-Device Handover Engine (`brain/sync.md`)**: Tracks environment variables, migrations, package installations, and git state between Machine A and Machine B.
* **Strict Clean Architecture Rules**: Enforces feature-based modularity, separation of UI and business logic, zero dead code, and defensive security.

---

## 2. Target Project Architecture

Every project bootstrapped or adopted by v2 adheres to this structure:

```text
<project-root>/
├── CLAUDE.md                          # Minimal 15-line pointer for Claude Code auto-load
├── README.md                          # Public GitHub README (clean, client/public facing)
├── .gitignore
├── .env.example
├── src/ (or project code)             # Clean, feature-based source code
│
└── brain/                             # ALL INTERNAL COGNITIVE & SYSTEM STATE
    ├── state.md                       # Active working memory snapshot (for `catch-me-up`)
    ├── progress.md                    # Dated chronological session history
    ├── sync.md                        # Cross-machine sync state & handover checklist
    ├── rules.md                       # Security, clean architecture, and shortcut definitions
    └── documentation/
        └── SRS.md                     # Comprehensive, PDF-ready System Requirements Spec
```

---

## 3. Core Shortcuts & Workflow Specification

The user shortcuts are preserved and standardized:

### `catch-me-up` (or `catch me up`)
* **When to run**: At the start of any session, especially after days/weeks away, or after pulling on a second machine.
* **Procedure**:
  1. Read `brain/state.md` and `brain/sync.md`.
  2. Inspect git branch and recent commits (`git status`, `git log -n 3`).
  3. Deliver a concise 30-second briefing:
     * **System Overview**: 2 sentences on what the system does.
     * **Where We Stopped**: Last working state and in-flight changes.
     * **Multi-Device Check**: Flag any pending `.env` keys, package installs, or migrations noted in `sync.md`.
     * **Recommended Immediate Action**: Exact file and function to start with right now.

### `wrap-up` (or `wrap up`)
* **When to run**: At the conclusion of a work session before shutting down or switching machines.
* **Procedure**:
  1. Update `brain/state.md`: Freeze current progress, in-flight work, known bugs, and the first task for next time.
  2. Append a dated entry to `brain/progress.md`.
  3. If new features or architectural changes occurred, update `brain/documentation/SRS.md`.
  4. If public features or setup steps changed, update root `README.md`.
  5. Update `brain/sync.md` with:
     * Current branch and last commit.
     * Any new `.env` variables required on the other machine.
     * Any new dependencies installed or migrations executed.
  6. **Safety**: Touches documentation only; does **NOT** run git commit or push automatically.
  7. Confirm with a summary: *"Wrap-up complete. Ready for 'commit' or machine handover."*

### `commit`
* **When to run**: When ready to push changes to GitHub.
* **Procedure**:
  1. Stage changes (`git add`).
  2. Safety audit: inspect staged files for leaked secrets, `.env` files, large binaries, or stray build artifacts. If found, stop and flag immediately.
  3. Generate a conventional, descriptive commit message explaining the *why* and *what*.
  4. Commit and push to the active branch.
  5. Confirm in one line.

### `plan`
* **When to run**: Before implementing non-trivial features.
* **Procedure**:
  * Propose the approach and at least one rejected alternative with tradeoffs. Stop and await approval before touching code.

---

## 4. Documentation Specification (`brain/documentation/SRS.md`)

Structured according to ISO/IEC/IEEE 29148 standards for single-file PDF compilation:

1. **Document Header & Revision Table** (Document Version, Date, Status, Author)
2. **Section 1: Executive Summary & System Objectives** (Problem statement, target audience, core value proposition)
3. **Section 2: High-Level Architecture & Tech Stack** (Architecture style, technology matrix with rationales, component data flow)
4. **Section 3: Functional Requirements (Module by Module)** (Domain breakdown, user stories, business logic & validation rules)
5. **Section 4: Data Architecture & Entity Relationships** (Entity dictionary, relational schemas, asset/media storage policy)
6. **Section 5: API & Integration Surface** (Endpoints, contracts, webhooks, third-party services)
7. **Section 6: Security, Compliance & Data Protection** (Authentication, RBAC, input sanitization, rate limiting, secrets handling)
8. **Section 7: Deployment & Environment Operations** (Infrastructure, `.env` matrix, build/deploy commands)

---

## 5. The Three Master Prompts in `v2/`

### Prompt 1: `01-new-project-prompt.md` (Greenfield Setup)
* **Goal**: Scaffold a brand-new project from scratch.
* **Steps**:
  1. Interview user for project concept, propose stack with tradeoffs, agree on stack.
  2. Create clean project scaffolding and `.gitignore`.
  3. Create root `CLAUDE.md` pointer (15 lines).
  4. Create public `README.md`.
  5. Scaffold `brain/` directory (`state.md`, `progress.md`, `rules.md`, `sync.md`, `documentation/SRS.md`).
  6. Final confirmation: *"Setup complete — the shortcuts are active."*

### Prompt 2: `02-existing-project-prompt.md` (Brownfield Adoption)
* **Goal**: Integrate into an existing codebase without breaking or reverting any code.
* **Steps**:
  1. Scan codebase: stack, architecture, existing configs, environment variables.
  2. Verify safety: do NOT delete, rewrite, or overwrite existing application code.
  3. Create or merge root `CLAUDE.md` pointer.
  4. Scaffold `brain/` directory. Reverse-engineer existing code to populate baseline `SRS.md` and current `state.md`.
  5. Check `.gitignore` and `.env.example` hygiene.
  6. Final confirmation: *"Setup complete — the shortcuts are active."*

### Prompt 3: `03-multidevice-sync-prompt.md` (Cross-Device Handover)
* **Goal**: Enable working across two machines (e.g. Laptop & Desktop) with zero context or environment drift.
* **Dual Operation**:
  * **Onboarding a New Machine**: Pulls repo, inspects `brain/sync.md`, identifies missing `.env` keys, runs necessary package installs and database migrations, tests project run.
  * **Switching Sessions**: Reads `brain/sync.md` and `brain/state.md`, triggers `catch-me-up` briefing, and resumes coding immediately.

---

## 6. Directory Layout of `project-system/v2/`

```text
/home/abdulrahman_abdulkarem/dev/project-system/v2/
├── README.md                          # Quickstart guide for using v2 prompts
├── prompts/
│   ├── 01-new-project-prompt.md       # Greenfield kickoff prompt
│   ├── 02-existing-project-prompt.md  # Existing project onboarding prompt
│   └── 03-multidevice-sync-prompt.md  # Multi-device sync & handover prompt
└── templates/
    ├── CLAUDE.md.template             # Root pointer template
    ├── state.md.template              # Working memory snapshot template
    ├── progress.md.template           # Historical changelog template
    ├── sync.md.template               # Cross-device sync engine template
    ├── rules.md.template              # Clean architecture & security rules
    └── SRS.md.template                # ISO/IEEE compliant system specification template
```

---

## 7. Verification & Testing Plan

1. **Prompt Dry-Run**: Verify each prompt against Claude Code constraints (token budget, clarity, unambiguous delimiters).
2. **Template Validation**: Ensure template variables (e.g. `[PROJECT_NAME]`, `[STACK]`) are consistent and self-documenting.
3. **SRS PDF Compatibility**: Verify that the generated `SRS.md.template` converts cleanly to PDF format with proper typography, markdown tables, and headers.
4. **Shortcut Consistency**: Verify that `wrap-up`, `catch-me-up`, and `commit` work symmetrically across all templates.
