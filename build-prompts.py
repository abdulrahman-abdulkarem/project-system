#!/usr/bin/env python3
"""
build-prompts.py — regenerates the setup prompts from the master files.

This is what "sync prompts" runs. Edit project-rules.md or project-checkpoints.md,
then run this. Never hand-edit the rules or checkpoints inside a prompt file:
they are generated regions and will be overwritten.

Usage:  python build-prompts.py
"""

import re
import pathlib

HERE = pathlib.Path(__file__).parent
MASTERS = HERE / "masters"
OUT = HERE / "prompts"

BEGIN = "# GENERATED BLOCK BEGINS"
END = "# GENERATED BLOCK ENDS"


def extract(filename):
    """Pull the generated region out of a master file.

    Skips the whole comment banner after the BEGIN marker, however many lines
    it runs to — an earlier version skipped a fixed count and leaked stray
    comment lines into the built prompts.
    """
    text = (MASTERS / filename).read_text(encoding="utf-8")
    i = text.index("\n", text.index(BEGIN)) + 1
    while i < len(text) and text[i] == "#":
        i = text.index("\n", i) + 1
    stop = text.rindex("# " + "=" * 67, 0, text.index(END))
    return text[i:stop].strip("\n")


RULES = extract("project-rules.md")
CHECKS = extract("project-checkpoints.md")

# ---------------------------------------------------------------------------
# Shared step fragments
# ---------------------------------------------------------------------------

CONVENTION = """Important: In the steps below, any content between "=== FILE START ===" and "=== FILE END ===" is the content to put INSIDE that file. Everything else is an instruction for you. Do not confuse the two."""

README_BODY = """=== FILE START ===
# [Project Name]

[One or two sentence description of what the project does and who it's for.]

## Features
- [Key feature]
- [Key feature]

## Tech Stack
- [The technologies, frameworks, and services used.]

## Getting Started

### Prerequisites
Everything someone needs installed before running the project, with versions where relevant. For example:
- [Runtime, e.g. Node.js v20+]
- [Package manager]
- [Any required CLI, database, or external service]

### Installation
1. Clone the repository:
   git clone [repo-url]
2. Install dependencies:
   [install command]
3. Set up environment variables:
   Copy .env.example to .env and fill in the required values.
4. [Any database setup / migration step]
5. Run the project:
   [run command]

### Environment Variables
List each required variable name and what it's for — never real values. See .env.example.

## Project Structure
[Brief overview of the main folders and what they contain.]

## Usage
[How to use the project once running — key flows or commands.]

## Scripts
[Available package scripts and what each does, if applicable.]

## License
[License, or "Private project" if not open source.]
=== FILE END ==="""

