# 0001. Use SQLite for companion persistence

- **Status:** Accepted
- **Date:** 2026-10-24
- **Decider:** Gui Fernandes
- **Spec references:** §3 (architecture), §9 (persistence, ingestion, API), §12 (acceptance gate 9)

## Context

The companion API owns all TrafficVision persistence: runs, event batches, crossing events, interval counts, metric samples and artifact records (spec §9). The MVP has these characteristics:

- One companion service process and one ingestion writer, receiving data from a single Jetson edge worker (online batches or imported run bundles).
- Low write volume: crossing events plus periodic metric samples from one video stream.
- The database lives on the companion's local disk. No hosted deployment, paid services or public exposure in the MVP.
- A clean setup from committed locks is an acceptance gate (§12, gate 9). Every additional service adds setup, security and backup steps.

The author's usual stack is PostgreSQL with SQLAlchemy and Alembic, so that option was evaluated explicitly rather than defaulted away.

## Decision

Use SQLite through Python's standard-library `sqlite3` module, with hand-written, numbered SQL migrations.

- **Location:** one database file on the companion's local disk, never on a network filesystem. Path comes from configuration; the file is excluded from Git.
- **Single writer:** run one Uvicorn worker; all mutations go through one coordinated write path.
- **Connection settings:** `PRAGMA foreign_keys = ON` on every connection (SQLite leaves it off by default); `PRAGMA journal_mode = WAL` (persistent once set); an explicit busy timeout (the `timeout` argument to `sqlite3.connect` or `PRAGMA busy_timeout`).
- **Migrations:** `apps/api/migrations/NNNN_description.sql`, applied in order by a small runner, each inside an explicit transaction and recorded in `schema_migrations`.
- **Idempotency in the database:** UNIQUE constraints from spec §9 (run/batch, run/track/line, aggregate keys) enforce deduplication, not only application checks.
- **Types:** media time as INTEGER milliseconds; wall-clock time as UTC ISO-8601 TEXT; UUIDs as TEXT.
- **Backups:** SQLite's online backup API (`Connection.backup`), not copying the file while the service is running.

## Alternatives considered

**PostgreSQL + SQLAlchemy + Alembic.** Familiar tooling, strong concurrency, and the natural choice for a hosted multi-user service. Not chosen for the MVP: it requires running, securing and backing up a separate database server on the companion, and its main strengths (many concurrent writers, network access) are not MVP needs.

**SQLAlchemy Core + Alembic on top of SQLite.** Keeps familiar migration tooling and would ease a later move to PostgreSQL. Deferred: it adds dependencies and abstraction while the schema is small, and writing raw SQL migrations is a deliberate learning goal for this project. It can be adopted later without changing the database engine.

## Consequences

**Positive**

- No extra service to install or run; the whole database is one file.
- Easy to inspect with the `sqlite3` CLI and easy to back up and restore.
- Fewest moving parts for the clean-install acceptance gate.

**Costs and things to watch**

- `sqlite3` is synchronous. Async FastAPI endpoints must not call it directly on the event loop. Use plain `def` endpoints (FastAPI runs them in a threadpool) or explicit thread offloading.
- A `sqlite3.Connection` is bound to the thread that created it by default (`check_same_thread=True`). Use a connection per request or a dedicated writer, not one global connection shared across threads.
- On Python 3.11, the `sqlite3` module opens transactions implicitly. The migration runner and ingestion code must control `BEGIN`/`COMMIT` explicitly (for example with `isolation_level=None`). Note that `executescript()` commits any pending transaction before it runs.
- Tests should use a temporary database file, not `:memory:`: each new connection to `:memory:` gets its own separate, empty database.
- Only one writer at a time. Acceptable for a single-stream MVP; a hard limit for multiple concurrent edge devices.
- SQLite's `ALTER TABLE` is limited. Changing constraints or column types requires the create-copy-rename table rebuild pattern inside a migration.
- Raw SQL means no ORM-level portability. Keep SQL close to standard where it costs little, so a future PostgreSQL migration stays mechanical.

## Revisit when

- More than one edge device, or any other concurrent writer, must write at the same time.
- The API needs to run on a different host from the database, or the project moves to a hosted deployment (for example GCP with Cloud SQL).
- Sustained tests show `database is locked` errors despite the single-writer design.
- Migration complexity makes Alembic's tooling worth its weight.
