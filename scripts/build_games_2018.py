import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games individual events -- 2018. Each verified against its official
# games.crossfit.com/workouts/games/2018/<n> page, cross-referenced via
# independent sources for events whose primary page 404'd.
#
# SKIPPED (per the Games scoping decision in ROADMAP.md):
# - Event 1 "Crit" -- a mass-start bike race (40 athletes simultaneously, no
#   individual movement/rep prescription beyond "ride 10 laps").
# - Event 5 "The Battleground" -- fixed Rescue Randy drags and rope climbs
#   bracket an "obstacle-course run" whose 8 obstacles are not itemized in any
#   available source; left out rather than guessed.
# - Event 6 "Clean and Jerk Speed Ladder" -- an elimination bracket (top 20
#   advance from the quarterfinal, top 5 from the semifinal), not all
#   competitors attempt all rounds.
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

w("games-18-30-muscle-ups", "30 Muscle-Ups", "for_time", (2018, 2),
  [{"exercise": "muscle-up", "reps": 30}],
  format_meta=CAP(5), tags=["games", "2018", "gymnastics"])

w("games-18-crossfit-total", "CrossFit Total", "max_load", (2018, 3),
  [{"exercise": "back-squat", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight; 3 attempts within a 4-minute window"},
   {"exercise": "strict-press", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight; 3 attempts within a 4-minute window"},
   {"exercise": "deadlift", "reps": 1, "notes": "athlete's own 1-rep-max; no fixed Rx weight; 3 attempts within a 4-minute window"}],
  format_meta={"time_cap_minutes": 12, "scoring": "load"},
  tags=["games", "2018", "barbell", "max-load"],
  notes=src(2018, 3) + "; score is the combined total of all three best lifts")

w("games-18-marathon-row", "Marathon Row", "for_time", (2018, 4),
  [{"exercise": "row", "distance_m": 42195, "notes": "marathon distance"}],
  format_meta=CAP(240), tags=["games", "2018", "rowing", "endurance"])

w("games-18-fibonacci", "Fibonacci", "for_time", (2018, 7),
  [{"exercise": "parallette-handstand-push-up", "reps": [5, 8, 13], "notes": "14 in deficit (men) / 8 in deficit (women)"},
   {"exercise": "kettlebell-deadlift", "reps": [5, 8, 13], "load": BB("203lb", "124lb"), "notes": "2 kettlebells"},
   {"exercise": "kettlebell-overhead-lunge", "distance_m": 27, "load": BB("53lb", "35lb"), "notes": "89 ft, 2 kettlebells overhead, finishing sequence"}],
  format_meta=CAP(6), tags=["games", "2018", "kettlebell", "gymnastics"])

w("games-18-madison-triplus", "Madison Triplus", "for_time", (2018, 8),
  [{"exercise": "swim", "distance_m": 500},
   {"exercise": "paddleboard", "distance_m": 1000},
   {"exercise": "run", "distance_m": 2000}],
  format_meta=CAP(40), tags=["games", "2018", "swim", "open-water", "running", "endurance"])

w("games-18-chaos", "Chaos", "for_time", (2018, 9),
  [{"exercise": "ski-erg", "reps": 35, "notes": "calories (women use 30)"},
   {"exercise": "burpee", "reps": 30, "notes": "to touch an elevated target bar (women use 25)"},
   {"exercise": "dumbbell-overhead-squat", "reps": 45, "load": BB("50lb", "35lb"), "notes": "single-arm (women perform 40)"},
   {"exercise": "pistol", "reps": 40, "notes": "alternating legs (women perform 45)"},
   {"exercise": "box-jump-over", "reps": 25, "notes": "42 in (men) / 36 in (women) box"},
   {"exercise": "sled-pull", "distance_m": 34, "load": BB("400lb", "300lb"), "notes": "110 ft, \"tumbler\" pull"}],
  format_meta=CAP(12), tags=["games", "2018", "venue-equipment", "dumbbell", "gymnastics"],
  notes=src(2018, 9) + "; a \"mystery\" event -- athletes were not told the movements or reps in advance, discovering each station on arrival")

w("games-18-bicouplet-1", "Bicouplet 1", "for_time", (2018, 10),
  [{"exercise": "snatch", "reps": [21, 15, 9], "load": BB("85lb", "55lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": [21, 15, 9]}],
  format_meta=CAP(6), tags=["games", "2018", "barbell", "gymnastics"],
  notes=src(2018, 10) + "; separately scored from Bicouplet 2, which follows after a 1-minute transition")

w("games-18-bicouplet-2", "Bicouplet 2", "for_time", (2018, 11),
  [{"exercise": "snatch", "reps": [12, 9, 6], "load": BB("135lb", "85lb")},
   {"exercise": "bar-muscle-up", "reps": [12, 9, 6]}],
  format_meta=CAP(6), tags=["games", "2018", "barbell", "gymnastics"],
  notes=src(2018, 11) + "; separately scored from Bicouplet 1, beginning after a 1-minute transition")

w("games-18-two-stroke-pull", "Two-Stroke Pull", "interval", (2018, 12),
  [{"exercise": "run", "distance_m": 300},
   {"exercise": "assault-bike", "reps": 20, "notes": "calories (women use 15)"},
   {"exercise": "sled-pull", "distance_m": 13, "load": BB("183lb", "153lb"), "notes": "44 ft"}],
  format_meta={"rounds": 5, "time_cap_minutes": 18, "scoring": "time"},
  tags=["games", "2018", "venue-equipment", "running"])

w("games-18-handstand-walk", "Handstand Walk", "for_time", (2018, 13),
  [{"exercise": "double-under", "reps": 50, "notes": "heavy rope"},
   {"exercise": "handstand-walk", "notes": "pylon slalom"},
   {"exercise": "handstand-walk", "notes": "up and down a ramp"},
   {"exercise": "handstand-walk", "notes": "up and down stairs"},
   {"exercise": "handstand-walk", "notes": "across parallel bars to the finish"}],
  format_meta=CAP(4), tags=["games", "2018", "venue-equipment", "gymnastics"],
  notes=src(2018, 13) + "; each obstacle must be completed without falling")

w("games-18-aeneas", "Aeneas", "for_time", (2018, 14),
  [{"exercise": "pegboard", "reps": 5, "notes": "5 (men) / 4 (women) ascents"},
   {"exercise": "thruster", "reps": 40, "load": BB("85lb", "55lb")},
   {"exercise": "yoke-carry", "distance_m": 10, "load": BB("425lb", "345lb"), "notes": "33 ft"},
   {"exercise": "yoke-carry", "distance_m": 10, "load": BB("565lb", "405lb"), "notes": "33 ft"},
   {"exercise": "yoke-carry", "distance_m": 10, "load": BB("665lb", "445lb"), "notes": "33 ft"}],
  format_meta=CAP(8), tags=["games", "2018", "venue-equipment", "barbell", "gymnastics"])

print(f"Wrote 2018 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