DESIGN_STEP_NEW = """Do this BEFORE building any UI. Skipping it is the main reason AI-built interfaces come out generic — with no decided point of view, the default is a templated look.

Settle these with me, then write them into DESIGN.md at the project root:

1. **Language and reading direction.** Ask me the primary language(s) and which of these three the project is — it drives layout, not just translation, and it decides how much of the language checkpoint applies:
   - **Single-direction LTR** (English or similar only). Still build with logical properties rather than hardcoded left/right, so adding a language later is a translation job and not a rewrite.
   - **Single-direction RTL** (Arabic or similar only). Treat RTL as the native layout direction, never as a mirrored afterthought.
   - **Bilingual / multi-directional.** One component set must serve both directions — no mirrored duplicates. Settle now: the default and fallback locale, the URL strategy (`/ar`, `/en`, subdomain), where the language switcher lives, and how `dir`/`lang` change on switch.
   - For every non-Latin script: confirm which font actually serves it, and VERIFY it is loaded by a real font loader — a CSS variable referencing a font does not mean the font exists. These fonts are heavy, so decide weights and subsetting deliberately. In bilingual projects, tune each script's size and weight separately; the same nominal size rarely looks balanced across two scripts.
   - Record the answer in DESIGN.md — the language checkpoint reads it to know which parts to run.

2. **Direction, from three inputs.** Don't propose a look in a vacuum — gather:
   - **References**: ask me for 2–3 sites/products whose look I admire.
   - **Mood**: ask me how it should feel in a few words (e.g. trustworthy, playful, premium, utilitarian).
   - **Options**: propose a small number of concrete directions with reasoning, and let me pick or combine.

3. **Anti-references.** Ask what I explicitly do NOT want, including any past attempt that was rejected and why. Record it — knowing what to avoid is as useful as knowing what to aim for.

4. **Register.** Is this primarily a product surface (workflows, task completion) or a brand surface (visual storytelling), or a split? This decides whether clarity or expression wins when they conflict, and it governs how much motion is appropriate.

5. **Approved Sources.** Decide, and record in DESIGN.md, where each kind of visual material comes from for this project. This list is what lets you ASK me for material instead of inventing it — name the source and the search terms, and I'll fetch it. Cover at minimum:
   - **Icons** — pick ONE set and use it everywhere. Never mix two icon systems, never use emoji as icons.
   - **Motion** — the animation source, if any.
   - **Component patterns** — where to look when a specific block is needed.
   - **Backgrounds / texture** — how depth is achieved.
   - **Type** — the font families and where they load from.
   Record for each: what it's for, the URL, and any licence constraint. If a project needs something this list doesn't cover, ask before choosing.

6. **Write DESIGN.md** documenting the ACTUAL system: color roles, typography scale, spacing, radii, elevation, and key components. Name the rules that follow from the direction (e.g. a single accent color for all interactive elements, elevation only on interaction). Document what the code really does, not what it aspires to — and flag any gaps you find.

Design tooling: if a design skill/plugin is available in this environment (for example an installed design plugin with init/critique/polish commands), use it to run this step and to review UI later. If not, do the above manually. Either way DESIGN.md is the source of truth and is committed alongside the other docs.

Browser access: check whether Chrome DevTools MCP is configured for this project (a `chrome-devtools` entry in `.mcp.json`). If it isn't, tell me — it is what lets you screenshot, read the console, inspect computed styles, read the accessibility tree, and record performance traces yourself instead of asking me for every check. Setup is one entry:

    {"mcpServers": {"chrome-devtools": {"command": "npx", "args": ["-y", "chrome-devtools-mcp@latest", "--isolated"]}}}

Ask before adding it — it is a new dependency."""

DESIGN_STEP_EXISTING = """Only if this project has a UI. The goal here is to DOCUMENT the design system that already exists, not to impose a new one — the same "going forward only" rule applies.

1. **Read the actual styles.** Go through the existing components, theme/config, and stylesheets and extract what is really in use: color roles, typography scale, spacing, radii, elevation, and the recurring component patterns.

2. **Language and reading direction.** Determine from the code which of these the project is: single-direction LTR, single-direction RTL, or bilingual/multi-directional. Then VERIFY the font for each script in use is genuinely loaded by a real font loader — a CSS variable referencing a font does not mean the font exists, and a missing non-Latin font falls back silently. Flag it if it is not. If the project is bilingual, also note whether one component set serves both directions or whether mirrored duplicates have crept in. Record the answer in DESIGN.md — the language checkpoint reads it to know which parts apply.

3. **Ask me for direction only where the code is ambiguous or inconsistent.** If two patterns solve the same problem, show me both and ask which is canonical rather than picking one silently.

4. **Register.** Ask whether this is primarily a product surface (workflows, task completion) or a brand surface (visual storytelling). This governs how much motion is appropriate.

5. **Approved Sources.** Identify what the project already uses for icons, motion, component patterns, backgrounds, and type, and record it in DESIGN.md as the Approved Sources list — this is what lets you ASK me for material instead of inventing it. If more than one icon set is in play, or emoji are being used as icons, flag it — don't fix it unless I ask.

6. **Write DESIGN.md** describing what the code ACTUALLY does, not what it aspires to. List the inconsistencies and gaps you found as an explicit section at the end, so I can decide what to fix later.

Design tooling: if a design skill/plugin is available in this environment (for example an installed design plugin with init/critique/polish commands), use it for this step and for UI review later."""

STACK_RULES_STEP = """- Add a "Stack-Specific Rules" subsection inside the Project Rules section of CLAUDE.md.
- Fill it with concrete best practices for the stack actually in use (framework conventions, security specifics, data and storage patterns, performance practices) — same spirit as the general rules, but specific to these technologies."""

