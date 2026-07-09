import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "open")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Open -- wave 3 (2016-2018). Each verified against its official
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
AMRAP = lambda n, s="rounds_reps": {"time_cap_minutes": n, "scoring": s}
RDS = lambda n: {"rounds": n, "scoring": "time"}

# ---- 2018 ----
w("open-18-1", "18.1", "amrap", (2018, 1),
  [{"exercise": "toes-to-bar", "reps": 8},
   {"exercise": "dumbbell-hang-clean-and-jerk", "reps": 10, "load": BB("50lb", "35lb")},
   {"exercise": "row", "reps": 14, "notes": "calories; 12 for women"}],
  format_meta=AMRAP(20), tags=["open", "2018", "dumbbell", "rowing", "gymnastics"])

w("open-18-2", "18.2", "multi_part", (2018, 2),
  segments=[
    {"label": "18.2", "format": "for_time",
     "movements": [{"exercise": "dumbbell-front-rack-squat", "reps": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "load": BB("50lb", "35lb")},
                   {"exercise": "bar-facing-burpee", "reps": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}],
     "scoring": "reps"},
    {"label": "18.2a", "format": "max_load",
     "movements": [{"exercise": "clean", "reps": 1,
                    "notes": "athlete's own 1-rep-max; power, squat, or split clean allowed; barbell with collars, no fixed Rx weight"}],
     "scoring": "load"},
  ],
  format_meta={"time_cap_minutes": 12},
  tags=["open", "2018", "dumbbell", "barbell", "max-load"],
  notes=src(2018, 2) + "; 18.2 (ascending ladder, scored by reps/time) and 18.2a "
        "(1-rep-max clean, scored by load) share one 12-minute clock and are scored separately")

w("open-18-3", "18.3", "interval", (2018, 3),
  [{"exercise": "double-under", "reps": 100},
   {"exercise": "overhead-squat", "reps": 20, "load": BB("115lb", "80lb")},
   {"exercise": "double-under", "reps": 100},
   {"exercise": "ring-muscle-up", "reps": 12},
   {"exercise": "double-under", "reps": 100},
   {"exercise": "dumbbell-snatch", "reps": 20, "load": BB("50lb", "35lb")},
   {"exercise": "double-under", "reps": 100},
   {"exercise": "bar-muscle-up", "reps": 12}],
  format_meta={"rounds": 2, "time_cap_minutes": 14, "scoring": "time"},
  tags=["open", "2018", "barbell", "dumbbell", "gymnastics", "jump-rope"])

w("open-18-4", "18.4", "for_time", (2018, 4),
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
  format_meta=CAP(9), tags=["open", "2018", "barbell", "gymnastics"])

