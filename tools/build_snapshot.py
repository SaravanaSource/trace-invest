from __future__ import annotations

import argparse
from pathlib import Path
import sys
import os

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from trace_invest.pipeline.snapshot_builder import build_snapshot


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a deterministic Trace Invest snapshot",
    )
    parser.add_argument(
        "--date",
        help="Snapshot date in YYYY-MM-DD format",
    )

    args = parser.parse_args()
    os.chdir(ROOT)
    build_snapshot(run_date=args.date)


if __name__ == "__main__":
    main()
