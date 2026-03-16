TRACE PLATFORM AUDIT
====================

Date: 2026-03-16

Purpose
-------
This document inventories the TRACE MARKETS repository, highlights missing components and temporary placeholders, and calls out inconsistencies to address during production hardening.

1) Existing modules (high level)
--------------------------------
- Core pipeline & snapshot: `tools/build_snapshot.py`, `src/trace_invest/pipeline/snapshot_builder.py` — deterministic snapshot generation.
- Data ingestion: `src/trace_invest/data_ingestion/` — stubs and `validator.py`.
- Governance / Analyzers: `src/trace_invest/` includes governance, stability, valuation, fraud analyzers used by snapshot pipeline.
- Research & factors: `src/trace_invest/research/factor_library/` and research assistant scaffolding.
- Backtesting engine (real): `src/trace_invest/research/backtesting_engine/backtest.py` (exists but not fully wired in Alpha pipeline).
- Alpha Factory (Phase-4): `src/trace_invest/alpha_factory/` (signal_lab, strategy_generator, strategy_ranking, strategy_monitor) — deterministic signal discovery and strategy composition implemented.
- Alpha API endpoints: `backend/app/api/alpha.py` — serves `/alpha/*` endpoints.
- Phase-5 scaffolding: `src/trace_invest/api/auth.py`, `platform/user_profiles.py`, `api/portfolio.py`, `market_connectors/yahoo_stub.py`, `insight_engine/`, `notification_engine/`, `monitoring/` — lightweight stubs.
- Frontend: `frontend/` — Next.js App Router with Alpha Lab pages at `frontend/app/alpha-lab/*`.
- Tools & orchestration: `tools/run_alpha_factory.py`, `tools/run_phase3.py`, `tools/run_phase2_pipeline.py`.
- Tests: `tests/` contains `test_phase3.py`, `test_alpha_factory.py`, `test_phase5.py` and other unit tests.

2) Missing or incomplete production components
---------------------------------------------
- Database persistence: no PostgreSQL/Postgres models or migrations; users and portfolios stored in file-based stubs.
- Background processing: No Redis/Celery worker; long-running tasks run inline (tools/scripts).
- Containerization: Dockerfiles and `docker-compose.yml` are missing or not complete for multi-service deployment.
- Auth: auth uses file-based/HMAC token stubs; lacks secure password storage, JWT, refresh tokens, RBAC.
- Backtesting integration: Alpha pipeline uses deterministic placeholder backtests; real backtester exists but is not integrated.
- Observability: No centralized logging/metrics (Prometheus/Grafana), no error reporting (Sentry) configured.
- Data versioning & lineage: no DVC/git-LFS, no dataset provenance tracking.
- Tests: E2E and integration tests for full Alpha pipeline and multi-user flows are absent.

3) Temporary placeholders and risky shortcuts
-------------------------------------------
- Deterministic placeholder backtests: `src/data/backtests/*.json` are synthetic/hash-based outputs.
- Demo/demo-data duplication: demo history and artifacts exist in both `data/` and `src/data/`.
- File-backed users/profiles: `data/users/` or `src/...` file-based storage (not transactional).
- Frontend served via `next start` in production but lacks Docker deployment orchestration.

4) Inconsistent data paths (critical)
------------------------------------
- The project currently writes artifacts to both `data/` (repo root) and `src/data/` (inside package). This causes:
  - Backend endpoints reading from different locations than frontend pages.
  - Confusion when running tools (some tools write to `src/data/`, market connector writes `data/market_prices.json`).
  - Partial commits where artifacts live in inconsistent locations.

Recommendation: select a single canonical data root and standardize access via a configuration object.
Suggested canonical path: `src/data/` (keeps artifacts versionable inside package workspace and makes imports simpler).

5) Backend / Frontend mismatches
--------------------------------
- API surface: Alpha endpoints exist under `backend/app/api/alpha.py` but some frontend pages expect endpoints at specific ports; CORS and host/port assumptions must be consolidated.
- Data root mismatch: frontend pages fetch artifacts produced under `src/data/` while some tools write to `data/`; this results in stale UI or missing artifacts.

6) Security and operational gaps
--------------------------------
- No secrets management; credentials may be stored in `.env.example` only. Need to add `.env` handling and vault/provider integration.
- No rate limiting / API protections on public endpoints.
- No TLS, no containerized runtime with environment-based secrets injection.

7) Proposed minimal productionization roadmap (prioritized)
---------------------------------------------------------
Phase A — Stabilize data & pipeline (critical, low effort)
  1. Consolidate data root to `src/data/` and update all modules/tools to use it via a central `src/trace_invest/config.py`.
  2. Wire real backtester into `tools/run_alpha_factory.py` so backtests produce real CAGR/Sharpe/drawdown/volatility.
  3. Add deterministic integration tests for the Alpha pipeline.

Phase B — Platform persistence & background jobs
  4. Add PostgreSQL + SQLAlchemy models (users, portfolios, watchlists, alerts, strategy_results).
  5. Add Alembic migrations.
  6. Add Redis + Celery for background tasks and schedule workers for ingestion and Alpha runs.

Phase C — Deployment & observability
  7. Add Dockerfiles for backend/frontend and `docker-compose.yml` including `postgres`, `redis`, `worker`.
  8. Add Prometheus metrics + Grafana dashboard and Sentry for error tracking.

Phase D — Features & hardening
  9. Replace auth stubs with JWT/secure password storage and role-based access.
 10. Implement portfolio tracking, analytics, and persist strategy results to DB.
 11. Expand frontend (portfolio, insights, alerts) and admin system-health pages.

8) Next immediate actions I will execute (with your confirmation)
----------------------------------------------------------------
- Create a central configuration module `src/trace_invest/config.py` and consolidate all read/write to `src/data/` (Step 2).
- Integrate the real backtester into `tools/run_alpha_factory.py` and run the pipeline to generate real backtests (Step 3).
- Create `TRACE_PLATFORM_AUDIT.md` (this file) and commit it.

If you confirm, I will start with data path consolidation (Step 2) next — this is the highest-impact change and required for everything else.

---
Generated by: TRACE Platform hardening agent
