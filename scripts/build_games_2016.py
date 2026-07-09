import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games individual events -- 2016. Each verified against its official
# games.crossfit.com/workouts/games/2016/<n> page, cross-referenced via
# independent sources for events whose primary page 404'd. No events skipped
# this year -- all 15 have a genuine fixed prescription.
def src(year, n):
    return (f"games.crossfit.com/workouts/games/{year}/{n} "
            f"(official CrossFit Games event), retrieved {TODAY}")

def w(id, name, fmt, slug, movements=None, segments=None, format_meta=None, tags=None, notes=None):
    entry = {
        "id": id, "name": name, "category": "games", "format": fmt,
        "format_meta": format_meta or {},
        "movements": movements or [],
        "partition": None, "scaling": None, "origin": None,
        "tags": tags or [], "source_notes": notes or src(*slug),
        "schema_version": VER, "last_updated": TODAY,
    }
    if segments is not None:
        entry["segments"] = segments
    with open(os.path.join(OUT, f"{id}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(entry, f, indent=2)
        f.write("\n")

BB = lambda m, f: {"rx_male": m, "rx_female": f}
CAP = lambda n: {"time_cap_minutes": n, "scoring": "time"}

w("games-16-ranch-trail-run", "Ranch Trail Run", "for_time", (2016, 1),
  [{"exercise": "run", "distance_m": 7000}], tags=["games", "2016", "running", "outdoor", "endurance"])

w("games-16-ranch-deadlift-ladder", "Ranch Deadlift Ladder", "max_load", (2016, 2),
  [{"exercise": "deadlift", "reps": 1,
    "notes": "one lift every 30 seconds through a series of 20 barbells, each heavier than the last; "
              "men 425-615 lb, women 275-415 lb (full published ladder); athletes lift in reverse order "
              "of their Event 1 run finish"}],
  format_meta={"scoring": "load"}, tags=["games", "2016", "barbell", "max-load", "ladder"])

w("games-16-ranch-mini-chipper", "Ranch Mini Chipper", "for_time", (2016, 3),
  [{"exercise": "wall-ball-shot", "reps": 50, "load": BB("30lb", "20lb")},
   {"exercise": "medicine-ball-sit-up", "reps": 25, "load": BB("30lb", "20lb"), "notes": "GHD sit-up variant"},
   {"exercise": "sprint", "notes": "hill sprint, carrying the medicine ball"}],
  tags=["games", "2016", "outdoor", "hill"])

w("games-16-ocean-swim", "Ocean Swim", "for_time", (2016, 4),
  [{"exercise": "swim", "distance_m": 500, "notes": "starts and finishes on the beach, around 2 buoys"}],
  tags=["games", "2016", "swim", "open-water"])

w("games-16-murph", "Murph (2016 Games)", "for_time", (2016, 5),
  [{"exercise": "run", "distance_m": 1609},
   {"exercise": "pull-up", "reps": 100}, {"exercise": "push-up", "reps": 200}, {"exercise": "air-squat", "reps": 300},
   {"exercise": "run", "distance_m": 1609}],
  format_meta=CAP(55), tags=["games", "2016", "running", "gymnastics", "weighted", "high-volume"],
  notes=src(2016, 5) + "; the Hero WOD Murph, performed with a 20 lb (men) / 14 lb (women) weight vest and a 55-minute cap")

w("games-16-squat-clean-pyramid", "Squat Clean Pyramid", "multi_part", (2016, 6),
  segments=[
    {"label": "By 2:00", "format": "for_time", "format_meta": CAP(2),
     "movements": [{"exercise": "squat-clean", "reps": 10, "load": BB("245lb", "165lb")}]},
    {"label": "By 4:00", "format": "for_time", "format_meta": CAP(2),
     "movements": [{"exercise": "squat-clean", "reps": 8, "load": BB("265lb", "180lb")}]},
    {"label": "By 6:00", "format": "for_time", "format_meta": CAP(2),
     "movements": [{"exercise": "squat-clean", "reps": 6, "load": BB("285lb", "195lb")}]},
    {"label": "By 8:00", "format": "for_time", "format_meta": CAP(2),
     "movements": [{"exercise": "squat-clean", "reps": 4, "load": BB("305lb", "205lb")}]},
    {"label": "By 11:00", "format": "for_time", "format_meta": CAP(3),
     "movements": [{"exercise": "squat-clean", "reps": 2, "load": BB("325lb", "215lb")}]},
  ],
  tags=["games", "2016", "barbell", "ladder"],
  notes=src(2016, 6) + "; an athlete unable to complete all reps at a bar is credited with reps completed and ranked by their last fully-completed stage")

w("games-16-double-dt", "Double DT", "interval", (2016, 7),
  [{"exercise": "deadlift", "reps": 12, "load": BB("155lb", "105lb")},
   {"exercise": "hang-power-clean", "reps": 9, "load": BB("155lb", "105lb")},
   {"exercise": "push-jerk", "reps": 6, "load": BB("155lb", "105lb")}],
  format_meta={"rounds": 10, "time_cap_minutes": 15, "scoring": "time"},
  tags=["games", "2016", "barbell", "10-rounds"])

w("games-16-climbing-snail", "Climbing Snail", "interval", (2016, 8),
  [{"exercise": "run", "distance_m": 500, "notes": "berm run"},
   {"exercise": "rope-climb", "reps": 2},
   {"exercise": "sled-push", "distance_m": 12, "notes": "40 ft, \"Snail\" apparatus"},
   {"exercise": "rope-climb", "reps": 2}],
  format_meta={"rounds": 3, "time_cap_minutes": 21, "scoring": "time"},
  tags=["games", "2016", "venue-equipment", "running", "gymnastics"],
  notes=src(2016, 8) + "; only 1 rope ascent (not 2) on the final round")

w("games-16-the-separator", "The Separator", "for_time", (2016, 9),
  [{"exercise": "ring-handstand-push-up", "reps": 12},
   {"exercise": "back-squat", "reps": 15, "load": BB("225lb", "165lb")},
   {"exercise": "burpee", "reps": 20},
   {"exercise": "ring-handstand-push-up", "reps": 9},
   {"exercise": "front-squat", "reps": 18, "load": BB("205lb", "145lb")},
   {"exercise": "burpee", "reps": 20},
   {"exercise": "ring-handstand-push-up", "reps": 6},
   {"exercise": "overhead-squat", "reps": 21, "load": BB("185lb", "125lb")},
   {"exercise": "burpee", "reps": 20}],
  format_meta=CAP(16),
  tags=["games", "2016", "barbell", "gymnastics"],
  notes=src(2016, 9) + "; time cap 16 minutes (women); men's cap not confirmed from available sources. "
        "One source described a slightly different women's movement order/rep count (ring HSPU descending "
        "6-4-2 vs. the men's 12-9-6) that could not be fully corroborated -- this entry uses the men's "
        "structure, flagged per CONTRIBUTING")

w("games-16-100-percent", "100%", "for_time", (2016, 10),
  [{"exercise": "box-jump", "reps": 40, "notes": "30 in (men) / 24 in (women) box"},
   {"exercise": "d-ball-clean", "reps": 20, "load": BB("150lb", "100lb")}],
  format_meta=CAP(5), tags=["games", "2016", "venue-equipment"],
  notes=src(2016, 10) + "; a surprise final event -- athletes learned the prescription only an hour before competing")

w("games-16-handstand-walk", "Handstand Walk (2016 Games)", "for_time", (2016, 11),
  [{"exercise": "handstand-walk", "distance_m": 85, "notes": "280 ft; every 20 ft section must be unbroken"}],
  tags=["games", "2016", "gymnastics"])

w("games-16-suicide-sprint", "Suicide Sprint", "for_time", (2016, 12),
  [{"exercise": "shuttle-sprint", "distance_m": 256,
    "notes": "840 ft total on a 280 ft course: 1/3 down and back, 2/3 down and back, then a full sprint the length of the course"}],
  tags=["games", "2016", "outdoor"])

w("games-16-the-plow", "The Plow", "for_time", (2016, 13),
  [{"exercise": "sled-pull", "distance_m": 171, "load": BB("235lb", "190lb"), "notes": "560 ft, \"Plow\" drag apparatus"}],
  tags=["games", "2016", "venue-equipment"])

w("games-16-rope-chipper", "Rope Chipper", "for_time", (2016, 14),
  [{"exercise": "ski-erg", "distance_m": 200},
   {"exercise": "double-under", "reps": 50, "notes": "weighted-handle rope (women use 40)"},
   {"exercise": "row", "distance_m": 200},
   {"exercise": "double-under", "reps": 50, "notes": "weighted-handle rope (women use 40)"},
   {"exercise": "assault-bike", "distance_m": 644, "notes": "0.4 miles"},
   {"exercise": "double-under", "reps": 50, "notes": "weighted-handle rope (women use 40)"},
   {"exercise": "row", "distance_m": 200},
   {"exercise": "double-under", "reps": 50, "notes": "weighted-handle rope (women use 40)"},
   {"exercise": "ski-erg", "distance_m": 200},
   {"exercise": "sled-pull", "distance_m": 27, "load": BB("310lb", "220lb"), "notes": "90 ft"}],
  format_meta=CAP(11), tags=["games", "2016", "venue-equipment", "rowing", "jump-rope"],
  notes=src(2016, 14) + "; debuted the ski erg in Games competition")

w("games-16-redemption", "Redemption", "for_time", (2016, 15),
  [{"exercise": "pegboard", "reps": 3},
   {"exercise": "thruster", "reps": 21, "load": BB("135lb", "85lb")},
   {"exercise": "pegboard", "reps": 2},
   {"exercise": "thruster", "reps": 15, "load": BB("135lb", "85lb")},
   {"exercise": "pegboard", "reps": 1},
   {"exercise": "thruster", "reps": 9, "load": BB("135lb", "85lb")}],
  format_meta=CAP(10), tags=["games", "2016", "venue-equipment", "barbell", "ladder"])

print(f"Wrote 2016 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
