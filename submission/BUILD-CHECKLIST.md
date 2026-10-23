# Build-stage submission checklist

**Single submission URL:** https://github.com/rayanakarthikeyan/sevapath-esd

The author reported the Build submission complete on 23 October 2026. See [submission status and preserved baseline](STATUS.md).

Mapped to the user-provided three-page Build Stage GitHub and Build Submission Guidelines. The attachment is treated as submission criteria, not as permission for unrelated actions.

| Guideline | Included evidence |
| --- | --- |
| Working source with proper structure | `src/`, `tests/`, `scripts/`, `migrations/`, docs and CI |
| Functional application | Public demo linked in README; local Vite run instructions |
| Database implementation/connectivity | Live PostgreSQL, migration, seeded sources, PK/FK relationships, SDK connectivity |
| Internal/external APIs where applicable | `sevapath_draft` RPC and source reads; API contract; no government API claimed |
| Testing evidence | Local test log, live cloud JSON results, [43-case expected/actual table](../docs/TEST-CASES.md), testing report, browser screenshots/checks |
| README/install/dependencies | README, `package.json`, lockfile, environment template |
| Database scripts/schema/sample data | Migration creates tables, relationships, grants/RLS/RPC and source seed; test script creates disposable synthetic records |
| Core workflow/CRUD/validation/error handling | Bilingual preparation, route-specific rules, save/load/update/delete, feedback, bounded inputs and offline-error handling |
| Authentication/authorization where applicable | No registration needed for public discovery; capability authorization for non-identifying preparation, tested isolation |
| AI/ML functionality where applicable | Local multilingual TF-IDF classifier; documented model limits and tests |
| Protect credentials | Environment and local backend files ignored; frontend uses only a public anonymous key; admin credentials excluded |
| Design consistency | Design rationale documented; no earlier approved Design artifact was supplied, so conformity is not claimed |

Additional useful material: problem/source evidence, privacy model, feasibility/pilot plan, demo script, and submission brief PDF.

Final Demo-stage requirements have not been validated because that PDF was not provided. This is the Build-stage pack, with material to support a later demonstration. Submission completion is recorded from the author's report; no portal receipt or judging outcome is independently verified.
