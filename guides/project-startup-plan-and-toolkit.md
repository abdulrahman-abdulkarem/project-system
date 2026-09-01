# Project Startup Plan & Design Toolkit

Your single reference for starting a project and making it look good. It ties together the prompts you already have, the design workflow, and every tool available — marked core vs optional so you never drag along tools a project doesn't need.

Principle throughout: **consistency beats coverage, and taste beats tools.** A lean workflow you follow every time, driven by your own taste, beats a big toolkit you half-use.

---

## Part 1 — The startup sequence (what to do, in order)

**1. Kickoff.** Run the right prompt for the situation:
- New project, one device → `new-project-kickoff-prompt.md`
- New project, two devices → `new-project-cross-device-prompt.md`
- Existing project, two devices → `existing-project-setup-prompt.md`
- Setup got interrupted / half-done → `repair-setup-prompt.md`

Let it finish ALL steps (it ends with a "setup complete" confirmation) before you start building. The kickoff handles stack, context files, rules, git, and — for UI projects — the design-direction step.

**2. Design direction (UI projects).** Before building UI, settle the look using the design workflow in Part 2. Output lands in DESIGN.md. Don't skip this — it's the #1 reason AI UIs come out generic.

**3. Build.** Work feature by feature. Say **"plan"** before anything non-trivial. If the feature needs new tables or columns, run **"schema check"** before writing the migration — the data model is the most expensive thing to change later. Review diffs before accepting; never blind-accept, especially anything touching logic or security config.

**4. Review & polish.** Use impeccable's critique/audit/polish on real screens. Verify in a real browser (RTL + mobile + console), not just a passing type-check.

**5. Performance pass (before shipping).** Run Lighthouse for a baseline score, then work through the checklist in Phase 7 of `project-lifecycle-playbook.md`: edge/CDN delivery, correct caching (Cache-Control/ETag/immutable assets), lean CSS and JS (remove unused, code-split, tree-shake, defer), subsetted + preloaded fonts, modern image formats + responsive sizes. Re-run Lighthouse after. This checklist is drafted but not yet validated on a real project — treat the first run as a test of the checklist itself.

**6. Ship, then keep running it.** "ship check" before deploying. After launch the project enters Phase 9 of the lifecycle playbook — error reporting, hotfix discipline, dependency updates, and (for client work) handover: transferred access, documented env vars, an operations note, and a written maintenance boundary.

**7. Session lifecycle.** "wrap up" (updates docs) → "commit" (pushes) at the end of each session. On the next device: git pull → new chat → it catches you up.

---

## Part 2 — The design workflow (how to make it look good)

This is the heart of it. It came from real experience (the ArabGo refresh) plus the Chase AI "Web Design Genius" method. The order matters.

### Step 1 — Curate a Taste Library (do once, reuse forever)
Your taste is the moat. You can't brief "make it look good" — but you CAN collect examples of good and hand those over.
- Collect 15–30 designs you genuinely react to, from Dribbble, Land-book, Godly, Pinterest, X/Twitter, or just screenshots of sites that stop your scroll.
- Save both **screenshots AND live URLs** (real sites beat static images for conveying feel).
- **Group by design family, not by project** (e.g. "warm editorial," "clean minimal," "bold brutalist"), and include Arabic/RTL examples since that's your context.
- For each, note its **vocabulary** — the words the style is made of ("warm paper ground," "halftone texture," "serif + mono mix," "soft layered shadows"). These keywords drop straight into prompts.
- Reuse this library at the start of every project. It grows over time and compounds.

### Step 2 — Set direction with the 4-Part Prompt
When briefing a design (to impeccable or Claude Code), give four inputs:
1. **Aesthetic** — which family from your Taste Library you're aiming for.
2. **Reference** — 2–3 specific screenshots or live URLs. Match the *feel*, never copy.
3. **Intent** — what it is, who it's for, what they should do (the primary action).
4. **Guardrails** — explicit ALWAYS / NEVER lists to kill slop before it renders (e.g. NEVER: blue-purple gradients, Inter everywhere, emoji as icons, identical card grids, evenly-distributed rainbow palettes. ALWAYS: one deliberate accent, real contrast, your brand colors, RTL-correct).

