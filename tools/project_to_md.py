import os

OUTPUT = "TRACE_CODEBASE.md"

# Exact folders that contain REAL SOURCE CODE
ALLOWED_PATH_PREFIXES = [
    "backend",
    "configs",
    "docs",
    "tools",
    "scripts",
    "frontend/app",
    "frontend/components",
    "frontend/lib"
]

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
    return any(path.startswith(p) for p in ALLOWED_PATH_PREFIXES)

def allowed_file(filename):
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

files = []

for root, dirs, filenames in os.walk("."):
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
