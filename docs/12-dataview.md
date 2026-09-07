# Dataview — Queries and Scripting

Dataview (community, by blacksmithgu) was for years the reason people chose Obsidian over everything else: SQL-like queries over your notes' metadata, rendered live as tables, lists, task lists, and calendars, plus a JavaScript API for anything the query language cannot express. Bases now covers the common cases better (Chapter 10), but Dataview remains essential for **inline fields**, **task queries with custom logic**, **cross-note joins**, **charts**, and **arbitrary computation**. Dataview is in maintenance mode — stable, widely used, not gaining features — which is fine: it does what it does. This chapter is the complete practical reference plus 40+ queries for a whole-life vault.

## Setup

Install **Dataview**. Settings that matter:

| Setting | Recommended |
| --- | --- |
| Enable JavaScript queries | On (you will need DataviewJS) |
| Enable inline JavaScript queries | On |
| Enable inline field highlighting | On |
| Date format / Date + time format | `yyyy-MM-dd`, `yyyy-MM-dd HH:mm` (Luxon tokens — lowercase `yyyy`, unlike Moment) |
| Automatic view refreshing | On; refresh interval 2500 ms |
| Inline query prefix | `=` (default) |
| Recursive sub-task completion | On if you use nested tasks |
| Task completion tracking | On + `completion` text if you want `[completion:: date]` stamped when checking boxes in Dataview views |

## Data model

Every Markdown file is a page with:

- **Frontmatter properties** as fields (`status`, `due`, …). Names are also available sanitized: `Sleep Hours` → `sleep-hours`; `snake_case` stays as is.
- **Inline fields** `key:: value` (own line), `[key:: value]` (inline, visible key) or `(key:: value)` (inline, hidden key). Inline fields inside list items/tasks attach to that item.
- **Implicit fields** under `file`: `file.name`, `file.folder`, `file.path`, `file.ext`, `file.link`, `file.size`, `file.ctime`, `file.cday`, `file.mtime`, `file.mday`, `file.tags` (with nesting expanded), `file.etags` (exact tags), `file.inlinks`, `file.outlinks`, `file.aliases`, `file.tasks`, `file.lists`, `file.frontmatter`, `file.day` (a date parsed from the filename like `2026-09-06`), `file.starred`.
- **Types**: text, number, boolean, date (`2026-09-06` or `2026-09-06T14:30`), duration (`3 days`, `2h 30m`), link, list, object. Types are inferred; property types set in Obsidian are respected for dates.

## DQL — the query language

````markdown
```dataview
TABLE [WITHOUT ID] col1 [AS "Name"], col2, ...
FROM source
WHERE condition
SORT field [ASC|DESC], field2 ...
GROUP BY field [AS "name"]
FLATTEN field [AS name]
LIMIT n
```
````

### Query types

| Type | Renders |
| --- | --- |
| `LIST` / `LIST expr` | Bulleted list of page links, optionally with one expression after each |
| `TABLE cols` | Table with a first column of page links (suppress with `WITHOUT ID`) |
| `TASK` | Interactive task list (check boxes update source files); `GROUP BY file.link` groups per note |
| `CALENDAR date_field` | Month calendar with dots per page on the date |

### `FROM` sources

```text
FROM "Projects"                      folder (and subfolders)
FROM "Projects/Active"
FROM #project                        tag (nested included)
FROM [[Alpha]]                       pages linking TO Alpha (inlinks)
FROM outgoing([[Alpha]])             pages Alpha links to
FROM "Projects" OR #project
FROM #a AND -#b                      exclude
FROM -"Templates"                    everything except a folder
FROM csv("Files/data.csv")           a CSV file as rows
(omit FROM)                          entire vault
```

### `WHERE` and expressions

Operators: `= != > < >= <=`, `AND OR !`, `+ - * / %`, `contains(list_or_string, x)`, `!contains(...)`. Field access `a.b`, `a[0]`, `a["key with space"]`. Dates and durations: `date(today)`, `date(now)`, `date(tomorrow)`, `date(yesterday)`, `date(sow)` / `date(eow)` (start/end of week), `date(som)`/`date(eom)`, `date(soy)`/`date(eoy)`, `dur(7 days)`, `date(today) - dur(1 week)`, `due - date(today)` gives a duration; `(due - date(today)).days`.

### Functions (the ones you will actually use)