### Step 3 — Cast wide, don't one-shot
One-shotting is the prompt lottery. Instead:
- Generate the page/section in **a few distinct aesthetic directions side by side**, pick the strongest.
- Then generate **2–3 variants** of the winner.
- Then **tweak** (fonts, colors, spacing, motion) in small moves.
- Wide beats deep: seeing options on one screen lets you compare instead of guess.

### Step 4 — Iterate visually, never in the dark
- Refine against what you SEE, not what you imagine. Screenshot, judge, adjust.
- Nail the hero first, then transitions/rhythm, then motion, then details.
- Feed it more references whenever it drifts. Always end where it "feels like you."

### Step 5 — Add motion, last and on purpose
Motion comes AFTER the static design is right. A page that isn't good standing still doesn't become good by moving. Two rules govern everything here: **great animations don't distract, they guide**, and **pick the interaction first, then pick the technique** — never the reverse.

**Register test before anything moves.** Your DESIGN.md already asks whether a project is a *product surface* (workflows, task completion) or a *brand surface* (visual storytelling). This is where that answer pays off:
- **Product surface** (a directory, a dashboard, a booking flow): motion is functional only — reveals, state feedback, focus and transition continuity. Anything that takes control of the user's scroll is a bug, not a feature. ArabGo lives here.
- **Brand surface** (a studio site, a launch page, a portfolio): the expressive scroll techniques below are on the table, because being memorable *is* the job.

**Scroll-effect decision table** — need this, use that:

| The interaction you need | Technique | Cost / caution |
|---|---|---|
| Reveal content as it enters the viewport | **Scroll trigger** | Cheapest and safest. The default; usually the only one a product surface needs. |
| Hold one element fixed while the rest scrolls past | **Pin** | Expensive. Reserves layout space, breaks often on mobile, edges toward scroll-jacking. |
| Depth and atmosphere from layers at different speeds | **Parallax** | Foreground ≈1.4x, midground 1.0x, background ≈0.5x. Subtlety is the whole game. |
| Move content sideways while the user scrolls down | **Horizontal scroll** | Hijacks a scroll axis. **Must be mirrored in RTL.** Good for showcases/galleries, bad for tasks. |
| Show how far through the page someone is | **Scroll progress** | A utility (reading/progress indicator), not decoration. Cheap and genuinely useful on long content. |
| Tie animation progress frame-by-frame to scroll position | **Scroll-linked (scrub)** | The most expensive. Every scroll event drives a render — keep it to transform/opacity. |

**Guardrails — these are the part the technique lists leave out:**
- **`prefers-reduced-motion` is not optional.** Every effect above needs a reduced-motion path that still delivers the content. Motion Primitives respects it by default; hand-rolled GSAP does not — you wire it yourself.
- **RTL mirrors motion too.** Vertical reveals and parallax are direction-agnostic; anything on the X axis is not. A horizontal scroll or slide-in built with `translateX` runs the wrong way under `dir="rtl"`. Treat motion direction as part of RTL-native, not a retrofit — the same rule already applied to layout.
- **Animate `transform` and `opacity`, nothing else.** Animating width/height/top/left forces layout on every frame — the exact layout thrashing the performance pass tells you to remove.
- **Motion is JS weight.** GSAP + ScrollTrigger is a real bundle cost on a stack that already ships Framer Motion. Lazy-load animation code that only runs below the fold, and count it against the "ship only what the user needs" rule.
- **Never make content reachable only through an animation.** If a scroll trigger doesn't fire — no JS, a crawler, a screen reader, reduced motion — the content must still be there and readable.
- **Don't animate the LCP element.** Fading in the hero delays the largest paint you just spent a performance pass optimizing.
- **Pin and scrub need a mobile verdict.** Both are where "works on my 27-inch monitor" fails hardest. Check on a real phone viewport before keeping them.

