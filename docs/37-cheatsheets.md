# Cheat Sheets

The syntax references from across the guide, condensed onto one page each: default hotkeys, Obsidian Markdown, search operators, Bases, Dataview, Templater, Tasks, the CLI, and URIs. Print the ones you use; the rest are here for the search box.

## Default hotkeys (Windows/Linux; macOS: ++cmd++ for ++ctrl++)

| Action | Key |
| --- | --- |
| Command palette | ++ctrl+p++ |
| Quick switcher | ++ctrl+o++ |
| Search all files | ++ctrl+shift+f++ |
| Find in note / replace | ++ctrl+f++ / ++ctrl+h++ |
| New note | ++ctrl+n++ |
| Open settings | ++ctrl+comma++ |
| Toggle Reading/Editing | ++ctrl+e++ |
| Toggle bold / italic | ++ctrl+b++ / ++ctrl+i++ |
| Insert link / follow link | ++ctrl+k++ / ++alt+enter++ (new tab: ++ctrl+enter++) |
| Toggle checkbox | ++ctrl+l++ |
| Indent / outdent list | ++tab++ / ++shift+tab++ |
| Move line up / down | ++alt+up++ / ++alt+down++ |
| Fold / unfold | ++ctrl+up++ / ++ctrl+down++ |
| Back / forward | ++alt+left++ / ++alt+right++ |
| Next / previous tab | ++ctrl+tab++ / ++ctrl+shift+tab++ |
| Close tab / reopen closed | ++ctrl+w++ / ++ctrl+shift+t++ |
| Graph view | ++ctrl+g++ |
| Developer tools | ++ctrl+shift+i++ |
| Zoom in / out / reset | ++ctrl+plus++ / ++ctrl+minus++ / ++ctrl+0++ |
| Delete paragraph | ++ctrl+d++ |
| Add cursor | ++alt++ + click |
| Page preview | ++ctrl++ + hover |
| Escape to editor | ++esc++ |
| Suggested additions | Daily note, Insert template, Toggle sidebars, Move file, Add property, Tasks: create/edit, Templater: jump to cursor, Workspaces |

## Obsidian Markdown

```markdown
# H1 … ###### H6            *em* **strong** ~~strike~~ ==highlight== `code`
%%comment%%                 <u>u</u> <sup>x</sup> <sub>x</sub> <kbd>K</kbd>
- item / 1. item / - [ ] task / - [x] done / - [-] cancelled / - [/] in progress
> quote                     > [!type]± Title  (note tip info warning danger example quote abstract todo success question failure bug)
[[Note]] [[Note|text]] [[Note#Heading]] [[Note#^block]] [[#Heading]]     ^block-id at line end
![[Note]] ![[Note#Heading]] ![[img.png|300]] ![[file.pdf#page=3]] ![[Base.base#View]] ![[Board.canvas]]
[text](url) <url> [text](Note.md)          ![alt](https://…)
Footnote[^1]  ^[inline]   [^1]: text
$inline$  $$block$$        ```lang … ```   ~~~ … ~~~   fences: mermaid dataview dataviewjs tasks base query
| a | b |  \| escapes pipe   <br> line break in cell
---  (hr)   \*escape\*     Two trailing spaces or \ = hard break (strict mode)
---
key: value                 # frontmatter on line 1; quote "[[links]]" and "colons: in values"
tags: [a, b/nested]   aliases: [x]   cssclasses: [wide]
---
```

## Search operators

```text
word  "phrase"  a OR b  -not  (grouping)
file:  path:  content:  tag:#t  line:(a b)  block:(a b)  section:(a b)
task:  task-todo:  task-done:
[prop]  [prop:value]  ["key with space":v]  -[prop]
/regex/            Aa toggle = match case
Embedded: ```query … ```     Bookmark searches from the Bookmarks pane
```

## Bases (`.base` YAML)

```yaml
filters: {and: [type == "x", '!file.inFolder("Archive")', status != "done"]}   # and/or/not, strings or nested
formulas: {days: 'if(due, ((due - today()) / 86400000).round(0), "")'}
properties: {status: {displayName: Status}}
summaries: {custom: 'values.mean().round(2)'}
views:
  - type: table          # table | cards | list | map | kanban (1.14+)
    name: View
    filters: {and: [...]}
    order: [file.name, prop, formula.days]
    sort: [{property: due, direction: ASC}]
    groupBy: {property: area, direction: ASC}
    limit: 50
    summaries: {prop: Sum}   # Average Min Max Sum Range Median Stddev Earliest Latest Checked Unchecked Empty Filled Unique
    image: cover             # cards/kanban: imageFit, imageAspectRatio, cardSize
```

