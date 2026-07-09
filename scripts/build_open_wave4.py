import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "open")
os.makedirs(OUT, exist_ok=True)
VER = "1.1"
TODAY = "2026-07-09"

# CrossFit Open -- wave 4 (2011-2015), the final wave, closing out full Open
# history. Each verified against its official
# games.crossfit.com/workouts/open/<year>/<n> page (both men's and women's Rx).
def src(year, n):
    return (f"games.crossfit.com/workouts/open/{year}/{n} "
            f"(official CrossFit Games Open workout), retrieved {TODAY}")

def w(id, name, fmt, slug, movements=None, segments=None, format_meta=None, tags=None, notes=None):
    entry = {
        "id": id, "name": name, "category": "open", "format": fmt,
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
AMRAP = lambda n, s="rounds_reps": {"time_cap_minutes": n, "scoring": s}
RDS = lambda n: {"rounds": n, "scoring": "time"}

# ---- 2015 ----
w("open-15-1", "15.1", "amrap", (2015, 1),
  [{"exercise": "toes-to-bar", "reps": 15},
   {"exercise": "deadlift", "reps": 10, "load": BB("115lb", "75lb")},
   {"exercise": "snatch", "reps": 5, "load": BB("115lb", "75lb")}],
  format_meta=AMRAP(9), tags=["open", "2015", "barbell", "gymnastics"])

w("open-15-2", "15.2", "interval", (2015, 2),
  [{"exercise": "overhead-squat", "reps": [10, 12, 14], "load": BB("95lb", "65lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": [10, 12, 14]}],
  format_meta={"rounds": 2, "scoring": "reps"},
  tags=["open", "2015", "barbell", "gymnastics", "time-extension-ladder"],
  notes=src(2015, 2) + "; each value is one 3-minute window (0:00-3:00, 3:00-6:00, "
        "6:00-9:00, ...) in which 2 rounds of the listed reps must be completed; "
        "the rep count increases by 2 each window and the pattern continues "
        "indefinitely until the athlete fails to complete both rounds in a window "
        "(no fixed time cap); identical prescription to 14.2")

w("open-15-3", "15.3", "amrap", (2015, 3),
  [{"exercise": "muscle-up", "reps": 7},
   {"exercise": "wall-ball-shot", "reps": 50, "load": BB("20lb", "14lb")},
   {"exercise": "double-under", "reps": 100}],
  format_meta=AMRAP(14), tags=["open", "2015", "gymnastics", "jump-rope"])

w("open-15-4", "15.4", "amrap", (2015, 4),
  [{"exercise": "handstand-push-up", "reps": [3, 6, 9, 12, 15, 18, 21]},
   {"exercise": "clean", "reps": [3, 3, 3, 6, 6, 6, 9], "load": BB("185lb", "125lb")}],
  format_meta=AMRAP(8, "reps"),
  tags=["open", "2015", "gymnastics", "barbell", "ascending"],
  notes=src(2015, 4) + "; handstand push-ups increase by 3 reps every round; "
        "clean reps increase by 3 every 3rd round; pattern continues indefinitely "
        "until the 8-minute cap")

w("open-15-5", "15.5", "for_time", (2015, 5),
  [{"exercise": "row", "reps": [27, 21, 15, 9], "notes": "calories"},
   {"exercise": "thruster", "reps": [27, 21, 15, 9], "load": BB("95lb", "65lb")}],
  tags=["open", "2015", "barbell", "rowing", "ladder"])

# ---- 2014 ----
w("open-14-1", "14.1", "amrap", (2014, 1),
  [{"exercise": "double-under", "reps": 30},
   {"exercise": "power-snatch", "reps": 15, "load": BB("75lb", "55lb")}],
  format_meta=AMRAP(10), tags=["open", "2014", "barbell", "jump-rope"])

w("open-14-2", "14.2", "interval", (2014, 2),
  [{"exercise": "overhead-squat", "reps": [10, 12, 14], "load": BB("95lb", "65lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": [10, 12, 14]}],
  format_meta={"rounds": 2, "scoring": "reps"},
  tags=["open", "2014", "barbell", "gymnastics", "time-extension-ladder"],
  notes=src(2014, 2) + "; each value is one 3-minute window (0:00-3:00, 3:00-6:00, "
        "6:00-9:00, ...) in which 2 rounds of the listed reps must be completed; "
        "the rep count increases by 2 each window and the pattern continues "
        "indefinitely until the athlete fails to complete both rounds in a window "
        "(no fixed time cap)")

w("open-14-3", "14.3", "amrap", (2014, 3),
  [{"exercise": "deadlift", "reps": 10, "load": BB("135lb", "95lb")},
   {"exercise": "box-jump", "reps": 15},
   {"exercise": "deadlift", "reps": 15, "load": BB("185lb", "135lb")},
   {"exercise": "box-jump", "reps": 15},
   {"exercise": "deadlift", "reps": 20, "load": BB("225lb", "155lb")},
   {"exercise": "box-jump", "reps": 15},
   {"exercise": "deadlift", "reps": 25, "load": BB("275lb", "185lb")},
   {"exercise": "box-jump", "reps": 15},
   {"exercise": "deadlift", "reps": 30, "load": BB("315lb", "205lb")},
   {"exercise": "box-jump", "reps": 15},
   {"exercise": "deadlift", "reps": 35, "load": BB("365lb", "225lb")},
   {"exercise": "box-jump", "reps": 15}],
  format_meta=AMRAP(8, "reps"), tags=["open", "2014", "barbell", "bodyweight"])

w("open-14-4", "14.4", "amrap", (2014, 4),
  [{"exercise": "row", "reps": 60, "notes": "calories"},
   {"exercise": "toes-to-bar", "reps": 50},
   {"exercise": "wall-ball-shot", "reps": 40, "load": BB("20lb", "14lb")},
   {"exercise": "clean", "reps": 30, "load": BB("135lb", "95lb")},
   {"exercise": "muscle-up", "reps": 20}],
  format_meta=AMRAP(14, "reps"), tags=["open", "2014", "rowing", "barbell", "gymnastics"])

w("open-14-5", "14.5", "for_time", (2014, 5),
  [{"exercise": "thruster", "reps": [21, 18, 15, 12, 9, 6, 3], "load": BB("95lb", "65lb")},
   {"exercise": "burpee", "reps": [21, 18, 15, 12, 9, 6, 3]}],
  tags=["open", "2014", "barbell", "bodyweight", "ladder"])

# ---- 2013 ----
w("open-13-1", "13.1", "amrap", (2013, 1),
  [{"exercise": "burpee", "reps": 40},
   {"exercise": "snatch", "reps": 30, "load": BB("75lb", "45lb")},
   {"exercise": "burpee", "reps": 30},
   {"exercise": "snatch", "reps": 30, "load": BB("135lb", "75lb")},
   {"exercise": "burpee", "reps": 20},
   {"exercise": "snatch", "reps": 30, "load": BB("165lb", "100lb")},
   {"exercise": "burpee", "reps": 10},
   {"exercise": "snatch", "reps": "max", "load": BB("210lb", "120lb"), "notes": "AMRAP for remainder of the time cap"}],
  format_meta=AMRAP(17, "reps"), tags=["open", "2013", "barbell", "bodyweight"])

w("open-13-2", "13.2", "amrap", (2013, 2),
  [{"exercise": "shoulder-to-overhead", "reps": 5, "load": BB("115lb", "75lb")},
   {"exercise": "deadlift", "reps": 10, "load": BB("115lb", "75lb")},
   {"exercise": "box-jump", "reps": 15}],
  format_meta=AMRAP(10), tags=["open", "2013", "barbell", "bodyweight"])

w("open-13-3", "13.3", "amrap", (2013, 3),
  [{"exercise": "wall-ball-shot", "reps": 150, "load": BB("20lb", "14lb")},
   {"exercise": "double-under", "reps": 90},
   {"exercise": "muscle-up", "reps": 30}],
  format_meta=AMRAP(12, "reps"), tags=["open", "2013", "gymnastics", "jump-rope"])

w("open-13-4", "13.4", "amrap", (2013, 4),
  [{"exercise": "clean-and-jerk", "reps": [3, 6, 9, 12, 15, 18], "load": BB("135lb", "95lb")},
   {"exercise": "toes-to-bar", "reps": [3, 6, 9, 12, 15, 18]}],
  format_meta=AMRAP(7, "reps"),
  tags=["open", "2013", "barbell", "gymnastics", "ascending"],
  notes=src(2013, 4) + "; ascending ladder (+3 reps each round); pattern continues indefinitely until the 7-minute cap")

w("open-13-5", "13.5", "amrap", (2013, 5),
  [{"exercise": "thruster", "reps": 15, "load": BB("100lb", "65lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": 15}],
  format_meta=AMRAP(4, "reps"),
  tags=["open", "2013", "barbell", "gymnastics", "time-extension-ladder"],
  notes=src(2013, 5) + "; continuous 15/15 couplet; the 4-minute cap extends to "
        "8 minutes if 90 total reps are completed, to 12 minutes at 180 reps, "
        "and to 16 minutes at 270 reps")

# ---- 2012 ----
w("open-12-1", "12.1", "amrap", (2012, 1),
  [{"exercise": "burpee", "notes": "target 6 in above max standing reach; continuous max effort"}],
  format_meta=AMRAP(7, "reps"), tags=["open", "2012", "bodyweight", "single-movement"])

w("open-12-2", "12.2", "amrap", (2012, 2),
  [{"exercise": "snatch", "reps": 30, "load": BB("75lb", "45lb")},
   {"exercise": "snatch", "reps": 30, "load": BB("135lb", "75lb")},
   {"exercise": "snatch", "reps": 30, "load": BB("165lb", "100lb")},
   {"exercise": "snatch", "reps": "max", "load": BB("210lb", "120lb"), "notes": "AMRAP for remainder of the time cap"}],
  format_meta=AMRAP(10, "reps"), tags=["open", "2012", "barbell", "single-movement"])

w("open-12-3", "12.3", "amrap", (2012, 3),
  [{"exercise": "box-jump", "reps": 15},
   {"exercise": "push-press", "reps": 12, "load": BB("115lb", "75lb")},
   {"exercise": "toes-to-bar", "reps": 9}],
  format_meta=AMRAP(18, "reps"), tags=["open", "2012", "barbell", "bodyweight", "gymnastics"])

w("open-12-4", "12.4", "amrap", (2012, 4),
  [{"exercise": "wall-ball-shot", "reps": 150, "load": BB("20lb", "14lb")},
   {"exercise": "double-under", "reps": 90},
   {"exercise": "muscle-up", "reps": 30}],
  format_meta=AMRAP(12, "reps"), tags=["open", "2012", "gymnastics", "jump-rope"])

w("open-12-5", "12.5", "amrap", (2012, 5),
  [{"exercise": "thruster", "reps": [3, 6, 9, 12, 15, 18, 21], "load": BB("100lb", "65lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": [3, 6, 9, 12, 15, 18, 21]}],
  format_meta=AMRAP(7, "reps"),
  tags=["open", "2012", "barbell", "gymnastics", "ascending"],
  notes=src(2012, 5) + "; ascending ladder (+3 reps each round); pattern continues indefinitely until the 7-minute cap")

# ---- 2011 ----
w("open-11-1", "11.1", "amrap", (2011, 1),
  [{"exercise": "double-under", "reps": 30},
   {"exercise": "power-snatch", "reps": 15, "load": BB("75lb", "55lb")}],
  format_meta=AMRAP(10), tags=["open", "2011", "barbell", "jump-rope"])

w("open-11-2", "11.2", "amrap", (2011, 2),
  [{"exercise": "deadlift", "reps": 9, "load": BB("155lb", "100lb")},
   {"exercise": "push-up", "reps": 12},
   {"exercise": "box-jump", "reps": 15}],
  format_meta=AMRAP(15), tags=["open", "2011", "barbell", "bodyweight"])

w("open-11-3", "11.3", "amrap", (2011, 3),
  [{"exercise": "squat-clean", "reps": 1, "load": BB("165lb", "110lb")},
   {"exercise": "jerk", "reps": 1, "load": BB("165lb", "110lb")}],
  format_meta=AMRAP(5, "reps"),
  tags=["open", "2011", "barbell", "single-movement"],
  notes=src(2011, 3) + "; one round = one squat clean + one jerk; the clean must be completed before the jerk is attempted")

w("open-11-4", "11.4", "amrap", (2011, 4),
  [{"exercise": "bar-facing-burpee", "reps": 60},
   {"exercise": "overhead-squat", "reps": 30, "load": BB("120lb", "90lb")},
   {"exercise": "muscle-up", "reps": 10}],
  format_meta=AMRAP(10), tags=["open", "2011", "barbell", "bodyweight", "gymnastics"])

w("open-11-5", "11.5", "amrap", (2011, 5),
  [{"exercise": "power-clean", "reps": 5, "load": BB("145lb", "100lb")},
   {"exercise": "toes-to-bar", "reps": 10},
   {"exercise": "wall-ball-shot", "reps": 15, "load": BB("20lb", "14lb")}],
  format_meta=AMRAP(20), tags=["open", "2011", "barbell", "gymnastics"])

w("open-11-6", "11.6", "amrap", (2011, 6),
  [{"exercise": "thruster", "reps": [3, 6, 9, 12, 15, 18, 21], "load": BB("100lb", "65lb")},
   {"exercise": "chest-to-bar-pull-up", "reps": [3, 6, 9, 12, 15, 18, 21]}],
  format_meta=AMRAP(7, "reps"),
  tags=["open", "2011", "barbell", "gymnastics", "ascending"],
  notes=src(2011, 6) + "; ascending ladder (+3 reps each round); pattern continues indefinitely until the 7-minute cap")

print(f"Wrote {len([f for f in os.listdir(OUT) if f.endswith('.json')])} Open entries to {OUT}")
