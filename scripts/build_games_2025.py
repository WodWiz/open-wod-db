import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games individual events -- 2025. Each verified against its official
# games.crossfit.com/workouts/games/2025/<n> page. No events skipped this
# year -- all 10 have a genuine fixed prescription.
def src(year, n):
    return (f"games.crossfit.com/workouts/games/{year}/{n} "
            f"(official CrossFit Games event), retrieved {TODAY}")

def w(id, name, fmt, slug, movements=None, segments=None, format_meta=None, tags=None, notes=None):
    entry = {
        "id": id, "name": name, "category": "games", "format": fmt,
        "format_meta": format_meta or {},
        "movements": movements or [],
        "partition": None, "scaling": None, "origin": None,
        "tags": tags or [], "source_notes": notes or src(*slug),
        "schema_version": VER, "last_updated": TODAY,
    }
    if segments is not None:
        entry["segments"] = segments
    with open(os.path.join(OUT, f"{id}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(entry, f, indent=2)
        f.write("\n")

BB = lambda m, f: {"rx_male": m, "rx_female": f}

w("games-25-run-row-run", "Run/Row/Run", "for_time", (2025, 1),
  [{"exercise": "run", "distance_m": 6437, "notes": "4 miles"},
   {"exercise": "row", "distance_m": 3000},
   {"exercise": "run", "distance_m": 3219, "notes": "2 miles"}],
  tags=["games", "2025", "running", "rowing", "endurance"])

w("games-25-all-crossed-up", "All Crossed Up", "for_time", (2025, 2),
  [{"exercise": "wall-climb", "reps": 20},
   {"exercise": "dumbbell-shoulder-to-overhead", "reps": 10, "load": BB("100lb", "70lb")},
   {"exercise": "crossover-single-under", "reps": 20},
   {"exercise": "toes-to-bar", "reps": 30},
   {"exercise": "crossover-single-under", "reps": 20},
   {"exercise": "dumbbell-shoulder-to-overhead", "reps": 10, "load": BB("100lb", "70lb")},
   {"exercise": "crossover-single-under", "reps": 20},
   {"exercise": "toes-to-bar", "reps": 30},
   {"exercise": "crossover-single-under", "reps": 20},
   {"exercise": "dumbbell-shoulder-to-overhead", "reps": 10, "load": BB("100lb", "70lb")}],
  format_meta={"time_cap_minutes": 10, "scoring": "time"},
  tags=["games", "2025", "dumbbell", "gymnastics", "jump-rope"])

w("games-25-climbing-couplet", "Climbing Couplet", "for_time", (2025, 3),
  [{"exercise": "pegboard", "reps": 4},
   {"exercise": "squat-clean", "reps": 4, "load": BB("235lb", "145lb"), "notes": "immediately followed by a front squat, counted together as 1 rep of the complex"},
   {"exercise": "pegboard", "reps": 3},
   {"exercise": "squat-clean", "reps": 3, "load": BB("265lb", "165lb"), "notes": "immediately followed by a front squat, counted together as 1 rep of the complex"},
   {"exercise": "pegboard", "reps": 2},
   {"exercise": "squat-clean", "reps": 2, "load": BB("285lb", "185lb"), "notes": "immediately followed by a front squat, counted together as 1 rep of the complex"},
   {"exercise": "pegboard", "reps": 1},
   {"exercise": "squat-clean", "reps": 1, "load": BB("305lb", "205lb"), "notes": "immediately followed by a front squat, counted together as 1 rep of the complex"}],
  tags=["games", "2025", "barbell", "gymnastics", "ladder"])

w("games-25-albany-grip-trip", "Albany Grip Trip", "interval", (2025, 4),
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "deadlift", "reps": 12, "load": BB("350lb", "220lb")},
   {"exercise": "handstand-walk", "distance_m": 30, "notes": "100 ft (150 ft on the final round)"}],
  format_meta={"rounds": 5, "scoring": "time"}, tags=["games", "2025", "barbell", "running", "gymnastics"])

w("games-25-1rm-back-squat", "1RM Back Squat", "max_load", (2025, 5),
  [{"exercise": "back-squat", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight"}],
  format_meta={"scoring": "load"}, tags=["games", "2025", "barbell", "max-load"])

w("games-25-throttle-up", "Throttle Up", "for_time", (2025, 6),
  [{"exercise": "ski-erg", "reps": 35, "notes": "calories"},
   {"exercise": "chest-to-bar-pull-up", "reps": 28},
   {"exercise": "burpee-box-jump-over", "reps": 24, "notes": "24 in (men) / 20 in (women) box"}],
  tags=["games", "2025", "venue-equipment", "gymnastics", "weight-vest"],
  notes=src(2025, 6) + "; performed wearing a 22 lb (men) / 16 lb (women) weight vest throughout")

w("games-25-hammer-down", "Hammer Down", "for_time", (2025, 7),
  [{"exercise": "bike", "reps": 35, "notes": "calories; Concept2 BikeErg"},
   {"exercise": "bar-muscle-up", "reps": 28},
   {"exercise": "burpee-box-jump-over", "reps": 24, "notes": "24 in (men) / 20 in (women) box"}],
  tags=["games", "2025", "gymnastics"],
  notes=src(2025, 7) + "; begins 7 minutes after the start of Throttle Up (Event 6)")

w("games-25-going-dark", "Going Dark", "for_time", (2025, 8),
  [{"exercise": "echo-bike", "reps": 50, "notes": "calories (women use 40)"},
   {"exercise": "yoke-carry", "distance_m": 30, "notes": "100 ft"},
   {"exercise": "deficit-handstand-push-up", "reps": 30},
   {"exercise": "yoke-carry", "distance_m": 30, "notes": "100 ft"},
   {"exercise": "echo-bike", "reps": 50, "notes": "calories (women use 40)"}],
  tags=["games", "2025", "venue-equipment", "gymnastics"])

w("games-25-running-isabel", "Running Isabel", "interval", (2025, 9),
  [{"exercise": "run", "distance_m": 61, "notes": "200 ft"},
   {"exercise": "snatch", "reps": 6, "load": BB("155lb", "105lb")}],
  format_meta={"rounds": 5, "scoring": "time"}, tags=["games", "2025", "barbell", "running"])

w("games-25-atlas", "Atlas", "for_time", (2025, 10),
  [{"exercise": "thruster", "reps": [9, 15, 21], "load": BB("135lb", "95lb")},
   {"exercise": "rope-climb", "reps": [3, 5, 7]},
   {"exercise": "overhead-walking-lunge", "distance_m": 30, "load": BB("135lb", "95lb"), "notes": "100 ft, finishing sequence"}],
  tags=["games", "2025", "barbell", "gymnastics", "ascending"],
  notes=src(2025, 10) + "; an ascending ladder (9-15-21), the reverse of the usual descending Fran-style scheme")

print(f"Wrote 2025 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
