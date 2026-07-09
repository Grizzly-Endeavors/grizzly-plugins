# Widgets, Interaction, Navigation, and Feathers

## Table of Contents
1. [Interaction System](#interaction-system)
2. [Headless Widgets (bevy_ui_widgets)](#headless-widgets)
3. [Button Widget](#button-widget)
4. [Slider Widget](#slider-widget)
5. [Checkbox Widget](#checkbox-widget)
6. [RadioButton and RadioGroup](#radiobutton-and-radiogroup)
7. [Scrollbar Widget](#scrollbar-widget)
8. [Popover (0.18)](#popover)
9. [MenuPopup (0.18)](#menupopup)
10. [Focus System](#focus-system)
11. [Directional Navigation](#directional-navigation)
12. [Feathers — Themed Widget Library](#feathers)
13. [Accessibility](#accessibility)

---

## Interaction System

The `Interaction` component tracks pointer state on UI entities. It is set automatically by
`ui_focus_system` for nodes that have both `Node` and `Interaction` inserted.

```rust
#[derive(Component)]
pub enum Interaction {
    Pressed,   // pointer button is down on this node
    Hovered,   // pointer is over this node
    None,      // no interaction
}
```

The `Button` marker component (not the headless widget) requires `Interaction`:
```rust
commands.spawn((
    Button,                              // marker, auto-inserts Interaction + Node
    Node { width: px(150.0), height: px(50.0), ..default() },
    BackgroundColor(Color::srgb(0.15, 0.15, 0.15)),
));
```

### Querying Interaction Changes
```rust
fn button_system(
    mut query: Query<
        (&Interaction, &mut BackgroundColor),
        (Changed<Interaction>, With<Button>),
    >,
) {
    for (interaction, mut bg) in &mut query {
        match *interaction {
            Interaction::Pressed => { *bg = Color::srgb(0.35, 0.75, 0.35).into(); }
            Interaction::Hovered => { *bg = Color::srgb(0.25, 0.25, 0.25).into(); }
            Interaction::None    => { *bg = Color::srgb(0.15, 0.15, 0.15).into(); }
        }
    }
}
```

### RelativeCursorPosition
Tracks pointer position relative to a node, (0,0) = center, (0.5, 0.5) = bottom-right:
```rust
commands.spawn((Node { ..default() }, RelativeCursorPosition::default()));
// Later:
fn track_cursor(q: Query<&RelativeCursorPosition>) {
    for pos in &q {
        if let Some(p) = pos.normalized {
            // p is within (-0.5..0.5) range when cursor is over the node
        }
    }
}
```

### FocusPolicy
Controls whether a node blocks interactions from reaching nodes below it:
```rust
FocusPolicy::Block  // default for nodes with Interaction — blocks pass-through
FocusPolicy::Pass   // lets interactions fall through to nodes behind
```

### InteractionDisabled
Grays out / disables a widget. Does not prevent rendering or focus, but prevents interaction:
```rust
commands.spawn((Button, InteractionDisabled));
```

### Pressed Component
Tracks pressed state for widgets. Lower-level than `Interaction`:
```rust
// Added/removed automatically by headless widget systems
```

## Headless Widgets

Bevy 0.17 introduced headless widgets in `bevy_ui_widgets`. These are **unstyled** behavioral
components. You add styling yourself. Available in 0.18 with improvements.

**Enable**: Headless widgets are included in DefaultPlugins. If using minimal features,
ensure `bevy_ui_widgets` feature is enabled.

**Philosophy**: Each widget is a component you add to a `Node` entity. The widget systems
handle input, state management, and emit events. You handle visuals via queries on
`Changed<Checked>`, `Changed<Interaction>`, etc.

## Button Widget

`bevy_ui_widgets::Button` — emits `Activate` entity event when clicked/pressed.

```rust
use bevy::ui_widgets::Button as WidgetButton;

commands.spawn((
    WidgetButton,
    Node { width: px(120.0), height: px(40.0), ..default() },
    BackgroundColor(Color::srgb(0.3, 0.3, 0.3)),
)).observe(|_trigger: Trigger<Activate>| {
    info!("Button activated!");
});
```

Note: The basic `bevy::prelude::Button` marker (from older Bevy) gives `Interaction`
tracking. The `bevy_ui_widgets::Button` provides richer event-based activation.

## Slider Widget

`Slider` — edits an `f32` value within a range.

```rust
use bevy::ui_widgets::{Slider, ValueChange};

commands.spawn((
    Slider::new(0.0, 100.0, 50.0), // min, max, initial
    Node { width: px(200.0), height: px(20.0), ..default() },
)).observe(|trigger: Trigger<ValueChange<f32>>| {
    info!("Slider value: {}", trigger.value);
});
```

The slider does NOT render a track/thumb by default — add child nodes for visual
representation, and query the `Slider` component to position the thumb.

## Checkbox Widget

`Checkbox` — toggleable state with `Checked` component.

```rust
use bevy::ui_widgets::{Checkbox, Checkable, Checked, ValueChange};

commands.spawn((
    Checkbox,
    Checkable,
    Node { width: px(24.0), height: px(24.0), ..default() },
)).observe(|trigger: Trigger<ValueChange<bool>>| {
    info!("Checked: {}", trigger.value);
});

// Query checked state:
fn check_state(q: Query<&Checked, With<Checkbox>>) {
    for checked in &q {
        // Checked is a unit struct — its presence means "checked"
    }
}
```

## RadioButton and RadioGroup

`RadioButton` — select one item from a set.

```rust
use bevy::ui_widgets::{RadioButton, RadioGroup, Checkable, ValueChange};

let group = commands.spawn(RadioGroup::default()).id();

for i in 0..3 {
    commands.spawn((
        RadioButton,
        Checkable,
        Node { width: px(24.0), height: px(24.0), ..default() },
    )).set_parent(group);
}
```

0.18 improvements:
- `RadioButton` now emits `ValueChange<bool>` when checked (even via `RadioGroup`).
- `RadioGroup` is now optional — can replace with custom implementation.
- Space/Enter keys trigger value change when focused.

## Scrollbar Widget

`Scrollbar` — linked to a scrollable container.

```rust
use bevy::ui_widgets::Scrollbar;

// Create scrollbar linked to a scroll container
commands.spawn((
    Scrollbar::new(scroll_container_entity),
    Node { width: px(12.0), ..default() },
));
```

## Popover (0.18)

`Popover` — automatic popup positioning relative to an anchor element. Inspired by
`floating-ui`. Flips sides to stay within the window. Usable for dropdowns and tooltips.

```rust
use bevy::ui_widgets::popover::Popover;

commands.spawn((
    Node {
        position_type: PositionType::Absolute,
        ..default()
    },
    Popover {
        anchor: anchor_entity,
        // placement preferences — tries each in order
        placements: vec![
            PopoverPlacement::Bottom,
            PopoverPlacement::Top,
        ],
        ..default()
    },
));
```

Dynamic repositioning: if anchor moves, window resizes, or container scrolls, the popover
auto-adjusts.

## MenuPopup (0.18)

`MenuPopup` — dropdown menu built on `Popover`. Adds open/close events, keyboard navigation,
and activation via the focus system.

```rust
use bevy::ui_widgets::MenuPopup;

commands.spawn((
    MenuPopup::new(trigger_button_entity),
    Node { ..default() },
)).with_children(|parent| {
    parent.spawn((
        Text::new("Option 1"),
        Node { padding: UiRect::all(Val::Px(8.0)), ..default() },
    ));
    parent.spawn((
        Text::new("Option 2"),
        Node { padding: UiRect::all(Val::Px(8.0)), ..default() },
    ));
});
```

## Focus System

Bevy 0.17+ introduced `bevy_input_focus` for keyboard/gamepad focus management.

```rust
use bevy::input_focus::InputFocus;

// Must be initialized for accessibility and keyboard nav:
app.init_resource::<InputFocus>();

// Set focus programmatically:
fn set_focus(mut focus: ResMut<InputFocus>) {
    focus.0 = Some(target_entity);
}
```

Focusable entities: any entity with `Node` + `Interaction` is focusable. Tab navigation
is built-in.

## Directional Navigation

### Manual Navigation (0.17+)
```rust
use bevy::input_focus::directional_navigation::DirectionalNavigationMap;

fn setup_nav(mut nav_map: ResMut<DirectionalNavigationMap>) {
    nav_map.add_symmetrical_edge(button_a, button_b, CompassOctant::East);
}
```

### Automatic Navigation (0.18)
Add `AutoDirectionalNavigation` to focusable entities — connections computed spatially:

```rust
use bevy::ui::auto_directional_navigation::AutoDirectionalNavigation;

commands.spawn((
    Button,
    Node { ..default() },
    AutoDirectionalNavigation::default(),
));
```

Use `AutoDirectionalNavigator` system parameter to navigate:
```rust
fn my_nav(mut nav: AutoDirectionalNavigator) {
    nav.navigate(CompassOctant::East); // move focus east
}
```

### Configuration
```rust
app.insert_resource(AutoNavigationConfig {
    min_alignment_factor: 0.0,       // 0.0=any overlap, 1.0=perfect alignment
    max_search_distance: Some(500.0),
    prefer_aligned: true,
});
```

Manual edges (`DirectionalNavigationMap::add_edge`) take precedence over auto-generated.

## Feathers

Feathers is an **experimental** themed widget library for tooling. Behind
`experimental_bevy_feathers` feature flag.

```toml
[dependencies]
bevy = { version = "0.18", features = ["experimental_bevy_feathers"] }
```

Feathers provides:
- Pre-styled buttons, sliders, checkboxes, menu buttons, etc.
- Layout containers.
- Basic theming system (not final).
- Accessibility / screen reader support.
- Cursor behavior on hover.
- Virtual keyboard for touchscreen.
- **ColorPlane widget** (0.18): 2D color picker with configurable color spaces.

```rust
use bevy::feathers::controls::ColorPlane;
// ColorPlane displays hue vs lightness, hue vs saturation, etc.
```

**Status**: Feathers is early / experimental. API will change. Targeted for BSN port in
future release. Good for editor tooling, less suited for game UI (use headless widgets +
custom styling instead).

## Accessibility

Bevy UI integrates with `accesskit` for screen reader support.

```rust
use accesskit::{Role, Accessible};
commands.spawn((
    Text::new("Settings"),
    AccessibilityNode(Accessible::new(Role::Heading)),
));
```

For interactive elements use `Role::Button`, `Role::Slider`, `Role::Checkbox`, etc.
The `Label` component marks text as descriptive (accessibility label).

`InputFocus` must be initialized for accessibility to work:
```rust
app.init_resource::<InputFocus>();
```
