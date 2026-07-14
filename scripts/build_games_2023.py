import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games individual events -- 2023. Each verified against its official
# games.crossfit.com/workouts/games/2023/<n> page (cross-referenced against a
# second independent source for events whose primary page returned incomplete
# or division-ambiguous content).
#
# SKIPPED: Event 2 "Ride" -- purely lap-count on a mountain-bike course with no
# fixed movement/rep prescription; left out per the Games scoping decision
# (documented in ROADMAP.md) rather than fabricated.
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

w("games-23-pig-chipper", "Pig Chipper", "for_time", (2023, 1),
  [{"exercise": "d-ball-over-shoulder", "reps": 10, "notes": "\"pig flips\""},
   {"exercise": "chest-to-bar-pull-up", "reps": 25},
   {"exercise": "toes-to-bar", "reps": 50},
   {"exercise": "wall-ball-shot", "reps": 100, "load": BB("20lb", "14lb")},
   {"exercise": "toes-to-bar", "reps": 50},
   {"exercise": "chest-to-bar-pull-up", "reps": 25},
   {"exercise": "d-ball-over-shoulder", "reps": 10, "notes": "\"pig flips\""}],
  format_meta=CAP(18), tags=["games", "2023", "venue-equipment", "gymnastics"])

w("games-23-inverted-medley", "Inverted Medley", "for_time", (2023, 3),
  [{"exercise": "handstand-walk", "distance_m": 9, "notes": "30 ft, unbroken, over a ramp"},
   {"exercise": "freestanding-handstand-push-up", "reps": 8},
   {"exercise": "obstacle-pirouette", "notes": "unbroken obstacle steps to a 180-degree pirouette"},
   {"exercise": "pull-over", "reps": 16},
   {"exercise": "obstacle-pirouette", "notes": "unbroken obstacle steps to a 360-degree pirouette"},
   {"exercise": "freestanding-handstand-push-up", "reps": 8},
   {"exercise": "handstand-walk", "distance_m": 9, "notes": "30 ft, unbroken, over a ramp"}],
  format_meta=CAP(7), tags=["games", "2023", "venue-equipment", "gymnastics"])

w("games-23-alpaca-redux", "The Alpaca Redux", "for_time", (2023, 4),
  [{"exercise": "sled-push", "distance_m": 38, "load": BB("443lb", "546lb"), "notes": "126 ft, starting with all six kettlebells"},
   {"exercise": "legless-rope-climb", "reps": 2},
   {"exercise": "kettlebell-clean-and-jerk", "reps": 12, "load": BB("53lb", "70lb")},
   {"exercise": "sled-push", "distance_m": 13, "load": BB("53lb", "70lb"), "notes": "42 ft, starting with two kettlebells; add two kettlebells to the sled after each round"},
   {"exercise": "legless-rope-climb", "reps": 2},
   {"exercise": "kettlebell-clean-and-jerk", "reps": 12, "load": BB("53lb", "70lb")},
   {"exercise": "sled-push", "distance_m": 13, "load": BB("53lb", "70lb"), "notes": "42 ft, add two kettlebells to the sled after each round"},
   {"exercise": "legless-rope-climb", "reps": 2},
   {"exercise": "kettlebell-clean-and-jerk", "reps": 12, "load": BB("53lb", "70lb")},
   {"exercise": "sled-push", "distance_m": 13, "load": BB("53lb", "70lb"), "notes": "42 ft, add two kettlebells to the sled after each round"}],
  format_meta=CAP(18), tags=["games", "2023", "venue-equipment", "kettlebell"])

w("games-23-ski-bag", "Ski-Bag", "for_time", (2023, 5),
  [{"exercise": "ski-erg", "reps": 30, "notes": "calories"},
   {"exercise": "sandbag-squat", "reps": 30, "load": BB("200lb", "125lb")},
   {"exercise": "ski-erg", "reps": 20, "notes": "calories"},
   {"exercise": "sandbag-squat", "reps": 20, "load": BB("200lb", "125lb")}],
  format_meta=CAP(6), tags=["games", "2023", "venue-equipment"])

w("games-23-helena", "Helena", "interval", (2023, 6),
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "bar-muscle-up", "reps": 12},
   {"exercise": "dumbbell-snatch", "reps": 21, "load": BB("50lb", "35lb")}],
  format_meta={"rounds": 3, "time_cap_minutes": 11, "scoring": "time"},
  tags=["games", "2023", "dumbbell", "running", "gymnastics"])

w("games-23-cross-country-5k", "Cross-Country 5K", "for_time", (2023, 7),
  [{"exercise": "run", "distance_m": 5000}],
  format_meta=CAP(30), tags=["games", "2023", "running", "outdoor", "endurance"])

