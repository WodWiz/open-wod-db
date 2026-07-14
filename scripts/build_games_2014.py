import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games individual events -- 2014. Each verified against its official
# games.crossfit.com/workouts/games/2014/<n> page, cross-referenced via
# independent sources for events whose primary page 404'd.
#
# SKIPPED: Event 9 "Clean Speed Ladder" -- a 3-round elimination bracket
# (top 24 advance from QF, top 8 from SF), not a fixed single prescription;
# left out per the Games scoping decision (ROADMAP.md).
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

w("games-14-the-beach", "The Beach", "for_time", (2014, 1),
  [{"exercise": "swim", "distance_m": 229, "notes": "250 yd"},
   {"exercise": "kettlebell-thruster", "reps": 50, "load": BB("35lb", "24lb")},
   {"exercise": "burpee", "reps": 30},
   {"exercise": "swim", "distance_m": 457, "notes": "500 yd"},
   {"exercise": "burpee", "reps": 30},
   {"exercise": "kettlebell-thruster", "reps": 50, "load": BB("35lb", "24lb")},
   {"exercise": "swim", "distance_m": 229, "notes": "250 yd"}],
  tags=["games", "2014", "swim", "open-water", "kettlebell"])

w("games-14-overhead-squat", "Overhead Squat (2014 Games)", "max_load", (2014, 2),
  [{"exercise": "overhead-squat", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight; 3 attempts"}],
  format_meta={"scoring": "load"}, tags=["games", "2014", "barbell", "max-load"])

w("games-14-triple-3", "Triple 3", "for_time", (2014, 3),
  [{"exercise": "row", "distance_m": 3000},
   {"exercise": "double-under", "reps": 300},
   {"exercise": "run", "distance_m": 4828, "notes": "3 miles"}],
  tags=["games", "2014", "rowing", "running", "jump-rope", "endurance"])

w("games-14-sprint-sled-1", "Sprint Sled 1", "for_time", (2014, 4),
  [{"exercise": "sled-push", "distance_m": 91, "notes": "100 yd (men) / 55 yd (women)"}],
  format_meta=CAP(2), tags=["games", "2014", "venue-equipment"])

w("games-14-sprint-sled-2", "Sprint Sled 2", "for_time", (2014, 5),
  [{"exercise": "sled-push", "distance_m": 91, "notes": "100 yd (men) / 55 yd (women)"}],
  format_meta=CAP(3), tags=["games", "2014", "venue-equipment"],
  notes=src(2014, 5) + "; separately scored from Sprint Sled 1")

w("games-14-21-15-9-complex", "21-15-9 Complex", "for_time", (2014, 6),
  [{"exercise": "deadlift", "reps": 8, "load": BB("155lb", "115lb")},
   {"exercise": "clean", "reps": 7, "load": BB("155lb", "115lb")},
   {"exercise": "snatch", "reps": 6, "load": BB("155lb", "115lb")},
   {"exercise": "pull-up", "reps": 8}, {"exercise": "chest-to-bar-pull-up", "reps": 7}, {"exercise": "bar-muscle-up", "reps": 6},
   {"exercise": "deadlift", "reps": 6, "load": BB("155lb", "115lb")},
   {"exercise": "clean", "reps": 5, "load": BB("155lb", "115lb")},
   {"exercise": "snatch", "reps": 4, "load": BB("155lb", "115lb")},
   {"exercise": "pull-up", "reps": 6}, {"exercise": "chest-to-bar-pull-up", "reps": 5}, {"exercise": "bar-muscle-up", "reps": 4},
   {"exercise": "deadlift", "reps": 4, "load": BB("155lb", "115lb")},
   {"exercise": "clean", "reps": 3, "load": BB("155lb", "115lb")},
   {"exercise": "snatch", "reps": 2, "load": BB("155lb", "115lb")},
   {"exercise": "pull-up", "reps": 4}, {"exercise": "chest-to-bar-pull-up", "reps": 3}, {"exercise": "bar-muscle-up", "reps": 2}],
  format_meta=CAP(7), tags=["games", "2014", "barbell", "gymnastics"],
  notes=src(2014, 6) + "; named for its three descending stages, though the actual rep scheme is 8-7-6, 6-5-4, 4-3-2 rather than literal 21-15-9")

w("games-14-muscle-up-biathlon", "Muscle-Up Biathlon", "for_time", (2014, 7),
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "muscle-up", "reps": 18},
   {"exercise": "run", "distance_m": 400},
   {"exercise": "muscle-up", "reps": 15},
   {"exercise": "run", "distance_m": 400},
   {"exercise": "muscle-up", "reps": 12}],
  format_meta=CAP(18), tags=["games", "2014", "running", "gymnastics"],
  notes=src(2014, 7) + "; each time an athlete breaks a set of muscle-ups, they must run an additional 200 m penalty lap")

