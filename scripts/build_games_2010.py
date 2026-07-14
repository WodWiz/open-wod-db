import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-10"

# CrossFit Games individual events -- 2010. Each verified against its official
# games.crossfit.com/workouts/games/2010/<n> page, cross-referenced via
# independent sources (the direct page conflated team and individual content
# for at least Events 1 and 4; the versions here reflect the confirmed
# INDIVIDUAL-division prescriptions only). No events skipped this year --
# there were 9 scored individual events, all with a genuine fixed prescription.
def src(year, n):
    return (f"games.crossfit.com/workouts/games/{year}/{n} "
            f"(official CrossFit Games event, individual division), retrieved {TODAY}")

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

w("games-10-amanda", "Amanda (2010 Games)", "for_time", (2010, 1),
  [{"exercise": "ring-muscle-up", "reps": [9, 7, 5]},
   {"exercise": "squat-snatch", "reps": [9, 7, 5], "load": BB("135lb", "95lb")}],
  tags=["games", "2010", "barbell", "gymnastics", "ladder"],
  notes=src(2010, 1) + "; the classic Girl WOD Amanda, reused as a Games event. "
        "Note: this repo's original research pass initially mis-attributed a "
        "team-division thruster/pull-up/buddy-carry workout to this event slot; "
        "corrected after cross-referencing a second source")

w("games-10-max-rep-deadlift", "Max Rep Deadlift", "amrap", (2010, 2),
  [{"exercise": "deadlift", "reps": "max", "load": BB("264lb", "264lb"), "notes": "max reps in 1 minute"}],
  format_meta={"time_cap_minutes": 1, "scoring": "reps"},
  tags=["games", "2010", "barbell", "max-effort"],
  notes=src(2010, 2) + "; available sources report a single 264 lb load without a gender split -- flagged per CONTRIBUTING rather than assumed")

w("games-10-shoulder-to-overhead", "Shoulder-to-Overhead (2010 Games)", "max_load", (2010, 2),
  [{"exercise": "shoulder-to-overhead", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight"}],
  format_meta={"time_cap_minutes": 12, "scoring": "load"},
  tags=["games", "2010", "barbell", "max-load"],
  notes=src(2010, 2) + "; must be completed within 12 minutes of the start of Max Rep Deadlift, immediately following it on the same clock")

w("games-10-event-3", "2010 Games Event 3", "interval", (2010, 3),
  [{"exercise": "run", "distance_m": 300},
   {"exercise": "box-jump-over", "reps": 15, "notes": "24 in box"},
   {"exercise": "dumbbell-squat-clean", "reps": 15, "load": BB("45lb", "25lb")},
   {"exercise": "double-under", "reps": 30},
   {"exercise": "hand-release-push-up", "reps": 15},
   {"exercise": "ghd-sit-up", "reps": 15},
   {"exercise": "walking-lunge", "distance_m": 27, "notes": "30 yd"}],
  format_meta=RDS(2), tags=["games", "2010", "dumbbell", "gymnastics", "running", "2-rounds"])

w("games-10-sandbag-move", "Sandbag Move", "for_time", (2010, 4),
  [{"exercise": "sandbag-carry", "load": BB("600lb total", "370lb total"),
    "notes": "down the stadium stairs, across the floor, up a wall, and up the far stairs"}],
  tags=["games", "2010", "venue-equipment"])

w("games-10-cleans-handstand-pushups", "Cleans-Handstand Pushups", "interval", (2010, 5),
  [{"exercise": "clean", "reps": 3, "load": BB("205lb", "135lb")},
   {"exercise": "ring-handstand-push-up", "reps": 4, "notes": "on rings (men); on the floor (women)"}],
  format_meta=RDS(7), tags=["games", "2010", "barbell", "gymnastics", "7-rounds"])

w("games-10-the-final-1", "The Final 1 (2010 Games)", "interval", (2010, 6),
  [{"exercise": "hand-release-push-up", "reps": 30},
   {"exercise": "wall-climb-over", "reps": 1},
   {"exercise": "overhead-squat", "reps": 21, "load": BB("95lb", "65lb")}],
  format_meta=RDS(3), tags=["games", "2010", "barbell", "gymnastics", "3-rounds"])

w("games-10-the-final-2", "The Final 2 (2010 Games)", "interval", (2010, 7),
  [{"exercise": "toes-to-bar", "reps": 30},
   {"exercise": "ground-to-overhead", "reps": 21, "load": BB("95lb", "65lb")}],
  format_meta=RDS(3), tags=["games", "2010", "barbell", "gymnastics", "3-rounds"])

w("games-10-the-final-3", "The Final 3 (2010 Games)", "interval", (2010, 8),
  [{"exercise": "burpee", "reps": 5, "notes": "\"burpee wall jump\" -- jump to touch/clear an elevated wall target"},
   {"exercise": "rope-climb", "reps": 3, "notes": "20 ft (men); women perform 2 reps"}],
  format_meta=RDS(3), tags=["games", "2010", "gymnastics", "3-rounds"])

print(f"Wrote 2010 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
