# open-wod-db

An open, structured, community-maintained database of CrossFit benchmark workouts — the Girls, the Heroes, the Open, Quarterfinals, and CrossFit Games history. No auth required, free to use.

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
| Heroes | 167 | 69 in `/data/staging/heroes_raw.csv` |
| Open | 70 (2011–2026, in progress) ✅ | — |
| Quarterfinals | 23 (2021–2026, none held in 2025) ✅ | — |
| Games | 203 (2007–2025) ✅ | — |

**496 structured WODs total**, backed by a **246-movement library** (`data/movements.json`).

See [ROADMAP.md](./ROADMAP.md) for what's left: a proposed `weight_vest` schema field, the 69 staged Heroes (partner/rest-scored/multi-stage) awaiting schema conventions, and general movement-library polish.

All entries are sourced directly from crossfit.com / games.crossfit.com — the primary source, not a secondary aggregator. See each entry's `source_notes` field. Games events that are pure elimination brackets, mass-start races, or obstacle courses with no itemized, fixed prescription are intentionally left out rather than fabricated — see ROADMAP for the full skip list.

## Structure

```
data/
  girls/*.json + *.md      fully structured, schema-validated (33 WODs)
  heroes/*.json + *.md     fully structured, schema-validated (167 WODs)
  open/*.json + *.md       Open (`open-YY-N`) + Quarterfinals (`qf-YY-N`), 2011–2026
  games/*.json + *.md      CrossFit Games individual events (`games-YY-<slug>`), 2007–2025
  staging/heroes_raw.csv   verified raw text, not yet converted to schema
  index.json               compiled bundle of all structured entries
  movements.json           movement library (dataset + common CrossFit movements)
schema/wod.schema.json     the contract every entry must satisfy
scripts/
  build_girls.py                 source script for the Girls dataset
  build_heroes_*.py              source scripts for structured Hero entries (batched)
  build_open_wave*.py            source scripts for the Open, by year-wave
  build_quarterfinals.py         source script for Quarterfinals
  build_games_<year>.py          one source script per CrossFit Games year (2007–2025)
  build_movements.py             compiles movements.json (source of truth for movements)
  build_index.py                 compiles index.json + renders .md twins from .json
  validate.py                    schema + referential-integrity validation (CI-enforced)
```

## Usage

Fetch the compiled index directly via jsdelivr (versioned by git tag once tagged):

```
https://cdn.jsdelivr.net/gh/wodwiz/open-wod-db@latest/data/index.json
```

Or clone and read `/data` directly — each WOD is one JSON file, human-browsable as its matching `.md` file.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). The fastest way to help right now: pick a row from `data/staging/heroes_raw.csv`, structure it against `schema/wod.schema.json`, and open a PR moving it into `data/heroes/`.

## Disclaimer

This is an independent, community-maintained dataset. It is **not affiliated with,
endorsed by, or sponsored by CrossFit, LLC**. "CrossFit" and "CrossFit Games" are
registered trademarks of CrossFit, LLC, used here nominatively only to accurately
identify the workouts described. Workout names and prescriptions are facts, not
claimed as anyone's intellectual property; all original structuring and
descriptions in this repository are licensed as noted above.

## Why this exists

Named CrossFit benchmarks (Fran, Murph, DT...) are common knowledge in the community, but there's no open, structured, freely-licensed dataset of them — only proprietary catalogs (WODwell) or unstructured HTML (CrossFit.com itself). This repo exists to be the free, structured, forkable version.
