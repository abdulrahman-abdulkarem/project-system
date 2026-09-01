# ArabGo — Visual Refresh Brief (for impeccable)

Hand this to impeccable as the design direction for a visual refresh of ArabGo. The goal is a **meaningful visual refresh that keeps the existing structure, content, and layout** — not a rebuild and not new imagery. Every current section stays; what changes is the visual styling: color, depth, typography, spacing, and treatment.

## The problem to solve
The site is structurally complete but visually flat: monotone, low contrast in visual interest, low impact. It should feel warm, spacious, trustworthy, and premium — while remaining a fast, clear Arabic-first (RTL) directory. The fix is purely stylistic — no new photos or images.

## Target feeling (from the owner's references: Airbnb, Houzz, Careem)
- **Warm and human**, not corporate or sterile.
- **Spacious and confident** — generous whitespace, larger type, clear hierarchy, nothing timid or cramped.
- **Trustworthy** — this is a directory whose whole value is trust; the design should feel credible and cared-for.
- **Premium but approachable** — polished, not flashy.

## Brand color palette (from the ArabGo logo — use these exact roles)

The visual system must be built from the brand's own three colors, with GOLD as the warmth/premium driver:

- **Brand Blue** (primary, trust): approx #1848A8 / #3060A8 — the "Arab" text and pin. Use for primary actions, links, and the main interactive/selected signal.
- **Brand Green** (secondary, fresh/approachable): approx #309030 / #2E9E44 — the "go" text and swoosh. Use as a supporting accent (success, secondary highlights).
- **Gold / Warm accent** (premium warmth): use **#FBD060** (rgb 251, 208, 96) — a warm, bright, soft gold chosen by the owner. THIS IS THE KEY to the warm, premium feeling. Use it deliberately and sparingly for featured/premium/trust moments (featured provider accents, the "verified/موثّق" detail, key highlights, soft gold gradients or underlines/hairlines). For very subtle fills or tints, use a lighter wash of it (e.g. #FBD060 at low opacity, or a tint around #FCE4A6). A little of this gold reads warm and premium; blanketing large areas in it reads gaudy — keep it as an accent, not a background flood.

- **Warm neutrals**: use warm off-whites and warm grays (a hint of warmth in the neutrals) rather than cold pure-gray, to support the overall warm feeling.

How to use them together:
- Blue is the workhorse (primary/interactive). Green is the supporting accent. Gold is the premium/warmth signal used sparingly on the moments that matter most (featured, verified, CTAs worth elevating).
- Depth comes from soft gradients and layered shadows built on these hues — e.g. subtle blue→deeper-blue or warm gold-tinted gradients in the hero, not flat fills.
- Keep the single-accent discipline for INTERACTIVE state (blue) so users always know what's clickable; gold and green are for status/emphasis, not primary actions.

## Hard constraint: NO imagery changes
Do NOT add photos, illustrations, or stock imagery, and do NOT change existing images. Achieve the warm, premium feeling purely through STYLING:
- A warmer, richer color system — more than one flat accent. Build depth from the existing brand blue/green but add a deliberate secondary and warm neutrals.
- Subtle gradients, soft layered shadows, and gentle background shapes/texture (CSS only) to replace flat surfaces with depth.
- Confident typography as the primary design element — larger, more expressive headings, a proper type scale, strong hierarchy. Respect Arabic/RTL: pick and actually load a real Arabic display font; never apply uppercase or letter-tracking to Arabic.
- Refined, consistent iconography instead of emoji (see below).
- Generous, deliberate spacing and rhythm so the page breathes.

## Specific changes (keep structure and content, change only styling)

1. **Remove all emoji used as UI/category icons** (🍽️🏠🏥 etc.) and replace with a single consistent icon set (lucide, already in the codebase) styled to match the brand. Emoji is the biggest "not premium / templated" signal and none of the reference sites use it. Highest-impact change, and it's styling-only.

2. **Restyle the hero** for real visual impact without imagery: a warm gradient or subtly textured background (CSS), a confident large Arabic headline with strong type hierarchy, and a prominent, well-designed search as the centerpiece. Make it feel like an inviting front door, not a plain text block.

3. **Category section** — turn the flat emoji list into designed category tiles: color-blocked or gradient tiles with a consistent styled icon and clear label, spacious and tappable (44px+). CSS/color only, no images.

4. **Provider cards** — give them a warmer, more premium treatment: softer layered shadow, better internal spacing, cleaner hierarchy, reduced badge/text clutter. Keep the existing provider logos as-is; just improve the card styling around them.

5. **Depth and warmth pass** — replace flat monotone surfaces with layered depth: subtly alternating section backgrounds, soft shadows, and generous vertical spacing so the page breathes.

6. **Fix the empty "0+" stats** — show real numbers or remove the stat block until there's data. Empty stats undercut trust.

## Guardrails
- Keep existing structure, sections, content, and images. This is a restyle, not a rebuild, and adds no new imagery.
- Arabic/RTL is first-class: verify the Arabic font actually loads; keep everything RTL-correct; respect Arabic typography (no uppercase, no tracking).
- Define the new visual system in DESIGN.md and apply it consistently; no one-off styles.
- Keep it fast and accessible: real contrast (WCAG AA), 44px touch targets, semantic markup, visible focus states.

## Suggested impeccable sequence
1. Update DESIGN.md to capture this warmer, richer direction (color system, gradients, type scale, elevation, category-tile and card patterns) — styling only.
2. `craft` / `bolder` the hero and category section against this brief — biggest visual gain.
3. `polish` the provider cards and section rhythm.
4. `critique` at the end to check the refresh holds up and stays RTL-correct.
Review each change before accepting, and verify in the browser (RTL + mobile + console) — a clean type-check is not proof it renders well.
