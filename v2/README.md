# Project System v2

A modular, clean setup-and-rules system for building software with Claude Code. Designed to eliminate prompt bloat, keep project roots spotless, synchronize seamlessly across two machines, and maintain an executive-ready System Requirements Specification (SRS) ready for instant PDF export.

---

## 🚀 Quickstart: Pick Your Prompt

When opening Claude Code, copy the entire markdown code block from the prompt file matching your situation:

| Situation | Prompt File | What It Does |
| :--- | :--- | :--- |
| **Brand-New Project** | `prompts/01-new-project-prompt.md` | Interviews on scope, chooses stack, scaffolds feature-based directories, sets up root `CLAUDE.md`, initializes `brain/` engine and baseline `SRS.md`. |
| **Existing Codebase** | `prompts/02-existing-project-prompt.md` | Audits code safely without altering existing application logic, reverse-engineers current features into `brain/documentation/SRS.md`, and activates shortcuts. |
| **Switching Machines** | `prompts/03-multidevice-sync-prompt.md` | Reconciles git, verifies missing `.env` variables and package dependencies from `sync.md`, runs a 30-second context briefing, and resumes coding. |

---

## 🧠 The `brain/` Architecture

In every project you build with v2, the project root remains 100% clean and professional. All internal cognitive and operational files live inside `brain/`:

```text
my-project/
├── CLAUDE.md                  <-- Minimal 15-line pointer (Claude Code auto-loads this)
├── README.md                  <-- Clean public GitHub README
├── .gitignore
├── .env.example
├── src/                       <-- Feature-based, clean application code
│
└── brain/                     <-- ALL INTERNAL COGNITIVE & SYSTEM MEMORY
    ├── state.md               <-- Frozen working memory snapshot (for `catch-me-up`)
    ├── progress.md            <-- Historical dated session changelog
    ├── sync.md                <-- Cross-device sync engine (.env diffs, migrations, git branch)
    ├── rules.md               <-- Security hard rules, clean architecture, and shortcuts
    └── documentation/
        └── SRS.md             <-- Standardized ISO/IEEE System Requirements Specification
```

---

## ⚡ Active Shortcuts Workflow

Typed directly in Claude Code chat during development:

### 1. `catch-me-up` (or `catch me up`)
* **When to use:** At the start of a session, especially after returning from days/weeks away, or after pulling on your second machine.
* **What it does:** Reads `brain/state.md` and `brain/sync.md`, checks git status, and delivers a **30-second briefing**:
  - Reminds you what the system does.
  - Summarizes where you stopped.
  - Warns of any missing `.env` keys or pending package installs.
  - Gives the exact file and line to start working on right now.

### 2. `wrap-up` (or `wrap up`)
* **When to use:** At the end of every work session or before switching to your other machine.
* **What it does:**
  - Freezes working memory into `brain/state.md`.
  - Appends a dated entry to `brain/progress.md`.
  - Updates `brain/documentation/SRS.md` if features or architecture changed.
  - Updates root `README.md` if public features or setup commands changed.
  - Updates `brain/sync.md` with git branch, commit hash, and any new `.env` variables.
  - **Safety:** Touches documentation only; does **NOT** auto-commit or push to git.

### 3. `commit`
* **When to use:** When you are ready to push changes to GitHub.
* **What it does:** Stages changes, performs a strict safety audit (stops immediately if any `.env`, secret, or large binary is staged), writes a descriptive conventional commit message, and pushes to origin.

### 4. `plan`
* **When to use:** Before starting any multi-step feature or architectural change.
* **What it does:** Outlines the proposed technical approach and at least one rejected alternative with tradeoffs, then waits for your approval before touching code.

---

## 📄 Converting `SRS.md` to PDF

Whenever a client, stakeholder, or manager asks: *"Can I have a document explaining the system?"*, follow these two steps:

1. Locate `brain/documentation/SRS.md`.
2. Give the file to an AI agent (or drop it into any markdown PDF tool like Typora, Pandoc, or Marp) with this instruction:
   > *"Convert this System Requirements Specification into a clean, executive-ready PDF. Use a professional title page, table of contents, clean typography, and neat tables."*

Because `SRS.md` is structured according to ISO/IEC/IEEE 29148 standards, it generates an enterprise-grade technical document with zero extra manual editing.
