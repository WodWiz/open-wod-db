import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "girls")
os.makedirs(OUT, exist_ok=True)
SRC = "crossfit.com/faq/wod (official CrossFit FAQ, 'Explain The Workouts with Names (the Girls)?'), retrieved 2026-07-08"
VER = "1.0"
TODAY = "2026-07-08"

def w(id, name, category, format, movements, format_meta=None, partition=None,
      origin_summary=None, first_posted=None, tags=None, notes=None):
    entry = {
        "id": id, "name": name, "category": category, "format": format,
        "format_meta": format_meta or {},
        "movements": movements,
        "partition": partition,
        "scaling": None,
        "origin": {"summary": origin_summary, "first_posted": first_posted} if origin_summary or first_posted else None,
        "tags": tags or [],
        "description": DESCRIPTIONS.get(id),
        "source_notes": notes or SRC,
        "schema_version": VER,
        "last_updated": TODAY,
    }
    with open(os.path.join(OUT, f"{id}.json"), "w") as f:
        json.dump(entry, f, indent=2)
        f.write("\n")

L = lambda male, female: {"rx_male": male, "rx_female": female}

w("angie", "Angie", "girl", "for_time",
  [{"exercise": "pull-up", "reps": 100}, {"exercise": "push-up", "reps": 100},
   {"exercise": "sit-up", "reps": 100}, {"exercise": "air-squat", "reps": 100}],
  first_posted="2004-07-26", tags=["bodyweight", "high-volume"])

w("barbara", "Barbara", "girl", "interval",
  [{"exercise": "pull-up", "reps": 20}, {"exercise": "push-up", "reps": 30},
   {"exercise": "sit-up", "reps": 40}, {"exercise": "air-squat", "reps": 50}],
  format_meta={"rounds": 5, "rest_between_seconds": 180, "scoring": "time"},
  first_posted="2003-09-27", tags=["bodyweight", "5-rounds"])

w("chelsea", "Chelsea", "girl", "emom",
  [{"exercise": "pull-up", "reps": 5}, {"exercise": "push-up", "reps": 10}, {"exercise": "air-squat", "reps": 15}],
  format_meta={"interval_seconds": 60, "total_minutes": 30},
  first_posted="2003-09-07", tags=["bodyweight", "emom"])

w("cindy", "Cindy", "girl", "amrap",
  [{"exercise": "pull-up", "reps": 5}, {"exercise": "push-up", "reps": 10}, {"exercise": "air-squat", "reps": 15}],
  format_meta={"time_cap_minutes": 20},
  first_posted="2004-12-29", tags=["bodyweight", "amrap", "triplet"])

w("diane", "Diane", "girl", "for_time",
  [{"exercise": "deadlift", "reps": [21, 15, 9], "load": L("225lb", "225lb")},
   {"exercise": "handstand-push-up", "reps": [21, 15, 9]}],
  first_posted="2003-09-19", tags=["couplet", "barbell", "gymnastics"])

w("elizabeth", "Elizabeth", "girl", "for_time",
  [{"exercise": "clean", "reps": [21, 15, 9], "load": L("135lb", "135lb")},
   {"exercise": "ring-dip", "reps": [21, 15, 9]}],
  first_posted="2003-09-12", tags=["couplet", "barbell", "gymnastics"])

w("fran", "Fran", "girl", "for_time",
  [{"exercise": "thruster", "reps": [21, 15, 9], "load": L("95lb", "65lb")},
   {"exercise": "pull-up", "reps": [21, 15, 9]}],
  first_posted="2003-08-25", tags=["couplet", "sprint", "barbell", "gymnastics"])

w("grace", "Grace", "girl", "for_time",
  [{"exercise": "clean-and-jerk", "reps": 30, "load": L("135lb", "135lb")}],
  first_posted="2004-06-24", tags=["single-movement", "barbell", "sprint"])

w("helen", "Helen", "girl", "interval",
  [{"exercise": "run", "distance_m": 400}, {"exercise": "kettlebell-swing", "reps": 21, "load": L("1.5 pood", "1.5 pood")},
   {"exercise": "pull-up", "reps": 12}],
  format_meta={"rounds": 3, "scoring": "time"},
  first_posted="2003-08-09", tags=["running", "kettlebell", "gymnastics"])

w("isabel", "Isabel", "girl", "for_time",
  [{"exercise": "snatch", "reps": 30, "load": L("135lb", "135lb")}],
  first_posted="2004-11-11", tags=["single-movement", "barbell", "sprint"])

