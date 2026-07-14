import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-10"

# CrossFit Games individual events -- 2012. Each verified against its official
# games.crossfit.com/workouts/games/2012/<n> page, cross-referenced via
# independent sources for events whose primary page 404'd.
#
# SKIPPED (per the Games scoping decision in ROADMAP.md):
# - Event 10 "Obstacle Course" -- a bracketed head-to-head military obstacle
#   course race at Camp Pendleton, not a fixed single prescription.
# - Event 14 "Sprint" -- a 300-yard shuttle contested in heats ("Sprint/
#   Rope-Sled: Men Heat 1/2/4..."), a pure race with no fixed reps.
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

w("games-12-ball-toss", "Ball Toss", "max_effort", (2012, 1),
  [{"exercise": "medicine-ball-throw", "load": BB("4lb", "2lb"),
    "notes": "seated in a GHD machine; scored by furthest throw"}],
  format_meta={"scoring": "load"}, tags=["games", "2012", "venue-equipment", "max-effort"])

w("games-12-broad-jump", "Broad Jump", "max_effort", (2012, 2),
  [{"exercise": "broad-jump", "reps": 3, "notes": "3 attempts; scored by the furthest single jump"}],
  format_meta={"scoring": "reps"}, tags=["games", "2012", "bodyweight", "max-effort"])

w("games-12-chipper", "Chipper (2012 Games)", "for_time", (2012, 3),
  [{"exercise": "overhead-squat", "reps": 10, "load": BB("155lb", "105lb")},
   {"exercise": "box-jump-over", "reps": 10, "notes": "24 in (men) / 20 in (women) box"},
   {"exercise": "thruster", "reps": 10, "load": BB("135lb", "95lb"), "notes": "fat bar"},
   {"exercise": "power-clean", "reps": 10, "load": BB("205lb", "125lb")},
   {"exercise": "toes-to-bar", "reps": 10},
   {"exercise": "burpee-muscle-up", "reps": 10},
   {"exercise": "toes-to-bar", "reps": 10},
   {"exercise": "power-clean", "reps": 10, "load": BB("205lb", "125lb")},
   {"exercise": "thruster", "reps": 10, "load": BB("135lb", "95lb"), "notes": "fat bar"},
   {"exercise": "box-jump-over", "reps": 10, "notes": "24 in (men) / 20 in (women) box"},
   {"exercise": "overhead-squat", "reps": 10, "load": BB("155lb", "105lb")}],
  format_meta=CAP(15), tags=["games", "2012", "barbell", "gymnastics"])

w("games-12-clean-ladder", "Clean Ladder (2012 Games)", "max_load", (2012, 4),
  [{"exercise": "clean", "reps": 1, "notes": "one rep every 30 seconds through progressively heavier barbells "
    "(245-385 lb men, 140-235 lb women); athletes ranked by heaviest successful clean"}],
  format_meta={"scoring": "load"}, tags=["games", "2012", "barbell", "max-load", "ladder"])

w("games-12-double-banger", "Double Banger", "for_time", (2012, 5),
  [{"exercise": "double-under", "reps": 50},
   {"exercise": "sledgehammer-strike", "notes": "\"low banger\" target"},
   {"exercise": "double-under", "reps": 50},
   {"exercise": "sledgehammer-strike", "notes": "\"down banger\" target"},
   {"exercise": "double-under", "reps": 50},
   {"exercise": "sledgehammer-strike", "notes": "\"mid banger\" target"}],
  format_meta=CAP(9), tags=["games", "2012", "venue-equipment", "jump-rope"])

w("games-12-elizabeth", "Elizabeth (2012 Games)", "for_time", (2012, 6),
  [{"exercise": "clean", "reps": [21, 15, 9], "load": BB("135lb", "95lb")},
   {"exercise": "ring-dip", "reps": [21, 15, 9]}],
  format_meta=CAP(6), tags=["games", "2012", "barbell", "gymnastics", "ladder"],
  notes=src(2012, 6) + "; the classic Girl WOD Elizabeth, reused as a Games event")

