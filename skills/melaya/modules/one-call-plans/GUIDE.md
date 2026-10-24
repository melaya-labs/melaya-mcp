<!-- Module of the melaya skill. Entry point: ../../SKILL.md -->
> Use when: a device task repeats the same kind of action many times or is long enough that one call per click would be slow: entering a table of records into a desktop app or a spreadsheet, filling the same web form for N rows, renaming or organising many files, drawing a diagram or picture from data in a canvas or whiteboard app, a repetitive admin flow in a desktop or web UI, or the same phone flow for a list of items. Covers the one-call method (read and calibrate, plan offline in code, preview, store the plan and run it in ONE call, verify against the expectation, recover from the failed step), choosing single actions vs fast mode vs batch vs stored plans on the computer, browser and phone, the exact step shapes, caps and time model, what runs in the background without taking the user's mouse, verification per surface, a failure table, worked recipes, and the `plankit.py` plan builder. Load the device module first for setup and safety rules (`../devices-computer/GUIDE.md`, `../devices-browser/GUIDE.md`).

# One-call plans: bulk and repeated device work in one call

An agent that clicks one element per tool call spends most of its time on round trips: every step costs a model turn and a network trip. For anything repetitive, Melaya can run the whole job from a plan the agent writes ahead of time: the device executes the list locally, checks each step, and stops at the first surprise. The same method painted the Mona Lisa in Microsoft Paint in one call (1786 steps, 17,386 strokes, 512 s) and enters a 30-row table into a desktop editor in 2.8 s; it works for any window, page or phone screen.

All the device rules still apply unchanged: status first, only allowed apps and sites, never widen access, never type secrets, approvals for send, delete, buy and publish, the user's Stop always wins. A plan goes through exactly the same checks as single actions.

## Pick the tool

| The situation | Use |
|---|---|
| Unknown or unread screen, sign-in, secure field, file dialog, or each result decides the next step | Single actions (`melaya_computer_click`, `melaya_browser_type`, `melaya_phone_click` ...) |
| You read the screen and can name the next 2 to 30 steps by their visible labels | Fast mode inline: `melaya_computer_fast`, `melaya_browser_fast`, `melaya_phone_fast` with `steps` |
| The same steps by label for many rows or pages (forms, lists, loops), each step should be re-found and checked | Fast mode with a stored plan (`plan`), up to 100 steps per call on browser and phone, 500 on the computer; `for_each` for list rows |
| Exact steps by ref or coordinates at high volume (hundreds to thousands), pointer drawing, keys held across steps, or the fastest possible execution | `melaya_computer_batch` with a stored plan: up to 5000 steps, 10 minutes per call |
| A short fixed browser sequence on one page you just read (navigate then read, focus type submit) | `melaya_browser_batch`, at most 20 steps, refs from the latest `melaya_browser_screen` |
| A short exact phone sequence (open an app, two known screens) | `melaya_phone_batch`, at most 25 steps |
| Strokes only (signature, drawing, slider) | `melaya_computer_path` (or `path` steps inside a batch) |

Store the plan whenever the list is longer than about 30 steps or will be reused: a long list written into the call is slow to start (every step is generated as tool-call text), a stored plan starts at once. Inline is fine for short lists.

## Caps

