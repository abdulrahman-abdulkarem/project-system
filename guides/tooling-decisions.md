# Tooling decisions

Tools decided on but not yet validated on a real project, and tools deliberately
deferred. Nothing here becomes a rule or a checkpoint procedure until it has been
run once on real work — an unvalidated procedure is theory wearing a checklist's
clothes, and that is the failure mode this system exists to prevent.

Move an item into `masters/` only after it has earned its place.

---

## Decided — add when validated

### Playwright CLI
**What it adds that nothing else here does:** repeatable automated checks. Chrome
DevTools MCP lets Claude Code *look* at a running app interactively; Playwright runs
the same checks every time, unattended.

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

**Note:** installing it is a dependency addition, which the always-on rules require
being asked about first.

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

---

## Rejected

- **Google Drive as the working store** — markdown round-trips failed on read.
  GitHub is the store.
