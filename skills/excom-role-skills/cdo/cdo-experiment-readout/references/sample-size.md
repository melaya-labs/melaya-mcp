# Sample size and readout rules

## Conversion rate (two arms, 5 percent significance, 80 percent power)

Sample per arm n is about 16 x p x (1 - p) / d squared, where p is the baseline rate and d is the absolute lift to detect.

Example: p = 0.03, relative lift 20 percent, so d = 0.006. n = 16 x 0.03 x 0.97 / 0.000036, about 12,900 per arm.

Duration in weeks = (n x number of arms) / eligible units per week. Count only units that reach the changed element, not total traffic.

## Averages (revenue per visitor, order value)

n is about 16 x sigma squared / delta squared, where sigma is the standard deviation and delta is the absolute difference to detect.

## Several variants

Use 0.05 / (number of variants) per comparison against control (Bonferroni). Sample per arm grows accordingly.

## Unequal split

Total sample grows by 1 / (4 x w x (1 - w)), where w is the control share: 70/30 costs 1.19 times, 80/20 costs 1.56 times, 90/10 costs 2.78 times.

## When not to test

- Fewer than about 400 conversions a month on the primary metric: only very large lifts (30 percent or more) are detectable in four weeks.
- Legal or security fixes, and broken experiences: just fix them.
- Changes you would ship anyway whatever the result.

## Readout rules

- Fixed horizon by default: read once, at the planned sample.
- Planned interim looks: stop early only if p is below 0.001, and use 0.05 at the end.
- Never extend a flat test "until it gets there". Plan a new, larger test or a bolder change instead.
- Report absolute and relative lift together: "15 percent" on a 4.0 percent baseline means 4.6 percent.
- One primary metric. With five metrics and no correction, the chance that at least one is significant by luck is about 23 percent.
- Sample ratio mismatch (the split differs from the plan beyond chance) invalidates the readout until it is explained.
- If one account holds many users, randomise and analyse by account.
- Changing the variant, split or audience mid-run starts a new experiment with a new key.

## Practical significance

A statistically significant lift smaller than the smallest lift worth shipping is a "do not ship". Write both numbers.