| Tool | Steps per call | Time per call | Notes |
|---|---|---|---|
| `melaya_computer_batch` | 5000 | 10 minutes | 120,000 path points per batch; long runs return a `run_id` |
| `melaya_computer_path` | 200 strokes, 20,000 points | 9 minutes | |
| `melaya_computer_fast` | 500 | 15 minutes (`budget_s` 5 to 900, default 120) | loops of 200 rows |
| `melaya_browser_fast`, `melaya_phone_fast` | 100 (15 inside a `for_each`) | 15 minutes (`budget_s`, default 120) | loops of 200 rows, `collect` up to 500 items; a phone run still going after about 50 s returns a `run_id` |
| `melaya_browser_batch` | 20 | short (one call's wait) | also enforced on stored plans |
| `melaya_phone_batch` | 25 | short | enforced when the plan runs: `melaya_phone_plan` saves a longer list without a warning, then the run is refused ("At most 25 steps per batch") |
| Stored plan | 2 MB per plan, 20 saved plans per account, kept 7 days (up to 30) | | `plan: {file}` needs the runner or desktop app online on that computer |

`max_steps` (1 to 30, default 8) on the fast tools limits only `goal` mode; a `steps` list is limited by the caps above. Over a cap, split the plan into several calls (`plankit.chunk`), each ending at a natural boundary (a whole record, a whole page).

## The method (every surface)

1. **Read and calibrate.** Read the window or page once (`melaya_computer_screen` / `find`, `melaya_browser_screen`, `melaya_phone_screen`). Resolve every target once: a stable label, a ref for this page load, or measured coordinates for canvases. Pick an anchor that proves you are in the right place and never changes during the run (a window title or heading you control, a field label, Paint's palette strip). Probe anything uncertain with a 2 or 3 step call before writing the full plan: line breaks, background delivery, whether a widget keeps a typed value. Write what you measured to a file next to the job.
2. **Plan offline in code.** Generate the whole step list from the data (rows, records, shapes) with a small script, never by hand: `references/plankit.py` builds steps for every tool, groups each record's steps, splits at the caps, estimates the time. Start the plan with a guard step that proves the anchor (an `expect` on the computer, an `expect` with `text` or `url_contains` in fast mode), so a plan started in the wrong place fails at step 1 with no effect.
3. **Preview.** Tell the user what will happen before acting: how many records and steps, the estimated time, how many calls, whether it takes the mouse (foreground) or runs in the background, and which steps commit anything (those wait for their approval). `plankit.preview` prints it. For drawings, show a simulation (paint-artist does).
4. **Store and run in ONE call.** Write the plan to `~/.melaya/plans/<name>.json` on the user's computer (`plankit.write_plan`; the runner or the desktop app reads that folder) and call the tool with `plan: {"file": "<name>.json"}` and nothing else in the list (`steps: []` or no `steps`). Equivalent: `melaya_<surface>_plan` `action: "save"` (with `source: {file}` or the steps) returns an id for `plan: {"id": "pl_..."}`; an https URL works as `plan: {"url": ...}`. A plan file is the step array, or `{"surface", "kind", "steps": [...], ...other arguments of that tool}`; `surface` and `kind` must match the tool. Long runs return `running` with a `run_id`: call the same tool again with only `run_id` (computer batch: `steps: []` + `run_id`) until the result arrives.
5. **Verify against the expectation, not the tool's own report.** Read the result back and compare it with the data: `get_text` or `read_table` on the computer, the page's field values or text in the browser, the screen or `collect` on the phone, a screenshot scored against a target for drawings. Per-step checks can all pass while the end state is wrong (a widget clears a value when focus leaves). `plankit` has `diff_lines`, `diff_flat`, `diff_rows`, `diff_fields`.
6. **Recover from the failed step.** On a failure, read the window or page first. A batch stops at the first failed step (unless that step says `onError: "continue"`) and names it; fast mode stops at the first step that does not resolve or does not take effect and returns the screen. Fix the cause, then run a plan that starts at the failed step (`steps[n:]`), never the whole plan again: steps before it already took effect. A computer batch or path stopped by `user_interrupted` returns a `resume_from`: pass it back with the same plan (if your client still shows a schema without `resume_from`, reconnect the MCP server to reload the tool list, or call again with `steps[n:]`). The phone tools have no `resume_from`: write the remainder as a new plan (with a fresh guard step first) and run that. Both phone tools name the failed step from 1 ("step 3 of 21 (click_text) failed", "Step 11 ... nothing on this screen matches"), so the remainder of failed step N is `steps[N-1:]`.

## Step shapes (exact)

**Computer batch** (`melaya_computer_batch`, also the plan file's `steps`): contract actions, camelCase keys.

| Kind | Shape |
|---|---|
| target | `{ref: "@e12"}` (this snapshot only), `{label, role?, near?, nth?}`, or `{x, y}` (last resort) |
| `type` | `{kind: "type", target?, text, clear?}`; line breaks go inside `text` ("\n"); never `submit` in a bulk plan |
| `set_value` | `{kind: "set_value", target, value}` (cells, number boxes, dates, a whole document) |
| `click` | `{kind: "click", target, button?, count?: 1-3, modifiers?}` |
| `press` | `{kind: "press", keys: "Tab", repeat?}` |
| `select`, `toggle` | `{kind: "select", target?, option? or menuPath: [..]}`, `{kind: "toggle", target, state?}` |
| `scroll`, `wait` | `{kind: "scroll", direction, amount?, target?}`, `{kind: "wait", ms?, until?: {appears?, disappears?, windowChange?}, timeoutMs?}` |
| `expect` | `{kind: "expect", condition: {appears? , disappears?, value?: {target, equals? or contains?}, enabled?, windowTitleContains?, idle?}, timeoutMs?}` (default wait about 3 s) |
| pointer | `{kind: "mouse", target: {x, y}, state: "down" or "up"}`, `{kind: "move", x, y}`, `{kind: "path", strokes: [[[x, y], ...]], speed?, stepPx?, strokeGapMs?, curve?}` (camelCase only: `step_px` is rejected inside a batch) |
| reads | `get_text`, `read_table`, `screenshot`, `find`, `current_app` can be steps too |
| on every step | `delivery?: "auto" or "background" or "foreground"`, `expect?: {condition}` checked after the step, `onError?: "stop" or "continue"`; `handoff` and `keep_awake` cannot be steps |

**Fast mode** (`melaya_computer_fast`, `melaya_browser_fast`, `melaya_phone_fast`): plain-word steps with the labels you read.

| Step | Shape | Surfaces |
|---|---|---|
| click | `{do: "click", target: "Save", near?, ref?, optional?}` | all |
| type | `{do: "type", into: "Email", text, submit?}` | all |
| select | `{do: "select", into: "Country", option: "France", ref?}` | computer, browser |
| pick | `{do: "pick", into: "Tags", options: [..]}` (multi-select, tag inputs) | all |
| press, scroll, wait | `{do: "press", key: "Tab"}` (phone keys: Enter, back, home, recents), `{do: "scroll", direction, times?}`, `{do: "wait", ms}` | all |
| expect | `{do: "expect", text?, url_contains?}` (browser: tab URL; computer: app id or window title; phone: app id). On the phone it waits up to about 4 s for the text, and the text is matched as a substring | all |
| read, collect | `{do: "read", max_chars?}`, `{do: "collect", role?, name_contains?, href_contains?, in?, max?, scroll_max?}` | all |
| for_each | `{do: "for_each", target? or name_contains / role / rid, in?, if?, if_row_contains?, max?, texts?, steps: [...]}` (no nesting, 15 inner steps) | all |
| open, back, visit, upload | `{do: "open", url}`, `{do: "back"}`, `{do: "visit", href_contains, max?, steps?}`, `{do: "upload", into?, file}` | browser (`back` on phone too) |
| draw | `{do: "draw", strokes, speed?, curve?, relative_to?}` | computer |

`for_each` walks rows that are on the screen, not a list of values you hold: for a list of values (expressions, names, records), write the steps once per value in code. A `for_each` that matches no row still reports `completed`, with `0 done` in its step line: read that count.

Tool arguments that can sit in the plan file: `budget_s`, `done_url`, `done_text`, `humanize`. `allow_commit` and the device choice (`computer_id`, `agent`) never come from a plan: pass them in the call.

**Browser batch** (`melaya_browser_batch`, max 20): `{do, args}` with `do` one of navigate (`url`), click (`ref`), tap (`x`, `y`), input_text (`ref`, `text`, `submit?`), press_key (`key`), scroll (`direction`, `amount_px?`), select_option (`ref`, `values`), submit (`ref`), get_screen_tree, get_text (`ref?`), screenshot, back, forward, wait (`ms`). Refs are valid only for the page load you read them from.

**Phone batch** (`melaya_phone_batch`, max 25): `{do, args, expect?, settle_ms?}` with `do` one of open_app (`app` package), click_text (`text`), click_id (`id`), input_text (`text`), paste (`text`), clear_text, press_enter, tap / double_tap / long_press (`x`, `y`), swipe (`x1`, `y1`, `x2`, `y2`), scroll (`direction`, `amount?`), home, back; `expect` holds one of `{app}`, `{text_visible}` or `{editable_focused: true}`. There is no wait step: `settle_ms` (0 to 3000, default 300) waits after a step. Two behaviours to plan around:

- The `expect` is checked right after the action, before `settle_ms`. A value that shows up a moment later (suggestions, a computed result, a search count) fails the check even with `settle_ms: 2000`. Type with a settle, then repeat the same `input_text` (it sets the same text again, nothing changes on screen) with the `expect` on that second step (`plankit.p_input_checked`).
- `text_visible` matches a substring: `"= 10"` passes on a screen that shows `"= 1000"`. Check expected texts against each other with `plankit.expect_collisions` and lengthen the ones that collide, or verify those values from a read.

`input_text` replaces the field's text (no `clear_text` needed before it). The phone fast tools have no `open` step: open the app first (`melaya_phone_open`, or `open_app` in a batch), then run the fast plan with an `expect` on the app id as its first step.

## Background or foreground

Prefer runs that leave the user's mouse and keyboard alone, and say before the run which kind it is.

| Surface | Runs in the background (user keeps working) | Needs the foreground (takes the mouse and focus) |
|---|---|---|
| Computer | typing into native fields and documents, `set_value`, clicks on buttons, tabs and menu items that the app exposes as controls, window minimize / restore, reads | key chords with Ctrl, Alt or Shift (refused with "need real keyboard input" when `delivery: "background"`), pointer drawing and drags (`path`, `mouse`, `move`), dropdowns and popups that only open on a real click (Paint's Brushes menu), canvas apps |
| Browser (extension) | everything: the agent works in its own tab, even a background tab; the user's visible tab and window never change | nothing on the user's screen |
| Phone | everything happens on the phone; the computer is untouched | the phone's screen must be awake and unlocked (`melaya_phone_wake`). It locks after about a minute with no step (long `wait` steps let it sleep), and the user may switch apps mid-run, so start every phone plan with an `expect` on the app id |

On the computer, write `delivery: "background"` on the steps that must not take the mouse: such a step fails instead of grabbing the cursor, and you learn it in the probe. `"auto"` (the default) tries background first and falls back to foreground. A foreground run needs the user's agreement first; keep it short, minimise other windows of the same app, and tell them that touching the mouse or keyboard pauses the run (it re-checks the window and resumes) and that Ctrl+Alt+End (Control+Command+Esc on a Mac) stops it.

Pin `window_id` when the whole run stays in one window; leave it out when the run opens menus, dropdowns or dialogs, which are separate windows (a pinned window made Paint's tool switches miss).

## Verify, per surface

| Surface | Read back with | Watch out for |
|---|---|---|
| Computer, text | `melaya_computer_get_text` on the document or field; an `expect` with `value` as the plan's last step | some editors return the value without its line breaks: compare with line breaks removed plus the character count (`plankit.diff_flat`) |
| Computer, grids and lists | `melaya_computer_read_table` (`max_rows`, `columns`) | compare by key column (`plankit.diff_rows`) |
| Computer, canvas | a screenshot compared with a target or simulation | paint-artist scores it (Lab dE) |
| Browser | the batch's step report (from the next server deploy: ok / FAILED / not run per step, `detail: true` for all; a typed value the field did not keep is FAILED), the final screen (text inputs show `="value"`), `melaya_browser_get_text`, a screenshot for selects, checkboxes, radios and widgets that the element list does not show (needs a browser extension update to show them) | per-step checks passing does not prove the end state |
| Browser, submitted data | the destination itself: the list page, the confirmation, the sheet the form feeds | read it after the run, not the form |
| Phone | the `read` steps' text (returned under PAGES, one entry per read), `melaya_phone_screen`, a `collect` by `rid` over the list, the app's own list or sent items | a `read` is a snapshot: a value that arrives late is missing from it although the run says `completed` (put a fast `expect` with the value before the read, it waits). A read that returns 0 characters from app `unknown` means the screen went off or an app that is not allowed came to the front (`melaya_phone_current_app` tells which). Chrome on the phone does not expose web page content to the screen read on every device (only its toolbar and menus): read such pages with `melaya_phone_screenshot` |

Report: records done, steps, the real duration from the result, background or foreground, the verification outcome with the first mismatch if any, and anything that waited for or was refused an approval.

## Time model

Measured live (2026-10-24): computer batch typing in the background about 0.08 s per step (35 steps in 2.8 s); Paint 17,386 strokes in 512 s (about 0.0245 s per stroke plus ink length / speed); browser fast: open a page 4.6 to 5.2 s, type 1.0 to 2.0 s, select 2.0 to 2.7 s, a click that changes the page about 3 s, read 1.2 to 1.4 s; browser batch about 1 s per step; phone batch about 0.3 s per step plus its `settle_ms` (300 ms by default; 21 steps with ten 1.2 s settles in 20.8 s); phone fast: type 0.5 to 1.4 s (up to 2 s), `wait` its ms plus 0.3 s, read 0.25 to 0.45 s, `expect` 0 s when the text is already there (up to about 4 s when it waits), collect about 0 s. A phone batch result gives no duration (time it yourself); phone fast reports one. Add about 3 s of call latency per call. `plankit.estimate` uses these numbers; time one real run of your app and pass your own costs.

## Failure table

| Symptom | Cause | Fix |
|---|---|---|
| The plan typed into the user's own document or tab | No guard; the app restored the user's tabs or windows and one of them was in front | Open your own window or tab, start the plan with an `expect` on an anchor you control, pin `window_id` |
| The guard fails after the first row | The anchor changed: the editor renamed its untitled tab after the first line typed | Anchor on text you write yourself (a header line), not on "Untitled" |
| `windowTitleContains` passes in the wrong place | Desktop helper 1.2.1 and older (Windows, macOS) match any window's title | Needs desktop helper 1.2.2 (next desktop app after 0.1.5; Linux already checked the target): it then checks only the window the step acts in (the step's `window_id`, else the batch's, else the window in front). Until then use a title text unique to your window |
| A chord step fails with "need real keyboard input" | Ctrl, Alt or Shift chords cannot be sent in the background | Use `set_value` (a whole value, or `""` to clear), or a foreground step with the user's agreement |
| An approval card for every row | `submit: true` or an Enter press commits in safe mode | Put line breaks inside the typed text, move between fields with Tab or labels; commit once at the end with the user's yes |
| A fast step returns `ambiguous` | A label and its control share the same name | Fixed in the next server deploy for `select` and `pick` (the control wins over its label); for `click` add `ref` (from the screen you read) or `near` |
| A browser batch is refused over 20 steps | The 20-step cap applies to stored plans too | Use `melaya_browser_fast` with a stored plan, or split |
| A stored plan is accepted, then refused at run for its size | Saving checked only the shape | Fixed in the next server deploy: saving refuses a plan over its tool's cap (browser batch 20, phone batch 25, fast 100, computer fast 500, computer batch 5000, path 200 strokes) and names the kind that takes it |
| A phone batch `expect` fails although the text shows a moment later | The phone app checks `expect` right after the action, before `settle_ms` | Fixed in the next server deploy (MCP `melaya_phone_batch`): the check runs after the step's `settle_ms`, so give `settle_ms` for slow results. With phone app 1.1.1 + server deploy the phone also re-checks it for up to 4 s after the settle; on an older app it is one check |
| `text_visible` passes on a longer text ("= 10" on "= 1000") | It is a substring match on the phone | With phone app 1.1.1 + server deploy: add `match: "exact"` (an element's whole text) or `match: "word"` (whole words) to the `expect`; an older app gets the batch refused (`app_update_required`) instead of a substring match. Phone fast `expect` takes the same `match` (checked on the server). Until then expect a text that is unique on the screen |
| A phone batch failure says "Nothing changed on the device", counts steps from 0, shows no screen | The failure text ignored what the phone reported | Fixed in the next server deploy: the failed step numbered from 1, the steps that ran, the time and the screen at the end; a staged approval inside the batch reads PENDING APPROVAL. With phone app 1.1.1 + server deploy it also says per step whether the screen changed ("Screen changed after: 1 open_app yes, 2 tap NO") |
| Phone fast says `completed` though a `read` returned nothing or a `for_each` matched no row | Empty and failed reads were not checked | Fixed in the next server deploy: an unreadable or empty read and a failed read after a `wait` end the run with `error`; a `for_each` with no row ends with `no_progress` unless it says `optional: true` |
| The phone screen reads `app=unknown nodes=0` | The phone refused the read: another app in front, the lock screen or shade, or accessibility off | Fixed in the next server deploy: the read fails with `app_not_allowed`, `locked`, `shade_open` or `accessibility_off`; `melaya_phone_status` reports `locked` and agrees with `melaya_phone_devices` on `online` |
| Refs fail after `open` or navigation | Refs belong to one page load | Labels in fast mode for reusable plans; refs only right after a read |
| A date or widget field is empty at the end although its step passed | The widget drops a typed value when focus moves on (browser extension: typing into `<input type=date>`) | From the next server deploy browser batch and type report it (FAILED: the field shows no value after typing). Pick from the widget (its calendar or list), fill it last, verify the end state, otherwise ask the user |
| Read-back has no line breaks | Windows editors (Notepad) end lines with a lone CR, which clients show as nothing | Fixed in the next server deploy for `get_text` and clipboard reads (a lone CR becomes a line break, the count is unchanged, the result says how many lines); the per-step "Field now" echo needs desktop helper 1.2.2. Until then compare flat text and the character count (`plankit.diff_flat`) |
| Control jumps to another tab after closing yours | Closing your tab hands control to another tab | Fixed in the next server deploy: the close returns a confirmation only, and nothing reads or acts until you open (`melaya_browser_tabs` action `open`) or switch to a tab. Before that deploy, stop right after (`melaya_browser_stop` with your `agent`) |
| A batch says "1 failed and continued" but stopped ("N step(s) were not run") | Desktop app 0.1.5 counted the stopping step as continued | Fixed in the next server deploy (and the next desktop app); the stopping step is the one named first |
| Slow to start | A long plan written inline | Store it (`plan: {file}` or `{id}`) |
| Result says `running` | Long run | Call again with only `run_id` until the summary |
| Stops near 10 minutes or is refused for size | Over a cap | Split with `plankit.chunk` at record boundaries |
| Run paused midway | The user touched the mouse or keyboard during a foreground run | It resumes by itself after re-checking the window; ask them to keep off |
| A stroke resized the canvas or window | It started on a resize handle at an edge | Keep 5 px or more away from canvas and window edges |
| Phone batch `batch_expect_failed` on a step whose value is on the screen right after | The check ran before `settle_ms` and the value came a moment later | Repeat the same `input_text` with the `expect` (`plankit.p_input_checked`), or use phone fast, whose `expect` waits |
| A phone check passed on the wrong value | `text_visible` and fast `expect` match substrings (`"= 10"` inside `"= 1000"`) | `plankit.expect_collisions` before the run; longer expected texts; verify those values from a read |
| A phone batch error says "Nothing changed on the device" | The message is generic: the steps before the failed one did take effect, and so did the failed step's action when its `expect` failed | Read the screen, then run the remainder from the failed step |
| Phone fast `low_confidence` "nothing on this screen matches" | The target is not on this screen (wrong label, or the app moved on) | Read the returned screen; fix the label; run the remainder as a new plan |
| Phone fast `no_progress` at step 1 with another app named | The user switched apps, or a previous step left another app in front; the guard stopped the run with no effect | Wait until the user is done, bring your app back, re-run the same remainder |
| A phone read returns 0 characters from app `unknown` and the run says `completed` | The screen locked during the run (about a minute without a step), or the user opened an app that is not allowed | `melaya_phone_current_app`, then `melaya_phone_wake`; on `locked` ask the user to unlock; re-run the reads; keep `wait` steps short |
| "The phone did not answer within N seconds" | The phone is locked or asleep (with a small `budget_s` this comes fast) | `melaya_phone_wake`; `locked` means only the user can fix it |
| `app_not_allowed` on `open_app` | The app is not on the user's allow-list (often Calculator, Notes, Settings) | Pick an allowed app, or ask the user to allow it in Device Control; never work around it |
| `shade_open` on a phone action | The notification shade was open (the user pulled it, or an approval opened it); the tool closed it and did nothing | Retry the same action once, after a read |
| A phone click by resource id returns `not_clickable` | The node reports clickable but ignores the accessibility click (Chrome's menu button) | `melaya_phone_click` with `mode: "tap"`, or `click_text` on its label |
| `not_allowed`, `tier_denied`, `approval_denied`, `stopped` | The user's settings or decision | Tell the user; never route around it |

## Recipes

Each recipe follows the method: probe 2 or 3 steps, build with `plankit`, preview, store, one call, verify, recover from the failed step. Import with `sys.path.insert(0, "<skill>/modules/one-call-plans/references")` then `from plankit import *`.

### 1. A table of records into a desktop editor or spreadsheet

Open your own document (a new tab or window), read it, probe line breaks and background typing with two rows.

```python
rows = read_records("orders.csv")
ED = T(label="Text editor", role="document")          # from melaya_computer_screen
HEADER = "ORDERS IMPORT 2026-10-24"                    # the anchor: becomes the tab title
steps = [c_expect(windowTitleContains="Untitled"),
         c_type(HEADER + "\n", target=ED, clear=True, delivery="background"),
         c_expect(timeout_ms=3000, windowTitleContains=HEADER)]
steps += [c_type("\t".join(r.values()) + "\n", target=ED, delivery="background",
                 expect={"windowTitleContains": HEADER}) for r in rows]
print(preview(steps, "computer", "batch")); write_plan("orders_import", steps, "computer", "batch")
# melaya_computer_batch {"steps": [], "plan": {"file": "orders_import.json"}, "window_id": "<yours>"}
# verify: melaya_computer_get_text -> diff_flat([HEADER] + lines, text, reported_chars)
```

For a spreadsheet grid, probe first whether the cells take `set_value` or typing in the background; write one `set_value` per cell (target by the cell's name as the screen lists it) or type a row with Tab between cells, then verify with `melaya_computer_read_table` and `diff_rows(rows, table, key="id")`.

### 2. The same web form for N rows

Read the form once, write steps by label, group each record so a split never cuts a record.

```python
steps = []
for i, r in enumerate(read_records("leads.csv")):
    g = [f("open", url=FORM_URL), f("expect", text="Contact us"),
         f("type", into="Name", text=r["name"]), f("type", into="Email", text=r["email"]),
         f("select", into="Country", option=r["country"], ref="@e16"),   # ref when a label is ambiguous
         f("click", target="Submit")]                                      # commit: needs allow_commit and the user's yes
    steps += [dict(s, _group=i) for s in g]
for path in write_plans("leads_form", steps, "browser", "fast", args={"budget_s": 600}):
    print(path)   # one melaya_browser_fast call per file: {"agent": "<id>", "plan": {"file": "leads_form_1.json"}, "allow_commit": true}
```

Without the user's yes to submit, leave the Submit step out and stop after the fields. Verify on the destination (the list of submitted entries, the sheet behind the form), with `diff_rows`. For one record on a page you just read, `melaya_browser_batch` with refs is enough (20 steps).

### 3. Renaming or organising many files in Explorer or a file dialog

Read the folder's list with `melaya_computer_read_table`, compute the new names in code, probe the rename on two files. A rename that ends with Enter commits and may ask for approval per file; Explorer also commits a rename with Tab and opens the next file for renaming, which chains without Enter (probe it). Moves and deletes always go through approvals.

```python
files = [r["Name"] for r in table_rows]                    # from read_table, in the list's order
new = ["%s_%03d.pdf" % (prefix, i + 1) for i in range(len(files))]
steps = [c_expect(windowTitleContains=FOLDER_NAME), c_click(T(label=files[0], role="listitem")), c_press("F2")]
for i, n in enumerate(new):
    steps.append(c_type(n, clear=True))
    if i < len(new) - 1:
        steps.append(c_press("Tab"))                       # commits this name and opens the next file for renaming
write_plan("rename_batch", steps, "computer", "batch")
# verify: read_table again, diff_rows([{"Name": n} for n in new], table, key="Name")
```

Never rename or move the user's files without a clear list they agreed to.

### 4. A diagram or picture from structured data in a canvas or whiteboard

Calibrate the canvas origin and scale from a screenshot (an anchor that never changes, like a palette strip or the canvas corner), convert the data to strokes in canvas coordinates, keep clear of the edges, run as `path` steps in one batch (foreground: it moves the pointer).

```python
nodes = {"A": (100, 80), "B": (320, 80), "C": (210, 240)}; edges = [("A", "B"), ("B", "C"), ("C", "A")]
ox, oy = 690, 239                                       # measured canvas origin on screen
box = lambda x, y: [[ox + x - 40, oy + y - 20], [ox + x + 40, oy + y - 20], [ox + x + 40, oy + y + 20], [ox + x - 40, oy + y + 20], [ox + x - 40, oy + y - 20]]
strokes = [box(*p) for p in nodes.values()] + [[[ox + nodes[a][0], oy + nodes[a][1]], [ox + nodes[b][0], oy + nodes[b][1]]] for a, b in edges]
steps = [c_path(strokes[i:i + 200], speed=2000, step_px=2, stroke_gap_ms=10) for i in range(0, len(strokes), 200)]
write_plan("diagram", steps, "computer", "batch")
# melaya_computer_batch {"steps": [], "plan": {"file": "diagram.json"}} with no window_id; then screenshot and compare
```

Browser whiteboards (Miro, Figma, Excalidraw) are drawn the same way through the computer (the browser window is the canvas), or with the app's own shape tools and text fields in fast mode. Full painting with colours, tools, simulation and scoring: the paint-artist skill (`../../../paint-artist/SKILL.md`), the advanced example of this method.

### 5. A repetitive admin flow in a desktop or web UI

Approve, tag, archive or update many list rows: one fast call with `for_each`, a condition per row, and the inner steps.

```python
steps = [f("expect", text="Requests"),
         f("for_each", target="Open", if_row_contains="Pending", max=50, **{"in": "@e40"},   # the list's ref
           steps=[f("select", into="Status", option="In review"), f("click", target="Save"), f("back")])]
write_plan("triage", steps, "browser", "fast", args={"budget_s": 600})
# melaya_browser_fast {"agent": "<id>", "plan": {"file": "triage.json"}}; then collect the list again and compare
```

The computer equivalent is `melaya_computer_fast` with the same steps (`in` = the list's ref from `melaya_computer_screen`). Rows whose approval card the user rejects are skipped and reported.

### 6. The same phone flow for a list

Check `melaya_phone_status` (online, app allowed; `melaya_phone_apps` lists every installed app with its `allowed` flag) and the app's playbook, `melaya_phone_wake` if the phone was idle, open the app, read the screen, then one fast call for the whole list. Messages and posts always stop on the phone's approval card. The user may be holding the phone: a guard `expect` on the app id at the start of every plan stops a run with no effect when they switched apps.

```python
contacts = ["Ana", "Ben", "Chloe"]
steps = [f("expect", url_contains="com.whatsapp")]
for name in contacts:
    steps += [f("click", target="Search"), f("type", into="Search", text=name), f("click", target=name),
              f("read", max_chars=600), f("back"), f("back")]
write_plan("phone_round", steps, "phone", "fast", args={"budget_s": 600, "done_url": "com.whatsapp"})
# melaya_phone_fast {"plan": {"file": "phone_round.json"}}; verify from the reads and the final screen
```

Values typed into a field and read back (a lookup, a converter, a search box that shows an answer), one value per row of the list. Type, `expect` the answer (it waits for it), then read, so the read never catches the screen before the answer:

```python
rows = read_records("values.csv")                         # columns: input, expected
assert not expect_collisions([r["expected"] for r in rows])
steps = [f("expect", url_contains=APP_ID)]
for r in rows:
    steps += [f("type", into=FIELD_ID, text=r["input"]), f("expect", text=r["expected"]), f("read", max_chars=300)]
write_plan("phone_values", steps, "phone", "fast", args={"budget_s": 300, "done_url": APP_ID})
# melaya_phone_fast {"plan": {"file": "phone_values.json"}}; parse every PAGES entry, diff_rows(rows, parsed, key="input")
```

For an exact short sequence with fixed ids, `melaya_phone_batch` (25 steps) with an `expect` on the steps that matter; for late values use `p_input_checked(text, expected)`, which adds the second, checking step. A phone job that should keep going after the chat belongs to `melaya_run_phone_agent` or a pipeline (`../devices-browser/GUIDE.md`).

## Reference runs (2026-10-24)

| Job | Tool and plan | Result |
|---|---|---|
| 30-row table (plus header and column line) into a new Notepad tab | `melaya_computer_batch`, stored plan, 35 steps (32 type, 3 expect), all `delivery: "background"` | 2.8 s, the user's mouse untouched; read back with `get_text`: identical text, 938 characters as expected; re-running the plan stopped at its guard with nothing typed |
| Public test web form, one record | `melaya_browser_batch`, stored plan, 9 steps by ref | text, textarea, select, datalist, checkbox and radio correct; the date widget empty at the end (see the failure table) |
| Same form, two records by label | `melaya_browser_fast`, stored plan, 18 steps | stopped at step 4 (`ambiguous` select); fixed with `ref` and resumed from step 4 in one call: 15 steps completed in 25.4 s; date widget again empty at the end, caught by the end-state check |
| Mona Lisa in Paint | `melaya_computer_batch`, stored plan, 1786 steps (path, mouse, move, set_value, click) | 512 s, foreground, Lab dE 6.30 vs the original |
| 10 expressions typed into Chrome's address bar on an Android phone, answers checked (nothing submitted) | `melaya_phone_batch`, stored plan (saved with `melaya_phone_plan` for an id, then as a file), 21 steps (guard + 2 per value) | First version (one `input_text` with `expect` and `settle_ms` 800) stopped at step 2: the check runs before the settle. Second version (`p_input_checked`): all 21 steps and 10 checks passed, 20.8 s wall, no duration in the result |
| 15 expressions, each typed then read back | `melaya_phone_fast`, stored plan, 47 steps (guard, 15 x type + wait 1000 + read, collect) | `completed` in 39.1 s (46.4 s wall); all 15 values in the reads matched (`diff_rows`) |
| Recovery: the same flow with a missing target at step 11 | `melaya_phone_fast`, stored plan, 20 steps | `low_confidence` at step 11 after 10 steps (10.3 s); the remainder as a new plan stopped at its guard (the user had opened another app), ran once the app was back: 10 steps in 11.2 s, but one read lacked its answer (1 s wait too short) while the run said `completed`; a type + `expect` + read version waited for it |
| Recovery in a batch: missing target at step 2 | `melaya_phone_batch`, 4 steps inline | `step 2 (click_text) failed: not_found ... Nothing changed on the device`, yet steps 0 and 1 had changed the field; resumed with the remainder in one call |
| Long fast run | `melaya_phone_fast`, 8 steps with 60 s of waits | returned `running (run_id ...)` after 50 s; a call with the `run_id` got the result, but the screen had locked: the last read returned 0 characters from app `unknown` and the run said `completed` |

## Definition of done

- [ ] The device module's status and safety checks done; only your own window or tab was touched.
- [ ] The probe confirmed delivery, line breaks and widgets before the full plan.
- [ ] The plan was generated in code, started with a guard, previewed to the user (steps, time, background or foreground, commits), stored and run in one call per cap-sized part.
- [ ] The result was verified against the data, not the step report; the first mismatch is named.
- [ ] Failures resumed from the failed step; nothing that took effect was run twice.
- [ ] What you opened is closed or minimised, test plan files removed, the user told what changed in plain words.
