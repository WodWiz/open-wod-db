#!/usr/bin/env python3
"""Keep each entry's `description` in step with wod_descriptions.DESCRIPTIONS.

The build_*.py scripts set `description` once, when they create an entry. After
that the text lives in two places, the JSON file and DESCRIPTIONS, and this
script makes the file follow the dictionary. It touches only `description` and
`last_updated`, and only where the two differ, so re-running it is harmless.

Run scripts/validate.py and scripts/build_index.py after.
"""
import glob
import json
import os

from wod_descriptions import DESCRIPTIONS

ROOT = os.path.join(os.path.dirname(__file__), "..")
TODAY = "2026-10-16"


def main():
    changed = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "*", "*.json"))):
        if os.sep + "staging" + os.sep in path:
            continue
        with open(path, encoding="utf-8") as f:
            wod = json.load(f)
        wanted = DESCRIPTIONS.get(wod.get("id"))
        if wanted is None or wod.get("description") == wanted:
            continue
        wod["description"] = wanted
        wod["last_updated"] = TODAY
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(wod, f, indent=2, ensure_ascii=False)
            f.write("\n")
        changed += 1
    print(f"descriptions synced: {changed}")


if __name__ == "__main__":
    main()
