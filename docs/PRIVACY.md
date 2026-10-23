# Privacy, trust and prototype threat model

## Data flow

Intent queries are processed in the browser and kept in memory, not written to our database. Device cache stores only language, channel, employment category and readiness flags. Cloud saving is explicit. Document selection reads only `type` and `size`; neither file name nor contents is uploaded or stored. Print/export is initiated by the user.

Cloud drafts contain a source ID, random row ID, hash of a device capability, preparation choices, boolean flags and timestamps. Optional feedback is a boolean associated with that draft. No citizen name, address, phone, government identifier, income amount, photograph or document is required.

Google Fonts requests and ordinary hosting/backend request metadata remain external network traffic. Browser speech synthesis may use a browser/OS-provided voice; this app does not promise that every available voice performs synthesis offline. It reads only generic requirement text. No speech recording is performed.

## Threats and controls

| Threat | Implemented control | Residual issue |
| --- | --- | --- |
| Reading another person's preparation | Random 256-bit capability, hashed server-side; every RPC operation scopes by hash | Anyone who obtains the bearer capability can access that draft |
| Direct database enumeration | RLS enabled; private table grants revoked | Administrator access still exists by design |
| Sending personal fields in a draft | Whitelist and 1 KB size cap in RPC; client sanitizes fields | Users must still avoid personal details in free text; providers handle request metadata |
| Stored XSS | Input escaped before rendering; no uploaded content or rich text accepted | Dependency and deployment review still needed |
| Hallucinated government decisions | Model selects a category only; guidance is source-linked authored text | Published materials may be stale; officials decide acceptance |
| Prompt injection | No LLM, tool execution or query-driven instructions | Token overlaps can still misclassify a request |
| Shared device / browser storage loss | No identity data; visible delete option, export and shared-device notice | Same browser profile shares the key; losing key prevents recovery |
| Anonymous storage abuse | Fixed schema and one row per capability | Gateway rate limiting, quotas and expiry are not implemented |

## Suitability

This is a demonstration with non-identifying preparation data. It is not suitable for storing citizen documents or identifiers. A government pilot requires department source approval, independent security review, privacy/retention policy, authenticated assisted-service operations where needed and deployment appropriate to departmental requirements.
