# Health, Fitness and Food

Health data is scattered across apps that do not talk to each other and companies that may not exist in five years. A vault gives you one place where the workout log, the symptom you noticed in March, the doctor's answer in April, the recipe that fixed your lunches, and the sleep numbers all sit next to each other — and where a Base can show you the pattern. This chapter designs the health records, the training log, nutrition and meal planning, habit tracking, and the quantified-self dashboards, with a realistic view of what to automate and what to type.

## What to keep in the vault (and what not to)

| Keep | Why | Don't keep | Why |
| --- | --- | --- | --- |
| Workout log (sessions, exercises, loads) | Programs need history; apps lose it | Second-by-second HR/GPS data | Belongs in the fitness app; link the activity URL |
| Symptoms, appointments, medications, lab results (summaries) | Timeline for you and your doctor | Full DICOM/imaging | Store files elsewhere; link |
| Recipes, meal plans, grocery patterns | Reuse and iteration | Every meal's macros | Unless medically required; a nutrition app does it better |
| Sleep hours, mood, energy (daily properties) | The three numbers that explain most weeks | Every wearable metric | Noise |
| Habits (completion) | Behaviour change | Habit *intensity* | Completion is the lever |
| Injuries and rehab protocols | Recur; you forget | | |
| Insurance, providers, records locations | Admin you need under stress | | |

## Folder and types

```text
Health/
├── Workouts/            type: workout      2026-09-06 Strength A.md
├── Log/                 type: health-event symptoms, appointments, meds, labs
├── Programs/            training programs (blocks), rehab protocols
├── Providers/           doctors, clinics (type: person with relationship: professional, or type: provider)
├── Body/                measurements over time (a single note with a table, or weekly-note properties)
└── Health MOC.md
Life/Recipes/            type: recipe
Life/Meal Plans/         weekly plans (or a section of the weekly note)
Life/Habits/             type: habit (only for habits with a why and a plan)
Areas/Health.md          the area note: standard, projects, goals
```

## Training log

One note per session, `type: workout`, from `tpl-workout` (Chapter 11): `date`, `kind` (strength/run/bike/swim/yoga/walk/climb/…), `duration_min`, `distance_km`, `rpe` (1–10), optional `program` (link), `location`, `activity_url` (Strava/Garmin link). Body: an exercise table for strength, splits for endurance, and a one-line "how it felt".

```markdown
| Exercise | Set 1 | Set 2 | Set 3 | Notes |
| --- | --- | --- | --- | --- |
| Squat | 80×5 | 80×5 | 80×5 | felt heavy |
| Bench | 60×5 | 60×5 | 60×4 | |
| Row | 50×8 | 50×8 | 50×8 | |
```

**Exercise history without a database**: for the exercises you care about, add inline fields on the table rows or a summary line: `- squat:: 80×5×3`. A DataviewJS widget in the program note then charts the top set over time:

```dataviewjs
const ex = "squat";
const rows = dv.pages('"Health/Workouts"').where(p => p[ex] && p.date).sort(p => p.date)
  .map(p => [p.file.link, p.date.toFormat("yyyy-MM-dd"), p[ex]]);
dv.table(["Session", "Date", ex], rows);
```

Alternative: keep a `Health/Programs/PRs.md` table updated by hand when a PR happens — often enough.

**Programs**: a `Programs/Strength Block 3.md` note with the plan (weeks × sessions), the rationale, and an embedded Base of its sessions (`program == this`) with `Sum` of duration and a count. When the block ends, a short retrospective at the bottom. The next block links to the previous one.

**Endurance**: `distance_km`, `duration_min`, `avg_hr`, `elevation_m` properties; a weekly Base grouped by `formula.week` with `Sum` of distance and duration is your training volume chart; a formula `pace: (duration_min / distance_km).toFixed(2)` for pace.

**Automation**: Strava/Garmin have no official Obsidian plugins but do have exports and APIs; a small script (Chapter 29) or an n8n/Zapier flow can create a workout note per activity via the CLI (`obsidian create path="Health/Workouts/2026-09-06 Run.md" template=tpl-workout`) and set properties (`property:set`). Apple Health → **Health Auto Export** app → JSON/CSV to a folder → script. For most people, typing five properties after a workout is fine and the friction is part of the reflection.

