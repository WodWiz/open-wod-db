import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "heroes")
os.makedirs(OUT, exist_ok=True)
VER = "1.0"
TODAY = "2026-07-09"

# Batch 4 (wave 1): 30 Hero WODs, each verified against its official
# crossfit.com/benchmark page (men -> rx_male, women -> rx_female). Box heights
# and wall-ball target heights are omitted (standard); barbell/DB/KB/sandbag/ball
# loads are recorded. Foot/yard distances converted to meters.
VEST_OPT = "; official Rx adds an optional load: 'If you have a weight vest or body armor, wear it.'"

def src(slug):
    return f"crossfit.com/benchmark/{slug} (official CrossFit Hero WOD page), retrieved {TODAY}"

def w(id, name, format, movements, slug, format_meta=None, tags=None, notes=None):
    entry = {
        "id": id, "name": name, "category": "hero", "format": format,
        "format_meta": format_meta or {},
        "movements": movements, "partition": None, "scaling": None, "origin": None,
        "tags": tags or [], "source_notes": notes or src(slug),
        "schema_version": VER, "last_updated": TODAY,
    }
    with open(os.path.join(OUT, f"{id}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(entry, f, indent=2)
        f.write("\n")

BB = lambda m, f: {"rx_male": m, "rx_female": f}
RDS = lambda n: {"rounds": n, "scoring": "time"}
AM = lambda n: {"time_cap_minutes": n}

w("adambrown", "Adambrown", "interval",
  [{"exercise": "deadlift", "reps": 24, "load": BB("295lb", "195lb")},
   {"exercise": "box-jump", "reps": 24},
   {"exercise": "wall-ball-shot", "reps": 24, "load": BB("20lb", "14lb")},
   {"exercise": "bench-press", "reps": 24, "load": BB("195lb", "135lb")},
   {"exercise": "box-jump", "reps": 24},
   {"exercise": "wall-ball-shot", "reps": 24, "load": BB("20lb", "14lb")},
   {"exercise": "clean", "reps": 24, "load": BB("145lb", "95lb")}],
  "adambrown", format_meta=RDS(2), tags=["barbell", "gymnastics", "2-rounds"])

w("arnie", "Arnie", "for_time",
  [{"exercise": "turkish-get-up", "reps": 21, "load": BB("70lb", "53lb"), "notes": "right arm"},
   {"exercise": "kettlebell-swing", "reps": 50, "load": BB("70lb", "53lb")},
   {"exercise": "overhead-squat", "reps": 21, "load": BB("70lb", "53lb"), "notes": "left arm"},
   {"exercise": "kettlebell-swing", "reps": 50, "load": BB("70lb", "53lb")},
   {"exercise": "overhead-squat", "reps": 21, "load": BB("70lb", "53lb"), "notes": "right arm"},
   {"exercise": "kettlebell-swing", "reps": 50, "load": BB("70lb", "53lb")},
   {"exercise": "turkish-get-up", "reps": 21, "load": BB("70lb", "53lb"), "notes": "left arm"}],
  "arnie", tags=["kettlebell", "single-kettlebell"])

w("artie", "Artie", "amrap",
  [{"exercise": "pull-up", "reps": 5},
   {"exercise": "push-up", "reps": 10},
   {"exercise": "air-squat", "reps": 15},
   {"exercise": "pull-up", "reps": 5},
   {"exercise": "thruster", "reps": 10, "load": BB("95lb", "65lb")}],
  "artie", format_meta=AM(20), tags=["amrap", "bodyweight", "barbell"])

w("barraza", "Barraza", "amrap",
  [{"exercise": "run", "distance_m": 200},
   {"exercise": "deadlift", "reps": 9, "load": BB("275lb", "185lb")},
   {"exercise": "burpee-bar-muscle-up", "reps": 6}],
  "barraza", format_meta=AM(18), tags=["amrap", "barbell", "gymnastics"])

w("bert", "Bert", "for_time",
  [{"exercise": "burpee", "reps": 50}, {"exercise": "run", "distance_m": 400},
   {"exercise": "push-up", "reps": 100}, {"exercise": "run", "distance_m": 400},
   {"exercise": "walking-lunge", "reps": 150, "notes": "steps"}, {"exercise": "run", "distance_m": 400},
   {"exercise": "air-squat", "reps": 200}, {"exercise": "run", "distance_m": 400},
   {"exercise": "walking-lunge", "reps": 150, "notes": "steps"}, {"exercise": "run", "distance_m": 400},
   {"exercise": "push-up", "reps": 100}, {"exercise": "run", "distance_m": 400},
   {"exercise": "burpee", "reps": 50}],
  "bert", tags=["bodyweight", "running", "high-volume"])

w("big-sexy", "Big Sexy", "interval",
  [{"exercise": "deadlift", "reps": 6, "load": BB("315lb", "205lb")},
   {"exercise": "burpee", "reps": 6},
   {"exercise": "clean", "reps": 5, "load": BB("225lb", "155lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": 5},
   {"exercise": "thruster", "reps": 4, "load": BB("155lb", "105lb")},
   {"exercise": "muscle-up", "reps": 4}],
  "big-sexy", format_meta=RDS(5), tags=["barbell", "gymnastics", "5-rounds"])

w("blake", "Blake", "interval",
  [{"exercise": "overhead-walking-lunge", "distance_m": 30, "load": BB("45lb", "25lb"), "notes": "plate held overhead"},
   {"exercise": "box-jump", "reps": 30},
   {"exercise": "wall-ball-shot", "reps": 20, "load": BB("20lb", "14lb")},
   {"exercise": "handstand-push-up", "reps": 10}],
  "blake", format_meta=RDS(4), tags=["barbell", "gymnastics", "4-rounds"])

w("bowen", "Bowen", "interval",
  [{"exercise": "run", "distance_m": 800},
   {"exercise": "deadlift", "reps": 7, "load": BB("275lb", "185lb")},
   {"exercise": "burpee-pull-up", "reps": 10},
   {"exercise": "single-arm-kettlebell-thruster", "reps": 14, "load": BB("53lb", "35lb"), "notes": "7 each arm"},
   {"exercise": "box-jump", "reps": 20}],
  "bowen", format_meta=RDS(3), tags=["running", "barbell", "kettlebell", "3-rounds"])

w("brehm", "Brehm", "for_time",
  [{"exercise": "rope-climb", "reps": 10, "notes": "to 15 feet"},
   {"exercise": "back-squat", "reps": 20, "load": BB("225lb", "155lb")},
   {"exercise": "handstand-push-up", "reps": 30},
   {"exercise": "row", "reps": 40, "notes": "calories"}],
  "brehm", tags=["gymnastics", "barbell", "rowing"])

w("buriak", "Buriak", "amrap",
  [{"exercise": "squat-clean", "reps": 5, "load": BB("155lb", "135lb")},
   {"exercise": "bar-facing-burpee", "reps": 10},
   {"exercise": "pull-up", "reps": 15},
   {"exercise": "run", "distance_m": 200}],
  "buriak", format_meta=AM(20), tags=["amrap", "barbell", "gymnastics"])

w("cameron", "Cameron", "for_time",
  [{"exercise": "walking-lunge", "reps": 50, "notes": "steps"},
   {"exercise": "chest-to-bar-pull-up", "reps": 25},
   {"exercise": "box-jump", "reps": 50},
   {"exercise": "triple-under", "reps": 25},
   {"exercise": "back-extension", "reps": 50},
   {"exercise": "ring-dip", "reps": 25},
   {"exercise": "knees-to-elbows", "reps": 50},
   {"exercise": "wall-ball-shot", "reps": 25, "load": BB("20lb", "14lb"), "notes": "two-for-ones"},
   {"exercise": "sit-up", "reps": 50},
   {"exercise": "rope-climb", "reps": 5, "notes": "to 15 feet"}],
  "cameron", tags=["bodyweight", "gymnastics", "high-volume"])

w("capoot", "Capoot", "for_time",
  [{"exercise": "push-up", "reps": 100}, {"exercise": "run", "distance_m": 800},
   {"exercise": "push-up", "reps": 75}, {"exercise": "run", "distance_m": 1200},
   {"exercise": "push-up", "reps": 50}, {"exercise": "run", "distance_m": 1600},
   {"exercise": "push-up", "reps": 25}, {"exercise": "run", "distance_m": 2000}],
  "capoot", tags=["bodyweight", "running"])

w("chad1000x", "Chad1000x", "for_time",
  [{"exercise": "box-step-up", "reps": 1000, "load": BB("45lb", "35lb"), "notes": "ruck; 20-inch box"}],
  "chad1000x", tags=["weighted", "single-movement", "high-volume"])

w("clovis", "Clovis", "for_time",
  [{"exercise": "run", "distance_m": 16093},
   {"exercise": "burpee-pull-up", "reps": 150, "notes": "partition the run and burpee pull-ups as needed"}],
  "clovis", tags=["running", "gymnastics", "endurance"])

w("coffey", "Coffey", "for_time",
  [{"exercise": "run", "distance_m": 800},
   {"exercise": "back-squat", "reps": 50, "load": BB("135lb", "95lb")},
   {"exercise": "bench-press", "reps": 50, "load": BB("135lb", "95lb")},
   {"exercise": "run", "distance_m": 800},
   {"exercise": "back-squat", "reps": 35, "load": BB("135lb", "95lb")},
   {"exercise": "bench-press", "reps": 35, "load": BB("135lb", "95lb")},
   {"exercise": "run", "distance_m": 800},
   {"exercise": "back-squat", "reps": 20, "load": BB("135lb", "95lb")},
   {"exercise": "bench-press", "reps": 20, "load": BB("135lb", "95lb")},
   {"exercise": "run", "distance_m": 800},
   {"exercise": "muscle-up", "reps": 1}],
  "coffey", tags=["running", "barbell", "gymnastics"])

w("collin", "Collin", "interval",
  [{"exercise": "sandbag-carry", "distance_m": 400, "load": BB("50lb", "35lb")},
   {"exercise": "push-press", "reps": 12, "load": BB("115lb", "75lb")},
   {"exercise": "box-jump", "reps": 12},
   {"exercise": "sumo-deadlift-high-pull", "reps": 12, "load": BB("95lb", "65lb")}],
  "collin", format_meta=RDS(6), tags=["barbell", "running", "6-rounds"])

w("crain", "Crain", "interval",
  [{"exercise": "push-up", "reps": 34}, {"exercise": "run", "distance_m": 46, "notes": "sprint"},
   {"exercise": "deadlift", "reps": 34, "load": BB("135lb", "95lb")}, {"exercise": "run", "distance_m": 46, "notes": "sprint"},
   {"exercise": "box-jump", "reps": 34}, {"exercise": "run", "distance_m": 46, "notes": "sprint"},
   {"exercise": "clean-and-jerk", "reps": 34, "load": BB("95lb", "65lb")}, {"exercise": "run", "distance_m": 46, "notes": "sprint"},
   {"exercise": "burpee", "reps": 34}, {"exercise": "run", "distance_m": 46, "notes": "sprint"},
   {"exercise": "wall-ball-shot", "reps": 34, "load": BB("20lb", "14lb")}, {"exercise": "run", "distance_m": 46, "notes": "sprint"},
   {"exercise": "pull-up", "reps": 34}, {"exercise": "run", "distance_m": 46, "notes": "sprint"}],
  "crain", format_meta=RDS(2), tags=["barbell", "high-volume", "2-rounds"])

w("dae-han", "Dae Han", "interval",
  [{"exercise": "run", "distance_m": 800, "notes": "carrying an empty barbell"},
   {"exercise": "rope-climb", "reps": 3, "notes": "to 15 feet"},
   {"exercise": "thruster", "reps": 12, "load": BB("135lb", "95lb")}],
  "dae-han", format_meta=RDS(3), tags=["running", "barbell", "gymnastics", "3-rounds"])

w("daniel-ray", "Daniel Ray", "interval",
  [{"exercise": "double-kettlebell-front-rack-lunge", "distance_m": 8, "load": BB("53lb", "35lb")},
   {"exercise": "strict-pull-up", "reps": 9},
   {"exercise": "double-kettlebell-overhead-carry", "distance_m": 15, "load": BB("53lb", "35lb")},
   {"exercise": "hand-release-push-up", "reps": 16},
   {"exercise": "double-kettlebell-front-rack-carry", "distance_m": 23, "load": BB("53lb", "35lb")},
   {"exercise": "air-squat", "reps": 23},
   {"exercise": "double-kettlebell-farmers-carry", "distance_m": 30, "load": BB("53lb", "35lb")},
   {"exercise": "run", "distance_m": 400}],
  "daniel-ray", format_meta=RDS(5), tags=["kettlebell", "weight-vest-optional", "5-rounds"],
  notes=src("daniel-ray") + VEST_OPT)

w("del", "Del", "for_time",
  [{"exercise": "burpee", "reps": 25},
   {"exercise": "run", "distance_m": 400, "notes": "carrying a 20/14 lb medicine ball"},
   {"exercise": "weighted-pull-up", "reps": 25, "load": BB("20lb", "15lb"), "notes": "holding a dumbbell"},
   {"exercise": "run", "distance_m": 400, "notes": "carrying a 20/14 lb medicine ball"},
   {"exercise": "handstand-push-up", "reps": 25},
   {"exercise": "run", "distance_m": 400, "notes": "carrying a 20/14 lb medicine ball"},
   {"exercise": "chest-to-bar-pull-up", "reps": 25},
   {"exercise": "run", "distance_m": 400, "notes": "carrying a 20/14 lb medicine ball"},
   {"exercise": "burpee", "reps": 25}],
  "del", tags=["bodyweight", "running", "dumbbell"])

w("dg", "DG", "amrap",
  [{"exercise": "toes-to-bar", "reps": 8},
   {"exercise": "dumbbell-thruster", "reps": 8, "load": BB("35lb", "20lb")},
   {"exercise": "dumbbell-walking-lunge", "reps": 12, "load": BB("35lb", "20lb")}],
  "dg", format_meta=AM(10), tags=["amrap", "dumbbell", "gymnastics"])

w("dobogai", "Dobogai", "interval",
  [{"exercise": "muscle-up", "reps": 8},
   {"exercise": "farmers-carry", "distance_m": 20, "load": BB("50lb", "35lb")}],
  "dobogai", format_meta=RDS(7), tags=["gymnastics", "dumbbell", "7-rounds"])

w("donny", "Donny", "for_time",
  [{"exercise": "deadlift", "reps": [21, 15, 9, 9, 15, 21], "load": BB("225lb", "155lb")},
   {"exercise": "burpee", "reps": [21, 15, 9, 9, 15, 21]}],
  "donny", tags=["barbell", "ladder"])

w("dork", "Dork", "interval",
  [{"exercise": "double-under", "reps": 60},
   {"exercise": "kettlebell-swing", "reps": 30, "load": BB("53lb", "35lb")},
   {"exercise": "burpee", "reps": 15}],
  "dork", format_meta=RDS(6), tags=["kettlebell", "bodyweight", "6-rounds"])

w("dunn", "Dunn", "amrap",
  [{"exercise": "muscle-up", "reps": 3},
   {"exercise": "shuttle-sprint", "reps": 1, "notes": "5, 10, and 15 yards"},
   {"exercise": "burpee-box-jump-over", "reps": 6, "notes": "jump over the box without touching it"}],
  "dunn", format_meta=AM(19), tags=["amrap", "gymnastics"])

w("erin", "Erin", "interval",
  [{"exercise": "dumbbell-split-clean", "reps": 15, "load": BB("40lb", "30lb")},
   {"exercise": "pull-up", "reps": 21}],
  "erin", format_meta=RDS(5), tags=["dumbbell", "gymnastics", "5-rounds"])

w("falkel", "Falkel", "amrap",
  [{"exercise": "handstand-push-up", "reps": 8},
   {"exercise": "box-jump", "reps": 8},
   {"exercise": "rope-climb", "reps": 1, "notes": "to 15 feet"}],
  "falkel", format_meta=AM(25), tags=["amrap", "gymnastics"])

w("feeks", "Feeks", "for_time",
  [{"exercise": "shuttle-sprint", "reps": [2, 4, 6, 8, 10, 12, 14, 16], "notes": "100 m each"},
   {"exercise": "dumbbell-squat-clean-thruster", "reps": [2, 4, 6, 8, 10, 12, 14, 16], "load": BB("65lb", "45lb")}],
  "feeks", tags=["dumbbell", "ladder"])

w("forrest", "Forrest", "interval",
  [{"exercise": "l-pull-up", "reps": 20},
   {"exercise": "toes-to-bar", "reps": 30},
   {"exercise": "burpee", "reps": 40},
   {"exercise": "run", "distance_m": 800}],
  "forrest", format_meta=RDS(3), tags=["gymnastics", "bodyweight", "3-rounds"])

w("fournier", "Fournier", "for_time",
  [{"exercise": "shoulder-to-overhead", "reps": 50, "load": BB("115lb", "75lb")},
   {"exercise": "sled-pull", "distance_m": 15, "notes": "arm-over-arm; challenging load"},
   {"exercise": "burpee", "reps": 40},
   {"exercise": "sled-pull", "distance_m": 15, "notes": "arm-over-arm; challenging load"},
   {"exercise": "sumo-deadlift-high-pull", "reps": 30, "load": BB("85lb", "55lb")},
   {"exercise": "sled-pull", "distance_m": 15, "notes": "arm-over-arm; challenging load"}],
  "fournier", tags=["barbell", "sled"])

print(f"Wrote batch-4 wave-1 entries; heroes dir now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
