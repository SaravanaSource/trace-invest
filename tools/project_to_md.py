import os

OUTPUT = "TRACE_CODEBASE.md"

# Exact folders that contain real source code
ALLOWED_PATH_PREFIXES = [
    "backend",
    "configs",
    "docs",
    "tools",
    "scripts",
    "src/trace_invest",
    "frontend/app",
    "frontend/components",
    "frontend/lib",
]

ALLOWED_EXACT_PATHS = {
    "README.md",
    "docker-compose.yml",
    "pyproject.toml",
    "requirements.txt",
    "frontend/package.json",
    "frontend/package-lock.json",
    "frontend/next.config.ts",
    "frontend/next.config.js",
    "frontend/tsconfig.json",
    "frontend/tailwind.config.js",
    "frontend/tailwind.config.mjs",
    "frontend/eslint.config.mjs",
    "backend/Dockerfile",
    "frontend/Dockerfile",
}

# Allowed file types
ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".html",
    ".css",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".sh",
    ".bat"
}

def allowed_path(path):
    path = path.replace("\\", "/")
    return path in ALLOWED_EXACT_PATHS or any(
        path.startswith(prefix) for prefix in ALLOWED_PATH_PREFIXES
    )

def allowed_file(filename):
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

files = []

for root, dirs, filenames in os.walk("."):
    dirs[:] = sorted(
        d for d in dirs if d not in {".git", ".next", "node_modules", "__pycache__"}
    )
    for name in filenames:
        rel = os.path.relpath(os.path.join(root, name), ".")
        rel = rel.replace("\\", "/")

        if allowed_path(rel) and allowed_file(name):
            files.append(rel)

files = sorted(files)

with open(OUTPUT, "w", encoding="utf-8") as out:
    out.write("# TRACE CODEBASE SNAPSHOT\n\n")

    out.write("## PROJECT TREE\n")
    for f in files:
        out.write(f"{f}\n")

    out.write("\n---\n")

    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as src:
                data = src.read()
        except:
            continue

        ext = f.split(".")[-1]
        out.write(f"\n### FILE: {f}\n")
        out.write(f"```{ext}\n")
        out.write(data)
        out.write("\n```\n")

print(f"TRACE_CODEBASE.md generated with {len(files)} source files only")
