# Residuum — Aesthetic Guide

The identity and messaging docs cover what Residuum feels like. This doc covers what that looks like in practice — the actual values, patterns, and rules that make new work feel consistent with what exists.

Source of truth for variables: `relay/web/src/styles/variables.css`

---

## Palette

Dark geological. Stone surfaces with two accent veins — blue energy and organic green growth.

### Stone (backgrounds & text)

| Token | Hex | Usage |
|---|---|---|
| `--bg-deep` | `#0e0e10` | Page background. Near-black obsidian. |
| `--bg-surface` | `#161618` | Cards, raised containers |
| `--bg-raised` | `#1c1c1f` | Elevated surfaces, nav |
| `--bg-input` | `#141416` | Form inputs |
| `--border` | `#2a2a2e` | Default borders |
| `--border-subtle` | `#222225` | Faint borders, dividers |
| `--text` | `#e8e8ea` | Primary text |
| `--text-muted` | `#9a9a9f` | Secondary text, descriptions |
| `--text-dim` | `#6a6a6f` | Tertiary text, hints |

Landing page aliases map to the same values with `stone-` prefix naming (`--stone-deepest` through `--stone-white`).

### Blue Vein (energy, accents, focus)

The blue is the energy running through the construct's seams. It signals life — something is still active inside.

| Token | Value | Usage |
|---|---|---|
| `--vein-blue` | `#3b8bdb` | Primary accent. Dividers, active states, focus rings. |
| `--vein-glow` | `#5aa3f0` | Brighter variant for hover/emphasis |
| `--vein-dim` | `#2a6cb5` | Darker variant for pressed/subtle states |
| `--vein-faint` | `rgba(59,139,219, 0.08)` | Background tints, radial halos |
| `--vein-subtle` | `rgba(59,139,219, 0.15)` | Gradient endpoints, soft glows |

App-side aliases: `--ember`, `--ember-bright`, `--ember-glow`, `--ember-dim`.

### Moss Green (growth, links, organic accents)

The green is what grows on the construct — lichen, vines, life finding footholds in stone.

| Token | Value | Usage |
|---|---|---|
| `--moss` | `#6b7a4a` | Links, organic accents |
| `--moss-dust` | `#5a693a` | Darker variant for emphasis text |
| `--moss-faint` | `rgba(107,122,74, 0.25)` | Hover borders, subtle highlights |

Link hover color: `#8a9e62` (lighter moss).

### Status Colors

| Token | Value | Usage |
|---|---|---|
| `--error` | `#c0392b` | Validation errors |
| `--error-bg` | `rgba(192,57,43, 0.1)` | Error background tint |
| `--success` | `#2ecc71` | Success states |

---

## Typography

Three typefaces. Classical weight meets technical precision.

### Font Stack

| Token | Family | Fallback | Role |
|---|---|---|---|
| `--font-display` | Cinzel | Georgia, serif | Headings, titles, nav brand |
| `--font-body` | Literata | Georgia, serif | Body text, descriptions |
| `--font-mono` | JetBrains Mono | Fira Code, SF Mono, Consolas, monospace | Code, labels, section markers |

Loaded via Google Fonts with `display=swap`. Preconnect in `index.html`.

### Weights

| Typeface | Weights loaded | Primary usage |
|---|---|---|
| Cinzel | 400, 500, 600, 700 | 400 for titles, 500 for headings/nav |
| Literata | 300, 400, 500 (+ italic) | 300 for body (default), 400/500 sparingly |
| JetBrains Mono | 300, 400, 500 | 300 for install/code, 400 for labels |

### Base Text

```
font-family: var(--font-body)
font-size: 17px
font-weight: 300
line-height: 1.7
-webkit-font-smoothing: antialiased
```

The default weight is 300 — light, quiet, bookish. Heavier weights are used to draw attention, not as defaults.

---

---

## Motion

Everything moves slowly. The UI has the pace of the construct — unhurried, geological.

### Easing

```
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1)
```

General transitions use `ease-out`. The expo curve is reserved for cards and higher-impact reveals.

### Scroll Reveals

Elements enter the viewport via the `use:reveal` Svelte action:
- **Trigger**: IntersectionObserver at 15% visibility, `-40px` bottom margin
- **Stagger**: 120ms between siblings (passed as `delay` option)
- **One-shot**: Observer disconnects after first intersection

