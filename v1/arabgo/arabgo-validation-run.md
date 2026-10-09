# ArabGo Validation Run — testing the system end to end

The point of this is **not** to improve ArabGo. It's to find out which parts of the system survive contact with a real project, so the parts that don't can be cut. Record what happens; the notes are the deliverable.

ArabGo's situation: it already has an OLDER version of the rules in CLAUDE.md, plus impeccable installed with its own DESIGN.md / PRODUCT.md / `.impeccable/`. So this is an **upgrade**, which means `repair-setup-prompt.md` is the right prompt — it's built to reconcile a setup that exists but is incomplete.

---

## Step 0 — Pre-flight (5 minutes, don't skip)

1. **Check what you're actually missing.** Open ArabGo's `CLAUDE.md` and search for `Web and API hardening` and `Design & UI Rules`. Note whether each is present. This is the before-measurement — it tells us how much drift had actually accumulated.
2. **Commit or stash everything.** The upgrade rewrites CLAUDE.md. You want a clean diff and a clean way back.
3. **Branch it:** `git checkout -b system-upgrade`. If the run goes badly you delete a branch instead of unpicking commits.
4. **Start a genuinely fresh Claude Code session.** Your own note from last time: the git `safe.directory` config only takes effect in a new session.

---

## Step 1 — Upgrade the setup

Paste the **full contents** of `repair-setup-prompt.md` into Claude Code, and add this at the end of the same message:

```
ADDITIONAL INSTRUCTIONS FOR THIS RUN:

1. CLAUDE.md already contains an older "Project Rules" section from a previous
   setup. REPLACE that entire section with the new PROJECT RULES above — do not
   merge the two, and do not keep both. Everything else in CLAUDE.md (Summary,
   Tech Stack, Architecture, Key Decisions, Conventions, Environment Setup,
   the Design Context pointer, Things Claude Code Should Know) must be preserved.

2. DESIGN.md and PRODUCT.md already exist, created by the impeccable plugin.
   MERGE into DESIGN.md — do not overwrite it. Keep the named design principles
   and the anti-reference already recorded there.

3. Do not modify anything inside .impeccable/, and do not touch the dev-only CSP
   patch in next.config.mjs.

4. Copy the PROJECT RULES and PROJECT CHECKPOINTS sections VERBATIM. Do not
   summarize, condense, or paraphrase them.
```

Point 4 matters. This is a ~42KB paste asking for ~35KB to be written into two files, and the realistic failure mode is a helpfully shortened version of the rules. That would be a genuine finding about the architecture, so note it if it happens.

---

## Step 2 — Verify the upgrade landed (this is a test, so actually check)

- [ ] `CHECKPOINTS.md` exists at the project root
- [ ] It contains all **seven** checkpoints: Code Review, Testing, Data model, RTL/i18n/Accessibility, Performance, Motion, Ship/Deploy
- [ ] `CLAUDE.md` contains `Web and API hardening` (full Security section survived)
- [ ] `CLAUDE.md` contains `Motion` and `### Testing` under the guidelines
- [ ] `CLAUDE.md` contains the Plan, Review, and Checkpoint shortcuts
- [ ] Only **one** "Project Rules" section exists — the old one is gone, not duplicated
- [ ] `DESIGN.md` still has impeccable's named principles and the 2026-07 anti-reference
- [ ] Nothing in `.impeccable/` changed, and `next.config.mjs` is untouched

Then `git diff` and read it. If anything was paraphrased rather than copied, that's the most important result of the whole run.

Finish the session: **"wrap up"** → **"commit"**.

**Record:** which steps needed correcting, and whether the rules were copied verbatim or reworded.

---

## Step 3 — The read-only checkpoint sweep (new session)

These all report without changing code, so they're safe to run back to back and they'll tell you fast whether a checkpoint earns its place. Run each, save the output, and don't fix anything yet.

1. **"schema check"** — ArabGo has Prisma/Supabase with real data. This is the one I'd most expect to surface something you'd otherwise ship.
2. **"rtl check"** — the highest-signal checkpoint for this project specifically. It should re-find the things you already fixed (good — it validates the checkpoint) plus anything new.
3. **"perf pass"** — needs a Lighthouse run for the baseline. Do it against the deployed site, not just local dev.
4. **"test check"** — ArabGo has essentially no tests, so expect a large "uncovered that meets the must bar" list. The useful question is whether the list is *right*, not whether it's long.
5. **"motion check"** — the hero has motion from the impeccable pass. This checks the register test and the RTL-mirroring guardrail against real code.

**Record for each:** how many findings, how many were real, how many were noise, and how long it took. A checkpoint that returns twenty findings of which three matter is worse than one that returns three.

---

## Step 4 — One full build loop (new session)

