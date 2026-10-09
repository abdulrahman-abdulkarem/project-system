# Tooling decisions

Tools decided on but not yet validated on a real project, and tools deliberately
deferred — except where a decision is already reflected directly in the tooling
check itself (see Active now), which needs no separate validation. Nothing else
here becomes a masters/ rule or checkpoint procedure until it has been run once
on real work — an unvalidated procedure is theory wearing a checklist's clothes,
and that is the failure mode this system exists to prevent.

Move an item into `masters/` only after it has earned its place.

---

## Active now — reflected in the tooling check

### Browser tool: Playwright, not Chrome DevTools MCP
Chrome DevTools MCP is dropped. One browser tool, not two, and it was failing to
connect anyway. Playwright CLI is the preferred route over Playwright MCP — it
drives a real browser directly, without an MCP server loading large tool schemas
and verbose accessibility trees into context on every session, which is exactly
what Playwright's own maintainers recommend for coding agents. Playwright MCP
still works if that's what a project already has configured; the tooling check
reports whichever is actually present rather than failing on the name.

Installing it is still a dependency addition, which the always-on rules require
being asked about first.

### Standard skills
Checked for by name in the tooling step, present/absent, every session:
- **superpowers** — development methodology.
- **supabase** + **postgres-best-practices** — Supabase/Postgres guidance.
- **caveman** — token reduction.
- **impeccable** — design execution and review.
- **grill-me** — interview a loose idea.

---

## Decided — add when validated

### Playwright as a checkpoint tool
Being the standard browser tool (above) is a separate decision from being written
into a checkpoint procedure — that part is still unvalidated. **What it would add
that nothing else here does:** repeatable automated checks, run the same way every
time, unattended, rather than a human clicking through by hand.

**Where it will attach, once proven:**
- `test check` — the testing checkpoint has no end-to-end story at all today.
- `ship check` — run the suite before deploy rather than clicking through by hand.
- `lang check` / `rtl check` — **the highest-value use.** Load the same page in both
  locales, screenshot both, diff them. Mirrored layouts, flipped icons, mixed-script
  title wrapping and bidi punctuation bugs are all things that only surface when the
  two locales are compared side by side. Every RTL finding in the taste library is of
  exactly this class.

**Before writing the procedure:** run it once on a real project. Note what actually
broke, what was slow, and what needed configuring. Write the checkpoint from that,
not from the docs.

---

## Deferred — decided later, not now

- **Vitest** — unit testing. Blocked on dependency approval. The testing checkpoint
  stays generic until something real runs against it.
- **TestSprite** (testsprite.com) — evaluate after Vitest, not before.
- **SEO layer** — a checkpoint or rule set for search visibility. Parked deliberately.
- **Launch / discoverability tooling** — post-launch registration and analytics.
  Parked deliberately.
- **ui-ux-pro-max skill** — worth testing specifically against Arabic/RTL work, which
  is the case its own docs don't cover.
- **next-dev-loop skill** — worth having on its own merits, separately from the
  rejected general-Next.js-best-practices use case below. Not evaluated yet.

---

## Rejected

- **Google Drive as the working store** — markdown round-trips failed on read.
  GitHub is the store.
- **vercel/next.js skill, as a source of general Next.js best practices.** Vercel
  deliberately retired `next-best-practices` as a skill; that knowledge now ships
  in the bundled docs and the AGENTS.md block `next dev` writes on 16.3+. The five
  skills that remain in that repo are Cache Components and partial-prefetching
  adoption, plus a dev-loop skill — not a general-guidance skill, so it doesn't
  fill the job it was being considered for. (`next-dev-loop` specifically is
  listed under Deferred above, on its own separate merits.)
