# Templates and Templater

Templates are how a vault enforces its own schema without willpower. Core Templates handles static text with a date; **Templater** (community, by SilentVoid13) adds a full scripting layer — dates with arithmetic, prompts, file operations, conditional content, folder-based auto-templates, and user-defined JavaScript. Almost every "how do I automate X in Obsidian" question that does not involve external tools is answered by Templater. This chapter covers the syntax and modules exhaustively, the patterns that matter, and a full set of production templates for the reference vault.

## Core Templates (recap)

Settings: template folder, date/time formats. Insert with *Templates: Insert template*. Placeholders: `{{title}}`, `{{date}}`, `{{time}}`, `{{date:YYYY-MM-DD}}` (Moment format). Used by Daily notes, Unique note creator, CLI `create template=…`. Keep it enabled; write everything real in Templater.

## Templater: setup

Install **Templater** from the community directory. Settings that matter:

| Setting | Recommended | Why |
| --- | --- | --- |
| Template folder location | `Templates` | Same folder as core Templates. |
| Syntax highlighting | On | |
| Automatic jump to cursor | On | Enables `<% tp.file.cursor() %>`. |
| **Trigger Templater on new file creation** | **On** | The key setting: every new note (from quick switcher, link click, daily notes, Unique note creator, URI, CLI) gets processed. |
| Enable folder templates | On | Map folders → templates (see below). |
| Enable file regex templates | Optional | Match file *names* to templates (e.g. `^\d{4}-W\d{2}$` → weekly template). Mutually exclusive with folder templates in older versions; newer versions allow both. |
| Startup templates | Optional | Run a template when Obsidian starts (regenerate Home dashboard). |
| Template hotkeys | Assign for daily, meeting, person, quick capture | Each template can have its own hotkey. |
| User script functions | Point to `Scripts/templater` | Enables `tp.user.*`. |
| System command user functions | Off unless needed | Runs shell commands — powerful but a security surface. |

**Daily notes integration.** Either set the Daily notes core plugin's template to your Templater file (Templater processes it because "trigger on new file creation" is on), or use Templater's own daily-note command. Both work; the first is simpler.

!!! warning "Templater and core Templates use different syntax"
    Core: `{{date}}`. Templater: `<% tp.date.now("YYYY-MM-DD") %>`. If a template contains `{{date}}` and Templater processes it, `{{date}}` stays literal. Convert templates fully when you adopt Templater.

## Syntax

```text
<% expression %>          output the value
<%* code %>               execute JavaScript, no output (use tR += "text" to output)
<%- expression -%>        whitespace control (trim newline before/after)
<%_ … _%>                 trim all whitespace
<% "text" %>              string literal
```

Everything inside `<% %>` is JavaScript. `tp` is the Templater object. Multi-line code blocks use `<%* … %>`; to emit text from them, append to the special string `tR`:

```javascript
<%*
const status = await tp.system.suggester(["active", "idea", "on-hold"], ["active", "idea", "on-hold"]);
tR += `status: ${status}\n`;
%>
```

## The `tp` modules

### `tp.date`

| Function | Purpose |
| --- | --- |
| `tp.date.now(format?, offset?, reference?, reference_format?)` | Now, formatted (Moment). `offset` in days (number) or ISO duration string (`"P1M"`, `"-P1W"`). `reference` lets you compute relative to another date string. |
| `tp.date.tomorrow(format?)` / `tp.date.yesterday(format?)` | |
| `tp.date.weekday(format, weekday, reference?, reference_format?)` | Day of the current week; `weekday` 0 = Monday … 6 = Sunday (locale-dependent). |
| `moment` | Full Moment.js is available globally in Templater code. |

```text
<% tp.date.now("YYYY-MM-DD") %>
<% tp.date.now("dddd, D MMMM YYYY") %>                     → Saturday, 6 September 2026
<% tp.date.now("YYYY-MM-DD", 7) %>                          → +7 days
<% tp.date.now("YYYY-MM-DD", "P1M") %>                      → +1 month
<% tp.date.now("YYYY-[W]WW") %>                             → 2026-W36
<% tp.date.now("YYYY-MM-DD", -1, tp.file.title, "YYYY-MM-DD") %>   → the day before this daily note's date
<% tp.date.weekday("YYYY-MM-DD", 0) %>                      → Monday of this week
<% moment(tp.file.title, "YYYY-MM-DD").add(1, "week").format("YYYY-[W]WW") %>
```

