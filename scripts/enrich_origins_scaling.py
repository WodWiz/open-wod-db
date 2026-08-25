#!/usr/bin/env python3
"""Fill origin.summary and scaling for entries where we have defensible content.

Three tiers, deliberately different in depth:

1. The Girls (all 33): hand-written origin summaries + scaled/beginner guidance.
   Scaling reflects long-established, widely-taught conventions for these
   benchmarks, not invented prescriptions.
2. Heroes (a curated subset): the honoree's story, written only where the facts
   are certain from the official CrossFit.com hero-workout postings. Heroes not
   in the dict are left untouched rather than risk an error about a real
   person. Scaling only for the most widely programmed ones.
3. Open / Quarterfinals / Games (all): short, formula-derived origin lines —
   the year and competition stage are encoded in the id, so these are factual
   by construction. No scaling (official scaled divisions varied per year and
   we don't restate what we can't verify per-workout).

Idempotent: re-running overwrites exactly these fields and nothing else.
Existing origin.first_posted values are preserved and appended to the summary
where present. Run scripts/validate.py and scripts/build_index.py after.
"""
import glob
import json
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
TODAY = "2026-08-25"

SERIES_BLURB = (
    "Part of CrossFit's original 'Girls' benchmark series — named workouts "
    "introduced by founder Greg Glassman starting in 2003, on the logic that "
    "anything that leaves you flat on your back deserves a name like a storm. "
    "They serve as repeatable fitness tests: revisit one every few months and "
    "the clock tells you whether you're fitter."
)

