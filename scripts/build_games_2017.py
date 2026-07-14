import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games individual events -- 2017. Each verified against its official
# games.crossfit.com/workouts/games/2017/<n> page, cross-referenced via
# independent sources for events whose primary page 404'd.
#
# SKIPPED (per the Games scoping decision in ROADMAP.md):
# - Event 2 "Cyclocross" -- a pure bike time-trial race with no fixed
#   movement/rep prescription.
# - Event 4 "Sprint O-Course" -- a 3-round bracketed heat race (heats of 5,
#   progressive elimination), not a fixed single prescription.
def src(year, n):
    return (f"games.crossfit.com/workouts/games/{year}/{n} "
            f"(official CrossFit Games event), retrieved {TODAY}")

def w(id, name, fmt, slug, movements=None, segments=None, format_meta=None, tags=None, notes=None):
    entry = {
        "id": id, "name": name, "category": "games", "format": fmt,
        "format_meta": format_meta or {},
        "movements": movements or [],
        "partition": None, "scaling": None, "origin": None,
        "tags": tags or [], "description": DESCRIPTIONS.get(id), "source_notes": notes or src(*slug),
        "schema_version": VER, "last_updated": TODAY,
    }
    if segments is not None:
        entry["segments"] = segments
    with open(os.path.join(OUT, f"{id}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(entry, f, indent=2)
        f.write("\n")

BB = lambda m, f: {"rx_male": m, "rx_female": f}
CAP = lambda n: {"time_cap_minutes": n, "scoring": "time"}

w("games-17-run-swim-run", "Run Swim Run", "for_time", (2017, 1),
  [{"exercise": "run", "distance_m": 2414, "notes": "1.5 miles"},
   {"exercise": "swim", "distance_m": 500},
   {"exercise": "run", "distance_m": 2414, "notes": "1.5 miles"}],
  format_meta=CAP(60), tags=["games", "2017", "running", "swim", "open-water", "endurance"])

w("games-17-amanda-45", "Amanda .45", "for_time", (2017, 3),
  [{"exercise": "muscle-up", "reps": [13, 11, 9, 7, 5]},
   {"exercise": "squat-snatch", "reps": [13, 11, 9, 7, 5], "load": BB("135lb", "95lb")}],
  format_meta=CAP(13), tags=["games", "2017", "barbell", "gymnastics", "ladder"],
  notes=src(2017, 3) + "; time cap 13 minutes (men) / 15 minutes (women)")

w("games-17-1rm-snatch", "1RM Snatch", "max_load", (2017, 5),
  [{"exercise": "snatch", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight; 2 attempts, plus 2 more for the top 10"}],
  format_meta={"scoring": "load"}, tags=["games", "2017", "barbell", "max-load"])

w("games-17-triple-g-chipper", "Triple-G Chipper", "for_time", (2017, 6),
  [{"exercise": "pull-up", "reps": 100},
   {"exercise": "ghd-sit-up", "reps": 80},
   {"exercise": "pistol", "reps": 60, "notes": "alternating legs"},
   {"exercise": "row", "reps": 40, "notes": "calories"},
   {"exercise": "dumbbell-push-press", "reps": 20, "load": BB("100lb", "70lb")}],
  format_meta=CAP(15), tags=["games", "2017", "gymnastics", "rowing", "dumbbell"])

w("games-17-assault-banger", "Assault Banger", "for_time", (2017, 7),
  [{"exercise": "assault-bike", "reps": 40, "notes": "calories (women use 30)"},
   {"exercise": "sledgehammer-strike", "distance_m": 6, "notes": "20 ft \"banger\" track"}],
  format_meta=CAP(6), tags=["games", "2017", "venue-equipment"])

w("games-17-strongmans-fear", "Strongman's Fear", "for_time", (2017, 8),
  [{"exercise": "yoke-carry", "distance_m": 18, "load": BB("500lb", "340lb"), "notes": "60 ft"},
   {"exercise": "handstand-walk", "distance_m": 18, "notes": "60 ft"},
   {"exercise": "log-carry", "distance_m": 18, "load": BB("200lb", "120lb"), "notes": "60 ft; farmers-style, two logs"},
   {"exercise": "handstand-walk", "distance_m": 18, "notes": "60 ft"},
   {"exercise": "sled-pull", "distance_m": 18, "load": BB("400lb", "310lb"), "notes": "60 ft, sled drag"},
   {"exercise": "yoke-carry", "distance_m": 18, "load": BB("500lb", "340lb"), "notes": "60 ft"},
   {"exercise": "handstand-walk", "distance_m": 18, "notes": "60 ft"},
   {"exercise": "log-carry", "distance_m": 18, "load": BB("200lb", "120lb"), "notes": "60 ft; farmers-style, two logs"},
   {"exercise": "handstand-walk", "distance_m": 18, "notes": "60 ft"},
   {"exercise": "sled-pull", "distance_m": 18, "load": BB("400lb", "310lb"), "notes": "60 ft, sled drag"}],
  format_meta=CAP(10), tags=["games", "2017", "venue-equipment", "gymnastics"],
  notes=src(2017, 8) + "; movements may be completed in any order; each retrieval trip includes a handstand-walk section")

w("games-17-muscle-up-clean-ladder", "Muscle-Up Clean Ladder", "interval", (2017, 9),
  [{"exercise": "bar-muscle-up", "reps": 4},
   {"exercise": "clean", "reps": 2, "load": BB("225lb", "145lb")}],
  format_meta={"rounds": 8, "time_cap_minutes": 11, "scoring": "time"},
  tags=["games", "2017", "barbell", "gymnastics", "ladder"],
  notes=src(2017, 9) + "; clean load increases each round: 225-245-265-285-305-320-335-350 lb (men), 145-160-175-190-205-215-225-235 lb (women)")

w("games-17-heavy-17-5", "Heavy 17.5", "interval", (2017, 10),
  [{"exercise": "thruster", "reps": 9, "load": BB("135lb", "95lb")},
   {"exercise": "double-under", "reps": 35}],
  format_meta={"rounds": 10, "time_cap_minutes": 12, "scoring": "time"},
  tags=["games", "2017", "barbell", "jump-rope"],
  notes=src(2017, 10) + "; a heavier-loaded variant of Open workout 17.5")

w("games-17-madison-triplet", "Madison Triplet", "interval", (2017, 11),
  [{"exercise": "run", "distance_m": 450},
   {"exercise": "burpee", "reps": 7, "load": BB("100lb", "70lb"), "notes": "clean a sandbag over a hay-bale wall as part of each burpee"}],
  format_meta={"rounds": 5, "time_cap_minutes": 20, "scoring": "time"},
  tags=["games", "2017", "venue-equipment", "running"])

w("games-17-2223-intervals", "2223 Intervals", "interval", (2017, 12),
  [{"exercise": "rope-climb", "reps": 2},
   {"exercise": "ski-erg", "reps": 10, "notes": "calories (women use 7)"},
   {"exercise": "overhead-squat", "reps": "max", "load": BB("155lb", "105lb"), "notes": "max reps in time remaining"}],
  format_meta={"rounds": 4, "work_seconds": 120, "rest_seconds": 60, "time_cap_minutes": 12, "scoring": "reps"},
  tags=["games", "2017", "venue-equipment", "barbell", "gymnastics"],
  notes=src(2017, 12) + "; the first 3 rounds are 2 minutes each, the 4th round extends to 3 minutes; 1 minute of rest after each round; scored by cumulative overhead squat reps across all rounds")

w("games-17-fibonacci-final", "Fibonacci Final", "for_time", (2017, 13),
  [{"exercise": "parallette-handstand-push-up", "reps": [5, 8, 13]},
   {"exercise": "kettlebell-deadlift", "reps": [5, 8, 13], "load": BB("203lb", "124lb")},
   {"exercise": "kettlebell-overhead-lunge", "distance_m": 27, "load": BB("53lb", "35lb"), "notes": "89 ft, 2 kettlebells overhead, finishing sequence"}],
  tags=["games", "2017", "kettlebell", "gymnastics"],
  notes=src(2017, 13) + "; essentially the same event as 2018's Fibonacci, reused with the same rep scheme and loads; one secondary source suggested a different women's rep breakdown, but this could not be corroborated and is not used here, flagged per CONTRIBUTING")

print(f"Wrote 2017 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
