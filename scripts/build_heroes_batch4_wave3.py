import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "heroes")
os.makedirs(OUT, exist_ok=True)
VER = "1.0"
TODAY = "2026-07-09"

# Batch 4 (wave 3): the final 40 cleanly-structurable Hero WODs, each verified
# against its official crossfit.com/benchmark page. Prescribed vests -> source_notes
# + weight-vest tag; bodyweight-relative/bodyweight loads noted; box/target heights
# omitted (standard). ft/yd/mile distances converted to meters.
VEST_20 = "; official Rx includes a 20 lb (men) / 14 lb (women) weight vest"

def src(slug):
    return f"crossfit.com/benchmark/{slug} (official CrossFit Hero WOD page), retrieved {TODAY}"

def w(id, name, format, movements, slug, format_meta=None, tags=None, notes=None):
    entry = {
        "id": id, "name": name, "category": "hero", "format": format,
        "format_meta": format_meta or {},
        "movements": movements, "partition": None, "scaling": None, "origin": None,
        "tags": tags or [], "description": DESCRIPTIONS.get(id), "source_notes": notes or src(slug),
        "schema_version": VER, "last_updated": TODAY,
    }
    with open(os.path.join(OUT, f"{id}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(entry, f, indent=2)
        f.write("\n")

BB = lambda m, f: {"rx_male": m, "rx_female": f}
RDS = lambda n: {"rounds": n, "scoring": "time"}
AM = lambda n: {"time_cap_minutes": n}

w("mr-joshua", "Mr. Joshua", "interval",
  [{"exercise": "run", "distance_m": 400}, {"exercise": "ghd-sit-up", "reps": 30},
   {"exercise": "deadlift", "reps": 15, "load": BB("250lb", "175lb")}],
  "mr-joshua", format_meta=RDS(5), tags=["running", "barbell", "gymnastics", "5-rounds"])

w("nick", "Nick", "interval",
  [{"exercise": "dumbbell-hang-squat-clean", "reps": 10, "load": BB("45lb", "30lb")},
   {"exercise": "handstand-push-up", "reps": 6, "notes": "on dumbbells"}],
  "nick", format_meta=RDS(12), tags=["dumbbell", "gymnastics", "12-rounds"])

w("nickman", "Nickman", "interval",
  [{"exercise": "farmers-carry", "distance_m": 200, "load": BB("55lb", "40lb")},
   {"exercise": "weighted-pull-up", "reps": 10, "load": BB("35lb", "20lb")},
   {"exercise": "alternating-dumbbell-power-snatch", "reps": 20, "load": BB("55lb", "40lb")}],
  "nickman", format_meta=RDS(10), tags=["dumbbell", "10-rounds"])

w("oda-7313", "ODA 7313", "interval",
  [{"exercise": "run", "distance_m": 300, "notes": "jog"},
   {"exercise": "dumbbell-thruster", "reps": 10, "load": BB("30lb", "20lb"), "notes": "left arm"},
   {"exercise": "dumbbell-thruster", "reps": 10, "load": BB("30lb", "20lb"), "notes": "right arm"},
   {"exercise": "strict-pull-up", "reps": 7}],
  "oda-7313", format_meta=RDS(7), tags=["running", "dumbbell", "gymnastics", "7-rounds"])

w("omar", "Omar", "for_time",
  [{"exercise": "thruster", "reps": [10, 20, 30], "load": BB("95lb", "65lb")},
   {"exercise": "bar-facing-burpee", "reps": [15, 25, 35]}],
  "omar", tags=["barbell", "ladder"])

w("ozzy", "Ozzy", "interval",
  [{"exercise": "deficit-handstand-push-up", "reps": 11}, {"exercise": "run", "distance_m": 1000}],
  "ozzy", format_meta=RDS(7), tags=["gymnastics", "running", "7-rounds"])

w("paul", "Paul", "interval",
  [{"exercise": "double-under", "reps": 50}, {"exercise": "knees-to-elbows", "reps": 35},
   {"exercise": "overhead-walk", "distance_m": 18, "load": BB("185lb", "125lb")}],
  "paul", format_meta=RDS(5), tags=["barbell", "5-rounds"])

w("pheezy", "Pheezy", "interval",
  [{"exercise": "front-squat", "reps": 5, "load": BB("165lb", "115lb")},
   {"exercise": "pull-up", "reps": 18},
   {"exercise": "deadlift", "reps": 5, "load": BB("225lb", "155lb")},
   {"exercise": "toes-to-bar", "reps": 18},
   {"exercise": "push-jerk", "reps": 5, "load": BB("165lb", "115lb")},
   {"exercise": "hand-release-push-up", "reps": 18}],
  "pheezy", format_meta=RDS(3), tags=["barbell", "gymnastics", "3-rounds"])

w("pike", "Pike", "interval",
  [{"exercise": "thruster", "reps": 20, "load": BB("75lb", "55lb")},
   {"exercise": "ring-dip", "reps": 10, "notes": "strict"},
   {"exercise": "push-up", "reps": 20},
   {"exercise": "handstand-push-up", "reps": 10, "notes": "strict"},
   {"exercise": "bear-crawl", "distance_m": 50}],
  "pike", format_meta=RDS(5), tags=["barbell", "gymnastics", "5-rounds"])

w("ralph", "Ralph", "interval",
  [{"exercise": "deadlift", "reps": 8, "load": BB("250lb", "175lb")},
   {"exercise": "burpee", "reps": 16},
   {"exercise": "rope-climb", "reps": 3, "notes": "to 15 feet"},
   {"exercise": "run", "distance_m": 600}],
  "ralph", format_meta=RDS(4), tags=["barbell", "gymnastics", "4-rounds"])

w("restrepo", "Restrepo", "interval",
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "strict-pull-up", "reps": 7},
   {"exercise": "strict-handstand-push-up", "reps": 7},
   {"exercise": "toes-to-bar", "reps": 20},
   {"exercise": "alternating-dumbbell-snatch", "reps": 22, "load": BB("50lb", "35lb")},
   {"exercise": "dumbbell-carry", "distance_m": 200, "load": BB("50lb", "35lb")}],
  "restrepo", format_meta=RDS(5), tags=["running", "dumbbell", "gymnastics", "5-rounds"])