Pick the smallest real finding from Step 3 — ideally the unfinished hero work (gold as a proper token, remove the scattered decorative shapes, restrain the headline to one hue plus one gold accent).

1. Say **"plan"**. Does the plan add anything, or is it ceremony on a small change?
2. Let it build.
3. Say **"review"**. Does it catch anything you'd have missed?
4. Verify in a real browser: RTL, mobile, console.
5. **"wrap up"** → **"commit"**.

This exercises the loop you'll use every day. If `plan` and `review` feel like friction on a change this size, that's a real finding — the rules should say when to skip them.

---

## Step 5 — Report back

Bring me:

1. **The before-check** from Step 0 — was ArabGo's CLAUDE.md actually missing the design and security sections?
2. **Verbatim or paraphrased?** The single most important architectural result.
3. **Per checkpoint:** findings count, real vs noise, time taken.
4. **What you skipped and why.** This is the most valuable data in the whole run — it drives the "then cut" step.
5. **Anything the system got wrong**, especially any rule Claude Code ignored despite it being in CLAUDE.md. A rule that's present but unfollowed is worse than no rule, because it creates false confidence.

---

## Known gotchas for this project

- Project lives inside OneDrive (`OneDrive\Documents\GitHub\ArabGo`) — git/tooling "unsafe location" quirks. `git config --global --add safe.directory "*"` then a **fresh** session.
- impeccable is invoked as `/impeccable:impeccable <command>`, not `/impeccable:<command>`.
- Env file is `.env.local` (Next.js), not `.env`.
- Console errors from browser extensions look like CSP/stylesheet failures. Test in incognito before believing them — this nearly caused a CSP weakening last time.

---

# RESULTS — run completed 2026-08-23

**Verdict: the system passed.** Every phase that was marked 🧪 has now been exercised once on real code. Four fixes were made to the masters as a direct result.

## Session 1 — upgrade the setup

- **Drift confirmed in the wild.** ArabGo's CLAUDE.md was missing `Design & UI Rules` entirely and had the 4-line Security stub instead of the full section. `HARD RULES` *was* present, so this was genuine drift from the old `existing-project-setup-prompt.md`, not a failed setup. ArabGo had been built for weeks against a rules file with no design lessons and almost no security section.
- **Verbatim copy held at 45KB.** No condensation, no paraphrasing, no summarising. The self-contained-prompt architecture survives at this size — that was the main open architectural question.
- All 7 checkpoints written to CHECKPOINTS.md. Exactly one rules block; the old one was replaced, not merged.
- Deviations: the QA.md template was rendered as a fenced code block (better than the spec asked for), and `Project Rules` landed as H1 rather than H2 (cosmetic).
- Stack-specific rules were genuinely project-specific — Next.js App Router, Prisma, NextAuth v5, zod, Supabase Storage, Arabic/RTL, rate limiting.

## Session 2 — checkpoint sweep

Low noise across the board. It changed nothing, refused to add Vitest without permission (Hard Rule 4), stated its own audit boundaries, and distinguished a documented deliberate trade-off (`force-dynamic`) from an oversight.

- **`schema check`** — an empty migration folder with no `migration.sql`; schema drift (`users.phone` live in the DB, absent from `schema.prisma`); `AdminLog` cascading on admin delete, which erases the audit trail; missing index on a core browse query; `ILIKE '%term%'` Arabic search with no trigram index. Paid for itself on first use.
- **`rtl check`** — 30+ `uppercase`/`tracking` on Arabic (the very first lesson ever banked, still live across four copies of the provider form); three `ArrowLeft` back-links pointing the wrong way in an RTL app; unlabelled inputs; duplicate `<h1>`; icon-only controls missing accessible names.
- **`perf pass`** — **partially blocked.** No Node, so no Lighthouse and no baseline. Still caught a real one statically: the home page's featured `ProviderCard` grid has no `priority`, while `providers/page.tsx` sets `priority={index < 3}`. Outstanding: re-run now that Node exists.
- **`test check`** — zero test infrastructure. Named the right targets: admin RBAC, IDOR, OTP expiry, rate limiting. The "must test" tiering worked as designed.
- **`motion check`** — `CountUp` had no no-JS path; the stat rendered as `0` for crawlers and no-JS clients. Correctly judged the `marquee` direction a non-issue on an RTL-only app rather than padding the report.
- **Best output wasn't asked for:** it identified that three findings across two checkpoints share one root cause — four near-identical provider forms with nothing keeping them in sync. Same disease the four prompt files had.

## Session 3 — build loop