| Category | Functions |
| --- | --- |
| Constructors | `date(x)`, `dur(x)`, `number(x)`, `string(x)`, `link(path, display?)`, `elink(url, display?)`, `list(...)`, `object(k, v, …)`, `typeof(x)`, `embed(link)` |
| Numeric | `round(n, digits?)`, `trunc`, `floor`, `ceil`, `min`, `max`, `sum(list)`, `average(list)`, `minby(list, fn)`, `maxby(list, fn)`, `product`, `reduce(list, op)` |
| Object/list | `contains`, `icontains`, `econtains` (exact), `containsword`, `extract(obj, keys…)`, `sort(list)`, `reverse`, `length`, `nonnull`, `all`, `any`, `none`, `join(list, sep)`, `filter(list, (x) => …)`, `map(list, (x) => …)`, `flat(list, depth?)`, `slice(list, a, b)`, `unique(list)`, `first(list)`, `last(list)` |
| String | `regextest(pattern, s)`, `regexmatch`, `regexreplace(s, pattern, repl)`, `replace`, `lower`, `upper`, `split(s, sep)`, `startswith`, `endswith`, `padleft`, `padright`, `substring`, `truncate(s, n, suffix?)` |
| Date | `dateformat(date, "yyyy-MM-dd")` (Luxon), `durationformat(dur, "h'h' m'm'")`, `striptime(date)`, `date.year/.month/.day/.weekday/.week/.hour`, `localtime` |
| Utility | `default(x, fallback)`, `choice(cond, a, b)`, `hash(seed, …)`, `striptime`, `meta(link)` (link metadata: `.display`, `.embed`, `.path`, `.subpath`) |

### `GROUP BY` and `rows`

After `GROUP BY`, each result is a group with `key` and `rows` (the pages). `TABLE rows.file.link, length(rows) GROUP BY status` shows each status with its notes. `FLATTEN` does the reverse — explodes a list field into one row per element (`FLATTEN attendees AS person`), which is how you count "meetings per person".

### Inline queries

`` `= this.due - date(today)` `` renders inside a sentence. `` `= length(filter(this.file.tasks, (t) => !t.completed))` `` gives a live count. `this` is the current page. Inline DataviewJS: `` `$= dv.current().file.mtime` ``.

## DataviewJS

````markdown
```dataviewjs
const pages = dv.pages('"Projects"').where(p => p.status === "active");
dv.table(["Project", "Due", "Days left"], pages.map(p => [p.file.link, p.due, p.due ? Math.round(p.due.diff(dv.date("today"), "days").days) : ""]));
```
````

The `dv` API:

| Method | Purpose |
| --- | --- |
| `dv.pages(source)` | Data array of pages (`'"Folder"'`, `'#tag'`, `'[[Note]]'`, combinations) |
| `dv.page(path)` / `dv.current()` | One page |
| `dv.pagePaths(source)` | Paths only |
| `dv.list(arr)`, `dv.table(headers, rows)`, `dv.taskList(tasks, groupByFile?)` | Render |
| `dv.header(level, text)`, `dv.paragraph(text)`, `dv.span(text)`, `dv.el(tag, text, attrs)` | Render arbitrary content (Markdown rendered) |
| `dv.date(x)`, `dv.duration(x)`, `dv.fileLink(path, embed?, display?)`, `dv.sectionLink`, `dv.blockLink` | Constructors |
| `dv.array(...)` | Wrap a JS array as a Data array (`.where`, `.sort`, `.groupBy`, `.map`, `.flatMap`, `.limit`, `.distinct`, `.sum`, `.length`) |
| `dv.compare`, `dv.equal` | Comparisons that understand Dataview types |
| `dv.io.csv(path)`, `dv.io.load(path)` | Read CSV / file text |
| `dv.view("Scripts/views/name", input)` | Run a `.js`/`.css` view script from a folder (reusable widgets) |
| `dv.execute(dql)`, `dv.executeJs(js)`, `dv.query(dql)`, `dv.tryQuery` | Run DQL from JS (returns structured results) |
| `app`, `dv.app` | Full Obsidian API — read and *write* files |

Dates are **Luxon** DateTime objects (`.diff()`, `.plus({days: 7})`, `.toFormat("yyyy-MM-dd")`, `.startOf("week")`), durations are Luxon Durations.

### Reusable views

`Scripts/views/progress/view.js`:

