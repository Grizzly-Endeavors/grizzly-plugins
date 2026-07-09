---
name: bevy-ui
description: >
  Comprehensive guide for building UI in Bevy 0.18. Use when creating, styling, or debugging
  any Bevy UI: menus, HUDs, buttons, sliders, scrollable lists, popover menus, tooltips,
  text styling, gamepad/keyboard navigation, or layout with flexbox/CSS grid. Also use for
  questions about Bevy's headless widget system (Button, Slider, Checkbox, RadioButton,
  Scrollbar, Popover, MenuPopup), the Feathers theming library, the Interaction/focus system,
  accessibility, font features, or any bevy_ui component (Node, Val, BackgroundColor,
  BorderColor, ImageNode, Text, BoxShadow, Gradient, etc). Triggers on keywords: bevy ui,
  bevy_ui, bevy menu, bevy hud, bevy button, bevy widget, bevy layout, bevy flexbox,
  bevy feathers, bevy navigation, bevy scroll, bevy popover.
---

# Bevy 0.18 UI

Bevy's UI is ECS-native. UI elements are entities with components. Layout is powered by `taffy`
(Flexbox + CSS Grid). Rendering is handled by `bevy_ui_render`.

**Key docs:**
- API: <https://docs.rs/bevy/0.18.0/bevy/ui/index.html>
- Widgets: <https://docs.rs/bevy/0.18.0/bevy/ui_widgets/index.html>
- Feathers: <https://docs.rs/bevy/0.18.0/bevy/feathers/index.html>
- Examples: <https://github.com/bevyengine/bevy/tree/release-0.18.0/examples/ui>

## Reference Files

- **Layout, styling, and core components**: See [references/core.md](references/core.md)
- **Widgets, interaction, navigation, and Feathers**: See [references/widgets.md](references/widgets.md)
- **Design patterns and best practices**: See [references/patterns.md](references/patterns.md)

Read the relevant reference file before generating code. For a basic layout question read
`core.md`. For widget/interaction work read `widgets.md`. For architecture advice read
`patterns.md`.

## Critical 0.18 Changes (from 0.17)

Always apply these when writing Bevy 0.18 UI code:

1. **`BorderRadius` is a field on `Node`, not a separate component.**
   ```rust
   Node { border_radius: BorderRadius::all(Val::Px(8.0)), ..default() }
   ```

2. **`LineHeight` is a separate component**, no longer on `TextFont`.
   ```rust
   commands.spawn((Text::new("Hi"), TextFont { font_size: 24.0, ..default() }, LineHeight(1.5)));
   ```

3. **`BorderRect` uses `Vec2` fields** (not `Val` per-side).

4. **New `ui` cargo feature collection** — Bevy as a pure UI framework:
   ```toml
   bevy = { version = "0.18", default-features = false, features = ["ui"] }
   ```

5. **`RenderTarget` is a component**, not a field on `Camera`.

6. **New widgets**: `Popover`, `MenuPopup`, `ColorPlane`.

7. **`AutoDirectionalNavigation`** — automatic gamepad/keyboard nav.

8. **`IgnoreScroll`** — sticky headers in scroll containers.

9. **Font Variations**: `FontWeight`, `Strikethrough`, `Underline`, `FontFeatures`.

10. **`TryStableInterpolate`** for animating `Val` and `Color`.

## Important 0.17 Changes (still apply in 0.18)

- **`Transform`/`GlobalTransform` replaced by `UiTransform`/`UiGlobalTransform`** for UI nodes.
  UI entities no longer use 3D transforms. See `core.md` § UI Transforms for details and migration.
