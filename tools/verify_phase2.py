"""Simple verification harness for Phase-2 outputs.

Runs quick checks and writes PHASE2_VERIFICATION_REPORT.md
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "PHASE2_VERIFICATION_REPORT.md"


def check_file(p: Path):
    return p.exists() and p.stat().st_size > 0


def main():
    issues = []
    checks = {
        "latest_snapshot": ROOT / "data" / "snapshots",
        "history_dir": ROOT / "data" / "history",
        "signals": ROOT / "data" / "signals" / "top_opportunities.json",
        "portfolio": ROOT / "data" / "portfolio" / "portfolio.json",
        "alerts": ROOT / "data" / "alerts" / "alerts.json",
    }

    for name, p in checks.items():
        ok = True
        if p.is_dir():
            ok = any(p.iterdir())
        else:
            ok = check_file(p)
        if not ok:
            issues.append(f"missing-or-empty: {name} -> {p}")

    out = ["# Phase2 Verification Report", ""]
    if not issues:
        out.append("All Phase-2 artifacts present.")
    else:
        out.append("Issues found:")
        for it in issues:
            out.append(f"- {it}")

    REPORT.write_text("\n".join(out), encoding="utf-8")
    print(REPORT)


if __name__ == '__main__':
    main()