```javascript
// input: {source: '"Projects"', field: "status", done: "done"}
const pages = dv.pages(input.source);
const done = pages.where(p => p[input.field] === input.done).length;
const pct = pages.length ? Math.round(100 * done / pages.length) : 0;
dv.paragraph(`**${done}/${pages.length}** (${pct}%)  \n\`${"█".repeat(pct/5)}${"░".repeat(20 - pct/5)}\``);
```

Use anywhere: `` ```dataviewjs dv.view("Scripts/views/progress", {source: '"Projects"', field: "status", done: "done"}) ``` ``.

## Query library for a whole-life vault

Assumes the Chapter 5 schema. Each fits in a `dataview` block unless marked `dataviewjs`.

### Daily note widgets

Notes created or modified on this day (put in `tpl-daily`; uses `this.file.day`):

```text
TABLE WITHOUT ID file.link AS "Note", type
FROM -"Journal" AND -"Templates"
WHERE file.cday = this.file.day OR file.mday = this.file.day
SORT file.mtime DESC
```

Tasks due today or overdue:

```text
TASK
FROM -"Templates"
WHERE !completed AND due AND due <= this.file.day
SORT due ASC
```

"On this day" in previous years:

```text
LIST
FROM "Journal/Daily"
WHERE file.day.month = this.file.day.month AND file.day.day = this.file.day.day AND file.day.year != this.file.day.year
```

Interstitial log with inline mood: given lines like `- 14:30 finished draft [mood:: 7] [energy:: 6]` in daily notes:

```text
TABLE WITHOUT ID file.link AS Day, round(average(rows.L.mood),1) AS Mood, round(average(rows.L.energy),1) AS Energy
FROM "Journal/Daily"
FLATTEN file.lists AS L
WHERE L.mood
GROUP BY file.link
SORT file.link DESC
LIMIT 30
```

### Weekly review

Completed tasks this week (uses `[completion:: date]` stamped by Dataview or Tasks' `✅ 2026-09-06`):

```text
TASK
WHERE completed AND completion >= date(sow) AND completion <= date(eow)
GROUP BY file.link
```

Projects without a next action:

```text
TABLE WITHOUT ID file.link AS Project, status
FROM "Projects"
WHERE status = "active" AND length(filter(file.tasks, (t) => !t.completed)) = 0
```

Stale active projects (no edit in 14 days):

```text
TABLE file.mtime AS "Last touched", (date(today) - file.mday).days AS "Days"
FROM "Projects"
WHERE status = "active" AND file.mday < date(today) - dur(14 days)
SORT file.mday ASC
```

Waiting-for items across the vault (tasks containing `#waiting` or the `👤` convention):

```text
TASK
WHERE !completed AND (contains(tags, "#waiting") OR contains(text, "👤"))
GROUP BY file.link
```

### Projects & goals

Project portfolio with task progress:

```text
TABLE WITHOUT ID file.link AS Project, area, due,
  length(filter(file.tasks, (t) => t.completed)) + "/" + length(file.tasks) AS Tasks,
  choice(due AND due < date(today), "🔴", "🟢") AS ""
FROM "Projects"
WHERE status = "active"
SORT priority ASC, due ASC
```

Goals with linked project counts:

```text
TABLE WITHOUT ID file.link AS Goal, horizon, status, length(filter(file.inlinks, (l) => meta(l).path AND contains(string(l), "Projects"))) AS Projects
FROM "Goals"
WHERE status != "done"
```

(Bases handles most of these more cleanly; keep Dataview where task counting is needed.)

### People

Last mention of each person in daily notes:

```text
TABLE WITHOUT ID file.link AS Person, max(filter(file.inlinks, (l) => contains(string(l), "Journal/Daily"))) AS "Last daily mention"
FROM "People"
SORT file.name ASC
```

Meetings per person (FLATTEN):

```text
TABLE WITHOUT ID person AS Person, length(rows) AS Meetings, max(rows.date) AS Last
FROM "Work/Meetings"
FLATTEN attendees AS person
GROUP BY person
SORT length(rows) DESC
```

Upcoming birthdays (next 30 days, year-agnostic):

```dataviewjs
const today = dv.date("today");
const rows = dv.pages('"People"').where(p => p.birthday).map(p => {
  let next = p.birthday.set({year: today.year});
  if (next < today) next = next.plus({years: 1});
  return {p, next, days: Math.ceil(next.diff(today, "days").days), age: next.year - p.birthday.year};
}).where(r => r.days <= 30).sort(r => r.days);
dv.table(["Person", "Birthday", "In", "Turns"], rows.map(r => [r.p.file.link, r.next.toFormat("d MMM"), r.days + " d", r.age]));
```

### Reading & learning

Reading stats by year:

```text
TABLE WITHOUT ID finished.year AS Year, length(rows) AS Books, round(average(rows.rating), 2) AS "Avg rating", sum(rows.pages) AS Pages
FROM "Sources/Books"
WHERE status = "read" AND finished
GROUP BY finished.year
SORT finished.year DESC
```

Highlights tagged for review (lines with `#review` inside source notes):