w("ricky", "Ricky", "amrap",
  [{"exercise": "pull-up", "reps": 10},
   {"exercise": "dumbbell-deadlift", "reps": 5, "load": BB("75lb", "50lb")},
   {"exercise": "push-press", "reps": 8, "load": BB("135lb", "95lb")}],
  "ricky", format_meta=AM(20), tags=["amrap", "dumbbell", "barbell"])

w("robbie", "Robbie", "amrap",
  [{"exercise": "freestanding-handstand-push-up", "reps": 8},
   {"exercise": "rope-climb", "reps": 1, "notes": "L-sit, to 15 feet"}],
  "robbie", format_meta=AM(25), tags=["amrap", "gymnastics"])

w("roney", "Roney", "interval",
  [{"exercise": "run", "distance_m": 200},
   {"exercise": "thruster", "reps": 11, "load": BB("135lb", "95lb")},
   {"exercise": "run", "distance_m": 200},
   {"exercise": "push-press", "reps": 11, "load": BB("135lb", "95lb")},
   {"exercise": "run", "distance_m": 200},
   {"exercise": "bench-press", "reps": 11, "load": BB("135lb", "95lb")}],
  "roney", format_meta=RDS(4), tags=["running", "barbell", "4-rounds"])

w("santiago", "Santiago", "interval",
  [{"exercise": "dumbbell-hang-squat-clean", "reps": 18, "load": BB("35lb", "20lb")},
   {"exercise": "pull-up", "reps": 18},
   {"exercise": "power-clean", "reps": 10, "load": BB("135lb", "95lb")},
   {"exercise": "handstand-push-up", "reps": 10}],
  "santiago", format_meta=RDS(7), tags=["dumbbell", "barbell", "gymnastics", "7-rounds"])

