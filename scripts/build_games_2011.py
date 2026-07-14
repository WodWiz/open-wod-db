import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-10"

# CrossFit Games individual events -- 2011. Each verified against its official
# games.crossfit.com/workouts/games/2011/<n> page, cross-referenced via
# independent sources for events whose primary page 404'd. No events skipped
# this year -- all 10 have a genuine fixed prescription (Skills 1/2 combine
# several individually-fixed sub-tests into one ranking, represented as
# multi_part).
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
AMRAP = lambda n, s="rounds_reps": {"time_cap_minutes": n, "scoring": s}

w("games-11-beach", "Beach (2011 Games)", "for_time", (2011, 1),
  [{"exercise": "swim", "distance_m": 210},
   {"exercise": "run", "distance_m": 1500, "notes": "soft sand"},
   {"exercise": "chest-to-bar-pull-up", "reps": 50},
   {"exercise": "hand-release-push-up", "reps": 100},
   {"exercise": "air-squat", "reps": 200},
   {"exercise": "run", "distance_m": 1500, "notes": "soft sand"}],
  tags=["games", "2011", "swim", "open-water", "running", "bodyweight", "endurance"])

w("games-11-dog-sled", "Dog-Sled", "for_time", (2011, 2),
  [{"exercise": "double-under", "reps": 30}, {"exercise": "overhead-squat", "reps": 10, "load": BB("135lb", "95lb")},
   {"exercise": "double-under", "reps": 30}, {"exercise": "overhead-squat", "reps": 10, "load": BB("135lb", "95lb")},
   {"exercise": "double-under", "reps": 30}, {"exercise": "overhead-squat", "reps": 10, "load": BB("135lb", "95lb")},
   {"exercise": "handstand-push-up", "reps": 10}, {"exercise": "sled-push", "distance_m": 12, "load": BB("385lb", "275lb"), "notes": "40 ft; total sled weight"},
   {"exercise": "handstand-push-up", "reps": 10}, {"exercise": "sled-push", "distance_m": 12, "load": BB("385lb", "275lb"), "notes": "40 ft; total sled weight"},
   {"exercise": "handstand-push-up", "reps": 10}, {"exercise": "sled-push", "distance_m": 12, "load": BB("385lb", "275lb"), "notes": "40 ft; total sled weight"}],
  tags=["games", "2011", "barbell", "gymnastics", "venue-equipment", "jump-rope"])

w("games-11-killer-kage", "Killer Kage", "interval", (2011, 3),
  [{"exercise": "front-squat", "reps": 7, "load": BB("225lb", "155lb")},
   {"exercise": "bike", "distance_m": 700},
   {"exercise": "parallel-bar-traverse", "distance_m": 30, "notes": "100 ft, monkey bars"}],
  format_meta={"rounds": 3, "scoring": "time"}, tags=["games", "2011", "barbell", "gymnastics", "3-rounds"])

w("games-11-rope-clean", "Rope-Clean", "for_time", (2011, 4),
  [{"exercise": "rope-climb", "reps": 5, "notes": "15 ft"},
   {"exercise": "clean-and-jerk", "reps": 5, "load": BB("145lb", "115lb")},
   {"exercise": "rope-climb", "reps": 4, "notes": "15 ft"},
   {"exercise": "clean-and-jerk", "reps": 4, "load": BB("165lb", "125lb")},
   {"exercise": "rope-climb", "reps": 3, "notes": "15 ft"},
   {"exercise": "clean-and-jerk", "reps": 3, "load": BB("185lb", "135lb")},
   {"exercise": "rope-climb", "reps": 2, "notes": "15 ft"},
   {"exercise": "clean-and-jerk", "reps": 2, "load": BB("205lb", "145lb")},
   {"exercise": "rope-climb", "reps": 1, "notes": "15 ft"},
   {"exercise": "clean-and-jerk", "reps": 1, "load": BB("225lb", "155lb")}],
  tags=["games", "2011", "barbell", "gymnastics", "ladder"])

w("games-11-skills-1", "Skills 1", "multi_part", (2011, 5),
  segments=[
    {"label": "L-sit hold", "format": "max_effort", "format_meta": {"scoring": "time"},
     "movements": [{"exercise": "l-sit", "notes": "1 attempt; scored by longest hold"}]},
    {"label": "Softball throw", "format": "max_effort", "format_meta": {"scoring": "reps"},
     "movements": [{"exercise": "medicine-ball-throw", "reps": 2, "notes": "softball; 2 attempts, scored by furthest throw"}]},
    {"label": "Handstand walk", "format": "max_effort", "format_meta": {"scoring": "reps"},
     "movements": [{"exercise": "handstand-walk", "notes": "1 attempt for maximum distance, with a mulligan allowed if under 5 yards"}]},
  ],
  tags=["games", "2011", "gymnastics", "max-effort"],
  notes=src(2011, 5) + "; three independently-ranked skill tests; final score is the sum of the three individual rankings (lower total wins)")