CHECKPOINTS_STEP = """Create CHECKPOINTS.md at the project root, containing the FULL "PROJECT CHECKPOINTS" section from the very bottom of this message, verbatim.

This file holds the procedures run on demand by the checkpoint shortcuts ("review", "test check", "rtl check", "perf pass", "motion check", "ship check"). It deliberately does NOT go into CLAUDE.md — it is read only when a shortcut fires, so it never consumes session context it isn't needed for. Commit it alongside the other docs."""

GIT_HYGIENE_NEW = """- Create a proper .gitignore appropriate to the stack BEFORE the first commit (some scaffolding tools generate one — extend it rather than duplicating it). It must exclude: .env and all env variants (except .env.example), dependency folders (e.g. node_modules), build/dist output, OS files (.DS_Store), editor folders (.vscode, .idea), logs, and any credentials or keys.
- Create a .env.example listing every required variable NAME with empty or dummy values. Never put real secrets in it.
- Never commit secrets, API keys, tokens, or credentials. If you ever spot one in the code, stop and warn me immediately."""

GIT_HYGIENE_EXISTING = """- Check the existing .gitignore. Make sure it excludes: .env and all env variants (except .env.example), dependency folders (e.g. node_modules), build/dist output, OS files (.DS_Store), editor folders (.vscode, .idea), logs, and any credentials or keys. Add anything missing — don't remove existing entries.
- Make sure a .env.example exists listing every required variable NAME with empty or dummy values, based on the variables the code actually uses. Create it if missing.
- If you spot any secret already committed in the codebase or its history, STOP and warn me immediately."""

VOCAB = """## Your command vocabulary

**Every session**
- **"wrap up"** (or "done for today" / "let's wrap") — updates PROGRESS.md, CLAUDE.md, README.md and DESIGN.md as needed. No git actions.
- **"commit"** — reviews what's staged, then commits and pushes with a proper message. (Or do it yourself in GitHub Desktop.)

**While working**
- **"plan"** — outlines the approach and waits for your go-ahead before writing code.
- **"Q&A"** / **"Q&A short"** — consult mode: answers without touching code, logs to QA.md. **"Q&A history"** shows past consults.

**Checkpoints** (each loads its procedure from CHECKPOINTS.md and reports without fixing)
- **"review"** — reviews the current uncommitted changes against the review checklist.
- **"test check"** — checks test coverage against the testing standards.
- **"schema check"** — reviews the data model before it hardens.
- **"lang check"** / **"rtl check"** / **"a11y check"** — reading-direction, i18n and accessibility audit.
- **"perf pass"** — the performance checklist, Lighthouse baseline first.
- **"motion check"** — the motion decision table and its guardrails.
- **"ship check"** — the pre-deploy checklist."""

def claude_md(body):
    return "=== FILE START ===\n" + body + """

## Project Rules
[Paste the FULL "PROJECT RULES" section (everything under the PROJECT RULES banner below) into here verbatim, so it loads every session.]
=== FILE END ==="""


# ---------------------------------------------------------------------------
# Prompt definitions
# ---------------------------------------------------------------------------

PROMPTS = []

# --- 1. New project, single device -----------------------------------------

