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
RTL = extract("rtl-guide.md")

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

TOOLING_STEP = """Do this before building anything. Report what you can ACTUALLY see in this
environment — don't assume, and don't claim a tool is available because it usually is.

**1. Browser access — the one that matters most.**
Check for a `chrome-devtools` entry in `.mcp.json`. This is what lets you take screenshots,
read the console, inspect the live DOM and computed styles, read the accessibility tree, and
record performance traces yourself, instead of asking me to check every time. Without it you
are guessing about anything visual.

If it isn't configured, tell me, and offer this:

    {"mcpServers": {"chrome-devtools": {"command": "npx", "args": ["-y", "chrome-devtools-mcp@latest", "--isolated"]}}}

**2. Design tooling.** Tell me whether any design-oriented skill or plugin is loaded (something
offering init / critique / polish / audit style commands). If one is, you'll use it for the
design step and for reviewing UI later. If none is, say so — the design step still runs
manually, it just takes longer.

**3. Anything else you can see that's relevant to this stack.** Test runners, linters,
formatters, deployment CLIs. List what's present.

Then give me a short summary in three lines: what's available, what's missing, and what each
missing item would buy me. **Ask before installing or configuring anything** — adding a
dependency needs my go-ahead, including this one. If I decline, continue setup without it and
don't ask again this session."""


