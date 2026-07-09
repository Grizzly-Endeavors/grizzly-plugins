# Bevy UI Design Patterns and Best Practices

## Table of Contents
1. [Spawning Patterns](#spawning-patterns)
2. [Responsive Layout](#responsive-layout)
3. [Common Layout Recipes](#common-layout-recipes)
4. [Styling Architecture](#styling-architecture)
5. [Dynamic UI Updates](#dynamic-ui-updates)
6. [State-Driven UI](#state-driven-ui)
7. [Animation and Transitions](#animation-and-transitions)
8. [Performance Tips](#performance-tips)
9. [Debugging Layout](#debugging-layout)
10. [Common Pitfalls](#common-pitfalls)

---

## Spawning Patterns

### children! Macro (preferred for static hierarchies)
```rust
use bevy::prelude::*;

commands.spawn((
    Node {
        width: Val::Percent(100.0),
        height: Val::Percent(100.0),
        flex_direction: FlexDirection::Column,
        ..default()
    },
    children![
        (
            Node { height: px(60.0), ..default() },
            BackgroundColor(Color::srgb(0.1, 0.1, 0.15)),
            children![
                (Text::new("Header"), TextFont { font_size: 28.0, ..default() }),
            ],
        ),
        (
            Node { flex_grow: 1.0, ..default() },
            children![
                (Text::new("Body content"), TextFont { font_size: 18.0, ..default() }),
            ],
        ),
    ],
));
```

### with_children (for more complex logic)
```rust
commands.spawn(Node { ..default() }).with_children(|parent| {
    for i in 0..10 {
        parent.spawn((
            Text(format!("Item {i}")),
            TextFont { font_size: 16.0, ..default() },
        ));
    }
});
```

### Children::spawn with SpawnIter (dynamic lists)
```rust
commands.spawn((
    Node { flex_direction: FlexDirection::Column, ..default() },
    Children::spawn(SpawnIter(items.iter().map(|item| {
        (
            Text::new(item.name.clone()),
            TextFont { font_size: 16.0, ..default() },
        )
    }))),
));
```

### Returning impl Bundle (reusable UI functions)
```rust
fn styled_button(label: &str) -> impl Bundle {
    (
        Button,
        Node {
            width: px(150.0),
            height: px(45.0),
            justify_content: JustifyContent::Center,
            align_items: AlignItems::Center,
            border: UiRect::all(Val::Px(2.0)),
            border_radius: BorderRadius::all(Val::Px(6.0)),
            ..default()
        },
        BackgroundColor(Color::srgb(0.2, 0.2, 0.2)),
        BorderColor(Color::srgb(0.4, 0.4, 0.4)),
        children![(
            Text::new(label.to_string()),
            TextFont { font_size: 18.0, ..default() },
            TextColor(Color::WHITE),
        )],
    )
}

// Usage:
commands.spawn(styled_button("Play"));
commands.spawn(styled_button("Settings"));
```

## Responsive Layout

### Viewport Units for Responsive Sizing
```rust
Node {
    width: Val::Vw(80.0),    // 80% of viewport width
    max_width: Val::Px(800.0), // cap at 800px
    min_width: Val::Px(300.0), // floor at 300px
    padding: UiRect::axes(Val::Vw(2.0), Val::Vh(2.0)),
    ..default()
}
```

### Flex-Based Responsive Columns
```rust
// Two columns that stack on narrow viewports (use flex_wrap)
Node {
    flex_direction: FlexDirection::Row,
    flex_wrap: FlexWrap::Wrap,
    ..default()
},
// Each child:
Node {
    flex_basis: Val::Px(300.0),  // min width before wrapping
    flex_grow: 1.0,
    ..default()
}
```

### UiScale for Global Scaling
```rust
// Scale all UI by 1.5x
commands.insert_resource(UiScale(1.5));
```

## Common Layout Recipes

### Centered Card
```rust
fn card(title: &str, body: &str) -> impl Bundle {
    (
        Node {
            width: px(400.0),
            padding: UiRect::all(Val::Px(24.0)),
            flex_direction: FlexDirection::Column,
            row_gap: Val::Px(12.0),
            border: UiRect::all(Val::Px(1.0)),
            border_radius: BorderRadius::all(Val::Px(12.0)),
            ..default()
        },
        BackgroundColor(Color::srgb(0.12, 0.12, 0.14)),
        BorderColor(Color::srgba(1.0, 1.0, 1.0, 0.1)),
        BoxShadow(vec![ShadowStyle {
            color: Color::srgba(0.0, 0.0, 0.0, 0.4),
            x_offset: Val::Px(0.0),
            y_offset: Val::Px(4.0),
            blur_radius: Val::Px(16.0),
            spread_radius: Val::Px(0.0),
            ..default()
        }]),
        children![
            (Text::new(title), TextFont { font_size: 24.0, ..default() }, TextColor(Color::WHITE)),
            (Text::new(body), TextFont { font_size: 16.0, ..default() }, TextColor(Color::srgba(1.0, 1.0, 1.0, 0.7))),
        ],
    )
}
```

### Sidebar + Content Layout
```rust
(
    Node {
        width: Val::Percent(100.0),
        height: Val::Percent(100.0),
        flex_direction: FlexDirection::Row,
        ..default()
    },
    children![
        // Sidebar
        (
            Node {
                width: px(250.0),
                height: Val::Percent(100.0),
                flex_direction: FlexDirection::Column,
                padding: UiRect::all(Val::Px(16.0)),
                ..default()
            },
            BackgroundColor(Color::srgb(0.08, 0.08, 0.1)),
        ),
        // Main content
        (
            Node {
                flex_grow: 1.0,
                height: Val::Percent(100.0),
                padding: UiRect::all(Val::Px(24.0)),
                ..default()
            },
        ),
    ],
)
```

### Absolute Overlay / Modal
```rust
(
    Node {
        position_type: PositionType::Absolute,
        left: Val::Px(0.0),
        top: Val::Px(0.0),
        width: Val::Percent(100.0),
        height: Val::Percent(100.0),
        justify_content: JustifyContent::Center,
        align_items: AlignItems::Center,
        ..default()
    },
    GlobalZIndex(100),
    BackgroundColor(Color::srgba(0.0, 0.0, 0.0, 0.6)),
    // Modal card as child...
)
```

### Horizontal Toolbar
```rust
(
    Node {
        width: Val::Percent(100.0),
        height: px(48.0),
        flex_direction: FlexDirection::Row,
        align_items: AlignItems::Center,
        padding: UiRect::axes(Val::Px(16.0), Val::Px(0.0)),
        column_gap: Val::Px(8.0),
        ..default()
    },
    BackgroundColor(Color::srgb(0.1, 0.1, 0.12)),
)
```

### Scrollable List with Sticky Header
```rust
// Outer container
(
    Node {
        flex_direction: FlexDirection::Column,
        height: Val::Px(400.0),
        overflow: Overflow::scroll_y(),
        ..default()
    },
    children![
        // Sticky header
        (
            Node { height: px(40.0), ..default() },
            BackgroundColor(Color::srgb(0.2, 0.2, 0.2)),
            IgnoreScroll { x: false, y: true }, // 0.18: stays in place
        ),
        // Scrollable items...
    ],
)
```

## Styling Architecture

### Marker Components for Themed Queries
```rust
#[derive(Component)]
struct PrimaryButton;

#[derive(Component)]
struct DangerButton;

// System that applies consistent styling
fn style_primary_buttons(
    mut q: Query<&mut BackgroundColor, (With<PrimaryButton>, Changed<Interaction>)>,
) { /* ... */ }
```

### Theme Resource
```rust
#[derive(Resource)]
struct UiTheme {
    primary: Color,
    secondary: Color,
    background: Color,
    surface: Color,
    text: Color,
    text_muted: Color,
    border: Color,
    font_sm: f32,
    font_md: f32,
    font_lg: f32,
    radius_sm: Val,
    radius_md: Val,
    spacing: Val,
}

impl Default for UiTheme {
    fn default() -> Self {
        Self {
            primary: Color::srgb(0.3, 0.5, 1.0),
            secondary: Color::srgb(0.5, 0.5, 0.5),
            background: Color::srgb(0.05, 0.05, 0.07),
            surface: Color::srgb(0.1, 0.1, 0.12),
            text: Color::WHITE,
            text_muted: Color::srgba(1.0, 1.0, 1.0, 0.6),
            border: Color::srgba(1.0, 1.0, 1.0, 0.1),
            font_sm: 14.0,
            font_md: 18.0,
            font_lg: 28.0,
            radius_sm: Val::Px(4.0),
            radius_md: Val::Px(8.0),
            spacing: Val::Px(8.0),
        }
    }
}

app.init_resource::<UiTheme>();
```

## Dynamic UI Updates

### Modifying Node Properties
```rust
fn grow_on_hover(mut q: Query<(&Interaction, &mut Node), Changed<Interaction>>) {
    for (interaction, mut node) in &mut q {
        node.width = match interaction {
            Interaction::Hovered => px(220.0),
            _ => px(200.0),
        };
    }
}
```

### Toggling Visibility
```rust
fn toggle_panel(
    mut q: Query<&mut Visibility, With<SettingsPanel>>,
    input: Res<ButtonInput<KeyCode>>,
) {
    if input.just_pressed(KeyCode::Escape) {
        for mut vis in &mut q {
            *vis = match *vis {
                Visibility::Hidden => Visibility::Inherited,
                _ => Visibility::Hidden,
            };
        }
    }
}
```

### Display::None vs Visibility::Hidden
- `Display::None` — removed from layout entirely (takes no space).
- `Visibility::Hidden` — invisible but still takes up layout space.

```rust
// Remove from layout:
node.display = Display::None;
// Bring back:
node.display = Display::Flex;
```

## State-Driven UI

### Using Bevy States for Screen Management
```rust
#[derive(States, Default, Debug, Clone, PartialEq, Eq, Hash)]
enum GameScreen { #[default] MainMenu, Playing, Paused }

app.init_state::<GameScreen>()
   .add_systems(OnEnter(GameScreen::MainMenu), spawn_main_menu)
   .add_systems(OnExit(GameScreen::MainMenu), despawn_main_menu)
   .add_systems(OnEnter(GameScreen::Playing), spawn_hud);

#[derive(Component)]
struct MainMenuRoot;

fn spawn_main_menu(mut commands: Commands) {
    commands.spawn((MainMenuRoot, Node { ..default() }));
}

fn despawn_main_menu(mut commands: Commands, q: Query<Entity, With<MainMenuRoot>>) {
    for entity in &q { commands.entity(entity).despawn(); }
}
```

## Animation and Transitions

### TryStableInterpolate (0.18)
`Val` and `Color` now support interpolation (same-unit/same-colorspace only):

```rust
use bevy::math::TryStableInterpolate;

let a = Val::Px(100.0);
let b = Val::Px(300.0);
let result = a.try_interpolate_stable(&b, 0.5); // Ok(Val::Px(200.0))

// Fails if units differ:
let c = Val::Percent(50.0);
let _ = a.try_interpolate_stable(&c, 0.5); // Err — snap instead
```

Use with Bevy's animation system for smooth UI transitions.

### Manual Lerp for Simple Animations
```rust
fn animate_width(mut q: Query<&mut Node, With<AnimatedBar>>, time: Res<Time>) {
    for mut node in &mut q {
        let target = 300.0;
        if let Val::Px(ref mut current) = node.width {
            *current += (target - *current) * time.delta_secs() * 5.0;
        }
    }
}
```

## Performance Tips

1. **Minimize hierarchy depth** — deep nesting increases layout cost.
2. **Use `Display::None`** instead of despawning/respawning for toggled UI.
3. **Avoid per-frame text updates** unless the text actually changed — use `Changed<T>` filters.
4. **Prefer `Visibility::Hidden`** for elements that are temporarily hidden but will reappear.
5. **Batch similar styles** — entities with identical component sets share archetypes.
6. **Use `LayoutConfig`** for fine-grained control over layout behavior if needed.

## Debugging Layout

### UI Debug Overlay
```rust
// Toggle in code:
fn toggle_debug(mut options: ResMut<UiDebugOptions>, input: Res<ButtonInput<KeyCode>>) {
    if input.just_pressed(KeyCode::F1) {
        options.toggle();
    }
}
```

Shows colored outlines for every UI node, helping visualize bounds, padding, margins.
In 0.18, the overlay also shows clipped sections and scrollbar outlines.

### Common Debugging Steps
1. Check if the node has a size — `width`/`height` default to `Auto` which is zero for empty nodes.
2. Check `display` is not `None`.
3. Check parent has appropriate `flex_direction` and `align_items`/`justify_content`.
4. Check overflow is not clipping children unexpectedly.
5. Use `BackgroundColor` on suspects to visualize bounds.
6. Remember: default `flex_direction` in Bevy is **Column**, not Row.

## Common Pitfalls

### 1. "My UI node is invisible / zero-sized"
- Root node needs explicit `width`/`height` (usually `Val::Percent(100.0)`).
- Text nodes auto-size. Empty `Node` with no children and no size = 0x0.

### 2. "Layout is vertical when I expected horizontal"
- Bevy default `flex_direction` is `Column`. Set `FlexDirection::Row` explicitly.

### 3. "My scroll container doesn't scroll"
- Container must have a bounded height/width.
- Must set `overflow: Overflow::scroll_y()` (or `scroll_x()`, `scroll()`).

### 4. "My button text isn't centered"
- Add `justify_content: JustifyContent::Center` AND `align_items: AlignItems::Center`
  to the button's `Node`.

### 5. "Using BorderRadius as a component does nothing in 0.18"
- BorderRadius moved to a field on `Node` in 0.18. Set `node.border_radius = ...`.

### 6. "My absolute-positioned element is in the wrong place"
- Absolute position is relative to the nearest ancestor with `PositionType::Relative`
  (which is the default), or the viewport if none.
- Set `left`, `top`, `right`, `bottom` on the `Node`.

### 7. "Observers not firing on my widget"
- Ensure `InputFocus` resource is initialized: `app.init_resource::<InputFocus>()`.
- Ensure the entity has `Interaction` (or a widget component that requires it).

### 8. "Gamepad/keyboard navigation doesn't work"
- Add `AutoDirectionalNavigation::default()` to navigable entities (0.18).
- Or manually wire `DirectionalNavigationMap`.
- Use `AutoDirectionalNavigator` system parameter to handle input.

### 9. "Querying `GlobalTransform` on UI entities returns nothing / compiler error"
- Since 0.17, UI nodes use `UiGlobalTransform` (not `GlobalTransform`).
- Replace `Query<&GlobalTransform, With<Node>>` → `Query<&UiGlobalTransform, With<Node>>`.
- `Transform`/`GlobalTransform` are still used for non-UI entities (sprites, meshes, cameras).