CSS for revealed elements follows this pattern:

```css
.element {
  opacity: 0;
  transform: translateY(12px);
  transition: all 0.8s ease-out;
}
.element.visible {
  opacity: 1;
  transform: translateY(0);
}
```

Durations by element type:
- Section labels, feature blocks: `0.8s`
- Large text blocks: `0.9s`
- Grid items, principles: `0.7s`
- Vein dividers: `1s`

### Hero Sequence

The hero doesn't use scroll reveal — it plays on load with explicit cascading delays:

| Element | Animation | Duration | Delay |
|---|---|---|---|
| Logo | `emerge` | 1.8s | 0.3s |
| Title | `emerge` | 1.6s | 0.8s |
| Tagline | `emerge` | 1.6s | 1.3s |
| Vein | `veinGrow` | 1.2s | 1.8s |
| Scroll hint | `emerge` | 1.0s | 2.5s |

Total sequence: ~3.5s. The page unfolds like something being uncovered.

---

### Keyframes

```css
@keyframes emerge {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes veinGrow {
  from { opacity: 0; transform: scaleX(0); }
  to   { opacity: 1; transform: scaleX(1); }
}

@keyframes pulse {
  0%, 100% { opacity: 0.3; }
  50%      { opacity: 0.8; }
}
```

### Interactive Transitions

Links, buttons, and hover states: `0.3s ease`. Quick enough to feel responsive, slow enough to not snap.

---

---

## Texture

### Grain Overlay

A fixed SVG noise texture covers the entire viewport. It gives every surface a stone-grain feel — subtle enough to be felt, not seen.

### Vein Dividers

```css
body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.025;
  background: url("data:image/svg+xml,..."); /* feTurbulence fractalNoise */
  background-size: 256px 256px;
}
```

Parameters: `baseFrequency: 0.85`, `numOctaves: 4`, `stitchTiles: stitch`.

Horizontal rules styled as luminescent cracks in stone:

```css
background: linear-gradient(90deg,
  transparent 0%,
  var(--vein-subtle) 20%,
  var(--vein-blue) 50%,
  var(--vein-subtle) 80%,
  transparent 100%
);
box-shadow: 0 0 8px rgba(59, 139, 219, 0.15);
```

### Radial Halos

```css
radial-gradient(circle, var(--vein-faint) 0%, transparent 70%)
```

### Card Effects

```
--card-shadow: 0 1px 4px rgba(0,0,0, 0.25), 0 0 1px rgba(0,0,0, 0.15)
--card-shadow-hover: 0 2px 8px rgba(0,0,0, 0.35), 0 0 1px rgba(0,0,0, 0.2)
```

---

## Interaction States

The construct is stone with energy running through it. Interaction states follow that metaphor — the stone reacts physically, the energy reacts luminously.

---

### Buttons

Primary actions use `--vein-blue` as background with `--stone-white` text. They should be visually distinct from the surrounding stone — these are the seams where the energy surfaces. Secondary actions use `--bg-raised` with a `--border` outline and `--text` color.

The energy is what distinguishes action from content. If a button blends into the page, it's missing the vein.

### Hover

The energy intensifies. Vein glow brightens (`--vein-glow`), box-shadow spreads slightly. The stone itself doesn't move — the light does. For primary buttons, the background shifts to `--vein-glow`. For secondary, a faint `--vein-faint` background appears.

Transition: `0.3s ease`.

### Active / Pressed

The stone depresses. Subtle `inset` shadow, slight `scale(0.98)`. Physical, tactile — you pressed on rock and it yielded slightly. The glow doesn't change, the surface does.

### Disabled

Faded moss. The element takes on `--moss-dust` tones at reduced opacity (~0.4). It's not broken or greyed out — the forest grew over it. The vein energy is absent. `cursor: not-allowed`.

### Focus (keyboard navigation)

Accessibility first. A clearly visible high-contrast outline — `2px solid` with enough offset to be unambiguous. This is not the place for subtlety. Meet WCAG requirements, even if it's slightly at odds with the ambient aesthetic. The focus ring can use `--vein-blue` as its color, but contrast and visibility take priority over brand consistency.

### Error States

### Error States

