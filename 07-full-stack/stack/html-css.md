# HTML5 and CSS3

## Semantic HTML5

`header`, `nav`, `main` (one per page), `article`, `section` (with a heading), `aside`, `footer`, `figure`/`figcaption`, `time`, `button` (actions) vs `a` (navigation).
Forms: `label for`, input types (`email`, `number`, `date`), built-in validation (`required`, `pattern`), `fieldset`/`legend`.
Benefits: accessibility (screen readers navigate landmarks), SEO, less ARIA needed.

## The cascade and specificity

- Order of precedence: origin & importance (`!important`) → **cascade layers** (`@layer`) → **specificity** → source order.
- Specificity (a, b, c): IDs (1,0,0) > classes/attributes/pseudo-classes (0,1,0) > elements/pseudo-elements (0,0,1). Inline styles beat all selectors.
  `:where()` adds zero specificity; `:is()`/`:not()` take their most specific argument.
- Inheritance: text properties (color, font) inherit; box properties (margin, border) don't.

## Box model

Content + padding + border + margin. `box-sizing: border-box` makes `width` include padding and border (set it globally).
Vertical margins between blocks **collapse**. Block formatting contexts (BFC; created by `display: flow-root`, flex/grid items, `overflow` other than visible) contain floats and stop margin collapse.

## Layout

| Use | Tool |
|---|---|
| One-dimensional (row *or* column), distributing space | **Flexbox** (`justify-content` main axis, `align-items` cross axis, `flex: 1 1 0`, `gap`) |
| Two-dimensional (rows *and* columns), page layouts | **Grid** (`grid-template-columns: repeat(auto-fill, minmax(200px, 1fr))`, named areas) |
| Overlays / pinned elements | `position: absolute/fixed/sticky` |

Centering: `display: grid; place-items: center` (or flex with `justify-content` + `align-items`).

**Positioning:** `relative` (offset from normal position, becomes the containing block for absolute children), `absolute` (relative to the nearest positioned ancestor),
`fixed` (viewport; broken by transformed ancestors), `sticky` (relative until a threshold, then fixed within its container).

**Stacking contexts:** `z-index` only compares within the same stacking context. New contexts come from positioned elements with z-index, `opacity < 1`, `transform`, `filter`, `isolation: isolate`.
This is why "z-index: 9999 doesn't work".

## Responsive design

Mobile-first media queries (`@media (min-width: 768px)`), **container queries** (`@container`; components respond to their container, not the viewport),
relative units (`rem` for type, `%`/`fr`/`vw`), `clamp()` for fluid type, responsive images (`srcset`, `sizes`, `<picture>`), `prefers-color-scheme`, `prefers-reduced-motion`.

## Modern CSS worth mentioning

Custom properties (`--brand: #0078d4`, themeable at runtime), `:has()` (parent selector), nesting, `@layer`, logical properties (`margin-inline`), `aspect-ratio`,
`color-mix()`, scroll-driven animations, view transitions.

## Architecture at scale

BEM naming, CSS Modules (scoped class names), utility-first (Tailwind), CSS-in-JS (runtime cost; zero-runtime alternatives), design tokens. Pick one and enforce it.

## Performance

Critical CSS inline, the rest loaded non-blocking; avoid huge selectors and deep nesting; animate `transform`/`opacity`; `content-visibility: auto` for long off-screen sections (careful with anchor links);
`will-change` sparingly.
