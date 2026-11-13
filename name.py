#!/usr/bin/env python3
from pathlib import Path

# ====== CONFIG ======
MODE = "remove"              # "add" -> adds TEXT at the end | "remove" -> removes TEXT from anywhere in the name
TEXT = "Mug_Mockup_"        # text to add or remove
BEFORE_EXTENSION = True      # True: change the name part only | False: work on the full name including extension
INCLUDE_FOLDERS = False      # also rename folders inside this folder
REMOVE_ALL_MATCHES = True    # True: remove every occurrence | False: remove only the first one
# ====================

script_path = Path(__file__).resolve()
target_dir = script_path.parent      # always the folder this script is in, no matter where you run it from

for item in sorted(target_dir.iterdir()):
    if item.resolve() == script_path:
        continue                     # never rename the script itself
    if item.is_dir() and not INCLUDE_FOLDERS:
        continue

    if item.is_dir() or not BEFORE_EXTENSION:
        base, ext = item.name, ""
    else:
        base, ext = item.stem, item.suffix

    if MODE == "add":
        new_name = base + TEXT + ext
    else:
        if TEXT not in base:
            print(f"SKIPPED ('{TEXT}' not found): {item.name}")
            continue
        count = -1 if REMOVE_ALL_MATCHES else 1
        new_base = base.replace(TEXT, "", count)
        if not new_base:
            print(f"SKIPPED (name would become empty): {item.name}")
            continue
        new_name = new_base + ext

    new_path = item.with_name(new_name)
    if new_path.exists():
        print(f"SKIPPED (already exists): {new_name}")
        continue

    item.rename(new_path)
    print(f"{item.name}  ->  {new_name}")

print("Done.")