```text
TABLE WITHOUT ID L.text AS Highlight, file.link AS Source
FROM "Sources"
FLATTEN file.lists AS L
WHERE contains(L.tags, "#review")
LIMIT 50
```

Ideas without sources / sources without ideas:

```text
LIST FROM "Notes" WHERE !sources OR length(sources) = 0
```

```text
LIST FROM "Sources" WHERE status = "read" AND length(filter(file.inlinks, (l) => contains(string(l), "Notes/"))) = 0
```

### Health & habits

Habit streaks from daily-note checkboxes (tasks in a `## Habits` section like `- [x] Meditate #habit/meditate`):

```dataviewjs
const habit = "#habit/meditate";
const days = dv.pages('"Journal/Daily"').sort(p => p.file.day, "desc");
let streak = 0;
for (const d of days) {
  const t = d.file.tasks.find(t => t.tags.includes(habit));
  if (t && t.completed) streak++; else break;
}
dv.paragraph(`**${habit}** current streak: **${streak}** days`);
```

Workout volume by week:

```text
TABLE WITHOUT ID dateformat(date, "kkkk-'W'WW") AS Week, length(rows) AS Sessions, sum(rows.duration_min) AS Minutes, round(sum(rows.distance_km),1) AS km
FROM "Health/Workouts"
GROUP BY dateformat(date, "kkkk-'W'WW")
SORT dateformat(date, "kkkk-'W'WW") DESC
LIMIT 12
```

Sleep vs mood correlation (quick and dirty):

```dataviewjs
const ps = dv.pages('"Journal/Daily"').where(p => p.sleep_h && p.mood);
const n = ps.length; if (n < 5) { dv.paragraph("Not enough data"); return; }
const mx = ps.map(p=>p.sleep_h).array().reduce((a,b)=>a+b)/n, my = ps.map(p=>p.mood).array().reduce((a,b)=>a+b)/n;
let num=0, dx=0, dy=0;
for (const p of ps) { num += (p.sleep_h-mx)*(p.mood-my); dx += (p.sleep_h-mx)**2; dy += (p.mood-my)**2; }
dv.paragraph(`Sleep↔mood correlation over ${n} days: **r = ${(num/Math.sqrt(dx*dy)).toFixed(2)}**`);
```

### Finance

Monthly spend from a transactions ledger note where each line is `- 2026-09-03 Groceries [amount:: 54.20] [cat:: food]`:

```text
TABLE WITHOUT ID cat AS Category, round(sum(rows.L.amount), 2) AS Total, length(rows) AS Items
FROM "Finance/Ledger"
FLATTEN file.lists AS L
FLATTEN L.cat AS cat
WHERE L.amount AND dateformat(date(regexreplace(L.text, "^(\d{4}-\d{2}-\d{2}).*", "$1")), "yyyy-MM") = dateformat(date(today), "yyyy-MM")
GROUP BY cat
SORT sum(rows.L.amount) DESC
```

Subscriptions total (Bases does this better, but for completeness):

```text
TABLE WITHOUT ID file.link AS Service, cost, billing, round(choice(billing = "yearly", cost/12, cost), 2) AS Monthly
FROM "Finance/Subscriptions"
WHERE status = "active"
SORT choice(billing = "yearly", cost/12, cost) DESC
```

Inline total for a sentence (inline DQL cannot query other pages, so use inline JS): `` `$= Math.round(dv.pages('"Finance/Subscriptions"').where(p=>p.status==="active").map(p=>p.billing==="yearly"?p.cost/12:p.cost).array().reduce((a,b)=>a+b,0)*100)/100` ``.

### Knowledge maintenance

Orphans and dead ends:

```text
TABLE WITHOUT ID file.link, length(file.inlinks) AS In, length(file.outlinks) AS Out
FROM -"Templates" AND -"Journal" AND -"Attachments"
WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0
```

Most linked notes (hub candidates without MOCs):

```text
TABLE WITHOUT ID file.link AS Note, length(file.inlinks) AS Inlinks
FROM -"Maps"
WHERE type != "moc" AND length(file.inlinks) > 15
SORT length(file.inlinks) DESC
```

Notes touched in the last 7 days, by type:

```text
TABLE WITHOUT ID type AS Type, rows.file.link AS Notes
FROM -"Journal" AND -"Templates"
WHERE file.mday >= date(today) - dur(7 days)
GROUP BY type
```

Unresolved-link frequency (DataviewJS via metadataCache):

```dataviewjs
const unres = app.metadataCache.unresolvedLinks;
const counts = {};
for (const src in unres) for (const t in unres[src]) counts[t] = (counts[t] || 0) + unres[src][t];
const rows = Object.entries(counts).sort((a,b)=>b[1]-a[1]).slice(0, 25);
dv.table(["Missing note", "Referenced"], rows.map(([t,c]) => [t, c]));
```

