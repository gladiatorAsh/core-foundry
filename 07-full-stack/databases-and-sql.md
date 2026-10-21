# Databases and SQL

## SQL you should write without hesitation

```sql
-- Joins: INNER (matches only), LEFT (all left rows + matches or NULLs), FULL OUTER, CROSS, self-join
SELECT c.name, COUNT(o.id) AS orders, COALESCE(SUM(o.total), 0) AS revenue
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id AND o.created_at >= DATE '2026-01-01'
GROUP BY c.id, c.name
HAVING COUNT(o.id) >= 3
ORDER BY revenue DESC
LIMIT 10;

-- Window functions: top 3 orders per customer
SELECT *
FROM (
  SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY total DESC) AS rn
  FROM orders o
) ranked
WHERE rn <= 3;

-- Running total and day-over-day change
SELECT day, revenue,
       SUM(revenue) OVER (ORDER BY day) AS running_total,
       revenue - LAG(revenue) OVER (ORDER BY day) AS change
FROM daily_revenue;

-- CTE + anti-join: customers with no orders
WITH active AS (SELECT DISTINCT customer_id FROM orders)
SELECT c.* FROM customers c
LEFT JOIN active a ON a.customer_id = c.id
WHERE a.customer_id IS NULL;
```

Know: `WHERE` filters rows before grouping, `HAVING` filters groups after. `COUNT(*)` counts rows; `COUNT(col)` skips NULLs.
`NULL = NULL` is unknown (use `IS NULL`). `ROW_NUMBER` vs `RANK` (gaps on ties) vs `DENSE_RANK` (no gaps).
`UNION` dedupes; `UNION ALL` doesn't (faster).

## Indexes

- B-tree indexes make lookups O(log n) and support range queries and ordering; they cost write speed and storage.
- **Composite index order matters:** an index on `(customer_id, created_at)` serves `WHERE customer_id = ?` and `WHERE customer_id = ? AND created_at > ?`,
  but not `WHERE created_at > ?` alone (leftmost-prefix rule). Put equality columns first, then range/sort columns.
- **Covering index** (includes all selected columns) → index-only scan, no table lookups.
- Indexes are skipped when you wrap the column in a function (`WHERE LOWER(email) = …`; use an expression index), use a leading wildcard `LIKE '%x'`, or filter on low-selectivity columns.
- Read plans with `EXPLAIN` / `EXPLAIN ANALYZE` (Postgres) or the execution plan (SQL Server): look for sequential scans on big tables, bad row estimates, nested loops over large inputs.
- Partial/filtered indexes (`WHERE deleted_at IS NULL`), GIN for JSONB/full-text, BRIN for huge append-only time data.

## Transactions and isolation

ACID: atomicity, consistency, isolation, durability.

| Isolation level | Prevents | Still allows |
|---|---|---|
| Read uncommitted | – | Dirty reads |
| **Read committed** (Postgres/SQL Server default) | Dirty reads | Non-repeatable reads, phantoms, lost updates |
| Repeatable read | + non-repeatable reads | Phantoms (in the SQL standard; Postgres' snapshot isolation prevents them but allows write skew) |
| Serializable | All anomalies | Lower throughput, retries on serialization failure |

- **Lost update** (two read-modify-writes overwrite each other): fix with `SELECT … FOR UPDATE`, atomic updates (`SET stock = stock - 1 WHERE stock > 0`), or optimistic locking (a version column).
- **Write skew** (two transactions read the same data and write different rows, breaking an invariant): serializable isolation or explicit locks.
- MVCC: readers don't block writers; old row versions are cleaned up later (Postgres VACUUM).
- Deadlocks: acquire locks in a consistent order; keep transactions short; retry.

## ORMs and the N+1 problem

Loading a list then lazily loading a relation per row = 1 + N queries. Fix with eager loading (`Include` in EF Core, `selectinload`/`joinedload` in SQLAlchemy),
batching (DataLoader in GraphQL), or a hand-written join. Watch the query log in development.

## Schema design and migrations

- Normalize to 3NF for OLTP (no duplicated facts); denormalize deliberately for read performance (with a way to keep copies in sync).
- Zero-downtime migrations use **expand → migrate → contract**: add the new column/table (nullable or with a default), dual-write,
  backfill in batches, switch reads, then drop the old one in a later deploy. Never rename or drop in the same release that stops using it.
- Soft deletes complicate unique constraints and queries; consider archival tables.

## SQL vs NoSQL (decision prompts)

Relational when you need joins, transactions, ad-hoc queries, and integrity constraints. Choose NoSQL (key-value/document/wide-column)
for massive scale with known access patterns, flexible schemas, or global distribution. Many teams use **Postgres for almost everything**
(JSONB, full-text, pgvector) until a specific need forces specialization.

## Connection management

Connection pools (PgBouncer, built-in pools in .NET/SQLAlchemy); size pools to the database's limits, not the number of app instances × an arbitrary number;
serverless functions need a proxy or pooler to avoid exhausting connections.
