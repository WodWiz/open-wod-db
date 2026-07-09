import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "heroes")
os.makedirs(OUT, exist_ok=True)
VER = "1.0"
TODAY = "2026-07-09"

# Batch 4 (wave 2): 30 more Hero WODs, each verified against its official
# crossfit.com/benchmark page. Prescribed vests -> source_notes + weight-vest tag;
# optional vests -> weight-vest-optional. Bodyweight-relative loads (Miron) noted
# rather than fabricated. Box/target heights omitted; loads recorded.
VEST_20 = "; official Rx includes a 20 lb (men) / 14 lb (women) weight vest"

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

w("gallant", "Gallant", "for_time",
  [{"exercise": "run", "distance_m": 1609, "notes": "carrying a 20/14 lb medicine ball"},
   {"exercise": "burpee-pull-up", "reps": 60},
   {"exercise": "run", "distance_m": 800, "notes": "carrying a 20/14 lb medicine ball"},
   {"exercise": "burpee-pull-up", "reps": 30},
   {"exercise": "run", "distance_m": 400, "notes": "carrying a 20/14 lb medicine ball"},
   {"exercise": "burpee-pull-up", "reps": 15}],
  "gallant", tags=["running", "gymnastics"])

w("garrett", "Garrett", "interval",
  [{"exercise": "air-squat", "reps": 75},
   {"exercise": "ring-handstand-push-up", "reps": 25},
   {"exercise": "l-pull-up", "reps": 25}],
  "garrett", format_meta=RDS(3), tags=["gymnastics", "bodyweight", "3-rounds"])

w("gunny", "Gunny", "for_time",
  [{"exercise": "run", "distance_m": 1609, "notes": "weighted"},
   {"exercise": "push-up", "reps": 50}, {"exercise": "sit-up", "reps": 50},
   {"exercise": "run", "distance_m": 1609, "notes": "weighted"},
   {"exercise": "push-up", "reps": 50}, {"exercise": "sit-up", "reps": 50},
   {"exercise": "run", "distance_m": 1609, "notes": "weighted"}],
  "gunny", tags=["running", "bodyweight", "weight-vest"],
  notes=src("gunny") + "; official Rx: wear a weight vest / body armor / loaded pack totaling 50 lb for the runs")

w("hollywood", "Hollywood", "for_time",
  [{"exercise": "run", "distance_m": 2000},
   {"exercise": "wall-ball-shot", "reps": 22, "load": BB("30lb", "20lb")},
   {"exercise": "muscle-up", "reps": 22},
   {"exercise": "wall-ball-shot", "reps": 22, "load": BB("30lb", "20lb")},
   {"exercise": "power-clean", "reps": 22, "load": BB("185lb", "125lb")},
   {"exercise": "wall-ball-shot", "reps": 22, "load": BB("30lb", "20lb")},
   {"exercise": "run", "distance_m": 2000}],
  "hollywood", tags=["running", "barbell", "gymnastics"])

w("hoover", "Hoover", "interval",
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "burpee-box-jump-over", "reps": 15},
   {"exercise": "bike", "reps": 10, "notes": "calories"},
   {"exercise": "alternating-dumbbell-snatch", "reps": 6, "load": BB("75lb", "50lb")}],
  "hoover-hero", format_meta=RDS(8), tags=["running", "dumbbell", "8-rounds"],
  notes=src("hoover-hero"))

w("hortman", "Hortman", "amrap",
  [{"exercise": "run", "distance_m": 800},
   {"exercise": "air-squat", "reps": 80},
   {"exercise": "muscle-up", "reps": 8}],
  "hortman", format_meta=AM(45), tags=["amrap", "running", "gymnastics"])

w("jbo", "JBo", "amrap",
  [{"exercise": "overhead-squat", "reps": 9, "load": BB("115lb", "75lb")},
   {"exercise": "bench-press", "reps": 12, "load": BB("115lb", "75lb")}],
  "jbo", format_meta=AM(28), tags=["amrap", "barbell"])

w("jorge", "Jorge", "for_time",
  [{"exercise": "ghd-sit-up", "reps": [30, 24, 18, 12, 6]},
   {"exercise": "squat-clean", "reps": [15, 12, 9, 6, 3], "load": BB("155lb", "105lb")}],
  "jorge", tags=["barbell", "gymnastics", "ladder"])

w("joshie", "Joshie", "interval",
  [{"exercise": "dumbbell-snatch", "reps": 21, "load": BB("40lb", "25lb"), "notes": "right arm"},
   {"exercise": "l-pull-up", "reps": 21},
   {"exercise": "dumbbell-snatch", "reps": 21, "load": BB("40lb", "25lb"), "notes": "left arm"},
   {"exercise": "l-pull-up", "reps": 21}],
  "joshie", format_meta=RDS(3), tags=["dumbbell", "gymnastics", "3-rounds"])

w("k27", "K27", "interval",
  [{"exercise": "hang-power-clean", "reps": 5, "load": BB("185lb", "105lb")},
   {"exercise": "burpee", "reps": 5},
   {"exercise": "double-under", "reps": 15}],
  "k27", format_meta=RDS(27), tags=["barbell", "27-rounds"])