### `tp.file`

| Function | Purpose |
| --- | --- |
| `tp.file.title` | Filename without extension. |
| `tp.file.path(relative?)` | Path. |
| `tp.file.folder(relative?)` | Folder name (or path). |
| `tp.file.content` | Current content. |
| `tp.file.creation_date(format?)` / `tp.file.last_modified_date(format?)` | |
| `tp.file.tags` | Tags in the file (array). |
| `tp.file.selection()` | Selected text at insertion time. |
| `tp.file.cursor(order?)` | Where the cursor lands after insertion; multiple cursors with ordering. |
| `tp.file.cursor_append(text)` | Append at cursor. |
| `tp.file.include(link_or_path)` | Include another template/file — **templates inside templates**. `tp.file.include("[[tpl-meeting-checklist]]")`. |
| `tp.file.exists(path)` | Boolean. |
| `tp.file.find_tfile(name)` | Get a TFile for other API calls. |
| `tp.file.create_new(template_or_content, filename?, open_new?, folder?)` | **Create another note** from a template. |
| `tp.file.rename(new_title)` | Rename the current note (e.g. after prompting for a title). |
| `tp.file.move(new_path)` | Move to a folder (`"People/" + tp.file.title`). |

### `tp.frontmatter`

Read the current note's properties: `tp.frontmatter.status`, `tp.frontmatter["due"]`. Works after the file exists; in a new-file template the frontmatter is whatever the template itself produced above the call — so put reads below the YAML block, or better, compute values in JS first and emit the YAML.

### `tp.system`

| Function | Purpose |
| --- | --- |
| `tp.system.prompt(prompt_text?, default?, throw_on_cancel?, multiline?)` | Text input dialog. |
| `tp.system.suggester(text_items, items, throw_on_cancel?, placeholder?, limit?)` | Fuzzy pick from a list; `text_items` shown, `items` returned. Both can be arrays or functions. |
| `tp.system.clipboard()` | Clipboard contents. |

The suggester over vault files is the workhorse:

```javascript
<%*
const people = app.vault.getMarkdownFiles().filter(f => f.path.startsWith("People/"));
const person = await tp.system.suggester(f => f.basename, people, false, "Who did you meet?");
tR += person ? `attendees: ["[[${person.basename}]]"]` : "attendees: []";
%>
```

### `tp.web`

`tp.web.daily_quote()`, `tp.web.random_picture(size?, query?, include_size?)`, `tp.web.request(url, path?)` (fetch JSON and optionally pick a path). Use sparingly — templates should not fail offline.

### `tp.obsidian` and `app`

`tp.obsidian` exposes the Obsidian API module (Notice, requestUrl, normalizePath, etc.); `app` is the global app object (vault, metadataCache, workspace, fileManager). This means a template can do anything a plugin can:

```javascript
<%*
const file = tp.file.find_tfile("Projects/Alpha");
await app.fileManager.processFrontMatter(file, fm => { fm.reviewed = tp.date.now("YYYY-MM-DD"); });
new tp.obsidian.Notice("Alpha marked reviewed");
%>
```

### `tp.hooks`

`tp.hooks.on_all_templates_executed(callback)` — run code after the template finishes (e.g. move the file *after* the rename has happened).

### `tp.config`

`tp.config.active_file`, `tp.config.run_mode`, `tp.config.target_file`, `tp.config.template_file`. Useful for templates that behave differently when inserted vs. applied on creation.

### `tp.user`

Your own functions. Put `.js` files in the user-scripts folder; each exports one function:

```javascript
// Scripts/templater/slug.js
function slug(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}
module.exports = slug;
```

Call with `<% tp.user.slug(tp.file.title) %>`. Functions receive `tp` if you pass it (`tp.user.fn(tp, …)`) — anything the template can do, a user script can do, and you keep templates readable.

## Patterns

### Folder templates

