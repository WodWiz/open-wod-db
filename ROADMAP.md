# Roadmap / Follow-ups

Known, deliberate follow-up work for this dataset. Items here are tracked but
not yet done — contributions welcome (see [CONTRIBUTING.md](./CONTRIBUTING.md)).

## Schema: add an optional `weight_vest` field

Several Hero WODs prescribe a weight vest (or note an optional one). Right now
that instruction lives only in `source_notes` plus a `weight-vest` /
`weight-vest-optional` tag, so it isn't structurally queryable or renderable.

Entries affected so far include: Andy, René, Sisson, Taylor, Gunny (50 lb),
Luce, Maxton, Severin (prescribed); Riley, Smykowski, Daniel Ray, McCluskey
(optional).

**Proposed shape** (discuss in an issue before implementing, per CONTRIBUTING):

```jsonc
"weight_vest": {              // null when no vest is prescribed
  "rx_male": "20lb",
  "rx_female": "14lb",
  "required": true            // false for "if you've got one, wear it"
}
```

This is an additive, backward-compatible change to `schema/wod.schema.json`.

## Movement library

`data/movements.json` (built by `scripts/build_movements.py`) is a curated library
of CrossFit movements — both those a benchmark uses and common library-only ones —
classified by functional category, each listing the `workouts` that use it.
`validate.py` enforces that every WOD `exercise` exists here. Follow-ups:

- **Original descriptions** — `description` is `null` for every movement; any text
  added must be original, never copied from a glossary.
- **Equipment refinement** — `equipment` is filled only for the loaded categories
  (barbell / dumbbell / kettlebell); the rest are left empty pending per-movement
  detail.
- **Normalize `bodyweight-clean-and-jerk`** — Lyla's clean is stored under this
  slug; the "bodyweight" load arguably belongs in a load/notes field with the
  movement as plain `clean-and-jerk`. Left as-is for now (workout data shouldn't be
  rewritten without sign-off); worth a deliberate pass later.

## Structure the remaining staged Hero WODs

`data/staging/heroes_raw.csv` still holds **69** Hero WODs that were deliberately
left unstructured because their prescriptions don't map cleanly onto the current
schema. They fall into three groups:

- **Partner / team (12):** City 100, Eva Strong, Goose, Horton, Josh-O, Kev,
  Laura, Martin, Maxim 56, McCartney, Ryan Comas, Timothy Helton.
  The schema already has a `partition` field (`you-go-i-go` / `synchro` /
  `shared-reps`); the blocker is representing per-partner vs. shared rep counts
  and team-of-3 splits. Needs a small schema convention before structuring.
- **Rest-scored / "each for time" (12):** Bradley, Emily, Hall, Hammer, Holbrook,
  Kerrie, Maloney, PK, T, The Lyon, Wood, Woehlke.
  These score each round separately and/or prescribe rest between rounds, which
  `format_meta` can partly express (`rest_between_seconds`) but the per-round
  scoring model needs a decision.
- **Multi-stage / time-window / find-a-max / "for reps" (45):** Alec, Brenton,
  Carse, Coffland, Dallas 5, Dominic J. Hall, Dragon, Drew, DVB, Estrada, FERN,
  Finseth, Foo, Gage, Gale Force, Garbo, Hammy, J.J., Josie, Leehan, Locke,
  Lorenzo, Luke, Manuel, Muller, Northrup, Nukes, Nunez, Otis, Pat, Peyton,
  Pikey, Rich, Ryan SO, Santora, Schmalls, Servais, Shawn, T.J., Tama, Tiff,
  TPT9000, Wade, Wes, Wesley.
  These chain multiple distinct sections (e.g. a buy-in, then rounds, then a
  cash-out), use escalating time windows, or score for reps/load rather than
  time. Each needs either a schema extension (chained segments) or a judgment
  call, so they're intentionally left for manual/PR structuring.

## Open and Quarterfinals — done

Full CrossFit Open history is structured: all 70 workouts, every year 2011–2026
(category `open`, ids `open-YY-N`, names `YY.N`). Individual Quarterfinals are
structured for every year they existed, 2021–2026 (no Quarterfinals were held in
2025 — that season went directly from the Open to Semifinals); category
`quarterfinal`, ids `qf-YY-N`, names `YY.QFN`, stored alongside Open under
`data/open/`. Both sourced from `games.crossfit.com`, cross-referenced against a
second independent source whenever the primary page returned only one division's
Rx loads.

## Games events — done

Category `games`, stored under `data/games/`, ids `games-YY-<slug>` using the
event's real name (Games events are named, e.g. "Lake Day", not numbered like
Open). Source: `games.crossfit.com/workouts/games/<year>/<n>`.

**Scoping decision:** unlike Girls/Heroes/Open/Quarterfinals, Games events are
competition-specific tests, not all repeatable in a standard gym — some need
Games-venue equipment (yoke, sled, echo bike) or open water/hills, and some are
pure heat-based obstacle-course races or bracket sprints with no fixed
movement/rep prescription at all. Decision: **structure every event that has a
genuine published prescription** (even if it needs uncommon equipment), tagging
what limits repeatability (`venue-equipment`, `swim`/`open-water`,
`outdoor`/`hill`, etc.) so the app can filter later. Events with **no fixed
prescription** (pure obstacle-course races, bracket/heat tournaments) are
intentionally left out rather than fabricated — same principle as the staged
Hero WODs.

**Complete: every Games year 2007–2026 is structured.** Per-year counts
(structured / total, skipped events in parentheses):
- 2026: 4/4 · 2025: 10/10 · 2024: 10/10
- 2023: 11/12 (Ride — pure lap-count bike race)
- 2022: 12/13 (Skill Speed Medley — elimination bracket)
- 2021: 14/15 (Event 8 — obstacle course, no fixed reps)
- 2020: 18/19 (Snatch Speed Triple — elimination bracket)
- 2019: 11/12 (Sprint — bracket heat race)
- 2018: 11/14 (Crit — mass-start bike race; The Battleground — obstacles not
  itemized; Clean and Jerk Speed Ladder — elimination bracket)
- 2017: 11/13 (Cyclocross — bike race; Sprint O-Course — bracket race)
- 2016: 15/15 (nothing skipped — every event had a genuine prescription)
- 2015: 10/13 (Snatch Speed Ladder — elimination bracket; Sprint Course 1/2 —
  obstacles not itemized)
- 2014: 12/13 (Clean Speed Ladder — elimination bracket)
- 2013: 11/12 (ZigZag Sprint — bracketed head-to-head obstacle race)
- 2012: 13/14 (Obstacle Course — bracketed head-to-head military obstacle race)
- 2011: 10/10 · 2010: 9/9 · 2009: 8/8 · 2008: 4/4 · 2007: 3/3 (nothing skipped)

**Skip categories, for reference:** elimination/advancement brackets (top N
advance each round), pure mass-start/lap-count races, and obstacle courses
whose individual obstacles aren't itemized in any available source. A couple
of entries (2016 The Separator, 2015 Sandbag 2015, 2017 Fibonacci Final, 2012
Rope-Sled) have a detail that couldn't be corroborated across sources — each
is flagged explicitly in its own `source_notes` per CONTRIBUTING rather than
guessed. 2010 Events 1 and 4 warrant special note: the official page initially
returned team-division content for those slots; both were corrected to the
true individual-division prescriptions after cross-referencing a second
source, and the correction is documented permanently in `games-10-amanda`'s
`source_notes`.

- **Community / affiliate-invented WODs** — intentionally grown organically via
  the PR-based contribution model rather than seeded by one contributor.
