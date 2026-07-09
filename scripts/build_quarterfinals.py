import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "open")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games Individual Quarterfinals (2021-2026; no Quarterfinals were held
# in 2025 -- that season went straight from the Open to Semifinals). Each
# verified against its official
# games.crossfit.com/workouts/quarterfinalsindividual/<year>/<n> page (Individual
# division specifically, not age-group/masters), both men's and women's Rx.
# Stored under data/open/ alongside Open workouts (category distinguishes them).
def src(year, n):
    return (f"games.crossfit.com/workouts/quarterfinalsindividual/{year}/{n} "
            f"(official CrossFit Games Individual Quarterfinals workout), retrieved {TODAY}")

def w(id, name, fmt, slug, movements=None, segments=None, format_meta=None, tags=None, notes=None):
    entry = {
        "id": id, "name": name, "category": "quarterfinal", "format": fmt,
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

# ---- 2021 ----
w("qf-21-1", "21.QF1", "multi_part", (2021, 1),
  segments=[
    {"label": "Part 1", "format": "interval", "format_meta": RDS(3),
     "movements": [{"exercise": "strict-handstand-push-up", "reps": 10},
                   {"exercise": "dumbbell-hang-power-clean", "reps": 10, "load": BB("50lb", "35lb")},
                   {"exercise": "double-under", "reps": 50}],
     "rest_after_seconds": 60},
    {"label": "Part 2", "format": "interval", "format_meta": RDS(3),
     "movements": [{"exercise": "handstand-push-up", "reps": 10},
                   {"exercise": "dumbbell-shoulder-to-overhead", "reps": 10, "load": BB("50lb", "35lb")},
                   {"exercise": "double-under", "reps": 50}]},
  ],
  format_meta=CAP(10), tags=["quarterfinal", "2021", "dumbbell", "gymnastics"])

w("qf-21-2", "21.QF2", "for_time", (2021, 2),
  [{"exercise": "ghd-sit-up", "reps": [60, 50, 40, 30]},
   {"exercise": "rope-climb", "reps": [6, 5, 4, 3], "notes": "to 15 feet"},
   {"exercise": "pistol", "reps": [60, 50, 40, 30], "notes": "alternating legs"}],
  format_meta=CAP(20), tags=["quarterfinal", "2021", "gymnastics", "bodyweight", "ladder"])

w("qf-21-3", "21.QF3", "for_time", (2021, 3),
  [{"exercise": "wall-ball-shot", "reps": 120, "load": BB("20lb", "14lb")},
   {"exercise": "row", "reps": 120, "notes": "calories"}],
  format_meta=CAP(15), tags=["quarterfinal", "2021", "rowing"])

w("qf-21-4", "21.QF4", "max_load", (2021, 4),
  [{"exercise": "front-squat", "reps": 4, "notes": "athlete's own 4-rep-max; no fixed Rx weight"}],
  format_meta={"time_cap_minutes": 20, "scoring": "load"},
  tags=["quarterfinal", "2021", "barbell", "max-load"])

w("qf-21-5", "21.QF5", "for_time", (2021, 5),
  [{"exercise": "snatch", "reps": [9, 6, 3], "load": BB("185lb", "135lb")},
   {"exercise": "burpee-box-jump-over", "reps": [9, 6, 3], "notes": "30 in box"}],
  format_meta=CAP(7), tags=["quarterfinal", "2021", "barbell", "bodyweight", "ladder"])

# ---- 2022 ----
w("qf-22-1", "22.QF1", "for_time", (2022, 1),
  [{"exercise": "dumbbell-walking-lunge", "reps": 50, "load": BB("50lb", "35lb"), "notes": "steps; two dumbbells"},
   {"exercise": "handstand-push-up", "reps": 30},
   {"exercise": "dumbbell-front-rack-lunge", "reps": 40, "load": BB("50lb", "35lb"), "notes": "steps; two dumbbells"},
   {"exercise": "deficit-handstand-push-up", "reps": 20, "notes": "3.5 in deficit (men) / 2 in (women)"},
   {"exercise": "dumbbell-overhead-lunge", "reps": 30, "load": BB("50lb", "35lb"), "notes": "steps; two dumbbells"},
   {"exercise": "strict-handstand-push-up", "reps": 10}],
  format_meta=CAP(15), tags=["quarterfinal", "2022", "dumbbell", "gymnastics"])

w("qf-22-2", "22.QF2", "interval", (2022, 2),
  [{"exercise": "pistol", "reps": 30, "notes": "alternating legs"},
   {"exercise": "ghd-sit-up", "reps": 30},
   {"exercise": "muscle-up", "reps": 10}],
  format_meta=RDS(3), tags=["quarterfinal", "2022", "gymnastics", "bodyweight", "3-rounds"])

w("qf-22-3", "22.QF3", "for_time", (2022, 3),
  [{"exercise": "wall-ball-shot", "reps": [8, 16, 24, 32, 24, 16, 8], "load": BB("20lb", "14lb")},
   {"exercise": "shuttle-run", "reps": [4, 8, 12, 16, 12, 8, 4], "notes": "50 ft"},
   {"exercise": "rope-climb", "reps": [1, 2, 3, 4, 3, 2, 1], "notes": "to 15 feet"}],
  format_meta=CAP(25), tags=["quarterfinal", "2022", "gymnastics", "pyramid"])

w("qf-22-4", "22.QF4", "max_load", (2022, 4),
  [{"exercise": "clean", "reps": 1}, {"exercise": "bench-press", "reps": 1},
   {"exercise": "overhead-squat", "reps": 1,
    "notes": "same barbell throughout; athlete's own max-load complex; no fixed Rx weight"}],
  format_meta={"time_cap_minutes": 30, "scoring": "load"},
  tags=["quarterfinal", "2022", "barbell", "max-load", "complex"])

w("qf-22-5", "22.QF5", "for_time", (2022, 5),
  [{"exercise": "row", "reps": 30, "notes": "calories"},
   {"exercise": "burpee-box-jump-over", "reps": 20, "notes": "20 in box"},
   {"exercise": "snatch", "reps": 10, "load": BB("185lb", "135lb")}],
  format_meta=CAP(7), tags=["quarterfinal", "2022", "barbell", "rowing"])

# ---- 2023 ----
w("qf-23-1", "23.QF1", "for_time", (2023, 1),
  [{"exercise": "front-squat", "reps": 9, "load": BB("225lb", "155lb")},
   {"exercise": "handstand-walk", "reps": 9, "distance_m": 7.6, "notes": "each rep = one 25 ft traversal"},
   {"exercise": "front-squat", "reps": 15, "load": BB("185lb", "125lb")},
   {"exercise": "muscle-up", "reps": 15},
   {"exercise": "front-squat", "reps": 21, "load": BB("135lb", "95lb")},
   {"exercise": "wall-facing-handstand-push-up", "reps": 21}],
  format_meta=CAP(15), tags=["quarterfinal", "2023", "barbell", "gymnastics"])

w("qf-23-2", "23.QF2", "amrap", (2023, 2),
  [{"exercise": "dumbbell-snatch", "reps": 8, "load": BB("70lb", "50lb"), "notes": "arm 1"},
   {"exercise": "dumbbell-overhead-lunge", "reps": 8, "load": BB("70lb", "50lb"), "notes": "steps; arm 1"},
   {"exercise": "dumbbell-snatch", "reps": 8, "load": BB("70lb", "50lb"), "notes": "arm 2"},
   {"exercise": "dumbbell-overhead-lunge", "reps": 8, "load": BB("70lb", "50lb"), "notes": "steps; arm 2"},
   {"exercise": "crossover-single-under", "reps": 40}],
  format_meta=AMRAP(12), tags=["quarterfinal", "2023", "dumbbell", "jump-rope"])

w("qf-23-3", "23.QF3", "for_time", (2023, 3),
  [{"exercise": "burpee-box-jump-over", "reps": 5, "notes": "24 in (men) / 20 in (women) box"},
   {"exercise": "clean-and-jerk", "reps": 1, "load": BB("275lb", "185lb")},
   {"exercise": "burpee-box-jump-over", "reps": 5, "notes": "24 in (men) / 20 in (women) box"},
   {"exercise": "clean-and-jerk", "reps": 2, "load": BB("275lb", "185lb")},
   {"exercise": "burpee-box-jump-over", "reps": 5, "notes": "24 in (men) / 20 in (women) box"},
   {"exercise": "clean-and-jerk", "reps": 3, "load": BB("275lb", "185lb")},
   {"exercise": "burpee-box-jump-over", "reps": 5, "notes": "24 in (men) / 20 in (women) box"},
   {"exercise": "clean-and-jerk", "reps": 4, "load": BB("275lb", "185lb")},
   {"exercise": "burpee-box-jump-over", "reps": 5, "notes": "24 in (men) / 20 in (women) box"},
   {"exercise": "clean-and-jerk", "reps": 5, "load": BB("275lb", "185lb")}],
  format_meta=CAP(10), tags=["quarterfinal", "2023", "barbell", "bodyweight", "ascending"])

w("qf-23-4", "23.QF4", "amrap", (2023, 4),
  [{"exercise": "row", "distance_m": 1000},
   {"exercise": "ghd-sit-up", "reps": 50},
   {"exercise": "row", "distance_m": 500},
   {"exercise": "v-up", "reps": 25}],
  format_meta=AMRAP(20), tags=["quarterfinal", "2023", "rowing", "gymnastics"])

w("qf-23-5", "23.QF5", "for_time", (2023, 5),
  [{"exercise": "deadlift", "reps": 21, "load": BB("225lb", "155lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": 21},
   {"exercise": "deadlift", "reps": 15, "load": BB("275lb", "185lb")},
   {"exercise": "bar-muscle-up", "reps": 15},
   {"exercise": "deadlift", "reps": 9, "load": BB("315lb", "205lb")},
   {"exercise": "rope-climb", "reps": 9, "notes": "to 15 feet"}],
  format_meta=CAP(15), tags=["quarterfinal", "2023", "barbell", "gymnastics"])

# ---- 2024 ----
w("qf-24-1", "24.QF1", "interval", (2024, 1),
  [{"exercise": "snatch", "reps": "max", "load": BB("135lb", "85lb"), "notes": "1 minute, max reps"},
   {"exercise": "row", "reps": "max", "notes": "1 minute, max reps (calories)"},
   {"exercise": "dumbbell-box-step-up", "reps": "max", "load": BB("50lb", "35lb"), "notes": "1 minute, max reps; 20 in box"}],
  format_meta={"rounds": 4, "work_seconds": 60, "rest_seconds": 60, "scoring": "reps"},
  tags=["quarterfinal", "2024", "barbell", "dumbbell", "rowing", "interval"],
  notes=src(2024, 1) + "; 4 rounds of 1 minute each of snatch, row, dumbbell box step-up, "
        "with 1 minute of rest after each round, scored by total reps across all rounds")

w("qf-24-2", "24.QF2", "interval", (2024, 2),
  [{"exercise": "wall-ball-shot", "reps": 50, "load": BB("20lb", "14lb")},
   {"exercise": "lateral-burpee", "reps": 50, "notes": "over a box; 24 in (men) / 20 in (women)"}],
  format_meta=RDS(3), tags=["quarterfinal", "2024", "bodyweight", "3-rounds"])

w("qf-24-3", "24.QF3", "for_time", (2024, 3),
  [{"exercise": "handstand-push-up", "reps": 10}, {"exercise": "toes-to-bar", "reps": 20},
   {"exercise": "handstand-push-up", "reps": 10}, {"exercise": "toes-to-bar", "reps": 20},
   {"exercise": "handstand-push-up", "reps": 10}, {"exercise": "toes-to-bar", "reps": 20},
   {"exercise": "strict-handstand-push-up", "reps": 10}, {"exercise": "rope-climb", "reps": 5, "notes": "to 15 feet"},
   {"exercise": "strict-handstand-push-up", "reps": 10}, {"exercise": "rope-climb", "reps": 5, "notes": "to 15 feet"},
   {"exercise": "wall-facing-handstand-push-up", "reps": 10}, {"exercise": "muscle-up", "reps": 20}],
  format_meta=CAP(15), tags=["quarterfinal", "2024", "gymnastics"])

w("qf-24-4", "24.QF4", "multi_part", (2024, 4),
  segments=[
    {"label": "Weight 1", "format": "for_time",
     "movements": [{"exercise": "clean-and-jerk", "reps": 10, "load": BB("135lb", "85lb")}],
     "rest_after_seconds": 60},
    {"label": "Weight 2", "format": "for_time",
     "movements": [{"exercise": "clean-and-jerk", "reps": 10, "load": BB("185lb", "125lb")}],
     "rest_after_seconds": 60},
    {"label": "Weight 3", "format": "for_time",
     "movements": [{"exercise": "clean-and-jerk", "reps": 10, "load": BB("225lb", "155lb")}],
     "rest_after_seconds": 60},
    {"label": "Weight 4 (AMRAP remainder)", "format": "amrap", "format_meta": {"scoring": "reps"},
     "movements": [{"exercise": "clean-and-jerk", "reps": "max", "load": BB("245lb", "165lb")}]},
  ],
  format_meta={"time_cap_minutes": 10, "scoring": "reps"},
  tags=["quarterfinal", "2024", "barbell"],
  notes=src(2024, 4) + "; continually running clock; scored by total reps in 10 minutes, "
        "ties broken by fastest 10th rep at the previous weight")

# ---- 2026 ----
w("qf-26-1", "26.QF1", "for_time", (2026, 1),
  [{"exercise": "shuttle-run", "reps": 10, "notes": "50 ft"},
   {"exercise": "overhead-squat", "reps": 20, "load": BB("115lb", "80lb")},
   {"exercise": "burpee-over-the-bar", "reps": 30},
   {"exercise": "burpee-over-the-bar", "reps": 30},
   {"exercise": "overhead-squat", "reps": 20, "load": BB("115lb", "80lb")},
   {"exercise": "shuttle-run", "reps": 10, "notes": "50 ft"}],
  format_meta=CAP(12), tags=["quarterfinal", "2026", "barbell", "bodyweight"],
  notes=src(2026, 1) + "; 1-minute mandatory rest between the two burpee-over-the-bar sets; score includes the rest period")

w("qf-26-2", "26.QF2", "for_time", (2026, 2),
  [{"exercise": "dumbbell-hang-squat-clean", "reps": 80, "load": BB("50lb", "35lb")},
   {"exercise": "bar-muscle-up", "reps": 40}],
  format_meta=CAP(15), tags=["quarterfinal", "2026", "dumbbell", "gymnastics"],
  notes=src(2026, 2) + "; movements may be completed in any order/partitioned as desired")

w("qf-26-3", "26.QF3", "for_time", (2026, 3),
  [{"exercise": "double-under", "reps": 50}, {"exercise": "deadlift", "reps": 10, "load": BB("225lb", "155lb")},
   {"exercise": "double-under", "reps": 50}, {"exercise": "deadlift", "reps": 10, "load": BB("225lb", "155lb")},
   {"exercise": "double-under", "reps": 50}, {"exercise": "deadlift", "reps": 10, "load": BB("225lb", "155lb")},
   {"exercise": "double-under", "reps": 50}, {"exercise": "deadlift", "reps": 10, "load": BB("275lb", "185lb")},
   {"exercise": "double-under", "reps": 50}, {"exercise": "deadlift", "reps": 10, "load": BB("275lb", "185lb")},
   {"exercise": "double-under", "reps": 50}, {"exercise": "deadlift", "reps": 10, "load": BB("315lb", "225lb")}],
  format_meta=CAP(12), tags=["quarterfinal", "2026", "barbell", "jump-rope"])

w("qf-26-4", "26.QF4", "for_time", (2026, 4),
  [{"exercise": "row", "distance_m": 1000},
   {"exercise": "clean-and-jerk", "reps": 30, "load": BB("135lb", "95lb")},
   {"exercise": "row", "distance_m": 1000},
   {"exercise": "strict-handstand-push-up", "reps": 30}],
  format_meta=CAP(20), tags=["quarterfinal", "2026", "barbell", "rowing", "gymnastics"])

print(f"Wrote quarterfinal entries; data/open now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
