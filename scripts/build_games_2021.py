import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games individual events -- 2021. Each verified against its official
# games.crossfit.com/workouts/games/2021/<n> page, cross-referenced via
# independent sources for events whose primary page 404'd.
#
# SKIPPED: Event 8 -- a handstand-walking obstacle course with no fixed
# repetition prescription (navigate the course twice, scored by time); left
# out per the Games scoping decision (ROADMAP.md).
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
AMRAP = lambda n, s="rounds_reps": {"time_cap_minutes": n, "scoring": s}
RDS = lambda n: {"rounds": n, "scoring": "time"}

w("games-21-event-1", "2021 Games Event 1", "for_time", (2021, 1),
  [{"exercise": "swim", "distance_m": 1609, "notes": "1 mile, with fins"},
   {"exercise": "kayak", "distance_m": 4828, "notes": "3 miles"}],
  tags=["games", "2021", "swim", "open-water", "endurance"])

w("games-21-event-2", "2021 Games Event 2", "for_time", (2021, 2),
  [{"exercise": "sled-push", "distance_m": 38, "load": BB("220lb", "180lb"), "notes": "126 ft, sled drag"},
   {"exercise": "d-ball-over-shoulder", "reps": 5, "load": BB("510lb", "350lb"), "notes": "\"pig flips\""},
   {"exercise": "muscle-up", "reps": 12},
   {"exercise": "bar-muscle-up", "reps": 12},
   {"exercise": "bar-muscle-up", "reps": 12},
   {"exercise": "muscle-up", "reps": 12},
   {"exercise": "d-ball-over-shoulder", "reps": 5, "load": BB("510lb", "350lb"), "notes": "\"pig flips\""},
   {"exercise": "sled-push", "distance_m": 38, "load": BB("220lb", "180lb"), "notes": "126 ft, sled drag"}],
  format_meta=CAP(12), tags=["games", "2021", "venue-equipment", "gymnastics"])

w("games-21-event-3", "2021 Games Event 3", "for_time", (2021, 3),
  [{"exercise": "sprint", "distance_m": 503, "notes": "550 yd"}],
  format_meta=CAP(4), tags=["games", "2021", "outdoor"])

w("games-21-event-4", "2021 Games Event 4", "for_time", (2021, 4),
  [{"exercise": "wall-climb", "reps": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]},
   {"exercise": "thruster", "reps": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], "load": BB("185lb", "135lb")}],
  format_meta=CAP(20), tags=["games", "2021", "barbell", "gymnastics", "ladder"])

w("games-21-event-5", "2021 Games Event 5", "interval", (2021, 5),
  [{"exercise": "rope-climb", "reps": 4},
   {"exercise": "ski-erg", "reps": 500, "notes": "meters (women use 400)"},
   {"exercise": "husafell-carry", "distance_m": 13, "load": BB("200lb", "150lb"), "notes": "42 ft"}],
  format_meta={"rounds": 4, "time_cap_minutes": 15, "scoring": "time"},
  tags=["games", "2021", "venue-equipment", "gymnastics"])

w("games-21-event-6", "2021 Games Event 6", "interval", (2021, 6),
  [{"exercise": "run", "distance_m": 250},
   {"exercise": "clean", "reps": 1, "load": BB("245lb", "165lb")}],
  format_meta={"rounds": 5, "time_cap_minutes": 7, "scoring": "time"},
  tags=["games", "2021", "barbell", "running", "ladder"],
  notes=src(2021, 6) + "; clean load increases each round: 245-265-285-305-315 lb (men), 165-175-185-195-205 lb (women)")

w("games-21-event-7", "2021 Games Event 7", "interval", (2021, 7),
  [{"exercise": "run", "distance_m": 200},
   {"exercise": "clean", "reps": 1, "load": BB("325lb", "210lb")}],
  format_meta={"rounds": 5, "time_cap_minutes": 8, "scoring": "time"},
  tags=["games", "2021", "barbell", "running", "ladder"],
  notes=src(2021, 7) + "; clean load increases each round: 325-335-340-345-350 lb (men), 210-215-220-225-230 lb (women); paired with Event 6 as a two-part 100-point couplet")

w("games-21-event-9", "2021 Games Event 9", "for_time", (2021, 9),
  [{"exercise": "echo-bike", "reps": 21, "notes": "calories"},
   {"exercise": "snatch", "reps": 21, "load": BB("75lb", "75lb")},
   {"exercise": "echo-bike", "reps": 15, "notes": "calories"},
   {"exercise": "snatch", "reps": 15, "load": BB("105lb", "105lb")},
   {"exercise": "echo-bike", "reps": 9, "notes": "calories"},
   {"exercise": "snatch", "reps": 9, "load": BB("105lb", "105lb")}],
  format_meta=CAP(8), tags=["games", "2021", "barbell", "venue-equipment"])

