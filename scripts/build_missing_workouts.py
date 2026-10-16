"""Six Hero WODs and eight community benchmarks that were missing from the catalog.

Every prescription was read from CrossFit's own pages (the benchmark pages for
the Heroes, the daily archive posts for the community workouts), retrieved
2026-10-16. Descriptions are in wod_descriptions.py. Idempotent: re-running
rewrites the same files.

Not added, for lack of a primary source: Kalsu (absent from the official Heroes
list) and King Kong (only a video caption on crossfit.com).
"""
import json
import os

from wod_descriptions import DESCRIPTIONS

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
VER = "1.0"
TODAY = "2026-10-16"


def hero_src(slug, first_posted=None):
    posted = f", first posted {first_posted}" if first_posted else ""
    return f"crossfit.com/benchmark/{slug} (official CrossFit Hero WOD page{posted}), retrieved 2026-10-16"


def daily_src(date, extra=""):
    y, m, d = date.split("-")
    return f"crossfit.com/workout/{y}/{m}/{d} (official CrossFit daily workout archive{extra}), retrieved 2026-10-16"


def w(folder, category, id, name, format, movements, format_meta, tags, notes):
    entry = {
        "id": id, "name": name, "category": category, "format": format,
        "format_meta": format_meta,
        "movements": movements,
        "partition": None,
        "scaling": None,
        "origin": None,
        "tags": tags,
        "description": DESCRIPTIONS.get(id),
        "source_notes": notes,
        "schema_version": VER,
        "last_updated": TODAY,
    }
    out = os.path.join(DATA, folder)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, f"{id}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(entry, f, indent=2, ensure_ascii=False)
        f.write("\n")


def L(m, f=None):
    return {"rx_male": m, "rx_female": f} if f else {"rx_male": m}


# ---------------- Heroes ----------------
w("heroes", "hero", "hidalgo", "Hidalgo", "for_time",
  [{"exercise": "run", "distance_m": 3218, "notes": "rest 2 minutes after this run"},
   {"exercise": "squat-clean", "reps": 20, "load": L("135lb", "95lb")},
   {"exercise": "box-jump", "reps": 20, "load": L('24"', '20"')},
   {"exercise": "overhead-walking-lunge", "reps": 20, "load": L("45lb plate", "25lb plate")},
   {"exercise": "box-jump", "reps": 20, "load": L('24"', '20"')},
   {"exercise": "squat-clean", "reps": 20, "load": L("135lb", "95lb"),
    "notes": "rest 2 minutes after this set"},
   {"exercise": "run", "distance_m": 3218}],
  {"scoring": "time"}, ["running", "barbell", "plyometric", "vest-optional"],
  hero_src("hidalgo", "Dec 29, 2011") + "; the page suggests a 20-lb vest or body armor if you have one")

w("heroes", "hero", "jag-28", "Jag 28", "for_time",
  [{"exercise": "run", "distance_m": 800},
   {"exercise": "kettlebell-swing", "reps": 28, "load": L("70lb", "53lb")},
   {"exercise": "strict-pull-up", "reps": 28},
   {"exercise": "kettlebell-clean-and-jerk", "reps": 28, "load": L("70lb", "53lb")},
   {"exercise": "strict-pull-up", "reps": 28},
   {"exercise": "run", "distance_m": 800}],
  {"scoring": "time"}, ["running", "kettlebell", "gymnastics"],
  hero_src("jag-28", "May 13, 2012"))

w("heroes", "hero", "holbrook", "Holbrook", "interval",
  [{"exercise": "thruster", "reps": 5, "load": L("115lb", "75lb")},
   {"exercise": "pull-up", "reps": 10},
   {"exercise": "sprint", "distance_m": 100}],
  {"rounds": 10, "rest_between_seconds": 60, "scoring": "time"},
  ["barbell", "gymnastics", "sprint", "10-rounds"],
  hero_src("holbrook") + "; each round is timed on its own, 1 minute of rest between rounds")

w("heroes", "hero", "hall", "Hall", "interval",
  [{"exercise": "clean", "reps": 3, "load": L("225lb", "155lb")},
   {"exercise": "sprint", "distance_m": 200},
   {"exercise": "kettlebell-snatch", "reps": 20, "load": L("53lb", "35lb"),
    "notes": "10 reps each arm"}],
  {"rounds": 5, "rest_between_seconds": 120, "scoring": "time"},
  ["barbell", "kettlebell", "sprint", "5-rounds"],
  hero_src("hall", "June 7, 2015") + "; 2 minutes of rest between rounds")

