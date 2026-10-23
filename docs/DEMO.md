# Demo script and judge Q&A

## 90-second walkthrough

**0-15 s - The real problem.** “A citizen knows they need a certificate, but not which documents fit their situation. The published MeeSeva guidance asks citizens to prepare before completing the application. SevaPath improves that preparation journey.”

**15-30 s - Understand a need.** Click **No payslip?**. Show that the assistant recognizes income preparation and explains the published alternatives. Open the official source. Click **College scholarship** to show that the app asks the citizen to confirm the exact service instead of assuming general income is interchangeable with fee reimbursement.

**30-50 s - Make the next step concrete.** Open **My preparation**. Switch citizen login to centre. Explain why a paper application appears for the centre route. Choose self-employment to see the proof-alternative guidance. Tick only the items you have.

**50-65 s - Show a real system.** Save the preparation to cloud. Change one item locally, then restore; the saved copy returns from PostgreSQL. Explain that a random capability controls this draft and that no ID number or document is collected.

**65-80 s - Inclusion and handoff.** Switch to Telugu. Show larger text, optional read aloud, and download/print. The checklist gives the citizen a useful handoff to MeeSeva; the app does not submit a government application.

**80-90 s - What comes next.** “The source-controlled build includes the schema, API contract and actual local/cloud tests. We propose a measured usability pilot with ESD to validate preparation accuracy and time, starting with this one service.”

## Answers to likely questions

**Where is the AI?** A small on-device TF-IDF classifier uses a curated multilingual corpus and cosine similarity for intent discovery. It is not an LLM. Guidance is bounded by authored source-linked rules. Citizens can choose service cards if inference is uncertain.

**Why not a broad chatbot?** The measurable outcome is correct preparation. A general answer without source grounding or a completed workflow would not solve that task reliably.

**Is there a real database/API?** Yes. InsForge PostgreSQL, source seeds, tables, PK/FK constraints, RLS and the `sevapath_draft` RPC. The integration suite exercises actual database-backed CRUD and isolation using the public anonymous SDK client.

**Why no registration?** Reading public requirements should not require an account. Saved preparation contains no identifying data, so a random device capability is sufficient for this limited prototype. Government transactions remain with the official system.

**Does “100%” mean approved?** No. It means the citizen has self-declared the checklist items ready. Officials decide document acceptance and the government service processes the application.

**Can it prevent every rejection?** No. It checks format and size metadata locally and explains requirements; it does not verify document contents or authenticity, decide eligibility, or promise acceptance.

**What has been measured?** Local behavior tests, live database integration tests, production build and browser checks documented in the evidence pack. Citizen pilot targets have not been achieved or measured yet.

**What about the earlier approved design?** No approved Design-stage artifact was supplied. This build's scope/design decisions are explicit; prior-stage conformance is not claimed.

## Submission logistics

The screenshot states Build submission is due **23 October 2026** and accepts one GitHub/Drive link. Use the repository root link. The screenshot separately lists Demo submission on **25 October 2026**. Its Final Demo guidelines PDF was not provided; inspect it before claiming the final stage is complete or recording/submitting any required pitch format.

No competition portal submission has been performed by this project build.