w("games-12-fran", "Fran (2012 Games)", "for_time", (2012, 7),
  [{"exercise": "thruster", "reps": [21, 15, 9], "load": BB("95lb", "65lb")},
   {"exercise": "pull-up", "reps": [21, 15, 9]}],
  format_meta=CAP(6), tags=["games", "2012", "barbell", "gymnastics", "ladder"],
  notes=src(2012, 7) + "; the classic Girl WOD Fran, reused as a Games event; contested by the top 12 athletes overall")

w("games-12-isabel", "Isabel (2012 Games)", "for_time", (2012, 8),
  [{"exercise": "snatch", "reps": 30, "load": BB("135lb", "95lb")}],
  format_meta=CAP(6), tags=["games", "2012", "barbell"],
  notes=src(2012, 8) + "; the classic Girl WOD Isabel, reused as a Games event; contested by the top 15 athletes overall, with the top 12 finishers advancing")

w("games-12-medball-handstand-push-up", "MedBall-Handstand Push-up", "interval", (2012, 9),
  [{"exercise": "medicine-ball-clean", "reps": 8, "load": BB("150lb", "80lb")},
   {"exercise": "farmers-carry", "distance_m": 30, "load": BB("150lb", "80lb"), "notes": "100 ft, carrying the medicine ball"},
   {"exercise": "parallette-handstand-push-up", "reps": 7},
   {"exercise": "farmers-carry", "distance_m": 30, "load": BB("150lb", "80lb"), "notes": "100 ft, carrying the medicine ball"}],
  format_meta={"rounds": 3, "time_cap_minutes": 10, "scoring": "time"},
  tags=["games", "2012", "odd-object", "gymnastics", "3-rounds"])

w("games-12-pendleton-1", "Pendleton 1", "for_time", (2012, 11),
  [{"exercise": "swim", "distance_m": 700, "notes": "approx.; with fins"},
   {"exercise": "bike", "distance_m": 8000, "notes": "approx. 8 km, undulating terrain including soft sand"},
   {"exercise": "run", "distance_m": 11000, "notes": "approx. 11 km dirt-road, over 1,400 ft of elevation gain"}],
  tags=["games", "2012", "swim", "outdoor", "hill", "endurance"],
  notes=src(2012, 11) + "; scored at a checkpoint approximately 150 m into the run; same continuous race as Pendleton 2")

w("games-12-pendleton-2", "Pendleton 2", "for_time", (2012, 12),
  [{"exercise": "swim", "distance_m": 700, "notes": "approx.; with fins"},
   {"exercise": "bike", "distance_m": 8000, "notes": "approx. 8 km, undulating terrain including soft sand"},
   {"exercise": "run", "distance_m": 11000, "notes": "approx. 11 km dirt-road, over 1,400 ft of elevation gain"}],
  tags=["games", "2012", "swim", "outdoor", "hill", "endurance"],
  notes=src(2012, 12) + "; scored at the full finish of the same continuous swim/bike/run race as Pendleton 1")

w("games-12-rope-sled", "Rope-Sled", "interval", (2012, 13),
  [{"exercise": "rope-climb", "reps": 1, "notes": "20 ft"},
   {"exercise": "sled-push", "distance_m": 18, "notes": "20 yd increments of a 100 yd total sled drive; "
    "available sources describe the added/total sled load inconsistently between men's and women's "
    "divisions and it could not be confidently resolved, flagged per CONTRIBUTING rather than guessed"}],
  format_meta={"rounds": 5, "time_cap_minutes": 13, "scoring": "time"},
  tags=["games", "2012", "venue-equipment", "gymnastics", "5-rounds"])

w("games-12-track-triplet", "Track Triplet", "interval", (2012, 15),
  [{"exercise": "snatch", "reps": 8, "load": BB("115lb", "75lb"), "notes": "split snatch, alternating legs"},
   {"exercise": "bar-muscle-up", "reps": 7},
   {"exercise": "run", "distance_m": 400}],
  format_meta={"rounds": 3, "time_cap_minutes": 13, "scoring": "time"},
  tags=["games", "2012", "barbell", "gymnastics", "running", "3-rounds"],
  notes=src(2012, 15) + "; performed immediately after Ball Toss")

print(f"Wrote 2012 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