PROMPTS.append(dict(
    filename="new-project-kickoff-prompt.md",
    header="""# New Project Kickoff Prompt for Claude Code

> Paste everything inside the code block below into Claude Code at the very start of a new project.
> It sets up your context files, project structure, and a permanent set of rules embedded into CLAUDE.md
> so the rules persist across every future session.
>
> This prompt is stack-agnostic — it works for any project (web, API, automation, etc.).
> Claude Code will discuss the stack with you and add stack-specific rules once you settle on it.
>
> Generated from project-rules.md + project-checkpoints.md — do not edit the rules or checkpoints
> below by hand. Edit the masters and run build-prompts.py ("sync prompts").""",
    intro="""You are setting up a new project. Follow the setup steps below in order, then follow the embedded PROJECT RULES for the entire lifetime of the project.""",
    steps=[
        ("Understand the project and choose the stack", """Start here, before creating anything. The stack determines the folder structure, .gitignore, and tooling, so it's decided first.
- Ask me what the project is and what it needs to do.
- Based on that, recommend the best-suited stack — frontend, backend, database, hosting, and any key services — explaining the tradeoffs and why each choice fits this specific project. Don't just list options; give a reasoned recommendation.
- Weigh factors like project type, scale, performance needs, my familiarity, cost, and long-term maintainability.
- Go back and forth with me until we settle on the final stack together."""),
        ("Create the context files", """Create three files at the project root, filled in with the real project and stack details we just settled on (not placeholders, except for things genuinely not known yet).

### File 1: CLAUDE.md
This file holds permanent project context AND the project rules, so it loads into every future session.

""" + claude_md("""# Project: [project name]

## Summary
[One paragraph — what the project does, who it's for, and why it exists.]

## Tech Stack
[The stack we agreed on — frameworks, database, hosting, key services.]

## Architecture
[Document the folder structure and what lives where. Keep updated as it grows.]

## Key Decisions
[Log important choices and the reasoning behind them as they happen — starting with why we chose this stack.]

## Conventions
[Naming, code style, patterns to follow and avoid.]

## Environment Setup
[Runtime version, install command, copy .env.example to .env, any local services.]""") + """

### File 2: PROGRESS.md

=== FILE START ===
# Progress Log

## Open / Next up
- [ ] [current tasks]

---

## [today's date] — Setup
- Initialized project, chose stack, set up structure and tooling
- [summary of what we set up]
=== FILE END ===

### File 3: README.md
A clean, professional README suitable for presenting publicly on GitHub. Keep it accurate to the actual project — never invent features. The setup sections must be complete enough that anyone (or me on a fresh machine) can clone and run the project from scratch.

""" + README_BODY),
        ("Establish a clean project structure", """Set up a clean, scalable folder structure appropriate to the chosen stack. Separate concerns clearly (UI, business logic, data access, utilities, config) — do not dump everything into one folder. Document the structure in CLAUDE.md under Architecture and in README.md under Project Structure."""),
        ("Git and secrets hygiene", GIT_HYGIENE_NEW),
        ("Add stack-specific rules", STACK_RULES_STEP),
        ("Establish design direction (skip if this project has no UI)", DESIGN_STEP_NEW),
        ("Create CHECKPOINTS.md", CHECKPOINTS_STEP),
        ("Confirm", """Give me a short summary of what you set up — the stack, structure, and files — then confirm: "Setup complete — the shortcuts are active." Wait for my next instruction before starting to build."""),
    ],
    footer="""## How to use this
1. Copy everything inside the code block above.
2. Paste it into Claude Code as your first message in a brand-new project.
3. It discusses the project and the best-fit stack with you first.
4. Once the stack is settled, it creates the context files, sets up a stack-appropriate structure and tooling, and adds stack-specific rules.
5. If the project has a UI, it works out the design direction with you and writes DESIGN.md.
6. It writes CHECKPOINTS.md, then summarizes what it set up — and you start building.

""" + VOCAB,
))

# --- 2. Existing project ----------------------------------------------------

