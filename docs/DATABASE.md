# Database implementation

The demo uses **live PostgreSQL on InsForge**, with access through the SDK/PostgREST. Reproducible DDL and source seeds are in `migrations/20261023135800_create-sevapath.sql`.

| Table | Primary key | Important columns | Relationships / access |
| --- | --- | --- | --- |
| `service_sources` | `id` text | title, official URL, review date, version | Public read only; administrator-managed source catalogue |
| `preparation_drafts` | `id` UUID | unique token hash, language, channel, employment, four boolean flags, timestamps | `source_id` references sources; no direct anonymous/authenticated table privileges |
| `preparation_feedback` | `draft_id` UUID | helpful boolean, creation timestamp | FK to draft; cascade delete; no direct anonymous/authenticated table privileges |

## Relationships

One source can support many preparation drafts. Each preparation has at most one feedback row. `token_hash` uniquely enforces one draft per capability. All three tables have RLS enabled. The private tables have no runtime read/write policies or grants; a narrowly scoped security-definer RPC provides the allowed actions.

The RPC pins `search_path` to `pg_catalog, public, pg_temp`, uses static parameterized PL/pgSQL, checks the capability and input, and scopes every private read/update/delete by the token hash. No dynamic SQL or service/admin key is shipped in the browser.

## Setup

Link your own empty test backend, then run `npx -y @insforge/cli db migrations up --all`. The migration seeds three official sources. No real citizen data is included. `npm run test:cloud` creates temporary synthetic records and deletes them in a `finally` block.

## Important inspection queries (administrator only)

```sql
SELECT id, title, reviewed_on, version FROM public.service_sources ORDER BY id;
SELECT channel, count(*) FROM public.preparation_drafts GROUP BY channel;
SELECT helpful, count(*) FROM public.preparation_feedback GROUP BY helpful;
SELECT relname, relrowsecurity
FROM pg_class WHERE relname IN ('service_sources','preparation_drafts','preparation_feedback');
```

Avoid publishing token hashes, row-level draft records or infrastructure credentials in evidence. Public dashboard metrics are deliberately not exposed. Feedback is a simple acceptability signal, not proof of real-world impact.

## CRUD evidence

See `docs/evidence/cloud-results.json`: create, read, update, delete, authorization, input validation and feedback were exercised against the actual cloud database. Restore uses `load`, and cloud save uses upsert. Deletion removes linked feedback automatically.

## Remaining operational work

Automated draft expiry/retention, quotas, abuse throttling, monitoring, backup/recovery exercises, source refresh governance and concurrency/version handling are production work. The current build does not claim these are implemented.
