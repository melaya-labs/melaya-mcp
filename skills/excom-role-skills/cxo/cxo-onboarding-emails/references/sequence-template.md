# Default onboarding sequence

| Email | Trigger | Goal | Suppressed when |
|---|---|---|---|
| Welcome | Email verified | Do the first step of the activation path | Already done |
| Unblock | No engine or setup after 1 day | Finish the one setup step that blocks value | Setup done |
| First success | Setup done, no success after 2 days | Run a validated template | First success |
| Second step | First success, days 4 to 6 | One adjacent step (another surface or integration) | Already used |
| Habit | Days 7 to 10 | Save or schedule one workflow, set approvals | Saved or scheduled |

## Paying customer variant

| Email | Trigger | Goal |
|---|---|---|
| Welcome | Subscription started | Their plan's limits, support level, the first step |
| Week-one check | 7 days after start, no success | One precise fix from their own usage |

## Writing rules

- One goal and one link per email.
- Subject names the outcome ("your first workflow in 10 minutes"), not "Welcome to our newsletter".
- Three to six lines, plain text, the user's language and register.
- Point to the same next step as the in-app guidance.
- No prices except in the paying-customer welcome, quoted from the pricing note.

## Principles

- Time to value first: remove steps before adding emails.
- Do, don't show: link to the action, not a tour.
- Respect the no: an easy unsubscribe in every email.

## Measures

- Activation within 7 days by email received versus not received.
- Unsubscribes and replies per email.
- Change one thing at a time.
