# Test cases, expected outcomes and recorded actual results

Build-stage evidence format: **test case / expected result / actual result / status**. All results below come from the passing assertions in [local TAP](evidence/local-tests.txt) and [live cloud results](evidence/cloud-results.json), rerun on 23 October 2026. They are regression/integration results, not a citizen study.

## Local suite: 26 cases

| Test case | Expected result | Recorded actual result | Status |
| --- | --- | --- | --- |
| Income proof for family | Income category | Income assertion passed | PASS |
| Income without payslip | Income category | Income assertion passed | PASS |
| Scholarship / fee reimbursement | Income category | Income assertion passed | PASS |
| Romanized Telugu income phrase | Income category | Income assertion passed | PASS |
| Telugu income-certificate phrase | Income category | Income assertion passed | PASS |
| Telugu irregular-income phrase | Income category | Income assertion passed | PASS |
| Newborn birth certificate | Birth category | Birth assertion passed | PASS |
| Telugu birth-certificate phrase | Birth category | Birth assertion passed | PASS |
| Address / residence proof | Residence category | Residence assertion passed | PASS |
| Telugu residence phrase | Residence category | Residence assertion passed | PASS |
| Old-age / Aasara pension | Pension category | Pension assertion passed | PASS |
| Telugu pension phrase | Pension category | Pension assertion passed | PASS |
| Weather query | No confident service match | Null-service assertion passed | PASS |
| Unrelated instruction-like query | No confident service match | Null-service assertion passed | PASS |
| Mixed income and birth query | Ask for clarification | Null-service assertion passed | PASS |
| Empty query | No service match | Null-service assertion passed | PASS |
| Scholarship-purpose flag | Exact-service confirmation required | True flag asserted | PASS |
| More than 500 characters | Reject input | Exception asserted | PASS |
| Citizen versus centre requirements | Three versus four checklist items | Both counts asserted | PASS |
| Route-aware readiness | Centre needs application form; citizen route does not | Both readiness assertions passed | PASS |
| Unknown/personal fields | Strip fields and use safe defaults | Sanitized snapshot asserted | PASS |
| Photo exactly at reference boundary | Accept metadata | Accepted flag asserted | PASS |
| Oversized photo | Reject metadata | Rejected flag asserted | PASS |
| Oversized document | Reject metadata | Rejected flag asserted | PASS |
| Unsupported or empty file | Reject metadata | Both rejected flags asserted | PASS |
| Small valid PDF metadata | Accept format/size only | Accepted flag asserted | PASS |

## Live cloud suite: 17 cases

| Test case | Expected result | Recorded actual result | Status |
| --- | --- | --- | --- |
| Read official sources | Three readable source rows | Count and error assertions passed | PASS |
| Create preparation | A draft ID; not ready; no token hash in response | All response assertions passed | PASS |
| Read owned draft | Saved employment category returned | Matching field asserted | PASS |
| Read with another capability | No draft returned | Null draft asserted | PASS |
| Update existing preparation | Telugu saved; readiness recalculated | Language and ready flag asserted | PASS |
| Centre without application form | Not ready | False readiness asserted | PASS |
| Invalid capability syntax | Error | Error asserted | PASS |
| Unexpected personal field | Error | Error asserted | PASS |
| Invalid route enum | Error | Error asserted | PASS |
| Invalid language enum | Error | Error asserted | PASS |
| Oversized payload | Error | Error asserted | PASS |
| Direct anonymous private-table read | Denial or no rows | Denial/no-rows assertion passed | PASS |
| Direct anonymous private-table insert | Error | Error asserted | PASS |
| Feedback for owned draft | Recorded | Recorded flag asserted | PASS |
| Feedback with another capability | Error | Error asserted | PASS |
| Non-boolean feedback | Error | Error asserted | PASS |
| Delete owned draft | Deleted; subsequent load returns null | Deletion/read assertions passed | PASS |

The raw results are the authoritative run evidence. This table states the assertions each passing case verifies; it does not claim unrecorded server response values. Existing bugs, fixes, retesting and outstanding verification limits remain in [TESTING.md](TESTING.md).