**Refs**: `prop` / `note.prop` / `note["a-b"]`, `file.name .basename .path .folder .ext .size .ctime .mtime .tags .links .embeds .backlinks .properties`, `formula.x`, `this` (base file / embedding note / active note in sidebar).
**Ops**: `+ - * / %`, `== != < > <= >=`, `!`, `&&`, `||`, date ± `"1d" "2w" "1M" "1y" "3h"`, `date - date` → ms.
**Global**: `now() today() date(s) duration(s) if(c,a,b) list(x) number(x) link(p,d) file(p) image(p) icon(n) html(s) min() max() random()`.
**String**: `.length .contains .containsAll .containsAny .startsWith .endsWith .lower .title .trim .slice .split .replace .repeat .reverse .isEmpty`.
**Number**: `.abs .ceil .floor .round(d) .toFixed(d)`. **Date**: `.year .month .day .hour .minute .date() .time() .format("YYYY-MM-DD") .relative()`.
**List**: `.length .contains .containsAll .containsAny .filter(value…) .map(value…) .reduce(acc…, init) .flat .join .reverse .slice .sort .unique .mean .median .stddev`.
**File**: `.asLink(d) .hasLink(f) .hasTag(...t) .hasProperty(n) .inFolder(f)`. **Link**: `.asFile() .linksTo(f)`. **Regex**: `/re/.matches(s)`.

## Dataview (DQL)

```text
TABLE [WITHOUT ID] a AS "A", b   |  LIST [expr]  |  TASK  |  CALENDAR datefield
FROM "Folder" / #tag / [[Note]] / outgoing([[Note]]) / csv("f.csv")   combine with AND OR -
WHERE cond    SORT f ASC|DESC    GROUP BY f    FLATTEN list AS x    LIMIT n
Fields: file.name .folder .path .link .size .ctime .cday .mtime .mday .tags .etags .inlinks .outlinks .aliases .tasks .lists .day
Dates: date(today|now|tomorrow|yesterday|sow|eow|som|eom|soy|eoy)  dur(7 days)  (a - b).days  dateformat(d, "yyyy-MM-dd")  striptime()
Funcs: contains icontains econtains length sum average min max round default choice filter(l,(x)=>…) map join sort reverse unique flat
       regextest regexmatch regexreplace replace lower upper split startswith endswith link elink embed meta typeof
Inline: `= this.prop`   `$= dv.current().file.mtime`
Inline fields: key:: value   [key:: value]   (key:: value)
```

```javascript
// DataviewJS
dv.pages('"Folder"').where(p => p.status === "active").sort(p => p.due).map(p => [p.file.link, p.due])
dv.table(headers, rows); dv.list(arr); dv.taskList(tasks, groupByFile); dv.header(n, t); dv.paragraph(md); dv.el(tag, text)
dv.date("today"); dv.duration("7d"); dv.fileLink(path); dv.view("Scripts/views/x", input); dv.io.csv(path); dv.query(dql)
// Luxon: d.plus({days:7}) d.diff(other, "days").days d.toFormat("yyyy-MM-dd") d.startOf("week")
```

## Templater

```text
<% expr %>   <%* code; tR += "out" %>   <%- trim -%>   <%+ dynamic %>
tp.date.now(fmt, offsetDaysOrISO, refStr, refFmt)  .tomorrow(fmt) .yesterday(fmt) .weekday(fmt, n, ref, refFmt)   moment(...)
tp.file.title .path(rel) .folder(rel) .content .tags .selection() .cursor(n) .cursor_append(t) .include("[[x]]")
        .exists(p) .find_tfile(n) .create_new(tplOrStr, name, open, folder) .rename(n) .move(p) .creation_date(f) .last_modified_date(f)
tp.frontmatter.key       tp.config.active_file / .run_mode / .target_file / .template_file
tp.system.prompt(text, default, throw, multiline)  .suggester(texts, items, throw, placeholder, limit)  .clipboard()
tp.web.daily_quote() .random_picture(size, q) .request(url, path)
tp.user.fn(...)   tp.obsidian.Notice / requestUrl   app.vault / app.metadataCache / app.fileManager.processFrontMatter(f, fm => …)
tp.hooks.on_all_templates_executed(cb)
Settings: trigger on new file ✓ · folder templates · file regex templates · startup templates · user scripts folder
```

## Tasks

