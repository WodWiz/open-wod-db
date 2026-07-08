#!/usr/bin/env python3
"""Validate every structured WOD entry under /data against the schema.

Checks, per entry:
  - conforms to schema/wod.schema.json (JSON Schema draft-07)
  - source_notes is present and non-empty (the defensibility record)
  - id matches the filename stem (keeps ids and files in sync)
  - id is unique across the whole dataset

Run locally before opening a PR:  python3 scripts/validate.py
Exits non-zero (and prints every problem it found) if anything fails.
"""
import glob
import json
import os
import sys

try:
    from jsonschema import Draft7Validator
except ImportError:
    sys.exit("Missing dependency: pip install jsonschema")

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data")
SCHEMA_PATH = os.path.join(ROOT, "schema", "wod.schema.json")


def entry_paths():
    # data/<category>/<id>.json — excludes data/index.json and data/staging/*
    for path in sorted(glob.glob(os.path.join(DATA, "*", "*.json"))):
        if os.path.normpath(os.path.dirname(path)).endswith(os.sep + "staging"):
            continue
        yield path


def main():
    with open(SCHEMA_PATH) as f:
        validator = Draft7Validator(json.load(f))

    errors = []
    seen_ids = {}
    count = 0

    for path in entry_paths():
        rel = os.path.relpath(path, ROOT)
        try:
            with open(path, encoding="utf-8") as f:
                wod = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: invalid JSON — {e}")
            continue

        count += 1

        for err in sorted(validator.iter_errors(wod), key=lambda e: e.path):
            loc = "/".join(str(p) for p in err.path) or "(root)"
            errors.append(f"{rel}: schema error at {loc} — {err.message}")

        if not str(wod.get("source_notes", "")).strip():
            errors.append(f"{rel}: source_notes is missing or empty — required")

        stem = os.path.splitext(os.path.basename(path))[0]
        wod_id = wod.get("id")
        if wod_id != stem:
            errors.append(f"{rel}: id '{wod_id}' does not match filename stem '{stem}'")

        if wod_id in seen_ids:
            errors.append(f"{rel}: duplicate id '{wod_id}' (also in {seen_ids[wod_id]})")
        elif wod_id is not None:
            seen_ids[wod_id] = rel

    if errors:
        print(f"Validation FAILED - {len(errors)} problem(s) across {count} entries:\n")
        for e in errors:
            print(f"  [x] {e}")
        sys.exit(1)

    print(f"Validation passed - {count} structured WODs conform to the schema.")


if __name__ == "__main__":
    main()
