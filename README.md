# open-wod-db

An open, structured, community-maintained database of CrossFit benchmark workouts — the Girls, the Heroes, and (eventually) Games/Open history. No auth required, free to use.

Maintained by [WodWiz](https://github.com/wodwiz).

## License

This repository contains two independently licensed things:

- **Data** (`/data`) — [Creative Commons Attribution 4.0](./LICENSE-DATA) (CC BY 4.0). Use it commercially, remix it, redistribute it — just credit WodWiz.
- **Code** (everything else — `/schema`, `/scripts`, `/.github`) — [MIT License](./LICENSE-CODE).

The underlying workout prescriptions (movements + reps/time schemes) aren't independently copyrightable — see the note at the bottom of [LICENSE-DATA](./LICENSE-DATA). The CC BY 4.0 license covers this repo's structuring, schema, and original descriptions.

## Current status

| Set | Structured | Staged (raw, awaiting structure) |
|---|---|---|
| Girls | 33 / 33 ✅ | — |
| Heroes | 19 / 249 | 230 in `/data/staging/heroes_raw.csv` |
| Games / Open | 0 | Not started |

All entries are sourced directly from crossfit.com — the primary source, not a secondary aggregator. See each entry's `source_notes` field.

## Structure

```
data/
  girls/*.json + *.md      fully structured, schema-validated
  heroes/*.json + *.md     fully structured, schema-validated
  staging/heroes_raw.csv   verified raw text, not yet converted to schema
  index.json               compiled bundle of all structured entries
schema/wod.schema.json     the contract every entry must satisfy
scripts/
  build_girls.py           source script for the Girls dataset
  build_heroes_core.py     source script for structured Hero entries
  build_index.py           compiles index.json + renders .md twins from .json
```

## Usage

Fetch the compiled index directly via jsdelivr (versioned by git tag once tagged):

```
https://cdn.jsdelivr.net/gh/wodwiz/open-wod-db@latest/data/index.json
```

Or clone and read `/data` directly — each WOD is one JSON file, human-browsable as its matching `.md` file.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). The fastest way to help right now: pick a row from `data/staging/heroes_raw.csv`, structure it against `schema/wod.schema.json`, and open a PR moving it into `data/heroes/`.

## Why this exists

Named CrossFit benchmarks (Fran, Murph, DT...) are common knowledge in the community, but there's no open, structured, freely-licensed dataset of them — only proprietary catalogs (WODwell) or unstructured HTML (CrossFit.com itself). This repo exists to be the free, structured, forkable version.
