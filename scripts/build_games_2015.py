import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games individual events -- 2015. Each verified against its official
# games.crossfit.com/workouts/games/2015/<n> page, cross-referenced via
# independent sources for events whose primary page 404'd.
#
# SKIPPED (per the Games scoping decision in ROADMAP.md):
# - Event 4 "Snatch Speed Ladder" -- a 3-round elimination bracket (top 20
#   advance from QF, top 10 from SF), not a fixed single prescription.
# - Events 6/7 "Sprint Course 1/2" -- a fixed-format sprint through an
#   obstacle course, but the individual obstacles aren't itemized in any
#   available source; left out rather than guessed.
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

w("games-15-pier-paddle", "Pier Paddle", "for_time", (2015, 1),
  [{"exercise": "swim", "distance_m": 500},
   {"exercise": "paddleboard", "distance_m": 3219, "notes": "2 miles"},
   {"exercise": "swim", "distance_m": 500}],
  format_meta=CAP(60), tags=["games", "2015", "swim", "open-water", "endurance"])

w("games-15-sandbag-2015", "Sandbag 2015", "for_time", (2015, 2),
  [{"exercise": "sandbag-carry", "reps": 8, "load": BB("720lb total", "480lb total"),
    "notes": "men move 4x100 lb + 4x80 lb bags (720 lb total); women's individual bag breakdown "
              "for the 480 lb total is not confirmed from available sources, flagged per "
              "CONTRIBUTING; up the north stairs, across the floor (wheelbarrow permitted), "
              "up a wall, to the top of the south stairs"}],
  format_meta=CAP(15), tags=["games", "2015", "venue-equipment"])

w("games-15-murph", "Murph (2015 Games)", "for_time", (2015, 3),
  [{"exercise": "run", "distance_m": 1609},
   {"exercise": "pull-up", "reps": 100}, {"exercise": "push-up", "reps": 200}, {"exercise": "air-squat", "reps": 300},
   {"exercise": "run", "distance_m": 1609}],
  format_meta=CAP(55), tags=["games", "2015", "running", "gymnastics", "weighted", "high-volume"],
  notes=src(2015, 3) + "; the Hero WOD Murph with 20 lb (men) / 14 lb (women) body armor and a "
        "55-minute cap; athletes advance to the next bar/rig every 25 pull-ups, 50 push-ups, and 75 squats")

w("games-15-heavy-dt", "Heavy DT", "interval", (2015, 5),
  [{"exercise": "deadlift", "reps": 12, "load": BB("205lb", "145lb")},
   {"exercise": "hang-power-clean", "reps": 9, "load": BB("205lb", "145lb")},
   {"exercise": "push-jerk", "reps": 6, "load": BB("205lb", "145lb")}],
  format_meta={"rounds": 5, "time_cap_minutes": 12, "scoring": "time"},
  tags=["games", "2015", "barbell", "5-rounds"])

w("games-15-soccer-chipper", "Soccer Chipper", "for_time", (2015, 8),
  [{"exercise": "d-ball-over-shoulder", "distance_m": 30, "load": BB("560lb", "395lb"), "notes": "100 ft, \"pig flip\""},
   {"exercise": "legless-rope-climb", "reps": 4},
   {"exercise": "handstand-walk", "distance_m": 30, "notes": "100 ft, in unbroken 50 ft sections"}],
  format_meta=CAP(12), tags=["games", "2015", "venue-equipment", "gymnastics"])

w("games-15-clean-and-jerk", "Clean and Jerk (2015 Games)", "max_load", (2015, 9),
  [{"exercise": "clean-and-jerk", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight; "
    "two 20-second lifting windows, one athlete lifting at a time"}],
  format_meta={"scoring": "load"}, tags=["games", "2015", "barbell", "max-load"])

w("games-15-triangle-couplet", "Triangle Couplet", "for_time", (2015, 10),
  [{"exercise": "thruster", "reps": [15, 10, 6], "load": BB("165lb", "115lb")},
   {"exercise": "bar-muscle-up", "reps": [15, 10, 6]}],
  format_meta=CAP(10), tags=["games", "2015", "barbell", "gymnastics", "ladder"])

w("games-15-midline-madness", "Midline Madness", "interval", (2015, 11),
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "yoke-carry", "distance_m": 15, "load": BB("380lb", "300lb"), "notes": "50 ft"}],
  format_meta={"rounds": 6, "time_cap_minutes": 25, "scoring": "time"},
  tags=["games", "2015", "venue-equipment", "running"])

w("games-15-pedal-to-the-metal-1", "Pedal to the Metal 1", "for_time", (2015, 12),
  [{"exercise": "pegboard", "reps": 3},
   {"exercise": "row", "reps": 24, "notes": "calories"},
   {"exercise": "bike", "reps": 16, "notes": "calories; assault bike"},
   {"exercise": "dumbbell-snatch", "reps": 8, "load": BB("100lb", "70lb"), "notes": "squat snatch variant"}],
  format_meta=CAP(6), tags=["games", "2015", "venue-equipment", "rowing", "dumbbell"],
  notes=src(2015, 12) + "; introduced the pegboard to Games competition for the first time")

w("games-15-pedal-to-the-metal-2", "Pedal to the Metal 2", "for_time", (2015, 13),
  [{"exercise": "parallette-handstand-push-up", "reps": 12},
   {"exercise": "row", "reps": 24, "notes": "calories"},
   {"exercise": "bike", "reps": 16, "notes": "calories; assault bike"},
   {"exercise": "kettlebell-deadlift", "reps": 8, "load": BB("203lb", "124lb")}],
  tags=["games", "2015", "rowing", "kettlebell", "gymnastics"],
  notes=src(2015, 13) + "; the final individual event of the 2015 Games, contested immediately after Pedal to the Metal 1")

print(f"Wrote 2015 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
