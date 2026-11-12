# Description and chapter rules

## Description layout

1. Line 1: the problem and the outcome in one line, under 120 characters, with the target query words verbatim. It is the only text shown above "Show more".
2. Blank line.
3. Three bullets, each a concrete result or step from the video (numbers, named tools).
4. The matching page link with a 2 to 5 word label, above the chapters.
5. Blank line.
6. The chapter list.
7. Optional: one or two related video or doc links, nothing else.

YouTube descriptions do not render markdown, so weight comes from position and wording.

## Chapter rules (strict)

1. The first chapter is 00:00, otherwise YouTube ignores the whole list.
2. Timestamps ascend and each chapter lasts at least 10 seconds; one short chapter breaks key-moment parsing for the entire list.
3. Count by length: under 3 minutes, 3 to 5 chapters (at least 3); 3 to 8 minutes, 6 to 10; over 8 minutes, 10 to 18.
4. Each label is 3 to 8 words, phrased as a searchable sub-step: verb, object, context. "Map columns to staff roles", "Fix the duplicate shift error".
5. The 00:00 label names the hook, never "Intro"; never "Part 1" or "Outro".
6. Use the time the step appears on screen, not when the speaker starts talking about it, so viewers arriving from search see the step at once.
7. Format mm:ss under one hour, h:mm:ss from one hour; one chapter per line.

## Validation before handoff

Print: "Chapters: N, first 00:00, all >= 10 s, count within band". Fix and re-check if any rule fails.

## Launch posts

- One plain-text block per platform: the strongest beat as the hook, one line on who it is for, 3 to 5 chapter lines, then the call to action.
- Follow the team's link policy per platform: where links are not allowed, name the place ("on our YouTube channel") instead of linking.
- Repeating chapter phrasing in posts gives the searchable wording a second indexed surface.

## Embed on the matching page

Place the video under the first H2 it answers, add video structured data whose parts mirror the chapters with start and end offsets in seconds, and add the page URL to the video description so each surface links to the other.