PROMPTS.append(dict(
    filename="existing-project-setup-prompt.md",
    header="""# Existing Project Setup Prompt for Claude Code

> Use this when a project is ALREADY underway and you want to add the context files,
> rules, checkpoints and shortcuts to it.
>
> Paste everything inside the code block below into Claude Code while inside the existing project.
>
> Generated from project-rules.md + project-checkpoints.md — do not edit the rules or checkpoints
> below by hand. Edit the masters and run build-prompts.py ("sync prompts").""",
    intro="""This project is already underway. Set it up with context files, rules, checkpoints, and shortcuts WITHOUT disrupting the existing code. Follow the steps below, then follow the embedded PROJECT RULES for the rest of the project's life.

Also important: The PROJECT RULES apply GOING FORWARD only. Do NOT refactor, rewrite, or "fix" existing code to match them unless I explicitly ask. Your job right now is to document what exists and set up the workflow — not to change the codebase. Fill the files with REAL details discovered from the actual code, not placeholders. If something isn't clear from the code, ask me instead of guessing.""",
    steps=[
        ("Scan the codebase", """Read through the project to understand its stack, architecture, folder structure, conventions, and any notable quirks. You'll use this to fill in the files below accurately. Note anything that looks intentional-but-odd so it can be recorded rather than "fixed" later."""),
        ("Create the context files", """Create three files at the project root, filled with real details from the scan.

### File 1: CLAUDE.md
Holds permanent project context AND the project rules, so it loads into every future session.

""" + claude_md("""# Project: [actual project name]

## Summary
[One paragraph — what this project does, who it's for, and why it exists.]

## Tech Stack
- Language / Framework: [actual]
- Database: [actual]
- Hosting / Infra: [actual]
- Key libraries: [actual]

## Architecture
[Brief overview of the existing structure — key folders and what lives where.]

## Key Decisions
[Important choices evident in the codebase and the reasoning behind them, where known.]
- **[Decision]**: [Why it was made / what it favors. Ask me if the reasoning isn't clear.]

## Conventions
[The naming, code style, and patterns ALREADY used in this codebase — describe what's there, don't impose new ones.]

## Environment Setup
- Runtime / version requirements: [actual]
- Install command: [actual]
- Copy .env.example to .env and fill in values
- Any local services needed: [actual]

## Things Claude Code Should Know
- [Codebase quirks]
- [Things that look wrong but are intentional]
- [Fragile areas needing extra care]""") + """

### File 2: PROGRESS.md

=== FILE START ===
# Progress Log

## Open / Next up
- [ ] [current tasks]
- [ ] Blocked: [anything blocking, if applicable]

---

## [today's date] — Project context setup
- Added CLAUDE.md, PROGRESS.md, README.md, CHECKPOINTS.md and project rules
- Current state of the project: [short summary of where things stand]
=== FILE END ===

### File 3: README.md
A clean, professional README suitable for presenting publicly on GitHub, accurate to what the project actually is. The setup sections must be complete enough that the project can be cloned and run from scratch on either device.

""" + README_BODY),
        ("Git and secrets hygiene", GIT_HYGIENE_EXISTING),
        ("Add stack-specific rules", STACK_RULES_STEP),
        ("Document the design system (skip if this project has no UI)", DESIGN_STEP_EXISTING),
        ("Create CHECKPOINTS.md", CHECKPOINTS_STEP),
        ("Commit the setup", """Once the files are created and the scan-based details are filled in:
- Stage the new files (CLAUDE.md, PROGRESS.md, README.md, CHECKPOINTS.md, DESIGN.md if created, and any .gitignore/.env.example changes).
- Review what's staged before committing. If anything looks like it shouldn't be there — a secret, a large binary, an env file — STOP and flag it.
- Commit with the message: "Add project context files, rules, checkpoints, and README".
- Push to GitHub.

This first push is intentional so both devices immediately have the new files. After this, commits follow the "commit" shortcut (not automatic)."""),
        ("Confirm", """Give me a short summary of what you set up and what you learned about the project. If anything was unclear during the scan and you had to make assumptions, list them so I can correct them. Then confirm: "Setup complete — the shortcuts are active." """),
    ],
    footer="""## How to use this
1. Open the existing project in Claude Code (on either device).
2. Copy everything inside the code block above and paste it as your message.
3. It scans the codebase, creates the files with real details, fixes gitignore/.env.example if needed, documents the existing design system, writes CHECKPOINTS.md, then commits and pushes the setup.
4. It reports what it set up and any assumptions it made — correct anything that's off.

""" + VOCAB,
))

# --- 3. Repair / finish an interrupted setup --------------------------------

