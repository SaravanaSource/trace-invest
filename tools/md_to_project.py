import os
import re

# ========= CONFIG =========

SOURCE_MD = "TRACE_CODEBASE.md"
OUTPUT_ROOT = "."

# ==========================

FILE_BLOCK_PATTERN = re.compile(
    r"### FILE: (.*?)\n```[a-zA-Z0-9]*\n([\s\S]*?)\n```",
    re.MULTILINE
)

def main():
    if not os.path.exists(SOURCE_MD):
        print(f"ERROR: {SOURCE_MD} not found")
        return

    with open(SOURCE_MD, "r", encoding="utf-8") as f:
        content = f.read()

    matches = FILE_BLOCK_PATTERN.findall(content)

    if not matches:
        print("No file blocks found.")
        return

    written = 0

    for rel_path, body in matches:
        rel_path = rel_path.strip()
        full_path = os.path.join(OUTPUT_ROOT, rel_path)

        folder = os.path.dirname(full_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(body)

        written += 1

    print(f"Rebuilt {written} files from {SOURCE_MD}")

if __name__ == "__main__":
    main()

