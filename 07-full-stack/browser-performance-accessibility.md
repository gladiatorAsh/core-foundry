# Browser internals, web performance, accessibility

## What happens when you type a URL (classic opener; aim for 2 minutes)

DNS lookup (browser/OS/resolver caches) → TCP + TLS handshake (or QUIC for HTTP/3) → HTTP request → server/CDN response →
**parse HTML → DOM**; CSS → **CSSOM**; DOM + CSSOM → **render tree** → **layout** (geometry) → **paint** → **composite** layers on the GPU.
`<script>` without `defer`/`async` blocks parsing; CSS blocks rendering. JS can change DOM/CSSOM and trigger re-layout.

- **Reflow (layout)** is expensive; avoid layout thrashing (alternating reads like `offsetHeight` with writes). Batch DOM reads, then writes.
- Animate **`transform` and `opacity`** (compositor-only) instead of `top/left/width` (layout + paint).
- `defer`: download in parallel, execute in order after parsing. `async`: execute as soon as downloaded (order not guaranteed).

## Core Web Vitals (Google's user-experience metrics; "good" at the 75th percentile of real users)

| Metric | Measures | Good | Common fixes |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | Loading: when the main content appears | ≤ 2.5 s | Fast server/CDN, preload the hero image/font, avoid client-only rendering of main content, compress/resize images (AVIF/WebP), don't lazy-load the LCP image |
| **INP** (Interaction to Next Paint) | Responsiveness of all interactions | ≤ 200 ms | Break up long tasks (> 50 ms), yield to the main thread, less JS, defer non-critical work, move heavy work to Web Workers |
| **CLS** (Cumulative Layout Shift) | Visual stability | ≤ 0.1 | Set width/height or aspect-ratio on media, reserve space for ads/embeds, `font-display` + size-adjusted fallbacks |

**INP replaced FID in March 2024.** Supporting metrics: TTFB, FCP, TBT (lab proxy for INP). Lab tools (Lighthouse) ≠ field data (CrUX, RUM).

## Loading strategy checklist

- Ship less JavaScript: code-split by route, tree-shake, drop unused dependencies, audit the bundle.
- Images: responsive `srcset`/`sizes`, modern formats, `loading="lazy"` below the fold, `fetchpriority="high"` for the LCP image.
- Fonts: self-host, subset, `preload` the critical one, `font-display: swap`.
- Resource hints: `preconnect` to critical origins, `preload` critical assets, `prefetch` likely next routes.
- Rendering strategy: SSR/SSG for content pages; stream HTML; hydrate less (islands, Server Components).
- Caching: hashed filenames + `Cache-Control: public, max-age=31536000, immutable`; HTML short-lived or `no-cache` + ETag;
  service workers for offline/app shell.
- Compression: Brotli/gzip. HTTP/2 multiplexing (so domain sharding is obsolete); HTTP/3 over QUIC avoids TCP head-of-line blocking.

## Browser storage

| | Size | Lifetime | Sent to server | Use |
|---|---|---|---|---|
| Cookies | ~4 KB | Set by expiry | **Every request** | Sessions (`HttpOnly; Secure; SameSite`) |
| localStorage | ~5–10 MB | Until cleared | No | Small preferences (synchronous API, so keep it small; never tokens if XSS is a risk) |
| sessionStorage | ~5 MB | Tab lifetime | No | Per-tab state |
| IndexedDB | Large | Until cleared | No | Offline data, large structured data (async) |
| Cache API | Large | Until cleared | No | Service-worker response cache |

## Accessibility (a11y): expected at Staff level

- Standard: **WCAG 2.2 AA**. Principles: perceivable, operable, understandable, robust.
- **Semantic HTML first** (`button`, `a`, `nav`, `main`, `label`, headings in order). "No ARIA is better than bad ARIA."
- Everything works with the **keyboard**: focus order, visible focus, no keyboard traps; modals trap focus while open and return it on close.
- Text alternatives (`alt`), form labels, error messages linked with `aria-describedby`.
- Color contrast ≥ **4.5:1** for normal text (3:1 for large text and UI components); never color alone.
- Dynamic updates announced with `aria-live` regions; respect `prefers-reduced-motion`.
- Test with axe/Lighthouse, keyboard-only use, and a screen reader (VoiceOver, NVDA).

## Rendering patterns cheat sheet

CSR · SSR · SSG · ISR (incremental static regeneration) · streaming SSR · islands architecture · React Server Components · edge rendering.
Pick by content freshness, personalization, SEO needs, and interactivity.
