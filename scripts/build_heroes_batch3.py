import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "heroes")
os.makedirs(OUT, exist_ok=True)
VER = "1.0"
TODAY = "2026-07-09"

# Batch 3: 24 Hero WODs, each verified against its official crossfit.com/benchmark
# page (men -> rx_male, women -> rx_female). Prescribed weight vests are recorded
# in source_notes + a "weight-vest" tag (the schema has no vest field yet). Box
# heights (standard) are omitted, matching existing entries.
VEST = "; official Rx includes a 20 lb (men) / 14 lb (women) weight vest"

def src(slug):
    return f"crossfit.com/benchmark/{slug} (official CrossFit Hero WOD page), retrieved {TODAY}"

def w(id, name, format, movements, slug, format_meta=None, tags=None, notes=None):
    entry = {
        "id": id, "name": name, "category": "hero", "format": format,
        "format_meta": format_meta or {},
        "movements": movements,
        "partition": None,
        "scaling": None,
        "origin": None,
        "tags": tags or [],
        "description": DESCRIPTIONS.get(id),
        "source_notes": notes or src(slug),
        "schema_version": VER,
        "last_updated": TODAY,
    }
    with open(os.path.join(OUT, f"{id}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(entry, f, indent=2)
        f.write("\n")

BB = lambda m, f: {"rx_male": m, "rx_female": f}
RDS = lambda n: {"rounds": n, "scoring": "time"}
AMRAP = lambda n: {"time_cap_minutes": n}

w("abbate", "Abbate", "for_time",
  [{"exercise": "run", "distance_m": 1609},
   {"exercise": "clean-and-jerk", "reps": 21, "load": BB("155lb", "105lb")},
   {"exercise": "run", "distance_m": 800},
   {"exercise": "clean-and-jerk", "reps": 21, "load": BB("155lb", "105lb")},
   {"exercise": "run", "distance_m": 1609}],
  "abbate", tags=["running", "barbell"])

w("alexander", "Alexander", "interval",
  [{"exercise": "back-squat", "reps": 31, "load": BB("135lb", "95lb")},
   {"exercise": "power-clean", "reps": 12, "load": BB("185lb", "125lb")}],
  "alexander", format_meta=RDS(5), tags=["barbell", "5-rounds"])

w("andy", "Andy", "for_time",
  [{"exercise": "thruster", "reps": 25, "load": BB("115lb", "75lb")},
   {"exercise": "box-jump", "reps": 50},
   {"exercise": "deadlift", "reps": 75, "load": BB("115lb", "75lb")},
   {"exercise": "run", "distance_m": 2414},
   {"exercise": "deadlift", "reps": 75, "load": BB("115lb", "75lb")},
   {"exercise": "box-jump", "reps": 50},
   {"exercise": "thruster", "reps": 25, "load": BB("115lb", "75lb")}],
  "andy", tags=["barbell", "running", "weight-vest", "high-volume"],
  notes=src("andy") + VEST)

w("brian", "Brian", "interval",
  [{"exercise": "rope-climb", "reps": 5, "notes": "to 15 feet"},
   {"exercise": "back-squat", "reps": 25, "load": BB("185lb", "125lb")}],
  "brian", format_meta=RDS(3), tags=["barbell", "gymnastics", "3-rounds"])

w("bruck", "Bruck", "interval",
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "back-squat", "reps": 24, "load": BB("185lb", "125lb")},
   {"exercise": "jerk", "reps": 24, "load": BB("135lb", "95lb")}],
  "bruck", format_meta=RDS(4), tags=["running", "barbell", "4-rounds"])

w("bulger", "Bulger", "interval",
  [{"exercise": "run", "distance_m": 150},
   {"exercise": "chest-to-bar-pull-up", "reps": 7},
   {"exercise": "front-squat", "reps": 7, "load": BB("135lb", "95lb")},
   {"exercise": "handstand-push-up", "reps": 7}],
  "bulger", format_meta=RDS(10), tags=["running", "barbell", "gymnastics", "10-rounds"])

w("bull", "Bull", "interval",
  [{"exercise": "double-under", "reps": 200},
   {"exercise": "overhead-squat", "reps": 50, "load": BB("135lb", "95lb")},
   {"exercise": "pull-up", "reps": 50},
   {"exercise": "run", "distance_m": 1609}],
  "bull", format_meta=RDS(2), tags=["barbell", "gymnastics", "running", "2-rounds"])

w("desforges", "Desforges", "interval",
  [{"exercise": "deadlift", "reps": 12, "load": BB("225lb", "155lb")},
   {"exercise": "pull-up", "reps": 20},
   {"exercise": "clean-and-jerk", "reps": 12, "load": BB("135lb", "95lb")},
   {"exercise": "knees-to-elbows", "reps": 20}],
  "desforges", format_meta=RDS(5), tags=["barbell", "gymnastics", "5-rounds"])

w("gator", "Gator", "interval",
  [{"exercise": "front-squat", "reps": 5, "load": BB("185lb", "125lb")},
   {"exercise": "ring-push-up", "reps": 26}],
  "gator", format_meta=RDS(8), tags=["barbell", "gymnastics", "8-rounds"])