w("heroes", "hero", "wood", "Wood", "interval",
  [{"exercise": "run", "distance_m": 400},
   {"exercise": "burpee-box-jump", "reps": 10, "load": L('24"', '20"')},
   {"exercise": "sumo-deadlift-high-pull", "reps": 10, "load": L("95lb", "65lb")},
   {"exercise": "thruster", "reps": 10, "load": L("95lb", "65lb")}],
  {"rounds": 5, "rest_between_seconds": 60, "scoring": "time"},
  ["running", "barbell", "5-rounds"],
  hero_src("wood", "Dec 7, 2011") + "; 1 minute of rest between rounds")

w("heroes", "hero", "hammer", "Hammer", "interval",
  [{"exercise": "power-clean", "reps": 5, "load": L("135lb", "95lb")},
   {"exercise": "front-squat", "reps": 10, "load": L("135lb", "95lb")},
   {"exercise": "jerk", "reps": 5, "load": L("135lb", "95lb")},
   {"exercise": "pull-up", "reps": 20}],
  {"rounds": 5, "rest_between_seconds": 90, "scoring": "time"},
  ["barbell", "gymnastics", "5-rounds"],
  hero_src("hammer", "Apr 17, 2011") + "; each round is timed on its own, 90 seconds of rest between rounds")

# ---------------- Community benchmarks ----------------
w("community", "community", "fight-gone-bad", "Fight Gone Bad", "interval",
  [{"exercise": "wall-ball-shot", "load": L("20lb"), "notes": "10 ft target; 1 minute, scored in reps"},
   {"exercise": "sumo-deadlift-high-pull", "load": L("75lb"), "notes": "1 minute, scored in reps"},
   {"exercise": "box-jump", "load": L('20"'), "notes": "1 minute, scored in reps"},
   {"exercise": "push-press", "load": L("75lb"), "notes": "1 minute, scored in reps"},
   {"exercise": "row", "notes": "1 minute, scored in calories"}],
  {"rounds": 3, "work_seconds": 60, "rest_between_seconds": 60, "scoring": "reps"},
  ["benchmark", "5-stations", "3-rounds", "points"],
  daily_src("2008-06-25", ", first posted")
  + "; one point per rep (per calorie on the rower), 1 minute of rest between the 5-minute rounds; the page lists a single set of loads")

w("community", "community", "filthy-fifty", "Filthy Fifty", "for_time",
  [{"exercise": "box-jump", "reps": 50, "load": L('24"')},
   {"exercise": "jumping-pull-up", "reps": 50},
   {"exercise": "kettlebell-swing", "reps": 50, "load": L("1 pood")},
   {"exercise": "walking-lunge", "reps": 50, "notes": "steps"},
   {"exercise": "knees-to-elbows", "reps": 50},
   {"exercise": "push-press", "reps": 50, "load": L("45lb")},
   {"exercise": "back-extension", "reps": 50},
   {"exercise": "wall-ball-shot", "reps": 50, "load": L("20lb")},
   {"exercise": "burpee", "reps": 50},
   {"exercise": "double-under", "reps": 50}],
  {"scoring": "time"}, ["chipper", "benchmark", "high-volume"],
  daily_src("2005-06-19", ", first posted; reposted 2009-04-23")
  + "; the name comes from crossfit.com/essentials/crossfit-15-benchmarks, the posts themselves do not name it")

w("community", "community", "nasty-girls", "Nasty Girls", "for_time",
  [{"exercise": "air-squat", "reps": 50},
   {"exercise": "muscle-up", "reps": 7},
   {"exercise": "hang-power-clean", "reps": 10, "load": L("135lb")}],
  {"rounds": 3, "scoring": "time"}, ["benchmark", "gymnastics", "barbell", "3-rounds"],
  daily_src("2008-01-25", ", first posted") + "; the page lists a single load")

w("community", "community", "the-chief", "The Chief", "interval",
  [{"exercise": "power-clean", "reps": 3, "load": L("135lb")},
   {"exercise": "push-up", "reps": 6},
   {"exercise": "air-squat", "reps": 9}],
  {"rounds": 5, "work_seconds": 180, "rest_seconds": 60, "scoring": "rounds_reps"},
  ["benchmark", "amrap", "5-cycles"],
  daily_src("2008-09-14", ", first posted")
  + "; five 3-minute AMRAP cycles with 1 minute of rest, post the rounds completed in each; the page lists a single load")