Settings → Folder templates: `People/` → `tpl-person`, `Projects/` → `tpl-project`, `Sources/Books/` → `tpl-book`, `Journal/Daily/` → `tpl-daily`, `Work/Meetings/` → `tpl-meeting`, `Inbox/` → `tpl-inbox`. Now *creating a note in a folder types it* — from the file explorer, from a link click when the new-note location is that folder, from the CLI, from Bases' *New* button. This is the single most valuable Templater feature for schema discipline.

### Ask-then-file ("one command to create anything")

A single `tpl-new` template with a hotkey: pick a type, prompt for a title, create the note from the type's template in the right folder.

```javascript
<%*
const types = {
  "Project": ["Projects", "tpl-project"],
  "Person": ["People", "tpl-person"],
  "Source (book)": ["Sources/Books", "tpl-book"],
  "Idea note": ["Notes", "tpl-note"],
  "Meeting": ["Work/Meetings", "tpl-meeting"],
  "Decision": ["Mind/Decisions", "tpl-decision"],
  "Recipe": ["Life/Recipes", "tpl-recipe"],
};
const choice = await tp.system.suggester(Object.keys(types), Object.keys(types), false, "Create what?");
if (!choice) return;
let title = await tp.system.prompt("Title");
if (!title) return;
const [folder, tplName] = types[choice];
if (choice === "Meeting") title = tp.date.now("YYYY-MM-DD") + " " + title;
const tpl = tp.file.find_tfile(tplName);
await tp.file.create_new(tpl, title, true, app.vault.getAbstractFileByPath(folder));
%>
```

Because the target template is applied by `create_new`, the folder template is not needed for this path — but keep both so either entrance works.

### Prompt-driven frontmatter

```javascript
---
type: project
status: <% await tp.system.suggester(["active","idea","on-hold"], ["active","idea","on-hold"]) %>
area: "[[<% (await tp.system.suggester(f => f.basename, app.vault.getMarkdownFiles().filter(f => f.path.startsWith("Areas/")))).basename %>]]"
priority: <% await tp.system.suggester(["1 — high","2 — normal","3 — low"], [1,2,3]) %>
start: <% tp.date.now("YYYY-MM-DD") %>
due:
---
```

Keep prompts to two or three per template; more and you will avoid creating notes.

### Rename from a prompt (for untitled captures)

```javascript
<%*
if (tp.file.title.startsWith("Untitled")) {
  const t = await tp.system.prompt("Note title");
  if (t) await tp.file.rename(t);
}
%>
```

### Move after creation

```javascript
<%* await tp.file.move("/Notes/" + tp.file.title) %>
```

### Conditional sections

```javascript
<%* if (tp.date.now("d") === "1") { %>
## Monday planning
- [ ] Review calendar for the week
<%* } %>
<%* if (tp.date.now("D") === "1") tR += "## Monthly review due\n" %>
```

### Include shared fragments

`<% tp.file.include("[[frag-review-checklist]]") %>` — the checklist lives once; every weekly note gets the current version at creation.

### Cursor placement

```text
## Notes
<% tp.file.cursor(1) %>

## Actions
- [ ] <% tp.file.cursor(2) %>
```

The *Jump to next cursor location* command (assign ++ctrl+j++… or any hotkey) hops between them.

### Insert into another note (append to a log)

```javascript
<%*
const daily = tp.file.find_tfile(tp.date.now("YYYY-MM-DD"));
if (daily) await app.vault.append(daily, `\n- ${tp.date.now("HH:mm")} Created [[${tp.file.title}]]`);
%>
```

### Dynamic commands (execute on view, not on creation)

Templater's **dynamic commands** `<%+ … %>` re-evaluate every time the note is rendered in Reading view — a live clock or "days since" counter. Rarely needed; Dataview inline `= …` and Bases formulas cover most live needs.

### Startup template (regenerate Home)

Settings → Startup templates → `tpl-home-refresh`, which rewrites the date links in `00 Home.md`:

```javascript
<%*
const home = tp.file.find_tfile("00 Home");
let c = await app.vault.read(home);
c = c.replace(/\*\*Today:\*\* \[\[.*?\]\]/, `**Today:** [[${tp.date.now("YYYY-MM-DD")}]]`)
     .replace(/\*\*Week:\*\* \[\[.*?\]\]/, `**Week:** [[${tp.date.now("YYYY-[W]WW")}]]`);
await app.vault.modify(home, c);
%>
```

