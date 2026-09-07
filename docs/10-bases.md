# Bases — the Native Database

Bases (core plugin, Obsidian 1.9, August 2025) turns any set of notes into a database view — table, cards, list, map, and (from 1.14) kanban — driven by properties, with filters, formulas, grouping, summaries, inline editing, and an open YAML file format. For most "show me all my X sorted by Y" needs it replaces Dataview with something faster, editable, mobile-native, and maintained by the Obsidian team. This chapter is the complete practical reference: the file format, every view type, the filter and formula language with the full function list condensed, and two dozen ready-to-paste bases for a whole-life vault.

## What a base is

A `.base` file is YAML describing **filters** (which notes), **formulas** (computed columns), **properties** (display config), **summaries** (aggregations), and **views** (how to show them). The set of notes is always "every file in the vault, narrowed by filters" — there is no `FROM`. Bases read **properties** (frontmatter), **file metadata** (name, path, folder, size, times, tags, links, embeds, backlinks) and, for non-Markdown files, file properties only. They do **not** read inline `key:: value` fields, tasks, or body text.

Create one: File explorer right-click → *New base*, the ribbon, or *Bases: Create new base* command. Or type it by hand — the UI and the YAML stay in sync. Embed with `![[Name.base]]` or `![[Name.base#View name]]`, or inline in any note:

````markdown
```base
filters:
  and:
    - type == "project"
    - status == "active"
views:
  - type: table
    name: Active projects
    order: [file.name, due, priority]
```
````

Inline bases are ideal for a project list inside an Area note; `.base` files are better for anything embedded in more than one place.

## The file format

```yaml
# Projects.base
filters:                       # global — applied to every view (AND-ed with view filters)
  and:
    - type == "project"
    - '!file.inFolder("Archive")'

formulas:                      # computed properties, referenced as formula.<name>
  days_left: 'if(due, (due - today()) / 86400000, "")'
  overdue: 'due && due < today() && status != "done"'
  age_days: '((now() - file.ctime) / 86400000).round(0)'

properties:                    # display configuration only (not used in filters/formulas)
  status:
    displayName: Status
  formula.days_left:
    displayName: Days left
  file.name:
    displayName: Project

summaries:                     # custom aggregations (optional; built-ins exist)
  pct_done: 'values.filter(value == "done").length / values.length'

views:
  - type: table
    name: Active
    filters:
      and:
        - status == "active"
    order:                     # columns, in order
      - file.name
      - area
      - due
      - formula.days_left
      - priority
    sort:
      - property: due
        direction: ASC
      - property: priority
        direction: ASC
    limit: 50
    summaries:
      formula.days_left: Min
  - type: table
    name: By area
    groupBy:
      property: area
      direction: ASC
    order: [file.name, status, due]
  - type: cards
    name: Gallery
    order: [file.name, status, area]
    image: cover               # property holding an image link/URL/hex colour
    imageFit: cover
    imageAspectRatio: 0.6
    cardSize: 240
  - type: list
    name: Quick list
    order: [file.name, status]
```

Key facts:

