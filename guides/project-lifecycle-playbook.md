# Project Lifecycle Playbook

Your at-a-glance guide for starting and running any project, phase by phase. Each phase lists what you do, which prompt/tool/shortcut to use, and its build-out status.

Status key: ✅ done · 🔨 in progress · 🧪 built but not yet validated on a real project · 📋 planned

**Honest state of the system (Aug 2026):** every phase below now has real content behind it — rules, a checkpoint, or a shortcut. Almost none of it has been run end-to-end on a live project, which is why so much of this page reads 🧪 rather than ✅. Built is not the same as proven. The next milestone isn't another phase; it's one full pass through this lifecycle on something real, after which the parts you skipped should be cut rather than kept for completeness.

---

## The lifecycle at a glance

Kickoff → Plan (per feature) → Design/Frontend → Backend & data → RTL/a11y checkpoint → Code review → Testing → Performance → Ship → Run & hand over

Running underneath all of it, every session: **Session start → work → wrap up → commit.**

---

## Phase 0 — Kickoff ✅

Set up the project foundation. Done once, at the very start.

- Run the right kickoff prompt:
  - New project → `new-project-kickoff-prompt.md`
  - Existing project → `existing-project-setup-prompt.md`
  - Setup got interrupted / half-done → `repair-setup-prompt.md`
- The prompt handles: stack discussion → CLAUDE.md + PROGRESS.md + README.md → clean structure → git/secrets hygiene → stack-specific rules → design direction (UI projects) → CHECKPOINTS.md.
- Confirm setup is complete (each prompt ends with "Setup complete — the shortcuts are active"). Only then start working.

All four prompts are generated from `project-rules.md` + `project-checkpoints.md` by `build-prompts.py`. Edit the masters, never the prompts, then run the script ("sync prompts").

---

## Phase 1 — Plan (per feature) 🧪

Before building any non-trivial feature, think first. This is the highest-value habit — it stops good execution of the wrong thing.

- Shortcut: **"plan"** → states the goal, the approach, the alternative rejected and why, the files that will change, and any decision needed from you — then stops and waits for your go-ahead.
- Keep it to a few lines. It's a checkpoint, not a document.

To validate: check whether the plan output is actually useful or just ceremony. If you find yourself skipping it on small features, that's correct behavior — the rule should say so rather than pretending otherwise.

---

## Phase 2 — Design direction & frontend 🔨

Set the design direction BEFORE building UI (this fixes the "generic/no style" problem at the root), then execute.

