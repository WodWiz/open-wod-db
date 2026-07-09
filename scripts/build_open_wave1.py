import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "open")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Open — wave 1 (2022-2026). Each verified against its official
# games.crossfit.com/workouts/open/<year>/<n> page (both men's and women's Rx).
# Multi-part workouts (24.3, 23.2, 23.3, 26.3) use format "multi_part" + segments.
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

# ---- 2024 ----
w("open-24-1", "24.1", "for_time", (2024, 1),
  [{"exercise": "dumbbell-snatch", "reps": [21, 15, 9], "load": BB("50lb", "35lb"), "notes": "arm 1"},
   {"exercise": "burpee-over-dumbbell", "reps": [21, 15, 9], "notes": "lateral"},
   {"exercise": "dumbbell-snatch", "reps": [21, 15, 9], "load": BB("50lb", "35lb"), "notes": "arm 2"},
   {"exercise": "burpee-over-dumbbell", "reps": [21, 15, 9], "notes": "lateral"}],
  format_meta=CAP(15), tags=["open", "2024", "dumbbell", "ladder"])

w("open-24-2", "24.2", "amrap", (2024, 2),
  [{"exercise": "row", "distance_m": 300},
   {"exercise": "deadlift", "reps": 10, "load": BB("185lb", "125lb")},
   {"exercise": "double-under", "reps": 50}],
  format_meta=AMRAP(20), tags=["open", "2024", "rowing", "barbell"])

w("open-24-3", "24.3", "multi_part", (2024, 3),
  segments=[
    {"label": "Part 1", "format": "interval", "format_meta": RDS(5),
     "movements": [{"exercise": "thruster", "reps": 10, "load": BB("95lb", "65lb")},
                   {"exercise": "chest-to-bar-pull-up", "reps": 10}],
     "rest_after_seconds": 60},
    {"label": "Part 2", "format": "interval", "format_meta": RDS(5),
     "movements": [{"exercise": "thruster", "reps": 7, "load": BB("135lb", "95lb")},
                   {"exercise": "bar-muscle-up", "reps": 7}]},
  ],
  format_meta=CAP(15), tags=["open", "2024", "barbell", "gymnastics"])

# ---- 2025 ----
w("open-25-1", "25.1", "amrap", (2025, 1),
  [{"exercise": "burpee-over-dumbbell", "reps": 3, "notes": "lateral; ascending +3 reps each round"},
   {"exercise": "dumbbell-hang-clean-to-overhead", "reps": 3, "load": BB("50lb", "35lb"), "notes": "ascending +3 reps each round"},
   {"exercise": "walking-lunge", "distance_m": 9, "notes": "30 ft (2 x 15 ft)"}],
  format_meta=AMRAP(15, "reps"), tags=["open", "2025", "dumbbell", "ascending"])

