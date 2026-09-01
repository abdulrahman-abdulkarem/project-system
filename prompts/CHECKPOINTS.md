# Project Checkpoints

Procedures run on demand by shortcut. Each one reports findings grouped by severity, most serious first, and changes nothing until told which findings to act on.

Two rules that apply to every checkpoint below:

- **State your boundaries.** Say what you actually read versus what you only grep-swept, and mark any finding confirmed in one place but merely suspected elsewhere. An audit that hides its own coverage gaps produces false confidence.
- **Name shared root causes.** If the same defect surfaces through more than one checkpoint, don't report it twice — say what the single underlying cause is. A defect visible through two different lenses is usually systemic, and fixing it at its source beats fixing each symptom.

---

## Code Review checkpoint — "review"

Run against the current uncommitted changes, not the whole codebase.

**Scope discipline**
- Does the diff do only what was asked? Flag any unrelated refactor, renaming, or "while I was in there" change.
- Any new file, wrapper, or abstraction that wasn't requested?

**Hard Rules**
- Walk the eight Hard Rules and confirm none is violated.

**Security on new surface area**
- Every new input path: validated and sanitized server-side?
- Every new route or action touching protected data: authorization enforced server-side, and checked against *this specific resource*, not just "is logged in"?
- Any secret, key, or connection string that moved toward the client bundle?
- Any new error path that could leak internals, stack traces, or reveal whether an account exists?

**Correctness under stress** — for each new code path, name what happens with:
- empty or missing data
- malformed or hostile parameters
- a slow or failed network call
- an unauthorized or logged-out user

**States and UI**
- Loading, empty, and error states handled for anything async that was added?
- Does any new skeleton match the real layout exactly?
- New styles: do they reuse existing tokens and utilities, or is this a one-off that should have been a token?
- Icon set consistent — no emoji standing in for icon components?

**Accessibility and reading direction**
- Labels on new inputs; heading levels unbroken; contrast checked numerically; focus visible; touch targets at the project minimum.
- Any new X-axis assumption (slide, arrow, chevron, horizontal scroll) that breaks under the project's reading direction?

**Documentation**
- Does this change make CLAUDE.md, README.md, or DESIGN.md inaccurate?

Report by severity: **Blocking** (Hard Rule violation, security hole, broken behavior) → **Should fix** (missing state, accessibility failure, scope creep) → **Worth noting** (style, naming, future risk). Then stop.

---

## Testing checkpoint — "test check"

**What must be tested** — high cost of being wrong, low cost to test:
- Authorization logic: who can see and do what. This is where a silent bug is most expensive.
- Input validation and sanitization, including the malformed and hostile cases.
- Money, pricing, quantity, and any arithmetic a user would notice being wrong.
- Date, time, and timezone handling — especially across the timezones the project actually serves.
- Anything that has broken once before. Every bug fix gets a regression test, written failing first.

**What's worth testing** — pure logic with real branching:
- Business rules and decision functions.
- Data transformations and parsing.
- API route contracts: status codes and response shape for success, failure, and unauthorized.

**What is deliberately not worth testing** — say so out loud rather than quietly skipping:
- Styling and visual appearance. That's what the browser check and the design review are for.
- Framework behavior. Don't test that the framework routes, renders, or fetches.
- Trivial pass-throughs and getters.
- Anything so mocked that the test only proves the mocks were configured.

**How to write them**
- Test behavior, not implementation. A test coupled to internals breaks on every refactor and protects nothing.
- Name the test after the behavior it protects, so a failure reads as a sentence about what broke.
- Keep them fast enough that running them isn't a decision.
- One clear reason to fail per test.

**When to run**
- Before declaring work done, and before "commit".
- A test suite that's never run is documentation, and out-of-date documentation at that.

**Reporting**
- List what's covered, what's uncovered *that meets the "must" bar above*, and any test that looks like it can never fail.
- Coverage percentage is not a goal and shouldn't be reported as one.

---

## Data model checkpoint — "schema check"

Run BEFORE writing a migration, not after reviewing one. A schema is the most expensive thing in the project to change once real data is sitting in it.

**Shape**
- Can you name each table's single responsibility in one sentence? If not, it's doing two jobs.
- Are relationships explicit foreign keys rather than implied by naming convention?
- One-to-many and many-to-many modelled correctly, with junction tables where they belong?
- Any column holding a list, a CSV string, or a JSON blob that should be its own table? You lose querying and integrity the moment data hides inside a string.
- Any field duplicated across tables that should be referenced or derived instead?

**Types and constraints**
- The right type per column: decimal for money, never float. Timestamps with timezone. Constrained enums rather than free text.
- `NOT NULL` on everything that shouldn't be nullable, with defaults chosen deliberately rather than inherited.
- `UNIQUE` enforced by the database on anything that must be unique — application-level checks race and lose.
- Delete behavior decided explicitly per relationship (cascade, restrict, set null), not left at the default.

