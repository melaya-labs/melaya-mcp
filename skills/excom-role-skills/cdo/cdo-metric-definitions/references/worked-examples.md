# Worked examples of good definitions

Each definition answers the same eight questions: name, formula, source of truth, cohort rule, exclusions, consent dependency, retention, owner. These two are the recommended defaults when the team's note lacks them. Propose them to the owner, and do not apply them silently.

## Active affiliate

| Field | Value |
|---|---|
| Name | Active affiliate |
| Formula | An affiliate account with at least one referred signup. Anyone without a referred signup is only an account, however long ago they enrolled |
| Source of truth | The affiliate platform: referrals per affiliate (for Affonso, `affonso_list_referrals` and `affonso_get_affiliate_analytics`), cross-checked against first-party registrations that carry the referral |
| Cohort rule | All-time by default ("has ever generated a referred signup"). If the team wants recency, state the window explicitly, for example "in the last 90 days" |
| Exclusions | Staff and test accounts, self-referrals, signups the programme terms exclude |
| Consent | The referral cookie may need consent. Count server-side registrations carrying the referral, not client clicks |
| Retention | As long as the affiliate platform keeps referral records |
| Owner | CDO (definition), revenue or partnerships role (programme) |

Why it is good: it counts a behaviour that predicts revenue (a real referral) instead of an enrolment, so the number cannot be inflated by sign-ups that never act.

## Signed partner

| Field | Value |
|---|---|
| Name | Signed partner |
| Formula | A partner whose signed agreement is filed in that partner's folder under the team's partner agreements folder in Google Drive |
| Source of truth | Google Drive: `drive_search` inside the partner agreements folder (the folder id is recorded in the knowledge base), one subfolder per partner. A signature record from the e-signature tool (`docusign_list_envelopes` or similar) supports it but does not replace the filed copy |
| Cohort rule | Count at the read time. A partner counts from the date of the filed signed agreement |
| Exclusions | Drafts, unsigned or partially signed versions, expired or terminated agreements (moved out of the folder or marked so), letters of intent unless the team counts them explicitly |
| Consent | Not applicable. Do not copy agreement contents into notes; link the file |
| Retention | As long as the agreement is in force |
| Owner | CDO (definition), partnerships role (filing) |

Why it is good: it is auditable. Anyone can open the folder and check, and "signed" cannot drift into "verbally agreed" or "page published".

## Checklist for any new definition

- Does it count an outcome, not an activity?
- Can two people compute it and get the same number?
- Is the source of truth one place that someone can open?
- Are exclusions written down?
- Does it state the window and time zone?
- Is the owner a role, not a person?
