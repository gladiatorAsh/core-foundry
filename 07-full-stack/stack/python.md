# Python (for backend and AI services)

## Language fundamentals

- Everything is an object; names bind to objects. **Mutable** (list, dict, set) vs **immutable** (int, str, tuple, frozenset). Only hashable (immutable) values can be dict keys.
- Mutable default argument bug: `def f(x, acc=[])` shares one list across calls. Use `None` and create inside.
- `is` (identity) vs `==` (equality). Small ints and some strings are interned; never rely on `is` for values.
- Comprehensions, generators (`yield`, lazy, constant memory), generator expressions, `itertools`.
- **Decorators** wrap functions (`functools.wraps` keeps metadata); **context managers** (`with`, `__enter__`/`__exit__`, or `@contextmanager`) handle setup/teardown.
- Dunder methods (`__repr__`, `__eq__`, `__hash__`, `__iter__`, `__len__`); `@dataclass` (with `frozen=True`, `slots=True`); `__slots__` to save memory.
- MRO and `super()` for multiple inheritance (C3 linearization).
- Type hints + mypy/pyright; `Protocol` for structural typing; `TypedDict`; generics (`list[int]`, `TypeVar`).

## Concurrency

| Workload | Tool |
|---|---|
| I/O-bound, many connections | `asyncio` (async/await) or threads |
| CPU-bound | `multiprocessing` / `ProcessPoolExecutor`, or native code (NumPy releases the GIL) |
| Mixed | asyncio + `asyncio.to_thread` / `run_in_executor` for blocking calls |

- The **GIL** allows one thread to run Python bytecode at a time; threads still help for I/O. Free-threaded CPython builds (PEP 703) are available but not yet the default.
- asyncio: `asyncio.gather` (parallel awaits), `asyncio.TaskGroup` (structured concurrency, 3.11+), `asyncio.Semaphore` to limit concurrency, timeouts with `asyncio.timeout()`.
- Never call blocking code (`requests`, `time.sleep`, sync DB drivers) inside `async def`. Use `httpx`/`aiohttp`, async DB drivers.

## FastAPI

- Built on Starlette (ASGI) + Pydantic. Type hints drive validation, serialization, and OpenAPI docs.
- `async def` endpoints run on the event loop; `def` endpoints run in a threadpool (fine for blocking libraries).
- Dependency injection with `Depends` (auth, DB sessions; `yield` dependencies for cleanup). Background tasks for light post-response work (use a real queue for anything important).
- Pydantic v2 models: validation, `model_config`, settings management with `pydantic-settings`.
- Deploy: Uvicorn (or Gunicorn managing Uvicorn workers), one worker per core-ish, behind a reverse proxy; health endpoints; structured logging.
- Streaming responses (`StreamingResponse`, SSE) for LLM token streaming.

## Data and AI libraries worth naming

NumPy, pandas/Polars, scikit-learn, PyTorch, Hugging Face transformers, the OpenAI / Azure OpenAI SDKs, LangChain/LlamaIndex/Semantic Kernel (and when you'd skip them), Pydantic for structured LLM outputs.

## Packaging and tooling

`venv`; `pip` + `requirements.txt` with pins, or **uv** / Poetry with lockfiles; `pyproject.toml`; ruff (lint + format); pytest (fixtures, parametrize, monkeypatch), coverage.

## Performance

Profile first (`cProfile`, `py-spy`). Use built-ins and vectorized NumPy; avoid repeated string concatenation; use sets/dicts for membership;
`functools.lru_cache`; move hot loops to native code; batch I/O.

## Questions to rehearse

1. Explain the GIL and how you'd parallelize CPU work. 2. Generators vs lists. 3. Write a decorator that retries with backoff. 4. Async vs threads in FastAPI.
5. What's wrong with a mutable default argument? 6. How do you structure a FastAPI app for testing (dependency overrides)? 7. Deep vs shallow copy.
