from datetime import datetime, timezone

def freshness_score(years: list[str]) -> dict:
    if not years:
        return {
            "age_days": None,
            "freshness": "UNKNOWN",
        }

    parsed_years = []

    for y in years:
        try:
            # Handles "2025-03-31 00:00:00"
            dt = datetime.fromisoformat(str(y))
            parsed_years.append(dt.year)
        except Exception:
            try:
                # Handles "2025"
                parsed_years.append(int(y))
            except Exception:
                continue

    if not parsed_years:
        return {
            "age_days": None,
            "freshness": "UNKNOWN",
        }

    latest_year = max(parsed_years)
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
