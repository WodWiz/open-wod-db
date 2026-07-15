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

# Biomechanical movement pattern(s), independent of the equipment-based `category`
# above. A movement can hit more than one pattern (e.g. a thruster is a squat AND
# a push; a clean-and-jerk is bucketed as a single "olympic" pattern rather than
# decomposed into hinge/pull/squat/push, matching how programming tools group the
# barbell classics). This is our own functional classification, not copied from
# any glossary. Every slug in GROUPS must have an entry here (checked below).
PATTERNS = {
    # barbell
    "back-squat": ["squat"], "front-squat": ["squat"], "overhead-squat": ["squat"],
    "box-squat": ["squat"],
    "back-rack-lunge": ["lunge"], "front-rack-lunge": ["lunge"],
    "barbell-overhead-lunge": ["lunge"], "barbell-step-up": ["lunge"],
    "good-morning": ["hinge"],
    "deadlift": ["hinge"], "sumo-deadlift": ["hinge"], "romanian-deadlift": ["hinge"],
    "stiff-legged-deadlift": ["hinge"], "deficit-deadlift": ["hinge"],
    "sumo-deadlift-high-pull": ["hinge", "pull"],
    "clean": ["olympic"], "power-clean": ["olympic"], "squat-clean": ["olympic"],
    "hang-clean": ["olympic"], "hang-power-clean": ["olympic"],
    "ground-to-overhead": ["olympic"], "hang-squat-clean": ["olympic"],
    "muscle-clean": ["olympic"], "clean-pull": ["olympic", "pull"],
    "clean-and-jerk": ["olympic"], "bodyweight-clean-and-jerk": ["olympic"],
    "snatch": ["olympic"], "power-snatch": ["olympic"], "squat-snatch": ["olympic"],
    "hang-snatch": ["olympic"], "hang-power-snatch": ["olympic"],
    "muscle-snatch": ["olympic"], "snatch-pull": ["olympic", "pull"],
    "snatch-balance": ["olympic"],
    "jerk": ["push"], "split-jerk": ["push"], "push-jerk": ["push"],
    "push-press": ["push"], "strict-press": ["push"], "shoulder-to-overhead": ["push"],
    "sots-press": ["push"],
    "thruster": ["squat", "push"],
    "bench-press": ["push"], "floor-press": ["push"],
    "bent-over-row": ["pull"], "pendlay-row": ["pull"],
    "overhead-walk": ["carry"],
    # dumbbell
    "dumbbell-thruster": ["squat", "push"], "single-arm-dumbbell-thruster": ["squat", "push"],
    "dumbbell-snatch": ["olympic"], "dumbbell-power-snatch": ["olympic"],
    "alternating-dumbbell-snatch": ["olympic"], "alternating-dumbbell-power-snatch": ["olympic"],
    "dumbbell-clean": ["olympic"], "dumbbell-power-clean": ["olympic"],
    "dumbbell-squat-clean": ["olympic"], "dumbbell-hang-squat-clean": ["olympic"],
    "dumbbell-split-clean": ["olympic"], "dumbbell-hang-split-snatch": ["olympic"],
    "dumbbell-clean-and-jerk": ["olympic"],
    "dumbbell-squat-clean-thruster": ["olympic", "squat", "push"],
    "dumbbell-hang-clean-to-overhead": ["olympic"], "dumbbell-hang-clean-and-jerk": ["olympic"],
    "dumbbell-front-rack-squat": ["squat"],
    "dumbbell-push-press": ["push"], "dumbbell-push-jerk": ["push"],
    "dumbbell-shoulder-press": ["push"], "dumbbell-strict-press": ["push"],
    "dumbbell-shoulder-to-overhead": ["push"], "dumbbell-hang-power-clean": ["olympic"],
    "dumbbell-front-squat": ["squat"], "dumbbell-overhead-squat": ["squat"],
    "dumbbell-goblet-squat": ["squat"],
    "dumbbell-bench-press": ["push"], "dumbbell-floor-press": ["push"],
    "dumbbell-deadlift": ["hinge"], "dumbbell-romanian-deadlift": ["hinge"],
    "dumbbell-burpee-deadlift": ["hinge", "core"],
    "dumbbell-walking-lunge": ["lunge"], "dumbbell-front-rack-lunge": ["lunge"],
    "dumbbell-overhead-lunge": ["lunge"], "dumbbell-box-step-up": ["lunge"],
    "dumbbell-row": ["pull"], "renegade-row": ["pull", "core"],
    "devils-press": ["olympic", "core"],
    "dumbbell-carry": ["carry"], "dumbbell-waiters-walk": ["carry"],
    "dumbbell-overhead-carry": ["carry"], "farmers-carry": ["carry"],
    # kettlebell
    "kettlebell-swing": ["hinge"], "american-kettlebell-swing": ["hinge"],
    "russian-kettlebell-swing": ["hinge"], "single-arm-kettlebell-swing": ["hinge"],
    "kettlebell-clean": ["olympic"], "kettlebell-clean-and-jerk": ["olympic"],
    "kettlebell-snatch": ["olympic"],
    "kettlebell-thruster": ["squat", "push"], "single-arm-kettlebell-thruster": ["squat", "push"],
    "kettlebell-push-press": ["push"], "kettlebell-press": ["push"],
    "kettlebell-deadlift": ["hinge"], "kettlebell-sumo-deadlift-high-pull": ["hinge", "pull"],
    "goblet-squat": ["squat"],
    "kettlebell-front-rack-lunge": ["lunge"], "kettlebell-overhead-lunge": ["lunge"],
    "turkish-get-up": ["core"], "kettlebell-windmill": ["core"], "kettlebell-halo": ["core"],
    "double-kettlebell-farmers-carry": ["carry"], "double-kettlebell-front-rack-carry": ["carry"],
    "double-kettlebell-front-rack-lunge": ["lunge"], "double-kettlebell-overhead-carry": ["carry"],
    # gymnastics
    "pull-up": ["pull"], "kipping-pull-up": ["pull"], "butterfly-pull-up": ["pull"],
    "strict-pull-up": ["pull"], "chest-to-bar-pull-up": ["pull"],
    "l-pull-up": ["pull", "core"], "weighted-pull-up": ["pull"],
    "burpee-pull-up": ["core", "pull"], "jumping-pull-up": ["pull"],
    "chin-up": ["pull"], "negative-pull-up": ["pull"],
    "muscle-up": ["pull", "push"], "bar-muscle-up": ["pull", "push"],
    "ring-muscle-up": ["pull", "push"], "strict-muscle-up": ["pull", "push"],
    "burpee-muscle-up": ["core", "pull", "push"], "burpee-bar-muscle-up": ["core", "pull", "push"],
    "handstand-push-up": ["push"], "strict-handstand-push-up": ["push"],
    "kipping-handstand-push-up": ["push"], "deficit-handstand-push-up": ["push"],
    "freestanding-handstand-push-up": ["push"], "wall-facing-handstand-push-up": ["push"],
    "ring-handstand-push-up": ["push"], "parallette-handstand-push-up": ["push"],
    "handstand": ["push"], "handstand-hold": ["push"], "handstand-walk": ["push", "carry"],
    "wall-climb": ["push"], "wall-climb-over": ["push"],
    "ring-dip": ["push"], "bar-dip": ["push"], "strict-dip": ["push"],
    "ring-row": ["pull"], "ring-push-up": ["push"], "push-up": ["push"],
    "hand-release-push-up": ["push"],
    "toes-to-bar": ["core"], "toes-to-ring": ["core"], "knees-to-elbows": ["core"],
    "hanging-knee-raise": ["core"], "hanging-hip-touch": ["core"],
    "rope-climb": ["pull"], "legless-rope-climb": ["pull"], "pegboard": ["pull"],
    "pistol": ["squat"], "forward-roll": ["core"], "ring-lower": ["pull"],
    "pull-over": ["pull"], "parallel-bar-traverse": ["pull"], "obstacle-pirouette": ["core"],
    "sit-up": ["core"], "ghd-sit-up": ["core"], "ab-mat-sit-up": ["core"], "v-up": ["core"],
    "hollow-rock": ["core"], "hollow-hold": ["core"], "l-sit": ["core"], "plank": ["core"],
    "back-extension": ["hinge"], "ghd-hip-extension": ["hinge"], "hip-extension": ["hinge"],
    # bodyweight
    "air-squat": ["squat"],
    "walking-lunge": ["lunge"], "reverse-lunge": ["lunge"], "jumping-lunge": ["lunge"],
    "overhead-walking-lunge": ["lunge"],
    "cossack-squat": ["squat"], "wall-sit": ["squat"],
    "burpee": ["core"], "bar-facing-burpee": ["core"], "burpee-over-the-bar": ["core"],
    "lateral-burpee": ["core"],
    "burpee-box-jump": ["core", "lunge"], "burpee-box-jump-over": ["core", "lunge"],
    "burpee-broad-jump": ["core"], "burpee-over-dumbbell": ["core"],
    "box-jump": ["lunge"], "box-jump-over": ["lunge"], "box-step-up": ["lunge"],
    "broad-jump": ["lunge"], "tuck-jump": ["squat"],
    "double-under": ["monostructural"], "single-under": ["monostructural"],
    "triple-under": ["monostructural"], "crossover-single-under": ["monostructural"],
    "jumping-jack": ["monostructural"],
    "bear-crawl": ["core"], "mountain-climber": ["core"],
    "high-knees": ["monostructural"], "inchworm": ["core"], "flutter-kick": ["core"],
    # monostructural
    "run": ["monostructural"], "sprint": ["monostructural"], "run-backward": ["monostructural"],
    "shuttle-sprint": ["monostructural"], "shuttle-run": ["monostructural"],
    "row": ["monostructural"], "ski-erg": ["monostructural"], "bike": ["monostructural"],
    "assault-bike": ["monostructural"], "echo-bike": ["monostructural"],
    "bike-erg": ["monostructural"], "swim": ["monostructural"], "kayak": ["monostructural"],
    "paddleboard": ["monostructural"], "stair-climb": ["monostructural"],
    # odd-object
    "wall-ball-shot": ["squat", "push"], "medicine-ball-clean": ["olympic"],
    "medicine-ball-sit-up": ["core"], "medicine-ball-box-step-over": ["lunge"],
    "ball-slam": ["core"],
    "sandbag-carry": ["carry"], "sandbag-clean": ["olympic"],
    "sandbag-ground-to-shoulder": ["olympic"], "sandbag-squat": ["squat"],
    "sandbag-over-log": ["hinge"],
    "jerry-bag-carry": ["carry"], "husafell-carry": ["carry"], "log-carry": ["carry"],
    "sledgehammer-strike": ["core"], "medicine-ball-throw": ["core"], "stake-drive": ["core"],
    "sled-push": ["push"], "sled-pull": ["pull"], "yoke-carry": ["carry"],
    "atlas-stone-over-shoulder": ["hinge"], "d-ball-clean": ["olympic"],
    "d-ball-over-shoulder": ["hinge"], "tire-flip": ["hinge"],
    "log-clean-and-jerk": ["olympic"], "log-press": ["push"],
    "plate-ground-to-overhead": ["olympic"], "plate-carry": ["carry"],
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


# Original, hand-written technique descriptions — never copied 
# from any other glossary (see the LEGAL NOTE above). One or two sentences: what
# the movement is and the setup/technique detail that distinguishes it from
# its nearest relatives (e.g. a power vs. squat clean, or a strict vs. kipping
# pull-up). Deliberately not exhaustive coaching cues or safety instructions —
# just enough to identify and differentiate the movement for a reader who
# already trains, matching this dataset's factual, non-editorial tone.
DESCRIPTIONS = {
    # barbell
    "back-squat": "A barbell held across the upper back (low- or high-bar) while squatting to at least hip-crease-below-knee depth, then standing back up — the foundational lower-body strength lift.",
    "front-squat": "Barbell racked across the front deltoids and collarbones with elbows high, squatting to full depth — builds quad and core strength and carries directly into the clean.",
    "overhead-squat": "Barbell locked out overhead in a wide snatch grip while squatting to full depth — demands shoulder stability, ankle/hip mobility, and a tight overhead position throughout.",
    "box-squat": "Back squat performed to a box or bench, briefly sitting back to touch it before standing — reinforces hip-driven depth and a controlled bottom position.",
    "back-rack-lunge": "Barbell racked on the back as in a back squat while stepping into a lunge, alternating legs — combines squat-pattern loading with single-leg stability.",
    "front-rack-lunge": "Barbell held in the front rack (as in a front squat) while lunging — the upright torso the front rack demands makes this more quad- and core-dominant than a back-rack lunge.",
    "barbell-overhead-lunge": "Barbell locked out overhead while lunging forward or walking — combines overhead stability with a single-leg squat pattern.",
    "barbell-step-up": "Stepping up onto a box with a loaded barbell on the back or in the front rack, driving through the lead leg to full hip extension at the top.",
    "good-morning": "Barbell on the back, hinging forward at the hips with a flat back and soft knees until the torso nears parallel to the floor, then returning upright — targets the posterior chain.",
    "deadlift": "Barbell lifted from the floor to full hip and knee extension with a flat back and the bar close to the shins — the fundamental hip-hinge strength movement.",
    "sumo-deadlift": "Deadlift with a wide stance and hands inside the knees, more upright torso than a conventional pull — shifts more of the load to the hips and inner thighs.",
    "romanian-deadlift": "Barbell lowered from the hips (not the floor) with knees only slightly bent, pushing the hips back until a hamstring stretch is felt, then driving back to standing.",
    "stiff-legged-deadlift": "Deadlift variation with minimal knee bend, hinging almost entirely from the hips — isolates the hamstrings and lower back.",
    "deficit-deadlift": "Deadlift performed standing on a raised platform, increasing the range of motion off the floor — demands extra hip and ankle mobility off the bottom.",
    "sumo-deadlift-high-pull": "Sumo-stance deadlift pulled explosively upward past the hips into a high pull, elbows leading, bar finishing near the collarbone.",
    "clean": "Barbell pulled from the floor and received in a front-rack squat in one continuous motion — the catch-all term for the squat clean unless a variant is specified.",
    "power-clean": "Barbell pulled from the floor and caught in the front rack above parallel (a partial-depth squat) — demands more raw pulling power since there's less assistance from the squat.",
    "squat-clean": "Barbell pulled from the floor and received in a full-depth front squat, standing up to complete the lift — the standard, most efficient way to move the heaviest load into the front rack.",
    "hang-clean": "Clean initiated from a 'hang' position (bar at or above the knee, not the floor) rather than pulling from the ground — removes the initial floor pull, emphasizing the second pull and catch.",
    "hang-power-clean": "Hang clean caught above parallel in a partial-depth squat rather than full depth.",
    "ground-to-overhead": "Any barbell movement taking the bar from the floor to locked out overhead by whatever method the athlete chooses — clean-and-jerk, clean-and-press, or a muscle clean into a press.",
    "hang-squat-clean": "Clean started from the hang position and received in a full-depth front squat.",
    "muscle-clean": "Clean received standing tall with no dip under the bar — pulled high enough to rack it without a re-bend of the knees, emphasizing pull strength over speed-under-the-bar.",
    "clean-pull": "The pulling portion of a clean (floor to full extension) performed without racking the bar — used to build pulling strength and speed without the catch.",
    "clean-and-jerk": "A clean immediately followed by a jerk to lock the bar out overhead — the classic two-lift combination used to move the heaviest loads from the ground to overhead.",
    "bodyweight-clean-and-jerk": "A clean-and-jerk loaded relative to the athlete's own bodyweight rather than a fixed load, so the percentage — not the number on the bar — is the prescription.",
    "snatch": "Barbell pulled from the floor to locked-out overhead in one continuous motion, caught in a full overhead squat — the most technical lift in the sport.",
    "power-snatch": "Snatch caught overhead above parallel in a partial-depth squat rather than a full overhead squat.",
    "squat-snatch": "Snatch received in a full-depth overhead squat, standing to complete the lift — the standard, most efficient snatch technique.",
    "hang-snatch": "Snatch initiated from the hang position rather than the floor, emphasizing the second pull and the catch.",
    "hang-power-snatch": "Hang snatch caught above parallel rather than in a full overhead squat.",
    "muscle-snatch": "Snatch pulled and pressed out overhead with no re-bend of the knees to catch it — an overhead-strength and technique builder, not a max-load lift.",
    "snatch-pull": "The pulling portion of a snatch (floor to full extension, wide grip) performed without the catch — builds pull speed and positions without receiving the bar.",
    "snatch-balance": "Barbell taken from behind the neck, dropped under with a slight dip and drive, and caught in an overhead squat — a speed-under-the-bar and overhead-stability drill for the snatch.",
    "jerk": "Barbell driven from the front rack to locked-out overhead using a dip-drive and a foot-split (or push jerk) receiving position — the second half of the clean-and-jerk.",
    "split-jerk": "Jerk received with a front-to-back foot split, one leg forward and one back, locking the bar out overhead — the most common competitive jerk style.",
    "push-jerk": "Jerk received with both feet moving straight out to a quarter-squat rather than splitting front-to-back.",
    "push-press": "Barbell pressed overhead using a short leg dip-and-drive for momentum, rather than a strict press from a static stand.",
    "strict-press": "Barbell pressed from the front rack to locked-out overhead using shoulder strength alone, with no leg drive or hip dip.",
    "shoulder-to-overhead": "Any method of moving a loaded barbell from the front rack to locked-out overhead by the athlete's choice — strict press, push press, or jerk.",
    "sots-press": "Overhead press performed from the bottom of an overhead squat position, bar taken from behind the neck — an advanced overhead-mobility and stability drill.",
    "thruster": "Front squat driven directly into a push press as the athlete stands, using the leg drive out of the bottom of the squat to help send the bar overhead — one continuous squat-to-press movement.",
    "bench-press": "Barbell lowered to the chest while lying on a bench and pressed back to full lockout — the classic horizontal pressing strength lift.",
    "floor-press": "Bench press performed lying on the floor instead of a bench, so the range of motion stops when the upper arms touch the ground — reduces shoulder strain and emphasizes lockout strength.",
    "bent-over-row": "Torso hinged forward and near-parallel to the floor, pulling a barbell to the lower ribs/stomach and lowering under control — targets the mid-back and lats.",
    "pendlay-row": "Bent-over row performed with the bar returning to a dead stop on the floor between every rep, torso held parallel throughout — a stricter, more explosive row variant.",
    "overhead-walk": "Walking a set distance with a loaded barbell locked out overhead — a loaded carry that tests overhead stability and core bracing under fatigue.",
    # dumbbell
    "dumbbell-thruster": "Front squat with a dumbbell (or two) at the shoulders driven directly into an overhead press as the athlete stands — the dumbbell version of the barbell thruster.",
    "single-arm-dumbbell-thruster": "Thruster performed holding one dumbbell in a single-arm front rack, alternating or fixed to one side per the workout's prescription — adds an anti-rotation core demand.",
    "dumbbell-snatch": "A single dumbbell pulled from the floor to locked-out overhead in one continuous motion, typically alternating arms — the dumbbell analog of the barbell snatch.",
    "dumbbell-power-snatch": "Dumbbell snatch caught with a partial dip rather than a full squat receive — usually interchangeable with dumbbell-snatch, naming the catch depth explicitly.",
    "alternating-dumbbell-snatch": "Dumbbell snatch performed for reps, switching arms either every rep or on a set schedule per the workout.",
    "alternating-dumbbell-power-snatch": "Alternating dumbbell snatch caught without a full squat, just a partial dip-and-catch.",
    "dumbbell-clean": "A dumbbell (or pair) pulled from the floor and received in the front rack, typically with a slight squat — the dumbbell analog of the barbell clean.",
    "dumbbell-power-clean": "Dumbbell clean caught above parallel with only a partial dip rather than a full-depth squat.",
    "dumbbell-squat-clean": "Dumbbell clean received in a full-depth front squat before standing.",
    "dumbbell-hang-squat-clean": "Dumbbell squat clean initiated from a hang position at or above the knee rather than pulling from the floor.",
    "dumbbell-split-clean": "Dumbbell clean received in a front-to-back split stance rather than a squat, similar in spirit to a split jerk's receiving position.",
    "dumbbell-hang-split-snatch": "Dumbbell snatch initiated from the hang and received in a front-to-back split stance overhead.",
    "dumbbell-clean-and-jerk": "A dumbbell clean immediately followed by a jerk to lock the dumbbell(s) out overhead.",
    "dumbbell-squat-clean-thruster": "A dumbbell squat clean received in the bottom of the squat and driven straight up into an overhead press without standing up in between — one continuous rep.",
    "dumbbell-hang-clean-to-overhead": "Dumbbell hang clean immediately followed by any method of getting it overhead (press, push press, or jerk), per the athlete's choice.",
    "dumbbell-hang-clean-and-jerk": "Dumbbell clean initiated from the hang, followed by a jerk to lock it out overhead.",
    "dumbbell-front-rack-squat": "Squat holding a dumbbell (or pair) in the front rack position at the shoulders throughout the descent and stand.",
    "dumbbell-push-press": "Dumbbell pressed overhead using a short dip-and-drive from the legs — the dumbbell version of the barbell push press.",
    "dumbbell-push-jerk": "Dumbbell driven overhead with a dip-drive and a quarter-squat receive — the dumbbell version of the push jerk.",
    "dumbbell-shoulder-press": "Dumbbell pressed from the shoulder to locked-out overhead with no leg drive — a strict, single- or double-arm overhead press.",
    "dumbbell-strict-press": "Dumbbell pressed overhead using shoulder strength alone, no hip or leg drive, matching the strictness standard of a barbell strict press.",
    "dumbbell-shoulder-to-overhead": "Any method of moving a dumbbell from the shoulder to locked-out overhead by the athlete's choice — press, push press, or push jerk.",
    "dumbbell-hang-power-clean": "Dumbbell hang clean caught above parallel with only a partial dip.",
    "dumbbell-front-squat": "Front squat holding a dumbbell at each shoulder (or one at the chest) instead of a barbell.",
    "dumbbell-overhead-squat": "Squat with one or two dumbbells locked out overhead throughout the full range of motion — demands significant shoulder stability.",
    "dumbbell-goblet-squat": "Squat holding a single dumbbell vertically against the chest with both hands cupping the top end — an accessible, upright-torso squat variation.",
    "dumbbell-bench-press": "Bench press performed with a dumbbell in each hand instead of a barbell, allowing a greater range of motion and independent arm paths.",
    "dumbbell-floor-press": "Dumbbell bench press performed lying on the floor, stopping the descent when the upper arms touch the ground.",
    "dumbbell-deadlift": "Deadlift performed holding a dumbbell in each hand (or one between the feet) instead of a barbell.",
    "dumbbell-romanian-deadlift": "Romanian deadlift performed holding dumbbells at the sides instead of a barbell in front.",
    "dumbbell-burpee-deadlift": "A burpee performed with a pair of dumbbells on the floor — chest to the ground between the dumbbells, then standing up and deadlifting them before the next rep.",
    "dumbbell-walking-lunge": "Walking lunge holding a dumbbell in each hand (or one at the shoulder), alternating legs with each step.",
    "dumbbell-front-rack-lunge": "Lunge holding dumbbell(s) in the front rack at the shoulders rather than at the sides, adding a core/upper-back demand to the leg work.",
    "dumbbell-overhead-lunge": "Lunge with one or two dumbbells locked out overhead throughout — a stability-heavy single-leg movement.",
    "dumbbell-box-step-up": "Stepping up onto a box holding a dumbbell in each hand (or at the shoulders), driving through the lead leg to full hip extension at the top.",
    "dumbbell-row": "Single-arm dumbbell pulled from a hang to the hip/ribs, typically bracing on a bench or in a bent-over stance — targets the lat and mid-back.",
    "renegade-row": "From a push-up (plank) position with a hand on each dumbbell, rowing one dumbbell to the hip while balancing on the other — combines a core-stability plank with a rowing pull.",
    "devils-press": "A burpee with a dumbbell in each hand — chest to the floor beside the dumbbells, then standing and driving straight into a dumbbell snatch to overhead in one motion, both arms together.",
    "dumbbell-carry": "Carrying one or two dumbbells over a set distance, position (front rack, overhead, or at the sides) specified by the workout.",
    "dumbbell-waiters-walk": "Walking a set distance with a single dumbbell held overhead on a flat palm, arm fully locked out — a unilateral overhead-stability carry.",
    "dumbbell-overhead-carry": "Walking a set distance with one or two dumbbells locked out overhead, arms fully extended throughout.",
    "farmers-carry": "Walking a set distance holding a heavy dumbbell (or other implement) in each hand at the sides — a grip- and core-bracing loaded carry.",
    # kettlebell
    "kettlebell-swing": "A kettlebell hiked back between the legs and driven forward by the hips to about chest or eye height — a hip-hinge power movement, not a shoulder lift.",
    "american-kettlebell-swing": "Kettlebell swing driven all the way to an overhead lockout at the top of each rep, rather than stopping at chest height.",
    "russian-kettlebell-swing": "Kettlebell swing driven only to approximately chest/eye height, arms staying roughly parallel to the floor at the top.",
    "single-arm-kettlebell-swing": "Kettlebell swing performed with one arm, often switching hands mid-set — adds an anti-rotation core demand to the standard two-handed swing.",
    "kettlebell-clean": "Kettlebell pulled from between the legs (or the floor) and received in the front rack against the forearm, absorbing it softly to avoid banging the wrist.",
    "kettlebell-clean-and-jerk": "A kettlebell clean immediately followed by driving it overhead with a jerk-style dip and drive.",
    "kettlebell-snatch": "A single kettlebell pulled from between the legs to locked-out overhead in one continuous motion, the bell rolling smoothly around the wrist rather than banging into the forearm.",
    "kettlebell-thruster": "Front squat holding a kettlebell in the front rack (or goblet position), driven directly into an overhead press as the athlete stands.",
    "single-arm-kettlebell-thruster": "Kettlebell thruster performed holding the bell in one arm's front rack, adding an anti-rotation core demand.",
    "kettlebell-push-press": "Kettlebell pressed overhead using a short dip-and-drive from the legs rather than a strict press.",
    "kettlebell-press": "Kettlebell pressed from the shoulder/rack position to locked-out overhead using shoulder strength alone.",
    "kettlebell-deadlift": "Deadlift performed holding a kettlebell (often between the feet or held with both hands) instead of a barbell.",
    "kettlebell-sumo-deadlift-high-pull": "Kettlebell deadlifted from a sumo stance and pulled explosively upward to about chin height, elbows leading.",
    "goblet-squat": "Squat holding a single kettlebell (or dumbbell) vertically against the chest with both hands cupping the horns/top — an accessible, upright-torso squat.",
    "kettlebell-front-rack-lunge": "Lunge holding one or two kettlebells in the front rack against the shoulders.",
    "kettlebell-overhead-lunge": "Lunge with a kettlebell locked out overhead throughout — demands shoulder stability on top of the single-leg squat pattern.",
    "turkish-get-up": "A structured, multi-step transition from lying on the floor to standing tall, kettlebell held locked out overhead the entire time — a slow, technical full-body stability movement.",
    "kettlebell-windmill": "Standing with a kettlebell locked out overhead, hinging sideways at the hips to touch (or reach toward) the opposite foot while keeping the arm vertical — an overhead-stability and hip-mobility drill.",
    "kettlebell-halo": "Circling a kettlebell around the head, close to the skull, reversing direction each rep or set — a shoulder-mobility and control movement, not a strength lift.",
    "double-kettlebell-farmers-carry": "Walking a set distance holding a kettlebell in each hand at the sides.",
    "double-kettlebell-front-rack-carry": "Walking a set distance holding a kettlebell in each hand racked at the shoulders.",
    "double-kettlebell-front-rack-lunge": "Lunge holding a kettlebell in each hand racked at the shoulders, alternating legs.",
    "double-kettlebell-overhead-carry": "Walking a set distance with a kettlebell locked out overhead in each hand.",
    # gymnastics
    "pull-up": "Hanging from a bar with an overhand grip, pulling the chin over the bar and lowering back to a full hang — the baseline pulling bodyweight movement, strict or kipping depending on the workout.",
    "kipping-pull-up": "Pull-up using a rhythmic hip/leg swing (the 'kip') to generate momentum, getting the chin over the bar faster and with less pure pulling strength than a strict rep.",
    "butterfly-pull-up": "A continuous, circular kipping pull-up where the hips trace a loop rather than a front-to-back swing — the fastest competitive pull-up style once the timing is mastered.",
    "strict-pull-up": "Pull-up performed with no swing or leg drive — a dead-hang start, pulling the chin over the bar using upper-body strength alone.",
    "chest-to-bar-pull-up": "Pull-up (strict or kipping) where the chest, not just the chin, must reach the bar at the top of every rep — a longer range of motion than a standard pull-up.",
    "l-pull-up": "Strict pull-up performed with the legs held straight out in front at a 90-degree angle (an L-sit position) for the entire rep — adds a core-and-hip-flexor demand to the pull.",
    "weighted-pull-up": "Pull-up performed with additional external load (a vest, belt, or dumbbell between the feet) beyond bodyweight.",
    "burpee-pull-up": "A standard burpee immediately followed by one pull-up before the next rep begins.",
    "jumping-pull-up": "Pull-up assisted by a small jump off the ground to help the chin clear the bar — a scaled version of a full pull-up for athletes still building pulling strength.",
    "chin-up": "Pull-up performed with an underhand (supinated) grip rather than overhand — the biceps-forward grip variation.",
    "negative-pull-up": "Starting at the top of a pull-up (chin over the bar) and lowering as slowly as possible to a full hang — builds pulling strength by isolating the eccentric portion.",
    "muscle-up": "A pull-up that continues past the bar/rings into a dip lockout above them in one continuous motion — combines a pull and a press into a single rep.",
    "bar-muscle-up": "Muscle-up performed on a straight pull-up bar rather than gymnastics rings.",
    "ring-muscle-up": "Muscle-up performed on gymnastics rings, which allow the hands to rotate through the transition — generally considered more technical than the bar version.",
    "strict-muscle-up": "Muscle-up performed with no kip or swing — a strict pull straight into the transition and dip lockout.",
    "burpee-muscle-up": "A standard burpee immediately followed by one muscle-up before the next rep begins.",
    "burpee-bar-muscle-up": "A standard burpee immediately followed by one bar muscle-up before the next rep begins.",
    "handstand-push-up": "Inverted against a wall for balance, lowering the head to the floor (or a target) and pressing back to a locked-out handstand — the vertical pressing bodyweight movement.",
    "strict-handstand-push-up": "Handstand push-up performed with no kip from the legs — a straight, controlled press from the bottom position back to full lockout.",
    "kipping-handstand-push-up": "Handstand push-up using a kip (a hip/knee drive against the wall) to help press back up out of the bottom, similar in spirit to a kipping pull-up.",
    "deficit-handstand-push-up": "Handstand push-up with the hands elevated on parallettes or plates, increasing the range of motion by lowering the head below hand height.",
    "freestanding-handstand-push-up": "Handstand push-up performed balancing in the middle of the floor with no wall for support — demands full handstand balance in addition to the press.",
    "wall-facing-handstand-push-up": "Handstand push-up performed facing the wall (toes or hands close to it) rather than back to the wall — a stricter balance and lockout standard, often called a chest-to-wall HSPU.",
    "ring-handstand-push-up": "Handstand push-up performed with the hands on gymnastics rings instead of the floor, adding significant instability to the press.",
    "parallette-handstand-push-up": "Handstand push-up performed with hands on parallettes, adding a deficit and requiring wrist/shoulder stability on the narrow bars.",
    "handstand": "Balancing inverted on the hands, whether freestanding or against a wall, holding the body in a straight vertical line.",
    "handstand-hold": "Holding a handstand position for time, freestanding or wall-supported per the workout's standard.",
    "handstand-walk": "Walking on the hands while inverted in a handstand, covering a set distance.",
    "wall-climb": "Starting in a push-up position with feet against a wall, walking the feet up the wall while walking the hands in until the chest is close to the wall in a handstand — used to reach a handstand position from the ground.",
    "wall-climb-over": "Wall climb continued until the athlete is fully vertical and then transitions over the top of the wall/obstacle to the other side.",
    "ring-dip": "Dip performed supporting the body on gymnastics rings instead of parallel bars, adding significant stability demand as the rings want to swing and rotate.",
    "bar-dip": "Dip performed on parallel bars, lowering the shoulders below the elbows and pressing back to full lockout.",
    "strict-dip": "Dip performed with no kip or leg swing — a controlled lower and press using triceps/chest/shoulder strength alone.",
    "ring-row": "Body held at an angle underneath a set of rings (or a bar), pulling the chest to the rings and lowering back — a horizontal, scalable pulling movement.",
    "ring-push-up": "Push-up performed with hands on gymnastics rings instead of the floor, adding an instability demand to the standard push-up.",
    "push-up": "From a plank position, lowering the chest to the floor and pressing back to full arm extension — the baseline horizontal pressing bodyweight movement.",
    "hand-release-push-up": "Push-up where the hands lift completely off the floor at the bottom of each rep before pressing back up — ensures full chest-to-floor depth on every rep.",
    "toes-to-bar": "Hanging from a pull-up bar, bringing both feet up to touch the bar between the hands and lowering back to a hang — a kipping or strict core-and-grip movement.",
    "toes-to-ring": "Toes-to-bar performed hanging from gymnastics rings instead of a fixed bar.",
    "knees-to-elbows": "Hanging from a bar, bringing both knees up to touch the elbows and lowering back — a shorter-range regression of toes-to-bar.",
    "hanging-knee-raise": "Hanging from a bar, raising the knees toward the chest under control with little to no kip — an ab/hip-flexor strength movement.",
    "hanging-hip-touch": "Hanging from a bar or rings, raising the legs to touch the hips to the bar/rings — an advanced core movement between knees-to-elbows and toes-to-bar in difficulty.",
    "rope-climb": "Climbing a suspended rope hand-over-hand (with or without the feet/legs for assistance) to a marked height, then descending under control.",
    "legless-rope-climb": "Rope climb performed using the arms and grip alone, with no assistance from the legs or feet on the rope.",
    "pegboard": "Climbing a vertical board studded with holes by moving a pair of wooden pegs upward hand over hand, to a marked height and back down.",
    "pistol": "A single-leg squat to full depth with the non-working leg held straight out in front, then standing back up on the one leg — demands significant single-leg strength and balance.",
    "forward-roll": "A tucked forward somersault along the ground, rolling from the shoulders through to standing.",
    "ring-lower": "Lowering the body from a support or muscle-up position on the rings down to a hang (or through the dip) under control, isolating the eccentric portion of a ring movement.",
    "pull-over": "Starting in a support position on a bar, rotating the body up and over the bar in a continuous swing to return to support facing the other way.",
    "parallel-bar-traverse": "Moving hand-over-hand along a row of parallel bars while supporting the body weight on straight arms, without the feet touching the ground.",
    "obstacle-pirouette": "A rotational transition move over a raised obstacle or bar, pivoting the body around a single point of contact to clear it — a Games-specific obstacle-course skill.",
    "sit-up": "Lying on the back with knees bent and feet anchored, curling the torso up to touch the chest to the knees (or per the workout's standard) and lowering back down.",
    "ghd-sit-up": "Sit-up performed on a Glute-Ham Developer, hips anchored so the torso can hinge well past parallel behind the hips before curling all the way forward to touch the toes — a much larger range of motion than a floor sit-up.",
    "ab-mat-sit-up": "Sit-up performed with an Ab Mat under the lower back to allow a deeper hip extension at the bottom of each rep, feet anchored or held by a partner.",
    "v-up": "Lying flat, simultaneously raising the straight legs and straight torso to meet in a 'V' with hands touching the toes, then lowering back down.",
    "hollow-rock": "Holding a hollow body position (lower back pressed to the floor, arms and legs extended and slightly raised) while rocking gently front to back — a core-control and rhythm drill.",
    "hollow-hold": "Holding the hollow body position (lower back flat to the floor, shoulders and legs raised) motionless for time.",
    "l-sit": "Supporting the body on the hands (on the floor, a box, or rings) with the legs held straight out in front at a 90-degree angle, held for time.",
    "plank": "Holding the body in a straight line supported on the forearms (or hands) and toes, core braced, for time.",
    "back-extension": "On a GHD or hyperextension bench, hinging the torso down and raising it back up to extend the lower back and glutes.",
    "ghd-hip-extension": "Hip-focused variation of the back extension on a GHD, emphasizing glute drive to extend the hips rather than lower-back rounding/extension.",
    "hip-extension": "General term for extending the hips from a flexed position back to neutral/extended against resistance or bodyweight, as prescribed on a GHD or hyperextension bench.",
    # bodyweight
    "air-squat": "A bodyweight squat to at least hip-crease-below-knee depth and back to standing, with no external load — the foundational squat pattern everything else builds on.",
    "walking-lunge": "Stepping forward into a lunge, then bringing the back foot through to step into the next lunge, alternating legs while traveling forward.",
    "reverse-lunge": "Lunge stepping backward instead of forward, then returning to standing before the next rep.",
    "jumping-lunge": "Lunge where the athlete jumps to switch the front/back leg mid-air between reps, rather than stepping.",
    "overhead-walking-lunge": "Walking lunge performed with the arms locked out overhead throughout, adding a stability demand to the traveling lunge.",
    "cossack-squat": "A wide-stance side-to-side squat, shifting weight fully onto one bent leg while the other stays straight, then shifting to the other side.",
    "wall-sit": "Holding a seated squat position with the back against a wall and thighs parallel to the floor, no chair, for time.",
    "burpee": "From standing, dropping to the floor with the chest touching down, then pushing back up and jumping with a clap overhead — the classic full-body conditioning movement.",
    "bar-facing-burpee": "Burpee performed facing a barbell (or other low bar), jumping over it with both feet together after standing up from each rep.",
    "burpee-over-the-bar": "Burpee performed beside a barbell, jumping or stepping laterally over it after standing up from each rep.",
    "lateral-burpee": "Burpee where the jump/stand-up finishes with a lateral jump over a line or low object, changing sides each rep.",
    "burpee-box-jump": "Burpee immediately followed by jumping onto a box and standing to full hip extension at the top.",
    "burpee-box-jump-over": "Burpee immediately followed by jumping onto and completely over a box, landing on the other side.",
    "burpee-broad-jump": "Burpee immediately followed by a maximal-distance broad jump forward instead of a vertical jump.",
    "burpee-over-dumbbell": "Burpee performed straddling or beside a dumbbell, jumping over it after standing up from each rep.",
    "box-jump": "Jumping with both feet from the ground onto a raised box, standing to full hip extension at the top, then stepping or jumping back down.",
    "box-jump-over": "Jumping with both feet onto a box and immediately continuing over the top to land on the other side, rather than standing on top of it.",
    "box-step-up": "Stepping up onto a box one foot at a time (no jump), driving through the lead leg to full hip extension at the top.",
    "broad-jump": "A standing jump for maximum forward distance, taking off and landing on both feet.",
    "tuck-jump": "A vertical jump bringing both knees up toward the chest at the peak before landing.",
    "double-under": "Jump rope pass where the rope passes under the feet twice per single jump — a faster wrist-driven turn than a basic single jump.",
    "single-under": "A standard jump rope pass, one rotation of the rope per jump.",
    "triple-under": "Jump rope pass where the rope passes under the feet three times in a single jump — an advanced, very fast turn.",
    "crossover-single-under": "Single-under jump rope where the arms cross in front of the body as the rope passes underfoot.",
    "jumping-jack": "Jumping to spread the feet wide while raising the arms overhead, then jumping back to the start position — a basic warm-up/conditioning movement.",
    "bear-crawl": "Crawling forward on hands and feet with the knees hovering just off the ground, opposite hand and foot moving together.",
    "mountain-climber": "From a plank position, rapidly driving alternating knees toward the chest while the hands stay planted.",
    "high-knees": "Running in place (or traveling) driving the knees up toward hip height with each step, at a fast cadence.",
    "inchworm": "From standing, folding forward to place the hands on the floor, walking the hands out to a plank, then walking the feet up to the hands to return to standing.",
    "flutter-kick": "Lying on the back with legs extended and slightly raised, kicking the legs in a small, rapid alternating up-down motion.",
    # monostructural
    "run": "Running a prescribed distance, typically outdoors or on a track, at whatever pace the workout's format calls for.",
    "sprint": "Running a short distance at maximum effort/speed.",
    "run-backward": "Running a prescribed distance moving backward instead of forward.",
    "shuttle-sprint": "Sprinting to a marked line and back (or between two lines repeatedly) rather than a single straight-line distance.",
    "shuttle-run": "Running back and forth between two fixed points a set number of times, rather than a single straight-line distance.",
    "row": "Rowing a prescribed distance or calorie count on a rowing ergometer (Concept2 or similar).",
    "ski-erg": "A prescribed distance or calorie count on a SkiErg machine, mimicking a double-pole cross-country ski motion.",
    "bike": "Riding a prescribed distance or calorie count on a stationary bike.",
    "assault-bike": "A prescribed calorie count or distance on an air-resistance fan bike (Assault Bike/AirBike), which uses both arms and legs.",
    "echo-bike": "A prescribed calorie count or distance on an Echo Bike, a fan bike similar in use to an Assault Bike.",
    "bike-erg": "A prescribed distance or calorie count on a Concept2 BikeErg, a standard-geometry stationary bike ergometer.",
    "swim": "Swimming a prescribed distance in a pool or open water.",
    "kayak": "Paddling a kayak a prescribed distance.",
    "paddleboard": "Paddling a standup paddleboard a prescribed distance.",
    "stair-climb": "Climbing a prescribed number of stairs or flights, typically for time or as part of a larger workout.",
    # odd-object
    "wall-ball-shot": "Squatting with a medicine ball held at the chest, then standing and throwing it to hit a target on the wall at a marked height, catching it on the way down into the next squat.",
    "medicine-ball-clean": "A medicine ball pulled from the floor and received at the shoulder/chest in a partial squat, similar in spirit to a barbell clean but with a ball instead of a bar.",
    "medicine-ball-sit-up": "Sit-up performed holding a medicine ball at the chest (or throwing it to a partner at the top), adding load to the standard sit-up.",
    "medicine-ball-box-step-over": "Stepping up and completely over a box while holding a medicine ball at the chest, landing on the other side.",
    "ball-slam": "Raising a medicine ball overhead and slamming it forcefully into the ground, then picking it back up for the next rep.",
    "sandbag-carry": "Carrying a loaded sandbag a set distance, held however the workout specifies (bear hug, shoulder, or overhead).",
    "sandbag-clean": "A sandbag pulled from the floor and received at the shoulder or chest in one motion, similar to a barbell/dumbbell clean but with an unwieldy, shifting load.",
    "sandbag-ground-to-shoulder": "Any method of moving a sandbag from the floor to one shoulder — a clean, a lap-and-heave, or a squat-and-press, athlete's choice unless specified.",
    "sandbag-squat": "Squat holding a sandbag at the chest, on the back, or on the shoulders per the workout's prescription.",
    "sandbag-over-log": "Lifting a loaded sandbag up and over a log or barrier obstacle.",
    "jerry-bag-carry": "Carrying a loaded jerry-can-style bag (handles on the sides) a set distance, typically at the sides or chest.",
    "husafell-carry": "Carrying a Husafell stone (an odd-shaped, bear-hugged concrete/rubber implement) a set distance against the chest.",
    "log-carry": "Carrying a loaded wooden or synthetic log a set distance, typically bear-hugged against the chest.",
    "sledgehammer-strike": "Swinging a sledgehammer overhead to strike a tire or target, alternating sides — a rotational, explosive conditioning movement.",
    "medicine-ball-throw": "Throwing a medicine ball for maximum distance or height, or at a partner/target, per the workout's standard.",
    "stake-drive": "Driving a stake or post into the ground (or a tire) using an overhead sledgehammer-style strike, a Games-specific strongman-style movement.",
    "sled-push": "Pushing a loaded sled across a set distance, driving through the legs with arms extended and braced against the sled's handles.",
    "sled-pull": "Pulling a loaded sled a set distance, either walking backward facing it or via a rope while facing away.",
    "yoke-carry": "Walking a set distance under a loaded yoke frame resting across the upper back/shoulders — a heavy, stability-demanding loaded carry.",
    "atlas-stone-over-shoulder": "Lifting a round, weighted atlas stone from the ground and placing it over one shoulder in a single motion.",
    "d-ball-clean": "A D-ball (a round, textured medicine-ball-style implement) pulled from the floor and received at the chest/shoulder, similar to a sandbag or medicine-ball clean.",
    "d-ball-over-shoulder": "Lifting a D-ball from the ground and placing it over one shoulder in a single motion.",
    "tire-flip": "Flipping a large tractor tire end over end by squatting to grip its underside and driving it up and over with the hips and legs.",
    "log-clean-and-jerk": "A loaded log pulled from the floor to the chest/shoulders and then driven overhead to a lockout, similar in structure to a barbell clean-and-jerk but with an axle-style implement.",
    "log-press": "Pressing a loaded log from the shoulders/chest to locked-out overhead, typically without a squat clean to get it there first.",
    "plate-ground-to-overhead": "Moving a weight plate from the floor to locked-out overhead by any method the athlete chooses.",
    "plate-carry": "Carrying one or two weight plates a set distance, typically pinched at the sides or held at the chest.",
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

    missing_patterns = set(category) - set(PATTERNS)
    if missing_patterns:
        raise SystemExit(
            "movements missing from PATTERNS: " + ", ".join(sorted(missing_patterns))
        )

    movements = [{
        "id": slug,
        "name": title(slug),
        "category": cat,
        "equipment": EQUIPMENT[cat],
        "patterns": PATTERNS[slug],
        "aliases": ALIASES.get(slug, []),
        "workouts": workouts.get(slug, []),
        "description": DESCRIPTIONS.get(slug),
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