w("open-18-5", "18.5", "amrap", (2018, 5),
  [{"exercise": "thruster", "reps": [3, 6, 9, 12, 15, 18], "load": BB("100lb", "65lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": [3, 6, 9, 12, 15, 18]}],
  format_meta=AMRAP(7, "reps"),
  tags=["open", "2018", "barbell", "gymnastics", "ascending"],
  notes=src(2018, 5) + "; ascending ladder (+3 reps each round) continues indefinitely until the 7-minute cap")

# ---- 2017 ----
w("open-17-1", "17.1", "for_time", (2017, 1),
  [{"exercise": "dumbbell-snatch", "reps": [10, 20, 30, 40, 50], "load": BB("50lb", "35lb")},
   {"exercise": "burpee-box-jump-over", "reps": 15, "notes": "24 in (men) / 20 in (women) box; repeated between each snatch set"}],
  format_meta=CAP(20), tags=["open", "2017", "dumbbell", "bodyweight"])

w("open-17-2", "17.2", "amrap", (2017, 2),
  [{"exercise": "dumbbell-walking-lunge", "distance_m": 15, "load": BB("50lb", "35lb"), "notes": "50 ft"},
   {"exercise": "toes-to-bar", "reps": 16},
   {"exercise": "power-clean", "reps": 8},
   {"exercise": "dumbbell-walking-lunge", "distance_m": 15, "load": BB("50lb", "35lb"), "notes": "50 ft"},
   {"exercise": "bar-muscle-up", "reps": 16},
   {"exercise": "power-clean", "reps": 8}],
  format_meta=AMRAP(12), tags=["open", "2017", "dumbbell", "barbell", "gymnastics"],
  notes=src(2017, 2) + "; alternates toes-to-bar and bar-muscle-ups every other round; power clean load increases with each pass (per official movement standards)")

w("open-17-3", "17.3", "multi_part", (2017, 3),
  segments=[
    {"label": "0:00-8:00 (Round Set 1)", "format": "interval", "format_meta": RDS(3),
     "movements": [{"exercise": "chest-to-bar-pull-up", "reps": 6},
                   {"exercise": "squat-snatch", "reps": 6, "load": BB("95lb", "65lb")}]},
    {"label": "0:00-8:00 (Round Set 2)", "format": "interval", "format_meta": RDS(3),
     "movements": [{"exercise": "chest-to-bar-pull-up", "reps": 7},
                   {"exercise": "squat-snatch", "reps": 5, "load": BB("135lb", "95lb")}]},
    {"label": "If complete, continue to 12:00", "format": "interval", "format_meta": RDS(3),
     "movements": [{"exercise": "chest-to-bar-pull-up", "reps": 8},
                   {"exercise": "squat-snatch", "reps": 4, "load": BB("185lb", "135lb")}]},
    {"label": "If complete, continue to 16:00", "format": "interval", "format_meta": RDS(3),
     "movements": [{"exercise": "chest-to-bar-pull-up", "reps": 9},
                   {"exercise": "squat-snatch", "reps": 3, "load": BB("225lb", "155lb")}]},
    {"label": "If complete, continue to 20:00", "format": "interval", "format_meta": RDS(3),
     "movements": [{"exercise": "chest-to-bar-pull-up", "reps": 10},
                   {"exercise": "squat-snatch", "reps": 2, "load": BB("245lb", "175lb")}]},
    {"label": "If complete, continue to 24:00", "format": "interval", "format_meta": RDS(3),
     "movements": [{"exercise": "chest-to-bar-pull-up", "reps": 11},
                   {"exercise": "squat-snatch", "reps": 1, "load": BB("265lb", "185lb")}]},
  ],
  format_meta={"total_minutes": 24, "scoring": "time"},
  tags=["open", "2017", "barbell", "gymnastics", "time-extension-ladder"])

w("open-17-4", "17.4", "amrap", (2017, 4),
  [{"exercise": "deadlift", "reps": 55, "load": BB("225lb", "155lb")},
   {"exercise": "wall-ball-shot", "reps": 55, "load": BB("20lb", "14lb")},
   {"exercise": "row", "reps": 55, "notes": "calories"},
   {"exercise": "handstand-push-up", "reps": 55}],
  format_meta=AMRAP(13), tags=["open", "2017", "barbell", "rowing", "gymnastics"])

w("open-17-5", "17.5", "interval", (2017, 5),
  [{"exercise": "thruster", "reps": 9, "load": BB("95lb", "65lb")},
   {"exercise": "double-under", "reps": 35}],
  format_meta={"rounds": 10, "time_cap_minutes": 40, "scoring": "time"},
  tags=["open", "2017", "barbell", "jump-rope", "10-rounds"])

# ---- 2016 ----
w("open-16-1", "16.1", "amrap", (2016, 1),
  [{"exercise": "overhead-walking-lunge", "distance_m": 8, "load": BB("95lb", "65lb"), "notes": "25 ft"},
   {"exercise": "burpee", "reps": 8},
   {"exercise": "overhead-walking-lunge", "distance_m": 8, "load": BB("95lb", "65lb"), "notes": "25 ft"},
   {"exercise": "chest-to-bar-pull-up", "reps": 8}],
  format_meta=AMRAP(20), tags=["open", "2016", "barbell", "bodyweight", "gymnastics"])

w("open-16-2", "16.2", "multi_part", (2016, 2),
  segments=[
    {"label": "0:00-4:00", "format": "for_time", "format_meta": CAP(4),
     "movements": [{"exercise": "toes-to-bar", "reps": 25}, {"exercise": "double-under", "reps": 50},
                   {"exercise": "squat-clean", "reps": 15, "load": BB("135lb", "85lb")}]},
    {"label": "If complete, +4:00 (to 8:00)", "format": "for_time", "format_meta": CAP(4),
     "movements": [{"exercise": "toes-to-bar", "reps": 25}, {"exercise": "double-under", "reps": 50},
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
  tags=["open", "2016", "barbell", "gymnastics", "time-extension-ladder"])

w("open-16-3", "16.3", "amrap", (2016, 3),
  [{"exercise": "power-snatch", "reps": 10, "load": BB("75lb", "55lb")},
   {"exercise": "bar-muscle-up", "reps": 3}],
  format_meta=AMRAP(7), tags=["open", "2016", "barbell", "gymnastics"])

w("open-16-4", "16.4", "amrap", (2016, 4),
  [{"exercise": "deadlift", "reps": 55, "load": BB("225lb", "155lb")},
   {"exercise": "wall-ball-shot", "reps": 55, "load": BB("20lb", "14lb")},
   {"exercise": "row", "reps": 55, "notes": "calories"},
   {"exercise": "handstand-push-up", "reps": 55}],
  format_meta=AMRAP(13), tags=["open", "2016", "barbell", "rowing", "gymnastics"])

w("open-16-5", "16.5", "for_time", (2016, 5),
  [{"exercise": "thruster", "reps": [21, 18, 15, 12, 9, 6, 3], "load": BB("95lb", "65lb")},
   {"exercise": "burpee", "reps": [21, 18, 15, 12, 9, 6, 3]}],
  tags=["open", "2016", "barbell", "bodyweight", "ladder"])

print(f"Wrote {len([f for f in os.listdir(OUT) if f.endswith('.json')])} Open entries to {OUT}")
