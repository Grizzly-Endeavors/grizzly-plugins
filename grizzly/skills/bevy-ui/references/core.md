# Core UI Components, Layout, and Styling

## Table of Contents
1. [Minimal Setup](#minimal-setup)
2. [The Node Component](#the-node-component)
3. [Val Enum — Sizing Units](#val-enum)
4. [Flexbox Layout](#flexbox-layout)
5. [CSS Grid Layout](#css-grid-layout)
6. [Visual Styling Components](#visual-styling-components)
7. [Text and Fonts](#text-and-fonts)
8. [Images in UI](#images-in-ui)
9. [Scrolling](#scrolling)
10. [Z-Ordering](#z-ordering)
11. [Camera Targeting](#camera-targeting)
12. [UI Transforms](#ui-transforms-uitransform--uiglobaltransform)

---

## Minimal Setup

```rust
use bevy::prelude::*;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup_ui)
        .run();
}

fn setup_ui(mut commands: Commands) {
    commands.spawn(Camera2d);

    // Root UI node — full screen flex container
    commands.spawn(Node {
        width: Val::Percent(100.0),
        height: Val::Percent(100.0),
        justify_content: JustifyContent::Center,
        align_items: AlignItems::Center,
        ..default()
    }).with_children(|parent| {
        parent.spawn((
            Text::new("Hello Bevy UI!"),
            TextFont { font_size: 40.0, ..default() },
        ));
    });
}
```

Key points:
- A camera entity is required (Camera2d or Camera3d).
- Root nodes without a parent fill from the top-left of the viewport by default.
- `Node` is THE layout component. Every UI entity needs one (or a widget that requires one).

## The Node Component

`Node` is the base component for all UI entities. It has 41 fields controlling layout and style.
When `Node` is inserted, these required components are auto-inserted:
`ComputedNode`, `ComputedUiTargetCamera`, `ComputedUiRenderTargetInfo`, `UiTransform`,
`BackgroundColor`, `BorderColor`, `FocusPolicy`, `ScrollPosition`, `Visibility`, `ZIndex`.

### Key Node Fields

```rust
Node {
    // Display mode
    display: Display,              // Flex (default), Grid, Block, None

    // Box model
    box_sizing: BoxSizing,         // BorderBox (default) or ContentBox
    width: Val,                    // default: Auto
    height: Val,                   // default: Auto
    min_width: Val, min_height: Val,
    max_width: Val, max_height: Val,
    aspect_ratio: Option<f32>,

    // Positioning
    position_type: PositionType,   // Relative (default) or Absolute
    left: Val, right: Val, top: Val, bottom: Val,

    // Flexbox
    flex_direction: FlexDirection, // Column (default!), Row, ColumnReverse, RowReverse
    flex_wrap: FlexWrap,           // NoWrap (default), Wrap, WrapReverse
    flex_grow: f32,                // 0.0 (default) — how much to grow
    flex_shrink: f32,              // 1.0 (default) — how much to shrink
    flex_basis: Val,               // Auto (default) — initial size before grow/shrink

    // Alignment
    align_items: AlignItems,       // Default (Stretch for flex)
    justify_content: JustifyContent, // Default (FlexStart)
    align_self: AlignSelf,
    justify_self: JustifySelf,
    align_content: AlignContent,
    justify_items: JustifyItems,

    // Spacing
    margin: UiRect,
    padding: UiRect,
    border: UiRect,
    border_radius: BorderRadius,   // NEW in 0.18: moved here from separate component
    row_gap: Val,
    column_gap: Val,

    // Overflow & scroll
    overflow: Overflow,
    scrollbar_width: f32,
    overflow_clip_margin: OverflowClipMargin,

    // CSS Grid
    grid_auto_flow: GridAutoFlow,
    grid_template_rows: Vec<RepeatedGridTrack>,
    grid_template_columns: Vec<RepeatedGridTrack>,
    grid_auto_rows: Vec<GridTrack>,
    grid_auto_columns: Vec<GridTrack>,
    grid_row: GridPlacement,
    grid_column: GridPlacement,
}
```

**IMPORTANT**: Bevy UI default `flex_direction` is `Column` (top to bottom), unlike CSS which
defaults to `Row`. This is the most common source of unexpected layouts.

## Val Enum

`Val` represents dimensional values:

```rust
Val::Auto          // let layout engine decide
Val::Px(f32)       // logical pixels
Val::Percent(f32)  // percentage of parent's size on the same axis
Val::Vw(f32)       // percentage of viewport width
Val::Vh(f32)       // percentage of viewport height
Val::VMin(f32)     // percentage of viewport's smaller dimension
Val::VMax(f32)     // percentage of viewport's larger dimension
```

Convenience functions: `px(v)`, `percent(v)`, `vh(v)`, `vw(v)`, `vmin(v)`, `vmax(v)`, `auto()`.

```rust
use bevy::ui::{px, percent};
Node { width: px(200.0), height: percent(50.0), ..default() }
```

### UiRect for margins/padding/border

```rust
UiRect::all(Val::Px(10.0))                    // uniform
UiRect::axes(Val::Px(20.0), Val::Px(10.0))   // horizontal, vertical
UiRect::new(left, right, top, bottom)          // individual sides
UiRect::left(Val::Px(5.0))                    // single side, rest Auto
UiRect { left: Val::Px(5.0), ..UiRect::DEFAULT } // explicit
```

## Flexbox Layout

Bevy's Flexbox matches CSS Flexbox semantics. Core concepts:

### Direction and Wrapping
```rust
Node {
    flex_direction: FlexDirection::Row,     // or Column, RowReverse, ColumnReverse
    flex_wrap: FlexWrap::Wrap,              // or NoWrap, WrapReverse
    ..default()
}
```

### Alignment (main axis = direction of flex_direction, cross axis = perpendicular)
```rust
Node {
    // Main axis distribution of children
    justify_content: JustifyContent::SpaceBetween, // Start, End, Center, SpaceAround, SpaceEvenly
    // Cross axis alignment of children
    align_items: AlignItems::Center,     // Start, End, Center, Stretch, Baseline
    // Multi-line cross axis distribution
    align_content: AlignContent::Center,
    ..default()
}
```

### Flex Item Properties
```rust
Node {
    flex_grow: 1.0,    // take up available space proportionally
    flex_shrink: 0.0,  // don't shrink below basis
    flex_basis: Val::Px(200.0), // starting size
    align_self: AlignSelf::FlexEnd, // override parent's align_items
    ..default()
}
```

### Centering (most common pattern)
```rust
Node {
    width: Val::Percent(100.0),
    height: Val::Percent(100.0),
    justify_content: JustifyContent::Center,
    align_items: AlignItems::Center,
    ..default()
}
```

### Gaps Between Items
```rust
Node {
    row_gap: Val::Px(10.0),
    column_gap: Val::Px(20.0),
    ..default()
}
```

## CSS Grid Layout

Set `display: Display::Grid` to use CSS Grid.

```rust
Node {
    display: Display::Grid,
    width: Val::Percent(100.0),
    grid_template_columns: vec![
        GridTrack::flex(1.0),       // 1fr
        GridTrack::px(200.0),       // 200px fixed
        GridTrack::flex(2.0),       // 2fr
    ],
    grid_template_rows: vec![
        GridTrack::auto(),          // auto-sized
        GridTrack::px(100.0),
        GridTrack::min_content(),
    ],
    row_gap: Val::Px(8.0),
    column_gap: Val::Px(8.0),
    ..default()
}
```

### Grid Item Placement
```rust
Node {
    grid_column: GridPlacement::span(2),  // span 2 columns
    grid_row: GridPlacement::start(1),    // start at row 1 (1-indexed)
    ..default()
}
```

### Repeated Tracks
```rust
grid_template_columns: vec![
    RepeatedGridTrack::flex(3, 1.0),  // repeat(3, 1fr)
],
```

## Visual Styling Components

### BackgroundColor
```rust
commands.spawn((Node { ..default() }, BackgroundColor(Color::srgb(0.2, 0.2, 0.2))));
```

### BorderColor and Borders
```rust
Node {
    border: UiRect::all(Val::Px(2.0)),
    border_radius: BorderRadius::all(Val::Px(8.0)), // 0.18: field on Node!
    ..default()
},
BorderColor(Color::WHITE),
```

`BorderColor` supports per-side colors:
```rust
let mut bc = BorderColor::default();
bc.top = Color::srgb(1.0, 0.0, 0.0);
bc.bottom = Color::srgb(0.0, 0.0, 1.0);
```

### BorderRadius Variants
```rust
BorderRadius::all(Val::Px(10.0))
BorderRadius::top(Val::Px(10.0))
BorderRadius::bottom(Val::Px(10.0))
BorderRadius::left(Val::Px(10.0))
BorderRadius::right(Val::Px(10.0))
BorderRadius::new(top_left, top_right, bottom_right, bottom_left) // each a Val
BorderRadius::MAX // fully circular / pill shape
```

### BoxShadow
```rust
commands.spawn((
    Node { ..default() },
    BoxShadow(vec![
        ShadowStyle {
            color: Color::srgba(0.0, 0.0, 0.0, 0.5),
            x_offset: Val::Px(2.0),
            y_offset: Val::Px(4.0),
            blur_radius: Val::Px(8.0),
            spread_radius: Val::Px(0.0),
            ..default()
        },
    ]),
));
```

### Gradients (introduced 0.17, available 0.18)
```rust
commands.spawn((
    Node { width: px(200.0), height: px(100.0), ..default() },
    BackgroundGradient(vec![Gradient::Linear(LinearGradient {
        angle: 90.0_f32.to_radians(),
        stops: vec![
            ColorStop { color: Color::srgb(1.0, 0.0, 0.0), position: Val::Percent(0.0) },
            ColorStop { color: Color::srgb(0.0, 0.0, 1.0), position: Val::Percent(100.0) },
        ],
        ..default()
    })]),
));
```

Also available: `ConicGradient`, `RadialGradient`, `BorderGradient`.

### Outline (does NOT affect layout)
```rust
Outline {
    width: Val::Px(2.0),
    offset: Val::Px(2.0),
    color: Color::srgb(1.0, 0.8, 0.0),
}
```

## Text and Fonts

### Basic Text
```rust
commands.spawn((
    Text::new("Hello!"),
    TextFont {
        font: asset_server.load("fonts/MyFont.ttf"),
        font_size: 32.0,
        ..default()
    },
    TextColor(Color::WHITE),
));
```

### Rich Text with TextSpan (multi-section)
```rust
commands.spawn((
    Text::new("Normal text "),
    TextFont { font_size: 20.0, ..default() },
)).with_children(|parent| {
    parent.spawn((
        TextSpan::new("bold part"),
        TextFont { font_size: 20.0, ..default() },
        FontWeight(700),
    ));
});
```

### 0.18 Font Features

**Font Weight** (variable fonts):
```rust
TextFont { font_size: 24.0, weight: FontWeight(400), ..default() }
// FontWeight wraps u16 clamped 1-1000; 400=normal, 700=bold
```

**Strikethrough and Underline**:
```rust
commands.spawn((Text::new("Deleted"), Strikethrough::default()));
commands.spawn((Text::new("Link"), Underline::default()));
// Optional color:
StrikethroughColor(Color::srgb(1.0, 0.0, 0.0))
UnderlineColor(Color::srgb(0.0, 0.0, 1.0))
```

**OpenType Font Features** (.otf fonts):
```rust
TextFont {
    font_features: FontFeatures::builder()
        .enable(FontFeatureTag::STANDARD_LIGATURES)
        .set(FontFeatureTag::WIDTH, 300)
        .build(),
    ..default()
}
// Or from array:
TextFont {
    font_features: [FontFeatureTag::STANDARD_LIGATURES, FontFeatureTag::SLASHED_ZERO].into(),
    ..default()
}
```

**LineHeight** (0.18: separate component):
```rust
commands.spawn((Text::new("Spaced"), LineHeight(1.8)));
```

**TextBackgroundColor** (per-span backgrounds):
```rust
commands.spawn((Text::new("Highlight me"), TextBackgroundColor(Color::srgba(1.0, 1.0, 0.0, 0.3))));
```

### Pickable Text Sections (0.18)
Individual text sections (TextSpan entities) are now pickable. Add observers for
click/hover behavior on specific words — useful for hyperlinks or tooltips.

## Images in UI

```rust
commands.spawn((
    ImageNode::new(asset_server.load("icon.png")),
    Node { width: px(64.0), height: px(64.0), ..default() },
));
```

`ImageNode` supports 9-slice via `ImageScaleMode::Sliced(TextureSlicer { .. })`.

## Scrolling

Set `overflow` to enable scrolling:
```rust
Node {
    overflow: Overflow::scroll_y(),   // vertical scroll
    // or Overflow::scroll_x(), Overflow::scroll(), Overflow::clip()
    height: Val::Px(300.0),           // container must have bounded size
    flex_direction: FlexDirection::Column,
    ..default()
}
```

Scroll position is stored in the `ScrollPosition` component (auto-inserted with Node).
Handle scroll events via the `Scroll` entity event with `On<Scroll>` observers or by
manually modifying `ScrollPosition`.

### IgnoreScroll (0.18)
Makes a child ignore parent scroll position — for sticky headers/columns:
```rust
commands.spawn((Node { ..default() }, IgnoreScroll { x: false, y: true }));
```

## Z-Ordering

- **`ZIndex`**: Controls front-to-back among siblings. Higher = on top.
  ```rust
  ZIndex(10) // above siblings with lower ZIndex
  ```
- **`GlobalZIndex`**: Escapes the hierarchy. Rendered above/below ALL other nodes.
  ```rust
  GlobalZIndex(100) // above everything with lower GlobalZIndex
  ```

## Camera Targeting

Attach UI to a specific camera (for multi-camera setups):
```rust
commands.spawn((
    Node { ..default() },
    UiTargetCamera(camera_entity),
));
```

Default behavior: UI renders to the camera with `IsDefaultUiCamera`, falling back to the
`PrimaryWindow` camera.

## UI Transforms (UiTransform / UiGlobalTransform)

Since Bevy 0.17, UI nodes use **`UiTransform`** and **`UiGlobalTransform`** instead of the general-purpose
`Transform` and `GlobalTransform`. These are specialized 2D transforms optimized for the UI layer,
avoiding redundant 3D transform propagation alongside the layout algorithm.

### UiTransform

```rust
UiTransform {
    translation: Val2,    // 2D offset using Val2 (e.g. Val2::px(x, y))
    rotation: Rot2,       // 2D rotation (clockwise)
    scale: Vec2,          // 2D scale (negative values reflect)
}
```

`UiTransform` is automatically inserted as a required component when `Node` is added.
**Do not modify `UiTransform` directly.** Position nodes through `Node` layout fields
(`position_type`, `left`, `right`, `top`, `bottom`, etc.). The layout system computes
`UiTransform` values during `ui_layout_system`.

### UiGlobalTransform

`UiGlobalTransform` is the absolute 2D screen-space transform, analogous to `GlobalTransform`
for world-space entities. It is computed from `UiTransform` and `Node` during layout. It wraps
a 2D affine matrix and provides:

- `transform_point2(point)` — apply full transform (shear, scale, rotation, translation)
- `transform_vector2(vector)` — apply rotation/scale only (no translation)
- `inverse()` — returns `Option`, `None` if not invertible
- `to_cols_array()` / `to_cols_array_2d()` — column-major matrix data

### Migration from Transform/GlobalTransform

If migrating code from Bevy ≤0.16 that queries `GlobalTransform` on UI entities:

```rust
// OLD (≤0.16) — no longer works for UI entities
fn ui_system(query: Query<&GlobalTransform, With<Node>>) { .. }

// NEW (0.17+) — use UiGlobalTransform
fn ui_system(query: Query<&UiGlobalTransform, With<Node>>) { .. }
```

Note: `Transform`/`GlobalTransform` still exist and are used for all non-UI entities (sprites,
meshes, cameras, etc.). Only UI nodes (`Node` entities) use the `Ui*Transform` variants.
