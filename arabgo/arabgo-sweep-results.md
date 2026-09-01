# ArabGo Checkpoint Sweep — Results

Consolidated report of five checkpoints run against the current state of the codebase
(branch `system-upgrade`, working tree clean). Nothing was fixed — this is a findings
report only, per the checkpoints' own rules.

**A note on timing:** no wall-clock timestamps were logged during the session, so exact
elapsed time per checkpoint isn't available and is not estimated here. As a rough proxy
for effort/scope, each section instead lists what the check actually required (files
read, greps run, whether a sub-agent was spawned) — treat that as a relative-effort
signal, not a duration.

---

## 1. Data model checkpoint — `schema check`

**Scope:** `prisma/schema.prisma` cross-checked against actual applied migrations in
`prisma/migrations/`. Direct file reads + a few targeted greps, no sub-agent.

### Should fix
- **Empty, broken migration folder** — `20260618000001_add_phone_verifications/` has no
  `migration.sql` at all.
- **Schema drift** — migration `20260501000001_add_user_phone` added `users.phone` to the
  live DB, but `schema.prisma`'s `User` model has no `phone` field (only `whatsapp`).
  Orphaned/undocumented column.
- **`ServiceProvider.countryId` duplicates `city.countryId`** — nothing enforces the two
  stay in sync; same risk on `City.stateId` vs `City.countryId`.
- **`AdminLog.admin` cascades on delete** — deleting an `Admin` erases their entire audit
  trail, defeating the purpose of an audit log.
- **Missing index on `ProviderCategory.categoryId`** — "providers in category X" (a core
  browse query) can't use the composite PK efficiently.
- **No trigram/GIN index behind Arabic search** — `buildSearchWhere` compiles to
  `ILIKE '%term%'`, which no existing index can serve; will degrade at scale.

### Worth noting
- `Review.rating` has no DB-level CHECK constraint (app-only validation).
- `Admin.permissions` is a free-form `String[]` instead of a constrained enum, unlike
  every other categorical field in the schema.
- Timestamps are `TIMESTAMP(3)` (no timezone), not `timestamptz`.
- `site_visits` / `admin_logs` are unbounded with no pruning/archiving plan.
- No Postgres RLS — access control is entirely application-layer (consistent with how
  the project uses Prisma, just stated explicitly per the checklist).
- No soft-delete strategy — deleting a provider hard-cascades and destroys its reviews/
  reports/images permanently.

### Sound
Real FKs throughout, correct junction tables (`ProviderCategory`, `Favorite`), DB-level
`UNIQUE` used properly, constrained enums for provider status/type/etc., and delete
behavior is deliberate everywhere except the `AdminLog` case above.

---

## 2. RTL / i18n / Accessibility checkpoint — `rtl check`

**Scope:** whole-codebase sweep across public + spot-checked admin surfaces. Delegated to
one Explore sub-agent (full checklist, ~14 priority files + repo-wide greps) because the
scope exceeded a few direct lookups.

### Should fix (bugs)
- **Three "back" links point the wrong way** — `ArrowLeft` used for "back to home" /
  "back to login" in `login/page.tsx` (×2) and `register/page.tsx`, while every other
  back-navigation control in the app correctly uses `ChevronRight`/`ArrowRight`.
- **Mismatched arrow + hover motion** on the social-links row in
  `providers/[slug]/page.tsx:433` — `ArrowRight` + rightward nudge where the matching
  pattern elsewhere uses `ChevronLeft` + leftward nudge.
- **Systemic `uppercase`/`tracking-wide` on Arabic text** — ~30+ hits, including the
  step-section headings duplicated across all four copies of the provider form
  (`PublicProviderForm`, `ProviderForm`, `UserProviderEditForm`, `ProviderConfirmClient`),
  Footer headers, provider detail labels, and most admin table headers.
- **Unlabelled form inputs in `PublicProviderForm.tsx`** — most `<Input>`/`<input>` +
  `<Label>` pairs have no `htmlFor`/`id` link and no `aria-label`; the file's own
  `<select>`/file inputs do this correctly, so it's an internal inconsistency. Likely
  repeated in the other three form copies (not individually confirmed).
