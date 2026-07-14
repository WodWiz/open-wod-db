import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-10"

# CrossFit Games individual events -- 2008. Each verified against its official
# games.crossfit.com/workouts/games/2008/<n> page, individual division
# explicitly confirmed for every event. No events skipped -- all 4 have a
# genuine fixed prescription.
def src(year, n):
    return (f"games.crossfit.com/workouts/games/{year}/{n} "
            f"(official CrossFit Games event, individual division confirmed), retrieved {TODAY}")

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
RDS = lambda n: {"rounds": n, "scoring": "time"}

w("games-08-sundays-workout", "Sunday's Workout", "for_time", (2008, 1),
  [{"exercise": "clean-and-jerk", "reps": 30, "load": BB("155lb", "100lb")}],
  tags=["games", "2008", "barbell"],
  notes=src(2008, 1) + "; the classic Girl WOD Grace, reused as a Games event -- this was the final event of the 2008 Games")

w("games-08-the-hill-run", "The Hill Run", "for_time", (2008, 2),
  [{"exercise": "run", "distance_m": 750, "notes": "steep, off-trail, rough terrain"}],
  format_meta=CAP(20), tags=["games", "2008", "running", "outdoor", "hill"])

w("games-08-workout-a", "Workout A (2008 Games)", "for_time", (2008, 3),
  [{"exercise": "thruster", "reps": [21, 15, 9], "load": BB("95lb", "65lb")},
   {"exercise": "pull-up", "reps": [21, 15, 9]}],
  format_meta=CAP(12), tags=["games", "2008", "barbell", "gymnastics", "ladder"],
  notes=src(2008, 3) + "; the classic Girl WOD Fran, reused as a Games event")

w("games-08-workout-b", "Workout B (2008 Games)", "interval", (2008, 4),
  [{"exercise": "deadlift", "reps": 5, "load": BB("275lb", "185lb")},
   {"exercise": "burpee", "reps": 10}],
  format_meta={**RDS(5), "time_cap_minutes": 12}, tags=["games", "2008", "barbell", "5-rounds"])

print(f"Wrote 2008 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
