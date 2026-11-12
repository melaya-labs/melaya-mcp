---
name: cto-partner-go-live
description: Takes a newly signed partner live on the site: checks the signed agreement is filed, runs the team's partner launch runbook and announcement blog post runbook in a coding session, deploys through CI with approvals, verifies the live pages and reports the URLs back. Use when a partner is signed, when the partnerships executive or CEO asks "put the partner live", "publish the partner page" or "announce the partnership", or when a partner page is missing after signature.
version: 2.0.0
---
# Partner go-live

Put a signed partner on the site the same week: partner page, listings and the announcement post, shipped safely and verified live. A partner who sees their page fast promotes it.

## Look up first

- The partner agreements folder id: `excom_knowledge_search` "partner agreements folder", then `excom_knowledge_read`. If missing, ask the owner with `excom_propose_task` (needs decision true) and stop.
- The partner launch runbook and the announcement blog post runbook in your knowledge base: `excom_knowledge_search` "partner launch runbook" and "blog post runbook". If either is missing, draft it from what the request contains with `excom_save_draft`, propose it to the owner, and do not improvise the code change.
- The requester and the partner record (name, slug, logo, approved copy, launch date): from the request, `excom_read_tasks`, or ask the partnerships executive with `excom_send_handoff` (kind question).
- Grants: Drive (`drive_*`), the coding grant, CI (`jenkins_*` if your CI is Jenkins). Missing: `excom_request_setup`.

## Steps

1. Verify the signature is filed: `drive_search` for the partner name inside the agreements folder, then `drive_list` on the partner's folder. The signed agreement must be there (a signed PDF or the e-signature completion certificate). If it is not filed, stop and ask the partnerships executive with `excom_send_handoff` (kind question), because nothing goes public before the contract is on file.
2. Check the inputs the launch runbook requires (copy approved by the partner, logo files, links, tracking or referral codes). Missing inputs go back to the requester in one question.
3. Code the launch in one coding session: `excom_code_task` (record write) with the launch runbook as the runbook and the partner record as evidence. Judge it with skill cto-coding-session-hygiene and `excom_code_status`.
4. Code the announcement post with the blog post runbook, in the same session if the runbook allows, otherwise a second session. Copy comes from the requester or the CMO, never invented.
5. Review with skill cto-push-review-gate, then `excom_code_push` target branch (send, asks) and target base (production, always asks).
6. Deploy with skill cto-jenkins-safe-deploy: `jenkins_trigger_build` (production, asks), `jenkins_wait_build` to green.
7. Verify live: `web_fetch` the partner page, the listing that should link to it and the blog post. Check title, partner name, links resolve, no placeholder text. If Search Console is granted, `gsc_url_inspect` the new URLs; submissions to search engines are send class and ask.
8. Report back to the requester (and the partnerships executive) with `excom_send_handoff`: the URLs, what was verified, anything left for the partner to do. Close with `excom_update_task`.

## Output

```text
Partner go-live: <partner>
Agreement filed: yes (folder path, file name)
Session(s): id, diff stat, checks
Push: branch / base approved
Deploy: job #build green
Live URLs: partner page, listing, blog post (each verified yes/no)
Open items: ...
```

## Approvals

- Starting the coding session (record write under Prepare).
- `excom_code_push` branch (send) and base (production); every CI build (production).
- Any announcement on social, email or to the partner directly (send, by the CMO or the partnerships executive).

## Example

The partnerships executive writes "Acme signed, put them live". `drive_search` finds "Acme - signed agreement.pdf" in the agreements folder. Session S-51 adds the partner page and listing entry; session S-52 adds the post. Both pushed and deployed after approval. `web_fetch` confirms /partners/acme and /blog/acme-partnership render. Report sent with both URLs.