DESIGN_STEP_NEW = """Do this BEFORE building any UI. Skipping it is the main reason AI-built interfaces come out generic — with no decided point of view, the default is a templated look.

Settle these with me, then write them into DESIGN.md at the project root.

1. **Language and reading direction.** Ask me the primary language(s), and which of these the project is. Do this first: it changes how the code is built, not just what it says.
   - **Single-direction LTR** (English or similar only).
   - **Single-direction RTL** (Arabic or similar only). Treat RTL as the native layout direction, never as a mirrored afterthought.
   - **Bilingual / multi-directional.** One component set must serve both directions — no mirrored duplicates. Settle now: default and fallback locale, URL strategy (`/ar`, `/en`, subdomain), where the switcher lives, and how `dir`/`lang` change on switch.

   Whatever the answer: use logical properties (`margin-inline`, `inset-inline-start`, `text-align: start`) rather than hardcoded left/right, even on a single-direction project. It costs nothing now and is the difference between adding a language later being a translation job or a rewrite.

   **If the answer is RTL or bilingual**, say so plainly and tell me the project needs the RTL guide — the language checkpoint's Parts B and C carry the script-specific rules, and they apply from the first component, not at review time.

   Record the answer in DESIGN.md. The language checkpoint reads it to know which parts to run.

2. **Direction, from real references — not from a description.**
   - Create a `design-references/` folder at the project root. (Part of setup — no need to ask first.)
   - Ask me to put full-page screenshots of **at least three** sites or products I react to into it, including at least one **interior** page per site — a list, detail, form or dashboard screen, not only homepages. A homepage is a marketing artifact; the interior page is where the real design system lives.
   - **Then STOP and wait until I confirm the files are there.** Do not design from nothing while waiting.
   - When I confirm, read the images and report what you actually see, mechanically: ground colour, type pairing and scale, spacing rhythm, corner-radius language, elevation treatment (or its absence), and how the single accent is used. Name what they share and where they disagree.
   - **Mood:** ask how it should feel in a few words (trustworthy, playful, premium, utilitarian).
   - **These are references, not specifications.** Match the feel; never copy a layout. Propose at least one direction the references did NOT suggest, and say why it might suit this project better. References raise the floor; they don't cap the ceiling.
   - Then propose a small number of concrete directions with reasoning, and let me pick or combine.
   - Once the direction is settled, decide with me whether `design-references/` is committed or gitignored. Those are third-party screenshots and can be large; committing keeps the design reasoning with the project. Either is fine — deciding silently is not.

3. **Colour — ask, don't guess.** Before writing a single colour into DESIGN.md:
   - Ask whether the project already has brand colours (a logo, existing material). If so, ask me for the hex values.
   - If not, propose **two or three** palettes drawn from the references, one sentence each, and let me pick. Don't decide for me.
   - **Ask about dark mode now: yes, later, or never.** This is nearly free while the tokens are being written and expensive months later, because every contrast pair has to be re-verified against a second set of grounds. If the answer is "later", still structure the tokens so it's a layer-2 addition rather than a rewrite.
   - Record the **jobs**, not just the values. Each colour gets one job and a stated limit: the page ground; the ink; exactly ONE primary action colour reserved for that and nothing else; semantic colours (success / error / warning) kept separate from brand colours; and for each, what it is NOT allowed to do.
   - **Verify every foreground/background pair numerically against WCAG AA now** — including hover, focus, active, disabled and selected, and every pair on dark surfaces if dark mode is in scope. A token that fails is worse than no token, because it gets followed. Nothing goes into DESIGN.md before it passes.
   - Then stop and show me the palette before continuing.

4. **Anti-references.** Ask what I explicitly do NOT want, including any past attempt that was rejected and why. Knowing what to avoid is as useful as knowing what to aim for.

5. **Register.** Product surface (workflows, task completion) or brand surface (visual storytelling), or a split? This decides whether clarity or expression wins when they conflict, and governs how much motion is appropriate.

6. **Approved Sources.** Record in DESIGN.md where each kind of visual material comes from. This is what lets you ASK me for material instead of inventing it — name the source and search terms, and I'll fetch it. Cover at minimum:
   - **Icons** — ONE set, used everywhere. Never two icon systems, never emoji as icons.
   - **Motion** — the animation source, if any.
   - **Component patterns** — where to look when a specific block is needed.
   - **Backgrounds / texture** — how depth is achieved.
   - **Type** — the families and where they load from.
   For each: what it's for, the URL, and any licence constraint. If the project needs something this list doesn't cover, ask before choosing.

7. **Design skills — who owns what.** Tooling was checked in an earlier step. If a design skill is available, it works INSIDE this system, never instead of it.

   **DESIGN.md is the single source of truth.** No skill's own config, spec or generated design file overrides it. If a skill wants to write its own design document, either point it at DESIGN.md or keep its file as scratch and reconcile into DESIGN.md — tell me which you did. Two competing design systems in one repo is worse than none.

   - **A generator-style skill** (catalogue of styles, palettes, font pairings) is a **proposer**. Its output is ONE more candidate in steps 2 and 3, clearly labelled as a catalogue suggestion, sitting beside the directions drawn from my actual references. It never decides, and never overwrites a decision I already made.
   - **A critic-style skill** (review and refinement commands — e.g. impeccable's `critique`, `audit`, `polish`, `live`) runs **after code exists**. Its value is catching the tells that make work read as machine-made: overused fonts, grey text on coloured grounds, untinted black, nested cards, dated easing. Do not run its `init`-style setup without asking me first — those commands typically create their own product and design files, which is exactly the conflict above.
   - **A critic removes what is wrong; it does not supply a point of view.** A clean report on a page built with no decided direction gives you a tidy generic page. The direction work above is what prevents generic; the skill is what prevents sloppy.
   - These skills do not know about reading direction or non-Latin scripts. A clean report from one says nothing about RTL correctness.
   - If no design skill is available, everything above still runs. It just takes longer.

8. **Write DESIGN.md** documenting the ACTUAL system: colour roles, typography scale, spacing, radii, elevation, breakpoints that matter for this project, and key components. Name the rules that follow from the direction. Document what the code really does, not what it aspires to — and flag any gaps.

   **Colour must be two layers in ONE file**, so the palette can change mid-project without hunting through components:
   - *Layer 1 — the raw palette.* The only place a hex value appears in the project.
   - *Layer 2 — the roles.* `--color-surface`, `--color-ink`, `--color-action`, `--color-action-hover`, each pointing at a layer-1 value.
   - Components reference layer 2 ONLY. Changing the palette is then a handful of lines in one file, and reassigning a role works without touching a component. Dark mode is a layer-2 redefinition; layer 1 does not move.

9. **Prove the direction on ONE screen before building anything else.**

   A direction that looks right on a hero can fall apart across twelve screens, and you will not find that out from a mockup. So:
   - Pick the **densest real screen** in the project — the one with the most information per square inch. A listing, a detail page, a form. Not the homepage.
   - Build it completely, using the **longest real content available** — real names, real prices, real Arabic strings if the project is bilingual. **Never lorem, never short samples.** Text-length and mixed-script problems are invisible until real data hits them, and they are the most common reason a design system fails in production.
   - Include its **empty, loading and error states.** These are part of the screen, not an afterthought — designing them later is how they end up unstyled.
   - Then look at it in the browser yourself, run `review`, and if a critic skill is available run it here. Fix what comes back.
   - **Only then build the rest against it.** Tell me explicitly when you consider the direction proven, and what changed between the plan and the working screen — that difference is the most useful thing this step produces."""