w("gaza", "Gaza", "interval",
  [{"exercise": "kettlebell-swing", "reps": 35, "load": BB("53lb", "35lb")},
   {"exercise": "push-up", "reps": 30},
   {"exercise": "pull-up", "reps": 25},
   {"exercise": "box-jump", "reps": 20},
   {"exercise": "run", "distance_m": 1609}],
  "gaza", format_meta=RDS(5), tags=["kettlebell", "bodyweight", "running", "5-rounds"])

w("glen", "Glen", "for_time",
  [{"exercise": "clean-and-jerk", "reps": 30, "load": BB("135lb", "95lb")},
   {"exercise": "run", "distance_m": 1609},
   {"exercise": "rope-climb", "reps": 10, "notes": "to 15 feet"},
   {"exercise": "run", "distance_m": 1609},
   {"exercise": "burpee", "reps": 100}],
  "glen", tags=["barbell", "running", "gymnastics"])

w("johnson", "Johnson", "amrap",
  [{"exercise": "deadlift", "reps": 9, "load": BB("245lb", "165lb")},
   {"exercise": "muscle-up", "reps": 8},
   {"exercise": "squat-clean", "reps": 9, "load": BB("155lb", "105lb")}],
  "johnson", format_meta=AMRAP(20), tags=["amrap", "barbell", "gymnastics"])

w("justin", "Justin", "for_time",
  [{"exercise": "back-squat", "reps": [30, 20, 10]},
   {"exercise": "bench-press", "reps": [30, 20, 10]},
   {"exercise": "strict-pull-up", "reps": [30, 20, 10]}],
  "justin", tags=["barbell", "gymnastics", "ladder"],
  notes=src("justin") + "; official page lists no barbell load for back squat/bench "
        "press (conventionally performed at bodyweight)")

w("larry", "Larry", "for_time",
  [{"exercise": "front-squat", "reps": [21, 18, 15, 12, 9, 6, 3], "load": BB("115lb", "75lb")},
   {"exercise": "bar-facing-burpee", "reps": [21, 18, 15, 12, 9, 6, 3]}],
  "larry", tags=["barbell", "ladder"])

w("ned", "Ned", "interval",
  [{"exercise": "back-squat", "reps": 11, "notes": "bodyweight"},
   {"exercise": "row", "distance_m": 1000}],
  "ned", format_meta=RDS(7), tags=["barbell", "rowing", "7-rounds"])

w("rankel", "Rankel", "amrap",
  [{"exercise": "deadlift", "reps": 6, "load": BB("225lb", "155lb")},
   {"exercise": "burpee-pull-up", "reps": 7},
   {"exercise": "kettlebell-swing", "reps": 10, "load": BB("70lb", "53lb")},
   {"exercise": "run", "distance_m": 200}],
  "rankel", format_meta=AMRAP(20), tags=["amrap", "barbell", "kettlebell"])

w("sean", "Sean", "interval",
  [{"exercise": "chest-to-bar-pull-up", "reps": 11},
   {"exercise": "front-squat", "reps": 22, "load": BB("75lb", "55lb")}],
  "sean", format_meta=RDS(10), tags=["gymnastics", "barbell", "10-rounds"])

w("sham", "Sham", "interval",
  [{"exercise": "deadlift", "reps": 11, "notes": "bodyweight"},
   {"exercise": "run", "distance_m": 100, "notes": "sprint"}],
  "sham", format_meta=RDS(7), tags=["barbell", "running", "7-rounds"])

w("tyler", "Tyler", "interval",
  [{"exercise": "muscle-up", "reps": 7},
   {"exercise": "sumo-deadlift-high-pull", "reps": 21, "load": BB("95lb", "65lb")}],
  "tyler", format_meta=RDS(5), tags=["gymnastics", "barbell", "5-rounds"])

w("adrian", "Adrian", "interval",
  [{"exercise": "forward-roll", "reps": 3},
   {"exercise": "wall-climb", "reps": 5},
   {"exercise": "toes-to-bar", "reps": 7},
   {"exercise": "box-jump", "reps": 9}],
  "adrian", format_meta=RDS(7), tags=["gymnastics", "bodyweight", "7-rounds"])

w("rene", "René", "interval",
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "walking-lunge", "reps": 21, "notes": "steps"},
   {"exercise": "pull-up", "reps": 15},
   {"exercise": "burpee", "reps": 9}],
  "rene", format_meta=RDS(7), tags=["running", "bodyweight", "weight-vest", "7-rounds"],
  notes=src("rene") + VEST)

w("rj", "RJ", "interval",
  [{"exercise": "run", "distance_m": 800},
   {"exercise": "rope-climb", "reps": 5, "notes": "to 15 feet"},
   {"exercise": "push-up", "reps": 50}],
  "rj", format_meta=RDS(5), tags=["running", "gymnastics", "bodyweight", "5-rounds"])

w("sisson", "Sisson", "amrap",
  [{"exercise": "rope-climb", "reps": 1, "notes": "to 15 feet"},
   {"exercise": "burpee", "reps": 5},
   {"exercise": "run", "distance_m": 200}],
  "sisson", format_meta=AMRAP(20), tags=["amrap", "gymnastics", "weight-vest"],
  notes=src("sisson") + VEST)

w("taylor", "Taylor", "interval",
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "burpee-muscle-up", "reps": 5}],
  "taylor", format_meta=RDS(4), tags=["running", "gymnastics", "weight-vest", "4-rounds"],
  notes=src("taylor") + VEST)

print(f"Wrote batch-3 Hero entries; heroes dir now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