w("open-25-2", "25.2", "for_time", (2025, 2),
  [{"exercise": "pull-up", "reps": 21}, {"exercise": "double-under", "reps": 42},
   {"exercise": "thruster", "reps": 21, "load": BB("95lb", "65lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": 18}, {"exercise": "double-under", "reps": 36},
   {"exercise": "thruster", "reps": 18, "load": BB("115lb", "75lb")},
   {"exercise": "bar-muscle-up", "reps": 15}, {"exercise": "double-under", "reps": 30},
   {"exercise": "thruster", "reps": 15, "load": BB("135lb", "85lb")}],
  format_meta=CAP(12), tags=["open", "2025", "barbell", "gymnastics"])

w("open-25-3", "25.3", "for_time", (2025, 3),
  [{"exercise": "wall-climb", "reps": 5}, {"exercise": "row", "reps": 50, "notes": "calories"},
   {"exercise": "wall-climb", "reps": 5}, {"exercise": "deadlift", "reps": 25, "load": BB("225lb", "155lb")},
   {"exercise": "wall-climb", "reps": 5}, {"exercise": "clean", "reps": 25, "load": BB("135lb", "85lb")},
   {"exercise": "wall-climb", "reps": 5}, {"exercise": "snatch", "reps": 25, "load": BB("95lb", "65lb")},
   {"exercise": "wall-climb", "reps": 5}, {"exercise": "row", "reps": 50, "notes": "calories"}],
  format_meta=CAP(20), tags=["open", "2025", "barbell", "gymnastics"])

# ---- 2026 ----
w("open-26-1", "26.1", "for_time", (2026, 1),
  [{"exercise": "wall-ball-shot", "reps": 20, "load": BB("20lb", "14lb")},
   {"exercise": "box-jump-over", "reps": 18},
   {"exercise": "wall-ball-shot", "reps": 30, "load": BB("20lb", "14lb")},
   {"exercise": "box-jump-over", "reps": 18},
   {"exercise": "wall-ball-shot", "reps": 40, "load": BB("20lb", "14lb")},
   {"exercise": "medicine-ball-box-step-over", "reps": 18, "load": BB("20lb", "14lb")},
   {"exercise": "wall-ball-shot", "reps": 66, "load": BB("20lb", "14lb")},
   {"exercise": "medicine-ball-box-step-over", "reps": 18, "load": BB("20lb", "14lb")},
   {"exercise": "wall-ball-shot", "reps": 40, "load": BB("20lb", "14lb")},
   {"exercise": "box-jump-over", "reps": 18},
   {"exercise": "wall-ball-shot", "reps": 30, "load": BB("20lb", "14lb")},
   {"exercise": "box-jump-over", "reps": 18},
   {"exercise": "wall-ball-shot", "reps": 20, "load": BB("20lb", "14lb")}],
  format_meta=CAP(12), tags=["open", "2026", "medicine-ball"])

w("open-26-2", "26.2", "for_time", (2026, 2),
  [{"exercise": "dumbbell-overhead-lunge", "distance_m": 24, "load": BB("50lb", "35lb"), "notes": "80 ft"},
   {"exercise": "alternating-dumbbell-snatch", "reps": 20, "load": BB("50lb", "35lb")},
   {"exercise": "pull-up", "reps": 20},
   {"exercise": "dumbbell-overhead-lunge", "distance_m": 24, "load": BB("50lb", "35lb"), "notes": "80 ft"},
   {"exercise": "alternating-dumbbell-snatch", "reps": 20, "load": BB("50lb", "35lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": 20},
   {"exercise": "dumbbell-overhead-lunge", "distance_m": 24, "load": BB("50lb", "35lb"), "notes": "80 ft"},
   {"exercise": "alternating-dumbbell-snatch", "reps": 20, "load": BB("50lb", "35lb")},
   {"exercise": "muscle-up", "reps": 20}],
  format_meta=CAP(15), tags=["open", "2026", "dumbbell", "gymnastics"])

w("open-26-3", "26.3", "multi_part", (2026, 3),
  segments=[
    {"label": "Weight 1", "format": "interval", "format_meta": RDS(2),
     "movements": [{"exercise": "burpee-over-the-bar", "reps": 12},
                   {"exercise": "clean", "reps": 12, "load": BB("95lb", "65lb")},
                   {"exercise": "burpee-over-the-bar", "reps": 12},
                   {"exercise": "thruster", "reps": 12, "load": BB("95lb", "65lb")}]},
    {"label": "Weight 2", "format": "interval", "format_meta": RDS(2),
     "movements": [{"exercise": "burpee-over-the-bar", "reps": 12},
                   {"exercise": "clean", "reps": 12, "load": BB("115lb", "75lb")},
                   {"exercise": "burpee-over-the-bar", "reps": 12},
                   {"exercise": "thruster", "reps": 12, "load": BB("115lb", "75lb")}]},
    {"label": "Weight 3", "format": "interval", "format_meta": RDS(2),
     "movements": [{"exercise": "burpee-over-the-bar", "reps": 12},
                   {"exercise": "clean", "reps": 12, "load": BB("135lb", "85lb")},
                   {"exercise": "burpee-over-the-bar", "reps": 12},
                   {"exercise": "thruster", "reps": 12, "load": BB("135lb", "85lb")}]},
  ],
  format_meta=CAP(16), tags=["open", "2026", "barbell"])

# ---- 2023 ----
w("open-23-1", "23.1", "for_time", (2023, 1),
  [{"exercise": "row", "reps": 60, "notes": "calories"},
   {"exercise": "toes-to-bar", "reps": 50},
   {"exercise": "wall-ball-shot", "reps": 40, "load": BB("20lb", "14lb")},
   {"exercise": "clean", "reps": 30, "load": BB("135lb", "95lb")},
   {"exercise": "muscle-up", "reps": 20}],
  format_meta=CAP(14), tags=["open", "2023", "barbell", "gymnastics"])

w("open-23-2", "23.2", "multi_part", (2023, 2),
  segments=[
    {"label": "23.2A", "format": "amrap", "format_meta": AMRAP(15, "reps"),
     "movements": [{"exercise": "burpee-pull-up", "reps": 5, "notes": "ascending +5 reps each round"},
                   {"exercise": "shuttle-run", "reps": 10, "notes": "1 rep = 25 ft down + 25 ft back"}],
     "scoring": "reps"},
    {"label": "23.2B", "format": "max_load", "format_meta": {"time_cap_minutes": 5, "scoring": "load"},
     "movements": [{"exercise": "thruster", "reps": 1, "notes": "1-rep-max from the floor"}],
     "scoring": "load"},
  ],
  tags=["open", "2023", "barbell", "gymnastics"])

w("open-23-3", "23.3", "multi_part", (2023, 3),
  segments=[
    {"label": "0:00-6:00", "format": "for_time", "format_meta": CAP(6),
     "movements": [{"exercise": "wall-climb", "reps": 5}, {"exercise": "double-under", "reps": 50},
                   {"exercise": "snatch", "reps": 15, "load": BB("95lb", "65lb")},
                   {"exercise": "wall-climb", "reps": 5}, {"exercise": "double-under", "reps": 50},
                   {"exercise": "snatch", "reps": 12, "load": BB("135lb", "95lb")}]},
    {"label": "If complete, +3:00", "format": "for_time", "format_meta": CAP(3),
     "movements": [{"exercise": "strict-handstand-push-up", "reps": 20}, {"exercise": "double-under", "reps": 50},
                   {"exercise": "snatch", "reps": 9, "load": BB("185lb", "125lb")}]},
    {"label": "If complete, +3:00", "format": "for_time", "format_meta": CAP(3),
     "movements": [{"exercise": "strict-handstand-push-up", "reps": 20}, {"exercise": "double-under", "reps": 50},
                   {"exercise": "snatch", "reps": 6, "load": BB("225lb", "155lb")}]},
  ],
  format_meta={"total_minutes": 12, "scoring": "time"}, tags=["open", "2023", "barbell", "gymnastics"])

# ---- 2022 ----
w("open-22-1", "22.1", "amrap", (2022, 1),
  [{"exercise": "wall-climb", "reps": 3},
   {"exercise": "dumbbell-snatch", "reps": 12, "load": BB("50lb", "35lb")},
   {"exercise": "box-jump-over", "reps": 15}],
  format_meta=AMRAP(15), tags=["open", "2022", "dumbbell", "gymnastics"])

w("open-22-2", "22.2", "for_time", (2022, 2),
  [{"exercise": "deadlift", "reps": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1], "load": BB("225lb", "155lb")},
   {"exercise": "bar-facing-burpee", "reps": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]}],
  format_meta=CAP(10), tags=["open", "2022", "barbell", "ladder"])

w("open-22-3", "22.3", "for_time", (2022, 3),
  [{"exercise": "pull-up", "reps": 21}, {"exercise": "double-under", "reps": 42},
   {"exercise": "thruster", "reps": 21, "load": BB("95lb", "65lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": 18}, {"exercise": "double-under", "reps": 36},
   {"exercise": "thruster", "reps": 18, "load": BB("115lb", "75lb")},
   {"exercise": "bar-muscle-up", "reps": 15}, {"exercise": "double-under", "reps": 30},
   {"exercise": "thruster", "reps": 15, "load": BB("135lb", "85lb")}],
  format_meta=CAP(12), tags=["open", "2022", "barbell", "gymnastics"])

print(f"Wrote {len([f for f in os.listdir(OUT) if f.endswith('.json')])} Open entries to {OUT}")
