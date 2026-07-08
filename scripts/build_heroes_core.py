import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "heroes")
os.makedirs(OUT, exist_ok=True)
SRC = "crossfit.com/heroes (official CrossFit Hero and Tribute Workouts page), retrieved 2026-07-08"
VER = "1.0"
TODAY = "2026-07-08"

def w(id, name, format, movements, format_meta=None, tags=None, notes=None):
    entry = {
        "id": id, "name": name, "category": "hero", "format": format,
        "format_meta": format_meta or {},
        "movements": movements,
        "partition": None,
        "scaling": None,
        "origin": None,
        "tags": tags or [],
        "source_notes": notes or SRC,
        "schema_version": VER,
        "last_updated": TODAY,
    }
    with open(os.path.join(OUT, f"{id}.json"), "w") as f:
        json.dump(entry, f, indent=2)
        f.write("\n")

w("murph", "Murph", "for_time",
  [{"exercise": "run", "distance_m": 1609}, {"exercise": "pull-up", "reps": 100},
   {"exercise": "push-up", "reps": 200}, {"exercise": "air-squat", "reps": 300},
   {"exercise": "run", "distance_m": 1609}],
  tags=["memorial-day", "high-volume", "running"],
  notes=SRC + "; partition pull-ups/push-ups/squats as needed, per official prescription")

w("dt", "DT", "interval",
  [{"exercise": "deadlift", "reps": 12, "load": {"rx_male": "155lb", "rx_female": "105lb"}},
   {"exercise": "hang-power-clean", "reps": 9, "load": {"rx_male": "155lb", "rx_female": "105lb"}},
   {"exercise": "push-jerk", "reps": 6, "load": {"rx_male": "155lb", "rx_female": "105lb"}}],
  format_meta={"rounds": 5, "scoring": "time"},
  tags=["barbell", "5-rounds"])

w("jt", "JT", "for_time",
  [{"exercise": "handstand-push-up", "reps": [21,15,9]}, {"exercise": "ring-dip", "reps": [21,15,9]},
   {"exercise": "push-up", "reps": [21,15,9]}],
  tags=["gymnastics", "bodyweight"])

w("nate", "Nate", "amrap",
  [{"exercise": "muscle-up", "reps": 2}, {"exercise": "handstand-push-up", "reps": 4},
   {"exercise": "kettlebell-swing", "reps": 8, "load": {"rx_male": "2 pood", "rx_female": "1.5 pood"}}],
  format_meta={"time_cap_minutes": 20},
  tags=["gymnastics", "kettlebell", "amrap"])

w("randy", "Randy", "for_time",
  [{"exercise": "power-snatch", "reps": 75, "load": {"rx_male": "75lb", "rx_female": "55lb"}}],
  tags=["single-movement", "barbell", "sprint"])

w("daniel", "Daniel", "for_time",
  [{"exercise": "pull-up", "reps": 50}, {"exercise": "run", "distance_m": 400},
   {"exercise": "thruster", "reps": 21, "load": {"rx_male": "95lb", "rx_female": "65lb"}},
   {"exercise": "run", "distance_m": 800},
   {"exercise": "thruster", "reps": 21, "load": {"rx_male": "95lb", "rx_female": "65lb"}},
   {"exercise": "run", "distance_m": 400}, {"exercise": "pull-up", "reps": 50}],
  tags=["running", "barbell", "gymnastics"])

w("jason", "Jason", "for_time",
  [{"exercise": "air-squat", "reps": 100}, {"exercise": "muscle-up", "reps": 5},
   {"exercise": "air-squat", "reps": 75}, {"exercise": "muscle-up", "reps": 10},
   {"exercise": "air-squat", "reps": 50}, {"exercise": "muscle-up", "reps": 15},
   {"exercise": "air-squat", "reps": 25}, {"exercise": "muscle-up", "reps": 20}],
  tags=["gymnastics", "bodyweight", "descending-ascending"])

w("josh", "Josh", "for_time",
  [{"exercise": "overhead-squat", "reps": 21, "load": {"rx_male": "95lb", "rx_female": "65lb"}},
   {"exercise": "pull-up", "reps": 42},
   {"exercise": "overhead-squat", "reps": 15, "load": {"rx_male": "95lb", "rx_female": "65lb"}},
   {"exercise": "pull-up", "reps": 30},
   {"exercise": "overhead-squat", "reps": 9, "load": {"rx_male": "95lb", "rx_female": "65lb"}},
   {"exercise": "pull-up", "reps": 18}],
  tags=["barbell", "gymnastics"])

