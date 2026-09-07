# Templates Library

Every template referenced in the guide, in one place, copy-ready. The core set (daily, weekly, monthly, project, person, book, note, meeting, decision, recipe, workout, inbox, quick task) is in [Chapter 11](11-templates-and-templater.md) with full Templater logic and is not repeated here; this chapter adds the remaining note types, the reusable fragments, the QuickAdd/Meta Bind forms, and a plain (non-Templater) daily note for people who want zero scripting. All templates assume the [Chapter 5 schema](05-properties-tags-and-metadata.md) and the [Chapter 8 folder tree](08-vault-architecture.md). Save each as `Templates/<name>.md`.

## Conventions

- `<% … %>` is Templater; `{{…}}` is core Templates / QuickAdd (do not mix in one file).
- `<% tp.file.cursor() %>` marks where the cursor lands.
- Properties left blank (`due:`) are intentional — fill in the property editor.
- Replace `Areas/`, `People/` etc. with your folder names if they differ.

## Periodic

### `tpl-quarterly`

```markdown
---
type: quarterly
period_start: <% moment(tp.file.title, "YYYY-[Q]Q").startOf("quarter").format("YYYY-MM-DD") %>
period_end: <% moment(tp.file.title, "YYYY-[Q]Q").endOf("quarter").format("YYYY-MM-DD") %>
---
« [[<% moment(tp.file.title, "YYYY-[Q]Q").subtract(1, "quarter").format("YYYY-[Q]Q") %>]] · [[<% moment(tp.file.title, "YYYY-[Q]Q").format("YYYY") %>|year]] · [[<% moment(tp.file.title, "YYYY-[Q]Q").add(1, "quarter").format("YYYY-[Q]Q") %>]] »

## Direction
![[<% moment(tp.file.title, "YYYY-[Q]Q").format("YYYY") %>#Theme]]
This quarter is for: <% tp.file.cursor() %>

## Goals (3–5)
```base
filters: {and: [type == "goal", horizon == "quarter", status == "active"]}
views: [{type: table, name: Goals, order: [file.name, area, metric, target, current, due]}]
```

## Project portfolio decision
![[Projects.base#Active]]
- Continue:
- Pause:
- Drop:
- Promote from someday:

## Stop doing
-

## Retrospective (last quarter)
- Planned vs happened:
- Why:
- Lesson:

## Systems review
- Plugins to remove:
- Templates to trim:
- Dashboards unused:

## Months
- [[<% moment(tp.file.title, "YYYY-[Q]Q").startOf("quarter").format("YYYY-MM") %>]] · [[<% moment(tp.file.title, "YYYY-[Q]Q").startOf("quarter").add(1, "month").format("YYYY-MM") %>]] · [[<% moment(tp.file.title, "YYYY-[Q]Q").startOf("quarter").add(2, "month").format("YYYY-MM") %>]]
```

### `tpl-yearly`

```markdown
---
type: yearly
year: <% tp.file.title %>
---
## Theme
<% tp.file.cursor() %>

## Vision (embedded)
![[Vision]]

## Goals
```base
filters: {and: [type == "goal", horizon == "year", due.year == <% tp.file.title %>]}
views: [{type: table, name: Goals, order: [file.name, area, metric, target, current, status]}]
```

## Quarters
- [[<% tp.file.title %>-Q1]] · [[<% tp.file.title %>-Q2]] · [[<% tp.file.title %>-Q3]] · [[<% tp.file.title %>-Q4]]

## Annual review
<% tp.file.include("[[frag-annual-review]]") %>

## Stats
- Books finished: (Reading Base, Finished by year)
- Workouts: (Workouts Base, By kind)
- Days journaled: `$= dv.pages('"Journal/Daily"').where(p => p.file.day && p.file.day.year === <% tp.file.title %>).length`
- Notes created: `$= dv.pages().where(p => p.file.cday.year === <% tp.file.title %>).length`
- Decisions logged: (Decisions Base)

## Photos of the year
```

### `tpl-daily-plain` (no Templater, core Templates only)

```markdown
---
type: daily
date: {{date:YYYY-MM-DD}}
mood:
energy:
sleep_h:
---
## Plan
- [ ]

## Log
- {{time}}

## Notes

## Evening
- Went well:
- Could improve:
- Grateful for:
```