- **`plan` scored 6/6** against its own rule: goal in one sentence, approach, alternative named *and rejected with a real reason* (`<noscript>` rejected because it doesn't cover hydration failure, only true no-JS), files listed, risk flagged, stopped and waited. Not ceremony — it produced a genuine decision on a small change.
- It also spotted that `CountUp` lacks a `prefers-reduced-motion` path (a rule violation) and **scoped it out rather than silently expanding the task**.
- Fix verified in a real browser with JavaScript disabled: real numbers render. 
- `commit` noticed unrelated `package-lock.json` drift and asked instead of sweeping it in — scope discipline working. Committed separately.

## Fixes made to the masters as a result

1. **QA.md template** indented as a code block with an explicit "not part of this document" note — removes reliance on the model choosing a sensible fence. (Robustness, not a defect: Claude Code had already handled it correctly.)
2. **`perf pass` must declare when it can't measure** — say so at the top, do the static pass, list measurement as outstanding. A static-only pass reported as complete is worse than not running it.
3. **All checkpoints must state audit boundaries** (read vs grep-swept, confirmed vs suspected) — it did this unprompted and it was valuable enough to mandate.
4. **All checkpoints must name shared root causes** rather than reporting the same defect through two lenses.

## Process findings (about the method, not the system)

- A grep is not a parser. `Select-String -Pattern "^#+ "` reported code-fenced lines as headings and produced a false positive. Same family as "a passing type-check is not proof" — verify structure with something that understands structure.
- **Node was never installed on this machine.** ArabGo had been developed entirely against Vercel deploys. This blocked the type-check, Lighthouse, and any possibility of running tests. Now installed.

## Open items

- [ ] Merge `system-upgrade` into main (branch has: rules upgrade, CountUp fix, lockfile).
- [ ] Re-run `perf pass` with Node available, for a real Lighthouse baseline.
- [ ] ArabGo's CHECKPOINTS.md is one version behind (pre-tiering, pre-boundaries). Refresh when convenient.
- [ ] `CountUp` still has no `prefers-reduced-motion` path — deliberately scoped out, still owed.
- [ ] The cut pass: decide which checkpoints stay. Current read — `schema check` and `rtl check` clearly earn their place; `test check` is right but blocked until a test runner exists; `perf pass` is unproven until it measures once.

---

# ADDENDUM — 2026-08-24

## Merge to main: the silent failure

Merging `system-upgrade` into main hit a conflict in PROGRESS.md, resolved fine — and then git **silently discarded the entire point of the branch**. Main's history contained `Revert accidental setup commit on main`, so from git's view the removal of CLAUDE.md's rules and CHECKPOINTS.md was intentional, and a clean merge preserved it. `git status` said "All conflicts fixed."

Caught only because we verified content rather than trusting the merge: `Test-Path CHECKPOINTS.md` → `False`, `Web and API hardening` → `0`, `Design & UI Rules` → `0`. Restored with `git checkout system-upgrade -- CLAUDE.md CHECKPOINTS.md` before concluding the merge.

**Rule added:** *DON'T assume a merge kept your work.* The only failure in this whole run that announced nothing. Every other problem raised an error; this one reported success.

## Build-script bug

`extract()` skipped a fixed number of banner lines after the BEGIN marker — correct for `project-rules.md`, wrong for `project-checkpoints.md`, so two stray comment lines leaked into all four prompts at the rules/checkpoints seam. Now skips the whole comment banner however long it runs. Found while generating a standalone CHECKPOINTS.md, not by reading the prompts.

## Cross-device gap

`E:\prompts` (the system) lives on the laptop; the code lives on the PC. Instructions of the form "read from E:\prompts" fail on the PC, and files have been moved by hand. **The system that teaches cross-device sync isn't itself synced.** Fix: make the prompts folder a git repo. Outstanding.

## `perf pass`, re-run with Node available — the headline result

The checkpoint passed its own new rules cleanly: it opened with a **Coverage** statement, named what it couldn't test (edge/CDN caching isn't testable locally — Vercel handles it in prod), and marked one claim **Suspected** rather than Confirmed because Lighthouse's LCP-element attribution errored.

Real measurement, production build, three pages:

| Page | Performance | LCP |
|---|---|---|
| `/` | **76** | **6.0s** |
| `/providers` | 96 | 2.6s |
| `/login` | 82 | 4.8s |

Same server — so this is page-specific, not infrastructure. The trace shows **3.0s of main-thread work** on `/`, split roughly evenly between Style & Layout (1.1s) and paint/composite (1.1s). Prime suspect: the **`blur-[96px]` / `blur-[64px]` ambient gradient blobs** scattered through the stats, categories and "why ArabGo" sections. `filter` and `backdrop-blur` are expensive to rasterise and there are many above the fold.

Second finding: **`LogoMarquee` server-renders up to 144 `<Image>` nodes** (SSR default `sets = 6`, each repeating the full logo set) before `useLayoutEffect` recalculates for the viewport. Home page DOM is 839 elements. Same architectural smell as the CountUp bug — SSR one thing, correct it in an effect.