DESIGN_STEP_EXISTING = """Only if this project has a UI. The goal here is to DOCUMENT the design system that already exists, not to impose a new one — the same "going forward only" rule applies.

**First, check there is actually a system to document.** If the styles are ad-hoc — no consistent colour roles, no type scale, one-off values everywhere — say so plainly rather than dressing up chaos as a system. Then offer me the choice, and ask rather than picking:
- **Document what exists** as a baseline and improve it incrementally, or
- **Establish a direction properly first.** That means: create a `design-references/` folder, ask me for full-page screenshots of 3+ sites (at least one interior page each), STOP and wait until I confirm they are there, then read them and report what you see mechanically — ground colour, type pairing and scale, spacing rhythm, radius language, elevation treatment, accent use. Ask me about colour rather than guessing it, record each colour's job and its limit, verify every pair against WCAG AA including hover/focus/active/disabled, and show me the palette before continuing.

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

This file holds the procedures run on demand by the checkpoint shortcuts ("review", "test check", "rtl check", "perf pass", "motion check", "ship check"). It deliberately does NOT go into CLAUDE.md — it is read only when a shortcut fires, so it never consumes session context it isn't needed for. Commit it alongside the other docs.

**Then, ONLY if this project's reading direction is RTL or bilingual:** also create RTL.md at the project root, containing the FULL "RTL / Bilingual Guide" section from the very bottom of this message, verbatim. Add one line to CLAUDE.md under Project Rules: *"This project is RTL/bilingual — read RTL.md before any UI work."* Then tell me you created it.

If the project is single-direction LTR, do NOT create RTL.md and do NOT add that line. Say which you did, so I know it was a decision rather than an omission."""

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
> below by hand. Edit the masters in this repo, then run `python3 build-prompts.py`.""",
    intro="""You are setting up a new project. Follow the setup steps below in order, then follow the embedded PROJECT RULES for the entire lifetime of the project.""",
    steps=[
        ("Understand the project and choose the stack", """Start here, before creating anything. The stack determines the folder structure, .gitignore, and tooling, so it's decided first.
- Ask me what the project is and what it needs to do.
- Based on that, recommend the best-suited stack — frontend, backend, database, hosting, and any key services — explaining the tradeoffs and why each choice fits this specific project. Don't just list options; give a reasoned recommendation.
- Weigh factors like project type, scale, performance needs, my familiarity, cost, and long-term maintainability.
- Go back and forth with me until we settle on the final stack together."""),
        ("Tooling check", TOOLING_STEP),
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
> below by hand. Edit the masters in this repo, then run `python3 build-prompts.py`.""",
    intro="""This project is already underway. Set it up with context files, rules, checkpoints, and shortcuts WITHOUT disrupting the existing code. Follow the steps below, then follow the embedded PROJECT RULES for the rest of the project's life.

Also important: The PROJECT RULES apply GOING FORWARD only. Do NOT refactor, rewrite, or "fix" existing code to match them unless I explicitly ask. Your job right now is to document what exists and set up the workflow — not to change the codebase. Fill the files with REAL details discovered from the actual code, not placeholders. If something isn't clear from the code, ask me instead of guessing.""",
    steps=[
        ("Scan the codebase", """Read through the project to understand its stack, architecture, folder structure, conventions, and any notable quirks. You'll use this to fill in the files below accurately. Note anything that looks intentional-but-odd so it can be recorded rather than "fixed" later."""),
        ("Tooling check", TOOLING_STEP),
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
> below by hand. Edit the masters in this repo, then run `python3 build-prompts.py`.""",
    intro="""The setup for this project was started but not finished correctly. There is already real work in this project, and some setup files (CLAUDE.md, PROGRESS.md, and/or README.md) may already exist partially. Your job is to FINISH and FIX the setup as described below.

CRITICAL — do not destroy existing work:
- Do NOT delete, reset, or revert any of my existing code or project work.
- Do NOT overwrite my existing files wholesale. If a file already exists, READ it first and MERGE — keep what's good, fill in what's missing, fix what's wrong. Only create a file from scratch if it doesn't exist.
- If anything is ambiguous or you're unsure whether something is intentional, ASK me instead of guessing or changing it.""",
    steps=[
        ("Take stock of the current state", """- Scan the codebase to understand the current stack, architecture, folder structure, conventions, and what has been built so far.
- Check whether CLAUDE.md, PROGRESS.md, README.md, DESIGN.md, CHECKPOINTS.md, .gitignore, and .env.example already exist, and note what each currently contains.
- Give me a short summary of what you found and what's missing or incomplete, BEFORE changing anything."""),
        ("Tooling check", TOOLING_STEP),
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
    parts.append("")
    parts.append(RTL)
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
    for name, text in (("CHECKPOINTS.md", CHECKS), ("RTL.md", RTL)):
        (OUT / name).write_text(text.rstrip() + "\n", encoding="utf-8")
        print(f"  {name:<40} {len(text):>7,} chars")
    print("\nDone. The rules and checkpoints in every file are now identical.")