```text
- [ ] text 📅 due ⏳ scheduled 🛫 start ➕ created ✅ done ❌ cancelled 🔁 every week [when done] 🔺⏫🔼🔽⏬ priority 🆔 id ⛔ blockedBy #tag
```

```text
Filters: done | not done | status.type is IN_PROGRESS
  due|scheduled|starts|happens|created|done  (today|tomorrow|yesterday|before X|after X|on X|this week|next month|in 3 days|on or before …)
  has due date | no due date | is recurring | priority is (above|below) high | is blocked | is not blocked | is blocking
  path includes X | folder includes | filename includes | heading includes | description includes | tags include #x | tag does not include
  (a) OR (b) | NOT (a) | filter by function task.due.moment?.isoWeekday() === 1 | filter by function task.file.property("type") === "project"
Sort: sort by urgency|due|priority|status|path|description|scheduled|created|done [reverse] | sort by function …
Group: group by due|folder|filename|heading|priority|tags|status.type | group by function task.due.category.groupText
Layout: short mode | show tree | hide (due date|recurrence rule|backlink|edit button|tags|priority|postpone button) | limit N | limit groups N | explain
Placeholders: {{query.file.path}} {{query.file.folder}} {{query.file.property('x')}}
```

## Obsidian CLI

```bash
obsidian [vault=Name] <command> param=value flag [--copy]      # TUI: obsidian
help version reload restart | vault vaults vault:open
file files folder folders open create read append prepend move rename delete
daily daily:path daily:read daily:append content= daily:prepend
search query= [path= limit= format= total case] search:context query= search:open
tasks [todo done daily file= status= verbose format=] task ref=path:line [toggle done todo status=]
properties [active file= name= counts sort=count] property:set name= value= [type=] property:read property:remove aliases tags tag name=
backlinks links unresolved orphans deadends outline
bases base:views base:create base:query file= [view= format=json|csv|tsv|md|paths]
bookmarks bookmark commands command id= hotkeys hotkey id=
templates template:read name= [resolve] template:insert name= unique
plugins plugins:enabled plugins:restrict on|off plugin id= plugin:enable plugin:disable plugin:install id= [enable] plugin:uninstall plugin:reload
themes theme theme:set theme:install snippets snippets:enabled snippet:enable snippet:disable
diff [file= from= to=] history history:list history:read history:restore version= history:open
sync on|off sync:status sync:history sync:read sync:restore sync:open sync:deleted
publish:site publish:list publish:status publish:add [changed] publish:remove publish:open
workspace workspaces workspace:save workspace:load name= workspace:delete tabs tab:open recents
random random:read web url= wordcount
devtools dev:debug dev:cdp dev:errors dev:screenshot path= dev:console dev:css selector= dev:dom selector= dev:mobile eval code=
```

## URIs

```text
obsidian://open?vault=V&file=Path/Note          obsidian://open?path=/abs/path.md
obsidian://new?vault=V&name=Folder/Note&content=…[&append=true|prepend=true|overwrite=true|silent=true|clipboard=true]
obsidian://search?vault=V&query=…               obsidian://unique?vault=V&name=…&content=…
Advanced URI: obsidian://adv-uri?vault=V&daily=true&heading=Log&data=…&mode=append
              …&filepath=Note.md&frontmatterkey=status&data=done   …&commandid=…   …&uid=…   …&openmode=split|tab|window|silent
URL-encode: space %20  newline %0A  # %23      1.13: confirmation dialog + allow list
```

## Property schema (reference vault)

```yaml
type: daily|weekly|monthly|quarterly|yearly|project|area|goal|person|meeting|source|note|moc|decision|belief|recipe|workout|health-event|subscription|account|networth|asset|document|trip|place|habit|pet|vehicle|doc|scene|character|draft|quote
# common: created tags aliases cssclasses
# project: status(idea|active|on-hold|done|dropped) area goal priority(1-3) start due completed reviewed
# person: relationship birthday last_contact contact_every location company photo
# source: medium(book|article|paper|podcast|video|course) author status(to-read|reading|read|abandoned) rating started finished topics url cover
# note: status(seedling|budding|evergreen) topics sources
# decision: date status(open|decided|reviewed) options chosen confidence review_on
```

## Key takeaways

- Everything on this page is covered in depth elsewhere; use it as the quick reference once the concepts are familiar.
- The four syntaxes worth memorizing: Markdown links/embeds/callouts, Bases filters and formulas, Tasks signifiers and filters, and the CLI's `create/append/search/property:set`.

## Next

[Chapter 38: Glossary and Resources →](38-resources-and-glossary.md)