## Areas, goals, habits

### `tpl-area`

```markdown
---
type: area
review_cadence: monthly
standard: ""
tags: []
---
## Why this matters
<% tp.file.cursor() %>

## Standard
(what "good enough" looks like — concrete, checkable)

## Active projects
```base
filters: {and: [type == "project", status == "active", area == this]}
views: [{type: table, name: Active, order: [file.name, due, priority]}]
```

## Goals
```base
filters: {and: [type == "goal", status != "done", area == this]}
views: [{type: list, name: Goals, order: [file.name, horizon, target, current]}]
```

## Routines
-

## Metrics

## Maps & notes
```

### `tpl-goal`

```markdown
---
type: goal
horizon: <% await tp.system.suggester(["quarter","year","life"], ["quarter","year","life"]) %>
status: active
area: "[[<% (await tp.system.suggester(f => f.basename, app.vault.getMarkdownFiles().filter(f => f.path.startsWith("Areas/")))).basename %>]]"
metric: ""
target:
current:
due:
parent:
tags: []
---
## Why
<% tp.file.cursor() %>

## Definition of done

## Projects serving this goal
```base
filters: {and: [type == "project", goal == this]}
views: [{type: table, name: Projects, order: [file.name, status, due]}]
```

## Progress log
- <% tp.date.now("YYYY-MM-DD") %> — baseline:
```

### `tpl-habit`

```markdown
---
type: habit
cadence: daily
active: true
start: <% tp.date.now("YYYY-MM-DD") %>
why: ""
tag: "#habit/<% tp.file.title.toLowerCase().replace(/\s+/g, "-") %>"
tags: []
---
## Why
<% tp.file.cursor() %>

## Design
- Cue:
- Routine:
- Reward:
- Minimum version (bad days):

## Tracking
Daily note checkbox: `- [ ] <% tp.file.title %> #habit/<% tp.file.title.toLowerCase().replace(/\s+/g, "-") %>`

## Monthly review
-
```

## Sources

### `tpl-article`

```markdown
---
type: source
medium: article
author: []
url:
published:
status: to-read
rating:
finished:
topics: []
tags: []
---
> [!summary] In one paragraph
>

## Key ideas (own words)
- <% tp.file.cursor() %>

## Highlights

## Quotes
```

### `tpl-podcast-video`

```markdown
---
type: source
medium: <% await tp.system.suggester(["podcast","video","talk"], ["podcast","video","talk"]) %>
creator: []
url:
duration_min:
status: to-watch
rating:
finished:
topics: []
tags: []
---
> [!summary]
>

## Notes with timestamps
- [00:00]( ) <% tp.file.cursor() %>

## Key ideas (own words)
-

## Follow-ups
- [ ]
```

### `tpl-course`

```markdown
---
type: source
medium: course
provider:
url:
status: in-progress
progress: 0
started: <% tp.date.now("YYYY-MM-DD") %>
finished:
topics: []
tags: []
---
## Why I'm taking this
<% tp.file.cursor() %>

## Modules
- [ ] 1.

## Lecture notes
```base
filters: {and: [type == "lecture", course == this]}
views: [{type: table, name: Lectures, order: [file.name, date, done], sort: [{property: file.name, direction: ASC}]}]
```

## Exercises & projects

## Takeaways
```

### `tpl-paper` (manual, non-Zotero version)

```markdown
---
type: source
medium: paper
citekey:
author: []
year:
journal:
doi:
url:
status: to-read
rating:
topics: []
tags: []
---
> [!abstract]- Abstract
>

## Summary (own words)
<% tp.file.cursor() %>

## Key claims
-

## Methods

## Limitations

## Connections to my work

## Quotes
```

## Knowledge

### `tpl-moc`

```markdown
---
type: moc
area:
tags: [moc]
---
Up: [[Knowledge MOC]]

> [!abstract] Scope
> <% tp.file.cursor() %>

## Start here
-

## Core ideas
-

## Sources
-

## Open questions
-

## Unsorted (linked here, not yet placed)
```dataview
LIST FROM [[]] AND -"Maps" WHERE type = "note" AND !contains(this.file.outlinks, file.link) SORT file.ctime DESC LIMIT 20
```
```

### `tpl-belief`

```markdown
---
type: belief
confidence: 70
domain:
last_updated: <% tp.date.now("YYYY-MM-DD") %>
sources: []
tags: []
---
## Claim
<% tp.file.title %>

