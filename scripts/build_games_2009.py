import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-10"

# CrossFit Games individual events -- 2009. Each verified against its official
# games.crossfit.com/workouts/games/2009/<n> page, with the individual (not
# team) division explicitly confirmed for every event this time, given the
# team/individual mix-up discovered while researching 2010. No events skipped
# this year -- all 8 have a genuine fixed prescription.
def src(year, n):
    return (f"games.crossfit.com/workouts/games/{year}/{n} "
            f"(official CrossFit Games event, individual division confirmed), retrieved {TODAY}")

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

w("games-09-hill-run", "7-k Hill Run", "for_time", (2009, 1),
  [{"exercise": "run", "distance_m": 7000, "notes": "hill terrain"}],
  tags=["games", "2009", "running", "outdoor", "hill", "endurance"])

w("games-09-deadlift-ladder", "Deadlift Ladder (2009 Games)", "max_load", (2009, 2),
  [{"exercise": "deadlift", "reps": 1, "load": BB("315lb", "185lb"),
    "notes": "starting weight; 1 rep every 30 seconds, increasing 10 lb each round (men to 505 lb, women to 375 lb)"}],
  format_meta={"scoring": "load"}, tags=["games", "2009", "barbell", "max-load", "ladder"])

w("games-09-hill-sprint-sandbags", "Hill Sprint with Sandbags", "for_time", (2009, 3),
  [{"exercise": "sandbag-carry", "distance_m": 170, "load": BB("35lb", "35lb"),
    "notes": "hill sprint; men carry 2 sandbags, women carry 1"}],
  tags=["games", "2009", "outdoor", "hill"])

w("games-09-row-stake", "Row and Stake", "for_time", (2009, 4),
  [{"exercise": "row", "distance_m": 500},
   {"exercise": "stake-drive", "notes": "drive a 4 ft (men) / 3 ft (women) stake into the ground"},
   {"exercise": "row", "distance_m": 500}],
  tags=["games", "2009", "rowing", "venue-equipment"])

w("games-09-wall-ball-snatch", "Wall-Ball Snatch", "interval", (2009, 5),
  [{"exercise": "wall-ball-shot", "reps": 30, "load": BB("20lb", "14lb")},
   {"exercise": "squat-snatch", "reps": 30, "load": BB("75lb", "45lb")}],
  format_meta={"rounds": 3, "scoring": "time"}, tags=["games", "2009", "barbell", "3-rounds"])

w("games-09-1rm-snatch", "1RM Snatch (2009 Games)", "max_load", (2009, 6),
  [{"exercise": "snatch", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight"}],
  format_meta={"scoring": "load"}, tags=["games", "2009", "barbell", "max-load"])

w("games-09-hspu-kb-ghd", "HSPU-KB Swing-GHD", "amrap", (2009, 7),
  [{"exercise": "handstand-push-up", "reps": 4},
   {"exercise": "russian-kettlebell-swing", "reps": 8, "load": BB("32kg", "24kg")},
   {"exercise": "ghd-sit-up", "reps": 12}],
  format_meta={"time_cap_minutes": 8, "scoring": "rounds_reps"},
  tags=["games", "2009", "gymnastics", "kettlebell"])

w("games-09-complex-chipper", "Complex Chipper (2009 Games)", "for_time", (2009, 8),
  [{"exercise": "clean", "reps": 15, "load": BB("155lb", "100lb")},
   {"exercise": "toes-to-bar", "reps": 30},
   {"exercise": "box-jump", "reps": 30, "notes": "24 in (men) / 20 in (women) box"},
   {"exercise": "muscle-up", "reps": 15},
   {"exercise": "dumbbell-push-press", "reps": 30, "load": BB("40lb", "25lb")},
   {"exercise": "double-under", "reps": 30},
   {"exercise": "thruster", "reps": 15, "load": BB("135lb", "95lb")},
   {"exercise": "pull-up", "reps": 30},
   {"exercise": "burpee", "reps": 30},
   {"exercise": "overhead-walking-lunge", "distance_m": 91, "load": BB("45lb", "25lb"), "notes": "300 ft"}],
  tags=["games", "2009", "barbell", "dumbbell", "gymnastics"])

print(f"Wrote 2009 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
