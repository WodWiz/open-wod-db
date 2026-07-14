import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "open")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Open -- wave 2 (2019-2021). Each verified against its official
# games.crossfit.com/workouts/open/<year>/<n> page (both men's and women's Rx).
def src(year, n):
    return (f"games.crossfit.com/workouts/open/{year}/{n} "
            f"(official CrossFit Games Open workout), retrieved {TODAY}")

def w(id, name, fmt, slug, movements=None, segments=None, format_meta=None, tags=None, notes=None):
    entry = {
        "id": id, "name": name, "category": "open", "format": fmt,
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
AMRAP = lambda n, s="rounds_reps": {"time_cap_minutes": n, "scoring": s}
RDS = lambda n: {"rounds": n, "scoring": "time"}

# ---- 2021 ----
w("open-21-1", "21.1", "for_time", (2021, 1),
  [{"exercise": "wall-climb", "reps": [1, 3, 6, 9, 15, 21]},
   {"exercise": "double-under", "reps": [10, 30, 60, 90, 150, 210]}],
  format_meta=CAP(15), tags=["open", "2021", "bodyweight", "gymnastics"],
  notes=src(2021, 1) + "; bodyweight only, no Rx load")

w("open-21-2", "21.2", "for_time", (2021, 2),
  [{"exercise": "dumbbell-snatch", "reps": [10, 20, 30, 40, 50], "load": BB("50lb", "35lb")},
   {"exercise": "burpee-box-jump-over", "reps": 15, "notes": "24 in (men) / 20 in (women) box; repeated between each snatch set"}],
  format_meta=CAP(20), tags=["open", "2021", "dumbbell", "bodyweight"])

w("open-21-3", "21.3", "multi_part", (2021, 3),
  segments=[
    {"label": "Part 1", "format": "for_time",
     "movements": [{"exercise": "front-squat", "reps": 15, "load": BB("95lb", "65lb")},
                   {"exercise": "toes-to-bar", "reps": 30},
                   {"exercise": "thruster", "reps": 15, "load": BB("95lb", "65lb")}],
     "rest_after_seconds": 60},
    {"label": "Part 2", "format": "for_time",
     "movements": [{"exercise": "front-squat", "reps": 15, "load": BB("95lb", "65lb")},
                   {"exercise": "chest-to-bar-pull-up", "reps": 30},
                   {"exercise": "thruster", "reps": 15, "load": BB("95lb", "65lb")}],
     "rest_after_seconds": 60},
    {"label": "Part 3", "format": "for_time",
     "movements": [{"exercise": "front-squat", "reps": 15, "load": BB("95lb", "65lb")},
                   {"exercise": "bar-muscle-up", "reps": 30},
                   {"exercise": "thruster", "reps": 15, "load": BB("95lb", "65lb")}]},
  ],
  format_meta=CAP(15), tags=["open", "2021", "barbell", "gymnastics"])

w("open-21-4", "21.4", "max_load", (2021, 4),
  [{"exercise": "deadlift", "reps": 1}, {"exercise": "clean", "reps": 1},
   {"exercise": "hang-clean", "reps": 1}, {"exercise": "jerk", "reps": 1,
    "notes": "same barbell throughout; no re-gripping/dropping between lifts"}],
  format_meta={"time_cap_minutes": 7, "scoring": "load"},
  tags=["open", "2021", "barbell", "max-load", "complex"],
  notes=src(2021, 4) + "; max-load complex -- athlete determines and builds their own "
        "barbell load (score is the heaviest complex completed), so there is no "
        "prescribed Rx weight; time begins immediately after 21.3")

# ---- 2020 ----
w("open-20-1", "20.1", "interval", (2020, 1),
  [{"exercise": "ground-to-overhead", "reps": 8, "load": BB("95lb", "65lb")},
   {"exercise": "bar-facing-burpee", "reps": 10}],
  format_meta=RDS(10), tags=["open", "2020", "barbell", "bodyweight"])

w("open-20-2", "20.2", "amrap", (2020, 2),
  [{"exercise": "dumbbell-thruster", "reps": 4, "load": BB("50lb", "35lb")},
   {"exercise": "toes-to-bar", "reps": 6},
   {"exercise": "double-under", "reps": 24}],
  format_meta=AMRAP(20), tags=["open", "2020", "dumbbell", "gymnastics"])

w("open-20-3", "20.3", "for_time", (2020, 3),
  [{"exercise": "deadlift", "reps": 21, "load": BB("225lb", "155lb")},
   {"exercise": "handstand-push-up", "reps": 21},
   {"exercise": "deadlift", "reps": 15, "load": BB("225lb", "155lb")},
   {"exercise": "handstand-push-up", "reps": 15},
   {"exercise": "deadlift", "reps": 9, "load": BB("225lb", "155lb")},
   {"exercise": "handstand-push-up", "reps": 9},
   {"exercise": "deadlift", "reps": 21, "load": BB("315lb", "205lb")},
   {"exercise": "handstand-walk", "distance_m": 15},
   {"exercise": "deadlift", "reps": 15, "load": BB("315lb", "205lb")},
   {"exercise": "handstand-walk", "distance_m": 15},
   {"exercise": "deadlift", "reps": 9, "load": BB("315lb", "205lb")},
   {"exercise": "handstand-walk", "distance_m": 15}],
  format_meta=CAP(9), tags=["open", "2020", "barbell", "gymnastics"])

w("open-20-4", "20.4", "for_time", (2020, 4),
  [{"exercise": "box-jump", "reps": 30},
   {"exercise": "clean-and-jerk", "reps": 15, "load": BB("95lb", "65lb")},
   {"exercise": "box-jump", "reps": 30},
   {"exercise": "clean-and-jerk", "reps": 15, "load": BB("135lb", "85lb")},
   {"exercise": "box-jump", "reps": 30},
   {"exercise": "clean-and-jerk", "reps": 10, "load": BB("185lb", "115lb")},
   {"exercise": "pistol", "reps": 30},
   {"exercise": "clean-and-jerk", "reps": 10, "load": BB("225lb", "145lb")},
   {"exercise": "pistol", "reps": 30},
   {"exercise": "clean-and-jerk", "reps": 5, "load": BB("275lb", "175lb")},
   {"exercise": "pistol", "reps": 30},
   {"exercise": "clean-and-jerk", "reps": 5, "load": BB("315lb", "205lb")}],
  format_meta=CAP(20), tags=["open", "2020", "barbell", "gymnastics"])

w("open-20-5", "20.5", "for_time", (2020, 5),
  [{"exercise": "muscle-up", "reps": 40},
   {"exercise": "row", "reps": 80, "notes": "calories"},
   {"exercise": "wall-ball-shot", "reps": 120, "load": BB("20lb", "14lb")}],
  format_meta=CAP(20), tags=["open", "2020", "gymnastics", "rowing", "any-order"],
  notes=src(2020, 5) + "; movements may be performed in any order, partitioned as desired")

# ---- 2019 ----
w("open-19-1", "19.1", "amrap", (2019, 1),
  [{"exercise": "wall-ball-shot", "reps": 19, "load": BB("20lb", "14lb")},
   {"exercise": "row", "reps": 19, "notes": "calories"}],
  format_meta=AMRAP(15), tags=["open", "2019", "rowing"])

w("open-19-2", "19.2", "multi_part", (2019, 2),
  segments=[
    {"label": "0:00-8:00", "format": "for_time", "format_meta": CAP(8),
     "movements": [{"exercise": "toes-to-bar", "reps": 25}, {"exercise": "double-under", "reps": 50},
                   {"exercise": "squat-clean", "reps": 15, "load": BB("135lb", "85lb")},
                   {"exercise": "toes-to-bar", "reps": 25}, {"exercise": "double-under", "reps": 50},
                   {"exercise": "squat-clean", "reps": 13, "load": BB("185lb", "115lb")}]},
    {"label": "If complete, +4:00 (to 12:00)", "format": "for_time", "format_meta": CAP(4),
     "movements": [{"exercise": "toes-to-bar", "reps": 25}, {"exercise": "double-under", "reps": 50},
                   {"exercise": "squat-clean", "reps": 11, "load": BB("225lb", "145lb")}]},
    {"label": "If complete, +4:00 (to 16:00)", "format": "for_time", "format_meta": CAP(4),
     "movements": [{"exercise": "toes-to-bar", "reps": 25}, {"exercise": "double-under", "reps": 50},
                   {"exercise": "squat-clean", "reps": 9, "load": BB("275lb", "175lb")}]},
    {"label": "If complete, +4:00 (to 20:00)", "format": "for_time", "format_meta": CAP(4),
     "movements": [{"exercise": "toes-to-bar", "reps": 25}, {"exercise": "double-under", "reps": 50},
                   {"exercise": "squat-clean", "reps": 7, "load": BB("315lb", "205lb")}]},
  ],
  format_meta={"total_minutes": 20, "scoring": "time"},
  tags=["open", "2019", "barbell", "gymnastics", "time-extension-ladder"])

w("open-19-3", "19.3", "for_time", (2019, 3),
  [{"exercise": "dumbbell-overhead-lunge", "distance_m": 61, "load": BB("50lb", "35lb"), "notes": "200 ft"},
   {"exercise": "dumbbell-box-step-up", "reps": 50, "load": BB("50lb", "35lb"), "notes": "24 in (men) / 20 in (women) box"},
   {"exercise": "strict-handstand-push-up", "reps": 50},
   {"exercise": "handstand-walk", "distance_m": 61, "notes": "200 ft"}],
  format_meta=CAP(10), tags=["open", "2019", "dumbbell", "gymnastics"])

w("open-19-4", "19.4", "multi_part", (2019, 4),
  segments=[
    {"label": "Part 1", "format": "interval", "format_meta": RDS(3),
     "movements": [{"exercise": "snatch", "reps": 10, "load": BB("95lb", "65lb")},
                   {"exercise": "bar-facing-burpee", "reps": 12}],
     "rest_after_seconds": 180},
    {"label": "Part 2", "format": "interval", "format_meta": RDS(3),
     "movements": [{"exercise": "bar-muscle-up", "reps": 10},
                   {"exercise": "bar-facing-burpee", "reps": 12}]},
  ],
  format_meta=CAP(12), tags=["open", "2019", "barbell", "gymnastics"])

w("open-19-5", "19.5", "for_time", (2019, 5),
  [{"exercise": "thruster", "reps": [33, 27, 21, 15, 9], "load": BB("95lb", "65lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": [33, 27, 21, 15, 9]}],
  format_meta=CAP(20), tags=["open", "2019", "barbell", "gymnastics", "ladder"])

print(f"Wrote {len([f for f in os.listdir(OUT) if f.endswith('.json')])} Open entries to {OUT}")
