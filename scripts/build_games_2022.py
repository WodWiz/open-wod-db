import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games individual events -- 2022. Each verified against its official
# games.crossfit.com/workouts/games/2022/<n> page, cross-referenced via search
# for events whose primary page 404'd.
#
# SKIPPED: Event 2 "Skill Speed Medley" -- a heat-based bracket race with
# progressive elimination rounds (quarterfinal/semifinal/final each cutting the
# field), not a fixed single prescription; left out per the Games scoping
# decision (ROADMAP.md).
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
CAP = lambda n: {"time_cap_minutes": n, "scoring": "time"}

w("games-22-bike-to-work", "Bike to Work", "for_time", (2022, 1),
  [{"exercise": "toes-to-bar", "reps": 75},
   {"exercise": "bike", "distance_m": 8047, "notes": "5 miles; 5 laps of a 1-mile course"},
   {"exercise": "chest-to-bar-pull-up", "reps": 75},
   {"exercise": "bike", "distance_m": 8047, "notes": "5 miles; 5 laps of a 1-mile course"}],
  format_meta=CAP(50), tags=["games", "2022", "outdoor", "gymnastics"])

w("games-22-elizabeth-elevated", "Elizabeth Elevated", "for_time", (2022, 3),
  [{"exercise": "squat-clean", "reps": [21, 15, 9, 9, 9], "load": BB("135lb", "95lb")},
   {"exercise": "bar-dip", "reps": [21, 15, 9, 9, 9],
    "notes": "split into 3 unbroken sets per round, each set beginning with a parallel bar traverse"}],
  format_meta={"time_cap_minutes": 10, "scoring": "time"},
  tags=["games", "2022", "barbell", "gymnastics"],
  notes=src(2022, 3) + "; time cap 10 minutes (men) / 12 minutes (women)")

w("games-22-shuttle-to-overhead", "Shuttle to Overhead", "multi_part", (2022, 4),
  segments=[
    {"label": "0:00-2:00", "format": "for_time", "format_meta": CAP(2),
     "movements": [{"exercise": "run", "distance_m": 400},
                   {"exercise": "jerk", "reps": "max", "load": BB("200lb", "155lb"), "notes": "max reps in time remaining"}],
     "rest_after_seconds": 60},
    {"label": "3:00-6:00", "format": "for_time", "format_meta": CAP(3),
     "movements": [{"exercise": "run", "distance_m": 600},
                   {"exercise": "jerk", "reps": "max", "load": BB("200lb", "155lb"), "notes": "max reps in time remaining"}],
     "rest_after_seconds": 120},
    {"label": "8:00-12:00", "format": "for_time", "format_meta": CAP(4),
     "movements": [{"exercise": "run", "distance_m": 800},
                   {"exercise": "jerk", "reps": "max", "load": BB("200lb", "155lb"), "notes": "max reps in time remaining"}]},
  ],
  tags=["games", "2022", "barbell", "running"],
  notes=src(2022, 4) + "; scored as two separate events: total time to complete the three "
        "runs, and cumulative jerks across all rounds")

w("games-22-the-capitol", "The Capitol", "for_time", (2022, 5),
  [{"exercise": "d-ball-over-shoulder", "reps": 20, "notes": "\"pig flips\""},
   {"exercise": "run", "distance_m": 5633, "notes": "3.5 miles"},
   {"exercise": "jerry-bag-carry", "distance_m": 183, "load": BB("100lb", "70lb"), "notes": "200 m; two bags"},
   {"exercise": "husafell-carry", "distance_m": 183, "load": BB("200lb", "150lb"), "notes": "200 m"}],
  tags=["games", "2022", "venue-equipment", "outdoor"],
  notes=src(2022, 5) + "; course runs from Alliant Energy Center to the Wisconsin State Capitol; reps/distances/loads are fixed and standardized despite the location-specific route")

w("games-22-up-and-over", "Up and Over", "interval", (2022, 6),
  [{"exercise": "muscle-up", "reps": 12},
   {"exercise": "box-jump-over", "reps": 25, "notes": "over a 50 in log, 30 in box, and 20 in \"Pig\" in sequence"},
   {"exercise": "ghd-sit-up", "reps": 30}],
  format_meta={"rounds": 3, "time_cap_minutes": 18, "scoring": "time"},
  tags=["games", "2022", "venue-equipment", "gymnastics"],
  notes=src(2022, 6) + "; followed by an 84 ft weighted lunge with a 125 lb (women) axle bar to finish")

w("games-22-echo-press", "Echo Press", "for_time", (2022, 7),
  [{"exercise": "echo-bike", "reps": 30, "notes": "calories (women use 25)"},
   {"exercise": "deficit-handstand-push-up", "reps": 10, "notes": "2 in deficit, performed from an elevated block"},
   {"exercise": "echo-bike", "reps": 20, "notes": "calories (women use 15)"},
   {"exercise": "deficit-handstand-push-up", "reps": 10, "notes": "2 in deficit, performed from an elevated block"},
   {"exercise": "echo-bike", "reps": 20, "notes": "calories (women use 15)"},
   {"exercise": "deficit-handstand-push-up", "reps": 10, "notes": "2 in deficit, performed from an elevated block"},
   {"exercise": "echo-bike", "reps": 30, "notes": "calories (women use 25)"}],
  format_meta=CAP(12), tags=["games", "2022", "venue-equipment", "gymnastics"])