GIRL_ORIGINS = {
    "fran": "The most famous workout in CrossFit. Its blend of two simple movements at a load light enough to keep moving — but heavy enough to punish — made it the sport's universal handshake: 'What's your Fran time?' remains the question CrossFitters ask each other first. Elite athletes finish under 2 minutes; sub-5 is a widely used marker of solid fitness.",
    "grace": "Thirty clean and jerks for time — nothing to hide behind. Grace is the classic test of barbell cycling under fatigue, and a rite of passage at 135/95: the load is manageable for one rep, and the workout asks whether it's manageable for thirty. Often programmed alongside Isabel, its snatch twin.",
    "isabel": "Grace's twin: the same thirty reps and the same barbell, but snatched instead of clean-and-jerked. Technique degrades faster overhead, which is exactly the test — elite athletes finish in under 2 minutes, but only with a snatch that survives a red-lined heart rate.",
    "helen": "Three rounds pairing a run with kettlebell swings and pull-ups — the archetypal light triplet. The run keeps the heart rate high enough that the 'easy' gymnastics and kettlebell work stop being easy. A benchmark for pacing discipline: the athletes with the best times are rarely the ones who sprint the first 400m.",
    "cindy": "The most accessible of the Girls: twenty minutes of bodyweight triplet work with no barbell and no skill barrier beyond a pull-up. Deceptive — 20 rounds (a long-standing 'good' score) is 100 pull-ups, 200 push-ups, and 300 squats. The push-ups are almost always what breaks first.",
    "chelsea": "Cindy's stricter sibling: the same 5-10-15 triplet, but on the minute for thirty minutes. Miss a minute and the workout is traditionally over — which turns a simple bodyweight circuit into a test of sustained precision. Completing all 30 rounds means the same volume as a very good Cindy, on someone else's schedule.",
    "angie": "One hundred pull-ups, then a hundred push-ups, then a hundred sit-ups, then a hundred squats — completed in order, each movement finished before the next begins. The format is brutal in its simplicity: no rotating away from a failing muscle group. How you break up the first two hundred reps decides the workout.",
    "barbara": "Five rounds of a descending-skill bodyweight ladder with exactly three minutes of rest between rounds. The rest is what defines Barbara: scores count work time only, so every round is an all-out effort into a recovery that never feels long enough by round four.",
    "diane": "Deadlifts at 225/155 paired with handstand push-ups in the classic 21-15-9. The pairing is the point: a heavy hinge that pools blood in the posterior chain, followed immediately by going upside down. Sub-3 elite times depend almost entirely on unbroken handstand push-ups.",
    "elizabeth": "Squat cleans at 135/95 against ring dips in a 21-15-9. Both movements reward efficiency and punish the shoulders — by the round of 9, the ring dips are the workout for most athletes. Commonly seen with power cleans as a slightly easier variant, but the original calls for full squat cleans.",
    "annie": "The gentlest-looking Girl: double-unders and sit-ups, 50-40-30-20-10. For athletes with double-unders it's a sprint and a welcome deload; for athletes without them it's the workout that finally forces the skill. A favorite re-test for tracking double-under progress.",
    "karen": "One movement, one number: 150 wall-ball shots for time. No complexity, no strategy beyond break-up scheme and mental tolerance. Karen is the purest example of CrossFit's 'simple, not easy' — everyone understands it immediately and nobody enjoys the back half.",
    "jackie": "A 1,000-meter row into fifty 45-pound thrusters into thirty pull-ups — light, fast, and unforgiving of a hot start on the rower. The empty-bar thrusters are where Jackie is won or lost: they look trivial on paper and feel very different after a hard row.",
    "kelly": "Five rounds of a 400m run, thirty box jumps, and thirty wall-balls — one of the longer Girls, a half-hour grind for most athletes. Nothing is heavy; the test is staying in continuous motion when every movement taxes the legs the previous one just used.",
    "nancy": "Five rounds of a 400m run and fifteen overhead squats at 95/65. The overhead squat is light — the workout is whether your overhead position survives arriving at the bar with a running heart rate, five times.",
    "eva": "One of the heaviest-volume Girls: five rounds of an 800m run, thirty two-pood kettlebell swings, and thirty pull-ups. A long, punishing test usually reserved for experienced athletes — the total is 2.5 miles of running, 150 heavy swings, and 150 pull-ups.",
    "linda": "Known as 'the Three Bars of Death': a 10-to-1 descending ladder of deadlifts at 1.5× bodyweight, bench presses at bodyweight, and cleans at 0.75× bodyweight. Unique among the Girls in scaling to the athlete by definition — the loads are set by what you weigh, and the logistics (three loaded barbells) make it a special-occasion workout.",
    "lynne": "Five rounds of max-rep bodyweight bench press and max-rep pull-ups, with no clock at all. One of only a few untimed benchmarks: the score is total reps, and the strategy question — how close to failure to push each set — has no clean answer.",
    "mary": "The advanced sibling of Cindy: the same 20-minute AMRAP format, but with handstand push-ups, one-legged squats, and pull-ups. Where Cindy tests engine, Mary gates the engine behind skill — pistols and handstand push-ups have to be automatic before the workout is about conditioning at all.",
    "nicole": "Twenty minutes of 400m runs, each followed by a max set of pull-ups — the round ends when you drop off the bar. The score is total pull-ups, which makes it an unusual strategic puzzle: shorter sets mean more running, bigger sets mean earlier grip failure.",
    "amanda": "Nine, seven, and five reps of muscle-ups and squat snatches at 135/95 — one of the most skill-dense benchmarks in the canon. It carries real history: it debuted at the 2010 CrossFit Games in tribute to Amanda Miller, a 2009 Games competitor who died of melanoma earlier in 2010, and it has been a Games-level test ever since.",
    "gwen": "Clean and jerks at 15-12-9 — but unbroken, with the load self-selected and the score being the weight, not the time. Dropping the bar mid-set ends the attempt. Gwen inverts the usual benchmark logic: instead of racing a clock at a fixed load, you're betting on how heavy you can go without letting go.",
    "hope": "Fight Gone Bad's format applied to new movements: three rounds of five one-minute stations — burpees, power snatches, box jumps, thrusters, and chest-to-bar pull-ups — with a minute of rest between rounds, scored in total reps. Originally created for the 'Hope for Kenya' fundraiser campaign on CrossFit.com.",
    "barbara-ann": "A latter-day heavier variation on Barbara from CrossFit.com's expansion of the Girls series: the same five-round, rest-defined structure, with the bodyweight movements traded for weighted work that changes what the three minutes of rest can actually recover.",
    "andi": "One of the newer Girls from CrossFit.com's expansion of the series — a high-volume single-couplet grind in the mold of the originals, built to be understood in one reading and remembered by lunchtime.",
    "candy": "One of the expanded Girls series: five rounds of pull-ups, push-ups, and squats at volumes that make Cindy look polite. The structure is classic early-CrossFit bodyweight attrition — no skill gate, no equipment, nowhere to hide.",
    "ellen": "A newer addition to the Girls canon: a triplet mixing burpees with dumbbell work, in the modern CrossFit.com style that folds dumbbells into the classic benchmark format.",
    "grettel": "One of the newer Girls: a fast barbell couplet in the Fran mold — few reps, quick rounds, and a load that stays light only if your technique holds under a redlined heart rate.",
    "ingrid": "A newer Girl built on the snatch and burpee — technical barbell work paired with the sport's most democratic conditioning movement, in the classic short-couplet format.",
    "lane": "One of the newer Girls: alternating barbell and gymnastics work in a descending-then-ascending scheme that keeps neither the arms nor the lungs fully in charge.",
    "lyla": "A newer addition to the Girls series pairing barbell cycling with rope climbs — a combination of grip-heavy skill work and load that the original Girls never used, reflecting how the movement pool has grown since 2003.",
    "maggie": "Five rounds of handstand push-ups, one-legged squats, and pull-ups — Mary's structure stretched into fixed rounds at higher volume. A skill-gated grinder: 100 handstand push-ups and 300 pistols total put it firmly in advanced territory.",
    "marguerita": "Fifty rounds of a five-movement bodyweight sequence done one rep at a time — burpee, push-up, jumping-jack, sit-up, handstand. Less a strength test than a coordination flywheel: the transitions are the workout.",
}

