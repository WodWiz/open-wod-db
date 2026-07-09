-- open-wod-db -> Supabase mirror: `wods` + `movements` tables + RLS
-- ---------------------------------------------------------------------------
-- Run this ONCE, in the ISOLATED public-data Supabase project — NOT the main
-- WodWiz app project that holds member data. This table is anonymously readable
-- by the whole internet; keeping it in its own project means a mistaken policy
-- here can never expose real member data.
--
-- The repo (github.com/WodWiz/open-wod-db) stays the source of truth. This table
-- is a queryable MIRROR, kept in sync by scripts/sync_supabase.py (run manually
-- once to verify, then from publish.yml CI on every merge to main). Never
-- hand-edit rows here — they will be overwritten on the next sync.
-- ---------------------------------------------------------------------------

-- Hybrid shape: indexed columns for filtering + a JSONB blob of the full entry
-- (movements, load, format_meta, scaling, origin, ...) so we don't over-normalize
-- a dataset this small. `id` is the schema's human-friendly slug (fran, murph).
create table if not exists public.wods (
  id       text primary key,
  name     text not null,
  category text not null,
  format   text not null,
  tags     text[] not null default '{}',
  data     jsonb  not null
);

-- Filter indexes for ?category= / ?format= / ?tag= query params.
create index if not exists wods_category_idx on public.wods (category);
create index if not exists wods_format_idx   on public.wods (format);
create index if not exists wods_tags_idx     on public.wods using gin (tags);

-- Trigram index so ?search=fran (name ILIKE '%fran%') stays fast.
create extension if not exists pg_trgm;
create index if not exists wods_name_trgm_idx
  on public.wods using gin (name gin_trgm_ops);

-- ---------------------------------------------------------------------------
-- RLS: anonymous, read-only. There are deliberately NO insert/update/delete
-- policies, so anon + authenticated roles can ONLY SELECT. The sync job connects
-- with the service-role key, which bypasses RLS entirely, so it can upsert and
-- prune without any write policy existing.
-- ---------------------------------------------------------------------------
alter table public.wods enable row level security;

drop policy if exists "Public read access" on public.wods;
create policy "Public read access"
  on public.wods
  for select
  to anon, authenticated
  using (true);

grant select on public.wods to anon, authenticated;

-- ---------------------------------------------------------------------------
-- `movements` — the movement library, mirrored from data/movements.json.
-- `workouts` is the movement->workout mapping (WOD ids that use the movement),
-- promoted to a text[] column so the app can query it (e.g. movements used in a
-- given WOD via `workouts @> array['fran']`). Full entry (equipment, aliases,
-- description, ...) lives in `data`.
-- ---------------------------------------------------------------------------
create table if not exists public.movements (
  id       text primary key,
  name     text not null,
  category text not null,
  workouts text[] not null default '{}',
  data     jsonb  not null
);

create index if not exists movements_category_idx on public.movements (category);
create index if not exists movements_workouts_idx  on public.movements using gin (workouts);
create extension if not exists pg_trgm;
create index if not exists movements_name_trgm_idx
  on public.movements using gin (name gin_trgm_ops);

alter table public.movements enable row level security;

drop policy if exists "Public read access" on public.movements;
create policy "Public read access"
  on public.movements
  for select
  to anon, authenticated
  using (true);

grant select on public.movements to anon, authenticated;