## The production template set

These are the Templater versions of the Chapter 8 skeletons plus a few more. Navigation links assume ISO weeks and the `Journal/` folders; adjust formats to your conventions.

### `tpl-daily`

```markdown
---
type: daily
date: <% tp.date.now("YYYY-MM-DD", 0, tp.file.title, "YYYY-MM-DD") %>
mood:
energy:
sleep_h:
tags: []
---
« [[<% tp.date.now("YYYY-MM-DD", -1, tp.file.title, "YYYY-MM-DD") %>]] · [[<% moment(tp.file.title, "YYYY-MM-DD").format("YYYY-[W]WW") %>|week]] · [[<% tp.date.now("YYYY-MM-DD", 1, tp.file.title, "YYYY-MM-DD") %>]] »

## Plan
```tasks
not done
(due on <% tp.date.now("YYYY-MM-DD", 0, tp.file.title, "YYYY-MM-DD") %>) OR (scheduled on <% tp.date.now("YYYY-MM-DD", 0, tp.file.title, "YYYY-MM-DD") %>) OR (due before <% tp.date.now("YYYY-MM-DD", 0, tp.file.title, "YYYY-MM-DD") %>)
sort by priority
short mode
```
- [ ] <% tp.file.cursor(1) %>

## Log
- <% tp.date.now("HH:mm") %>

## Notes

## Evening
- Went well:
- Could improve:
- Grateful for:
```

### `tpl-weekly` (file regex `^\d{4}-W\d{2}$` or Periodic Notes)

```markdown
---
type: weekly
period_start: <% moment(tp.file.title, "YYYY-[W]WW").startOf("isoWeek").format("YYYY-MM-DD") %>
period_end: <% moment(tp.file.title, "YYYY-[W]WW").endOf("isoWeek").format("YYYY-MM-DD") %>
tags: []
---
« [[<% moment(tp.file.title, "YYYY-[W]WW").subtract(1, "week").format("YYYY-[W]WW") %>]] · [[<% moment(tp.file.title, "YYYY-[W]WW").format("YYYY-MM") %>|month]] · [[<% moment(tp.file.title, "YYYY-[W]WW").add(1, "week").format("YYYY-[W]WW") %>]] »

## Days
<%*
const start = moment(tp.file.title, "YYYY-[W]WW").startOf("isoWeek");
for (let i = 0; i < 7; i++) tR += `- [[${start.clone().add(i, "days").format("YYYY-MM-DD")}|${start.clone().add(i, "days").format("ddd D")}]]\n`;
%>

## Focus this week
1. <% tp.file.cursor(1) %>
2.
3.

## Review (fill on Sunday)
<% tp.file.include("[[frag-weekly-review]]") %>

## Mood & energy
```base
filters:
  and:
    - type == "daily"
    - date >= this.period_start
    - date <= this.period_end
views:
  - type: table
    name: Week
    order: [file.name, mood, energy, sleep_h]
    summaries: {mood: Average, energy: Average, sleep_h: Average}
```
```

### `frag-weekly-review`

```markdown
- [ ] Inbox to zero (`Inbox/`, email, downloads, photos)
- [ ] Daily notes of the week skimmed; loose tasks captured or dropped
- [ ] Every active project has a next action
- [ ] Waiting-for list reviewed
- [ ] Calendar: last week (anything to capture?) and next two weeks
- [ ] Someday/maybe skimmed
- [ ] People: contact-due list
- [ ] Health, finance, home quick check
- [ ] Three wins · one lesson · one thing to change
```

### `tpl-monthly`