## Evidence for
- <% tp.file.cursor() %>

## Evidence against
-

## What would change my mind

## Update log
- <% tp.date.now("YYYY-MM-DD") %> — set to 70%.
```

### `tpl-quote`

```markdown
---
type: quote
author:
source:
themes: []
tags: []
---
> <% tp.file.cursor() %>

— 
```

## Life records

### `tpl-trip`

```markdown
---
type: trip
destination: <% tp.file.title %>
country:
start:
end:
status: idea
companions: []
budget:
spent:
lat:
long:
photo:
tags: []
---
## Bookings
| What | Ref | When | Link |
| --- | --- | --- | --- |

## Itinerary
- Day 1 —

## Packing
<%* const kind = await tp.system.suggester(["city 3 days","hiking","none"], ["frag-packing-city","frag-packing-hiking",""]); if (kind) tR += await tp.file.include("[[" + kind + "]]"); %>

## Research & places
-

## Budget
| Item | Planned | Actual |
| --- | --- | --- |

## Afterwards
- Worked:
- Next time:
```

### `tpl-place`

```markdown
---
type: place
city:
country:
kind: <% await tp.system.suggester(["restaurant","cafe","bar","museum","hotel","hike","viewpoint","shop","other"], ["restaurant","cafe","bar","museum","hotel","hike","viewpoint","shop","other"]) %>
rating:
status: want
visited: []
lat:
long:
url:
tags: []
---
<% tp.file.cursor() %>
```

### `tpl-asset`

```markdown
---
type: asset
category:
purchased:
price:
merchant:
model:
serial:
warranty_until:
manual_url:
location:
status: owned
lent_to:
lent_on:
photo:
tags: []
---
## Notes
<% tp.file.cursor() %>

## Service / repairs
- 
```

### `tpl-document`

```markdown
---
type: document
kind:
owner:
issued:
expires:
location: ""
renewal_notes: ""
tags: []
---
<% tp.file.cursor() %>
```

### `tpl-subscription`

```markdown
---
type: subscription
cost:
currency: EUR
billing: monthly
renews:
status: active
category:
account:
cancel_url:
shared_with: []
tags: []
---
## Why we have it
<% tp.file.cursor() %>

## History
- <% tp.date.now("YYYY-MM-DD") %> — started.
```

### `tpl-account`

```markdown
---
type: account
institution:
kind:
currency:
owner:
opened:
closed:
rate:
status: active
login_hint: ""
statements_url:
tags: []
---
## Purpose
<% tp.file.cursor() %>

## Fees & quirks

## In an emergency
```

### `tpl-networth`

```markdown
---
type: networth
date: <% moment(tp.file.title, "YYYY-MM").startOf("month").format("YYYY-MM-DD") %>
cash:
investments:
retirement:
property:
other_assets:
debts:
---
## Balances
| Account | Balance |
| --- | --- |
<%* for (const a of app.vault.getMarkdownFiles().filter(f => f.path.startsWith("Finance/Accounts/")).sort((x,y)=>x.basename.localeCompare(y.basename))) tR += `| [[${a.basename}]] | |\n`; %>

## Month
- Income:
- Spend:
- Saved / invested:
- Notable:

## Notes
<% tp.file.cursor() %>
```

### `tpl-health-event`

```markdown
---
type: health-event
date: <% tp.date.now("YYYY-MM-DD") %>
kind: <% await tp.system.suggester(["symptom","appointment","medication","lab","vaccination","injury","procedure"], ["symptom","appointment","medication","lab","vaccination","injury","procedure"]) %>
patient: "[[Me]]"
provider:
severity:
body_part:
tags: []
---
## What happened
<% tp.file.cursor() %>

## What was said / decided

## Follow-ups
- [ ]
```

### `tpl-vehicle`

```markdown
---
type: vehicle
make_model:
year:
plate:
vin:
bought:
price:
insurance:
registration_renews:
inspection_due:
service_interval_km:
odometer:
tags: []
---
## Service log
| Date | km | Work | Garage | Cost |
| --- | --- | --- | --- | --- |

