# Worked example: a research vault

Fictional throughout: Dr. Amara Lindqvist, a researcher at the (invented) Ridgeback Urban Climate Group, studies how street-tree canopy changes night-time summer temperatures. Every paper, author and number below is invented for illustration. The flow follows scenario 4 in [../modules/scenarios.md](../modules/scenarios.md).

## 1. Charter

Readers: Amara and two doctoral students; later a reading assistant agent. Zones: internal, plus a public "Concepts" set for a course website. Language: English; a few German papers summarised in English.

Test questions:

| # | Question |
|---|---|
| 1 | Which studies measured night-time cooling from canopy, and how large was it? |
| 2 | Which methods (fixed sensors, mobile transects, satellite) were used, with what limits? |
| 3 | Where do studies disagree, and why? |
| 4 | Which of our own datasets cover 2024 and 2025 summers? |
| 5 | What is the current draft argument of chapter 3? |

## 2. Sources

| Source | Items | Handling |
|---|---|---|
| Reference manager export (BibTeX plus PDFs) | 146 references, 131 PDFs (18 scanned) | one literature note per reference read; OCR for scans |
| Web clippings | 40 pages | literature or reference notes, short quotes |
| Lab notebook (OneNote) | 3 notebooks, 210 pages | methods, data descriptions, decisions |
| Seminar recordings | 12 talks with transcripts | concept and claim notes, cited by timestamp |
| Drive folder "Data" | 9 sheets | described in data notes, data stays in Drive |

## 3. Architecture

```bash
python3 scripts/scaffold.py --vault ~/vaults/canopy --name "Canopy and Night Heat" \
  --sections "10 Questions,20 Concepts,30 Literature,40 Methods,50 Data,60 Findings,70 Writing,90 Reference" \
  --owner amara --today 2026-11-10
```

`_Meta/vault-config.json` adds two types and their required sections:

```json
{
  "types": ["moc", "concept", "process", "reference", "decision", "person", "team", "project", "glossary", "term",
            "faq", "meeting", "source", "log", "meta", "literature", "claim"],
  "sections": {"literature": ["At a glance", "Claims", "Method", "Limits", "My reading", "Related"],
               "claim": ["At a glance", "Evidence for", "Evidence against", "Related"]}
}
```

Tags: `topic/canopy`, `topic/night-temperature`, `topic/sensors`, `topic/transects`, `topic/remote-sensing`, `source/bibtex`, `source/onenote`.

## 4. A literature note

`30 Literature/Okafor 2023 Canopy Night Cooling.md` (citation key as alias):

```markdown
---
type: literature
description: A fictional 2023 sensor study that reports night-time cooling under dense street canopy in one mid-size city.
tags:
  - area/literature
  - topic/canopy
  - topic/sensors
  - source/bibtex
aliases:
  - okafor2023canopy
related:
  - "[[Literature]]"
  - "[[Canopy Cover]]"
  - "[[Claim Dense Canopy Cools Nights]]"
audience: team
updated: 2026-11-08
---

# Okafor 2023 Canopy Night Cooling

Okafor and Hale (2023, fictional) placed 60 fixed sensors under streets with different canopy cover for two summers.

## At a glance

- Dense canopy streets were 0.4 to 0.9 C warmer at 03:00 than open streets (p. 7, Table 2).
- The effect reversed in the afternoon (p. 8).
- Limits: one city, two summers, sensors at 3 m.

## Claims

- Canopy traps longwave radiation at night (p. 9). ^claim-trap

## Method

Fixed sensors, 10-minute interval, June to August 2021 and 2022 (p. 4).

## Limits

- Single city; humidity not controlled (p. 11).

## My reading

> [!info] Inference
> The warming at night may depend on sky view factor more than on canopy alone; compare [[Sky View Factor]].

## Related

- [[Literature]]
- [[Claim Dense Canopy Cools Nights]]
- [[Fixed Sensor Networks]]
```

Note how the source's finding contradicts the claim note's title: the claim note lists this paper under Evidence against, with `[[Okafor 2023 Canopy Night Cooling#^claim-trap]]`.

## 5. Claims, views and maps

- 38 claim notes, each with Evidence for and Evidence against linking literature at block level.
- `Bases/Literature.base`: table by year and method; cards view of papers without "My reading" (a reading queue: `file.hasProperty("read")` false).
- `Canvas/Argument Chapter 3.canvas`: claim notes as file nodes, groups "supports", "contradicts", "open", edges labelled with the page reference.

## 6. Scans and transcripts

18 scanned PDFs were run through `ocrmypdf`; numbers quoted from them carry `(OCR, verify)` until Amara checked them against the page image (14 verified in the first pass). Seminar claims cite `Seminar 2025-03-12, 00:41:10`.

## 7. Public concepts

The 20 Concepts notes are public for the course site; literature, data and writing stay internal (`_Meta/.publishignore` lists `30 Literature/`, `50 Data/`, `60 Findings/`, `70 Writing/`). `export_public.py --out ../canopy-site --unlink` produces 21 notes (concepts plus Home), with links into internal notes turned into plain text.

## 8. Result

163 literature notes, 38 claims, 26 concepts, 11 method notes, 9 data notes; checker 0 errors; graph: one component, max 3 hops, 5.4 links per note. Test question 3 ("where do studies disagree") is answered by the claim notes' Evidence against sections, each with page-level citations.
