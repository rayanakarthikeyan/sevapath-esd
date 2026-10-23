# Testing evidence

Tests executed on **23 October 2026**, against the working build and its newly created prototype cloud backend.

| Layer | Cases / result | Evidence |
| --- | --- | --- |
| Local intent/rules/file/privacy regression | **26 passed, 0 failed** | [Raw TAP log](evidence/local-tests.txt), `tests/core.test.mjs` |
| Live PostgreSQL + SDK integration | **17 passed, 0 failed** | [Machine-readable actual results](evidence/cloud-results.json), `scripts/test-cloud.mjs` |
| Production build | **Pass** | [Build output](evidence/build.txt) |
| GitHub CI and public Pages deployment | **Success** | [Repository Actions](https://github.com/rayanakarthikeyan/sevapath-esd/actions) |

## Local cases

Sixteen intent regressions include English, Telugu-script, Romanized Telugu, off-topic text, mixed categories and a prompt-like unrelated request. Other cases cover service-purpose confirmation, maximum query length, citizen versus centre requirements, route-aware readiness, field stripping, exact and oversized photo boundaries, document limits, unsupported/empty files and valid PDF metadata.

These are curated regression cases, not an independently sampled multilingual benchmark. The tiny training corpus and thresholds are prototype choices. No generalization accuracy claim is made.

## Cloud cases

The test uses the real public anonymous SDK client, never an administrator client. Cases: public source read; create/read/update/delete; different-capability isolation; server-computed readiness; centre form requirement; invalid key; unexpected personal field; invalid route; invalid language; payload limit; direct private-table read/insert denial; feedback insertion; feedback ownership; invalid feedback type.

Each run generates new synthetic capabilities, removes its draft records in `finally`, and writes only redacted, non-identifying outcomes to the evidence file. No government system or citizen data is touched.

## Browser checks

Verified against the public GitHub Pages build:

| Check | Expected | Actual |
| --- | --- | --- |
| Scholarship prompt | Income preparation with exact-service caution | Caution displayed |
| Centre route | Additional completed-application checklist item | Four items displayed |
| Self-employment choice | Explain source-listed evidence alternatives | Guidance displayed |
| Complete checklist | Self-declared readiness, not approval | 4/4 and explicit boundary displayed |
| Cloud save/restore | Restore saved choices after a local change | Success toast and restored checked item |
| Telugu and phone layout | Core workflow remains available and readable | Rendered at 390 x 844; evidence screenshot included |
| Desktop layout | Core workspace and service cards render | Rendered at 1440 x 1000 |

Screenshots: [home](evidence/home-desktop.png), [cloud-restored plan](evidence/plan-cloud-restored.png), [Telugu mobile](evidence/plan-telugu-mobile.png). Further final-pass browser observations may be recorded in `evidence/browser-checks.json`.

Final-pass evidence: [eight browser checks](evidence/browser-checks.json), including successful cloud restore, route/language focus retention, mobile layout without horizontal content overflow, enlarged text, and [downloaded handoff content](evidence/sample-preparation.txt). No browser console warnings or errors were observed in that final pass. Print-to-PDF itself was not exercised; the downloadable text handoff was checked.

The first restricted localhost preview was inaccessible from the browser; public deployment was used for browser verification. The actual production build and API were tested, rather than claiming a successful inaccessible preview.

## Bugs identified, fixed and retested

1. Node 20 on Windows did not expand the test-file glob. The npm script now names the test file explicitly; all 26 tests pass.
2. A Romanized Telugu phrase matched below the threshold. Added normalization to a canonical intent term and reran the complete local regression suite.
3. Rerendered form controls lost keyboard focus. Focus restoration was added for language, text size, route, select and checklist controls; UI verification included the resulting focus behavior.
4. The cloud-saved label could remain after a device edit. A device mutation now resets the saved-session indicator.

## Remaining issues / verification limits

- No field usability study, government-side integration test, load test or formal penetration test.
- Native Telugu copy review and full screen-reader/200% browser-zoom review remain pending; no WCAG certification is claimed.
- Browser speech depends on installed voices; Telugu read aloud reports if a voice is unavailable. No claim of a tested installed Telugu voice.
- File validation checks MIME metadata and size only. It is not OCR, malware scanning or authenticity checking.
- Source text can be stale. The dates mean published guidance was reviewed, not that current departmental rules were certified.
- Quotas/rate limiting, automatic retention, draft recovery across devices and multi-tab conflict resolution are not implemented.
- The Vite SDK build emits a browser-externalized `crypto` module warning; the browser cloud workflow has been verified working. It is recorded instead of hidden.

## Reproduce

```sh
npm ci
npm test
npm run build
# Configure .env.local for your own linked test backend first:
npm run test:cloud
```
