# Angular, Redux, and D3.js

## Angular

- **Building blocks:** components (template + class + styles), directives (structural like `@if`/`@for` control flow, attribute directives), pipes, services, **dependency injection**
  (`providedIn: 'root'` singletons; hierarchical injectors per component tree), router (lazy-loaded routes, guards, resolvers), HTTP client with **interceptors** (auth headers, error handling).
- **Standalone components** are now the default (NgModules are optional/legacy).
- **Change detection:** historically Zone.js patches async APIs and checks the component tree after every async event. `ChangeDetectionStrategy.OnPush` only checks a component when its inputs change
  (by reference), an event fires inside it, or an observable used with the `async` pipe emits. **Signals** (`signal`, `computed`, `effect`) give fine-grained reactivity and enable zoneless apps.
- **RxJS** (core to Angular): Observables are lazy streams. Know the higher-order mapping operators cold:

| Operator | Behavior | Use for |
|---|---|---|
| `switchMap` | Cancels the previous inner observable | Typeahead search (only the latest query matters) |
| `mergeMap` | Runs all concurrently | Independent parallel requests |
| `concatMap` | Queues; one at a time, in order | Ordered writes |
| `exhaustMap` | Ignores new values while busy | Login / submit button double-clicks |

  Plus `debounceTime`, `distinctUntilChanged`, `combineLatest`, `forkJoin`, `catchError`, `retry`, `shareReplay`, `takeUntil`/`takeUntilDestroyed` (avoid subscription leaks).
- **Forms:** reactive forms (`FormGroup`, typed, testable; preferred for complex forms) vs template-driven (`ngModel`).
- Lifecycle hooks: `ngOnInit`, `ngOnChanges`, `ngAfterViewInit`, `ngOnDestroy` (cleanup).
- State management: services with signals/BehaviorSubjects for most apps; NgRx (Redux pattern) for large, complex shared state.

## Redux (and Redux Toolkit)

- One **store**; state changes only by dispatching **actions** to pure **reducers** `(state, action) => newState`; components subscribe via selectors.
  Benefits: predictable updates, time-travel debugging, a single place for shared state.
- **Redux Toolkit (RTK)** is the official, modern way: `configureStore`, `createSlice` (uses Immer so you can "mutate" drafts safely), `createAsyncThunk`, and **RTK Query** for data fetching and caching.
- Middleware intercepts actions (thunks for async logic, logging, analytics). Selectors with `createSelector` (Reselect) memoize derived data.
- Keep the store **normalized** (`{ ids: [], entities: {} }`, `createEntityAdapter`).
- When **not** to use Redux: server state belongs in a query cache (TanStack Query / RTK Query); local UI state belongs in components. Redux is for genuinely shared, complex client state.

## D3.js (data visualization)

- **Selections and data joins:** bind data to DOM elements; `selection.data(data, keyFn).join("rect")` handles **enter** (new data), **update**, and **exit** (removed data).
  The key function keeps elements matched to the right data across updates.
- **Scales** map data to pixels: `scaleLinear`, `scaleBand` (bar charts), `scaleTime`, `scaleOrdinal` (colors); `.domain()` (data range) and `.range()` (pixel range); `.nice()`.
- **Axes** (`axisBottom(scale)`), **shapes** (`line`, `area`, `arc`, `pie`), **transitions** (`.transition().duration(500)`), zoom/brush behaviors, `d3-hierarchy` (trees, treemaps), `d3-force` (network graphs).
- **D3 with React:** both want to own the DOM. Common approaches:
  1. React renders the SVG elements; D3 provides math only (scales, shapes, layouts). Declarative, testable; the preferred default.
  2. D3 owns a container via a `ref` inside `useEffect` (for complex transitions, zoom, force layouts); React doesn't touch its children.
- **SVG vs Canvas:** SVG is easy (DOM events, CSS, accessibility) but slows beyond a few thousand elements; Canvas (or WebGL) handles tens of thousands of points; hybrid = Canvas for marks, SVG for axes.
- Accessibility for charts: titles/descriptions (`<title>`, `aria-label`), data tables as alternatives, not color alone.
- For dashboards, many teams use higher-level libraries (Recharts, Vega-Lite, ECharts, Observable Plot) and drop to D3 for custom visuals.
