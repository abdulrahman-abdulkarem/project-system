# Design-phase evaluation — 12/13 September 2026

A live run of the new-project prompt against a real project (`Test`, a taste
library viewer: Node, zero dependencies, ~12 unit tests). The design phase
was run end to end and evaluated as it went.

## Provenance and what is missing

Findings were numbered 1–42 during the run. This file contains **15 of them**:
the twelve that survived a context compaction, plus three logged afterwards
that never got numbers at the time (43–45).

Numbers 1–4, 6–10, 12–16, 18–24, 27, 28, 30, 32–37 are **not recoverable**.
They existed only in the conversation and were lost when it compacted. They
have not been reconstructed from memory, because a plausible-looking
reconstruction is indistinguishable from the real thing and this file is
supposed to be evidence.

Status codes: FIXED (commit), NO FIX (nothing to change — recorded because
it's true), OPEN.

---

## The three that matter most

**#29 — The system's core premise, confirmed.**
Claude Code reasoned about design at a high level for two hours — palette
with verified contrast ratios, colour jobs with limits, a written DESIGN.md —
and then produced a first layout that contradicted its own brief: 120×80
thumbnails against text running 850px wide. Nothing in the plan predicted it.
Nothing short of rendering it would have caught it.
*NO FIX — this is the failure the system exists to catch.*

**#39 — The model executes UI well when told precisely what's wrong, and
poorly when judging its own output.**
Three rounds of browse-view iteration. Every fix landed cleanly and fully
when the defect was named precisely. No round began with the model finding
the defect itself. This makes the one-screen proof not merely a checkpoint
but the mechanism that converts a person's eye into something the model can
act on.
*NO FIX — this is the argument for item 9 being non-droppable.*

**#42 — Rules freeze at setup and never refresh.**
A project's CLAUDE.md and CHECKPOINTS.md are written once, at setup, from
whatever masters/ said that day. Nothing propagates afterwards. Confirmed
against `Test`: it had diverged by exactly the four additions made that
evening, and had no mechanism to catch up.
*FIXED — deed3a2 (project-system) / af6d4f1 (Test). Delimited generated
regions, content-hash stamps, a drift check in `wrap up`, and a
`rules refresh` shortcut. Verified end to end: zero drift after migration,
refresh idempotent on a second run.*

---

## Design step

**#5 — The design step doesn't defend itself.**
Claude Code looked at the nine-item step, judged it heavy for the project,
invented a "condensed" variant of its own, and recommended skipping the full
step. Each individual judgement was defensible. The problem was that the
reduction was improvised, so nobody could tell which items were dropped
deliberately and which were dropped because they looked expensive.
*FIXED — 445a3ab. Two named modes, FULL and REDUCED, with fixed contents.
Item 9 is non-droppable in either. The person chooses; the step may offer
REDUCED and may not invent a third.*

**#11 — Structural and aesthetic references were not distinguished.**
A reference supplied for how a site organises information gets its palette
copied. The same screenshot can be either kind and you cannot tell by
looking.
*FIXED — 445a3ab. Labelled per reference by the person, proposed back after
the decode, confirmed before anything is designed from it.*

**#25 — The one-screen proof found two problems invisible in any plan.**
Uppercase, letter-spaced headings broke badly on three-line real content;
empty families rendered invisibly. Neither is predictable from a spec.
*FIXED — 3b1a137 (uppercase rule), 445a3ab (empty states).*

**#45 — The deliberate empty state looked less deliberate than the accidental
one.** Entries with no screenshot rendered as a labelled dashed placeholder;
an unlucky image crop rendered as a plain grey box. The genuine failure
looked more intentional than the intended state.
*FIXED — 445a3ab, item 9.*

---

## Review and verification

**#17 — The contrast check produced genuinely correct numbers.**
WCAG figures for the chosen palette were independently verified: 11.80:1
ink-on-ground, 6.86:1 accent-on-ground, both as claimed.
*NO FIX — recorded because the system working is also evidence.*

**#31 — Nothing compared the rendered screen against DESIGN.md.**
*FIXED — 3b1a137, `review`: line-by-line, naming which of the two is wrong.*

**#38 — Verification screenshots deleted before review.**
Cleanup instinct beat purpose.
*FIXED — 3b1a137, ANTI-RATIONALIZATION row: "I deleted the screenshot/log
once I'd confirmed the thing worked."*

**#40 — Kept but gitignored.**
After #38 was fixed, the screenshots survived on disk but were excluded from
the repo. "Not scratch" had been read as "don't delete," not "preserve as
evidence." The proof of a design decision didn't travel with the decision.
*FIXED — 3b1a137 wording; proof screenshot committed in Test d7c4fb4.*

**#44 — A faithful render of bad data is indistinguishable from a design
failure.** Changing the layout to compensate is the worst available outcome.
*FIXED — 3b1a137, `review`.*

---

## Model behaviour

**#26 — Uppercase and letter-spacing applied to text of uncontrolled length.**
*FIXED — 3b1a137.*

**#41 — Refused twice to act on a premise it couldn't verify.**
Once catching a conflation of two different folders; once refusing to "extend"
a rule that had never been written, after grepping for it and finding nothing.
Both refusals came from a grep, not from judgement — which corroborates #39
exactly: reliable where the question has a checkable answer, unreliable where
the question is "does this look right."
*NO FIX.*

**#43 — Once a screen becomes legible, the proof starts reporting on the data
rather than the design.** On the third browse-view render, four apparent
family headers were commentary, one family name appeared twice, and markdown
emphasis leaked as literal asterisks. None of it was visible until the text
was readable enough to read closely. Three of the five problems on that screen
were data defects, not design defects.
*FIXED at the data level — 8ebc3ee. The general rule is #44.*

---

## Also fixed during the run (data, not system)

In `taste-library/taste-library.md`, found by the viewer rendering it:
notes used the same heading level as entries and rendered as family headers;
the declared family list predated every real entry and was wrong three ways;
a note was appended into talabat's `Family:` grouping key; markdown emphasis
sat inside plain-text fields; two Careem screenshots were cited as evidence
for content they don't contain. All fixed in 8ebc3ee. Families are now
derived from the entries, with a separate labelled wishlist, and the names
are marked provisional until roughly ten real entries exist.