**Access and privacy**
- For each table, state which user can see which rows — before it ships, not after. If the project uses row-level security, the policy is part of the schema, not an afterthought.
- Soft delete or hard delete, decided per table and written down.
- Any personal data: is it genuinely needed, minimized, and handled per the security rules?

**Growth**
- Indexes on the columns you already know will be filtered and joined on, based on the queries the features actually run.
- What does this look like at 100× the rows? Name anything that only works while the table is small.
- Anything unbounded — logs, events, sessions — that will need pruning, archiving, or partitioning?

**Change safety**
- Is the migration reversible, and what's the rollback?
- Does it need a backfill or downtime? Say so before running it, not during.
- Naming matches the project's existing convention.

Report what's sound, what should change before shipping, and any deliberate trade-off worth recording under Key Decisions in CLAUDE.md.

---

## Language, Direction & Accessibility checkpoint — "lang check" / "rtl check" / "a11y check"

All three shortcut names load this checkpoint. It runs in tiers: **Part A applies to every project ever built**, Part B only if a non-Latin or RTL language is involved, Part C only if the project serves more than one reading direction. Check DESIGN.md for which case this project is, and say at the top of your report which parts you ran and which you skipped and why.

### Part A — every project, every language

**Accessibility**
- Heading outline complete and unskipped — read it top to bottom as a table of contents.
- Every input has a persistent, programmatically associated label. A placeholder is not a label.
- Contrast measured numerically against WCAG AA, including text carrying opacity modifiers.
- Focus visible on every interactive element, and focus order follows reading order.
- Touch targets meet the project minimum (44×44px).
- Collections use semantic list markup.
- Icon-only controls have accessible names.
- The critical path is completable by keyboard alone.

**Language hygiene**
- No hardcoded user-facing strings, even in a single-language project — they're the thing that makes adding a language later expensive.
- Dates, times, numbers, and currency formatted through a locale-aware API rather than hand-built strings. Timezone explicit rather than inherited from the server.
- Layout tolerates text of unexpected length without clipping or breaking.

**Direction-readiness**
- Spacing, alignment, and positioning use logical properties rather than hardcoded left/right — including on single-direction projects, where this is cheap insurance rather than dead weight.

### Part B — any non-Latin script or RTL language

- `dir` and `lang` correct on the root element, and on any element whose language differs from its container.
- Layout genuinely mirrors: not just text alignment, but component internals, iconography, and spacing logic.
- Directional elements mirrored: arrows, chevrons, back/forward controls, progress indicators, sliders, carousels, and any X-axis animation.
- Mixed-direction runs isolated — Latin brand names, URLs, emails, phone numbers, and code inside RTL text render in the correct order with punctuation in the right place.
- Every script in use has a font genuinely loaded — verified in the browser, not inferred from a CSS variable.
- No `uppercase` and no letter-spacing/tracking on Arabic or any cursive script.
- Line-height and font-size suit the script. Arabic generally needs more vertical room than Latin at the same nominal size.
- Numerals: one deliberate choice of numeral system, applied consistently.
- Plural and count-noun agreement follows each language's own grammar.

### Part C — bilingual or multi-directional projects

The failure mode here is different from single-direction work: it isn't that one direction is wrong, it's that fixing one direction quietly breaks the other.

- **One component set serves both directions.** No mirrored duplicates — a forked component drifts, and the second direction becomes the neglected one.
- Switching locale switches `dir` and `lang` together, and re-renders correctly without a full reload leaving stale direction behind.
- The language switcher is reachable on every page, labelled in the target language (say "العربية", not "Arabic"), and doesn't lose the user's place.
- Default and fallback locale decided and documented: what an unknown locale, a missing translation, or a first-time visitor gets.
- URL strategy consistent (`/ar`, `/en`, subdomain, or query) and reflected in `hreflang` and canonical tags.
- Font pairing balanced across scripts — a Latin and an Arabic face at the same nominal size rarely look the same weight or height. Tune per script rather than accepting the default mismatch.
- Test the **same page** in both directions at the same breakpoint. Most bilingual bugs are invisible until you view them side by side.
- Content that must stay LTR in an RTL layout (code blocks, phone numbers, IBANs) explicitly marked, not left to the browser's guess.

---

## Performance checkpoint — "perf pass"

Run before shipping, and after any change that adds a dependency or a lot of markup.

1. **Measure first.** Run Lighthouse (Performance, Accessibility, Best Practices, SEO) and record the baseline before changing anything. Don't optimize what you haven't measured — a static reading of the code produces a *hypothesis* about what's slow, and measurement regularly reassigns the blame. If Lighthouse or a production build can't run in this environment, say so at the TOP of the report, do the static pass anyway, and list the measurement steps as explicitly outstanding — a static-only pass is a partial result, not a completed checkpoint, and reporting it as complete is worse than not running it.
   - **Measure more than one page.** A slow page sitting next to a fast sibling on the same infrastructure isolates page-specific causes from infrastructure ones immediately. It's the cheapest way to know whether you're chasing your own code or your hosting.
   - **Know which number you're reading.** Lighthouse's headline Performance score and LCP are a *simulated* mobile result — modelled CPU and network throttling applied to the trace, not what actually happened on the machine. The same trace also holds the real observed values. Report both, and state which one a change is meant to move. Work that genuinely cuts main-thread cost may not shift the simulated score at all, and work that shifts the simulated score may be pure network modelling. Optimising the wrong one wastes effort and hides real gains.