w("games-21-event-10", "2021 Games Event 10", "for_time", (2021, 10),
  [{"exercise": "toes-to-bar", "reps": 30},
   {"exercise": "run", "distance_m": 2414, "notes": "1.5 miles"},
   {"exercise": "toes-to-bar", "reps": 30},
   {"exercise": "run", "distance_m": 2414, "notes": "1.5 miles"},
   {"exercise": "toes-to-bar", "reps": 30}],
  format_meta=CAP(27), tags=["games", "2021", "running", "gymnastics"])

w("games-21-event-11", "2021 Games Event 11", "amrap", (2021, 11),
  [{"exercise": "pegboard", "reps": 1},
   {"exercise": "dumbbell-overhead-squat", "reps": 7, "load": BB("70lb", "50lb"), "notes": "single-arm"},
   {"exercise": "double-under", "reps": 15, "notes": "heavy rope, loaded to roughly 2x bodyweight"}],
  format_meta=AMRAP(11), tags=["games", "2021", "venue-equipment", "dumbbell", "gymnastics"])

w("games-21-event-12", "2021 Games Event 12", "max_load", (2021, 12),
  [{"exercise": "snatch", "reps": 1, "load": BB("260lb", "160lb"),
    "notes": "starting weight; athlete's own progressive attempts thereafter, 20 seconds per lift (30 seconds in the final single-platform round)"}],
  format_meta={"scoring": "load"},
  tags=["games", "2021", "barbell", "max-load"],
  notes=src(2021, 12) + "; tiebreak (for athletes who fail their opening lift) was 3 squat snatches for time at 225 lb (men) / 145 lb (women)")

w("games-21-event-13", "2021 Games Event 13", "multi_part", (2021, 13),
  segments=[
    {"label": "Round 1", "format": "for_time", "format_meta": CAP(2),
     "movements": [{"exercise": "ghd-sit-up", "reps": 20},
                   {"exercise": "burpee", "reps": 8, "load": BB("100lb", "70lb"), "notes": "over a hay bale, carrying a weighted \"cheese curd\" bag"},
                   {"exercise": "yoke-carry", "distance_m": 51, "load": BB("605lb", "425lb"), "notes": "168 ft"}],
     "rest_after_seconds": 60},
    {"label": "Round 2", "format": "for_time", "format_meta": CAP(2),
     "movements": [{"exercise": "ghd-sit-up", "reps": 20},
                   {"exercise": "burpee", "reps": 8, "load": BB("100lb", "70lb"), "notes": "over a hay bale, carrying a weighted \"cheese curd\" bag"},
                   {"exercise": "yoke-carry", "distance_m": 51, "load": BB("605lb", "425lb"), "notes": "168 ft"}],
     "rest_after_seconds": 60},
    {"label": "Round 3", "format": "for_time", "format_meta": CAP(2),
     "movements": [{"exercise": "ghd-sit-up", "reps": 20},
                   {"exercise": "burpee", "reps": 8, "load": BB("100lb", "70lb"), "notes": "over a hay bale, carrying a weighted \"cheese curd\" bag"},
                   {"exercise": "yoke-carry", "distance_m": 51, "load": BB("605lb", "425lb"), "notes": "168 ft"}],
     "rest_after_seconds": 60},
    {"label": "Round 4", "format": "for_time", "format_meta": CAP(3),
     "movements": [{"exercise": "ghd-sit-up", "reps": 20},
                   {"exercise": "burpee", "reps": 8, "load": BB("100lb", "70lb"), "notes": "over a hay bale, carrying a weighted \"cheese curd\" bag"},
                   {"exercise": "yoke-carry", "distance_m": 51, "load": BB("605lb", "425lb"), "notes": "168 ft"}]},
  ],
  tags=["games", "2021", "venue-equipment", "gymnastics"],
  notes=src(2021, 13) + "; 1 minute to return to the GHD rig before each next round begins")

w("games-21-event-14", "2021 Games Event 14", "for_time", (2021, 14),
  [{"exercise": "deadlift", "reps": [6, 10, 14], "load": BB("405lb", "275lb")},
   {"exercise": "freestanding-handstand-push-up", "reps": [6, 10, 14]}],
  format_meta=CAP(7), tags=["games", "2021", "barbell", "gymnastics", "ladder"],
  notes=src(2021, 14) + "; introduced freestanding handstand push-ups to the Games for the first time")

w("games-21-event-15", "2021 Games Event 15", "for_time", (2021, 15),
  [{"exercise": "row", "distance_m": 600, "notes": "600 m for men, 500 m for women"},
   {"exercise": "chest-to-bar-pull-up", "reps": 90},
   {"exercise": "back-rack-lunge", "distance_m": 11, "load": BB("185lb", "135lb"), "notes": "36 ft, walking"},
   {"exercise": "front-rack-lunge", "distance_m": 11, "load": BB("185lb", "135lb"), "notes": "36 ft, walking"},
   {"exercise": "overhead-walking-lunge", "distance_m": 11, "load": BB("185lb", "135lb"), "notes": "36 ft"}],
  tags=["games", "2021", "rowing", "barbell", "gymnastics"])

print(f"Wrote 2021 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
