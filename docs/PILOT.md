# Feasibility, scalability and impact plan

## Proposed pilot (not conducted)

Recruit 24 participants across Telugu-first rural/low-digital-literacy users, first-time applicants and senior citizens; include participants using assistive technology, with an accessibility facilitator. Recruitment must be voluntary and use synthetic situations rather than collecting actual citizen documents.

Use counterbalanced tasks: half begin with the published-form baseline, half with SevaPath; rotate equivalent scenarios to limit learning effects. Ask participants to identify a suitable document alternative, distinguish citizen login from centre preparation, and explain the next official step.

| Measure | Definition | Proposed success criterion |
| --- | --- | --- |
| Correct checklist completion | Correct mandatory items, no unnecessary mandatory payslip claim | At least 85% of pilot tasks; compare with baseline |
| Preparation time | Seconds from task start to correct checklist, excluding official processing | Median at least 30% below baseline |
| Missing-document errors | Required items omitted in the synthetic task | Reduction versus baseline; report counts and uncertainty |
| Assistance requests | Moderator intervention count | Lower than baseline without reducing accuracy |
| Confidence calibration | Participant can explain that readiness is not approval | At least 90% correctly explain boundary |
| Accessibility | Keyboard, screen reader, 200% zoom, Telugu comprehension | No blocker in core task; native Telugu copy review required |

Targets are hypotheses. No savings, rejection reduction, user count or field success is claimed in this submission. Report raw task counts, medians, ranges and small-sample uncertainty rather than extrapolating to all Telangana citizens.

## Integration route

1. ESD/service-owner validation of requirements, source freshness and terminology.
2. Read-only preparation companion with official links; no production portal modification is required for the initial pilot.
3. Add approved source snapshots and service-specific schemas one service at a time.
4. With department permission, embed the preparation layer in an existing portal or assisted-service flow. Authenticated government APIs would be separate future integration work.

## Cost and scaling

Local classification has no per-query model-provider cost. Static assets can be CDN-hosted; database reads are bounded and writes occur only on explicit save/feedback. Schema normalization separates source records, drafts and feedback. The project uses standard JavaScript and PostgreSQL, with source-controlled migrations.

No claim of load-test results or production capacity is made. Before a public rollout add rate limits, expiration/retention, monitoring, source review ownership, source version updates and capacity/load tests. Confirm hosting bills, data residency and departmental requirements before any government use. No new paid subscription is required by this prototype design.

## Defensibility

The differentiator is a verifiable preparation outcome: intent -> source-linked alternatives -> route-aware checklist -> saved progress -> official-service handoff. It is deliberately narrow enough to demonstrate real functionality and test it. A larger language model can later assist with paraphrasing only after a safety/evaluation plan; it should never infer unsupported rules or decide eligibility.
