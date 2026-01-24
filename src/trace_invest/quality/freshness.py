from datetime import datetime

def freshness_score(latest_period: str) -> dict:
    """
    latest_period: ISO date string (e.g. '2024-03-31')
    """
    latest = datetime.fromisoformat(latest_period)
    age_days = (datetime.utcnow() - latest).days

    if age_days <= 180:
        label = "GOOD"
    elif age_days <= 365:
        label = "STALE"
    else:
        label = "OLD"

    return {
        "age_days": age_days,
        "freshness": label,
    }