GIRL_SCALING = {
    "fran": {
        "scaled": "65/45 lb thrusters; jumping pull-ups or a band. Keep the reps at 21-15-9 — the scheme is the workout. Target: finish under 10 minutes with no set lasting less than 5 reps.",
        "beginner": "Empty-bar or light-dumbbell thrusters; ring rows. Cut the scheme to 15-12-9. The goal is continuous movement and a first benchmark time to beat, not survival.",
    },
    "grace": {
        "scaled": "95/65 lb — a load you could cycle in steady singles or small touch-and-go sets without form breaking. Cap the effort around 6 minutes.",
        "beginner": "45-35 lb bar or light dumbbells, 20-30 reps, treating every rep as a deliberate ground-to-overhead. Learn the hang power clean and push press pattern first.",
    },
    "isabel": {
        "scaled": "95/65 lb power snatches, singles from the floor. The snatch degrades fastest under fatigue of any lift — scale until 30 crisp reps is realistic.",
        "beginner": "Empty bar or light dumbbell, 20-30 reps, as technique practice under a gentle clock. A PVC-to-empty-bar progression session beats a sloppy timed effort.",
    },
    "helen": {
        "scaled": "35/26 lb kettlebell; banded or jumping pull-ups. Keep the runs — they are the engine test. Target under 15 minutes.",
        "beginner": "200-300m runs or a 500m row substitute, 26/18 lb Russian swings, ring rows. Three even-paced rounds beat two fast ones and a walk.",
    },
    "cindy": {
        "scaled": "Banded pull-ups, knee or box push-ups if straight sets of 10 break early. The target is steady rounds every 60-75 seconds for all 20 minutes.",
        "beginner": "Ring rows, elevated push-ups, squats to a target box; 12-15 minutes. Log the rounds — Cindy is the easiest benchmark to re-test progress on.",
    },
    "chelsea": {
        "scaled": "Banded pull-ups and knee push-ups, holding the every-minute-on-the-minute structure. If a minute is missed, keep going Cindy-style and note the round.",
        "beginner": "3 ring rows, 6 elevated push-ups, 9 squats per minute for 15-20 minutes — the EMOM structure teaches pacing better than any open AMRAP.",
    },
    "angie": {
        "scaled": "50 reps per movement, or bands for the pull-ups. Keep the do-all-of-one-before-the-next order — rotating movements defeats the test.",
        "beginner": "25-50 ring rows, elevated push-ups, sit-ups, and box squats. Break into small planned sets from rep one; nobody's arms survive improvisation.",
    },
    "barbara": {
        "scaled": "Banded pull-ups, knee push-ups, 3-4 rounds. Guard the 3-minute rests — compressing them turns a repeat-sprint test into a grind and ruins the comparison.",
        "beginner": "3 rounds of 10 ring rows, 15 elevated push-ups, 20 sit-ups, 25 squats with the full rest. The structure teaches recovering on purpose.",
    },
    "diane": {
        "scaled": "155/105 lb deadlifts; pike push-ups on a box or dumbbell strict presses in place of handstand push-ups. Abmat-and-band HSPU only for athletes with an established inversion base.",
        "beginner": "95/65 lb deadlifts with a coach's eye on the set-up, seated dumbbell presses, 15-12-9 or 12-9-6. The hinge pattern is the priority; upside-down can wait.",
    },
    "elizabeth": {
        "scaled": "95/65 lb power cleans; banded ring dips or box dips. The round of 9 dips is where the workout lives — scale so it's hard, not impossible.",
        "beginner": "Light hang power cleans (bar or dumbbells) and bench or box dips, 15-12-9. Full squat cleans come after the power version is automatic.",
    },
    "annie": {
        "scaled": "Half the double-unders (25-20-15-10-5) with full sit-ups, or 2x singles. If you're 'almost' at double-unders, this is the workout to attempt them in.",
        "beginner": "Single-unders at the written scheme, or 30-20-10. Sit-ups unmodified. A perfect first benchmark: low load, low skill floor, obvious progress marker.",
    },
    "karen": {
        "scaled": "14/10 lb ball or a reduced target height, planned sets of 10-15 with short rests from the start. 150 improvised reps always ends in long stares at the ball.",
        "beginner": "75-100 reps with a light ball, or 150 goblet-squat-to-press reps. The squat depth and hip drive matter more than the target on day one.",
    },
    "jackie": {
        "scaled": "The row stays; 35/25 lb bar or PVC-plus for thrusters, banded pull-ups. The classic error is rowing 15 seconds too hard — scale the pacing, not just the load.",
        "beginner": "500-750m row, 25-35 empty-bar or dumbbell thrusters, 15-20 ring rows. One continuous effort at conversational-plus pace.",
    },
    "kelly": {
        "scaled": "20\" box (step-ups allowed), 14/10 lb ball, 3-4 rounds. This is a 25-35 minute workout even scaled — start slower than feels right.",
        "beginner": "3 rounds: 200m run, 15 box step-ups, 15 light wall-balls. Volume is the hazard here, not load — cut rounds before cutting movements.",
    },
    "nancy": {
        "scaled": "65/45 lb overhead squats, or front squats if overhead mobility isn't there yet. Keep all five runs.",
        "beginner": "PVC or empty-bar overhead squats (or goblet squats), 200m runs, 3-4 rounds. Nancy is secretly a mobility screen — treat a failed overhead position as information, not failure.",
    },
    "eva": {
        "scaled": "53/35 lb kettlebell, banded pull-ups, 3-4 rounds. Even elite athletes take 30+ minutes on Eva — respect the total volume when choosing.",
        "beginner": "Not a beginner workout. Substitute 3 rounds of a 400m run, 15 Russian swings, and 15 ring rows, and build toward it over months.",
    },
    "linda": {
        "scaled": "1× bodyweight deadlift, 0.75× bench, 0.5× clean — or run the ladder from 8. The bodyweight-multiplier design means 'scaled Linda' is still honestly Linda.",
        "beginner": "A 5-to-1 ladder at light fixed loads with a coach nearby. Three barbells and descending reps make this a logistics lesson as much as a workout.",
    },
    "lynne": {
        "scaled": "Dumbbell bench at a load allowing 8-15 reps per set; banded pull-ups or ring rows. Score total reps — the no-clock format already scales itself.",
        "beginner": "5 rounds of max push-ups and max ring rows. Same strategic puzzle (how close to failure per set?), no barbell required.",
    },
    "mary": {
        "scaled": "Pike push-ups on a box, pistols to a box or with a heel counterweight, banded pull-ups. If two of the three movements need scaling, do Cindy instead and log it as Cindy.",
        "beginner": "Do Cindy. Mary is Cindy for athletes whose pistols and handstand push-ups are already automatic — there's no shame and no shortcut in that order.",
    },
    "nicole": {
        "scaled": "Banded pull-ups or a fixed set of 5-10 ring rows per round; keep the max-set scoring if using bands. Runs stay 400m.",
        "beginner": "200-300m runs with max-rep ring rows. The run-recover-hang rhythm is the point — any pulling movement preserves it.",
    },
    "amanda": {
        "scaled": "Ring or bar muscle-up transitions/jumping muscle-ups, 95/65 lb squat snatches. If muscle-ups are close but not there, 9-7-5 of 2× pull-ups + 2× dips keeps the intent.",
        "beginner": "9-7-5 of ring rows + push-ups and overhead squats with an empty bar. Amanda unmodified is a Games-level test — the scaled version is what makes it trainable.",
    },
    "gwen": {
        "scaled": "The format self-scales — choose a load with 3-4 clean and jerks in reserve on the first set of 15. Newer athletes err heavy here; the 12 and 9 arrive fast.",
        "beginner": "15-12-9 with an empty bar or light dumbbells, resting as needed but practicing the no-drop discipline of the last few reps of each set.",
    },
    "hope": {
        "scaled": "Lighter snatch (45-65/35-45 lb), regular pull-ups or jumping pull-ups, lower box. Rotate stations even when a minute goes badly — the score absorbs it.",
        "beginner": "Same station format with squats in place of snatches and ring rows in place of pull-ups. Fight Gone Bad's format is the friendliest scoring in CrossFit for a first-timer: every rep counts.",
    },
    "barbara-ann": {
        "scaled": "Reduce loads to what allows unbroken sets of 10+ in round one, and cut to 3-4 rounds before touching the 3-minute rests.",
        "beginner": "Do Barbara scaled instead, and come back to the weighted variant with a strength base.",
    },
    "andi": {
        "scaled": "Cut the total volume by a third and choose loads that keep sets of 10+ alive in the opening rounds.",
        "beginner": "Halve the volume with light implements; long single-couplet grinds teach pacing fastest when the load is nearly trivial.",
    },
    "candy": {
        "scaled": "Banded pull-ups, knee push-ups, 3 rounds. The volume dwarfs Cindy's — plan set sizes before the clock starts.",
        "beginner": "3 rounds of 10 ring rows, 20 elevated push-ups, 30 squats. Build to the full five rounds over weeks.",
    },
    "ellen": {
        "scaled": "Lighter dumbbells and steady burpee pacing — pick a burpee cadence in round one you can still hold in the final round.",
        "beginner": "Cut the round count, keep the triplet structure, and use the lightest dumbbells in the gym without embarrassment.",
    },
    "grettel": {
        "scaled": "Drop the barbell load until the intended round rhythm survives — short couplets only test what they're meant to when the bar keeps moving.",
        "beginner": "Empty bar or dumbbells with halved reps, treating it as barbell-cycling practice under a light clock.",
    },
    "ingrid": {
        "scaled": "Power snatches at a weight allowing touch-and-go triples when fresh; step-down burpee pacing from the start.",
        "beginner": "Dumbbell snatches and a fixed easy burpee cadence — the snatch-plus-burpee combination is about breathing rhythm, learnable at any load.",
    },
    "lane": {
        "scaled": "Reduce the barbell to a weight that never demands more than two breaks per set, and substitute the gymnastics progressions you'd use in Fran or Diane.",
        "beginner": "Halve the scheme with an empty bar and ring rows — descending-ascending ladders teach set management better than straight sets.",
    },
    "lyla": {
        "scaled": "Lay-back rope pulls from the floor or towel pull-ups for the climbs; a barbell load that cycles in sets of 5+.",
        "beginner": "Ring rows and light barbell cycling. Save actual rope climbs for a skill session — grip fails suddenly, not gradually.",
    },
    "maggie": {
        "scaled": "Pike push-ups, pistols to a box, banded pull-ups, 3 rounds. Same rule as Mary: if most movements need scaling, the workout is telling you to do Cindy.",
        "beginner": "Do Cindy or scaled Mary first. Maggie is volume stacked on top of skill — earn the skill at lower volume.",
    },
    "marguerita": {
        "scaled": "25-35 rounds, kick-to-handstand against a wall or an inchworm in place of the handstand.",
        "beginner": "20-25 rounds substituting a plank shoulder-tap pair for the handstand. The single-rep carousel format is pure practice — use it as exactly that.",
    },
}