2. **Bring content closer.** Serve static and cacheable content from a CDN/edge rather than one distant origin — distance is latency.
3. **Cache correctly, once.** `Cache-Control` and `ETag` set deliberately; content-hashed filenames for immutable assets so they cache indefinitely; confirm the CDN is actually caching rather than refetching what hasn't changed.
4. **Trim the CSS.** Remove unused rules, simplify over-specific selectors, avoid layout thrashing (reading and writing layout properties in the same tick), and use containment where a component's internals shouldn't affect outside layout.
5. **Ship less JS.** Code-split by route, tree-shake unused exports, lazy-load what's below the fold or rarely used, defer non-critical scripts off the main thread.
6. **Fonts are a performance decision.** WOFF2, subset to the characters and scripts actually used (this matters most for non-Latin), `font-display: swap`, and preload only the fonts that block first paint.
7. **Right-size images.** Modern formats (WebP/AVIF), responsive sizes via `srcset`, lazy-load offscreen images — and never the LCP element.
8. **Re-measure, then keep measuring.** Run Lighthouse again to confirm the change helped. If the project has real traffic, monitor over time rather than treating this as a one-off.

---

## Motion checkpoint — "motion check"

**First, the register test.** Is this a *product surface* (workflows, task completion) or a *brand surface* (visual storytelling)?
- **Product surface:** motion is functional only — reveals, state feedback, transition continuity. Anything that takes control of the user's scroll is a defect, not a feature. Most projects live here.
- **Brand surface:** the expressive techniques below are available, because being memorable is part of the job.

**Then pick the interaction before the technique** — never the reverse.

| The interaction you need | Technique | Cost / caution |
|---|---|---|
| Reveal content as it enters the viewport | Scroll trigger | Cheapest and safest. The default; usually all a product surface needs. |
| Hold one element fixed while the rest scrolls past | Pin | Expensive. Reserves layout space, breaks often on mobile, edges toward scroll-jacking. |
| Depth from layers moving at different speeds | Parallax | Foreground ≈1.4x, midground 1.0x, background ≈0.5x. Subtlety is the whole game. |
| Move content sideways as the user scrolls down | Horizontal scroll | Hijacks an axis. Must be mirrored in RTL. Good for showcases, bad for tasks. |
| Show how far through the page someone is | Scroll progress | A utility, not decoration. Cheap and genuinely useful on long content. |
| Tie animation progress to scroll position frame by frame | Scroll-linked (scrub) | Most expensive — every scroll event drives a render. Transform/opacity only. |

**Verify before keeping any of it**
- Reduced motion: enable it and confirm the content still arrives.
- RTL: confirm X-axis motion mirrors.
- Mobile: pin and scrub fail here first — check a real phone viewport.
- No-JS: confirm nothing is reachable *only* through an animation.
- Bundle: if a second animation library was added, confirm it earned its weight.

---

## Ship / Deploy checkpoint — "ship check"

"Works on my machine" is not done.

**Configuration**
- Every variable in `.env.example` has a real value set in the production environment.
- No server-only key reachable from client-side code — check the built bundle, not just the source.
- Production URLs, callback URLs, and allowed origins updated for the real domain.

**Data**
- Migrations run against production, in order, with a rollback path identified.
- A backup exists and restoring from it has been tested at least once.

**Production hardening**
- Debug mode off, verbose errors disabled, stack traces not reaching the client.
- Source maps not publicly served (or deliberately served, if you've decided that).
- Default, seed, or demo credentials removed — including any admin account created during development.
- Security headers verified as actually present in the production response, not merely configured. Configured is not the same as served.
- Rate limiting confirmed active against the production deployment, not just in code.

**Build and behavior**
- Clean production build; no errors in the browser console on the key pages.
- 404 and 500 pages exist and are styled.
- Errors return generic messages to the client while logging full detail server-side.
- Auth flows tested against the production configuration, not a local stub.

**Pre-flight**
- Performance checkpoint run and re-measured.
- RTL / i18n / accessibility checkpoint run.
- For public sites: meta tags, Open Graph, `robots.txt`, sitemap, and canonical URLs correct.
- Domain, SSL, and redirects (www/non-www, http→https) resolving properly.

**After deploying**
- Walk the critical path on the live site, on a phone, in the project's real reading direction.
- Confirm logging and error reporting are actually receiving events.
- Record the deploy in PROGRESS.md — what shipped, and anything left behind.