- **Duplicate `<h1>`** on the home page (two sibling `<h1>` elements forming one visual
  headline).
- **Icon-only controls missing one of the two required attributes** (`aria-label` +
  `title`): `MobileNav.tsx` hamburger, `UserMenu.tsx` trigger, `register/page.tsx`
  password toggle.
- **Inconsistent list semantics** — home page's featured/category grids use plain `<div>`
  where `providers/page.tsx` correctly uses `<ul role="list">`/`<li>` for the same kind
  of collection.

### Worth noting
- No consistent numeral convention — Western digits used for data (counts, prices,
  dates), Arabic-Indic digits used for step badges and a couple of admin labels.
- One English "e.g." inside an otherwise-Arabic placeholder.
- `CategoryList.tsx`'s expand chevron direction is a judgment call, not clearly wrong.
- A few corner-placement choices (`MapView`, `AdCarousel`) are arbitrary but not broken.

### Sound
Root `dir="rtl"`/`lang="ar"` correct; Cairo font genuinely applied everywhere (zero
`font-sans` overrides found on Arabic text); most leading-icon/trailing-action and
forward/back chevron pairs across the app are correctly RTL-oriented; heading hierarchy
is clean on every other page checked.

### Audit boundaries
Categories, map, favorites, profile, join, report, and static pages were only
grep-swept, not individually read; the label bug was confirmed in one of four form
copies and is suspected (not verified) in the other three.

---

## 3. Performance checkpoint — `perf pass`

**Scope:** static analysis only — this environment has no `node`/`npm`/`npx` and no
Chrome/Edge binary, so `next build` and Lighthouse could not be run. Findings below are
from reading `next.config.js`, `ProviderCard`/`AdCarousel`/page files, and dependency
usage, not from a measured baseline.

### Should fix
- **Home page's featured `ProviderCard` grid has no `priority` prop**
  (`app/(public)/page.tsx:447`) — almost certainly the LCP element on the highest-traffic
  page, and it's lazy-loaded by default. `providers/page.tsx` does this correctly
  (`priority={index < 3}`); the home page doesn't.
- **`AdCarousel` hardcodes `priority={false}`** — worth re-checking against a real LCP
  trace once the above is fixed, since the `AFTER_STATS` ad sits high on the page.

### Worth noting
- The entire public site opts out of the Full Route Cache/ISR via
  `export const dynamic = "force-dynamic"` on `app/(public)/layout.tsx`, because `Header`
  calls `auth()` on every request. This is a **documented, deliberate** trade-off (the
  code comment explains it), not an oversight — but it's the single biggest lever
  available for CDN/edge caching on this app, and worth a conscious decision rather than
  leaving as the default. Not changed without sign-off.
- No live Lighthouse baseline exists; steps 1 and 8 of the checkpoint ("measure first" /
  "re-measure") are outstanding and need to be run on a machine with Node + Chrome.

### Sound
Heavy dependencies are properly isolated: `dompurify`+`jsdom` only ever imported from
server route handlers, `xlsx` is dynamically `import()`ed at call time, `leaflet`/
`react-leaflet` is loaded via `next/dynamic({ ssr: false })`. Every content image uses
`next/image` (no raw `<img>` found); fonts are self-hosted via `next/font/google` with
explicit weights/subsets (automatic `font-display: swap` + preloading); `remotePatterns`
in `next.config.js` is scoped to `*.supabase.co`, not wildcarded.

---

## 4. Testing checkpoint — `test check`

**Scope:** `package.json` + repo-wide file search for test infrastructure, then targeted
reads of the highest-risk pure-logic files (`lib/otp.ts`, `lib/security/rateLimit.ts`,
`lib/admin-permissions.ts`).

### Blocking / should fix (meets the "must" bar, zero coverage)
- **No test suite exists at all** — no `test` script in `package.json`, no
  `playwright.config.ts` despite `@playwright/test` being installed, and no test files
  anywhere in the repo outside `node_modules`.
- **Authorization logic untested** — admin RBAC (`lib/admin-permissions.ts` + middleware)
  and resource-ownership/IDOR checks (`app/api/providers/[id]/route.ts` and `/mine`) have
  no coverage. This is the checkpoint's own highest-priority category.