## Health records and events

`type: health-event` in `Health/Log/`, one per occurrence, `date`, `kind` (symptom/appointment/medication/lab/vaccination/injury/procedure), `provider` (link), `severity` (1–5 for symptoms), `body_part`, `tags`. Body: what happened, what was said, what was decided, follow-ups as tasks.

Why one note per event and not a running log: Bases can then filter "all knee events", "all appointments with Dr. X", "symptoms severity ≥ 3 in the last 90 days" — which is exactly what you want to hand a doctor.

**Medications**: a `Health/Medications.md` note with a table (name, dose, schedule, started, stopped, prescriber, why) plus a health-event note for each start/stop/change. Recurring tasks in `Routines.md` for daily doses if you need reminders (or the phone alarm — honest answer).

**Labs**: a `Health/Labs.md` note with one table per marker over time (date, value, reference range, lab) or one health-event per lab date with the values as properties (`ldl: 2.9`, `hba1c: 5.4`) — the property approach lets a Base chart a marker over time. Attach the PDF report in `Attachments/health/` and link it.

**Providers**: `type: person` with `relationship: professional`, `specialty`, `clinic`, `phone`, `portal_url`; their backlinks list every appointment.

**Injuries and rehab**: a `Health/Programs/Knee rehab 2026.md` note with the protocol, a Base of related workouts and events, and a `## Timeline`. Injuries recur; the note is a reusable playbook.

**Family health**: for children and dependants, a `Health/Family/<Name>/` mirror of the above, or a `person` property on health events. Vaccination records as a table per person.

**Emergency sheet**: `Health/Emergency.md` — blood type, allergies, medications, conditions, emergency contacts, insurance numbers, GP. Export to PDF and keep in your phone's wallet/medical ID too. This note alone justifies the folder.

## Sleep, mood, energy

Three numbers in the daily note (Chapter 15), five seconds each via Meta Bind sliders. Analysis: the Daily Base's monthly averages; the sleep↔mood correlation DataviewJS from Chapter 12; a **Heatmap Calendar** per metric in the yearly note; **Tracker** for line charts over months.

Wearable sleep data: Apple Health / Oura / Whoop exports can set `sleep_h` automatically via a script; or type it from the app each morning — the act of typing keeps you aware.

## Habits

Two mechanisms, pick per habit:

1. **Daily-note checkboxes** with a tag: `- [ ] Meditate #habit/meditate`, `- [ ] 10k steps #habit/steps`. Free, visible, mobile-friendly. Tracking: streak query (Chapter 12), Heatmap Calendar per habit, or a Dataview completion-rate table for the month:

```text
TABLE WITHOUT ID H AS Habit, length(filter(rows.T, (t) => t.completed)) + "/" + length(rows) AS "Done/Days"
FROM "Journal/Daily"
WHERE file.day >= date(som) AND file.day <= date(eom)
FLATTEN file.tasks AS T
FLATTEN T.tags AS H
WHERE startswith(H, "#habit/")
GROUP BY H
```

2. **Habit notes** (`Life/Habits/Meditate.md`, `type: habit`) for habits with a *why*, a cue/routine/reward design, and a monthly review — the note holds the reasoning; the daily checkbox holds the data.

Design rules that the vault enforces: few habits at once (the daily template only has room for 3–5 checkboxes), completion not intensity, monthly review (`## Habits` section in the monthly template embedding the heatmaps), and dropping habits that have become automatic to free the slot.

## Body measurements

Weight weekly (a property on the weekly note, or a `Health/Body/Measurements.md` table), waist monthly, photos quarterly (in `Attachments/health/body/`, embedded in the quarterly note if you like). Daily weight is noise; a Base of weekly notes with `weight` and a `Range` summary is signal.

## Food: recipes

`type: recipe` in `Life/Recipes/`, from `tpl-recipe`: `cuisine`, `course`, `servings`, `prep_min`, `cook_min`, `rating`, `last_made`, `photo`, `source` (URL or book link), `tags` (vegetarian, quick, batch, freezer-friendly, kid-approved). Body: ingredients as a list (one per line — scaling and shopping lists depend on it), numbered method, notes & variations (what you changed, what to try).

