import json, os

from wod_descriptions import DESCRIPTIONS

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "games")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Games individual events (category "games") -- unlike Girls/Heroes/Open/
# Quarterfinals, these are competition-specific tests, not all of which are
# repeatable in a standard gym: some need Games-venue equipment (yoke, echo bike,
# sled) or open water/hills. Every entry here IS a genuine, published, fixed
# movement/rep/load prescription (verified against its official
# games.crossfit.com/workouts/games/<year>/<n> page); pure heat-based obstacle-
# course races and bracket sprints with no fixed prescription are intentionally
# left out of this dataset rather than fabricated (staged separately if ever
# revisited). Tags flag what limits repeatability: "venue-equipment" (yoke, sled,
# echo bike, ski erg -- less common but ownable), "swim"/"open-water",
# "hill"/"outdoor", "bracket-race" would go here but none this year.
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

w("games-24-lake-day", "Lake Day", "for_time", (2024, 1),
  [{"exercise": "run", "distance_m": 5633, "notes": "3.5 miles"},
   {"exercise": "swim", "distance_m": 800}],
  tags=["games", "2024", "swim", "open-water", "endurance"])

w("games-24-midline-climb", "Midline Climb", "for_time", (2024, 2),
  [{"exercise": "deadlift", "reps": 50, "load": BB("225lb", "155lb")},
   {"exercise": "rope-climb", "reps": 3},
   {"exercise": "ski-erg", "reps": 50, "notes": "calories (women use 30)"},
   {"exercise": "rope-climb", "reps": 3},
   {"exercise": "ghd-sit-up", "reps": 50},
   {"exercise": "rope-climb", "reps": 3},
   {"exercise": "ghd-sit-up", "reps": 50},
   {"exercise": "rope-climb", "reps": 3},
   {"exercise": "ski-erg", "reps": 50, "notes": "calories (women use 30)"},
   {"exercise": "rope-climb", "reps": 3},
   {"exercise": "deadlift", "reps": 50, "load": BB("225lb", "155lb")}],
  format_meta=CAP(20), tags=["games", "2024", "venue-equipment", "gymnastics"])

w("games-24-firestorm", "Firestorm", "interval", (2024, 3),
  [{"exercise": "echo-bike", "reps": 15, "notes": "calories (women use 11)"},
   {"exercise": "burpee", "reps": 11, "notes": "over a barricade/obstacle"}],
  format_meta={"rounds": 3, "time_cap_minutes": 4, "scoring": "time"},
  tags=["games", "2024", "venue-equipment"],
  notes=src(2024, 3) + "; men's time cap 4 minutes, women's 5 minutes")

w("games-24-track-and-field", "Track and Field", "multi_part", (2024, 4),
  segments=[
    {"label": "Phase 1", "format": "for_time",
     "movements": [{"exercise": "run", "distance_m": 1600}]},
    {"label": "Phase 2 (begins at the 12:00 mark regardless of Phase 1 completion)",
     "format": "for_time", "format_meta": CAP(3),
     "movements": [{"exercise": "sprint", "distance_m": 46, "notes": "50 yd"},
                   {"exercise": "sandbag-carry", "distance_m": 46, "load": BB("100lb", "70lb"), "notes": "50 yd"},
                   {"exercise": "sprint", "distance_m": 69, "notes": "75 yd"},
                   {"exercise": "sandbag-carry", "distance_m": 69, "load": BB("100lb", "70lb"), "notes": "75 yd"},
                   {"exercise": "sprint", "distance_m": 91, "notes": "100 yd"}]},
  ],
  tags=["games", "2024", "outdoor", "hill"],
  notes=src(2024, 4) + "; Phase 2 begins at a fixed clock time (12:00) regardless of when Phase 1 finishes")

w("games-24-chad", "Chad", "for_time", (2024, 5),
  [{"exercise": "box-step-up", "reps": 1000, "load": BB("45lb", "35lb"), "notes": "weight vest; completed as 250 trips"}],
  format_meta=CAP(67),
  tags=["games", "2024", "weighted", "high-volume"],
  notes=src(2024, 5) + "; same core movement as the Hero WOD Chad1000x, but this is the "
        "official 2024 Games version with a 67-minute cap and vest load")