## Notes
<% tp.file.cursor() %>
```

### `tpl-pet`

```markdown
---
type: pet
species:
breed:
born:
chip:
vet:
insurance:
food: ""
tags: []
---
## Care
<% tp.file.cursor() %>

## Vaccinations
| Vaccine | Date | Next due |
| --- | --- | --- |

## Medications

## Weight
| Date | kg |
| --- | --- |

## Health events
```base
filters: {and: [type == "health-event", patient == this]}
views: [{type: table, name: Events, order: [file.name, date, kind], sort: [{property: date, direction: DESC}]}]
```
```

## Work

### `tpl-1on1`

```markdown
---
type: meeting
series: "1:1"
date: <% tp.date.now("YYYY-MM-DD") %>
attendees: ["[[<% (await tp.system.suggester(f => f.basename, app.vault.getMarkdownFiles().filter(f => f.path.startsWith("People/")))).basename %>]]"]
tags: []
---
## Since last time
- Wins:
- Blockers:

## Their topics
<% tp.file.cursor() %>

## My topics

## Feedback (both ways)

## Growth

## Actions
- [ ] 👤 
- [ ] Me — 
```

### `tpl-doc`

```markdown
---
type: doc
doc_kind: <% await tp.system.suggester(["proposal","spec","plan","retro","runbook","howto"], ["proposal","spec","plan","retro","runbook","howto"]) %>
status: draft
project:
audience:
last_verified: <% tp.date.now("YYYY-MM-DD") %>
tags: []
---
> [!summary] TL;DR
> <% tp.file.cursor() %>

## Context

## Content

## Open questions

## Changelog
- <% tp.date.now("YYYY-MM-DD") %> — created.
```

### `tpl-weekly-status`

```markdown
## Status — <% tp.date.now("YYYY-[W]WW") %>
### Done
```tasks
done this week
path includes Work
short mode
```
### Next
```tasks
not done
path includes Work
happens next week
short mode
```
### Blockers / needs
-
```

## Creative

### `tpl-scene`

```markdown
---
type: scene
chapter:
order:
pov:
location:
time: ""
status: draft
words:
beat: ""
tension:
tags: []
---
<% tp.file.cursor() %>
```

### `tpl-character`

```markdown
---
type: character
role:
age:
first_appears:
arc: ""
portrait:
tags: []
---
## Wants / needs
<% tp.file.cursor() %>

## Appearance & voice

## Relationships
-

## Arc

## Appearances
```dataview
LIST FROM [[]] WHERE type = "scene" SORT order ASC
```
```

### `tpl-draft`

```markdown
---
type: draft
kind: <% await tp.system.suggester(["essay","post","newsletter","talk"], ["essay","post","newsletter","talk"]) %>
status: idea
target:
publish_on:
published_url:
audience: ""
tags: []
---
## Thesis
<% tp.file.cursor() %>

## Outline (idea notes to draw from)
- ![[ ]]

## Draft

## Editing passes
<% tp.file.include("[[frag-editing-passes]]") %>
```

## Fragments (included by other templates)

### `frag-weekly-review`

```markdown
- [ ] Inbox to zero (`Inbox/`, email, downloads, photos)
- [ ] Daily notes of the week skimmed; loose tasks captured or dropped
- [ ] Every active project has a next action; `reviewed` updated
- [ ] Waiting-for list reviewed
- [ ] Calendar: last week (anything to capture?) and next two weeks
- [ ] Someday/maybe skimmed (monthly)
- [ ] People: contact-due list; message one or two
- [ ] Health, finance, home quick check
- [ ] Three wins · one lesson · one change
- [ ] Focus for next week (3 outcomes) → schedule tasks with ⏳
```

### `frag-annual-review`

```markdown
### Read the year
- [ ] Skim the twelve monthly notes — one line each below
- [ ] Reread every decision note of the year; grade the reasoning
- [ ] Reread beliefs updated this year
- [ ] Reread the letters

### The year, month by month
- Jan: · Feb: · Mar: · Apr: · May: · Jun: · Jul: · Aug: · Sep: · Oct: · Nov: · Dec:

### Areas (score /10 + a paragraph)
- Health: · Finances: · Career: · Family: · Friends: · Home: · Learning: · Play: · Mind:

### People
- Who mattered this year: · Who I lost touch with:

### Decisions
- Best: · Worst: · Luckiest events:

### Values check
- For each value: honoured when / betrayed when

