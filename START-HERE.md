# START HERE

Open this beside a new project and work down it. Everything else in this repo is
detail you only need when something goes wrong.

---

## Before you paste anything — 5 minutes

**Pick your prompt:**

| Situation | File |
|---|---|
| New project | `prompts/new-project-kickoff-prompt.md` |
| Project already underway | `prompts/existing-project-setup-prompt.md` |
| Setup got interrupted or half-finished | `prompts/repair-setup-prompt.md` |

**Have these ready.** Setup will stop and ask for each one, and every answer you
don't have is one it has to guess:

- What the project is, in a sentence, and who it's for
- The stack, if you've decided
- **Language and reading direction** — LTR only, RTL only, or bilingual. This
  drives layout, not just translation.
- **Brand colours**, if any exist. Hex values.
- **3+ screenshots** of sites you react to, with at least one interior page each
  (a list, detail, form or dashboard — not just homepages)

You don't need the screenshots before you start — setup creates the folder and
waits. But having them ready saves a round trip.

---

## 1 · Run setup

Copy the **whole code block** from your chosen prompt file and paste it as the
first message in a new Claude Code session.

**It will stop and ask you things. That's the design.** Two stops are deliberate
and matter most:

- **Design references.** It creates `design-references/`, asks you to fill it,
  and waits. Put the screenshots in, tell it they're there. It then reads them
  and reports back what it sees mechanically — and proposes one direction the
  references didn't suggest.
- **The palette.** It asks for your colours or proposes two or three. It checks
  every pair against WCAG AA before writing anything, then shows you the palette
  and waits.

If it starts designing without asking, it skipped a step — tell it to go back.

Setup ends with **"Setup complete — the shortcuts are active."** Don't start
giving it work before that line appears.

---

## 2 · Every session after that

1. **Start a new chat.** It reads PROGRESS.md and tells you where things stand.
2. **"plan"** — before anything non-trivial. It gives an approach and one
   rejected alternative, then waits.
3. **Build.**
4. **"review"** — on the uncommitted changes, before you forget what they were.
5. **"wrap up"** — updates PROGRESS.md, CLAUDE.md, README.md, DESIGN.md. Touches
   no git.
6. **"commit"** — reviews what's staged, then commits and pushes.

Anytime: **"Q&A"** / **"Q&A short"** to consult without changing code ·
**"Q&A history"** to see past consults.

---

## 3 · Checkpoints — run these at the moment, not at the end

| When | Shortcut |
|---|---|
| Changes are written and not yet committed | `review` |
| A feature is working and needs coverage | `test check` |
| Before the data model hardens | `schema check` |
| Any UI exists — and always before launch | `lang check` |
| The app feels slow, or before launch | `perf pass` |
| Before building anything beyond a simple reveal | `motion check` |
| Before deploying | `ship check` |

Each one loads its procedure, reports by severity, and **changes nothing** until
you say which findings to act on.

`lang check` runs in tiers — Part A applies to every project ever built, even a
single-language one. Don't skip it because the project is English-only.

---

## 4 · When something goes wrong

**Setup was interrupted or came out half-finished.** Use
`prompts/repair-setup-prompt.md`. Don't re-run the kickoff prompt over the top.

**It's designing without having asked you anything.** It skipped the references
step. Tell it to stop and go back to it.

**A git merge that resolved cleanly.** Verify the files actually contain what you
expect. A clean merge can silently discard a whole branch if the target contains
a revert of a shared commit — this has already happened once here.

**A tool reported everything passing but the UI is wrong.** Automated checks only
measure the resting state. Hover, focus, active, disabled and selected are yours
to check by hand.

---

## Changing the system itself

Edit `masters/`, never `prompts/`. Then:

```bash
python3 build-prompts.py
```

Everything in `prompts/` is generated. Hand-editing a generated file is how these
files silently drifted apart four separate times — and each time, nobody noticed
for weeks.

**What earns a place in the always-on rules:** only something that stops you
writing the wrong thing *at the moment you write it*. Everything else is a
procedure and belongs in `masters/project-checkpoints.md`, where it costs nothing
until it's called. The kickoff prompt is already 65KB; without this test it only
grows.
