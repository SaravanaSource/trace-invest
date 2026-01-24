from datetime import datetime, timezone

def freshness_score(years: list[str]) -> dict:
    if not years:
        return {
            "age_days": None,
            "freshness": "UNKNOWN",
        }

    latest_year = max(int(y) for y in years)
    latest_date = datetime(latest_year, 3, 31, tzinfo=timezone.utc)

    age_days = (datetime.now(timezone.utc) - latest_date).days

    if age_days <= 180:
        label = "GOOD"
    elif age_days <= 365:
        label = "STALE"
    else:
        label = "OLD"

    return {
        "latest_year": latest_year,
        "age_days": age_days,
        "freshness": label,
    }