w("kelly-brown", "Kelly Brown", "interval",
  [{"exercise": "row", "distance_m": 440},
   {"exercise": "box-jump", "reps": 10},
   {"exercise": "deadlift", "reps": 10, "load": BB("275lb", "185lb")},
   {"exercise": "wall-ball-shot", "reps": 10, "load": BB("30lb", "20lb")}],
  "kelly-brown", format_meta=RDS(5), tags=["rowing", "barbell", "5-rounds"])

w("kevin", "Kevin", "interval",
  [{"exercise": "deadlift", "reps": 32, "load": BB("185lb", "125lb")},
   {"exercise": "hanging-hip-touch", "reps": 32, "notes": "alternating arms"},
   {"exercise": "farmers-carry", "distance_m": 800, "load": BB("15lb", "10lb"), "notes": "running"}],
  "kevin", format_meta=RDS(3), tags=["barbell", "dumbbell", "3-rounds"])

w("klepto", "Klepto", "interval",
  [{"exercise": "box-jump", "reps": 27},
   {"exercise": "burpee", "reps": 20},
   {"exercise": "squat-clean", "reps": 11, "load": BB("145lb", "95lb")}],
  "klepto", format_meta=RDS(4), tags=["barbell", "gymnastics", "4-rounds"])

w("kutschbach", "Kutschbach", "interval",
  [{"exercise": "back-squat", "reps": 11, "load": BB("185lb", "125lb")},
   {"exercise": "jerk", "reps": 10, "load": BB("135lb", "95lb")}],
  "kutschbach", format_meta=RDS(7), tags=["barbell", "7-rounds"])

w("ledesma", "Ledesma", "amrap",
  [{"exercise": "parallette-handstand-push-up", "reps": 5},
   {"exercise": "toes-to-ring", "reps": 10},
   {"exercise": "medicine-ball-clean", "reps": 15, "load": BB("20lb", "14lb")}],
  "ledesma", format_meta=AM(20), tags=["amrap", "gymnastics"])

w("lee", "Lee", "interval",
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "deadlift", "reps": 1, "load": BB("345lb", "225lb")},
   {"exercise": "squat-clean", "reps": 3, "load": BB("185lb", "125lb")},
   {"exercise": "push-jerk", "reps": 5, "load": BB("185lb", "125lb")},
   {"exercise": "muscle-up", "reps": 3},
   {"exercise": "rope-climb", "reps": 1, "notes": "to 15 feet"}],
  "lee", format_meta=RDS(5), tags=["running", "barbell", "gymnastics", "5-rounds"])

w("liam", "Liam", "for_time",
  [{"exercise": "run", "distance_m": 800, "load": BB("45lb", "25lb"), "notes": "carrying a plate"},
   {"exercise": "toes-to-bar", "reps": 100},
   {"exercise": "front-squat", "reps": 50, "load": BB("155lb", "105lb")},
   {"exercise": "rope-climb", "reps": 10, "notes": "to 15 feet"},
   {"exercise": "run", "distance_m": 800, "load": BB("45lb", "25lb"), "notes": "carrying a plate"}],
  "liam", tags=["running", "barbell", "gymnastics"])

w("luce", "Luce", "interval",
  [{"exercise": "run", "distance_m": 1000},
   {"exercise": "muscle-up", "reps": 10},
   {"exercise": "air-squat", "reps": 100}],
  "luce", format_meta=RDS(3), tags=["running", "gymnastics", "weight-vest", "3-rounds"],
  notes=src("luce") + VEST_20)

w("lumberjack-20", "Lumberjack 20", "for_time",
  [{"exercise": "deadlift", "reps": 20, "load": BB("275lb", "185lb")}, {"exercise": "run", "distance_m": 400},
   {"exercise": "kettlebell-swing", "reps": 20, "load": BB("70lb", "53lb")}, {"exercise": "run", "distance_m": 400},
   {"exercise": "overhead-squat", "reps": 20, "load": BB("115lb", "75lb")}, {"exercise": "run", "distance_m": 400},
   {"exercise": "burpee", "reps": 20}, {"exercise": "run", "distance_m": 400},
   {"exercise": "chest-to-bar-pull-up", "reps": 20}, {"exercise": "run", "distance_m": 400},
   {"exercise": "box-jump", "reps": 20}, {"exercise": "run", "distance_m": 400},
   {"exercise": "dumbbell-squat-clean", "reps": 20, "load": BB("45lb", "30lb")}, {"exercise": "run", "distance_m": 400}],
  "lumberjack-20", tags=["barbell", "running", "high-volume"])

w("marston", "Marston", "amrap",
  [{"exercise": "deadlift", "reps": 1, "load": BB("405lb", "275lb")},
   {"exercise": "toes-to-bar", "reps": 10},
   {"exercise": "bar-facing-burpee", "reps": 15}],
  "marston", format_meta=AM(20), tags=["amrap", "barbell", "gymnastics"])