w("jackie", "Jackie", "girl", "for_time",
  [{"exercise": "row", "distance_m": 1000}, {"exercise": "thruster", "reps": 50, "load": L("45lb", "45lb")},
   {"exercise": "pull-up", "reps": 30}],
  first_posted="2005-08-03", tags=["triplet", "rowing", "barbell"])

w("karen", "Karen", "girl", "for_time",
  [{"exercise": "wall-ball-shot", "reps": 150, "load": L("20lb", "14lb")}],
  first_posted="2008-08-07", tags=["single-movement", "high-volume"])

w("linda", "Linda", "girl", "for_time",
  [{"exercise": "deadlift", "reps": [10,9,8,7,6,5,4,3,2,1], "load": L("1.5x bodyweight", "1.5x bodyweight")},
   {"exercise": "bench-press", "reps": [10,9,8,7,6,5,4,3,2,1], "load": L("bodyweight", "bodyweight")},
   {"exercise": "clean", "reps": [10,9,8,7,6,5,4,3,2,1], "load": L("0.75x bodyweight", "0.75x bodyweight")}],
  first_posted="2003-07-05", tags=["descending-ladder", "bodyweight-relative", "barbell"])

w("mary", "Mary", "girl", "amrap",
  [{"exercise": "handstand-push-up", "reps": 5}, {"exercise": "pistol", "reps": 10, "notes": "alternating legs"},
   {"exercise": "pull-up", "reps": 15}],
  format_meta={"time_cap_minutes": 20},
  first_posted="2005-01-19", tags=["amrap", "gymnastics", "triplet"])

w("nancy", "Nancy", "girl", "interval",
  [{"exercise": "run", "distance_m": 400}, {"exercise": "overhead-squat", "reps": 15, "load": L("95lb", "65lb")}],
  format_meta={"rounds": 5, "scoring": "time"},
  first_posted="2004-12-05", tags=["running", "barbell"])

w("annie", "Annie", "girl", "for_time",
  [{"exercise": "double-under", "reps": [50,40,30,20,10]}, {"exercise": "sit-up", "reps": [50,40,30,20,10]}],
  first_posted="2005-04-16", tags=["couplet", "descending-ladder", "jump-rope"])

w("eva", "Eva", "girl", "interval",
  [{"exercise": "run", "distance_m": 800}, {"exercise": "kettlebell-swing", "reps": 30, "load": L("2 pood", "2 pood")},
   {"exercise": "pull-up", "reps": 30}],
  format_meta={"rounds": 5, "scoring": "time"},
  first_posted="2008-02-24", tags=["running", "kettlebell", "gymnastics"])

w("kelly", "Kelly", "girl", "interval",
  [{"exercise": "run", "distance_m": 400}, {"exercise": "box-jump", "reps": 30, "notes": "24in box"},
   {"exercise": "wall-ball-shot", "reps": 30, "load": L("20lb", "20lb")}],
  format_meta={"rounds": 5, "scoring": "time"},
  first_posted="2005-04-10", tags=["running", "box-jump"])

w("lynne", "Lynne", "girl", "interval",
  [{"exercise": "bench-press", "reps": "max", "load": L("bodyweight", "bodyweight")},
   {"exercise": "pull-up", "reps": "max"}],
  format_meta={"rounds": 5, "scoring": "reps"},
  first_posted="2004-04-22", tags=["max-reps", "strength", "bodyweight-relative"])

w("nicole", "Nicole", "girl", "amrap",
  [{"exercise": "run", "distance_m": 400}, {"exercise": "pull-up", "reps": "max"}],
  format_meta={"time_cap_minutes": 20, "scoring": "rounds_reps"},
  first_posted="2006-12-11", tags=["running", "amrap"])

w("amanda", "Amanda", "girl", "for_time",
  [{"exercise": "muscle-up", "reps": [9,7,5]}, {"exercise": "squat-snatch", "reps": [9,7,5], "load": L("135lb", "135lb")}],
  first_posted="2010-07-17", tags=["couplet", "gymnastics", "barbell", "high-skill"])

w("gwen", "Gwen", "girl", "max_load",
  [{"exercise": "clean-and-jerk", "reps": [15,12,9], "notes": "touch and go at floor only; no dumping; same load across all sets; rest as needed"}],
  format_meta={"scoring": "load"},
  first_posted="2003-05-25", tags=["load-test", "barbell", "touch-and-go"])

w("marguerita", "Marguerita", "girl", "for_time",
  [{"exercise": "burpee", "reps": 50}, {"exercise": "push-up", "reps": 50},
   {"exercise": "jumping-jack", "reps": 50}, {"exercise": "sit-up", "reps": 50}, {"exercise": "handstand", "reps": 50}],
  first_posted="2014-01-15", tags=["bodyweight", "high-volume"])

