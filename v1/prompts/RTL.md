<!-- BEGIN system-rtl-guide (generated from rtl-guide.md@092e3110 — do not edit by hand) -->
# RTL / Bilingual Guide

This project's reading direction is RTL or bilingual. Read this before writing any UI, not
after. Direction is a layout decision, not a translation job — retrofitting it is the single
most expensive mistake available here.

`rtl check` / `lang check` load this file. So does any UI work on this project.

---

## 1. Foundations

- `dir` and `lang` correct on the root element, and on any element whose language differs from
  its container.
- **Logical properties everywhere.** `margin-inline`, `padding-inline`, `inset-inline-start`,
  `text-align: start`. Never `left`/`right`. This is the difference between a direction change
  being a config switch and a rewrite.
- **One component set serves both directions.** No mirrored duplicates — a forked component
  drifts, and the second direction becomes the neglected one.
- Every script in use has a font **genuinely loaded** — verified in the browser, not inferred
  from a CSS variable. A missing non-Latin font falls back silently and looks almost right.

---

## 2. Mirroring — what flips, and what must not

Layout mirrors: not just text alignment, but component internals, iconography and spacing
logic.

**Flips** — these follow reading direction:
- Arrows, chevrons, back/forward controls
- Progress indicators, sliders, carousels, any X-axis animation
- **Tables, completely — column order included.** The first column moves to the reading start,
  the action column crosses to the other side, and sort indicators stay attached to their own
  headers.
- **Breadcrumbs, pagination and step indicators.** First item at the reading start, chevrons
  pointing along the reading direction, page 1 where the eye starts.

**Does NOT flip** — these carry meaning, not direction:
- An arrow meaning "increase" or "decrease"
- A play triangle
- A checkmark
- Anything whose meaning would invert if mirrored

**Mirroring a trend arrow inverts what it says.** Walk the icon set and sort it into the two
piles before mirroring anything.

---

## 3. Typography per script

- **No `uppercase`, no letter-spacing / tracking on Arabic or any cursive script.** `uppercase`
  is a no-op; tracking breaks letter-joining and legibility.
- Line-height and font-size suit the script. Arabic generally needs more vertical room than
  Latin at the same nominal size.
- **Optical size, not nominal size.** Arabic has no ascenders or descenders, so at an equal
  nominal size it reads smaller than Latin beside it. A wordmark, nav label or display line may
  need to be set larger in Arabic to hold equal presence. Judge by eye at real sizes, not by the
  number in the CSS.
- Font pairing balanced across scripts — a Latin and an Arabic face at the same nominal size
  rarely look the same weight or height. Tune each script separately rather than accepting the
  default mismatch.
- **Graphical emphasis survives a script change; typographic emphasis does not.** A highlight,
  a circle, an underline or a coloured slab sits *around* the text and transfers to any script.
  A two-weight stack, letter-spacing or capitalisation is a property *of* the text and breaks.
  Forcing an English typographic device onto Arabic looks worse than dropping it.
- Numerals: one deliberate choice of numeral system, applied consistently.
- Plural and count-noun agreement follows each language's own grammar.

---

## 4. Mixed-direction content

This is where most real bugs live.

- **Isolate embedded runs.** Latin brand names, URLs, emails, phone numbers and code inside RTL
  text must render in the correct order with punctuation in the right place.
- **Latin brand, product and person names stay in Latin script** rather than being
  transliterated. Only the descriptor around them translates. Verify the surrounding
  punctuation and spacing survive the switch.
- **Numbers, currency and percentages keep LTR order** inside RTL text. The number and its
  symbol behave as one unit; the row around them reverses.
- **Sentence-ending punctuation must land at the correct end of the line.** Check with real
  content, not placeholder text — a full stop rendering at the *start* of a line is a bidi
  failure that only appears in RTL and that no English-language QA pass will catch.
- **Mixed-script wrapping in width-constrained containers.** A short phrase in one script
  followed by a long run in the other wraps and truncates badly inside a card. Test with the
  longest REAL content in both scripts, never short samples — this failure is invisible until
  real data hits it, and it is the most common way a card design fails in production.
- Content that must stay LTR in an RTL layout (code blocks, phone numbers, IBANs) explicitly
  marked, not left to the browser's guess.

---

## 5. Bilingual projects specifically

The failure mode here is different from single-direction work: it isn't that one direction is
wrong, it's that fixing one direction quietly breaks the other.

- Switching locale switches `dir` and `lang` together, and re-renders correctly without a full
  reload leaving stale direction behind.
- The language switcher is reachable on every page, labelled **in the target language** (say
  "العربية", not "Arabic"), and doesn't lose the user's place.
- Default and fallback locale decided and documented: what an unknown locale, a missing
  translation, or a first-time visitor gets.
- URL strategy consistent (`/ar`, `/en`, subdomain, or query) and reflected in `hreflang` and
  canonical tags.

---

## 6. Verification

- **Test the same page in both directions at the same breakpoint.** Most bilingual bugs are
  invisible until the two are viewed side by side.
- Use real content at real length. The longest name, the longest product title, the longest
  Arabic string you actually have.
- Check the states, not just the resting page: hover, focus, active, disabled, selected, empty,
  loading, error.
- An automated pass says nothing about direction. Design and accessibility tools do not know
  RTL exists — a clean report from one is not evidence of RTL correctness.

---

## 7. Open questions — decide deliberately and record in DESIGN.md

**Do chart interiors mirror?** Observed references disagree. One reversed its chronological
timeline in Arabic, putting the earliest date on the right. Another left its time axis running
left-to-right in both languages and did not reorder its bars, while mirroring the page layout
around them. There is no settled answer. Pick one for this project, write the decision in
DESIGN.md, and apply it consistently — the inconsistency is worse than either choice.
<!-- END system-rtl-guide -->
