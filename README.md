# Project System v2

A modular, clean setup-and-rules system for building software with Claude Code. Designed to eliminate prompt bloat, keep project roots spotless, synchronize seamlessly across two machines, and maintain an executive-ready System Requirements Specification (SRS) ready for instant PDF export.

---

## 🚀 Quickstart: Pick Your Prompt

When opening Claude Code, copy the entire markdown code block from the prompt file matching your situation:

| Situation | Prompt File | What It Does |
| :--- | :--- | :--- |
| **Brand-New Project** | `prompts/01-new-project-prompt.md` | Greenfield kickoff. Interviews on scope, chooses stack, scaffolds feature-based directories, sets up root `CLAUDE.md`, initializes `brain/` engine with ambient greeting and full PDF-ready `SRS.md`. |
| **Existing Codebase / v1 Upgrade** | `prompts/02-existing-project-prompt.md` | Brownfield onboarding & v1 upgrade. Audits code, auto-detects and upgrades v1 projects (cleaning root clutter & migrating history to `brain/`), builds `SRS.md`, and activates shortcuts. |
| **Switching Machines** | `prompts/03-multidevice-sync-prompt.md` | Multi-machine handover. Reconciles git, verifies missing `.env` variables and package dependencies from `sync.md`, runs a 30-second context briefing, and resumes coding. |
| **Exporting to PDF** | `prompts/04-export-srs-to-pdf-prompt.md` | Document publisher. Turns `brain/documentation/SRS.md` into an executive-styled HTML/PDF with cover page, table of contents, shaded tables, and Mermaid architecture diagrams. |

---

## 🧠 The `brain/` Architecture

In every project you build with v2, the project root remains 100% clean and professional. All internal cognitive and operational files live inside `brain/`:

```text
my-project/
├── CLAUDE.md                  <-- Minimal 20-line pointer (Auto-loaded: provides ambient greeting)
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
        └── SRS.md             <-- Standardized ISO/IEEE System Requirements Specification (with Mermaid)
```

---

## ⚡ Ambient Orientation & Shortcuts Workflow

### Ambient Orientation (Zero Typing Required)
Every time you open Claude Code, `CLAUDE.md` automatically directs Claude to read `brain/state.md` and greet you with a **2-line snapshot**:
> *"📍 Current Milestone: User Authentication & Profile Module*  
> *🎯 Immediate Next Step: Open `src/features/auth/login.tsx` line 42 to implement submission handler."*

Even if you forgot where you left off weeks ago, you are instantly oriented before typing a single command.

---

### On-Demand Shortcuts (Typed in Claude Code Chat)

#### 1. `catch-me-up` (or `catch me up`)
* **When to use:** When returning after long breaks or after pulling on your second machine.
* **What it does:** Delivers a comprehensive **30-second briefing**:
  - Reminds you of the full system purpose.
  - Summarizes where the previous session or machine stopped.
  - Warns of any missing `.env` keys or pending package installs.
  - Gives the exact file and line to start working on right now.

#### 2. `wrap-up` (or `wrap up`)
* **When to use:** At the end of every work session or before switching to your other machine.
* **What it does:**
  - Freezes working memory into `brain/state.md`.
  - Appends a dated entry to `brain/progress.md`.
  - Updates `brain/documentation/SRS.md` if features or architecture changed.
  - Updates root `README.md` if public features or setup commands changed.
  - Updates `brain/sync.md` with git branch, commit hash, and any new `.env` variables.
  - **Safety:** Touches documentation only; does **NOT** auto-commit or push to git.

#### 3. `commit`
* **When to use:** When you are ready to push changes to GitHub.
* **What it does:** Stages changes, performs a strict safety audit (stops immediately if any `.env`, secret, or large binary is staged), writes a descriptive conventional commit message, and pushes to origin.

#### 4. `plan`
* **When to use:** Before starting any multi-step feature or architectural change.
* **What it does:** Outlines the proposed technical approach and at least one rejected alternative with tradeoffs, then waits for your approval before touching code.

---

## 📄 Converting `SRS.md` to PDF

Whenever a client, stakeholder, or manager asks: *"Can I have a document explaining the system?"*, follow these steps:

1. Copy the prompt from `prompts/04-export-srs-to-pdf-prompt.md`.
2. Paste it into an AI chat (Claude, ChatGPT, or Gemini), appending the text of `brain/documentation/SRS.md`.
3. Save the resulting HTML file and open it in Chrome/Edge/Safari.
4. Press `Ctrl + P` (or `Cmd + P`) and select **"Save as PDF"**.

You get an executive-grade document featuring:
* Professional corporate cover page and confidentiality notice.
* Numbered Table of Contents.
* Modern typography and shaded data tables.
* Clean vector-rendered **Mermaid architecture & sequence diagrams**.
* Proper print pagination with zero cut-off headings.

---

## 🏛️ Legacy Version 1
The original v1 prompt-generator system is preserved intact in `v1/` for archival reference.

