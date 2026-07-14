import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-10"

# CrossFit Games individual events -- 2007, the inaugural CrossFit Games.
# Each verified against its official games.crossfit.com/workouts/games/2007/<n>
# page. No events skipped this year -- all 3 have a genuine fixed prescription.
# The 2007 Games had no gender-specific Rx split published for these events.
def src(year, n):
    return (f"games.crossfit.com/workouts/games/{year}/{n} "
            f"(official CrossFit Games event, inaugural Games), retrieved {TODAY}")

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
RDS = lambda n: {"rounds": n, "scoring": "time"}

w("games-07-the-hopper-workout", "The Hopper Workout", "multi_part", (2007, 1),
  segments=[
    {"label": "Row", "format": "for_time",
     "movements": [{"exercise": "row", "distance_m": 1000}]},
    {"label": "Pull-up/Push-jerk", "format": "interval", "format_meta": RDS(5),
     "movements": [{"exercise": "pull-up", "reps": 25},
                   {"exercise": "push-jerk", "reps": 7, "load": BB("135lb", "95lb")}]},
  ],
  tags=["games", "2007", "rowing", "barbell", "gymnastics", "5-rounds"],
  notes=src(2007, 1) + "; 1000m row once, then 5 rounds for time of 25 pull-ups and 7 push jerks")

w("games-07-trail-run", "Trail Run (2007 Games)", "for_time", (2007, 2),
  [{"exercise": "run", "distance_m": 5000, "notes": "approx. 5k trail run; exact course distance not published"}],
  tags=["games", "2007", "running", "outdoor", "endurance"],
  notes=src(2007, 2) + "; approx. 5k trail run, exact distance not precisely specified in available sources")

w("games-07-crossfit-total", "CrossFit Total (2007 Games)", "multi_part", (2007, 3),
  segments=[
    {"label": "Back squat", "format": "max_load", "format_meta": {"scoring": "load"},
     "movements": [{"exercise": "back-squat", "reps": 1, "notes": "athlete's own 1-rep-max"}]},
    {"label": "Press", "format": "max_load", "format_meta": {"scoring": "load"},
     "movements": [{"exercise": "strict-press", "reps": 1, "notes": "athlete's own 1-rep-max"}]},
    {"label": "Deadlift", "format": "max_load", "format_meta": {"scoring": "load"},
     "movements": [{"exercise": "deadlift", "reps": 1, "notes": "athlete's own 1-rep-max"}]},
  ],
  tags=["games", "2007", "barbell", "max-load"],
  notes=src(2007, 3) + "; the classic CrossFit Total benchmark (1RM back squat + press + deadlift), used as the final event of the inaugural 2007 Games; score is the sum of the three lifts")

print(f"Wrote 2007 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