w("community", "community", "the-ghost", "The Ghost", "interval",
  [{"exercise": "row", "notes": "1 minute, scored in calories"},
   {"exercise": "burpee", "notes": "1 minute, scored in reps"},
   {"exercise": "double-under", "notes": "1 minute, scored in reps"}],
  {"rounds": 6, "work_seconds": 60, "rest_seconds": 60, "scoring": "reps"},
  ["benchmark", "monostructural", "6-rounds"],
  daily_src("2014-06-17")
  + "; 1 minute on each movement, then 1 minute of rest, six times; score the total of each movement")

w("community", "community", "bear-complex", "Bear Complex", "complex",
  [{"exercise": "power-clean", "reps": 1},
   {"exercise": "front-squat", "reps": 1},
   {"exercise": "push-press", "reps": 1},
   {"exercise": "back-squat", "reps": 1},
   {"exercise": "push-press", "reps": 1}],
  {"rounds": 5, "scoring": "load"}, ["benchmark", "barbell", "complex"],
  "crossfit.com/essentials/the-power-clean (Common Power Clean Workouts), retrieved 2026-10-16; five rounds, each of 7 unbroken sets of the complex, scored by the load used")

w("community", "community", "tabata-something-else", "Tabata Something Else", "tabata",
  [{"exercise": "pull-up"}, {"exercise": "push-up"}, {"exercise": "sit-up"}, {"exercise": "air-squat"}],
  {"work_seconds": 20, "rest_seconds": 10, "rounds": 8, "scoring": "reps"},
  ["benchmark", "tabata", "bodyweight"],
  daily_src("2017-08-25")
  + "; 8 intervals of 20 seconds on, 10 off for each movement, no rest between movements, score the total reps of all 32 intervals")

w("community", "community", "tabata-this", "Tabata This", "tabata",
  [{"exercise": "row", "notes": "scored in calories"}, {"exercise": "air-squat"},
   {"exercise": "pull-up"}, {"exercise": "push-up"}, {"exercise": "sit-up"}],
  {"work_seconds": 20, "rest_seconds": 10, "rounds": 8, "scoring": "reps"},
  ["benchmark", "tabata"],
  daily_src("2015-01-11")
  + "; 1 minute of rest after each of the first four movements, score the lowest interval for each movement (calories on the row) and add them")


# ---------------- Added later (2026-10-16, at Ricky's request) ----------------
# The official pages for these two would not load, so the prescriptions come from
# CrossFit-hosted excerpts (the CrossFit discussion board thread "Beware of Kalsu",
# the Games video page for Josh Everett's King Kong) and match every secondary
# source. Marked in source_notes so a reader can see the weaker footing.
w("heroes", "hero", "kalsu", "Kalsu", "for_time",
  [{"exercise": "burpee", "reps": 5, "notes": "at the start of every minute, until the thrusters are finished"},
   {"exercise": "thruster", "reps": 100, "load": L("135lb", "95lb"), "notes": "fit them into the rest of each minute"}],
  {"scoring": "time"}, ["barbell", "burpee", "every-minute", "high-volume"],
  "CrossFit discussion board thread 'Beware of Kalsu' (board.crossfit.com/archive/index.php/t-54457.html), retrieved 2026-10-16; not on the official Heroes list page, prescription confirmed by every secondary source; the 95-lb women's load is the commonly posted standard")

w("community", "community", "king-kong", "King Kong", "for_time",
  [{"exercise": "deadlift", "reps": 1, "load": L("455lb")},
   {"exercise": "muscle-up", "reps": 2},
   {"exercise": "squat-clean", "reps": 3, "load": L("250lb")},
   {"exercise": "handstand-push-up", "reps": 4}],
  {"rounds": 3, "scoring": "time"}, ["benchmark", "heavy", "gymnastics", "3-rounds"],
  "games.crossfit.com/video/josh-everetts-king-kong (CrossFit Games video page, October 2008), retrieved 2026-10-16; posted as a challenge from CrossFit Alexandria and answered by Josh Everett; the rep ladder 1-2-3-4 follows the numbered list on that page and matches secondary sources; single load, no women's standard published")
