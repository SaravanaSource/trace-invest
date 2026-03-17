from pathlib import Path

# Canonical data root for the repository. By default this resolves to
# <repo>/trace-invest/src/data so all modules should use `data_path(...)`
# to locate runtime artifacts in a single canonical location.
# PACKAGE_SRC points to the top-level `src/` directory so DATA_ROOT becomes `src/data`
PACKAGE_SRC = Path(__file__).resolve().parents[2]
DATA_ROOT = PACKAGE_SRC / "data"


def data_path(*parts: str) -> Path:
	"""Return a Path under the canonical `src/data/` root.

	Example: `data_path('backtests', 'foo.json')` -> <repo>/trace-invest/src/data/backtests/foo.json
	"""
	return DATA_ROOT.joinpath(*parts)


def ensure_data_dirs(*paths: str) -> None:
	"""Create the data root and any requested subdirectories.
	"""
	DATA_ROOT.mkdir(parents=True, exist_ok=True)
	for p in paths:
		(DATA_ROOT / p).mkdir(parents=True, exist_ok=True)