Subdued red, tightly contained. Use `--error` for a thin border or small accent mark — not a full background wash. Error text can use `--error` at full opacity, but the surrounding treatment stays restrained. A faint `--error-bg` tint is the maximum background treatment. The error is noted, not screamed.

### Loading

Minimal and utilitarian. A small pulsing indicator in `--vein-blue` — dot, spinner, or subtle bar. Use the `pulse` keyframe or equivalent. Don't over-theme it. Loading is a moment to get out of the way, not an opportunity for brand expression. The construct doesn't rush, but it also doesn't make you watch it think.

### Empty States

Quiet potential. A clean, sparse surface with a single line of `--text-muted` text. No illustrations, no mascot, no calls to action. The space is available — an empty workshop with good lighting, ready for work. Not sad, not inviting, just present.

---

## Elevation & Texture

### Surface Hierarchy

Higher surfaces are lighter, smoother stone. The base rock is rough; raised surfaces are more refined, like worked stone.

| Level | Token | Feel |
|---|---|---|
| Base | `--bg-deep` | Raw bedrock, darkest |
| Surface | `--bg-surface` | Hewn stone, cards and panels |
| Raised | `--bg-raised` | Polished stone, nav, modals, dropdowns |

Shadow depth increases with elevation:

```
Level 0 (base): no shadow
Level 1 (surface): --card-shadow
Level 2 (raised): --card-shadow-hover or deeper
```

The SVG noise texture is global and uniform across all elevation levels. The grain doesn't change with depth — it's the material itself, not a surface treatment. Vein dividers and radial halos are defined in the Texture section above.

---

---

## Spacing & Shape

| Token | Value |
|---|---|
| `--radius` | `6px` |
| `--radius-sm` | `4px` |

Corners are barely rounded — stone doesn't have sharp edges, but it doesn't have soft ones either.

### Spatial Rhythm

Generous on desktop, tighter on mobile. The brand says "let them breathe" — that's not a suggestion, it's a rule.

**Between sections**: 80–120px on desktop. These are geological strata — they don't crowd each other.

**Within sections**: 24–40px between related elements. Enough room to parse each piece without scanning effort.

**On mobile**: Spacing scales down meaningfully, not proportionally. Sections get closer together (40–60px) rather than everything shrinking by the same ratio. The content density increases but the reading rhythm should still feel unhurried.

---

---

## Responsive

### Breakpoints

| Breakpoint | Target |
|---|---|
| `768px` | Tablet — nav links hidden, grid collapses, section spacing reduces |
| `480px` | Mobile — further scaling, hero logo shrinks (220px → 160px → 130px) |

### Motion on Mobile

Case by case. The current landing page motion works on mobile. Busier sections (app UI, dense grids) may need reduction — shorter durations, less stagger, or dropping choreography entirely in favor of simple fades. Judge by feel, not by rule. If the animation is competing with the content for attention on a small screen, simplify it.

### Touch Targets

### Touch Targets

Interactive elements need minimum 44px touch targets on mobile, regardless of visual size. Padding or invisible hit areas can make up the difference. Hover-dependent interactions (glow intensification, tooltip reveals) need a tap-equivalent — don't rely on hover for information or affordance on touch devices.

### Light Mode

Dark only for now. This isn't a brand statement — it's a current constraint. The geological palette is built for dark surfaces. A light variant may come later, but it would need its own material language, not just inverted values.

---

## Rules

1. **No bright colors outside the vein blue and moss green.** The palette is deliberately constrained. New accents don't belong.
2. **No animations faster than 0.3s** except micro-interactions (focus rings, active states).
3. **No animation on load** except the hero sequence. Everything else waits for scroll.
4. **Glow effects stay subtle.** Box-shadow opacity for vein glows should stay at or below `0.3`. The light is coming from inside, not shining on top.
5. **The grain overlay stays.** It's global, fixed, and permanent. Don't disable it per-page or per-component.
6. **Literata at 300 is the default.** If text feels heavy, the weight is probably wrong.
7. **Primary actions carry the vein.** Buttons and CTAs use vein-blue to stand apart from stone. If an action blends into the page, it needs more energy.
8. **Accessibility overrides aesthetics.** Focus states, contrast ratios, and touch targets meet standards first. Brand consistency is secondary to usability.

