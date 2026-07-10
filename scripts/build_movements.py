import json, os, glob

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data")

# Movement library for the dataset + the WodWiz app.
#
# LEGAL NOTE: movement *names* are facts / short phrases and are not copyrightable
# (37 CFR 202.1). The category grouping below is our own functional classification.
# `description` is intentionally null — any future movement description must be
# ORIGINAL text, never copied from CrossFit's or anyone else's glossary.
#
# This is a curated, comprehensive library of standard CrossFit movements — not
# just the ones the current workouts use. There is no official closed list, so
# this is a deliberate selection; extend it freely. A movement a WOD needs is
# REQUIRED here (validate.py rejects a WOD that references an unknown movement).
# Each movement lists the `workouts` (WOD ids) that use it — the movement->workout
# mapping — so a library-only movement is simply one with an empty `workouts` list.
# This script never modifies workout data.

GROUPS = {
    "barbell": [
        "back-squat", "front-squat", "overhead-squat", "box-squat",
        "back-rack-lunge", "front-rack-lunge", "barbell-overhead-lunge",
        "barbell-step-up", "good-morning",
        "deadlift", "sumo-deadlift", "romanian-deadlift", "stiff-legged-deadlift",
        "deficit-deadlift", "sumo-deadlift-high-pull",
        "clean", "power-clean", "squat-clean", "hang-clean", "hang-power-clean",
        "ground-to-overhead",
        "hang-squat-clean", "muscle-clean", "clean-pull", "clean-and-jerk",
        "bodyweight-clean-and-jerk",
        "snatch", "power-snatch", "squat-snatch", "hang-snatch", "hang-power-snatch",
        "muscle-snatch", "snatch-pull", "snatch-balance",
        "jerk", "split-jerk", "push-jerk", "push-press", "strict-press",
        "shoulder-to-overhead", "sots-press",
        "thruster", "bench-press", "floor-press", "bent-over-row", "pendlay-row",
        "overhead-walk",
    ],
    "dumbbell": [
        "dumbbell-thruster", "single-arm-dumbbell-thruster", "dumbbell-snatch",
        "dumbbell-power-snatch", "alternating-dumbbell-snatch",
        "alternating-dumbbell-power-snatch", "dumbbell-clean", "dumbbell-power-clean",
        "dumbbell-squat-clean", "dumbbell-hang-squat-clean", "dumbbell-split-clean",
        "dumbbell-hang-split-snatch", "dumbbell-clean-and-jerk",
        "dumbbell-squat-clean-thruster", "dumbbell-hang-clean-to-overhead",
        "dumbbell-hang-clean-and-jerk", "dumbbell-front-rack-squat",
        "dumbbell-push-press", "dumbbell-push-jerk",
        "dumbbell-shoulder-press", "dumbbell-strict-press", "dumbbell-shoulder-to-overhead",
        "dumbbell-hang-power-clean", "dumbbell-front-squat",
        "dumbbell-overhead-squat", "dumbbell-goblet-squat", "dumbbell-bench-press",
        "dumbbell-floor-press", "dumbbell-deadlift", "dumbbell-romanian-deadlift",
        "dumbbell-burpee-deadlift", "dumbbell-walking-lunge", "dumbbell-front-rack-lunge",
        "dumbbell-overhead-lunge", "dumbbell-box-step-up", "dumbbell-row",
        "renegade-row", "devils-press", "dumbbell-carry", "dumbbell-waiters-walk",
        "dumbbell-overhead-carry", "farmers-carry",
    ],
    "kettlebell": [
        "kettlebell-swing", "american-kettlebell-swing", "russian-kettlebell-swing",
        "single-arm-kettlebell-swing", "kettlebell-clean", "kettlebell-clean-and-jerk",
        "kettlebell-snatch", "kettlebell-thruster", "single-arm-kettlebell-thruster",
        "kettlebell-push-press", "kettlebell-press", "kettlebell-deadlift",
        "kettlebell-sumo-deadlift-high-pull", "goblet-squat", "kettlebell-front-rack-lunge",
        "kettlebell-overhead-lunge", "turkish-get-up", "kettlebell-windmill",
        "kettlebell-halo", "double-kettlebell-farmers-carry",
        "double-kettlebell-front-rack-carry", "double-kettlebell-front-rack-lunge",
        "double-kettlebell-overhead-carry",
    ],
    "gymnastics": [
        "pull-up", "kipping-pull-up", "butterfly-pull-up", "strict-pull-up",
        "chest-to-bar-pull-up", "l-pull-up", "weighted-pull-up", "burpee-pull-up",
        "jumping-pull-up", "chin-up", "negative-pull-up",
        "muscle-up", "bar-muscle-up", "ring-muscle-up", "strict-muscle-up",
        "burpee-muscle-up", "burpee-bar-muscle-up",
        "handstand-push-up", "strict-handstand-push-up", "kipping-handstand-push-up",
        "deficit-handstand-push-up", "freestanding-handstand-push-up",
        "wall-facing-handstand-push-up", "ring-handstand-push-up",
        "parallette-handstand-push-up",
        "handstand", "handstand-hold", "handstand-walk", "wall-climb", "wall-climb-over",
        "ring-dip", "bar-dip", "strict-dip", "ring-row", "ring-push-up", "push-up",
        "hand-release-push-up",
        "toes-to-bar", "toes-to-ring", "knees-to-elbows", "hanging-knee-raise",
        "hanging-hip-touch",
        "rope-climb", "legless-rope-climb", "pegboard",
        "pistol", "forward-roll", "ring-lower", "pull-over", "parallel-bar-traverse",
        "obstacle-pirouette",
        "sit-up", "ghd-sit-up", "ab-mat-sit-up", "v-up", "hollow-rock", "hollow-hold",
        "l-sit", "plank",
        "back-extension", "ghd-hip-extension", "hip-extension",
    ],
    "bodyweight": [
        "air-squat", "walking-lunge", "reverse-lunge", "jumping-lunge",
        "overhead-walking-lunge", "cossack-squat", "wall-sit",
        "burpee", "bar-facing-burpee", "burpee-over-the-bar", "lateral-burpee",
        "burpee-box-jump", "burpee-box-jump-over", "burpee-broad-jump",
        "burpee-over-dumbbell",
        "box-jump", "box-jump-over", "box-step-up", "broad-jump", "tuck-jump",
        "double-under", "single-under", "triple-under", "crossover-single-under",
        "jumping-jack", "bear-crawl", "mountain-climber", "high-knees", "inchworm",
        "flutter-kick",
    ],
    "monostructural": [
        "run", "sprint", "run-backward", "shuttle-sprint", "shuttle-run", "row",
        "ski-erg", "bike", "assault-bike", "echo-bike", "bike-erg", "swim", "kayak",
        "paddleboard",
        "stair-climb",
    ],
    "odd-object": [
        "wall-ball-shot", "medicine-ball-clean", "medicine-ball-sit-up",
        "medicine-ball-box-step-over", "ball-slam",
        "sandbag-carry", "sandbag-clean", "sandbag-ground-to-shoulder", "sandbag-squat",
        "sandbag-over-log", "jerry-bag-carry", "husafell-carry", "log-carry",
        "sledgehammer-strike", "medicine-ball-throw", "stake-drive", "sled-push",
        "sled-pull", "yoke-carry", "atlas-stone-over-shoulder", "d-ball-clean",
        "d-ball-over-shoulder", "tire-flip", "log-clean-and-jerk", "log-press",
        "plate-ground-to-overhead", "plate-carry",
    ],
}