w("games-11-skills-2", "Skills 2", "multi_part", (2011, 6),
  segments=[
    {"label": "Weighted chest-to-bar pull-up", "format": "max_load", "format_meta": {"time_cap_minutes": 2, "scoring": "load"},
     "movements": [{"exercise": "weighted-pull-up", "reps": 1, "notes": "chest-to-bar; athlete's own max load"}]},
    {"label": "Snatch", "format": "max_load", "format_meta": {"time_cap_minutes": 2, "scoring": "load"},
     "movements": [{"exercise": "snatch", "reps": 1, "notes": "athlete's own 1-rep-max"}]},
    {"label": "Jug carry", "format": "max_effort", "format_meta": {"time_cap_minutes": 1, "scoring": "reps"},
     "movements": [{"exercise": "farmers-carry", "notes": "2 weighted water jugs; 60 seconds for maximum distance"}]},
  ],
  tags=["games", "2011", "barbell", "gymnastics", "max-effort"],
  notes=src(2011, 6) + "; three independently-ranked skill tests; final score is the sum of the three individual rankings (lower total wins); no gender-differentiated loads reported")

w("games-11-the-end-1", "The End 1", "amrap", (2011, 7),
  [{"exercise": "row", "reps": 20, "notes": "calories"},
   {"exercise": "wall-ball-shot", "reps": 30, "load": BB("20lb", "14lb")},
   {"exercise": "toes-to-bar", "reps": 20},
   {"exercise": "box-jump", "reps": 30, "notes": "24 in box"},
   {"exercise": "kettlebell-sumo-deadlift-high-pull", "reps": 20, "load": BB("108lb", "72lb")},
   {"exercise": "burpee", "reps": 30},
   {"exercise": "shoulder-to-overhead", "reps": 20, "load": BB("135lb", "95lb")},
   {"exercise": "sled-pull", "notes": "distance/load not specified in available sources"}],
  format_meta=AMRAP(3, "reps"),
  tags=["games", "2011", "rowing", "barbell", "kettlebell", "gymnastics"],
  notes=src(2011, 7) + "; 1 minute of rest follows before The End 2")

w("games-11-the-end-2", "The End 2", "amrap", (2011, 8),
  [{"exercise": "row", "reps": 20, "notes": "calories"},
   {"exercise": "wall-ball-shot", "reps": 30, "load": BB("20lb", "14lb")},
   {"exercise": "toes-to-bar", "reps": 20},
   {"exercise": "box-jump", "reps": 30, "notes": "24 in box"},
   {"exercise": "kettlebell-sumo-deadlift-high-pull", "reps": 20, "load": BB("108lb", "72lb")},
   {"exercise": "burpee", "reps": 30},
   {"exercise": "shoulder-to-overhead", "reps": 20, "load": BB("135lb", "95lb")},
   {"exercise": "sled-pull", "notes": "distance/load not specified in available sources"}],
  format_meta=AMRAP(6, "reps"),
  tags=["games", "2011", "rowing", "barbell", "kettlebell", "gymnastics"],
  notes=src(2011, 8) + "; same movement circuit as The End 1, over a longer time domain")

w("games-11-the-end-3", "The End 3", "for_time", (2011, 9),
  [{"exercise": "row", "reps": 20, "notes": "calories"},
   {"exercise": "wall-ball-shot", "reps": 30, "load": BB("20lb", "14lb")},
   {"exercise": "toes-to-bar", "reps": 20},
   {"exercise": "box-jump", "reps": 30, "notes": "24 in box"},
   {"exercise": "kettlebell-sumo-deadlift-high-pull", "reps": 20, "load": BB("108lb", "72lb")},
   {"exercise": "burpee", "reps": 30},
   {"exercise": "shoulder-to-overhead", "reps": 20, "load": BB("135lb", "95lb")},
   {"exercise": "sled-pull", "notes": "distance/load not specified in available sources"}],
  tags=["games", "2011", "rowing", "barbell", "kettlebell", "gymnastics"],
  notes=src(2011, 9) + "; same movement circuit as The End 1/2, performed once for time rather than as an AMRAP")

w("games-11-triplet-sprint", "Triplet Sprint", "for_time", (2011, 10),
  [{"exercise": "muscle-up", "reps": 5}, {"exercise": "deadlift", "reps": 10, "load": BB("245lb", "165lb")}, {"exercise": "ghd-sit-up", "reps": 15},
   {"exercise": "sprint", "distance_m": 46, "notes": "50 yd"},
   {"exercise": "muscle-up", "reps": 5}, {"exercise": "deadlift", "reps": 10, "load": BB("245lb", "165lb")}, {"exercise": "ghd-sit-up", "reps": 15},
   {"exercise": "sprint", "distance_m": 91, "notes": "100 yd"},
   {"exercise": "muscle-up", "reps": 5}, {"exercise": "deadlift", "reps": 10, "load": BB("245lb", "165lb")}, {"exercise": "ghd-sit-up", "reps": 15},
   {"exercise": "sprint", "distance_m": 137, "notes": "150 yd"},
   {"exercise": "muscle-up", "reps": 5}, {"exercise": "deadlift", "reps": 10, "load": BB("245lb", "165lb")}, {"exercise": "ghd-sit-up", "reps": 15},
   {"exercise": "sprint", "distance_m": 137, "notes": "150 yd (men); the women's final sprint was 200 yd"}],
  tags=["games", "2011", "barbell", "gymnastics", "running"])

print(f"Wrote 2011 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