```markdown
---
type: monthly
period_start: <% moment(tp.file.title, "YYYY-MM").startOf("month").format("YYYY-MM-DD") %>
period_end: <% moment(tp.file.title, "YYYY-MM").endOf("month").format("YYYY-MM-DD") %>
---
« [[<% moment(tp.file.title, "YYYY-MM").subtract(1, "month").format("YYYY-MM") %>]] · [[<% moment(tp.file.title, "YYYY-MM").format("YYYY-[Q]Q") %>|quarter]] · [[<% moment(tp.file.title, "YYYY-MM").add(1, "month").format("YYYY-MM") %>]] »

## Weeks
<%*
const s = moment(tp.file.title, "YYYY-MM").startOf("month").startOf("isoWeek");
const e = moment(tp.file.title, "YYYY-MM").endOf("month");
for (let w = s.clone(); w.isSameOrBefore(e); w.add(1, "week")) tR += `- [[${w.format("YYYY-[W]WW")}]]\n`;
%>

## Goals for the month
- [ ] <% tp.file.cursor() %>

## Areas check-in
<%*
const areas = app.vault.getMarkdownFiles().filter(f => f.path.startsWith("Areas/")).sort((a,b)=>a.basename.localeCompare(b.basename));
for (const a of areas) tR += `### [[${a.basename}]]\n- \n\n`;
%>