### Step 6 — Verify
- Real browser check: RTL + mobile + console (a clean type-check is not proof it renders well).
- Contrast numerically (WCAG AA), 44px touch targets, semantic markup, visible focus.
- If anything moves: re-check with reduced motion enabled, confirm X-axis motion mirrors in RTL, and confirm the page still works with JS disabled or a trigger that never fires.

---

## Part 3 — The toolkit (everything available, honestly categorized)

### CORE — use these on essentially every project
- **Your prompt set** (kickoff / cross-device / existing / repair) — the foundation, rules, and shortcuts. Already built and battle-tested.
- **impeccable** (installed) — the design engine. `init` (set direction + DESIGN.md), `critique`/`audit` (scored review), `polish`/`bolder` (refine/add impact), `craft` (build), `adapt`/`typeset`/`clarify` (targeted fixes). Runs in the VS Code Claude panel or CLI. Nearly 50K stars; the strongest design skill available.
- **Your Taste Library** — the reference bank you build in Part 2. Not a tool to install, a practice to maintain. Highest-leverage thing you own for visual quality.

### OPTIONAL — know they exist; use only when a project actually needs them
- **21st.dev** — a library of copy-paste UI component prompts/snippets (buttons, cards, pricing sections, etc.). Use when you need a specific, well-designed component fast and don't want to design it from scratch. Not a workflow, a lookup — reach for it per-component, not per-project.
- **Taste Skill v2** — another design skill (layout/type/motion/spacing). SKIP by default: running it alongside impeccable means two general design engines competing. Only try it if impeccable ever falls short on a specific need (e.g. motion), and use it scoped to that.
- **Higgsfield MCP / image generation** (gpt-image for stills, SeaDance for video) — generates hero imagery inside Claude Code. YOU CURRENTLY DON'T WANT THIS (styling-only, no imagery). Documented only so you know it exists if that ever changes.
- **Tweaks bar** — ask Claude to build a live in-browser controls panel (fonts, sizes, colors, motion) so you tune visually instead of guessing in chat. Nice for heavy visual iteration; skip for small jobs.
- **Component taste references** — collecting examples of borders, backgrounds, pagination styles etc. you'd never think to prompt. A niche extension of the Taste Library; optional.

### ASSET SOURCES — materials to pull from once direction is set (not workflow, not a substitute for taste)
These give you raw materials (backgrounds, motion, components, icons). Rule: set direction in DESIGN.md FIRST, then pull only pieces that match it. Grabbing shiny assets that don't fit your system is how a page ends up inconsistent.

- **Haikei** (haikei.app) — generates SVG backgrounds, gradients, waves, blobs, textures. Free, no signup, exports clean SVG. Solves "flat backgrounds / need depth without photos" — pairs directly with the styling-only design brief. Use it to create warm gradient or layered-shape hero/section backgrounds in your brand colors.
- **Motion Primitives** (motion-primitives.com) — copy-paste animated React components (Framer Motion + Tailwind + Next.js, your exact stack). Solves "animation is weak/missing." Your go-to motion source; production-ready and respects prefers-reduced-motion. Add motion after the static design is right, not before.

- **The animation stack — add in this order, and only as far as you actually need:**
  1. **Framer Motion** (already in your stack, via Motion Primitives) — component and UI motion: enter/exit, layout transitions, and scroll-triggered reveals through `whileInView`. This covers the entire motion need of a product surface. **Start here and usually stop here.**
  2. **GSAP + ScrollTrigger** — the timeline engine. The only reasons to add it: pin, scrub/scroll-linked animation, or a horizontal-scroll timeline. If you're not building one of those three, it's bundle weight for nothing. Note it's a second animation library alongside Framer Motion — justify it per project, don't install it by default.
  3. **Lenis** — smooth/inertial scrolling. A pure feel upgrade for brand surfaces. It overrides native scroll behavior, which can fight the user's OS settings and assistive tech, so skip it on anything task-oriented.
  4. **Three.js** — 3D. Out of scope for directory/product work and a large bundle; documented only so the category isn't a blank spot.