Capture: **Web Clipper** with a recipe template that extracts ingredients and steps (Interpreter does this well: "return the ingredients as a Markdown list and the method as numbered steps"); cookbook recipes typed or photographed (photo embedded, key steps typed).

The Recipes Base (Chapter 10): gallery by cuisine, quick weeknight (`total_min <= 35`), not-made-in-60-days favourites (`rating >= 4`). When you cook something, set `last_made` (Bases table cell or the property editor) — that one edit powers the rotation view.

**Scaling**: a Templater snippet or the **Numerals** plugin to multiply ingredient quantities; or keep servings at your household size and skip it.

## Meal planning and groceries

Weekly, in the weekly note (or `Life/Meal Plans/2026-W36.md`):

```markdown
## Meals
| Day | Lunch | Dinner |
| --- | --- | --- |
| Mon | leftovers | [[Shakshuka]] |
| Tue | [[Lentil salad]] | [[Chicken stir-fry]] |
| ... | | |

## Groceries
- [ ] eggs
- [ ] tomatoes
```

A DataviewJS block can generate the grocery list by reading the `## Ingredients` sections of the linked recipes and de-duplicating — a nice 20-line script; or copy-paste ingredients under the list. On the phone, the grocery list is a checklist in the weekly note (mobile toolbar → toggle checkbox). Some people prefer the shared family shopping app for the list itself and keep only the plan in Obsidian; sensible.

**Pantry / staples**: `Life/Home/Pantry.md` list of staples with `- [ ]` for "need to buy"; reset weekly.

**Nutrition tracking**: leave it to a dedicated app unless a clinician asks for it. If you do track, an inline field per meal in the daily log (`[kcal:: 650] [protein:: 40]`) and a Dataview sum is enough for a few weeks of awareness.

## Dashboards

**Health area note** (`Areas/Health.md`):

```markdown
## Standard
Train 3×/week · sleep ≥ 7h avg · resting HR < 60 · annual check-up · dentist 2×/year

## This month
![[Workouts.base#Last 30 days]]
![[Daily.base#Last 30 days]]

## Habits (heatmaps)
(Heatmap Calendar DataviewJS blocks: meditate, steps, alcohol-free)

## Open health items
```tasks
not done
path includes Health
sort by due
```

## Recent health events
```base
filters: {and: [type == "health-event", date >= today() - "90d"]}
views: [{type: table, name: Recent, order: [file.name, date, kind, severity, provider], sort: [{property: date, direction: DESC}]}]
```

## Programs
[[Strength Block 3]] · [[Knee rehab 2026]]
## Records
[[Medications]] · [[Labs]] · [[Emergency]] · [[Health MOC]]
```

**Yearly note health section**: workouts by kind with sums (Base), sleep average by month (Base grouped by `formula.month`), habit heatmaps, weight range, health events count, one paragraph.

## Privacy

Health notes are second only to the journal in sensitivity. Same rules: E2E-encrypted sync only, excluded from Publish/shares, optionally Meld Encrypt for specific notes, or the whole `Health/` folder in a separate encrypted vault if you share your main vault with anyone.

## Anti-patterns

- Logging every metric a wearable offers. Three daily numbers, weekly weight, per-session workout basics.
- Recipes as clipped web pages with 2,000 words of blog preamble. Clip with a template that extracts only ingredients and method.
- Health events buried in daily notes. One typed note per event or the doctor's question ("when did this start?") is unanswerable.
- Habit trackers with fifteen habits. Three to five.
- Never reading the dashboards. Put them in the monthly review template.

## Key takeaways

- Keep summaries, logs and decisions in the vault; keep raw sensor data and images in their apps and link.
- One note per workout with typed properties and an exercise table; programs embed their sessions; PRs tracked by hand or inline fields.
- One note per health event (`kind`, `severity`, `provider`) so Bases can answer the doctor's questions; medications, labs, providers, injuries and an emergency sheet as records.
- Sleep/mood/energy as daily properties; habits as tagged daily checkboxes (heatmaps, streaks) with habit notes only where the why matters.
- Recipes as typed notes with ingredient lists, `last_made` powering rotation views; meal plans and groceries in the weekly note.
- Health and journal share the same privacy rules.

## Next

[Chapter 21: Finance →](21-finance.md)