w("scotty", "Scotty", "amrap",
  [{"exercise": "deadlift", "reps": 5, "load": BB("315lb", "205lb")},
   {"exercise": "wall-ball-shot", "reps": 18, "load": BB("20lb", "14lb")},
   {"exercise": "bar-facing-burpee", "reps": 17}],
  "scotty", format_meta=AM(11), tags=["amrap", "barbell"])

w("severin", "Severin", "for_time",
  [{"exercise": "strict-pull-up", "reps": 50},
   {"exercise": "hand-release-push-up", "reps": 100},
   {"exercise": "run", "distance_m": 5000}],
  "severin", tags=["gymnastics", "running", "weight-vest"], notes=src("severin") + VEST_20)

w("spehar", "Spehar", "for_time",
  [{"exercise": "thruster", "reps": 100, "load": BB("135lb", "95lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": 100},
   {"exercise": "run", "distance_m": 9656, "notes": "partition the thrusters, pull-ups, and run as needed"}],
  "spehar", tags=["barbell", "gymnastics", "running", "endurance"])

w("stephen", "Stephen", "for_time",
  [{"exercise": "ghd-sit-up", "reps": [30, 25, 20, 15, 10, 5]},
   {"exercise": "back-extension", "reps": [30, 25, 20, 15, 10, 5]},
   {"exercise": "knees-to-elbows", "reps": [30, 25, 20, 15, 10, 5]},
   {"exercise": "stiff-legged-deadlift", "reps": [30, 25, 20, 15, 10, 5], "load": BB("95lb", "65lb")}],
  "stephen", tags=["barbell", "gymnastics", "ladder"])

w("strange", "Strange", "interval",
  [{"exercise": "run", "distance_m": 600},
   {"exercise": "weighted-pull-up", "reps": 11, "load": BB("53lb", "35lb")},
   {"exercise": "walking-lunge", "reps": 11, "load": BB("53lb", "35lb"), "notes": "carrying two kettlebells"},
   {"exercise": "kettlebell-thruster", "reps": 11, "load": BB("53lb", "35lb")}],
  "strange", format_meta=RDS(8), tags=["running", "kettlebell", "8-rounds"])

w("t-u-p", "T.U.P.", "for_time",
  [{"exercise": "power-clean", "reps": [15, 12, 9, 6, 3], "load": BB("135lb", "95lb")},
   {"exercise": "pull-up", "reps": [15, 12, 9, 6, 3]},
   {"exercise": "front-squat", "reps": [15, 12, 9, 6, 3], "load": BB("135lb", "95lb")},
   {"exercise": "pull-up", "reps": [15, 12, 9, 6, 3]}],
  "t-u-p", tags=["barbell", "gymnastics", "ladder"])

w("the-don", "The Don", "for_time",
  [{"exercise": "deadlift", "reps": 66, "load": BB("110lb", "70lb")},
   {"exercise": "box-jump", "reps": 66},
   {"exercise": "kettlebell-swing", "reps": 66, "load": BB("53lb", "35lb")},
   {"exercise": "knees-to-elbows", "reps": 66},
   {"exercise": "sit-up", "reps": 66},
   {"exercise": "pull-up", "reps": 66},
   {"exercise": "thruster", "reps": 66, "load": BB("55lb", "55lb")},
   {"exercise": "wall-ball-shot", "reps": 66, "load": BB("20lb", "14lb")},
   {"exercise": "burpee", "reps": 66},
   {"exercise": "double-under", "reps": 66}],
  "the-don-hero", tags=["barbell", "kettlebell", "high-volume"], notes=src("the-don-hero"))

w("tk", "TK", "amrap",
  [{"exercise": "strict-pull-up", "reps": 8},
   {"exercise": "box-jump", "reps": 8, "notes": "36-inch box (men) / 30-inch (women)"},
   {"exercise": "kettlebell-swing", "reps": 12, "load": BB("70lb", "53lb")}],
  "tk", format_meta=AM(20), tags=["amrap", "kettlebell", "gymnastics"])

w("tom", "Tom", "amrap",
  [{"exercise": "muscle-up", "reps": 7},
   {"exercise": "thruster", "reps": 11, "load": BB("155lb", "105lb")},
   {"exercise": "toes-to-bar", "reps": 14}],
  "tom", format_meta=AM(25), tags=["amrap", "barbell", "gymnastics"])

w("topsy", "Topsy", "amrap",
  [{"exercise": "ring-muscle-up", "reps": 3},
   {"exercise": "thruster", "reps": 8, "load": BB("115lb", "75lb")},
   {"exercise": "row", "reps": 17, "notes": "calories"}],
  "topsy", format_meta=AM(25), tags=["amrap", "barbell", "gymnastics"])

w("triple-deuce", "Triple Deuce", "amrap",
  [{"exercise": "burpee", "reps": 22},
   {"exercise": "air-squat", "reps": 22},
   {"exercise": "pull-up", "reps": 22},
   {"exercise": "sandbag-ground-to-shoulder", "reps": 22, "load": BB("60lb", "40lb")},
   {"exercise": "run", "distance_m": 722, "notes": "sprint"}],
  "triple-deuce", format_meta=AM(20), tags=["amrap", "sandbag", "bodyweight"])

w("tully", "Tully", "interval",
  [{"exercise": "swim", "distance_m": 200},
   {"exercise": "dumbbell-squat-clean", "reps": 23, "load": BB("40lb", "30lb")}],
  "tully", format_meta=RDS(4), tags=["swimming", "dumbbell", "4-rounds"])

w("tumilson", "Tumilson", "interval",
  [{"exercise": "run", "distance_m": 200},
   {"exercise": "dumbbell-burpee-deadlift", "reps": 11, "load": BB("60lb", "45lb")}],
  "tumilson-hero", format_meta=RDS(8), tags=["running", "dumbbell", "8-rounds"], notes=src("tumilson-hero"))

w("viola", "Viola", "amrap",
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "power-snatch", "reps": 11, "load": BB("95lb", "65lb")},
   {"exercise": "pull-up", "reps": 17},
   {"exercise": "power-clean", "reps": 13, "load": BB("95lb", "65lb")}],
  "viola", format_meta=AM(20), tags=["amrap", "barbell", "gymnastics"])

