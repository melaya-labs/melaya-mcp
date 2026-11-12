# Locale checks

## Per-file checks (blocking unless marked warn)

| Check | Blocks when |
|---|---|
| Key parity | a locale file lacks a source key, or has an empty value (a missing key shows the source language silently) |
| Orphan keys | warn: keys in a locale file that the source no longer has |
| Placeholders | a placeholder is renamed or dropped; moving it is fine; brace style must match the source file's convention |
| Plurals | plural branches do not follow CLDR for the target locale (for example Russian needs one, few, many, other; Chinese has one form); a file that copies the source's two forms into a locale that needs more |
| ICU syntax | a plural or select without an other branch; a zero branch that can never match (use =0) |
| Banned content | characters or markup the team's sanitizer blocks (often em or en dashes, HTML, BiDi controls), curly quotes inside code attributes or translation call arguments |
| Names | brand, product and technical names translated when the house style keeps them in Latin script |
| Untranslated | warn: value equal to the source and not on the runbook's allow-list (brand names, tier names, technical jargon, sample values, URLs) |
| Audit trail | a changed value without its audit entry, or below the runbook's confidence threshold and not flagged for review |
| Human lock | a human correction not locked as human in the audit file (the next machine run overwrites it) |

## Code checks (from the session diff)

- User-facing text not routed through the translation function (literal text between tags, literal placeholder, alt, aria-label or title attributes).
- Translated fragments concatenated into a sentence; one message per sentence with named placeholders instead.
- Dates, numbers or currency formatted without passing the locale.

## Live checks after deploy (sample per locale)

- html lang matches the locale.
- The title and description are localized, not the source language.
- Exactly one self-referencing canonical.
- hreflang lists every locale page, including itself, plus x-default, and the set is reciprocal across the sample pair.
- Structured data carries the page language.
- The page is in the locale's sitemap.

## Verdict rules

- Every finding names the file, the key and the locale.
- Counts come from files or check output read this turn.
- A gate that was not run is "not verified", never green.
- The CQO does not write translated copy; fixes go to the CPO.
