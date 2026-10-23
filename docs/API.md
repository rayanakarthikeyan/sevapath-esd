# API contract

The frontend uses `@insforge/sdk`, not a simulated local API. Backend URL is configured using `VITE_INSFORGE_URL`. No government transaction API is used.

## Source catalogue

`client.database.from('service_sources').select('id,url').limit(10)`

Read-only public source records. Other returned fields can include title, review date and source version. Anonymous clients cannot modify the catalogue.

## Preparation RPC

**RPC name:** `sevapath_draft` (PostgREST function endpoint exposed by InsForge).

**Authentication/authorization:** SDK uses the project's public anonymous key. A private, random 64-character lowercase hexadecimal capability is passed as `p_token` in the JSON body. It authorizes only its own preparation draft. Tokens are generated with browser `crypto.getRandomValues`; SHA-256 hashes are stored. Never place the capability in URLs, logs, analytics, commits or screenshots.

```js
const {data,error} = await client.database.rpc('sevapath_draft', {
  p_action: 'save',
  p_token: deviceCapability,
  p_data: {
    language: 'en', channel: 'citizen', employment: 'self',
    identity_ready: true, income_ready: false,
    photo_ready: true, form_ready: false
  }
});
```

| Action | Input | Response | Behavior |
| --- | --- | --- | --- |
| `save` | Whitelisted preparation fields | `{draft:{id,source_id,language,channel,employment,...flags,created_at,updated_at},ready:false}` | Create or update the one draft owned by the capability. Server computes readiness. |
| `load` | Empty object | `{draft:{...},ready:boolean}` or `{draft:null}` | Return the matching draft, never another capability's record. |
| `delete` | Empty object | `{deleted:true}` | Idempotent deletion of own draft; linked feedback cascades. |
| `feedback` | `{helpful:true}` | `{recorded:true}` | Insert/update one optional boolean feedback row for an existing owned draft. |

The response never includes `token_hash` or raw capabilities. The returned ID is an opaque row identifier, not an application number.

## Validation

- `p_token`: exactly 64 lowercase hexadecimal characters.
- Save JSON must be an object, at most 1,024 serialized bytes; unknown keys rejected.
- Language `en|te`; channel `citizen|centre`; employment `salaried|self|other`.
- Checklist fields are booleans. DB constraints and casts reject invalid values.
- Feedback must be a JSON boolean; there must be a saved owned draft.
- Unknown action rejected. Missing draft on load is a normal null result.
- SDK errors are checked. UI preserves the device copy if a cloud call fails.

Omitted save fields reset to defaults; the frontend always sends a sanitized complete snapshot. This is a prototype last-write-wins API, without multi-tab conflict resolution.

## Local interfaces

`classify(text)` accepts at most 500 characters; returns a service or null, alternatives, evidence identifiers and a service-purpose flag. `requirements(plan,language)` returns source-linked rows. `readiness(plan)` returns checked/total/percent/ready. `validateFile({type,size},isPhoto)` examines MIME metadata and size only; it does not read contents or make a network request.

## Production boundary

The anonymous capability design limits data exposure but does not prevent a malicious party from creating many fresh drafts. Before wider rollout add gateway throttling, quotas, expiry, abuse monitoring and security review. No personal data is accepted by the intended save schema. The infrastructure provider still handles ordinary request metadata.