w("walsh", "Walsh", "interval",
  [{"exercise": "burpee-pull-up", "reps": 22},
   {"exercise": "back-squat", "reps": 22, "load": BB("185lb", "125lb")},
   {"exercise": "run", "distance_m": 200, "load": BB("45lb", "25lb"), "notes": "with a plate held overhead"}],
  "walsh", format_meta=RDS(4), tags=["barbell", "gymnastics", "running", "4-rounds"])

w("weaver", "Weaver", "interval",
  [{"exercise": "l-pull-up", "reps": 10}, {"exercise": "push-up", "reps": 15},
   {"exercise": "chest-to-bar-pull-up", "reps": 15}, {"exercise": "push-up", "reps": 15},
   {"exercise": "pull-up", "reps": 20}, {"exercise": "push-up", "reps": 15}],
  "weaver", format_meta=RDS(4), tags=["gymnastics", "bodyweight", "4-rounds"])

w("weston", "Weston", "interval",
  [{"exercise": "row", "distance_m": 1000},
   {"exercise": "farmers-carry", "distance_m": 200, "load": BB("45lb", "30lb")},
   {"exercise": "dumbbell-waiters-walk", "distance_m": 50, "load": BB("45lb", "30lb"), "notes": "right arm"},
   {"exercise": "dumbbell-waiters-walk", "distance_m": 50, "load": BB("45lb", "30lb"), "notes": "left arm"}],
  "weston", format_meta=RDS(5), tags=["rowing", "dumbbell", "5-rounds"])