w("matt-16", "Matt 16", "for_time",
  [{"exercise": "deadlift", "reps": 16, "load": BB("275lb", "185lb")},
   {"exercise": "hang-power-clean", "reps": 16, "load": BB("185lb", "125lb")},
   {"exercise": "push-press", "reps": 16, "load": BB("135lb", "95lb")},
   {"exercise": "run", "distance_m": 800},
   {"exercise": "deadlift", "reps": 16, "load": BB("275lb", "185lb")},
   {"exercise": "hang-power-clean", "reps": 16, "load": BB("185lb", "125lb")},
   {"exercise": "push-press", "reps": 16, "load": BB("135lb", "95lb")},
   {"exercise": "run", "distance_m": 800},
   {"exercise": "deadlift", "reps": 16, "load": BB("275lb", "185lb")},
   {"exercise": "hang-power-clean", "reps": 16, "load": BB("185lb", "125lb")},
   {"exercise": "push-press", "reps": 16, "load": BB("135lb", "95lb")}],
  "matt-16", tags=["barbell", "running"])

w("maupin", "Maupin", "interval",
  [{"exercise": "run", "distance_m": 800},
   {"exercise": "push-up", "reps": 49},
   {"exercise": "sit-up", "reps": 49},
   {"exercise": "air-squat", "reps": 49}],
  "maupin", format_meta=RDS(4), tags=["running", "bodyweight", "4-rounds"])

w("maxton", "Maxton", "interval",
  [{"exercise": "strict-pull-up", "reps": 8},
   {"exercise": "box-step-up", "reps": 26},
   {"exercise": "burpee", "reps": 21}],
  "maxton", format_meta=RDS(13), tags=["gymnastics", "weight-vest", "13-rounds"],
  notes=src("maxton") + VEST_20)

w("mccluskey", "McCluskey", "interval",
  [{"exercise": "muscle-up", "reps": 9},
   {"exercise": "burpee-pull-up", "reps": 15},
   {"exercise": "pull-up", "reps": 21},
   {"exercise": "run", "distance_m": 800}],
  "mccluskey", format_meta=RDS(3), tags=["gymnastics", "running", "weight-vest-optional", "3-rounds"],
  notes=src("mccluskey") + "; official Rx adds an optional 20 lb vest or body armor if available")

w("meadows", "Meadows", "for_time",
  [{"exercise": "muscle-up", "reps": 20},
   {"exercise": "ring-lower", "reps": 25, "notes": "slow, from inverted hang, straight body and arms"},
   {"exercise": "ring-handstand-push-up", "reps": 30},
   {"exercise": "ring-row", "reps": 35},
   {"exercise": "ring-push-up", "reps": 40}],
  "meadows", tags=["gymnastics", "rings"])

w("miron", "Miron", "interval",
  [{"exercise": "run", "distance_m": 800},
   {"exercise": "back-squat", "reps": 23, "notes": "3/4 bodyweight"},
   {"exercise": "deadlift", "reps": 13, "notes": "1 1/2 bodyweight"}],
  "miron", format_meta=RDS(5), tags=["running", "barbell", "5-rounds"])

w("monti", "Monti", "interval",
  [{"exercise": "barbell-step-up", "reps": 50, "load": BB("45lb", "35lb")},
   {"exercise": "clean", "reps": 15, "load": BB("135lb", "95lb")},
   {"exercise": "barbell-step-up", "reps": 50, "load": BB("45lb", "35lb")},
   {"exercise": "snatch", "reps": 10, "load": BB("135lb", "95lb")}],
  "monti", format_meta=RDS(5), tags=["barbell", "5-rounds"])

w("moon", "Moon", "interval",
  [{"exercise": "dumbbell-hang-split-snatch", "reps": 10, "load": BB("40lb", "30lb"), "notes": "right arm"},
   {"exercise": "rope-climb", "reps": 1, "notes": "to 15 feet"},
   {"exercise": "dumbbell-hang-split-snatch", "reps": 10, "load": BB("40lb", "30lb"), "notes": "left arm"},
   {"exercise": "rope-climb", "reps": 1, "notes": "to 15 feet"}],
  "moon", format_meta=RDS(7), tags=["dumbbell", "gymnastics", "7-rounds"])

w("moore", "Moore", "amrap",
  [{"exercise": "rope-climb", "reps": 1, "notes": "to 15 feet"},
   {"exercise": "run", "distance_m": 400},
   {"exercise": "handstand-push-up", "reps": "max", "notes": "max reps"}],
  "moore", format_meta=AM(20), tags=["amrap", "gymnastics"])

w("morrison", "Morrison", "for_time",
  [{"exercise": "wall-ball-shot", "reps": [50, 40, 30, 20, 10], "load": BB("20lb", "14lb")},
   {"exercise": "box-jump", "reps": [50, 40, 30, 20, 10]},
   {"exercise": "kettlebell-swing", "reps": [50, 40, 30, 20, 10], "load": BB("53lb", "35lb")}],
  "morrison", tags=["kettlebell", "ladder"])

print(f"Wrote batch-4 wave-2 entries; heroes dir now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