### Principles
- Used most: · To add: · To retire:

### Patterns
- Recurred: · Improved:

### Themes
- The year in three words: · The story I'd tell: · What it was for:

### Next year
- Theme: · Goals: · Stop: · Protect: · Vision paragraph revised: [ ]

### Gratitude
-

### Letter to next year's self
[[<% Number(tp.date.now("YYYY")) + 1 %> from <% tp.date.now("YYYY") %>]]
```

### `frag-editing-passes`

```markdown
- [ ] Structure: does each section earn its place? Is the order the argument's order?
- [ ] Argument: is every claim supported or linked to its source?
- [ ] Clarity: one idea per paragraph; topic sentences; define terms once
- [ ] Line: cut adverbs, hedges, passive voice; shorten sentences over 30 words
- [ ] Read aloud
- [ ] Title and first paragraph rewritten last
```

### `frag-packing-city`

```markdown
- [ ] Passport / ID · [ ] Wallet, cards · [ ] Phone, charger, power bank · [ ] Adapter
- [ ] Clothes ×3 days · [ ] Comfortable shoes · [ ] Jacket · [ ] Sleepwear
- [ ] Toiletries · [ ] Medications · [ ] Glasses / contacts
- [ ] Tickets / bookings (offline) · [ ] Headphones · [ ] Book / Kindle · [ ] Tote bag
```

### `frag-packing-hiking`

```markdown
- [ ] Boots · [ ] Layers (base, mid, shell) · [ ] Hat, gloves · [ ] Socks ×N
- [ ] Pack · [ ] Water 2L+ / filter · [ ] Food, snacks · [ ] Map, compass, GPS · [ ] Headlamp
- [ ] First aid · [ ] Sun protection · [ ] Emergency blanket · [ ] Whistle · [ ] Knife
- [ ] Permits · [ ] Weather checked · [ ] Route shared with someone
```

### `frag-meeting-checklist`

```markdown
- [ ] Purpose stated in one line
- [ ] Agenda pulled from the person's/project's "Next time"
- [ ] Decisions written as sentences; actions with 👤 owner and 📅 date
- [ ] Next meeting date set (or explicitly none)
- [ ] Two-minute tidy done within the hour
```

## QuickAdd and Meta Bind snippets

### QuickAdd capture: log line

Type **Capture**. Capture to: daily note (`Journal/Daily/{{DATE:YYYY-MM-DD}}`), create if missing with `tpl-daily`. Insert after: `## Log`. Format: `- {{DATE:HH:mm}} {{VALUE}}`.

### QuickAdd capture: quick task

Capture to the daily note, insert after `## Plan`, format `- [ ] {{VALUE}}`.

### QuickAdd multi menu "New…"

Type **Multi**; children: Template choices for Project/Person/Book/Idea/Meeting/Decision/Recipe (each a **Template** choice with its folder and `tpl-*`), plus the captures above. One hotkey; add to the mobile toolbar.

### Meta Bind daily controls (paste under properties in `tpl-daily`)

```markdown
Mood `INPUT[slider(minValue(1), maxValue(10), addLabels):mood]` · Energy `INPUT[slider(minValue(1), maxValue(10), addLabels):energy]` · Sleep `INPUT[number:sleep_h]` h
```

### Meta Bind project controls (in `tpl-project`)

```markdown
Status `INPUT[inlineSelect(option(idea), option(active), option(on-hold), option(done), option(dropped)):status]` · Priority `INPUT[inlineSelect(option(1), option(2), option(3)):priority]` · Due `INPUT[date:due]` · `BUTTON[mark-reviewed]`
```

```meta-bind-button
label: Mark reviewed
id: mark-reviewed
style: primary
actions:
  - type: updateMetadata
    bindTarget: reviewed
    evaluate: true
    value: 'moment().format("YYYY-MM-DD")'
```

## Key takeaways

- Every note type in the reference vault has a template here or in Chapter 11; fragments hold checklists once so every template includes the current version.
- Prompts are kept to two or three per template; blank properties are filled in the editor or via Meta Bind controls.
- QuickAdd captures (log line, quick task) and a "New…" multi menu cover mobile and hotkey capture; Meta Bind makes daily and project notes into forms.

## Next

[Chapter 37: Cheat Sheets →](37-cheatsheets.md)