w("games-24-clean-ladder", "Clean Ladder", "multi_part", (2024, 6),
  segments=[
    {"label": "Round 1", "format": "max_load", "format_meta": CAP(2),
     "movements": [{"exercise": "clean", "reps": 1, "load": BB("255lb", "165lb")},
                   {"exercise": "clean", "reps": 1, "load": BB("265lb", "175lb")},
                   {"exercise": "clean", "reps": 1, "load": BB("275lb", "185lb")},
                   {"exercise": "clean", "reps": 1, "load": BB("285lb", "195lb")},
                   {"exercise": "clean", "reps": 1, "load": BB("295lb", "205lb")}]},
    {"label": "Round 2", "format": "max_load", "format_meta": CAP(2),
     "movements": [{"exercise": "clean", "reps": 1, "load": BB("295lb", "205lb")},
                   {"exercise": "clean", "reps": 1, "load": BB("305lb", "215lb")},
                   {"exercise": "clean", "reps": 1, "load": BB("315lb", "225lb")},
                   {"exercise": "clean", "reps": 1, "load": BB("325lb", "230lb")}]},
    {"label": "Round 3", "format": "max_load", "format_meta": CAP(2),
     "movements": [{"exercise": "clean", "reps": 1, "load": BB("325lb", "230lb")},
                   {"exercise": "clean", "reps": 1, "load": BB("345lb", "240lb")},
                   {"exercise": "clean", "reps": 1, "load": BB("365lb", "250lb")}]},
  ],
  tags=["games", "2024", "barbell", "max-load", "ladder"],
  notes=src(2024, 6) + "; make-or-miss ladder across 3 rounds (each with its own 2-minute "
        "window), each attempt at a heavier weight; score is the heaviest successful clean")

w("games-24-push-pull-2", "Push Pull 2.0", "for_time", (2024, 7),
  [{"exercise": "handstand-push-up", "reps": 45},
   {"exercise": "sled-pull", "distance_m": 24, "load": BB("180lb", "110lb"), "notes": "80 ft, from standing"},
   {"exercise": "strict-handstand-push-up", "reps": 30},
   {"exercise": "sled-pull", "distance_m": 24, "load": BB("180lb", "110lb"), "notes": "80 ft, seated from a platform"},
   {"exercise": "freestanding-handstand-push-up", "reps": 15}],
  format_meta=CAP(10), tags=["games", "2024", "venue-equipment", "gymnastics"])

w("games-24-dickies-triplet", "Dickies Triplet", "interval", (2024, 8),
  [{"exercise": "run", "distance_m": 175},
   {"exercise": "toes-to-bar", "reps": 12},
   {"exercise": "alternating-dumbbell-snatch", "reps": 8, "load": BB("100lb", "70lb")}],
  format_meta={"rounds": 5, "time_cap_minutes": 11, "scoring": "time"},
  tags=["games", "2024", "dumbbell", "running"])

w("games-24-final-2421", "Final 2421", "for_time", (2024, 9),
  [{"exercise": "thruster", "reps": 24, "load": BB("95lb", "65lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": 24},
   {"exercise": "yoke-carry", "distance_m": 24, "load": BB("425lb", "245lb"), "notes": "80 ft"},
   {"exercise": "chest-to-bar-pull-up", "reps": 21},
   {"exercise": "thruster", "reps": 21, "load": BB("95lb", "65lb")}],
  format_meta=CAP(5), tags=["games", "2024", "venue-equipment", "barbell", "gymnastics"])

w("games-24-final-1815", "Final 1815", "for_time", (2024, 10),
  [{"exercise": "thruster", "reps": 18, "load": BB("135lb", "95lb")},
   {"exercise": "bar-muscle-up", "reps": 18},
   {"exercise": "yoke-carry", "distance_m": 24, "load": BB("525lb", "345lb"), "notes": "80 ft"},
   {"exercise": "bar-muscle-up", "reps": 15},
   {"exercise": "thruster", "reps": 15, "load": BB("135lb", "95lb")}],
  tags=["games", "2024", "venue-equipment", "barbell", "gymnastics"],
  notes=src(2024, 10) + "; contested immediately after Final 2421 with only 2 minutes of rest between")

print(f"Wrote 2024 Games entries; data/games now has "
      f"{len([f for f in os.listdir(OUT) if f.endswith('.json')])} JSON files.")