EQUIPMENT = {
    "barbell": ["barbell"], "dumbbell": ["dumbbell"], "kettlebell": ["kettlebell"],
    "gymnastics": [], "bodyweight": [], "monostructural": [], "odd-object": [],
}

# Two distinct burpee standards, kept separate on purpose:
#   bar-facing-burpee = face the bar, chest to floor, two-foot jump over facing it
#   burpee-over-the-bar = lateral, jump/step over the bar
ALIASES = {
    "burpee-over-the-bar": ["lateral burpee over the bar"],
    "chest-to-bar-pull-up": ["chest-to-bar", "c2b"],
    "toes-to-bar": ["toes to bar", "t2b"],
    "knees-to-elbows": ["knees to elbows", "k2e"],
    "handstand-push-up": ["hspu"],
    "sumo-deadlift-high-pull": ["sdhp"],
    "double-under": ["du", "dubs"],
    "ghd-sit-up": ["ghd sit-up"],
    "clean-and-jerk": ["c&j"],
    "overhead-squat": ["ohs"],
    "american-kettlebell-swing": ["kettlebell swing (american)"],
    "russian-kettlebell-swing": ["kettlebell swing (russian)"],
    "wall-climb": ["wall walk"],
    "goblet-squat": ["kettlebell goblet squat"],
    "devils-press": ["devil's press"],
    "ab-mat-sit-up": ["abmat sit-up"],
    "bar-muscle-up": ["bmu"],
    "ring-muscle-up": ["rmu"],
    "handstand-walk": ["hs walk"],
    "pistol": ["single-leg squat", "pistol squat"],
    "wall-facing-handstand-push-up": ["chest-to-wall handstand push-up"],
}


def title(s):
    return " ".join(w.capitalize() for w in s.split("-"))


def build_category_map():
    category = {}
    for cat, slugs in GROUPS.items():
        for s in slugs:
            if s in category:
                raise SystemExit(f"duplicate movement slug: {s}")
            category[s] = cat
    return category


def movement_workouts():
    # slug -> sorted list of WOD ids that use it (the movement->workout mapping)
    mapping = {}
    for path in glob.glob(os.path.join(DATA, "*", "*.json")):
        if os.path.normpath(os.path.dirname(path)).endswith(os.sep + "staging"):
            continue
        wod = json.load(open(path, encoding="utf-8"))
        for m in wod.get("movements", []):
            mapping.setdefault(m["exercise"], set()).add(wod["id"])
    return {slug: sorted(ids) for slug, ids in mapping.items()}


def main():
    category = build_category_map()
    workouts = movement_workouts()

    # Superset invariant: every movement a WOD uses MUST be defined here (else the
    # dictionary and workouts drift and validate.py can't check integrity). Extra
    # library-only movements are allowed and expected.
    missing = set(workouts) - set(category)
    if missing:
        raise SystemExit(
            "movements used in WODs but missing from the library: "
            + ", ".join(sorted(missing))
        )

    movements = [{
        "id": slug,
        "name": title(slug),
        "category": cat,
        "equipment": EQUIPMENT[cat],
        "aliases": ALIASES.get(slug, []),
        "workouts": workouts.get(slug, []),
        "description": None,
    } for slug, cat in category.items()]
    movements.sort(key=lambda m: m["id"])

    out = os.path.join(DATA, "movements.json")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"count": len(movements), "movements": movements}, f, indent=2)
        f.write("\n")

    by_cat = {}
    for m in movements:
        by_cat[m["category"]] = by_cat.get(m["category"], 0) + 1
    in_ds = sum(1 for m in movements if m["workouts"])
    print(f"Wrote {len(movements)} movements -> {out}")
    print(f"  {in_ds} used in a WOD, {len(movements) - in_ds} library-only")
    print("  " + ", ".join(f"{c}: {n}" for c, n in sorted(by_cat.items())))


if __name__ == "__main__":
    main()