- **Component libraries** — copy-paste React blocks/components for when you need a specific well-designed piece fast (buttons, cards, pricing, dashboards):
  - 21st.dev, and Watermelon UI (ui.watermelon.sh) — both Tailwind/shadcn, same category. PICK ONE as your primary so you're not hopping between two overlapping sources; the other is a fallback. Reach for these per-component, not per-project.
- **Icon set** — a consistent icon system is the fix for the emoji-as-icons problem. Options: lucide (already in your codebase), Koboyo (koboyo.com/icons). PICK ONE primary icon set per project and use it everywhere — never mix icon sets (mixing is the exact inconsistency impeccable flags). Since lucide is already installed, default to it unless a project has a reason to switch wholesale.

### SKIP — not worth the friction for solo/small work
- Heavy CI/CD pipelines, formal architecture-decision-record processes, sprint ceremonies. Your wrap-up/commit rhythm already covers the need.

### EVALUATED AND SKIPPED — the tool anti-reference list
The same logic as design anti-references: recording *why* something was rejected stops you re-litigating it in six months, and tells you what would have to change for the answer to flip.

- **Lordicon** (animated icons, Lottie-based) — *skipped, Aug 2026.* Three reasons, in order of weight: (1) the free tier is personal-use-only with mandatory attribution, so commercial and client work needs the paid plan (~$16/mo or $96/yr; icons downloaded while subscribed stay usable forever with full rights); (2) it would mean running a second icon system alongside lucide, breaking the one-icon-set rule, and it has no static-icon story to replace lucide wholesale; (3) Lottie animates path data frame-by-frame on the main thread and ships its own runtime, which contradicts both "animate transform and opacity only" and "ship only what the user needs". Animated icons also read playful-consumer rather than premium-trustworthy — none of the Airbnb / Houzz / Careem references animate their icons. **What would flip it:** a brand-surface project wanting two or three expressive moments. Then buy one month, export those specific icons, cancel. A purchase, not a system. **The cheaper substitute:** animate a lucide SVG directly with Framer Motion or CSS — transform/opacity only, no dependency, no licence, one icon system.

---

## Part 4 — Quick-start checklist for a new UI project

1. Run the right kickoff prompt; let it finish fully.
2. Open your Taste Library; pick the design family and 2–3 references for this project.
3. Give impeccable the 4-Part Prompt (Aesthetic + Reference + Intent + Guardrails); run `init` to write DESIGN.md.
4. Craft the hero in a few directions; pick one; refine.
5. Build the rest against DESIGN.md, section by section, reviewing diffs.
6. `critique`/`polish` on real screens; verify in browser (RTL + mobile + console).
7. Pull matching assets only as needed: Haikei for backgrounds/depth, Motion Primitives for animation, a component library (21st.dev / Watermelon UI) for specific blocks, one icon set (lucide by default). Only pieces that fit DESIGN.md.
8. Motion last, if at all: settle the register (product vs brand surface), pick the interaction before the technique, then add the smallest effect that does the job — with reduced-motion, RTL-mirroring, and transform/opacity-only as non-negotiables.
9. Performance pass before shipping — Lighthouse baseline → the Phase 7 checklist (delivery, caching, CSS/JS trim, font subsetting, image formats) → re-measure.
10. "wrap up" → "commit" each session.

## Honest reminders
- Tools don't create taste; they execute it. The Taste Library + references are what actually move quality — the rest is machinery.
- Don't add a tool because it exists. Add it because a specific project needs it. Everything in "Optional" is opt-in for a reason.
- Review every change, especially logic and security config. A tool that self-verifies is good; your review is still the last gate.
