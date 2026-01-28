from typing import List, Dict


def generate_long_term_watchlist(decisions: List[Dict]) -> Dict:

    core = []
    candidates = []
    watch = []

    for d in decisions:
        v = d.get("validation", {})

        master = v.get("master", {})
        governance = v.get("governance", {})
        stability = v.get("stability", {})

        master_band = master.get("master_band")
        gov_band = governance.get("governance_band")
        stab_band = stability.get("stability_band")

        row = {
            "symbol": d.get("stock"),
            "master_score": master.get("master_score"),
        }

        # CORE
        if (
            master_band == "ELITE"
            and gov_band == "LOW"
            and stab_band == "STRONG"
        ):
            core.append(row)

        # CANDIDATES
        elif (
            master_band == "GOOD"
            and gov_band == "LOW"
            and stab_band in ("STRONG", "AVERAGE")
        ):
            candidates.append(row)

        # WATCH
        elif (
            master_band == "AVERAGE"
            and gov_band == "LOW"
        ):
            watch.append(row)

    return {
        "core": core,
        "candidates": candidates,
        "watch": watch,
    }