HERO_ORIGINS = {
    "murph": "Honors Navy Lieutenant Michael P. Murphy, 29, of Patchogue, New York, killed in Afghanistan on June 28, 2005, during Operation Red Wings, and posthumously awarded the Medal of Honor. This workout was one of Mike's favorites — he called it 'Body Armor.' Traditionally performed with a 20/14 lb vest, it has become CrossFit's Memorial Day tradition, completed by hundreds of thousands of athletes worldwide each year.",
    "jt": "Honors Petty Officer 1st Class Jeff Taylor, 30, of Little Creek, Virginia, a Navy SEAL killed in Afghanistan on June 28, 2005, when the MH-47 helicopter carrying a quick-reaction force to support Operation Red Wings was shot down. Posted in 2005, JT was the first Hero workout on CrossFit.com — three pressing movements and no legs to hide behind.",
    "michael": "Honors Navy Lieutenant Michael M. McGreevy Jr., 30, of Portville, New York, a SEAL killed in Afghanistan on June 28, 2005, in the same helicopter shoot-down during Operation Red Wings that took the men honored by JT and Murph. Three rounds of running, back extensions, and sit-ups — deceptively simple, brutally repeatable trunk endurance.",
    "daniel": "Honors Army Sergeant First Class Daniel Crabtree of the Ohio National Guard's Special Forces, killed in Al Kut, Iraq, on June 8, 2006. A symmetric chipper — pull-ups and sprints bracketing a hundred thrusters — posted among the earliest Hero workouts.",
    "josh": "Honors Army Staff Sergeant Joshua Hager, 29, killed in Ramadi, Iraq, on February 22, 2007, by an improvised explosive device. Overhead squats and pull-ups in a descending-ascending ladder — one of the shorter Heroes, and no gentler for it.",
    "jason": "Honors Navy Special Warfare Operator 1st Class Jason Dale Lewis, 30, a SEAL killed in Baghdad, Iraq, on July 6, 2007. Ascending squats against descending muscle-ups — a format that front-loads the hardest gymnastics while the athlete is freshest, then takes the legs anyway.",
    "badger": "Honors Navy Chief Petty Officer Mark Carter, 27, of Fallbrook, California, a SEAL killed in Iraq on December 11, 2007. Three rounds of squat cleans, pull-ups, and 800m runs — among the most feared of the early Heroes for its combination of load, volume, and distance.",
    "nate": "Honors Navy Chief Special Warfare Operator Nate Hardy, killed in Iraq on February 4, 2008, alongside Chief Michael Koch (honored by a separate workout). A 20-minute AMRAP of muscle-ups, handstand push-ups, and heavy swings — skill-dense and honest about it.",
    "randy": "Honors Los Angeles Police Department SWAT Officer Randy Simmons, 51, killed in the line of duty on February 7, 2008 — the first LAPD SWAT officer to die in the unit's history. Seventy-five power snatches at 75 lb: light, fast, and a masterclass in how a 'light' barbell stops being light.",
    "tommy-v": "Honors Navy Senior Chief Petty Officer Thomas Valentine, 37, of Ham Lake, Minnesota, a SEAL who died in a training accident in Arizona on February 13, 2008. Thrusters and rope climbs — grip against legs, with neither getting a turn off.",
    "griff": "Honors Air Force Staff Sergeant Travis Griffin, 28, killed on April 3, 2008, in Baghdad by an improvised explosive device while on his second tour. Uniquely in the canon, half of Griff's running is done backward — a nod that the workout should be as unusual as the man was.",
    "ryan": "Honors Maplewood, Missouri, firefighter Ryan Hummert, 22, killed by sniper fire on July 21, 2008, while responding to his first call as a firefighter. Muscle-ups and burpees, five rounds — short on movements, long on suffering.",
    "erin": "Honors Canadian Army Master Corporal Erin Doyle, 32, killed in a firefight in the Panjwaii District of Afghanistan on August 11, 2008. Dumbbell split cleans and pull-ups — one of the few Heroes built on a dumbbell staple.",
    "mr-joshua": "Honors Navy Special Warfare Operator 1st Class Joshua Thomas Harris, 36, a SEAL who drowned during combat operations on August 30, 2008. Runs, GHD sit-ups, and heavy deadlifts — midline endurance stacked against a heavy hinge, five times.",
    "danny": "Honors Oakland Police Sergeant Daniel Sakai, 35, killed in the line of duty on March 21, 2009, alongside three fellow officers. A 20-minute AMRAP of box jumps, push presses, and pull-ups — Fight Gone Bad's engine in Hero clothing.",
    "hansen": "Honors Marine Staff Sergeant Daniel Hansen, killed in Farah Province, Afghanistan, on February 14, 2009, by an improvised explosive device. Five rounds of heavy swings, burpees, and GHD sit-ups — a midline crucible.",
    "mcghee": "Honors Army Corporal Ryan C. McGhee, 21, killed in action on May 13, 2009, in central Iraq during his fourth deployment, serving with the 3rd Battalion, 75th Ranger Regiment. A 30-minute AMRAP of heavy deadlifts, push-ups, and box jumps — long, heavy, and relentless.",
    "tyler": "Honors Army First Lieutenant Tyler E. Parten, 24, killed in Afghanistan's Konar Province on September 10, 2009. Five rounds of muscle-ups and heavy sumo deadlift high pulls — an upper-body attrition test.",
    "lumberjack-20": "Honors the thirteen killed and thirty wounded at Fort Hood, Texas, on November 5, 2009 — many of them members of the 20th Engineer Battalion. Every couplet is separated by a 400m run: twenty reps, run, repeat, until six movements are gone.",
    "wittman": "Honors Army Sergeant Jeremiah Wittman, 26, of Darby, Montana, killed in Zhari Province, Afghanistan, on February 13, 2010. Seven rounds of kettlebell swings, power cleans, and box jumps — a straightforward, grinding triplet.",
    "adambrown": "Honors Navy Chief Special Warfare Operator Adam Brown, 36, a SEAL killed in Afghanistan on March 17, 2010. Adam's story — documented in the book 'Fearless' — of overcoming addiction to become a decorated SEAL made this two-round heavy chipper one of the most retold Hero tributes.",
    "dt": "Honors Air Force Staff Sergeant Timothy P. Davis, 28, killed on February 20, 2009, in Afghanistan when his vehicle was struck by an improvised explosive device. Five rounds of deadlifts, hang power cleans, and push jerks at 155/105 — DT has become a competition classic, a pure test of barbell cycling and grip management.",
    "small": "Honors Army Staff Sergeant Marc Small, 29, of Collegeville, Pennsylvania, killed in Faryab Province, Afghanistan, on February 12, 2009. Three rounds of rowing, burpees, and running — Big's sibling workout, all engine, no barbell.",
    "holleyman": "Honors Army Special Forces Sergeant First Class Aaron N. Holleyman, 27, killed in Khutayiah, Iraq, on August 30, 2004, when his vehicle struck an improvised explosive device. Thirty rounds of five wall-balls, three handstand push-ups, and one heavy power clean — a metronome of a workout.",
    "zembiec": "Honors Marine Major Douglas A. Zembiec, 34, the 'Lion of Fallujah,' killed in Baghdad on May 11, 2007, during his fourth deployment. Five rounds pairing heavy back squats with strict burpee pull-ups and running — strength, gymnastics, and engine with nothing optional.",
    "glen": "Honors Glen Doherty, 42, a former Navy SEAL working as a security contractor, killed in Benghazi, Libya, on September 11, 2012, alongside Tyrone Woods (honored by a separate workout). A long chipper — clean and jerks, running, rope climbs, and more running — matching the scale of the story it carries.",
    "chad1000x": "Honors Navy SEAL Chad Wilkinson, who died by suicide on October 29, 2018, after multiple deployments and traumatic brain injuries. One thousand box step-ups with a 45-lb ruck, created by his wife Sara to raise awareness of veteran suicide — completed by thousands each Veterans Day as the CHAD1000X event.",
    "the-seven": "Honors seven CIA officers killed on December 30, 2009, when a suicide bomber attacked Forward Operating Base Chapman in Khost, Afghanistan. Seven rounds of seven reps of seven movements — the arithmetic is the memorial.",
    "loredo": "Honors Army Staff Sergeant Edwardo Loredo, 34, killed in Jelewar, Afghanistan, on June 24, 2010, by an improvised explosive device. Six rounds of squats, push-ups, walking lunges, and running — no equipment, no ceiling on effort.",
    "whitten": "Honors Army Captain Dan Whitten, 28, killed in Zabul Province, Afghanistan, on February 2, 2010, by an improvised explosive device. Five rounds through kettlebell swings, box jumps, running, burpees, and wall-balls — a long five-station engine test.",
    "manion": "Honors Marine First Lieutenant Travis Manion, 26, killed in Al Anbar Province, Iraq, on April 29, 2007, by sniper fire while aiding wounded comrades. Seven rounds of 400m runs and heavy back squats — 'If not me, then who...' became the motto of the foundation bearing his name.",
    "garrett": "Honors Marine Captain Garrett 'Tubes' Lawton, 31, killed by an improvised explosive device in Herat Province, Afghanistan, on August 4, 2008. Three rounds of high-volume squats, ring handstand push-ups, and L-pull-ups — gymnastics density few Heroes match.",
    "riley": "Honors Army Sergeant First Class Riley Stephens, 39, killed in Afghanistan on September 28, 2012. A running-and-lunging sandwich — 1.5 miles, 150 burpees, 1.5 miles — traditionally worn with a 20-lb vest.",
    "gator": "Honors Army Sergeant Dale 'Gator' Wayrynen, 26, killed in Afghanistan on May 29, 2007 (as posted with the original CrossFit.com tribute). Eight rounds of front squats and ring dips — a leg-and-press couplet with no run to breathe on.",
    "coe": "Honors Army Sergeant Keith Adam Coe, 30, killed in Khalis, Iraq, on April 27, 2010, by an explosive device. Ten rounds of thrusters and ring push-ups — pressing volume stacked past what feels reasonable, on purpose.",
}