- **OTP/token expiry logic untested** — `lib/otp.ts`'s `checkOtp`, `isEmailVerified`,
  `signVerifyToken` are pure, cheaply-testable functions built around HMAC + `Date.now()`
  expiry, with no tests pinning expired/tampered/malformed cases.
- **Rate limiting untested** — `lib/security/rateLimit.ts`'s window-reset-vs-increment
  branch and the 24-hour one-review-per-provider dedupe have no coverage.
- **Duplicate provider-validation schemas unverified against each other** —
  `lib/validations/provider.ts` and `ProviderConfirmClient.tsx`'s own local zod schema
  are meant to accept the same shapes (per project convention) but nothing proves they
  actually do.

### Worth noting (not yet covered, lower priority)
- `lib/utils/search.ts`'s Arabic normalization/synonym expansion has real branching and
  no tests.
- `lib/utils/slugify.ts` is a cheap, deterministic transform worth pinning, especially
  for Arabic input handling.

### Deliberately not worth testing
Styling/visual appearance (covered by the rtl/perf/motion checkpoints instead), Next.js/
Prisma framework behavior itself, trivial pass-throughs like `lib/utils/cn.ts`.

### Recommendation
Offered to scope a minimal Vitest setup for the `lib/` pure-function gaps above — this
needs the user's go-ahead since it's a new dependency (Hard Rule 4). Not started.

---

## 5. Motion checkpoint — `motion check`

**Scope:** full read of `app/globals.css`'s animation system, plus targeted reads of
`CountUp.tsx` and `AdCarousel.tsx` for the no-JS check.

### Should fix
- **`CountUp.tsx` has no no-JS fallback** — starts at `useState(0)` and only reaches the
  real value inside a `useEffect` + `IntersectionObserver` + `requestAnimationFrame`
  loop. Without JS (crawler, no-JS client), the displayed stat is stuck at `0` — the real
  number is never in the DOM. Direct violation of "content must still be there if the
  animation trigger never fires."
- The RTL/motion-direction mismatches already reported under the RTL checkpoint (the
  `ArrowRight`+rightward-nudge row, the three `ArrowLeft`-for-"back" links) apply here
  too, since the wrong transition direction is what makes the wrong icon choice visible.
  Not duplicated in full — see checkpoint 2 above.

### Worth noting
- The `marquee` keyframe always scrolls visually leftward regardless of direction; since
  this app is RTL-only with no LTR variant to mirror against, this isn't actually a
  mirroring bug — flagged only as a judgment call.
- Ambient decorative animations (`float`, `morph`, `gradientShift`, `spin-slow`,
  `pulse-glow`) are used in exactly two files (home page hero, `MobileNav`), staying
  scoped to background decoration rather than competing with task content — reasonable
  for a product surface.

### Sound
The global `prefers-reduced-motion` rule (`globals.css:501-509`) collapses all animation/
transition durations to near-zero for `*` rather than disabling specific classes one by
one — entrance animations still land on their end state, so content isn't hidden under
reduced motion. No motion library dependency exists (pure CSS), so there's no bundle cost
to weigh. No scroll-hijacking technique (pin/parallax/scrub) is used anywhere, so nothing
in that category needed checking.

---

## Cross-checkpoint patterns worth flagging on their own

A few issues surfaced independently from more than one checkpoint, which usually means
they're worth fixing together rather than piecemeal:

- **The four provider-form copies keep drifting from each other** — the `uppercase`/
  tracking bug (RTL check), the unlabelled-input bug (RTL check), and the unverified
  dual validation schemas (testing check) all stem from the same root cause: four
  near-identical copies of the same form with no shared enforcement that they stay in
  sync, beyond the CLAUDE.md convention asking a human to remember.
- **RTL motion-direction bugs** appear in both the RTL checkpoint and the motion
  checkpoint because they're the same underlying defect (wrong icon + wrong transition
  direction) viewed through two different checklists.

Nothing in this report has been changed. Let me know which findings (from any section)
you want acted on and I'll scope those specifically.
