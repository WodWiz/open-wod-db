import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "heroes")
os.makedirs(OUT, exist_ok=True)
VER = "1.0"
TODAY = "2026-07-09"

# Batch 2: load-bearing Hero WODs. Every prescribed weight was verified against
# the entry's official crossfit.com/benchmark page (men -> rx_male, women ->
# rx_female). Box heights (universal 24 in / 20 in) are omitted to match the
# existing entries; barbell/kettlebell loads are recorded.
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

BB = lambda m, f: {"rx_male": m, "rx_female": f}  # barbell/kettlebell load

w("bell", "Bell", "interval",
  [{"exercise": "deadlift", "reps": 21, "load": BB("185lb", "125lb")},
   {"exercise": "pull-up", "reps": 15},
   {"exercise": "front-squat", "reps": 9, "load": BB("185lb", "125lb")}],
  "bell", format_meta={"rounds": 3, "scoring": "time"},
  tags=["barbell", "gymnastics", "3-rounds"])

w("danny", "Danny", "amrap",
  [{"exercise": "box-jump", "reps": 30},
   {"exercise": "push-press", "reps": 20, "load": BB("115lb", "75lb")},
   {"exercise": "pull-up", "reps": 30}],
  "danny", format_meta={"time_cap_minutes": 20},
  tags=["amrap", "barbell", "gymnastics"])

w("jack", "Jack", "amrap",
  [{"exercise": "push-press", "reps": 10, "load": BB("115lb", "75lb")},
   {"exercise": "kettlebell-swing", "reps": 10, "load": BB("1.5 pood", "1 pood")},
   {"exercise": "box-jump", "reps": 10}],
  "jack", format_meta={"time_cap_minutes": 20},
  tags=["amrap", "barbell", "kettlebell"])

w("jennifer", "Jennifer", "amrap",
  [{"exercise": "pull-up", "reps": 10},
   {"exercise": "kettlebell-swing", "reps": 15, "load": BB("53lb", "35lb")},
   {"exercise": "box-jump", "reps": 20}],
  "jennifer", format_meta={"time_cap_minutes": 26},
  tags=["amrap", "kettlebell", "gymnastics"])

w("manion", "Manion", "interval",
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "back-squat", "reps": 29, "load": BB("135lb", "95lb")}],
  "manion", format_meta={"rounds": 7, "scoring": "time"},
  tags=["running", "barbell", "7-rounds"])

w("coe", "Coe", "interval",
  [{"exercise": "thruster", "reps": 10, "load": BB("95lb", "65lb")},
   {"exercise": "ring-push-up", "reps": 10}],
  "coe", format_meta={"rounds": 10, "scoring": "time"},
  tags=["barbell", "gymnastics", "10-rounds"])

w("roy", "Roy", "interval",
  [{"exercise": "deadlift", "reps": 15, "load": BB("225lb", "155lb")},
   {"exercise": "box-jump", "reps": 20},
   {"exercise": "pull-up", "reps": 25}],
  "roy", format_meta={"rounds": 5, "scoring": "time"},
  tags=["barbell", "gymnastics", "5-rounds"])

w("mcghee", "McGhee", "amrap",
  [{"exercise": "deadlift", "reps": 5, "load": BB("275lb", "185lb")},
   {"exercise": "push-up", "reps": 13},
   {"exercise": "box-jump", "reps": 9}],
  "mcghee", format_meta={"time_cap_minutes": 30},
  tags=["amrap", "barbell", "bodyweight"])

w("marco", "Marco", "interval",
  [{"exercise": "pull-up", "reps": 21},
   {"exercise": "handstand-push-up", "reps": 15},
   {"exercise": "thruster", "reps": 9, "load": BB("135lb", "95lb")}],
  "marco", format_meta={"rounds": 3, "scoring": "time"},
  tags=["gymnastics", "barbell", "3-rounds"])

w("jenny", "Jenny", "amrap",
  [{"exercise": "overhead-squat", "reps": 20, "load": BB("45lb", "35lb")},
   {"exercise": "back-squat", "reps": 20, "load": BB("45lb", "35lb")},
   {"exercise": "run", "distance_m": 400}],
  "jenny", format_meta={"time_cap_minutes": 20},
  tags=["amrap", "barbell", "running"])

w("zembiec", "Zembiec", "interval",
  [{"exercise": "back-squat", "reps": 11, "load": BB("185lb", "125lb")},
   {"exercise": "burpee-pull-up", "reps": 7,
    "notes": "strict: strict push-up, then strict pull-up on a bar ~12 in above max standing reach"},
   {"exercise": "run", "distance_m": 400}],
  "zembiec", format_meta={"rounds": 5, "scoring": "time"},
  tags=["barbell", "gymnastics", "5-rounds"])

w("bradshaw", "Bradshaw", "interval",
  [{"exercise": "handstand-push-up", "reps": 3},
   {"exercise": "deadlift", "reps": 6, "load": BB("225lb", "155lb")},
   {"exercise": "pull-up", "reps": 12},
   {"exercise": "double-under", "reps": 24}],
  "bradshaw", format_meta={"rounds": 10, "scoring": "time"},
  tags=["barbell", "gymnastics", "10-rounds"])

print(f"Wrote batch-2 Hero entries; heroes dir now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