### MOC helpers

Unsorted notes that link to this MOC's topic but are not listed in it:

```text
LIST
FROM [[]] AND -"Maps"
WHERE !contains(this.file.outlinks, file.link)
SORT file.ctime DESC
```

Random note from this MOC's neighbourhood for review:

```dataviewjs
const ps = dv.pages("[[]]").where(p => p.type === "note").array();
if (ps.length) { const p = ps[Math.floor(Math.random()*ps.length)]; dv.paragraph(`🎲 ${p.file.link}`); }
```

## Charts

Dataview does not chart, but two plugins render charts from Dataview output:

- **Obsidian Charts** — a `chart` code block (Chart.js). DataviewJS can build one: `dv.paragraph("```chart\ntype: bar\nlabels: [" + labels + "]\nseries:\n  - title: km\n    data: [" + data + "]\n```")` — or use `window.renderChart(config, container)`.
- **Tracker** — habit/metric charts over daily notes with its own query language (line, bar, heatmap, summary).
- **Heatmap Calendar** — GitHub-style yearly heatmaps from a DataviewJS array (mood, workouts, words written).

```dataviewjs
// Heatmap Calendar of workout minutes
const entries = dv.pages('"Health/Workouts"').where(p => p.date && p.duration_min).map(p => ({date: p.date.toFormat("yyyy-MM-dd"), intensity: p.duration_min, content: ""})).array();
renderHeatmapCalendar(this.container, {year: dv.date("today").year, colors: {c: ["#ede9fe","#c4b5fd","#8b5cf6","#6d28d9"]}, entries});
```

## Performance

- Dataview indexes the whole vault at startup; on mobile with 10k+ notes this can take seconds. There is no per-folder exclusion (Obsidian's *Excluded files* does not affect Dataview), so keep the vault lean instead.
- `FROM` a folder or tag before `WHERE` — it narrows before evaluating expressions.
- Avoid `file.inlinks`/`file.outlinks` computations over the whole vault in notes you open often.
- DataviewJS that loops over all pages and reads files (`app.vault.read`) is slow; read metadata (`file.tasks`, `file.lists`) instead — it is already indexed.
- Every open note with queries re-renders on the refresh interval; dashboards with 20 queries are fine on desktop, sluggish on phones. Move heavy dashboards to Bases.

## Common errors

| Symptom | Cause |
| --- | --- |
| "No results" but notes exist | `FROM "Folder"` case/path mismatch; property is a string but compared to a number; date property stored as text (`due: "2026-09-01"` in quotes is still parsed; `due: 1 Sept` is not) |
| Field shows as `-` | Field missing on that page; use `default(field, "")` |
| `contains()` on a link field fails | Compare links properly: `contains(attendees, [[Jane Doe]])`, or `contains(string(attendees), "Jane")` |
| Dates off by hours | Property has time/timezone; use `striptime()` |
| Query renders in Live Preview but not in Reading view (or vice versa) | Usually a nested code fence issue — use four backticks around examples |
| `TASK` query shows tasks twice | Nested tasks with *Recursive sub-task completion*; add `WHERE !parent` or flatten intentionally |
| Slow vault open | Too many pages with heavy DataviewJS; disable the plugin to confirm |

## Dataview ↔ Bases coexistence

Use Dataview for: `TASK` queries with logic, inline fields (`[mood:: 7]`), FLATTEN-based stats, joins, charts, anything JavaScript. Use Bases for: every list of notes filtered by properties, anything you edit, anything on mobile. When you write a new Dataview `TABLE`, ask whether a Base would do; usually yes.

## Key takeaways

- Dataview reads properties, inline fields, tasks, and list items — the last three are what Bases cannot see, and where Dataview remains irreplaceable.
- DQL: `TABLE/LIST/TASK/CALENDAR` + `FROM/WHERE/SORT/GROUP BY/FLATTEN/LIMIT`; learn `contains`, `filter`, `map`, `length`, `sum`, `dateformat`, `default`, `choice`, and date/duration arithmetic.
- DataviewJS with `dv.pages/.where/.map/.table` and Luxon dates handles everything else; `dv.view` makes widgets reusable; `app` gives write access.
- Keep a library of the queries above in `Meta/Query Library.md` and copy from it.
- Use charts plugins for visuals, keep heavy dashboards on desktop, and migrate plain tables to Bases.

## Next

[Chapter 13: Tasks, Time and Planning →](13-tasks-and-time.md)