w("games-22-rinse-n-repeat", "Rinse 'N' Repeat", "interval", (2022, 8),
  [{"exercise": "swim", "distance_m": 46, "notes": "50 yd; 25 yd down, 25 yd back"},
   {"exercise": "ski-erg", "reps": 8, "notes": "calories; add 2 calories each round for 6 rounds, then max calories for rounds 7-8"}],
  format_meta={"rounds": 8, "interval_seconds": 120, "scoring": "reps"},
  tags=["games", "2022", "swim", "venue-equipment"],
  notes=src(2022, 8) + "; every 2 minutes for up to 8 rounds")

w("games-22-hat-trick", "Hat Trick", "interval", (2022, 9),
  [{"exercise": "sprint"},
   {"exercise": "wall-ball-shot", "reps": 20, "load": BB("20lb", "14lb"), "notes": "12 ft (men) / 11 ft (women) target"},
   {"exercise": "alternating-dumbbell-snatch", "reps": 6, "load": BB("100lb", "70lb")}],
  format_meta={"rounds": 3, "interval_seconds": 120, "rest_seconds": 240, "scoring": "time"},
  tags=["games", "2022", "dumbbell"],
  notes=src(2022, 9) + "; 2 minutes per round then 4 minutes rest; performed in two overlapping heats")

w("games-22-sandbag-ladder", "Sandbag Ladder", "max_load", (2022, 10),
  [{"exercise": "sandbag-clean", "reps": 1,
    "load": BB("240-340lb (ladder)", "160-250lb (ladder)"),
    "notes": "to one shoulder, may release one hand to show control; progressively heavier sandbags until failure to lift"}],
  format_meta={"scoring": "load"},
  tags=["games", "2022", "max-load", "venue-equipment"],
  notes=src(2022, 10) + "; exact intermediate ladder increments between the confirmed "
        "endpoints (240-340 lb men, 160-250 lb women) are not confirmed from available "
        "sources -- flagged per CONTRIBUTING rather than guessed; tiebreak was a 3-sandbag "
        "toss over a yoke (100/150/200 lb men, 50/100/150 lb women)")

w("games-22-the-alpaca", "The Alpaca", "for_time", (2022, 11),
  [{"exercise": "sled-push", "distance_m": 38, "notes": "126 ft; starts loaded with all six kettlebells, removed progressively during the push"},
   {"exercise": "kettlebell-clean-and-jerk", "reps": 20, "load": BB("70lb", "53lb"), "notes": "32 kg (men) / 24 kg (women)"},
   {"exercise": "sled-push", "distance_m": 13, "load": BB("70lb", "53lb"), "notes": "42 ft; 2 kettlebells"},
   {"exercise": "kettlebell-clean-and-jerk", "reps": 15, "load": BB("70lb", "53lb")},
   {"exercise": "sled-push", "distance_m": 13, "load": BB("70lb", "53lb"), "notes": "42 ft; 4 kettlebells"},
   {"exercise": "kettlebell-clean-and-jerk", "reps": 10, "load": BB("70lb", "53lb")},
   {"exercise": "sled-push", "distance_m": 13, "load": BB("70lb", "53lb"), "notes": "42 ft; 6 kettlebells"}],
  format_meta=CAP(18), tags=["games", "2022", "venue-equipment", "kettlebell"],
  notes=src(2022, 11) + "; originally included legless rope climbs between each sled push/"
        "kettlebell station, but these were removed for weather/safety reasons in the "
        "version actually contested -- this entry reflects the as-performed version; the "
        "exact load-removal mechanic during the initial 126 ft push is not precisely "
        "confirmed from available sources, flagged per CONTRIBUTING")

w("games-22-back-nine", "Back Nine", "for_time", (2022, 12),
  [{"exercise": "yoke-carry", "distance_m": 16, "load": BB("665lb", "485lb"), "notes": "54 ft"},
   {"exercise": "front-squat", "reps": 2, "load": BB("315lb", "215lb")},
   {"exercise": "deadlift", "reps": 3, "load": BB("475lb", "315lb")},
   {"exercise": "front-squat", "reps": 2, "load": BB("315lb", "215lb")},
   {"exercise": "yoke-carry", "distance_m": 16, "load": BB("665lb", "485lb"), "notes": "54 ft"}],
  format_meta=CAP(4), tags=["games", "2022", "venue-equipment", "barbell", "max-effort"])

w("games-22-jackie-pro", "Jackie Pro", "for_time", (2022, 13),
  [{"exercise": "row", "distance_m": 1000,
    "notes": "must be completed within 3:15 (men) / 3:40 (women) to continue"},
   {"exercise": "thruster", "reps": 50, "load": BB("95lb", "65lb")},
   {"exercise": "bar-muscle-up", "reps": 30}],
  tags=["games", "2022", "rowing", "barbell", "gymnastics"],
  notes=src(2022, 13) + "; a heavier-loaded, bar-muscle-up variant of the Girl WOD Jackie, "
        "with a qualifying row-time standard to continue to the thrusters/muscle-ups")

print(f"Wrote 2022 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
