import json, os, glob

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data")

def title(s):
    return " ".join(w.capitalize() for w in s.replace("-", " ").replace("_", " ").split())

def same_scheme(movements):
    reps = [tuple(m["reps"]) if isinstance(m.get("reps"), list) else None for m in movements]
    return len(set(reps)) == 1 and reps[0] is not None

def format_movement_line(m):
    name = title(m["exercise"])
    load = f" ({m['load']['rx_male']}/{m['load']['rx_female']})" if m.get("load") else ""
    dist = f" {m['distance_m']}m" if m.get("distance_m") else ""
    reps = m.get("reps")
    if isinstance(reps, list):
        reps_str = "-".join(str(r) for r in reps) + " "
    elif isinstance(reps, (int, str)):
        reps_str = f"{reps} "
    else:
        reps_str = ""
    return f"  {reps_str}{name}{dist}{load}".rstrip()

def render_markdown(wod):
    lines = [f"# {wod['name']}", ""]
    movements = wod["movements"]
    if wod["format"] == "for_time" and same_scheme(movements):
        scheme = "-".join(str(r) for r in movements[0]["reps"])
        lines.append(f"**{scheme}**")
        for m in movements:
            load = f" ({m['load']['rx_male']}/{m['load']['rx_female']})" if m.get("load") else ""
            lines.append(f"  {title(m['exercise'])}{load}")
    else:
        meta = wod.get("format_meta") or {}
        header = {
            "amrap": f"**AMRAP {meta.get('time_cap_minutes','?')} min**",
            "emom": f"**EMOM {meta.get('total_minutes','?')} min**",
            "interval": f"**{meta.get('rounds','?')} rounds for time**",
            "max_load": "**Max load**",
        }.get(wod["format"], f"**{title(wod['format'])}**")
        lines.append(header)
        for m in movements:
            lines.append(format_movement_line(m))
    lines += ["", f"*Type: {title(wod['format'])} · Category: {title(wod['category'])}*"]
    return "\n".join(lines) + "\n"

all_entries = []
for category_dir in ["girls", "heroes"]:
    for path in sorted(glob.glob(os.path.join(DATA, category_dir, "*.json"))):
        with open(path, encoding="utf-8") as f:
            wod = json.load(f)
        all_entries.append(wod)
        md_path = path.replace(".json", ".md")
        # Force UTF-8 + LF so output is byte-identical on Windows and Linux
        # (default text mode would emit cp1252/CRLF on Windows).
        with open(md_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(render_markdown(wod))

index_path = os.path.join(DATA, "index.json")
with open(index_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump({"count": len(all_entries), "wods": all_entries}, f, indent=2)

print(f"Indexed {len(all_entries)} structured WODs -> {index_path}")
print("Generated matching .md files for each entry.")