HERO_SCALING = {
    "murph": {
        "scaled": "No vest; partition the middle as 20 rounds of 5 pull-ups, 10 push-ups, 15 squats (Cindy-style); band the pull-ups if needed. Keep both mile runs if at all possible — they are the memorial's bookends.",
        "beginner": "Half Murph: 800m runs bracketing 50 pull-ups (ring rows), 100 push-ups (elevated), 150 squats, partitioned. Build to the full distance across a season, not a morning.",
    },
    "dt": {
        "scaled": "115/75 lb — the round rhythm (fast singles on deadlifts, unbroken hang cleans, jerks in one or two sets) is what to preserve. Grip management is the entire workout.",
        "beginner": "65-75/45-55 lb with 3-4 rounds, or 12-9-6 per round. Learn the hang power clean's hook grip release before adding load — DT eats grip mistakes.",
    },
    "jt": {
        "scaled": "Pike push-ups off a box for HSPU, banded ring dips, regular push-ups if needed. Three pressing movements means shoulders go fast — break sets before failure, from the first round.",
        "beginner": "15-12-9 of seated dumbbell press, bench dips, and elevated push-ups. Pressing endurance builds slowly; volume across weeks beats heroics on day one.",
    },
    "michael": {
        "scaled": "Reduce runs to 600m or back extensions to 35 supermans on the floor; sit-ups unmodified. The test is repeatability across three identical rounds.",
        "beginner": "3 rounds: 400m run or 500m row, 25 supermans, 25 sit-ups. The posterior-chain endurance this builds transfers to every deadlift you'll ever do.",
    },
    "randy": {
        "scaled": "55/35 lb keeping sets of 10+, or 50 reps at 75/55. When form degrades to a stiff-legged pull, the load is wrong regardless of what the clock says.",
        "beginner": "50 dumbbell snatches (alternating arms) at a light weight. The power snatch pattern first, the volume later.",
    },
    "badger": {
        "scaled": "95/65 lb squat cleans, banded pull-ups, 600m runs. This is a long workout at any scale — expect 30+ minutes and pace round one like round three.",
        "beginner": "3 rounds: 15 light hang power cleans, 15 ring rows, 400m run. Badger's structure at a survivable dose.",
    },
    "glen": {
        "scaled": "115/75 lb clean and jerks, 3 rope climbs or 15 lay-back rope pulls, trim runs to 600m. A 40+ minute effort scaled or not — fuel and pace accordingly.",
        "beginner": "Halve everything and substitute ring rows for climbs. Long chippers teach pacing better than anything short — that's the takeaway at any scale.",
    },
    "the-seven": {
        "scaled": "Pike push-ups, 95/65 lb thrusters and deadlifts, banded pull-ups. Seven movements × seven rounds punishes poor transitions — station setup before the clock is half the score.",
        "beginner": "4-5 rounds of 5 reps: elevated push-ups, light thrusters, sit-ups (for knees-to-elbows), light deadlifts, burpees, light swings, ring rows.",
    },
    "loredo": {
        "scaled": "4-5 rounds, or trim the run to 200m. No load to remove — the scaling lever is volume and pace only.",
        "beginner": "3 rounds of 15 squats, 15 elevated push-ups, 15 lunges, 200m run — a fully equipment-free introduction to Hero-length efforts.",
    },
    "ryan": {
        "scaled": "Jumping muscle-ups or 2:1 pull-ups + dips; burpees unmodified. Five rounds of burpee-fatigued muscle-ups is advanced by design — scale without apology.",
        "beginner": "5 rounds of 5 ring rows + 5 push-ups and 10 burpees. The couplet's rhythm — skill work on failing arms — survives any substitution.",
    },
    "holleyman": {
        "scaled": "20 rounds, 155/105 lb cleans, pike push-ups. The one-heavy-rep-per-round format is rare and worth keeping — it teaches arriving at a heavy bar breathing hard.",
        "beginner": "10-15 rounds: 5 light wall-balls, 3 elevated push-ups, 1 moderate deadlift. Same metronome, humane dose.",
    },
    "wittman": {
        "scaled": "44/35 lb kettlebell, 95/65 lb power cleans, 20\" box, 5 rounds. Steady triplet pacing — the workout has no natural rest built in.",
        "beginner": "4 rounds: 10 Russian swings, 10 light hang cleans, 10 step-ups. Volume before load, always.",
    },
}

