# Contributing

By submitting a pull request, you agree your contribution to `/data` is licensed under CC BY 4.0 and your contribution to code is licensed under MIT, consistent with this repo's [LICENSE-DATA](./LICENSE-DATA) and [LICENSE-CODE](./LICENSE-CODE).

## Adding or structuring a WOD

1. Check `schema/wod.schema.json` for the required shape.
2. If it's a row in `data/staging/heroes_raw.csv`, structure it into `data/heroes/{id}.json`, matching the pattern of existing entries in that folder, then remove the row from the CSV.
3. If it's a new entry entirely, add it to the right folder under `data/` with a unique `id` (lowercase, hyphenated).
4. Always fill `source_notes` — a URL or citation for where you verified the movements/reps/scoring. Entries without this will be asked for it before merge.
5. Don't copy descriptive text, hero bios, or narrative content from any other site verbatim — write your own from the facts, or omit the `origin.summary` field.
6. Run `python3 scripts/validate.py` to check your entry against the schema (also verifies `source_notes` is present, `id` matches the filename, and ids are unique). Requires `pip install jsonschema`.
7. Run `python3 scripts/build_index.py` to regenerate the index and your entry's `.md` twin.

CI runs both of these on every PR (`.github/workflows/validate.yml`) — a PR that fails schema validation won't be merged, so running them locally first saves a round-trip.

## Format reference

See the `format` enum in `schema/wod.schema.json`: `for_time`, `amrap`, `emom`, `tabata`, `death_by`, `max_effort`, `interval`, `complex`, `max_load`. If a WOD doesn't fit cleanly, open an issue before adding a new format — we'd rather extend the schema deliberately than have inconsistent one-off shapes.

## Disputed or uncertain entries

If sources disagree on reps/load/scoring for a WOD, don't guess — either skip it or note the discrepancy explicitly in `source_notes` (e.g. `"disputed load — CrossFit.com says X, WODwell says Y, verify before merge"`). A flagged gap is more useful than a silently wrong entry.