- Direction comes from three inputs: reference sites/images you like + a mood in words + options Claude proposes. Plus anti-references (what you explicitly don't want) and register (product surface vs brand surface). Output lands in DESIGN.md.
- **impeccable** — design execution + review (`polish`, `audit`, `critique`, `harden`, `craft`). Install: `/plugin marketplace add pbakaus/impeccable`, then `/impeccable init`. Invoke as `/impeccable:impeccable <command>`.
- Motion is the last step of this phase, never the first — see "Step 5 — Add motion" in `project-startup-plan-and-toolkit.md`, and run **"motion check"** before building anything beyond a simple reveal.
- RTL guardrail: always tell the design tools the project is Arabic/RTL and verify the output — no tool is RTL-aware by default, and that applies to motion direction as much as to layout.

**The one real gap left in this phase: the Taste Library doesn't exist.** Steps 2–4 of the design workflow all point at it ("pick the family," "give 2–3 references") and it isn't there. Needs 15–30 designs grouped into three or four distinct families with vocabulary keywords, including Arabic/RTL examples. This is the last 🔨 in the system.

---

## Phase 3 — Backend & data model 🧪

Build server-side with the standards in your rules — but design the data before building on top of it.

- **Data model first.** Run **"schema check"** before writing any migration. Shape, types and constraints, row-level access, growth behavior, and rollback safety. The schema is the most expensive thing in the project to change once real rows exist, which makes it the highest-leverage thinking you do in this phase.
- Enforce integrity in the database — foreign keys, uniqueness, NOT NULL, constrained enums — not only in application code.
- Already covered by the always-on rules: secrets management, server-side validation, authorization, media-as-links (object storage), migrations, parameterized queries, error handling, API response shape, indexes.

To validate: whether the schema checkpoint catches anything you'd otherwise have shipped. If it's the same five obvious questions every time, shorten it.

---

## Phase 4 — Language, direction & accessibility checkpoint 🧪

Shortcut: **"lang check"** / **"rtl check"** / **"a11y check"** — all three load the same checkpoint. It runs in three tiers, because not every project is Arabic-first:

- **Part A — every project, every language.** Accessibility (heading outline, labels, numeric contrast, focus order, touch targets, semantic collections, keyboard path), language hygiene (no hardcoded strings, locale-aware date/number/currency formatting, layouts that tolerate unexpected text length), and direction-readiness (logical properties instead of hardcoded left/right, even on LTR-only work).
- **Part B — any non-Latin script or RTL language.** `dir`/`lang` correctness, genuine mirroring, directional icons and X-axis motion, isolated mixed-direction runs, fonts actually loaded, no uppercase or tracking on cursive scripts, numeral system, per-language plural rules.
- **Part C — bilingual or multi-directional.** One component set for both directions (never mirrored duplicates), locale switching that changes `dir` and `lang` together, switcher labelled in the target language, default/fallback locale decided, URL and `hreflang` strategy, font pairing tuned per script, and the same page compared side by side in both directions.

The tiering exists because the original version was named "RTL check" with accessibility buried inside it — on an English-only project you'd correctly skip it and silently lose the accessibility pass that applies to everything.

---

## Phase 5 — Code review 🧪

Self-review against your own standards before committing. Shortcut: **"review"**.

- Runs against uncommitted changes only: scope discipline, Hard Rules, security on new surface area, correctness under stress (empty data, malformed params, slow network, unauthorized user), states and UI, accessibility and reading direction, documentation impact.
- Reports by severity — Blocking / Should fix / Worth noting — and changes nothing until you say which findings to act on.

---

## Phase 6 — Testing 🧪

Was the thinnest area in the system; now has real standards. Shortcut: **"test check"**.

- **Must test:** authorization logic, input validation, money and quantity math, date/timezone handling, and anything that has broken once (regression test written failing first).
- **Worth testing:** business rules, data transformations, API route contracts.
- **Deliberately not worth testing:** styling, framework behavior, trivial pass-throughs, anything so mocked the test only proves the mocks work.
- Test behavior, not implementation. Run them before "commit". Coverage percentage is not a goal.

To validate: this is the phase most likely to be quietly abandoned under deadline. If that happens, find out whether the standard is wrong or the discipline is — and fix the honest one.

---

## Phase 7 — Performance pass 🧪

A checkpoint before shipping so it actually happens. Shortcut: **"perf pass"**.

Measure with Lighthouse first → edge/CDN delivery → caching (Cache-Control, ETag, immutable assets) → trim CSS → ship less JS → fonts (WOFF2, subset, swap, preload) → right-size images → re-measure and keep measuring.

---

## Phase 8 — Ship / deploy 🧪

"Works on my machine" isn't done. Shortcut: **"ship check"**.

Configuration (env vars, no server keys in the bundle, production URLs) → data (migrations, rollback, tested backup) → build and behavior (clean build, 404/500 pages, auth against production config) → pre-flight (perf pass, rtl check, meta/OG/robots/sitemap, domain and SSL) → after deploying (walk the critical path live on a phone in the real reading direction, confirm error reporting is receiving events, record the deploy in PROGRESS.md).

---

## Phase 9 — Run, maintain, hand over 📋

**New.** The lifecycle used to end at "ship", which quietly assumed a project stops needing attention the moment it goes live. Most of a project's life happens here.

**Launch & discoverability** 📋 *(planned — not yet built)*

The gap between "deployed" and "running". Currently undocumented, and the place a launch quietly goes wrong.

- Domain purchased, DNS pointed, SSL valid, redirects resolving (www/non-www, http→https).
- Verified with Google Search Console and Bing Webmaster Tools; sitemap submitted; indexing confirmed rather than assumed.
- Analytics installed **and confirmed receiving events** — an analytics snippet that silently isn't firing is worse than none, because you'll trust the zero.
- Error tracking and uptime monitoring live, with an alert that actually reaches you.
- Structured data / Open Graph verified with the real crawlers, not just present in the markup.

**Tooling.** The menu should carry **several real options per category, with honest trade-offs** — free vs paid, what each is genuinely best at, where it's overkill for a project this size, and any limit that bites later (event caps, data retention, seat pricing). Claude Code recommends from that documented menu and explains the trade-off; you choose; the choice gets recorded in the project so it isn't re-litigated every time.

This is deliberately **not** the one-per-category rule that governs icons and design sources. Two icon sets produce visible inconsistency in the product; two monitoring tools never touch the UI. Categories are additive — analytics, error tracking and uptime are different jobs and most real projects want all three, and some pair legitimately inside one category (e.g. Vercel Analytics for Web Vitals alongside a separate traffic tool). The only thing worth avoiding is genuine redundancy: two tools measuring the same thing, paid for twice.

To build: the tool menu (categories, two or three real options each with the trade-off stated, and an honest "you probably don't need this yet" line per category), plus the launch checklist above turned into a checkpoint if it proves worth running every time.

**Running it**
- Know how you'd find out the site is down. If the answer is "a user tells me", that's the gap.
- Error tracking receiving events — re-check when it goes quiet. Silence usually means broken reporting, not zero errors.
- Note recurring issues in PROGRESS.md. Three instances of the same bug is a design problem, not three bugs.

**Fixing it live**
- Hotfix discipline: the smallest change that fixes it, plus a regression test — never bundle unrelated work into an urgent deploy.
- If a fix touches auth, data, or money, run **"review"** even under time pressure. That's exactly when it's most needed and most skipped.

**Keeping it healthy**
- Patch security advisories promptly; batch routine dependency updates and run the tests.
- Re-run **"perf pass"** after any significant feature addition — performance regresses gradually, not suddenly.
- Rotate keys if anyone leaves the project, or if a key was ever pasted somewhere it shouldn't have been.

**Handing it over** (client work — Gulf/MENA and SE Asia delivery)
- README complete enough that someone else can run it without you.
- Access transferred: repo, hosting, database, domain, third-party services — and confirm the client actually controls the billing, not just the login.
- Env vars documented with what each is for and where the real value lives (never the value itself).
- A short operations note: how to deploy, how to roll back, where errors surface, what to do when the common things break.
- State in writing what is NOT covered. The maintenance boundary is the thing that causes disputes later.

To finalize: run it once on a live project. If client delivery becomes routine, handover earns its own checkpoint and shortcut.

---

## Ongoing — every session ✅

The rhythm that runs regardless of phase.

1. Start a NEW chat → Claude Code auto-reads CLAUDE.md + PROGRESS.md and catches you up.
2. Work — using **"plan"** before anything non-trivial.
3. **"wrap up"** → updates PROGRESS.md, CLAUDE.md, README.md, DESIGN.md as needed (no git action).
4. **"commit"** → reviews what's staged, then commits + pushes with a proper message.

Anytime: **"Q&A"** / **"Q&A short"** to consult without changing code · **"Q&A history"** to see past consults.

---

## Deliberately skipped (would add friction without payoff for solo/small work)

- Heavy CI/CD pipelines, formal architecture decision records, sprint ceremonies. The wrap-up/commit rhythm and CLAUDE.md's Key Decisions section already cover the need.

---

## Build-out order (what's actually left)

1. 🔨 **Build the Taste Library** — the last unbuilt piece, and the foundation the design workflow already assumes exists.
2. 🧪 **Run the entire lifecycle on one real project** — the validation pass. Everything marked 🧪 is a hypothesis about what you'll do under real conditions.
3. ✂️ **Then cut.** After that run, delete the phases and rules you didn't actually use. A shorter lifecycle you follow every time beats a complete one you skip half of.

Guiding principle: consistency beats coverage. Only keep a phase if you'll genuinely run it every project — and the only way to find that out is to run it once.
