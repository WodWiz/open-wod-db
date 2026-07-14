import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games individual events -- 2013. Each verified against its official
# games.crossfit.com/workouts/games/2013/<n> page, cross-referenced via
# independent sources for events whose primary page 404'd.
#
# SKIPPED: Event "ZigZag Sprint" -- a bracketed head-to-head obstacle race,
# not a fixed single prescription; left out per the Games scoping decision
# (ROADMAP.md).
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

w("games-13-2007", "2007 (2013 Games)", "for_time", (2013, 1),
  [{"exercise": "row", "distance_m": 1000},
   {"exercise": "pull-up", "reps": 25}, {"exercise": "push-jerk", "reps": 7, "load": BB("135lb", "85lb")},
   {"exercise": "pull-up", "reps": 25}, {"exercise": "push-jerk", "reps": 7, "load": BB("135lb", "85lb")},
   {"exercise": "pull-up", "reps": 25}, {"exercise": "push-jerk", "reps": 7, "load": BB("135lb", "85lb")},
   {"exercise": "pull-up", "reps": 25}, {"exercise": "push-jerk", "reps": 7, "load": BB("135lb", "85lb")},
   {"exercise": "pull-up", "reps": 25}, {"exercise": "push-jerk", "reps": 7, "load": BB("135lb", "85lb")}],
  format_meta=CAP(15), tags=["games", "2013", "rowing", "barbell", "gymnastics"],
  notes=src(2013, 1) + "; the original event this workout is named for; later revisited as \"2007 Reload\" at the 2020 Games")

w("games-13-burden-run", "Burden Run", "for_time", (2013, 2),
  [{"exercise": "run", "distance_m": 3380, "notes": "2.1 miles"},
   {"exercise": "d-ball-over-shoulder", "distance_m": 91, "notes": "100 yd, \"pig flip\""},
   {"exercise": "log-carry", "distance_m": 549, "notes": "600 yd"},
   {"exercise": "sled-pull", "distance_m": 60, "notes": "66 yd, \"Iditarod\" drag apparatus"}],
  format_meta=CAP(40), tags=["games", "2013", "venue-equipment", "running", "outdoor"])

w("games-13-clean-jerk-ladder", "Clean & Jerk Ladder", "max_load", (2013, 3),
  [{"exercise": "clean-and-jerk", "reps": 1,
    "notes": "athlete chooses one of four starting weights (225, 255, 285, or 315 lb men / 145, 165, 185, or 205 lb women), "
              "then attempts progressively heavier singles every 90 seconds; failing the OPENING attempt eliminates the "
              "athlete; partial credit given for a successful clean with a failed jerk after at least one made lift"}],
  format_meta={"scoring": "load"}, tags=["games", "2013", "barbell", "max-load"])

w("games-13-legless", "Legless", "for_time", (2013, 4),
  [{"exercise": "thruster", "reps": 27, "load": BB("95lb", "65lb")},
   {"exercise": "legless-rope-climb", "reps": 4},
   {"exercise": "thruster", "reps": 21, "load": BB("95lb", "65lb")},
   {"exercise": "legless-rope-climb", "reps": 3},
   {"exercise": "thruster", "reps": 15, "load": BB("95lb", "65lb")},
   {"exercise": "legless-rope-climb", "reps": 2},
   {"exercise": "thruster", "reps": 9, "load": BB("95lb", "65lb")},
   {"exercise": "legless-rope-climb", "reps": 1}],
  format_meta=CAP(10), tags=["games", "2013", "barbell", "gymnastics", "ladder"])

w("games-13-naughty-nancy", "Naughty Nancy", "interval", (2013, 5),
  [{"exercise": "run", "distance_m": 600, "notes": "up and over a berm"},
   {"exercise": "overhead-squat", "reps": 25, "load": BB("140lb", "95lb")}],
  format_meta={"rounds": 4, "time_cap_minutes": 20, "scoring": "time"},
  tags=["games", "2013", "barbell", "running", "outdoor", "4-rounds"])

w("games-13-row-1", "Row 1", "for_time", (2013, 6),
  [{"exercise": "row", "distance_m": 21097, "notes": "half-marathon distance; this event scores the 2,000 m checkpoint split"}],
  format_meta={"time_cap_minutes": 120, "scoring": "time"},
  tags=["games", "2013", "rowing", "endurance"],
  notes=src(2013, 6) + "; time cap 2 hours (men) / 2 hours 10 minutes (women); scored at the 2,000 m mark of a continuous half-marathon row")

w("games-13-row-2", "Row 2", "for_time", (2013, 7),
  [{"exercise": "row", "distance_m": 21097, "notes": "half-marathon distance; this event scores the full finish"}],
  format_meta={"time_cap_minutes": 120, "scoring": "time"},
  tags=["games", "2013", "rowing", "endurance"],
  notes=src(2013, 7) + "; time cap 2 hours (men) / 2 hours 10 minutes (women); same continuous row as Row 1, scored at the full 21,097 m finish")

w("games-13-sprint-chipper", "Sprint Chipper", "for_time", (2013, 8),
  [{"exercise": "medicine-ball-sit-up", "reps": 21, "notes": "GHD variant"},
   {"exercise": "snatch", "reps": 15, "load": BB("165lb", "100lb")},
   {"exercise": "burpee", "reps": 9, "notes": "to touch an elevated wall target"}],
  tags=["games", "2013", "barbell"],
  notes=src(2013, 8) + "; top 30 men and top 30 women advance to the final")

w("games-13-the-cinco-1", "The Cinco 1", "interval", (2013, 9),
  [{"exercise": "deadlift", "reps": 5, "load": BB("405lb", "265lb")},
   {"exercise": "pistol", "reps": 5, "load": BB("53lb", "35lb"), "notes": "left leg, holding a kettlebell"},
   {"exercise": "pistol", "reps": 5, "load": BB("53lb", "35lb"), "notes": "right leg, holding a kettlebell"}],
  format_meta={"rounds": 3, "time_cap_minutes": 7, "scoring": "time"},
  tags=["games", "2013", "barbell", "kettlebell", "gymnastics", "3-rounds"],
  notes=src(2013, 9) + "; finishes with an 80 ft handstand walk; The Cinco 2 begins exactly 1 minute after this event's cap")

w("games-13-the-cinco-2", "The Cinco 2", "interval", (2013, 10),
  [{"exercise": "muscle-up", "reps": 5},
   {"exercise": "deficit-handstand-push-up", "reps": 5}],
  format_meta={"rounds": 3, "time_cap_minutes": 7, "scoring": "time"},
  tags=["games", "2013", "gymnastics", "3-rounds"],
  notes=src(2013, 10) + "; finishes with a 90 ft overhead walking lunge holding a 160/100 lb axle bar; begins 1 minute after The Cinco 1's cap")

w("games-13-the-pool", "The Pool", "interval", (2013, 11),
  [{"exercise": "swim", "distance_m": 23, "notes": "25 yd"},
   {"exercise": "bar-muscle-up", "reps": 3},
   {"exercise": "swim", "distance_m": 23, "notes": "25 yd"}],
  format_meta={"rounds": 10, "time_cap_minutes": 25, "scoring": "time"},
  tags=["games", "2013", "swim", "gymnastics", "10-rounds"])

print(f"Wrote 2013 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