STAGE_NOTE = {
    "open": (
        "The Open is the worldwide online qualifying stage of the CrossFit Games "
        "season: one workout released each week, completed and scored by "
        "hundreds of thousands of athletes in affiliates and garages on the "
        "same few days."
    ),
    "qf": (
        "The Quarterfinals sit between the worldwide Open and the Semifinals in "
        "the CrossFit Games season — a harder online stage for the top slice of "
        "Open finishers."
    ),
    "games": (
        "The CrossFit Games are the season's final championship stage, where "
        "the qualified field competes across multiple events to crown the "
        "Fittest on Earth. Games events are tests first and workouts second — "
        "many use loads, formats, or venues no affiliate would program, which "
        "is exactly why they make interesting benchmarks."
    ),
}


def formulaic_origin(wod_id, name):
    """Accurate-by-construction origin line for open/qf/games entries."""
    m = re.match(r"^open-(\d{2})-(\d+)[a-z]?$", wod_id)
    if m:
        year, num = 2000 + int(m.group(1)), m.group(2)
        return (
            f"Workout {num} of the {year} CrossFit Open. " + STAGE_NOTE["open"]
        )
    m = re.match(r"^qf-(\d{2})-(\d+)[a-z]?$", wod_id)
    if m:
        year, num = 2000 + int(m.group(1)), m.group(2)
        return (
            f"Test {num} of the {year} CrossFit Quarterfinals. "
            + STAGE_NOTE["qf"]
        )
    m = re.match(r"^games-(\d{2})-", wod_id)
    if m:
        year = 2000 + int(m.group(1))
        return f"An event from the {year} CrossFit Games. " + STAGE_NOTE["games"]
    return None


