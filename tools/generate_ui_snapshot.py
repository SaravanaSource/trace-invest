import requests
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools" / "ui_snapshot.html"

def fetch(path):
    url = f"http://localhost:8000/research/{path}"
    try:
        r = requests.get(url, timeout=5)
        return r.status_code, r.json()
    except Exception as e:
        return 500, {"error": str(e)}

def main():
    parts = []
    parts.append("<html><head><meta charset=\"utf-8\"><title>TRACE Research Snapshot</title></head><body>")
    parts.append("<h1>TRACE Research Snapshot</h1>")

    for p in ("strategies", "backtests", "performance", "factors"):
        status, data = fetch(p)
        parts.append(f"<h2>{p} (status {status})</h2>")
        parts.append('<pre style="white-space:pre-wrap; background:#f6f8fa; padding:10px; border:1px solid #ddd">')
        parts.append(json.dumps(data, indent=2))
        parts.append('</pre>')

    parts.append("</body></html>")

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print("Wrote snapshot to:", OUT)

if __name__ == '__main__':
    main()
