# Frontend system design

Different from backend design: the focus is **component architecture, state, data fetching, rendering, performance, accessibility, and API
contracts with the backend**. Backend boxes stay at "an API exists".

## RADIO framework (45–60 min)

| Step | Time | Content |
|---|---|---|
| **R**equirements | ~10% | Core features, devices (mobile/desktop), offline?, i18n, accessibility, performance targets, scale (items, users) |
| **A**rchitecture | ~20% | Component tree, where state lives (server cache / client store / URL), rendering strategy (CSR/SSR/SSG), main modules |
| **D**ata model | ~10% | Client-side entities and normalized store shape; what's server state vs UI state |
| **I**nterface (API) | ~15% | Endpoints or GraphQL queries the UI needs, pagination (cursor), real-time channel, error shapes, and component props APIs |
| **O**ptimizations | ~45% | Performance (virtualization, code splitting, caching, prefetch), network (batching, retries, optimistic updates), a11y, i18n, security (XSS, CSP), offline, observability |

## Case studies (outlines)

### 1. Autocomplete / typeahead component
- Debounce input (~200–300 ms); cancel stale requests with `AbortController` (or ignore responses out of order using a request ID).
- Client cache of query → results (LRU, with TTL); prefix reuse for filtering locally.
- Keyboard: ↑/↓ moves the active option, Enter selects, Esc closes; ARIA **combobox** pattern (`aria-expanded`, `aria-activedescendant`, `role="listbox"`/`option`).
- Highlight the matched substring safely (no `innerHTML` with user input).
- Props API: `fetchSuggestions`, `renderItem`, `minChars`, `debounceMs`, `onSelect`.

### 2. News feed (infinite scroll)
- Cursor-based pagination; `IntersectionObserver` sentinel to load more; **virtualize** the list; keep scroll position on back navigation.
- Normalized store (posts by ID; feed = list of IDs) so likes update everywhere. Optimistic updates for likes/comments with rollback.
- New-posts indicator instead of shifting content (CLS); image dimensions reserved; lazy-load media.
- SSR the first page for fast LCP; prefetch the next page when idle.

### 3. Chat application (web)
- WebSocket with reconnect and backoff, heartbeat, and resubscribe; fall back to SSE/long-polling.
- Message states: sending → sent → delivered → read; client-generated IDs for idempotent retries and dedupe.
- Ordering by server sequence number; gap detection triggers a fetch of missed messages.
- Virtualized message list anchored to the bottom; pagination upward; unread markers.
- Offline queue in IndexedDB; notifications via the Notifications API / service worker.
- **AI chat specifics** (your domain): stream tokens over SSE, render Markdown incrementally and safely, stop/regenerate,
  show citations, and handle partial failures mid-stream.

### 4. Data grid / table (100K rows)
- Server-side sort/filter/pagination for large data; virtualize rows *and* columns; sticky headers; resizable columns.
- Accessible grid semantics (`role="grid"`, keyboard cell navigation). Export via server job for big datasets.

### 5. Collaborative document editor (Google Docs-like)
- Conflict resolution: **OT** (operational transformation; central server transforms ops) vs **CRDTs** (e.g. Yjs/Automerge; merge without a central authority, good offline).
- Presence/cursors over WebSocket; local-first edits, then sync; snapshot + op log persistence; undo per user.

### 6. Image gallery / carousel
- Responsive images, lazy loading, preloading neighbors, swipe gestures, keyboard + screen-reader support, reduced motion.

### 7. E-commerce checkout
- Multi-step form with validation (client + server), saved progress, idempotent "place order" (disable double submit + idempotency key),
  payment iframe / hosted fields (PCI scope reduction), address autocomplete, error recovery, analytics funnel.

## Cross-cutting talking points

- **Server state ≠ client state.** Use a query cache for server data; keep client stores small.
- **Optimistic UI** with rollback and conflict messaging.
- **Error and loading states** for every async boundary (`Suspense` + error boundaries); skeletons over spinners for layout stability.
- **Observability:** RUM (Core Web Vitals), JS error tracking (Sentry), feature flags, A/B testing.
- **Security:** escape output, CSP, avoid `dangerouslySetInnerHTML`, HttpOnly cookies, CSRF protection.
- **i18n:** ICU message formats, RTL layouts, locale-aware dates/numbers.
- **Design system:** shared accessible components, tokens, theming (light/dark), documentation (Storybook).