### The important lesson

The **static-only** perf pass had confidently blamed a missing `priority` prop on the home page's `ProviderCard` grid — "almost certainly the LCP element." Measurement says otherwise: the delay is main-thread rasterisation from decorative blurs, not image loading. A plausible, well-reasoned, **wrong** diagnosis, corrected only by measuring.

That is the concrete justification for "measure first," and it also converges with the design work: those same decorative blobs were already on the list to remove for *visual* reasons (scattered floating shapes cheapening the hero). Two checkpoints, two different lenses, one root cause — and now with a 20-point Lighthouse gap attached to it.

**Rule added:** measure more than one page; a slow page beside a fast sibling on the same infrastructure isolates page-specific causes from infrastructure ones immediately.

## Second build loop — the decorative blurs

`plan` caught an error in **my** brief. I had conflated the hero's large blurred blobs with the "scattered floating shapes" from the original ArabGo notes; DESIGN.md documented the blobs as the *correct, intentional* depth technique, and the scattered shapes were actually small dots in the CTA section. It refused to guess, laid out both readings, and asked. Scope discipline working against a badly-worded instruction.

Fix: replaced `filter: blur()` on the two hero blobs with `radial-gradient` fading brand colour to transparent — visually near-identical, no GPU rasterisation — and dropped `animate-morph` from those two elements (it animated `border-radius` on an infinite loop, repainting every frame, against the transform/opacity-only motion rule). DESIGN.md §2 updated to match. Hero verified in browser: still warm, mobile fine.

### It corrected its own earlier finding, unprompted

Re-measuring after the fix, the headline "LCP 6.0s / Performance 76" **did not move** (6.046s → 6.054s). Digging into the raw trace: that figure is Lighthouse's *simulated mobile* estimate — 4× CPU slowdown, throttled 4G, `throttlingMethod: "simulate"`. The observed numbers tell a different story:

| | before | after |
|---|---|---|
| Real observed LCP | 1.58s | 1.46s |
| Main-thread Style & Layout | 1142ms | 970ms |
| Main-thread paint/composite | 1093ms | 837ms |
| Total main-thread work | 3.0s | 2.5s |

So the fix genuinely worked — ~17% less main-thread work, ~120ms faster real LCP — but the blobs were never the dominant cause of the *simulated* 6s figure, which is mostly modelled network latency (562ms simulated request latency × the render-blocking CSS chain).

**Why the correction was clean rather than embarrassing:** the original claim had been marked **Suspected**, not Confirmed, because the LCP-element gatherer errored and only circumstantial evidence was available. The audit-boundaries rule added the day before is what made the finding correctable instead of load-bearing. That rule has now paid for itself.

**Rule added:** *Know which number you're reading.* Lighthouse's headline is a simulated-mobile model; the same trace holds real observed values. Report both and say which one a change is meant to move.

Render-blocking CSS delivery chain logged as a separate follow-up, not bundled.

## Running tally of fixes produced by this validation run

1. QA.md template indented as a code block (robustness).
2. `perf pass` must declare when it can't measure.
3. All checkpoints must state audit boundaries.
4. All checkpoints must name shared root causes.
5. *DON'T assume a merge kept your work* — the only silent failure in the run.
6. `build-prompts.py` `extract()` leaked banner lines into all four prompts.
7. Measure more than one page.
8. Know which number you're reading (simulated vs observed).

## Still open

- [ ] Install CHECKPOINTS.md v3 in ArabGo (v2 is current there; v3 adds the two measurement rules).
- [ ] Make `E:\prompts` a git repo — the system that teaches cross-device sync still isn't synced.
- [ ] `CountUp` still owes a `prefers-reduced-motion` path.
- [ ] Render-blocking CSS chain on the home page.
- [ ] **The cut pass** — decide which of the seven checkpoints stay. Current read: `schema check`, `rtl check` and `perf pass` have all earned their place on evidence; `motion check` found one real bug; `review` and `plan` both produced genuine value on small changes; `test check` is correct but blocked until a runner exists; `ship check` is still entirely unexercised.
- [ ] **Launch & discoverability** (new, parked): domain/DNS/SSL, Search Console + Bing verification, sitemap submission, analytics installed *and confirmed receiving*, error tracking, uptime monitoring. Plus a tool menu — one per category, chosen deliberately, recorded in the project. Placeholder added to Phase 9 of the playbook.
- [ ] **SEO layer** (hinted, parked): beyond the basics already in `ship check` — structured data, Arabic keyword strategy, hreflang for bilingual, Core Web Vitals as a ranking input. Overlaps heavily with `perf pass` and the bilingual Part C work.