PROMPTS.append(dict(
    filename="repair-setup-prompt.md",
    header="""# Repair / Finish Setup Prompt for Claude Code

> Use this when you pasted a kickoff prompt but the setup didn't finish properly —
> e.g. you jumped into giving the stack and tasks, real work got done, and the "wrap up"
> shortcut doesn't work (because CLAUDE.md never got the rules embedded).
>
> This finishes the setup correctly using whatever already exists, WITHOUT deleting or
> undoing any of your current work. Paste everything inside the code block below into
> Claude Code inside the project.
>
> Generated from project-rules.md + project-checkpoints.md — do not edit the rules or checkpoints
> below by hand. Edit the masters and run build-prompts.py ("sync prompts").""",
    intro="""The setup for this project was started but not finished correctly. There is already real work in this project, and some setup files (CLAUDE.md, PROGRESS.md, and/or README.md) may already exist partially. Your job is to FINISH and FIX the setup as described below.

CRITICAL — do not destroy existing work:
- Do NOT delete, reset, or revert any of my existing code or project work.
- Do NOT overwrite my existing files wholesale. If a file already exists, READ it first and MERGE — keep what's good, fill in what's missing, fix what's wrong. Only create a file from scratch if it doesn't exist.
- If anything is ambiguous or you're unsure whether something is intentional, ASK me instead of guessing or changing it.""",
    steps=[
        ("Take stock of the current state", """- Scan the codebase to understand the current stack, architecture, folder structure, conventions, and what has been built so far.
- Check whether CLAUDE.md, PROGRESS.md, README.md, DESIGN.md, CHECKPOINTS.md, .gitignore, and .env.example already exist, and note what each currently contains.
- Give me a short summary of what you found and what's missing or incomplete, BEFORE changing anything."""),
        ("Reconcile / complete CLAUDE.md", """Make sure CLAUDE.md exists at the project root and contains all of the sections below, filled in with REAL details from the current project. Merge into the existing file if there is one — don't discard content that's already accurate.

The most important fix: the full "PROJECT RULES" section (everything under the PROJECT RULES banner further below) MUST be embedded into CLAUDE.md verbatim. This is what makes the shortcuts work — they likely failed before because these rules were never in CLAUDE.md.

""" + claude_md("""# Project: [actual project name]

## Summary
[One paragraph — what the project does, who it's for, and why it exists.]

## Tech Stack
[The actual stack in use — frameworks, database, hosting, key services.]

## Architecture
[The actual folder structure and what lives where.]

## Key Decisions
[Important choices made so far and the reasoning, including the stack choice.]

## Conventions
[The naming, code style, and patterns already used in this codebase.]

## Environment Setup
[Runtime version, install command, how to create the local env file, any local services.]""")),
        ("Reconcile / complete PROGRESS.md", """Make sure PROGRESS.md exists with the structure below. If it already exists, keep its history and just make sure the format matches and the current state is captured. If it doesn't exist, create it and record everything done so far as the first entries (reconstruct from the code and from what you know of this session).

=== FILE START ===
# Progress Log

## Open / Next up
- [ ] [current open tasks]

---

## [today's date] — Setup finished + progress so far
- [Summary of what has already been built in the project up to now]
- Completed project setup: context files, rules, checkpoints, structure docs
=== FILE END ==="""),
        ("Reconcile / complete README.md", """Make sure README.md exists and is accurate to the actual project, with complete setup instructions (prerequisites, install steps, environment variables, scripts) so the project can be cloned and run from scratch. Merge with any existing README — don't wipe good content.

""" + README_BODY),
        ("Git and secrets hygiene (only fix what's missing)", GIT_HYGIENE_EXISTING),
        ("Add stack-specific rules", STACK_RULES_STEP),
        ("Reconcile DESIGN.md (skip if this project has no UI)", DESIGN_STEP_EXISTING),
        ("Create CHECKPOINTS.md", CHECKPOINTS_STEP),
        ("Confirm", """- Summarize what you completed or fixed, and list anything you merged or any assumptions you made so I can correct them.
- Explicitly confirm: "Setup is now complete — the shortcuts are active." so I know the system is live.
- Do NOT commit anything yet — wait for me to say "commit" or to do it myself."""),
    ],
    footer="""## After running this
- The setup is now complete and the shortcuts are live.
- Tip for next time: let the kickoff prompt finish ALL its setup steps (it ends with a "Setup complete" confirmation) BEFORE you start giving it tasks or using shortcuts.

""" + VOCAB,
))


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build(p):
    parts = [p["header"], "", "---", "", "```", p["intro"], "", CONVENTION, ""]

    for i, (title, body) in enumerate(p["steps"], start=1):
        parts.append(f"## STEP {i} — {title}")
        parts.append("")
        parts.append(body)
        parts.append("")

    parts.append(RULES)
    parts.append("")
    parts.append(CHECKS)
    parts.append("```")
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append(p["footer"])

    text = "\n".join(parts).rstrip() + "\n"
    (OUT / p["filename"]).write_text(text, encoding="utf-8")
    return len(text)


if __name__ == "__main__":
    print("Regenerating prompts from masters...\n")
    for p in PROMPTS:
        size = build(p)
        print(f"  {p['filename']:<40} {size:>7,} chars")
    print("\nDone. The rules and checkpoints in every file are now identical.")