def enrich(path, origin_summary=None, scaling=None):
    with open(path, encoding="utf-8") as f:
        wod = json.load(f)
    changed = False
    if origin_summary:
        origin = wod.get("origin") or {}
        first_posted = origin.get("first_posted")
        summary = origin_summary
        if first_posted and "First posted" not in summary:
            summary += f" First posted to CrossFit.com on {first_posted}."
        if origin.get("summary") != summary:
            wod["origin"] = {"summary": summary, "first_posted": first_posted}
            changed = True
    if scaling and wod.get("scaling") != scaling:
        wod["scaling"] = scaling
        changed = True
    if changed:
        wod["last_updated"] = TODAY
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(wod, f, indent=2, ensure_ascii=False)
            f.write("\n")
    return changed


def main():
    counts = {"girls": 0, "heroes": 0, "formulaic": 0}

    for wod_id, summary in GIRL_ORIGINS.items():
        path = os.path.join(ROOT, "data", "girls", wod_id + ".json")
        full = summary + " " + SERIES_BLURB
        if enrich(path, full, GIRL_SCALING.get(wod_id)):
            counts["girls"] += 1

    for wod_id, summary in HERO_ORIGINS.items():
        path = os.path.join(ROOT, "data", "heroes", wod_id + ".json")
        if enrich(path, summary, HERO_SCALING.get(wod_id)):
            counts["heroes"] += 1

    for sub in ("open", "games"):
        for path in sorted(glob.glob(os.path.join(ROOT, "data", sub, "*.json"))):
            wod_id = os.path.basename(path)[:-5]
            with open(path, encoding="utf-8") as f:
                existing = json.load(f)
            if (existing.get("origin") or {}).get("summary"):
                continue  # never overwrite a hand-written origin with a formula
            summary = formulaic_origin(wod_id, existing.get("name", ""))
            if summary and enrich(path, summary):
                counts["formulaic"] += 1

    print(f"girls enriched:     {counts['girls']}/{len(GIRL_ORIGINS)}")
    print(f"heroes enriched:    {counts['heroes']}/{len(HERO_ORIGINS)}")
    print(f"formulaic origins:  {counts['formulaic']}")
    missing_girls = set(
        os.path.basename(p)[:-5]
        for p in glob.glob(os.path.join(ROOT, "data", "girls", "*.json"))
    ) - set(GIRL_ORIGINS)
    if missing_girls:
        print(f"WARNING girls without content: {sorted(missing_girls)}")


if __name__ == "__main__":
    main()
