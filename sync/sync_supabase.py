#!/usr/bin/env python3
"""Sync the compiled data into the Supabase mirror tables (`wods`, `movements`).

The repo is the source of truth; this pushes the compiled bundles into Supabase so
the data is queryable (not just bulk-fetchable). Idempotent per table: it upserts
every current entry and deletes any row whose id is no longer present, so each
table ends up an exact mirror of its source file.

Run it manually once (after creating the tables with sync/supabase_schema.sql) to
verify, then let publish.yml run it on every merge to main.

Environment:
  SUPABASE_URL                 e.g. https://abcdefgh.supabase.co   (required)
  SUPABASE_SERVICE_ROLE_KEY    service-role key (bypasses RLS)      (required)
  WODS_TABLE                   table name (default: wods)           (optional)
  MOVEMENTS_TABLE              table name (default: movements)      (optional)

Uses only the standard library so it needs no dependencies to run.
Exits non-zero on any error.
"""
import json
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.join(os.path.dirname(__file__), "..")
INDEX_PATH = os.path.join(ROOT, "data", "index.json")
MOVEMENTS_PATH = os.path.join(ROOT, "data", "movements.json")
UPSERT_CHUNK = 500  # rows per request; well above current dataset size


# Columns promoted out of the JSONB blob for indexed filtering; everything else
# lives in `data`.
def wod_row(wod):
    return {
        "id": wod["id"],
        "name": wod["name"],
        "category": wod["category"],
        "format": wod["format"],
        "tags": wod.get("tags") or [],
        "data": wod,
    }


def movement_row(m):
    return {
        "id": m["id"],
        "name": m["name"],
        "category": m["category"],
        "workouts": m.get("workouts") or [],  # WOD ids that use this movement
        "data": m,
    }


def request(method, url, key, body=None, extra_prefer=None):
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal" + (f",{extra_prefer}" if extra_prefer else ""),
    }
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode("utf-8"), dict(resp.headers)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        sys.exit(f"Supabase {method} {url} failed: HTTP {e.code}\n{detail}")
    except urllib.error.URLError as e:
        sys.exit(f"Supabase {method} {url} failed: {e.reason}")


def sync_table(base, key, table, rows, source):
    """Upsert all rows, prune any id no longer present, verify the count."""
    if not rows:
        sys.exit(f"{source} has no entries — refusing to sync (would empty {table}).")
    ids = [r["id"] for r in rows]

    # Upsert on the primary key; merge-duplicates treats a matching id as update.
    upsert_url = f"{base}/rest/v1/{table}?on_conflict=id"
    for i in range(0, len(rows), UPSERT_CHUNK):
        request("POST", upsert_url, key, body=rows[i:i + UPSERT_CHUNK],
                extra_prefer="resolution=merge-duplicates")

    # Prune rows whose id is gone so the table exactly mirrors the source.
    # ids are [a-z0-9-], safe unquoted in the PostgREST filter.
    request("DELETE", f"{base}/rest/v1/{table}?id=not.in.({','.join(ids)})", key)

    _, headers = request("GET", f"{base}/rest/v1/{table}?select=id", key,
                         extra_prefer="count=exact")
    content_range = headers.get("Content-Range") or headers.get("content-range", "")
    total = content_range.split("/")[-1] if "/" in content_range else "?"
    print(f"{table}: upserted {len(rows)}, pruned stale; table now reports {total} rows.")
    if total.isdigit() and int(total) != len(rows):
        sys.exit(f"{table}: row count mismatch — table has {total}, expected {len(rows)}.")


def main():
    base = os.environ.get("SUPABASE_URL", "").rstrip("/")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    wods_table = os.environ.get("WODS_TABLE", "wods")
    movements_table = os.environ.get("MOVEMENTS_TABLE", "movements")
    if not base or not key:
        sys.exit("Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY.")

    with open(INDEX_PATH, encoding="utf-8") as f:
        wods = json.load(f).get("wods", [])
    with open(MOVEMENTS_PATH, encoding="utf-8") as f:
        movements = json.load(f).get("movements", [])

    sync_table(base, key, wods_table, [wod_row(w) for w in wods], INDEX_PATH)
    sync_table(base, key, movements_table, [movement_row(m) for m in movements], MOVEMENTS_PATH)
    print("Sync complete.")


if __name__ == "__main__":
    main()
