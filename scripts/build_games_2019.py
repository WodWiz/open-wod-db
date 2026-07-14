import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games individual events -- 2019. Each verified against its official
# games.crossfit.com/workouts/games/2019/<n> page, cross-referenced via
# independent sources for events whose primary page 404'd.
#
# SKIPPED: Event 6 "Sprint" -- a 3-round bracketed heat race (5 athletes per
# heat, progressive elimination), not a fixed single prescription; left out
# per the Games scoping decision (ROADMAP.md).
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

w("games-19-first-cut", "First Cut", "interval", (2019, 1),
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "legless-rope-climb", "reps": 3},
   {"exercise": "squat-snatch", "reps": 7, "load": BB("185lb", "130lb")}],
  format_meta={"rounds": 4, "time_cap_minutes": 20, "scoring": "time"},
  tags=["games", "2019", "barbell", "gymnastics"],
  notes=src(2019, 1) + "; top 75 athletes score points, the rest are ranked with 0")

w("games-19-second-cut", "Second Cut", "for_time", (2019, 2),
  [{"exercise": "row", "distance_m": 800},
   {"exercise": "kettlebell-press", "reps": 66, "load": BB("35lb", "26lb"), "notes": "shoulder-to-overhead; 2 kettlebells (16 kg men / 12 kg women)"},
   {"exercise": "handstand-walk", "distance_m": 40, "notes": "132 ft"}],
  format_meta=CAP(10), tags=["games", "2019", "rowing", "kettlebell", "gymnastics"],
  notes=src(2019, 2) + "; top 50 athletes advance")

w("games-19-ruck", "Ruck", "for_time", (2019, 3),
  [{"exercise": "run", "distance_m": 1500, "load": BB("20lb", "20lb"), "notes": "weighted ruck run"},
   {"exercise": "run", "distance_m": 1500, "load": BB("30lb", "30lb"), "notes": "weighted ruck run"},
   {"exercise": "run", "distance_m": 1500, "load": BB("40lb", "40lb"), "notes": "weighted ruck run"},
   {"exercise": "run", "distance_m": 1500, "load": BB("50lb", "50lb"), "notes": "weighted ruck run"}],
  format_meta=CAP(40), tags=["games", "2019", "running", "weighted", "endurance"],
  notes=src(2019, 3) + "; 4 laps of the same 1,500 m course, adding weight each lap (same for both divisions); top 40 athletes advance")

w("games-19-sprint-couplet", "Sprint Couplet", "for_time", (2019, 4),
  [{"exercise": "sled-push", "distance_m": 52, "notes": "172 ft"},
   {"exercise": "bar-muscle-up", "reps": 18, "notes": "18 reps (men) / 15 reps (women)"},
   {"exercise": "sled-push", "distance_m": 52, "notes": "172 ft"}],
  format_meta=CAP(6), tags=["games", "2019", "venue-equipment", "gymnastics"],
  notes=src(2019, 4) + "; top 30 athletes advance")

w("games-19-mary", "Mary (2019 Games)", "amrap", (2019, 5),
  [{"exercise": "handstand-push-up", "reps": 5},
   {"exercise": "pistol", "reps": 10, "notes": "alternating legs"},
   {"exercise": "pull-up", "reps": 15}],
  format_meta=AMRAP(20), tags=["games", "2019", "gymnastics", "bodyweight"],
  notes=src(2019, 5) + "; the classic Girl WOD Mary, reused as a Games event")

w("games-19-split-triplet", "Split Triplet", "interval", (2019, 7),
  [{"exercise": "pegboard", "reps": 1},
   {"exercise": "double-under", "reps": 100},
   {"exercise": "dumbbell-hang-split-snatch", "reps": 10, "load": BB("80lb", "55lb"), "notes": "alternating arms each rep"},
   {"exercise": "dumbbell-hang-clean-and-jerk", "reps": 10, "load": BB("80lb", "55lb"), "notes": "split jerk variant; opposite arm from lead leg"}],
  format_meta={"rounds": 5, "time_cap_minutes": 20, "scoring": "time"},
  tags=["games", "2019", "gymnastics", "dumbbell"])

w("games-19-clean", "Clean (2019 Games)", "max_load", (2019, 8),
  [{"exercise": "clean", "reps": 1, "load": BB("315lb", "215lb"),
    "notes": "starting weight; athletes lift in reverse order of current placement, weight increasing each round; possible weights up to 385 lb (men) / 260 lb (women)"}],
  format_meta={"scoring": "load"},
  tags=["games", "2019", "barbell", "max-load"],
  notes=src(2019, 8) + "; tiebreak was 5 reps at 295 lb (men) / 195 lb (women) for athletes who failed their attempt")

w("games-19-swim-paddle", "Swim Paddle", "for_time", (2019, 9),
  [{"exercise": "swim", "distance_m": 1000},
   {"exercise": "paddleboard", "distance_m": 1000}],
  format_meta=CAP(50), tags=["games", "2019", "swim", "open-water", "endurance"])

w("games-19-ringer-1", "Ringer 1", "for_time", (2019, 10),
  [{"exercise": "bike", "reps": 30, "notes": "calories; air bike"},
   {"exercise": "toes-to-ring", "reps": 30},
   {"exercise": "bike", "reps": 20, "notes": "calories; air bike"},
   {"exercise": "toes-to-ring", "reps": 20},
   {"exercise": "bike", "reps": 10, "notes": "calories; air bike"},
   {"exercise": "toes-to-ring", "reps": 10}],
  format_meta={"time_cap_minutes": 6, "scoring": "time"},
  tags=["games", "2019", "gymnastics"],
  notes=src(2019, 10) + "; time cap 6 minutes (men) / 7 minutes (women); scored separately from Ringer 2, which begins 1 minute after this event's cap")

w("games-19-ringer-2", "Ringer 2", "for_time", (2019, 11),
  [{"exercise": "burpee", "reps": 15, "notes": "with a jump to touch the rings"},
   {"exercise": "overhead-squat", "reps": 15, "load": BB("135lb", "95lb")},
   {"exercise": "burpee", "reps": 10, "notes": "with a jump to touch the rings"},
   {"exercise": "overhead-squat", "reps": 10, "load": BB("135lb", "95lb")},
   {"exercise": "burpee", "reps": 5, "notes": "with a jump to touch the rings"},
   {"exercise": "overhead-squat", "reps": 5, "load": BB("135lb", "95lb")}],
  format_meta=CAP(5), tags=["games", "2019", "barbell", "gymnastics"],
  notes=src(2019, 11) + "; scored separately from Ringer 1, starting 7 minutes after Ringer 1 begins")

w("games-19-the-standard", "The Standard", "for_time", (2019, 12),
  [{"exercise": "clean-and-jerk", "reps": 30, "load": BB("135lb", "95lb")},
   {"exercise": "muscle-up", "reps": 30},
   {"exercise": "snatch", "reps": 30, "load": BB("135lb", "95lb")}],
  format_meta=CAP(12), tags=["games", "2019", "barbell", "gymnastics"])

print(f"Wrote 2019 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
