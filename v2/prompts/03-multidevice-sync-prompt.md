# Prompt 03: Multi-Device Sync & Machine Handover

> **When to use:** Paste this into Claude Code when switching between two development machines (e.g., transitioning from your Desktop to your Laptop, or vice versa), or when setting up the project on a secondary machine for the first time.  
> **What it does:** Reconciles git status, audits local `.env` keys against `brain/sync.md` to prevent runtime crashes, verifies dependencies and migrations, executes an automated `catch-me-up` briefing, and registers the current machine as active.

---

```markdown
You are performing a multi-device synchronization and handover for this project. The project state was saved on another machine using `wrap-up`. Your objective is to ensure this machine is 100% in sync (code, environment variables, dependencies, and database migrations) and deliver a 30-second context briefing so coding can resume immediately.

Follow these steps in order:

---

### STEP 1 — Git & Sync State Verification
1. Inspect the local git status:
   - Run `git fetch` and check if there are upstream commits to pull.
   - If behind `origin`, alert me and ensure changes are safely pulled (`git pull`).
2. Read `brain/sync.md` to determine:
   - Which machine was active last.
   - The latest pushed branch and commit.
   - Any specific handover notes left by the previous session.

---

### STEP 2 — Environment & Secrets Reconciliation
Environment drift is the #1 cause of broken builds when switching machines:
1. Compare this machine's local `.env` file against `.env.example` and the "Environment & Secrets Reconciliation" section in `brain/sync.md`.
2. If any required environment variable is missing on this machine:
   - Stop and list the missing key(s) clearly.
   - Prompt me to supply the value or add it to my local `.env`.
   - Never display existing secret values in plaintext.

---

### STEP 3 — Dependencies & Database Migrations Check
1. Check package locks (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `requirements.txt`):
   - If commits pulled in Step 1 modified dependencies or if `brain/sync.md` marked dependencies required, run the install command (e.g. `npm install` / `pip install`) or instruct me to run it.
2. Check database migrations:
   - If new migration files were pulled, report them and ask to execute the migration command (e.g. `npx prisma migrate dev` / `npx drizzle-kit migrate`).

---

### STEP 4 — Context Recovery (`catch-me-up` Briefing)
Read `brain/state.md` and deliver an immediate 30-second briefing:

1. **🗺️ System Overview:** 2 sentences reminding me of the system purpose and current milestone.
2. **📍 Where the Previous Machine Stopped:** What feature or file was being worked on right before wrap-up.
3. **🚧 In-Flight Work & Gotchas:** Any half-done functions, failing tests, or open decisions.
4. **🎯 Immediate Next Step (Start Here):** The exact file, function, and task to touch first right now on this machine.

---

### STEP 5 — Update Sync State & Confirm Readiness
1. Update `brain/sync.md`:
   - Set **Last Active Machine** to this current machine (e.g. Machine-2 / Laptop).
   - Clear the pending handover checklist once resolved.
2. Confirm with:
   **"Machine handover complete — the shortcuts are active and ready to code."**
```