w("tommy-v", "Tommy V", "for_time",
  [{"exercise": "thruster", "reps": 21, "load": {"rx_male": "115lb", "rx_female": "75lb"}},
   {"exercise": "rope-climb", "reps": 12},
   {"exercise": "thruster", "reps": 15, "load": {"rx_male": "115lb", "rx_female": "75lb"}},
   {"exercise": "rope-climb", "reps": 9},
   {"exercise": "thruster", "reps": 9, "load": {"rx_male": "115lb", "rx_female": "75lb"}},
   {"exercise": "rope-climb", "reps": 6}],
  tags=["barbell", "gymnastics"])

w("hansen", "Hansen", "interval",
  [{"exercise": "kettlebell-swing", "reps": 30}, {"exercise": "burpee", "reps": 30}, {"exercise": "ghd-sit-up", "reps": 30}],
  format_meta={"rounds": 5, "scoring": "time"},
  tags=["kettlebell", "bodyweight", "5-rounds"])

w("the-seven", "The Seven", "interval",
  [{"exercise": "handstand-push-up", "reps": 7}, {"exercise": "thruster", "reps": 7},
   {"exercise": "knees-to-elbows", "reps": 7}, {"exercise": "deadlift", "reps": 7},
   {"exercise": "burpee", "reps": 7}, {"exercise": "kettlebell-swing", "reps": 7}, {"exercise": "pull-up", "reps": 7}],
  format_meta={"rounds": 7, "scoring": "time"},
  tags=["7-rounds", "high-skill"])

w("nutts", "Nutts", "for_time",
  [{"exercise": "handstand-push-up", "reps": 10}, {"exercise": "deadlift", "reps": 15},
   {"exercise": "box-jump", "reps": 25}, {"exercise": "pull-up", "reps": 50},
   {"exercise": "wall-ball-shot", "reps": 100}, {"exercise": "double-under", "reps": 200},
   {"exercise": "run", "distance_m": 400, "notes": "with a plate"}],
  tags=["gymnastics", "high-volume"])

w("badger", "Badger", "interval",
  [{"exercise": "squat-clean", "reps": 30}, {"exercise": "pull-up", "reps": 30}, {"exercise": "run", "distance_m": 800}],
  format_meta={"rounds": 3, "scoring": "time"},
  tags=["barbell", "running", "3-rounds"])

w("holleyman", "Holleyman", "for_time",
  [{"exercise": "wall-ball-shot", "reps": 5}, {"exercise": "handstand-push-up", "reps": 3}, {"exercise": "power-clean", "reps": 1}],
  format_meta={"rounds": 30, "scoring": "time"},
  tags=["30-rounds", "gymnastics"])

w("rahoi", "Rahoi", "amrap",
  [{"exercise": "box-jump", "reps": 12}, {"exercise": "thruster", "reps": 6}, {"exercise": "bar-facing-burpee", "reps": 6}],
  format_meta={"time_cap_minutes": 12},
  tags=["amrap", "barbell"])

w("wittman", "Wittman", "interval",
  [{"exercise": "kettlebell-swing", "reps": 15}, {"exercise": "power-clean", "reps": 15}, {"exercise": "box-jump", "reps": 15}],
  format_meta={"rounds": 7, "scoring": "time"},
  tags=["7-rounds", "kettlebell", "barbell"])

w("ship", "Ship", "interval",
  [{"exercise": "squat-clean", "reps": 7}, {"exercise": "burpee-box-jump", "reps": 8}],
  format_meta={"rounds": 9, "scoring": "time"},
  tags=["9-rounds", "barbell"])

w("thompson", "Thompson", "interval",
  [{"exercise": "rope-climb", "reps": 1, "notes": "to 15 feet, start seated"}, {"exercise": "back-squat", "reps": 29},
   {"exercise": "farmers-carry", "distance_m": 10}],
  format_meta={"rounds": 10, "scoring": "time"},
  tags=["10-rounds", "gymnastics"])

w("small", "Small", "for_time",
  [{"exercise": "row", "distance_m": 1000}, {"exercise": "burpee", "reps": 50}, {"exercise": "box-jump", "reps": 50},
   {"exercise": "run", "distance_m": 800}],
  tags=["rowing", "running", "bodyweight"])

print(f"Wrote {len(os.listdir(OUT))} core Hero entries to {OUT}")