w("white", "White", "interval",
  [{"exercise": "rope-climb", "reps": 3, "notes": "to 15 feet"},
   {"exercise": "toes-to-bar", "reps": 10},
   {"exercise": "overhead-walking-lunge", "reps": 21, "load": BB("45lb", "25lb"), "notes": "plate held overhead"},
   {"exercise": "run", "distance_m": 400}],
  "white-hero", format_meta=RDS(5), tags=["gymnastics", "barbell", "running", "5-rounds"])

w("whitt", "Whitt", "interval",
  [{"exercise": "run", "distance_m": 800, "notes": "carrying a 30/20 lb medicine ball"},
   {"exercise": "wall-ball-shot", "reps": 30, "load": BB("30lb", "20lb")},
   {"exercise": "ball-slam", "reps": 30, "load": BB("30lb", "20lb")}],
  "whitt-hero", format_meta=RDS(3), tags=["running", "3-rounds"])

w("whitten", "Whitten", "interval",
  [{"exercise": "kettlebell-swing", "reps": 22, "load": BB("72lb", "53lb")},
   {"exercise": "box-jump", "reps": 22},
   {"exercise": "run", "distance_m": 400},
   {"exercise": "burpee", "reps": 22},
   {"exercise": "wall-ball-shot", "reps": 22, "load": BB("20lb", "14lb")}],
  "whitten", format_meta=RDS(5), tags=["kettlebell", "running", "5-rounds"])

w("willy", "Willy", "interval",
  [{"exercise": "run", "distance_m": 800},
   {"exercise": "front-squat", "reps": 5, "load": BB("225lb", "155lb")},
   {"exercise": "run", "distance_m": 200},
   {"exercise": "chest-to-bar-pull-up", "reps": 11},
   {"exercise": "run", "distance_m": 400},
   {"exercise": "kettlebell-swing", "reps": 12, "load": BB("70lb", "53lb")}],
  "willy", format_meta=RDS(3), tags=["running", "barbell", "kettlebell", "3-rounds"])

w("wyk", "Wyk", "interval",
  [{"exercise": "front-squat", "reps": 5, "load": BB("225lb", "155lb")},
   {"exercise": "rope-climb", "reps": 5, "notes": "to 15 feet"},
   {"exercise": "run", "distance_m": 400, "load": BB("45lb", "25lb"), "notes": "carrying a plate"}],
  "wyk", format_meta=RDS(5), tags=["barbell", "gymnastics", "running", "5-rounds"])

w("yeti", "Yeti", "for_time",
  [{"exercise": "pull-up", "reps": 25},
   {"exercise": "muscle-up", "reps": 10},
   {"exercise": "run", "distance_m": 2414},
   {"exercise": "muscle-up", "reps": 10},
   {"exercise": "pull-up", "reps": 25}],
  "yeti", tags=["gymnastics", "running"])

w("zeus", "Zeus", "interval",
  [{"exercise": "wall-ball-shot", "reps": 30, "load": BB("20lb", "14lb")},
   {"exercise": "sumo-deadlift-high-pull", "reps": 30, "load": BB("75lb", "55lb")},
   {"exercise": "box-jump", "reps": 30},
   {"exercise": "push-press", "reps": 30, "load": BB("75lb", "55lb")},
   {"exercise": "row", "reps": 30, "notes": "calories"},
   {"exercise": "push-up", "reps": 30},
   {"exercise": "back-squat", "reps": 10, "notes": "bodyweight"}],
  "zeus", format_meta=RDS(3), tags=["barbell", "high-volume", "3-rounds"])

w("zimmerman", "Zimmerman", "amrap",
  [{"exercise": "chest-to-bar-pull-up", "reps": 11},
   {"exercise": "deadlift", "reps": 2, "load": BB("315lb", "205lb")},
   {"exercise": "handstand-push-up", "reps": 10}],
  "zimmerman", format_meta=AM(25), tags=["amrap", "barbell", "gymnastics"])

print(f"Wrote batch-4 wave-3 entries; heroes dir now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
