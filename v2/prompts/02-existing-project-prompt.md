# Prompt 02: Brownfield Existing Project Adoption

> **When to use:** Paste this into Claude Code inside an existing project that already has code written, but lacks the `brain/` context system, rules, and SRS documentation.  
> **What it does:** Safely audits the codebase without deleting or altering any existing code, sets up the root `CLAUDE.md` pointer, reverse-engineers the existing architecture into a professional PDF-ready SRS document, and initializes `brain/` memory and shortcuts.

---

```markdown
You are adopting an existing codebase into a professional, modular project system. Your goal is to establish the `brain/` cognitive architecture, create a comprehensive System Requirements Specification (SRS) by analyzing the existing code, and activate session shortcuts.

CRITICAL SAFETY DIRECTIVE:
- Do NOT delete, rewrite, or reset any existing application code or database files.
- Do NOT overwrite existing documentation blindly. If a file (like README.md) already exists, read it first and preserve all accurate information.
- All internal operational files belong inside `brain/`.

Follow these steps in order:

---

### STEP 1 — Non-Destructive Codebase Audit
Scan the project to understand what currently exists:
1. Identify the tech stack by reading package manifests (`package.json`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, etc.), configs, and dependencies.
2. Inspect the directory tree to identify architectural patterns, existing modules, database schemas, and entry points.
3. Check for existing documentation, `.gitignore`, and `.env.example`.
4. Provide me with a concise 5-bullet summary of what you discovered:
   - Framework & Language
   - Database / ORM & Storage
   - Main Architectural Modules
   - Current Completion State
   - Any immediate hygiene issues (e.g. unignored secrets)

---

### STEP 2 — Setup Root CLAUDE.md Pointer
Create or update `CLAUDE.md` at the project root. If an existing `CLAUDE.md` exists, preserve any project-specific commands and prepend/append this standard pointer:

=== FILE START ===
# [Project Name]

> **Stack:** [Discovered Stack]  
> **Environment:** Runtime [Discovered Version], package manager [npm/pnpm/pip]

---

## System Architecture & Cognitive Engine
All operational memory, engineering rules, and system documentation live in the `brain/` directory.

- **On session start**: Always read `brain/state.md` and `brain/rules.md` before taking actions.
- **Active Shortcuts**:
  - `catch-me-up` : Read `brain/state.md` + `brain/sync.md`, inspect git, and provide a 30-second context briefing.
  - `wrap-up`     : Update `brain/state.md`, `brain/progress.md`, `brain/sync.md`, and `brain/documentation/SRS.md` before finishing work.
  - `commit`      : Audit staged changes for secrets/temp files, generate a descriptive commit message, and push to GitHub.
  - `plan`        : Outline approach + rejected alternative before coding non-trivial changes.
=== FILE END ===

---

### STEP 3 — Reconcile Git & Secrets Hygiene
1. Check `.gitignore`. Ensure `.env`, `.env.*.local`, dependencies (`node_modules`, `venv`), and build directories are strictly excluded. If missing, append them.
2. Check `.env.example`. Ensure every environment variable referenced in the code is documented with a placeholder key.

---

### STEP 4 — Scaffold the `brain/` Cognitive Engine
Create the `brain/` directory and populate the 5 internal operational files using the discoveries from Step 1:

#### File 1: `brain/state.md` (Active Working Memory for `catch-me-up`)
Reconstruct current state from the codebase:
- **System Snapshot:** 2-3 sentence overview of what the application does.
- **Where We Stopped:** The most recently edited files or latest feature visible in git.
- **In-Flight Work:** Any partial implementations, unhandled TODOs, or open bugs found in the code.
- **Immediate Next Step:** Recommended next action to continue development.

#### File 2: `brain/progress.md` (Changelog)
Create `brain/progress.md` with an initial entry:
- Date: [Today's Date] — Project Adoption & Brain Initialization
- Summary of existing features and modules cataloged during onboarding.

#### File 3: `brain/sync.md` (Cross-Device Sync State)
- Current branch, commit hash, required `.env` variables from `.env.example`, and package install commands.

#### File 4: `brain/rules.md` (Clean Architecture & Shortcuts)
=== FILE START ===
# Project Operational Rules & Standards (`rules.md`)

## 1. 🛡️ HARD SECURITY RULES (Never Violate)
1. **Never Commit Secrets**: Never commit `.env` files, API keys, private tokens, or credentials.
2. **Media Storage**: Never store media files directly in database tables; upload to object storage and store URLs only.
3. **Destructive Actions**: Never drop tables, reset databases, delete files wholesale, or force-push without explicit, written confirmation.
4. **Server-Side Authority**: Enforce authentication, role permissions (RBAC), and input sanitization on the server.
5. **No Leaked Internals**: Never return raw database errors or server stack traces to client responses.
6. **No Unapproved Dependencies**: Always ask before installing new packages or restructuring core directories.

## 2. 🏛️ CLEAN ARCHITECTURE & PROFESSIONAL CODE STANDARDS
1. **Feature/Domain Modularity**: Group code by domain/feature. Avoid flat dumping of dozens of files into generic directories.
2. **Strict Layer Separation**: UI components must focus on presentation. Data access and business logic live in separate service/repository layers.
3. **Zero Dead Code & Speculative Wrappers**: No speculative helper functions. Clean up unused imports, dead functions, and commented-out code.
4. **Data Validation & Type Safety**: Validate all external inputs with schema validators (e.g. Zod, Pydantic). Avoid `any` types.
5. **Single Source of Truth**: Centralize constants, configs, and design tokens.

## 3. ⚡ SESSION SHORTCUTS WORKFLOW

### `catch-me-up` (or `catch me up`)
- Read `brain/state.md` and `brain/sync.md`.
- Inspect git status and recent commits (`git log -n 3`).
- Output a concise 30-second briefing:
  - **Project Snapshot:** 2-sentence reminder of project purpose.
  - **Where We Stopped:** Last completed feature & active branch.
  - **Cross-Device Status:** Flag any pending `.env` keys, package installs, or migrations from `sync.md`.
  - **Immediate Next Step:** Exact file, function, and task to start right now.

### `wrap-up` (or `wrap up`)
- Freeze working memory in `brain/state.md`: Update where we stopped, in-flight work, and the exact next step.
- Append a dated summary to `brain/progress.md`.
- If new features or architectural changes occurred, update `brain/documentation/SRS.md`.
- If public features or setup steps changed, update root `README.md`.
- Update `brain/sync.md` with current branch, commit, required `.env` variables, and dependency/migration commands.
- **Safety:** Updates documentation only. Does NOT automatically commit or push to git.
- Confirm with a summary: *"Wrap-up complete. All brain state updated. Ready for 'commit' or device switch."*

### `commit`
- Run `git status` and stage files.
- Audit staged files: Ensure no `.env`, secrets, large binaries, or temp artifacts are staged.
- Generate a concise, conventional commit message reflecting real changes.
- Commit and push to origin.
- Confirm with commit hash and pushed branch.

### `plan`
- Propose implementation strategy and at least one rejected alternative with tradeoffs.
- Stop and wait for user approval before writing code.
=== FILE END ===

#### File 5: `brain/documentation/SRS.md` (Reverse-Engineered Specification — PDF Ready)
Create `brain/documentation/SRS.md` by reverse-engineering the codebase. Include:
1. **Document Header:** Version 1.0.0, status, date.
2. **Executive Summary:** Synthesize the business purpose from the codebase and existing readme.
3. **Architecture & Tech Stack Matrix:** Catalog all discovered frameworks, databases, and libraries with their exact roles.
4. **Functional Requirements:** Group discovered features into domain modules with capability tags (`FR-1.1`, `FR-2.1`, etc.).
5. **Data Architecture:** Document discovered database schemas, tables, relationships, and asset storage policies.
6. **API & Integration Surface:** Document all discovered API endpoints, route handlers, and external services.
7. **Security & Deployment Guide:** Document auth flows, required `.env` keys, and run/build scripts.

---

### STEP 5 — Confirmation & Readiness
1. Output a short summary of the discovered architecture, files created, and any assumptions made during reverse engineering.
2. Explicitly confirm:
   **"Setup complete — the shortcuts are active."**
```