w("games-23-intervals", "Intervals", "multi_part", (2023, 8),
  segments=[
    {"label": "Interval 1", "format": "for_time",
     "movements": [{"exercise": "box-jump-over", "reps": 21, "notes": "24 in (men) / 20 in (women)"},
                   {"exercise": "row", "reps": 15, "notes": "calories"},
                   {"exercise": "burpee-box-jump-over", "reps": 9, "notes": "48 in (men) / 36 in (women)"},
                   {"exercise": "box-jump-over", "reps": 21, "notes": "24 in (men) / 20 in (women)"},
                   {"exercise": "row", "reps": 15, "notes": "calories"},
                   {"exercise": "burpee-box-jump-over", "reps": 9, "notes": "48 in (men) / 36 in (women)"}]},
    {"label": "Interval 2 (starts at the 6:00 mark)", "format": "for_time",
     "movements": [{"exercise": "burpee-box-jump-over", "reps": 9, "notes": "48 in (men) / 36 in (women)"},
                   {"exercise": "row", "reps": 15, "notes": "calories"},
                   {"exercise": "box-jump-over", "reps": 21, "notes": "24 in (men) / 20 in (women)"},
                   {"exercise": "burpee-box-jump-over", "reps": 9, "notes": "48 in (men) / 36 in (women)"},
                   {"exercise": "row", "reps": 15, "notes": "calories"},
                   {"exercise": "box-jump-over", "reps": 21, "notes": "24 in (men) / 20 in (women)"}]},
  ],
  format_meta={"time_cap_minutes": 12, "scoring": "time"},
  tags=["games", "2023", "rowing", "bodyweight"],
  notes=src(2023, 8) + "; Interval 2 begins at a fixed clock time (6:00) regardless of when Interval 1 finishes, movements reversed")

w("games-23-olympic-total", "Olympic Total", "max_load", (2023, 9),
  [{"exercise": "snatch", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight; 2 attempts, 20 seconds per lift"},
   {"exercise": "clean-and-jerk", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight; 2 attempts, 20 seconds per lift"}],
  format_meta={"scoring": "load"},
  tags=["games", "2023", "barbell", "max-load"],
  notes=src(2023, 9) + "; score is the combined total of best snatch + best clean and jerk")

w("games-23-muscle-up-logs", "Muscle-up Logs", "for_time", (2023, 10),
  [{"exercise": "muscle-up", "reps": 7}, {"exercise": "sandbag-over-log", "reps": 3, "load": BB("150lb", "100lb")},
   {"exercise": "muscle-up", "reps": 7}, {"exercise": "sandbag-over-log", "reps": 3, "load": BB("150lb", "100lb")},
   {"exercise": "muscle-up", "reps": 7}, {"exercise": "sandbag-over-log", "reps": 3, "load": BB("150lb", "100lb")},
   {"exercise": "muscle-up", "reps": 7}, {"exercise": "sandbag-over-log", "reps": 3, "load": BB("150lb", "100lb")},
   {"exercise": "muscle-up", "reps": 7}, {"exercise": "sandbag-over-log", "reps": 3, "load": BB("200lb", "125lb")}],
  tags=["games", "2023", "venue-equipment", "gymnastics"],
  notes=src(2023, 10) + "; sandbag carried and tossed over 3 logs each round; weight increases in the final (5th) round")

w("games-23-parallel-bar-pull", "Parallel-bar Pull", "interval", (2023, 11),
  [{"exercise": "parallel-bar-traverse", "notes": "down and back"},
   {"exercise": "double-under", "reps": 30, "notes": "heavy rope"},
   {"exercise": "sled-pull", "load": BB("345lb", "290lb"), "notes": "one section, hand-over-hand"}],
  format_meta={"rounds": 8, "time_cap_minutes": 15, "scoring": "time"},
  tags=["games", "2023", "venue-equipment", "gymnastics"])

w("games-23-echo-thruster-final", "Echo Thruster Final", "for_time", (2023, 12),
  [{"exercise": "echo-bike", "reps": 21, "notes": "calories"},
   {"exercise": "thruster", "reps": 21, "load": BB("115lb", "85lb")},
   {"exercise": "echo-bike", "reps": 18, "notes": "calories"},
   {"exercise": "thruster", "reps": 18, "load": BB("135lb", "95lb")},
   {"exercise": "echo-bike", "reps": 15, "notes": "calories"},
   {"exercise": "thruster", "reps": 15, "load": BB("155lb", "105lb")},
   {"exercise": "overhead-walking-lunge", "distance_m": 20, "load": BB("155lb", "105lb"), "notes": "66 ft"}],
  format_meta=CAP(10), tags=["games", "2023", "venue-equipment", "barbell"])

print(f"Wrote 2023 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
