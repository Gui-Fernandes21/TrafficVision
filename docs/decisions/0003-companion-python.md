# 0003. Companion Python 3.12 on native Windows

- **Status:** Accepted
- **Date:** 2026-10-25
- **Decider:** Gui Fernandes
- **Spec references:** §4 (companion environment), §13 (CI)
- **Amends:** 0002 (companion Python version only; the deployment profile is unchanged)

## Context

- Spec §4 proposes Python 3.11 for the companion as a candidate version, with the instruction to pin the exact security patch available.
- The companion computer is the Windows development machine, running Python natively rather than in WSL2.
- As of October 2026, both 3.11 and 3.12 receive security fixes only, and those releases are published as source code. The last python.org Windows installers were 3.11.9 (April 2024) and 3.12.10 (April 2025). Getting current security patches on Windows therefore needs a distribution that builds them, such as uv's managed Python builds.
- Security support ends in October 2027 for 3.11 and around October 2028 for 3.12.
- No companion code, lockfile or CI exists yet, so changing the version now costs nothing.

## Decision

- **Companion Python:** 3.12, latest security patch, installed with uv (`uv python install 3.12`).
- **Virtual environment:** `.venv` at the repository root, created with `uv venv --python 3.12 .venv` and excluded from Git.
- **Exact version:** recorded in `docs/compatibility.md` after installation, and pinned in the companion lockfile when it's created in M3.
- **Package pins:** the direct pins from spec §4 are unchanged: `fastapi==0.115.6`, `pydantic==2.10.4`, `uvicorn==0.34.0`, `httpx==0.28.1`, `pytest==8.3.4`. All declare support for Python 3.12; this is confirmed when the lockfile is resolved.
- **CI:** companion jobs run on Python 3.12, and a separate check keeps running `packages/` under Python 3.6.

## Alternatives considered

**Python 3.11 (the spec's candidate).** Works, but needs the same uv workaround on Windows and loses security support a year earlier.

**A python.org installer (3.11.9 or 3.12.10).** Simplest to install, but frozen at a release that is missing later security fixes. Rejected.

**Python 3.13.** Even longer support, but it moves further from the spec's candidate for no benefit this project needs now. Can be revisited.

**Python 3.14.** Rejected for now: the pinned Pydantic 2.10.4 was released before Python 3.14, so the pins would have to change.

## Consequences

**Positive**

- One more year of security support than 3.11.
- Current security patches on Windows.
- No code changes needed.

**Costs and things to watch**

- uv is required to set up the companion. The setup instructions must say so.
- The rules for shared code don't change: everything under `packages/` must still run under Python 3.6.9. Syntax that only exists in newer versions, such as `type` alias statements or 3.12's relaxed f-string quoting, must stay out of it.
- `datetime.utcnow()` is deprecated in 3.12. Use `datetime.now(timezone.utc)`, which also works on 3.6.
- Decision 0001's `sqlite3` notes still apply: 3.12 keeps the legacy implicit-transaction behavior by default. It also adds an `autocommit` option to `sqlite3.connect()` as another way to control transactions explicitly.
- The companion runs on Windows while CI runs on Linux. Companion code must build paths with `pathlib` rather than hard-coded separators.
- The lockfile is generated on Windows but must also install on Linux CI. Some packages, such as `pydantic-core`, ship a separate compiled wheel per platform, so check this when the lockfile is created in M3.

## Revisit when

- Python 3.12 security support approaches its end (around October 2028).
- A pinned package drops 3.12 support, or a needed upgrade requires a newer Python.