## Month in review
- Highlights:
- Lowlights:
- Finished projects: ![[Projects.base#Done this year]]
```

### `tpl-project`

```markdown
---
type: project
status: <% await tp.system.suggester(["active","idea","on-hold"], ["active","idea","on-hold"], false, "Status") %>
area: "[[<% (await tp.system.suggester(f => f.basename, app.vault.getMarkdownFiles().filter(f => f.path.startsWith("Areas/")), false, "Area")).basename %>]]"
goal:
priority: 2
start: <% tp.date.now("YYYY-MM-DD") %>
due:
completed:
reviewed: <% tp.date.now("YYYY-MM-DD") %>
tags: []
---
## Outcome
<% tp.file.cursor(1) %>

## Next actions
- [ ]

## Log
- <% tp.date.now("YYYY-MM-DD") %> — Created.

## Meetings
![[Meetings.base#By project]]

## Notes & links
```

### `tpl-person`

```markdown
---
type: person
relationship: <% await tp.system.suggester(["family","friend","colleague","acquaintance","professional"], ["family","friend","colleague","acquaintance","professional"]) %>
birthday:
email:
phone:
company:
location:
last_contact: <% tp.date.now("YYYY-MM-DD") %>
contact_every: 60
photo:
aliases: []
tags: []
---
## About
<% tp.file.cursor() %>

## Interactions
![[Meetings.base#With this person]]

## Gift ideas & preferences

## Connections
```

### `tpl-book`

```markdown
---
type: source
medium: book
author: []
status: to-read
rating:
started:
finished:
pages:
pages_read:
isbn:
cover:
url:
topics: []
tags: []
---
> [!summary] In one paragraph
>

## Key ideas (own words)
- <% tp.file.cursor() %>

## Highlights & notes

## Quotes
```

(The **Book Search** plugin fills author/cover/ISBN/pages from an online lookup and then applies this template — see Chapter 17.)

### `tpl-note` (idea)

```markdown
---
type: note
status: seedling
topics: []
sources: []
created: <% tp.date.now("YYYY-MM-DD") %>
tags: []
---
<% tp.file.cursor() %>

## Related
-
```

### `tpl-meeting`

```markdown
---
type: meeting
date: <% tp.date.now("YYYY-MM-DD") %>
attendees: <%* const ppl = app.vault.getMarkdownFiles().filter(f => f.path.startsWith("People/")); const p = await tp.system.suggester(f => f.basename, ppl, false, "Main attendee (Esc to skip)"); tR += p ? `["[[${p.basename}]]"]` : "[]"; %>
project: <%* const prj = app.vault.getMarkdownFiles().filter(f => f.path.startsWith("Projects/")); const q = await tp.system.suggester(f => f.basename, prj, false, "Project (Esc to skip)"); tR += q ? `"[[${q.basename}]]"` : '""'; %>
decisions: []
next_meeting:
tags: []
---
## Agenda
- <% tp.file.cursor(1) %>

## Notes

## Decisions

## Actions
- [ ] 👤 
- [ ] Me — 
```

### `tpl-decision`

```markdown
---
type: decision
date: <% tp.date.now("YYYY-MM-DD") %>
status: open
confidence:
review_on: <% tp.date.now("YYYY-MM-DD", "P6M") %>
options: []
chosen:
tags: []
---
## Context
<% tp.file.cursor() %>

## Options considered
| Option | Pros | Cons | Reversible? |
| --- | --- | --- | --- |

## Decision & reasoning

## What would change my mind

## Expected outcome (check on review_on)

## Review
```

### `tpl-recipe`

```markdown
---
type: recipe
cuisine:
course: main
servings: 2
prep_min:
cook_min:
rating:
last_made:
photo:
source:
tags: []
---
## Ingredients
- <% tp.file.cursor() %>

## Method
1.

## Notes & variations
```

### `tpl-workout`

```markdown
---
type: workout
date: <% tp.date.now("YYYY-MM-DD") %>
kind: <% await tp.system.suggester(["strength","run","bike","swim","yoga","walk","other"], ["strength","run","bike","swim","yoga","walk","other"]) %>
duration_min:
distance_km:
rpe:
tags: []
---
| Exercise | Set 1 | Set 2 | Set 3 | Notes |
| --- | --- | --- | --- | --- |
| <% tp.file.cursor() %> | | | | |

## How it felt
```

### `tpl-inbox` (quick capture)

```markdown
---
type: inbox
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
source: <% tp.config.run_mode === 0 ? "manual" : "auto" %>
---
<% tp.file.cursor() %>
```

### `tpl-quick-task` (insert into daily note from anywhere)

Bind to a hotkey; works from any note:

```javascript
<%*
const text = await tp.system.prompt("Task");
if (!text) return;
const dailyName = tp.date.now("YYYY-MM-DD");
let daily = tp.file.find_tfile(dailyName);
if (!daily) {
  const tpl = tp.file.find_tfile("tpl-daily");
  daily = await tp.file.create_new(tpl, dailyName, false, app.vault.getAbstractFileByPath("Journal/Daily"));
}
let content = await app.vault.read(daily);
content = content.replace(/## Plan\n/, `## Plan\n- [ ] ${text}\n`);
await app.vault.modify(daily, content);
new tp.obsidian.Notice("Added to today: " + text);
%>
```

## Templater vs QuickAdd vs Meta Bind

- **Templater**: templates + scripting; runs on file creation; the foundation.
- **QuickAdd**: a *command builder* — captures (append text to a target file with a format), templates (create from template into a folder with a name format), macros (chains of commands/scripts/prompts), multis (menus). QuickAdd is faster to configure for "append a line to my daily note under ## Log" or "create a book note with these prompts" and has a nicer choice menu. Many power users run both: Templater for templates, QuickAdd for capture commands and macros. QuickAdd can call Templater templates.
- **Meta Bind**: in-note **input widgets** bound to properties (`INPUT[toggle:done]`, `INPUT[inlineSelect(option(a), option(b)):status]`, `INPUT[date:due]`, `INPUT[slider(minValue(1), maxValue(10)):mood]`) and buttons that run commands/JS. It is how you make a daily note *form* on mobile without editing YAML.

## Debugging templates

- A template that errors shows a Notice with the JS error; open the developer console (++ctrl+shift+i++) for the stack trace.
- YAML errors after generation: usually an unquoted `[[link]]`, a stray colon, or a prompt cancelled (returning `null` into YAML). Guard: `const x = await …; if (!x) return;` or emit a default.
- "Template not applied" on new files: check *Trigger Templater on new file creation* and that the folder template mapping matches the actual folder path (case-sensitive).
- Templates with `await` must be inside `<%* %>` blocks or single-expression `<% await … %>`.
- Templater runs `tp.file.rename`/`move` asynchronously; use `tp.hooks.on_all_templates_executed` if later code depends on the new path.

## Key takeaways

- Templater's *Trigger on new file creation* plus folder templates makes every new note typed and structured with zero effort.
- Learn `tp.date.now` (with offsets and reference dates), `tp.system.suggester`/`prompt`, `tp.file.create_new/rename/move/include`, `tp.file.cursor`, and `tR` — that is 90% of daily use.
- Templates can call the full Obsidian API (`app`, `tp.obsidian`) and your own `tp.user` scripts; keep templates readable by moving logic to scripts.
- Use a single "create anything" command, keep prompts to a few per template, and include shared fragments so checklists live in one place.
- Pair with QuickAdd for capture commands and Meta Bind for in-note inputs.

## Next

[Chapter 12: Dataview — Queries and Scripting →](12-dataview.md)
