import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games individual events -- 2020. Each verified against its official
# games.crossfit.com/workouts/games/2020/<n> page, cross-referenced via
# independent sources for events whose primary page 404'd.
#
# SKIPPED: Event 14 "Snatch Speed Triple" -- a 3-round elimination tournament
# (slowest athlete cut each round, survivors advance to a heavier round), not
# a fixed single prescription; left out per the Games scoping decision
# (ROADMAP.md).
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
CAP = lambda n: {"time_cap_minutes": n, "scoring": "time"}

w("games-20-friendly-fran", "Friendly Fran", "interval", (2020, 1),
  [{"exercise": "thruster", "reps": 21, "load": BB("115lb", "85lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": 21}],
  format_meta={"rounds": 3, "scoring": "time"}, tags=["games", "2020", "barbell", "gymnastics"])

w("games-20-1rm-front-squat", "1RM Front Squat", "max_load", (2020, 2),
  [{"exercise": "front-squat", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight"}],
  format_meta={"time_cap_minutes": 20, "scoring": "load"}, tags=["games", "2020", "barbell", "max-load"])

w("games-20-damn-diane", "Damn Diane", "interval", (2020, 3),
  [{"exercise": "deadlift", "reps": 15, "load": BB("315lb", "205lb")},
   {"exercise": "strict-handstand-push-up", "reps": 15, "notes": "3.5 in (men) / 2 in (women) deficit"}],
  format_meta={"rounds": 3, "scoring": "time"}, tags=["games", "2020", "barbell", "gymnastics"])

w("games-20-1000m-row", "1,000-M Row", "for_time", (2020, 4),
  [{"exercise": "row", "distance_m": 1000}], tags=["games", "2020", "rowing"])

w("games-20-nasty-nancy", "Nasty Nancy", "interval", (2020, 5),
  [{"exercise": "run", "distance_m": 500},
   {"exercise": "overhead-squat", "reps": 15, "load": BB("185lb", "125lb")},
   {"exercise": "bar-facing-burpee", "reps": 15}],
  format_meta={"rounds": 5, "scoring": "time"}, tags=["games", "2020", "barbell", "running", "bodyweight"])

w("games-20-handstand-hold", "Handstand Hold", "max_effort", (2020, 6),
  [{"exercise": "handstand-hold", "notes": "freestanding, within a 4x4 ft box; ends on a hand touching/crossing the box border or foot/head touching the ground; multiple attempts allowed"}],
  format_meta={"time_cap_minutes": 20, "scoring": "time"},
  tags=["games", "2020", "gymnastics", "max-effort"],
  notes=src(2020, 6) + "; score is longest single hold duration, not fastest time")

w("games-20-awful-annie", "Awful Annie", "for_time", (2020, 7),
  [{"exercise": "double-under", "reps": [50, 40, 30, 20, 10]},
   {"exercise": "ghd-sit-up", "reps": [50, 40, 30, 20, 10]},
   {"exercise": "clean", "reps": [5, 4, 3, 2, 1], "load": BB("275lb", "185lb")}],
  tags=["games", "2020", "barbell", "gymnastics", "ladder"],
  notes=src(2020, 7) + "; the field was cut to the top 5 men and top 5 women after this event (end of Stage 1)")

w("games-20-2007-reload", "2007 Reload", "for_time", (2020, 8),
  [{"exercise": "row", "distance_m": 1500},
   {"exercise": "bar-muscle-up", "reps": 10},
   {"exercise": "shoulder-to-overhead", "reps": 7, "load": BB("235lb", "145lb")},
   {"exercise": "bar-muscle-up", "reps": 10},
   {"exercise": "shoulder-to-overhead", "reps": 7, "load": BB("235lb", "145lb")},
   {"exercise": "bar-muscle-up", "reps": 10},
   {"exercise": "shoulder-to-overhead", "reps": 7, "load": BB("235lb", "145lb")},
   {"exercise": "bar-muscle-up", "reps": 10},
   {"exercise": "shoulder-to-overhead", "reps": 7, "load": BB("235lb", "145lb")},
   {"exercise": "bar-muscle-up", "reps": 10},
   {"exercise": "shoulder-to-overhead", "reps": 7, "load": BB("235lb", "145lb")}],
  tags=["games", "2020", "rowing", "barbell", "gymnastics"])

w("games-20-corn-sack-sprint", "Corn Sack Sprint", "for_time", (2020, 9),
  [{"exercise": "sandbag-carry", "distance_m": 293, "load": BB("50lb", "30lb"), "notes": "320 m hill sprint, carrying a corn sack"}],
  tags=["games", "2020", "outdoor", "hill"])

w("games-20-crossfit-total", "CrossFit Total", "max_load", (2020, 10),
  [{"exercise": "back-squat", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight; 3 attempts, 3 minutes between"},
   {"exercise": "strict-press", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight; 3 attempts, 3 minutes between"},
   {"exercise": "deadlift", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight; 3 attempts, 3 minutes between"}],
  format_meta={"scoring": "load"},
  tags=["games", "2020", "barbell", "max-load"],
  notes=src(2020, 10) + "; score is the combined total of all three best lifts")

w("games-20-handstand-sprint", "Handstand Sprint", "for_time", (2020, 11),
  [{"exercise": "handstand-walk", "distance_m": 91, "notes": "100 yd"}],
  tags=["games", "2020", "gymnastics"])

w("games-20-ranch-loop", "Ranch Loop", "for_time", (2020, 12),
  [{"exercise": "run", "distance_m": 9656, "notes": "approx. 6 miles: the ~3-mile varied-terrain loop run out, then reversed and run back"}],
  tags=["games", "2020", "running", "outdoor", "hill", "endurance"],
  notes=src(2020, 12) + "; originally announced as a single ~3-mile loop, but athletes were told on the day to turn around and run the course in reverse, doubling its length")

w("games-20-toes-to-bar-lunge", "Toes-to-Bar/Lunge", "for_time", (2020, 13),
  [{"exercise": "toes-to-bar", "reps": [30, 20, 10]},
   {"exercise": "kettlebell-front-rack-lunge", "distance_m": 1, "reps": [30, 20, 10],
    "load": BB("70lb", "53lb"), "notes": "2 kettlebells (32 kg men / 24 kg women); reps measured in yards walked"}],
  tags=["games", "2020", "gymnastics", "kettlebell", "ladder"])

w("games-20-bike-repeater", "Bike Repeater", "interval", (2020, 15),
  [{"exercise": "bike", "distance_m": 440},
   {"exercise": "legless-rope-climb", "reps": 1, "notes": "to 15 feet"}],
  format_meta={"rounds": 10, "scoring": "time"}, tags=["games", "2020", "venue-equipment", "gymnastics"])

w("games-20-happy-star", "Happy Star", "for_time", (2020, 16),
  [{"exercise": "run", "distance_m": 300, "notes": "hill run; course changes each round"},
   {"exercise": "burpee", "reps": 5}, {"exercise": "thruster", "reps": 5, "load": BB("135lb", "95lb")},
   {"exercise": "run", "distance_m": 300, "notes": "hill run; course changes each round"},
   {"exercise": "burpee", "reps": 7}, {"exercise": "thruster", "reps": 7, "load": BB("145lb", "105lb")},
   {"exercise": "run", "distance_m": 300, "notes": "hill run; course changes each round"},
   {"exercise": "burpee", "reps": 9}, {"exercise": "thruster", "reps": 9, "load": BB("155lb", "110lb")},
   {"exercise": "run", "distance_m": 300, "notes": "hill run; course changes each round"},
   {"exercise": "burpee", "reps": 11}, {"exercise": "thruster", "reps": 11, "load": BB("165lb", "115lb")}],
  tags=["games", "2020", "outdoor", "hill", "barbell", "ascending"])

w("games-20-swim-n-stuff", "Swim 'N' Stuff", "interval", (2020, 17),
  [{"exercise": "bike", "reps": 15, "notes": "calories (women use 10); air bike"},
   {"exercise": "swim", "distance_m": 46, "notes": "50 m"},
   {"exercise": "ghd-sit-up", "reps": 10},
   {"exercise": "ball-slam", "reps": 10, "load": BB("60lb", "40lb")}],
  format_meta={"rounds": 4, "interval_seconds": 240, "scoring": "time"},
  tags=["games", "2020", "swim", "venue-equipment"],
  notes=src(2020, 17) + "; new round begins every 4 minutes; rounds 2 and 4 are performed with the movement order reversed")

w("games-20-sprint-sled-sprint", "Sprint Sled Sprint", "for_time", (2020, 18),
  [{"exercise": "sprint", "distance_m": 91, "notes": "100 yd"},
   {"exercise": "sled-push", "distance_m": 91, "load": BB("105lb", "80lb"), "notes": "100 yd"},
   {"exercise": "sprint", "distance_m": 91, "notes": "100 yd"}],
  tags=["games", "2020", "venue-equipment"])

w("games-20-atalanta", "Atalanta", "for_time", (2020, 19),
  [{"exercise": "run", "distance_m": 1609, "notes": "1 mile; weight vest 20 lb (men) / 14 lb (women)"},
   {"exercise": "handstand-push-up", "reps": 100, "notes": "weight vest 20 lb (men) / 14 lb (women)"},
   {"exercise": "pistol", "reps": 200, "notes": "weight vest 20 lb (men) / 14 lb (women); alternating legs"},
   {"exercise": "pull-up", "reps": 300, "notes": "weight vest 20 lb (men) / 14 lb (women)"},
   {"exercise": "run", "distance_m": 1609, "notes": "1 mile; weight vest 20 lb (men) / 14 lb (women)"}],
  tags=["games", "2020", "weighted", "high-volume", "gymnastics"],
  notes=src(2020, 19) + "; all reps must be unpartitioned (each movement fully completed before advancing); combines elements of Mary and the Hero WOD Murph")

print(f"Wrote 2020 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
