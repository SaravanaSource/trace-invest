import os
import hashlib
from datetime import datetime, timezone

OUTPUT = "TRACE_SYSTEM_STATE.md"

ALLOWED_PATHS = [
    "configs",
    "data",
    "backend/Dockerfile",
    "frontend/Dockerfile",
    "docker-compose.yml"
]

MAX_HASH_SIZE = 2_000_000  # 2MB

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()[:16]

def file_info(path):
    size = os.path.getsize(path)
    info = f"size={size}B"
    if size <= MAX_HASH_SIZE:
        info += f" sha256={sha256(path)}"
    return info

def allowed(path):
    path = path.replace("\\", "/")
    return any(
        path == p or path.startswith(p + "/")
        for p in ALLOWED_PATHS
    )

with open(OUTPUT, "w", encoding="utf-8") as out:

    out.write("# TRACE SYSTEM STATE\n\n")
    out.write(f"generated_at: {datetime.now(timezone.utc).isoformat()}\n\n")

    for root, dirs, files in os.walk("."):
        dirs[:] = sorted(
            d for d in dirs if d not in {".git", ".next", "node_modules", "__pycache__"}
        )
        files = sorted(files)
        for name in files:
            rel = os.path.relpath(os.path.join(root, name), ".")
            rel = rel.replace("\\", "/")

            if not allowed(rel):
                continue

            try:
                info = file_info(rel)
            except:
                continue

            out.write(f"{rel} | {info}\n")

print("TRACE_SYSTEM_STATE.md generated (clean)")