w("games-14-sprint-carry", "Sprint Carry", "for_time", (2014, 8),
  [{"exercise": "sprint", "distance_m": 91, "notes": "100 yd"},
   {"exercise": "sandbag-carry", "distance_m": 91, "load": BB("100lb", "60lb"), "notes": "100 yd; metal cylinder"},
   {"exercise": "sprint", "distance_m": 91, "notes": "100 yd"},
   {"exercise": "sandbag-carry", "distance_m": 91, "load": BB("120lb", "80lb"), "notes": "100 yd"},
   {"exercise": "sprint", "distance_m": 91, "notes": "100 yd"},
   {"exercise": "sandbag-carry", "distance_m": 91, "load": BB("150lb", "100lb"), "notes": "100 yd; metal cylinder"}],
  tags=["games", "2014", "venue-equipment"])

w("games-14-push-pull", "Push Pull", "for_time", (2014, 10),
  [{"exercise": "deficit-handstand-push-up", "reps": 7, "notes": "strict, no kipping; smallest deficit"},
   {"exercise": "sled-pull", "distance_m": 15, "load": BB("204lb", "145lb"), "notes": "50 ft"},
   {"exercise": "deficit-handstand-push-up", "reps": 8, "notes": "strict, no kipping; deficit increases each round"},
   {"exercise": "sled-pull", "distance_m": 15, "load": BB("260lb", "180lb"), "notes": "50 ft"},
   {"exercise": "deficit-handstand-push-up", "reps": 9, "notes": "strict, no kipping; deficit increases each round"},
   {"exercise": "sled-pull", "distance_m": 15, "load": BB("315lb", "215lb"), "notes": "50 ft"},
   {"exercise": "deficit-handstand-push-up", "reps": 10, "notes": "strict, no kipping; largest deficit"},
   {"exercise": "sled-pull", "distance_m": 15, "load": BB("370lb", "250lb"), "notes": "50 ft"}],
  format_meta=CAP(11), tags=["games", "2014", "venue-equipment", "gymnastics"])

w("games-14-midline-march", "Midline March", "interval", (2014, 11),
  [{"exercise": "ghd-sit-up", "reps": 25},
   {"exercise": "handstand-walk", "distance_m": 15, "notes": "50 ft"},
   {"exercise": "overhead-walking-lunge", "distance_m": 15, "load": BB("155lb", "115lb"), "notes": "50 ft"}],
  format_meta={"rounds": 3, "scoring": "time"}, tags=["games", "2014", "barbell", "gymnastics", "3-rounds"])

w("games-14-thick-n-quick", "Thick 'n Quick", "for_time", (2014, 12),
  [{"exercise": "rope-climb", "reps": 4, "notes": "20 ft, on a 2-inch thick rope"},
   {"exercise": "overhead-squat", "reps": 3, "load": BB("245lb", "165lb")}],
  format_meta=CAP(4), tags=["games", "2014", "venue-equipment", "barbell", "gymnastics"])

w("games-14-double-grace", "Double Grace", "for_time", (2014, 13),
  [{"exercise": "clean-and-jerk", "reps": 60, "load": BB("135lb", "95lb")}],
  format_meta=CAP(7), tags=["games", "2014", "barbell"],
  notes=src(2014, 13) + "; double the reps of the Girl WOD Grace; announced only 30 seconds before the event began")

print(f"Wrote 2014 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
