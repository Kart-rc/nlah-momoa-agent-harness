# Day 1 — DataJunction & the Semantic Layer

- **Date read:** 2026-05-07
- **Source:** Netflix Tech Blog (Feb 2026)
- **Article:** [DataJunction as Netflix's answer to the missing piece of the modern data stack](https://netflixtechblog.medium.com/datajunction-as-netflixs-answer-to-the-missing-piece-of-the-modern-data-stack-92af926b40a5)
- **Topic bucket:** Data engineering / architecture
- **Visual app:** open [`./app/index.html`](./app/index.html) in a browser.

## Why this article

Most "modern data stacks" have storage (Iceberg/Delta), compute (Spark/Trino),
ingestion (Fivetran), and BI (Tableau/Looker) — but the layer that defines
**what a metric actually means** has historically lived inside dashboards or
buried in dbt models. Two consumers of the same number routinely disagree
because each one re-derives it. The semantic layer is the missing piece, and
DataJunction (DJ) is Netflix's open-source take on it.

## The problem in one picture

```
              Without a semantic layer
   ┌──────────┐     ┌──────────┐     ┌──────────┐
   │ Tableau  │     │ Notebook │     │  App API │
   │  query   │     │  query   │     │  query   │
   └────┬─────┘     └────┬─────┘     └────┬─────┘
        │ "DAU"          │ "DAU"          │ "DAU"
        ▼                ▼                ▼
   handwritten      handwritten      handwritten
   SQL #1           SQL #2           SQL #3
        \              |              /
         \             |             /
          ▼            ▼            ▼
         ┌─────────────────────────┐
         │    fact_user_session    │   ← three different
         └─────────────────────────┘     answers, same metric
```

Three teams, three SQL dialects, three subtly different `DAU` numbers. The
semantic layer collapses those into one canonical definition served to every
consumer.

## What DataJunction is

DJ is a **metrics platform**: a service that stores metric and dimension
definitions as a graph, parses SQL, and generates SQL on demand for any
combination of metric × dimensions × filters.

The graph has five node types:

| Node type | What it represents | Example |
|---|---|---|
| **Source** | A physical table | `warehouse.fact_user_session` |
| **Transform** | A reusable SQL transformation (a view) | `active_session = SELECT * FROM session WHERE duration > 30s` |
| **Dimension** | A reusable join target with attributes | `dim_user(country, plan_tier, signup_cohort)` |
| **Metric** | An aggregation expression on a node | `dau = COUNT(DISTINCT user_id)` |
| **Cube** | A pre-bound selection of metrics + dimensions + filters | `daily_engagement_cube` |

Edges encode how nodes depend on each other (transform → source, metric →
transform, etc.) and **how to join a dimension** to a fact node via a foreign
key declaration. Once the FK is declared, a consumer never writes the JOIN
again — they just ask for `dau` sliced by `dim_user.country` and DJ figures out
the path.

## The request lifecycle

```
 consumer asks: "DAU by country, last 30 days, plan_tier=premium"
        │
        ▼
 ┌─────────────────────────────────────────┐
 │ 1. DJ resolves nodes from the graph     │
 │    metric=dau  dim=user.country         │
 │    filter=event_date >= today-30        │
 │           AND user.plan_tier='premium'  │
 └─────────────────┬───────────────────────┘
                   ▼
 ┌─────────────────────────────────────────┐
 │ 2. Walks edges to find required joins   │
 │    fact_user_session ⟶ dim_user via     │
 │    user_id (declared FK)                │
 └─────────────────┬───────────────────────┘
                   ▼
 ┌─────────────────────────────────────────┐
 │ 3. Compiles a single SQL statement      │
 │    against the warehouse                │
 └─────────────────┬───────────────────────┘
                   ▼
 ┌─────────────────────────────────────────┐
 │ 4. Executes (or returns SQL) and        │
 │    returns one canonical answer         │
 └─────────────────────────────────────────┘
```

## Concrete example

Suppose the warehouse has two tables:

```sql
-- source: fact_user_session
user_id   BIGINT
session_start TIMESTAMP
duration_seconds INT
event_date DATE

-- source: dim_user
user_id   BIGINT  PK
country   STRING
plan_tier STRING        -- 'free' | 'premium'
signup_date DATE
```

In DJ you register them once:

```yaml
# source nodes
- name: warehouse.fact_user_session
  type: source
- name: warehouse.dim_user
  type: source
  primary_key: [user_id]

# dimension link (no SQL JOINs in app code after this)
- name: warehouse.fact_user_session.user_id
  dimension: warehouse.dim_user
  via: user_id

# metric
- name: metrics.dau
  type: metric
  query: |
    SELECT COUNT(DISTINCT user_id) AS dau
    FROM   warehouse.fact_user_session
    WHERE  duration_seconds >= 30
```

Now any consumer — Tableau, a notebook, a feature flag service, an LLM agent —
asks DJ:

```
GET /metrics/dau?dimensions=warehouse.dim_user.country
                &filters=warehouse.dim_user.plan_tier='premium'
                &filters=event_date>=current_date - interval '30' day
```

and DJ produces (and optionally executes) something like:

```sql
SELECT   u.country,
         COUNT(DISTINCT s.user_id) AS dau
FROM     warehouse.fact_user_session s
JOIN     warehouse.dim_user u
  ON     s.user_id = u.user_id
WHERE    s.duration_seconds >= 30
  AND    u.plan_tier = 'premium'
  AND    s.event_date >= current_date - interval '30' day
GROUP BY u.country;
```

Same SQL, every caller, every BI tool — that's the whole point.

## What makes DJ interesting versus alternatives

- **Graph-native storage.** Definitions are nodes/edges, not YAML files compiled
  per build. This means DJ can answer impact-analysis questions (what breaks if
  I rename `duration_seconds`?) cheaply.
- **First-class SQL parser/generator.** Most semantic layers (LookML, Cube,
  MetricFlow) emit SQL but treat it as opaque strings. DJ parses and rewrites
  it, so it can re-target the same metric to different engines (Trino, Spark,
  Druid) by swapping a dialect.
- **Cube nodes.** A "saved selection" of metrics+dimensions+filters becomes a
  first-class graph object that downstream tools can subscribe to and that DJ
  can pre-materialize.
- **Lineage for free.** Because every metric is reachable through the graph
  back to its source tables, column-level lineage falls out without an extra
  product.

## Trade-offs / things to watch

- **Compile vs execute.** DJ generates SQL, but actually serving p95 < 200 ms
  to dashboards usually requires a cube/cache layer or an MPP engine in front.
- **Governance is now a graph problem.** Renaming a dimension is no longer a
  Find/Replace; you need approval flows over the graph.
- **Single source of truth requires social, not just technical, buy-in.** If
  teams keep computing `dau` outside DJ, the canonical answer is canonical in
  name only.

## Take-aways for my own work

1. Treat metric definitions as **first-class long-lived assets** with owners,
   not as snippets re-derived per dashboard.
2. Push the join from the consumer into the platform via declared FKs — the
   user should ask for *what they want*, not *how to get it*.
3. A graph model of metadata makes lineage, impact analysis, and dialect
   re-targeting almost free; pick storage that supports it.
4. The semantic layer is most valuable at the moment LLM / agent consumers
   show up — they need a typed, governed surface, not raw SQL.

## The visual app

`app/index.html` is a single-file interactive demo:

- A small in-browser metric graph (3 sources, 1 transform, 1 dimension, 2
  metrics, 1 cube).
- A query builder where you pick a metric, drag in dimensions, add filters.
- A live SQL panel that **regenerates the SQL** as you change selections — so
  you can see how the same metric expands into different physical SQL when you
  slice it differently.
- A toy in-memory data set so you also see the numeric result change.

Open it directly in a browser — no build step. See [`app/README.md`](app/README.md).