- Filters: a **string expression** or a **nested object** with exactly one of `and`, `or`, `not`, containing a list of expressions or further objects. Global `filters` and view `filters` are combined with AND.
- Formulas are strings in YAML; text literals inside need their own quotes (`'if(x, "yes", "no")'`). Output type follows the data (a formula returning a date sorts as a date).
- `order` lists the columns/properties shown; `sort` is a list of `{property, direction}`; `groupBy` takes one property (and a direction); `limit` caps rows.
- Property references: `note.price` or just `price` for frontmatter; `file.<x>` for file metadata; `formula.<x>` for formulas. Hyphenated names need brackets: `note["sleep-hours"]` — one more reason to use `snake_case`.
- Views can store extra keys for their layout (cards' `image`, `cardSize`, table column widths, etc.). The UI writes these; you rarely hand-edit them.

## Views

### Table

Rows are files; columns are properties/formulas. Cells for **note properties are editable inline** (text, number, date pickers, checkboxes, lists), and edits write straight to the note's frontmatter. Since 1.10: cell **selection** (shift-click, ++ctrl+shift+arrow++), **copy/paste** across cells (paste a value down a column — the fastest way to fix a hundred `status` typos), **undo/redo**, full keyboard navigation (++tab++, ++enter++ to edit, ++esc++, ++home++/++end++, ++ctrl+space++ column, ++shift+space++ row), **row height** setting, column resize (1.13 menu item), and right-click on a row for the file's context menu (1.12). Formula cells open a formula editor on ++enter++.

**Summaries** (1.10): right-click a column header → *Summarize…* → Average, Min, Max, Sum, Range, Median, Stddev (numbers); Earliest, Latest, Range (dates); Checked, Unchecked (booleans); Empty, Filled, Unique (any); or a custom summary formula operating on `values`. Summaries appear in a footer row and respect the current filters — a live "total monthly subscription cost" or "average mood this month".

**Group by** (1.10): one property; groups collapse; summaries apply per group when grouped.

### Cards

A gallery grid. Settings: card size, image property (a property holding `"[[cover.jpg]]"`, an `https://` URL, or a hex colour like `#7c3aed`), image fit (cover/contain), aspect ratio. Perfect for books with covers, recipes with photos, people with avatars, trips with a hero image, and colour-coded projects (put a hex colour in a `color` property).

### List

Bulleted or numbered list of files with chosen properties inline; supports multi-line content and nested properties. Great embedded in MOCs and area notes where a table is too heavy.

### Map

Requires the official **Maps** plugin (community directory, open source — also the reference implementation of a Bases view plugin). Pins are placed by latitude/longitude properties with a title property. Travel logs, restaurants, running routes' start points, people by city.

### Kanban (1.14+, early access at time of writing)

Columns are the values of the **group-by property**; drag a card to another column to change that property in the note; `+` in a column creates a note pre-filled with the value; drag column headers to reorder (right-click → *Reset order*). Options: hide empty columns, column width, image property. Grouping by a formula or file property makes the board read-only. This replaces the community Kanban plugin for property-driven boards (project status, reading pipeline, hiring pipeline, recipe test status) — the community plugin remains better for free-form boards of ad-hoc cards.

### Plugin views

The Bases API (1.10) lets plugins register view types. Beyond Maps, expect calendar, timeline, gallery, chart, and graph views from the community. Check the plugin directory for "Bases view".

## The toolbar

View menu (add/switch/reorder/configure views) · Results (count, **limit**, **Copy to clipboard** as a table that pastes into Sheets/Excel, **Export CSV**) · Sort (sort and group) · Filter (point-and-click builder with **All views** / **This view** sections and an *advanced* code editor for raw expressions) · Properties (choose displayed columns, **create formulas**) · Search (1.12: filter rows by displayed text) · New (create a file that satisfies the current filters — Bases infers `type: project` and `status: active` from equality filters).

Drag-and-drop: drop files onto a base to import them (1.12); drag a row's link from a base into the File explorer to move the file (1.13).

## Filters and formulas: the language

Bases expressions follow JavaScript semantics. Property names are bare identifiers; strings are quoted; numbers plain; booleans `true`/`false`; regex literals `/pattern/flags`.

### Operators

| Kind | Operators |
| --- | --- |
| Arithmetic | `+ - * / %` and parentheses |
| Comparison | `== != > < >= <=` (dates and numbers; `==`/`!=` on anything, including links vs files) |
| Boolean | `!`, `&&`, `\|\|` |
| Date arithmetic | `date + "1M"`, `now() - "2h"`, `today() + "7d"`; units `y M d w h m s` and long forms (`"1 week"`). `date - date` → milliseconds. `duration("5h") * 2` (duration on the left). |

### `this`

- In a base opened in the main area: `this` = the base file.
- In a base **embedded** in a note or canvas: `this` = the embedding note. So `area == this` inside `Areas/Health.md` shows Health's projects; `file.hasLink(this.file)` shows the note's backlinks.
- In a base in the **sidebar**: `this` = the active note in the main area — a live "related items" panel that follows you around.

### Global functions

`date(str)` · `duration(str)` · `now()` · `today()` · `file(pathOrLink)` · `link(path, display?)` · `image(pathOrUrl)` · `icon(lucideName)` · `html(str)` · `escapeHTML(str)` · `if(cond, a, b?)` · `list(x)` (wrap non-list into list — essential when a property is sometimes a string, sometimes a list) · `number(x)` · `min(...)` · `max(...)` · `random()`.

### By type (condensed)

| Type | Fields / functions |
| --- | --- |
| **Any** | `.isTruthy()`, `.isType("string")` etc., `.toString()`, `.isEmpty()` |
| **String** | `.length`, `.contains(s)`, `.containsAll(...)`, `.containsAny(...)`, `.startsWith(s)`, `.endsWith(s)`, `.lower()`, `.title()`, `.trim()`, `.slice(a,b?)`, `.split(sep, n?)`, `.replace(pattern\|regex, repl)` (capture groups `$1`), `.repeat(n)`, `.reverse()` |
| **Number** | `.abs()`, `.ceil()`, `.floor()`, `.round(digits?)`, `.toFixed(digits)` |
| **Date** | `.year .month .day .hour .minute .second .millisecond`, `.date()` (strip time), `.time()`, `.format("YYYY-MM-DD")` (Moment format), `.relative()` ("3 days ago") |
| **List** | `.length`, `.contains(v)`, `.containsAll(...)`, `.containsAny(...)`, `.filter(expr)` and `.map(expr)` (use `value`, `index`), `.reduce(expr, init)` (use `acc`, `value`), `.flat()`, `.join(sep)`, `.reverse()`, `.slice(a,b?)`, `.sort()`, `.unique()`, `.mean()`, `.median()`, `.stddev()` |
| **Link** | `.asFile()`, `.linksTo(file)` |
| **File** | `.name .basename .path .folder .ext .size .ctime .mtime .tags .links .embeds .backlinks .properties`, `.asLink(display?)`, `.hasLink(fileOrPath)`, `.hasTag(...tags)` (nested included), `.hasProperty(name)`, `.inFolder(folder)` (subfolders included) |
| **Object** | `.keys()`, `.values()`, `.isEmpty()` |
| **Regexp** | `.matches(str)` |

`file.backlinks` and `file.properties` are expensive and do not auto-refresh; prefer reversing the lookup (`file.hasLink(this.file)` on the other side).

### Formula cookbook

```yaml
formulas:
  # Days until due (negative = overdue), blank if no due date
  days_left: 'if(due, ((due - today()) / 86400000).round(0), "")'
  # Traffic light
  health: 'if(!due, "", if(due < today(), "🔴", if(due < today() + "7d", "🟡", "🟢")))'
  # Age of note in days
  age: '((now() - file.ctime) / 86400000).floor()'
  # Reading progress
  progress: 'if(pages && pages_read, (pages_read / pages * 100).round(0) + "%", "")'
  # Monthly cost normalised
  monthly: 'if(billing == "yearly", (cost / 12).round(2), cost)'
  # Contact overdue?
  contact_due: 'if(last_contact && contact_every, last_contact + (contact_every + "d") < today(), false)'
  # Birthday this year
  bday_this_year: 'if(birthday, date(today().year + "-" + birthday.format("MM-DD")), "")'
  # Link back to the area with an icon
  area_link: 'if(area, link(area, icon("compass")), "")'
  # Cover image from URL or attachment
  cover_img: 'if(cover, image(cover), "")'
  # First topic only, when topics may be string or list
  first_topic: 'list(topics)[0]'
  # Tag list as a string
  tag_str: 'file.tags.join(", ")'
  # Size in KB
  size_kb: '(file.size / 1024).toFixed(1) + " KB"'
  # Week number of the daily note
  week: 'if(date, date.format("YYYY-[W]WW"), "")'
  # Rating stars
  stars: 'if(rating, "★".repeat(rating) + "☆".repeat(5 - rating), "")'
  # Relative modified
  touched: 'file.mtime.relative()'
```

### Filter cookbook

```yaml
# Notes modified this week
- file.mtime > now() - "1w"
# Created this month
- file.ctime.month == today().month && file.ctime.year == today().year
# Any of several tags (nested included)
- file.hasTag("idea", "question")
# Property list contains a link to the current note
- topics.contains(this)
# Notes linking to this note (backlinks)
- file.hasLink(this.file)
# Notes this note links to (outlinks)
- this.file.hasLink(file)
# Empty or missing property
- status.isEmpty()
# Regex on file name
- /^\d{4}-\d{2}-\d{2}/.matches(file.name)
# Only Markdown, exclude templates
- file.ext == "md"
- '!file.inFolder("Templates")'
# Overdue and not done
- due < today() && status != "done"
# Big attachments
- file.ext != "md" && file.size > 5000000
```

YAML gotcha: expressions starting with `!` must be quoted (`'!file.inFolder("Archive")'`), and expressions containing `: ` or `#` should be quoted too.

## Ready-made bases for a whole-life vault

Paste each into `Bases/<name>.base`. They assume the Chapter 5/8 schema.

### Inbox

```yaml
filters:
  and:
    - file.inFolder("Inbox")
views:
  - type: table
    name: To process
    order: [file.name, type, file.ctime, file.size]
    sort:
      - property: file.ctime
        direction: DESC
```

### Projects

```yaml
filters:
  and:
    - type == "project"
formulas:
  days_left: 'if(due, ((due - today()) / 86400000).round(0), "")'
  health: 'if(status == "done", "✅", if(!due, "", if(due < today(), "🔴", if(due < today() + "7d", "🟡", "🟢"))))'
  last_review_age: 'if(reviewed, ((today() - reviewed) / 86400000).floor(), "")'
properties:
  formula.days_left: {displayName: "Days left"}
  formula.health: {displayName: ""}
views:
  - type: table
    name: Active
    filters:
      and:
        - status == "active"
    order: [formula.health, file.name, area, due, formula.days_left, priority]
    sort:
      - {property: priority, direction: ASC}
      - {property: due, direction: ASC}
  - type: table
    name: By area
    filters:
      and:
        - status != "done"
        - status != "dropped"
    groupBy: {property: area, direction: ASC}
    order: [file.name, status, due, priority]
  - type: table
    name: Needs review
    filters:
      and:
        - status == "active"
        - 'formula.last_review_age > 14 || reviewed.isEmpty()'
    order: [file.name, reviewed, formula.last_review_age]
  - type: table
    name: Done this year
    filters:
      and:
        - status == "done"
        - completed.year == today().year
    order: [file.name, area, completed]
    sort: [{property: completed, direction: DESC}]
  - type: table
    name: Someday
    filters:
      and:
        - 'status == "idea" || status == "on-hold"'
    order: [file.name, area, file.mtime]
```

### People

```yaml
filters:
  and:
    - type == "person"
formulas:
  next_contact: 'if(last_contact && contact_every, last_contact + (contact_every + "d"), "")'
  overdue_days: 'if(formula.next_contact, ((today() - formula.next_contact) / 86400000).floor(), "")'
  bday_md: 'if(birthday, birthday.format("MM-DD"), "")'
  age: 'if(birthday, ((today() - birthday) / 31557600000).floor(), "")'
views:
  - type: table
    name: Contact due
    filters:
      and:
        - 'formula.next_contact && formula.next_contact <= today()'
        - relationship != "former"
    order: [file.name, relationship, last_contact, formula.overdue_days]
    sort: [{property: formula.overdue_days, direction: DESC}]
  - type: table
    name: Birthdays this month
    filters:
      and:
        - birthday.month == today().month
    order: [file.name, birthday, formula.age]
    sort: [{property: formula.bday_md, direction: ASC}]
  - type: cards
    name: Directory
    groupBy: {property: relationship, direction: ASC}
    order: [file.name, company, location, email]
    image: photo
    cardSize: 180
```

### Reading / sources

```yaml
filters:
  and:
    - type == "source"
formulas:
  stars: 'if(rating, "★".repeat(rating), "")'
  days_reading: 'if(started && !finished, ((today() - started) / 86400000).floor(), "")'
  progress: 'if(pages && pages_read, (pages_read / pages * 100).round(0) + "%", "")'
views:
  - type: table
    name: Reading now
    filters: {and: [status == "reading"]}
    order: [file.name, author, medium, started, formula.days_reading, formula.progress]
  - type: cards
    name: To read
    filters: {and: [status == "to-read"]}
    order: [file.name, author, medium]
    image: cover
    imageAspectRatio: 1.5
    cardSize: 160
    sort: [{property: file.ctime, direction: DESC}]
  - type: table
    name: Finished by year
    filters: {and: [status == "read"]}
    groupBy: {property: finished, direction: DESC}
    order: [file.name, author, medium, formula.stars, finished]
    summaries:
      rating: Average
  - type: table
    name: By topic
    filters: {and: [status != "abandoned"]}
    groupBy: {property: topics, direction: ASC}
    order: [file.name, medium, status]
```

### Ideas (evergreen pipeline)

```yaml
filters:
  and:
    - type == "note"
views:
  - type: table
    name: Seedlings to develop
    filters: {and: [status == "seedling"]}
    order: [file.name, topics, file.mtime]
    sort: [{property: file.mtime, direction: ASC}]
    limit: 25
  - type: list
    name: Evergreens
    filters: {and: [status == "evergreen"]}
    order: [file.name, topics]
  - type: table
    name: Recently touched
    order: [file.name, status, file.mtime]
    sort: [{property: file.mtime, direction: DESC}]
    limit: 30
```

### Meetings

```yaml
filters:
  and:
    - type == "meeting"
views:
  - type: table
    name: This week
    filters:
      and:
        - date >= today() - "7d"
    order: [file.name, date, project, attendees]
    sort: [{property: date, direction: DESC}]
  - type: table
    name: By project
    groupBy: {property: project, direction: ASC}
    order: [file.name, date, attendees]
    sort: [{property: date, direction: DESC}]
  - type: table
    name: With this person   # embed in a person note
    filters:
      and:
        - attendees.contains(this)
    order: [file.name, date, project]
    sort: [{property: date, direction: DESC}]
```

### Decisions

```yaml
filters:
  and:
    - type == "decision"
views:
  - type: table
    name: Open
    filters: {and: [status == "open"]}
    order: [file.name, date, options]
  - type: table
    name: Due for review
    filters:
      and:
        - status == "decided"
        - review_on <= today()
    order: [file.name, date, chosen, confidence, review_on]
  - type: table
    name: All
    order: [file.name, date, status, confidence]
    sort: [{property: date, direction: DESC}]
    summaries:
      confidence: Average
```

### Recipes

```yaml
filters:
  and:
    - type == "recipe"
formulas:
  total_min: '(prep_min + cook_min)'
  since_made: 'if(last_made, ((today() - last_made) / 86400000).floor(), "never")'
views:
  - type: cards
    name: Gallery
    groupBy: {property: cuisine, direction: ASC}
    order: [file.name, course, formula.total_min, rating]
    image: photo
    imageAspectRatio: 0.75
  - type: table
    name: Quick weeknight
    filters:
      and:
        - formula.total_min <= 35
        - course == "main"
    order: [file.name, cuisine, formula.total_min, rating]
    sort: [{property: rating, direction: DESC}]
  - type: table
    name: Not made in 60 days
    filters:
      and:
        - 'last_made.isEmpty() || last_made < today() - "60d"'
        - rating >= 4
    order: [file.name, cuisine, formula.since_made]
```

### Subscriptions

```yaml
filters:
  and:
    - type == "subscription"
formulas:
  monthly: 'if(billing == "yearly", (cost / 12).round(2), cost)'
  yearly: 'if(billing == "yearly", cost, (cost * 12).round(2))'
  renews_in: 'if(renews, ((renews - today()) / 86400000).floor(), "")'
views:
  - type: table
    name: Active
    filters: {and: [status == "active"]}
    order: [file.name, cost, billing, formula.monthly, formula.yearly, renews, formula.renews_in]
    sort: [{property: formula.monthly, direction: DESC}]
    summaries:
      formula.monthly: Sum
      formula.yearly: Sum
  - type: table
    name: Renewing in 30 days
    filters:
      and:
        - status == "active"
        - renews <= today() + "30d"
    order: [file.name, cost, renews, cancel_url]
```

### Workouts

```yaml
filters:
  and:
    - type == "workout"
views:
  - type: table
    name: Last 30 days
    filters: {and: [date >= today() - "30d"]}
    order: [file.name, date, kind, duration_min, distance_km, rpe]
    sort: [{property: date, direction: DESC}]
    summaries:
      duration_min: Sum
      distance_km: Sum
      rpe: Average
  - type: table
    name: By kind (this year)
    filters: {and: [date.year == today().year]}
    groupBy: {property: kind, direction: ASC}
    order: [file.name, date, duration_min, distance_km]
    summaries:
      duration_min: Sum
      distance_km: Sum
```

### Daily notes (mood/energy/sleep)

```yaml
filters:
  and:
    - type == "daily"
formulas:
  week: 'if(date, date.format("YYYY-[W]WW"), "")'
views:
  - type: table
    name: Last 30 days
    filters: {and: [date >= today() - "30d"]}
    order: [file.name, mood, energy, sleep_h, highlights]
    sort: [{property: date, direction: DESC}]
    summaries:
      mood: Average
      energy: Average
      sleep_h: Average
  - type: table
    name: This month by week
    filters: {and: [date.month == today().month, date.year == today().year]}
    groupBy: {property: formula.week, direction: DESC}
    order: [file.name, mood, energy, sleep_h]
    summaries:
      sleep_h: Average
```

### Attachments audit

```yaml
filters:
  and:
    - file.ext != "md"
    - file.ext != "base"
    - file.ext != "canvas"
formulas:
  mb: '(file.size / 1048576).toFixed(2)'
  linked: file.backlinks.length > 0
views:
  - type: table
    name: Largest
    order: [file.name, file.ext, formula.mb, file.folder]
    sort: [{property: file.size, direction: DESC}]
    limit: 100
  - type: table
    name: Possibly unused
    filters: {and: ['!formula.linked']}
    order: [file.name, file.ext, formula.mb]
```

### Sidebar "related to active note"

Open this base in a right-sidebar tab; `this` becomes the active note.

```yaml
views:
  - type: list
    name: Backlinks
    filters: {and: [file.hasLink(this.file)]}
    order: [file.name, type]
    sort: [{property: file.mtime, direction: DESC}]
  - type: list
    name: Same topics
    filters:
      and:
        - file != this.file
        - 'list(topics).filter(list(this.topics).contains(value)).length > 0'
    order: [file.name, status]
```

### Schema audit

```yaml
views:
  - type: table
    name: Missing type
    filters:
      and:
        - file.ext == "md"
        - type.isEmpty()
        - '!file.inFolder("Templates")'
        - '!file.inFolder("Journal")'
    order: [file.name, file.folder, file.mtime]
  - type: table
    name: Project status values
    filters: {and: [type == "project"]}
    groupBy: {property: status, direction: ASC}
    order: [file.name]
```

## Bases vs Dataview

| | Bases | Dataview |
| --- | --- | --- |
| Maintained by | Obsidian team (core) | Community (feature-frozen, maintenance only) |
| Data sources | Properties, file metadata | Properties, file metadata, **inline fields, tasks, list items** |
| Editing | **Inline** in table/kanban | Read-only (JS API can write) |
| Views | Table, cards, list, map, kanban (1.14), plugin views | Table, list, task, calendar, DataviewJS custom rendering |
| Computation | Formulas (expression language) | DQL functions + full JavaScript |
| Cross-note joins | Limited (`file()`, `link.asFile()`) | Full via JS |
| Aggregations | Summaries (footer), groupBy | `GROUP BY` with `rows`, JS |
| Performance | Fast, indexed, lazy | Fine to a few thousand notes; JS can be slow |
| Mobile | Native | Works; heavy JS slow |
| Export | CSV / clipboard | Via JS |
| Charts | Via plugin views | Via Charts + DataviewJS |
| Future | Actively expanding | Stable, no new features |

Rule: **Bases first.** Use Dataview when you need inline fields, task queries with custom rendering, joins, charts from computed data, or arbitrary JavaScript. Chapter 12 covers Dataview in the same depth.

### Migrating a Dataview table to a Base

```text
TABLE author, status, rating FROM "Sources" WHERE status = "reading" SORT started DESC
```

becomes

```yaml
filters:
  and:
    - file.inFolder("Sources")
    - status == "reading"
views:
  - type: table
    name: Reading
    order: [file.name, author, status, rating]
    sort: [{property: started, direction: DESC}]
```

Mapping: `FROM "folder"` → `file.inFolder()`; `FROM #tag` → `file.hasTag()`; `FROM [[Note]]` → `file.hasLink("Note")`; `WHERE` → filters; `SORT` → `sort`; `TABLE cols` → `order`; `GROUP BY` → `groupBy` (one level); `contains(list, x)` → `list.contains(x)`; `dateformat(d, "…")` → `d.format("…")`; `date(today)` → `today()`; `dur(7 days)` → `"7d"`; `length(rows)` → summaries `Filled`/`Unique` or `values.length`.

## Performance and hygiene

- Global filters that cut the vault early (`type == …`, `file.inFolder()`) make everything faster.
- Avoid `file.backlinks` and `file.properties` in large bases.
- A view embedded in a note re-renders when the note is opened; a dozen embedded bases in one dashboard is fine, fifty is not.
- Keep `.base` files in `Bases/`; name views as you would say them ("Contact due", "Renewing soon").
- The CLI's `obsidian base:query file=Projects view=Active format=csv` exports a view from the terminal — use it for backups, spreadsheets, or feeding scripts (Chapter 29).

## Key takeaways

- Bases are property-driven, editable, fast, core, and expanding (kanban in 1.14, plugin views). Default to them for every list-of-things.
- Learn the file format — filters (`and`/`or`/`not`), formulas (`if`, date math, list ops), views (`order`, `sort`, `groupBy`, `limit`, `summaries`) — so you can paste and adapt bases as fast as you can type.
- `this` changes meaning by context (base file / embedding note / active note) and enables area-scoped, person-scoped, and sidebar-related views.
- Summaries and group-by turn tables into dashboards without any scripting.
- Keep Dataview for inline fields, tasks, joins and JavaScript; migrate everything else.

## Next

[Chapter 11: Templates and Templater →](11-templates-and-templater.md)
