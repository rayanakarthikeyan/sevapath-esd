# Problem evidence and design rationale

## Selected problem

**Citizens need help turning published certificate requirements into a complete, situation-aware preparation plan before starting a government application.**

First scope: general income certificates, especially a student or a citizen without a payslip. The intervention improves the journey into an existing service instead of creating a parallel government transaction system.

## Primary sources reviewed on 23 October 2026

| Source | Supported observation | Design response |
| --- | --- | --- |
| [Telangana mobile-governance FAQ](https://mgov.telangana.gov.in/faqnew.html), Applications & Certificates / General | The published guidance describes immediate completion of a begun application, advance document preparation and restrictions on changing submitted requests. It also describes document/photo format and size limits. | Resumable preparation before official submission; a checklist and local reference-limit checks. |
| [Income form](https://www.telangana.gov.in/wp-content/uploads/2023/03/IncomeGeneralApplicationForm.pdf), documents section | The form lists several identity and income-evidence alternatives, a photograph, and an application-form exception for citizen login. | Show alternatives, not an invented universal payslip requirement; change the checklist by application route. |
| [State public utility forms](https://www.telangana.gov.in/services/public-utility-forms/) | The official service index links citizens to separate forms/services. | Use citizen language for discovery and link back to the official resource. |

The source URL date/path is not its effective policy date. A review date means the published text was read, not that a department certified its currency. The FAQ could refer to an older system. No current portal audit, representative interviews, abandonment baseline or measured repeat-visit rate is claimed.

## User story (illustrative, not an interview)

A Telugu-first student needs an income-related document for an institution. The household has irregular earnings and no payslip. They need to identify the exact service, see the evidence alternatives, decide whether to use citizen login or seek centre assistance, and bring the relevant items.

The assistant flags that general income and fee-reimbursement services may differ. The citizen must confirm the institution's exact requirement. It does not decide scholarship eligibility or automatically treat one certificate as interchangeable with another.

## Why this intervention

The unit of improvement is a correct next step, not chatbot engagement. Guidance is bounded by a maintained source catalogue. Route-specific readiness makes the outcome testable. The offline local model avoids an inference bill and avoids sending citizen queries to a model provider. A complete narrow workflow is more feasible to validate with ESD owners than a speculative catalogue of hundreds of services.

## Design decisions

- A calm forest-green, ivory and sage workspace; an original inline architectural illustration evokes Telangana without official endorsement.
- A natural-language entry and visible service shortcuts; citizens can bypass inference entirely.
- Ambiguous/mixed or unrelated requests ask for clarification. Similarity scores are not probabilities and are not exposed as false certainty.
- English/Telugu switching, keyboard controls, large-text control, browser read aloud, responsive layout and printable handoff. No claim of WCAG certification.
- No account/OTP wall for discovering public requirements. Random device capability protects non-identifying cloud preparation.
- The complete experience covers income preparation only; other service cards explicitly disclose their directory-only scope.

## How this fits the challenge

AI-enabled discovery: small, local multilingual classification. UX innovation: intent-to-preparation, route-aware checklist, saved progress. ESD: existing official service handoff. Inclusion: Telugu-first copy and lower-complexity interaction. Governance: provenance, uncertainty, minimal data and measurable pilot criteria.