w("candy", "Candy", "girl", "interval",
  [{"exercise": "pull-up", "reps": 20}, {"exercise": "push-up", "reps": 40}, {"exercise": "air-squat", "reps": 60}],
  format_meta={"rounds": 5, "scoring": "time"},
  tags=["bodyweight", "5-rounds"])

w("maggie", "Maggie", "girl", "interval",
  [{"exercise": "handstand-push-up", "reps": 20}, {"exercise": "pull-up", "reps": 40},
   {"exercise": "pistol", "reps": 60, "notes": "alternating legs"}],
  format_meta={"rounds": 5, "scoring": "time"},
  first_posted="2006-07-28", tags=["bodyweight", "gymnastics", "5-rounds"])

w("hope", "Hope", "girl", "interval",
  [{"exercise": "burpee"}, {"exercise": "power-snatch", "load": L("75lb", "75lb")},
   {"exercise": "box-jump", "notes": "24in box"}, {"exercise": "thruster", "load": L("75lb", "75lb")},
   {"exercise": "chest-to-bar-pull-up"}],
  format_meta={"rounds": 3, "interval_seconds": 60, "scoring": "reps"},
  origin_summary="Same format as Fight Gone Bad: five one-minute stations, one-minute rest between rounds, clock runs continuously, scored by total reps across stations.",
  first_posted="2012-06-08", tags=["fgb-format", "station-based"])

w("grettel", "Grettel", "girl", "for_time",
  [{"exercise": "clean-and-jerk", "reps": 3, "load": L("135lb", "95lb")},
   {"exercise": "burpee-over-the-bar", "reps": 3}],
  format_meta={"rounds": 10, "scoring": "time"},
  first_posted="2021-01-03", tags=["couplet", "barbell", "10-rounds"])

w("ingrid", "Ingrid", "girl", "for_time",
  [{"exercise": "snatch", "reps": 3, "load": L("135lb", "95lb")}, {"exercise": "burpee-over-the-bar", "reps": 3}],
  format_meta={"rounds": 10, "scoring": "time"},
  first_posted="2021-01-03", tags=["couplet", "barbell", "10-rounds"])

w("barbara-ann", "Barbara Ann", "girl", "interval",
  [{"exercise": "handstand-push-up", "reps": 20}, {"exercise": "deadlift", "reps": 30, "load": L("135lb", "95lb")},
   {"exercise": "sit-up", "reps": 40}, {"exercise": "double-under", "reps": 50}],
  format_meta={"rounds": 5, "rest_between_seconds": 180, "scoring": "time"},
  first_posted="2021-01-04", tags=["5-rounds", "gymnastics", "barbell"])

w("lyla", "Lyla", "girl", "for_time",
  [{"exercise": "muscle-up", "reps": [10,9,8,7,6,5,4,3,2,1]},
   {"exercise": "bodyweight-clean-and-jerk", "reps": [10,9,8,7,6,5,4,3,2,1]}],
  first_posted="2021-01-07", tags=["couplet", "descending-ladder", "gymnastics", "bodyweight-relative"])

w("ellen", "Ellen", "girl", "for_time",
  [{"exercise": "burpee", "reps": 20}, {"exercise": "dumbbell-snatch", "reps": 21, "load": L("50lb", "35lb")},
   {"exercise": "dumbbell-thruster", "reps": 12, "load": L("50lb", "35lb"), "notes": "pair of dumbbells"}],
  format_meta={"rounds": 3, "scoring": "time"},
  first_posted="2021-01-10", tags=["triplet", "dumbbell", "3-rounds"])

w("andi", "Andi", "girl", "for_time",
  [{"exercise": "hang-power-snatch", "reps": 100, "load": L("65lb", "45lb")},
   {"exercise": "push-press", "reps": 100, "load": L("65lb", "45lb")},
   {"exercise": "sumo-deadlift-high-pull", "reps": 100, "load": L("65lb", "45lb")},
   {"exercise": "front-squat", "reps": 100, "load": L("65lb", "45lb")}],
  first_posted="2021-01-14", tags=["high-volume", "barbell"])

w("lane", "Lane", "girl", "interval",
  [{"exercise": "hang-power-snatch", "reps": "max", "load": L("0.75x bodyweight", "0.75x bodyweight")},
   {"exercise": "handstand-push-up", "reps": "max"}],
  format_meta={"rounds": 5, "scoring": "reps"},
  first_posted="2021-01-26", tags=["max-reps", "gymnastics", "bodyweight-relative"])

print(f"Wrote {len(os.listdir(OUT))} Girls entries to {OUT}")
