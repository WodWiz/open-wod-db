import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "heroes")
os.makedirs(OUT, exist_ok=True)
VER = "1.0"
TODAY = "2026-07-08"

# Batch 1: load-free Hero WODs (bodyweight / running / rowing only). Deliberately
# excludes any WOD with a prescribed barbell/kettlebell load, since the staging CSV
# does not carry Rx weights and we won't fabricate them. Each source_notes points at
# the specific crossfit.com/benchmark page the movements/reps were verified against.
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
        "source_notes": notes or src(slug),
        "schema_version": VER,
        "last_updated": TODAY,
    }
    with open(os.path.join(OUT, f"{id}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(entry, f, indent=2)
        f.write("\n")

w("griff", "Griff", "for_time",
  [{"exercise": "run", "distance_m": 800},
   {"exercise": "run", "distance_m": 400, "notes": "run backward"},
   {"exercise": "run", "distance_m": 800},
   {"exercise": "run", "distance_m": 400, "notes": "run backward"}],
  "griff", tags=["running", "single-modality"])

w("jerry", "Jerry", "for_time",
  [{"exercise": "run", "distance_m": 1609},
   {"exercise": "row", "distance_m": 2000},
   {"exercise": "run", "distance_m": 1609}],
  "jerry", tags=["running", "rowing", "endurance"])

w("michael", "Michael", "interval",
  [{"exercise": "run", "distance_m": 800},
   {"exercise": "back-extension", "reps": 50},
   {"exercise": "sit-up", "reps": 50}],
  "michael", format_meta={"rounds": 3, "scoring": "time"},
  tags=["running", "bodyweight", "3-rounds"])

w("riley", "Riley", "for_time",
  [{"exercise": "run", "distance_m": 2414},
   {"exercise": "burpee", "reps": 150},
   {"exercise": "run", "distance_m": 2414}],
  "riley", tags=["running", "bodyweight", "high-volume", "weight-vest-optional"],
  notes=src("riley") + "; official Rx adds an optional load: 'If you've got a weight vest or body armor, wear it.'")

w("ryan", "Ryan", "interval",
  [{"exercise": "muscle-up", "reps": 7},
   {"exercise": "burpee", "reps": 21}],
  "ryan", format_meta={"rounds": 5, "scoring": "time"},
  tags=["gymnastics", "bodyweight", "5-rounds"])

w("wilmot", "Wilmot", "interval",
  [{"exercise": "air-squat", "reps": 50},
   {"exercise": "ring-dip", "reps": 25}],
  "wilmot", format_meta={"rounds": 6, "scoring": "time"},
  tags=["bodyweight", "gymnastics", "6-rounds"])

w("terry", "Terry", "for_time",
  [{"exercise": "run", "distance_m": 1609},
   {"exercise": "push-up", "reps": 100},
   {"exercise": "bear-crawl", "distance_m": 100},
   {"exercise": "run", "distance_m": 1609},
   {"exercise": "bear-crawl", "distance_m": 100},
   {"exercise": "push-up", "reps": 100},
   {"exercise": "run", "distance_m": 1609}],
  "terry", tags=["running", "bodyweight", "high-volume"])

w("hamilton", "Hamilton", "interval",
  [{"exercise": "row", "distance_m": 1000},
   {"exercise": "push-up", "reps": 50},
   {"exercise": "run", "distance_m": 1000},
   {"exercise": "pull-up", "reps": 50}],
  "hamilton", format_meta={"rounds": 3, "scoring": "time"},
  tags=["rowing", "running", "bodyweight", "3-rounds"])

w("loredo", "Loredo", "interval",
  [{"exercise": "air-squat", "reps": 24},
   {"exercise": "push-up", "reps": 24},
   {"exercise": "walking-lunge", "reps": 24, "notes": "steps"},
   {"exercise": "run", "distance_m": 400}],
  "loredo", format_meta={"rounds": 6, "scoring": "time"},
  tags=["bodyweight", "running", "6-rounds"])

w("jared", "Jared", "interval",
  [{"exercise": "run", "distance_m": 800},
   {"exercise": "pull-up", "reps": 40},
   {"exercise": "push-up", "reps": 70}],
  "jared", format_meta={"rounds": 4, "scoring": "time"},
  tags=["running", "bodyweight", "4-rounds"])

w("smykowski", "Smykowski", "for_time",
  [{"exercise": "run", "distance_m": 6000},
   {"exercise": "burpee-pull-up", "reps": 60}],
  "smykowski", tags=["running", "bodyweight", "endurance", "weight-vest-optional"],
  notes=src("smykowski") + "; official Rx adds an optional load: 'If you've got body armor or a 30-lb vest, wear it.'")

w("rocket", "Rocket", "amrap",
  [{"exercise": "swim", "distance_m": 46, "notes": "50 yards"},
   {"exercise": "push-up", "reps": 10},
   {"exercise": "air-squat", "reps": 15}],
  "rocket", format_meta={"time_cap_minutes": 30},
  tags=["swimming", "bodyweight", "amrap"])

print(f"Wrote batch-1 Hero entries; heroes dir now has {len(os.listdir(OUT))} files ({len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON).")
