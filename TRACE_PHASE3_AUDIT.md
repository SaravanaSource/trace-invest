# TRACE Phase-3 Audit

Date: 2026-03-16

Summary: inventory and findings for Phase-3 (research layer)

Implemented components
- `src/trace_invest/research/__init__.py` — research package present
- `src/trace_invest/research/factor_library/` — contains value, quality, growth, momentum, volatility modules (but with inconsistencies)
- `src/trace_invest/research/strategy_engine/strategy_runner.py` — strategy runner(s) present; can run simple rules and persist results to `data/strategies`
- `src/trace_invest/research/backtesting_engine/backtest.py` — backtest implementations present; writes to `data/backtests`
- `src/trace_invest/research/performance_engine/` — performance helpers and report writer to `data/performance_reports`
- `src/trace_invest/research/research_assistant/assistant.py` — basic research assistant functions
- `tools/run_phase3.py` — orchestration script exists (contains duplicate concatenated versions)

Incomplete / problematic components
- Factor modules: duplicate function definitions and inconsistent return schema. Current outputs use `factor_name`/`factor_value` but Phase-3 requires keys: `symbol`, `factor_name`, `value`, `metrics_used`, `explanation`.
- `value_factor.py`, `growth_factor.py`, `momentum_factor.py`, `volatility_factor.py` each include two differing implementations in the same file — risk of shadowing and unpredictable behavior.
- `tools/run_phase3.py` contains multiple concatenated implementations; needs cleanup and deterministic orchestration of: compute factors, evaluate strategies (from definitions), backtest, performance reports.
- API: No research FastAPI endpoints implemented. Only `api/history.py` exists.
- Frontend: No Next.js research pages (`/strategy-lab`, `/backtests`, `/performance`, `/factor-explorer`) present.
- Tests: `tests/test_phase3.py` exists but minimal; lacks deterministic validation for factors, strategy execution, backtests, and performance metrics.
- Research assistant: basic features present but limited query support.

Missing components to implement or improve
- Normalize factor library to required schema and remove duplicate definitions.
- Add consistent factor-registration mechanism (discoverable list of factor functions).
- Ensure `strategy_engine` provides a single, well-defined API to run strategy definitions (load from `data/strategy_definitions` and write to `data/strategies`).
- Standardize backtest API and add required metrics (CAGR, Sharpe, Max drawdown, Volatility, Benchmark comparison).
- Improve performance engine to compute Sortino and Alpha vs benchmark and write detailed reports to `data/performance_reports`.
- Implement `tools/verify_phase3.py` that runs checks and emits `PHASE3_VERIFICATION_REPORT.md`.
- Add FastAPI endpoints under `/research/*` that read precomputed artifacts and do not recompute analysis.
- Add minimal Next.js research pages that read the above API and visualize results.
- Expand `tests/test_phase3.py` to validate deterministic outputs for factors, strategy runner, backtest and performance functions.

Architecture inconsistencies and risks
- Multiple duplicate function definitions inside single module files (likely due to iterative development). This creates ambiguity about which implementation is used at import time.
- Non-uniform return payloads across factor functions. Consumers of factors expect a consistent schema.
- Orchestration script duplicates may cause unexpected behavior if run as-is.
- Lack of API endpoints for research artifacts prevents the frontend from being built in a decoupled, read-only manner.

Recommendations (next steps)
1. Normalize factor outputs to the canonical schema and remove duplicate code. Add unit tests.
2. Clean `tools/run_phase3.py` to a single deterministic pipeline implementing Steps 2–6.
3. Implement research API endpoints that only read artifacts.
4. Add minimal frontend pages in `frontend/app/` that call the API and render simple tables/plots.
5. Add `tools/verify_phase3.py` and a final verification report file.

This audit is the baseline; I will now start by normalizing the factor library to the canonical schema and adding a factor registry.
