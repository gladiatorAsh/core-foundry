# React (and how Angular differs)

## Rendering model

- A component is a function of props + state → UI description. React **re-renders** a component when its state changes, its parent re-renders, or a context it uses changes.
- **Render** (call components, build the element tree) vs **commit** (apply DOM changes, run layout effects, then effects).
- **Reconciliation:** React diffs the new tree against the previous one. Different element type → unmount/remount the subtree. Same type → update props.
- **Keys** identify list items across renders. Use stable IDs, **not array indexes**, when items can be reordered, inserted, or deleted;
  otherwise state (input values, focus) attaches to the wrong item.
- React 18+ **concurrent rendering**: rendering can be interrupted; `startTransition`/`useTransition` marks non-urgent updates;
  `useDeferredValue` defers expensive derived UI. Automatic batching groups state updates (including in promises/timeouts).

## Hooks

- **Rules:** call hooks only at the top level of components/custom hooks (not in loops/conditions), because React tracks hooks by call order.
- `useState` (functional updates `setX(x => x + 1)` avoid stale values) · `useReducer` (complex state transitions) ·
  `useRef` (mutable box that doesn't trigger renders; DOM refs) · `useContext`.
- `useEffect` runs **after paint** for synchronizing with external systems (subscriptions, fetching, DOM APIs). Return a cleanup.
  The dependency array must include every reactive value used. In Strict Mode dev, effects run setup → cleanup → setup to surface missing cleanups.
- `useLayoutEffect` runs before paint (measure the DOM to avoid flicker). `useId` for accessible IDs. `useSyncExternalStore` for external stores.
- **You might not need an effect:** derive values during render instead of syncing state with effects; handle user events in event handlers.
- **Stale closures:** an effect or callback captures the values from the render it was created in. Fix with correct dependencies, functional updates, or a ref.

```tsx
function useDebouncedValue<T>(value: T, ms: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), ms);
    return () => clearTimeout(id);           // cancel when value changes or on unmount
  }, [value, ms]);
  return debounced;
}
```

## Performance

- Measure first (React DevTools Profiler). Common fixes: move state down / lift content up (composition), split contexts,
  `React.memo` for expensive pure children, `useMemo` / `useCallback` for stable props and costly computations (they cost something too).
- Virtualize long lists (react-window / TanStack Virtual). Code-split routes with `lazy` + `Suspense`.
- The **React Compiler** (stable in 2025) auto-memoizes components and hooks, reducing manual `useMemo`/`useCallback`. Know that it exists and what it does.

## State management: pick by kind of state

| State | Tool |
|---|---|
| Server/cache state (fetched data) | **TanStack Query** / SWR / RTK Query: caching, dedupe, retries, invalidation, stale-while-revalidate |
| Local UI state | `useState` / `useReducer` |
| Shared client state | Context (low-frequency), Zustand, Redux Toolkit, Jotai |
| URL state (filters, pagination) | The router's search params; shareable and survives reloads |
| Form state | React Hook Form + schema validation (zod) |

## Server rendering and React Server Components

- **CSR** (client renders everything) → fast navigations, slow first load, weaker SEO. **SSR** (HTML per request, then hydrate) → fast first paint, server cost.
  **SSG/ISR** (pre-built, revalidated) → fastest for mostly static pages.
- **Hydration:** attaching event handlers to server-rendered HTML; server and client markup must match.
- **React Server Components** (Next.js App Router): components that run only on the server (direct data access, zero client JS); `"use client"` marks interactive boundaries;
  Server Actions handle mutations. Streaming with `Suspense` sends HTML in chunks.

## Testing

React Testing Library (test behavior through the DOM the way users interact; query by role/label) · Jest or Vitest ·
Playwright/Cypress for E2E · MSW to mock network calls · test hooks via components.

## Angular differences (since you've used both)

| | React | Angular |
|---|---|---|
| Type | UI library + ecosystem | Full framework (router, DI, forms, HTTP built in) |
| Change detection | Re-render on state change, diff the virtual DOM | Zone.js-based change detection, moving to **Signals** and zoneless (stable in recent versions) |
| Data flow | One-way; props down, callbacks up | One-way + two-way binding (`[(ngModel)]`) |
| Async | Promises / hooks | RxJS Observables everywhere (HTTP, forms, events) |
| DI | None built in (context as a substitute) | Hierarchical dependency injection |

Be ready to say which you'd choose for a new project and why (team skills, ecosystem, enterprise structure vs flexibility).
