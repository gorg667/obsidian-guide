# Automation and Integrations

Because a vault is a folder of text files, anything that can write a file can write to your vault — and because Obsidian exposes a URI scheme, a command-line interface (1.12), and (via plugins) a REST API and shell access, anything can also trigger Obsidian itself. This chapter is the complete automation toolkit: the `obsidian://` URI scheme and Advanced URI, the Obsidian CLI with a full command cheat sheet and working scripts, Shell commands, the Local REST API, launcher integrations (Raycast, Alfred, AutoHotkey), Apple Shortcuts and Tasker, the Web Clipper and its Interpreter, and common integration recipes (calendar → meeting notes, email → inbox, Readwise, Strava, Letterboxd).

## The automation surfaces

| Surface | Direction | Needs Obsidian running? | Platforms | Use for |
| --- | --- | --- | --- | --- |
| **Write files to the vault folder** | in | No (indexed on next open/focus) | All | The most robust automation: scripts, Shortcuts, Tasker, cron, cloud functions writing Markdown |
| **`obsidian://` URIs** | in | Launches it | All | Open/create/append notes, search; from browsers, launchers, other apps |
| **Advanced URI plugin** | in | Launches it | All | Everything the core URI cannot: append to headings, set properties, run commands, open by UID, daily notes |
| **Obsidian CLI** (1.12+) | in/out | Yes (launches if not) | Desktop | Scripting: read/create/append/search/tasks/properties/bases/plugins/sync/publish/dev |
| **Shell commands plugin** | out | Yes | Desktop | Run scripts from inside Obsidian with note variables; output to notes |
| **Local REST API plugin** | in/out | Yes | Desktop (mobile experimental) | HTTP access for external tools, MCP servers, launchers |
| **Templater / QuickAdd / DataviewJS** | internal | Yes | All | Automation inside notes and commands (Chapters 11–12) |
| **Web Clipper** | in | No (writes via URI or file) | Browser | Capture from the web with templates and AI extraction |
| **Share Sheet / share intent** | in | No | Mobile | Capture from any app (Chapter 27) |

Rule: **prefer writing files** for anything that runs unattended (cron, webhooks); use URIs/CLI when you need Obsidian to *do* something (open, run a command, use a template's logic).

## The `obsidian://` URI scheme (core)

```text
obsidian://open?vault=Main&file=Projects/Alpha
obsidian://open?path=/absolute/path/to/note.md
obsidian://new?vault=Main&name=Inbox/Quick%20note&content=Hello%0A-%20item
obsidian://new?vault=Main&file=Journal/Daily/2026-09-06&append=true&content=...   (append to existing)
obsidian://new?vault=Main&name=Note&silent=true      (create without opening)
obsidian://new?vault=Main&name=Note&prepend=true&content=...
obsidian://new?vault=Main&name=Note&overwrite=true&content=...
obsidian://new?vault=Main&clipboard=true             (content from clipboard)
obsidian://search?vault=Main&query=tag%3A%23waiting
obsidian://hook-get-address                          (Hookmark integration)
obsidian://unique?vault=Main&name=...&content=...    (1.12: Unique note creator; paneType=tab|split|window)
```

Parameters must be URL-encoded (`%20` space, `%0A` newline, `%23` `#`). `vault` is the vault *name* (or its ID). Since 1.13, every URI action shows a **confirmation dialog** the first time; choose *Don't ask again* to allow-list that action type (managed in Settings).

## Advanced URI (plugin)

`obsidian://adv-uri?vault=Main&…` with far more parameters:

| Goal | URI |
| --- | --- |
| Append to today's daily note under a heading | `obsidian://adv-uri?vault=Main&daily=true&heading=Log&data=-%2014%3A32%20text&mode=append` |
| Prepend/append/overwrite/new | `…&filepath=Inbox/Quick.md&data=…&mode=append` (modes: `append`, `prepend`, `overwrite`, `new`) |
| Open by UID (survives renames) | `…&uid=abc-123` (plugin writes a `uid` property) |
| Set a property | `…&filepath=Projects/Alpha.md&frontmatterkey=status&data=done` |
| Run a command | `…&commandid=daily-notes` or `…&commandname=Templater%3A%20Open%20insert%20template%20modal` |
| Open in new pane/window | `…&openmode=split` / `tab` / `window` / `popover` / `silent` |
| Search & replace | `…&filepath=…&search=foo&replace=bar` |
| Open a specific block/heading | `…&filepath=Note.md&heading=Section` or `&block=id` |
| Navigate workspace | `…&workspace=Planning` |
| Run a template's logic | Not directly; run a Templater/QuickAdd command via `commandid=` |

The plugin adds commands *Copy URI for current file / block / daily note / command* — use them to generate URIs without memorizing the syntax. Cross-vault links inside notes are also Advanced URIs.

## Obsidian CLI (1.12+)

Enable in Settings → General → *Command line interface* and let it register the PATH (installer 1.12.7+; macOS symlinks `/usr/local/bin/obsidian`, Linux copies to `~/.local/bin/obsidian`, Windows adds `Obsidian.com` redirector). Obsidian must be running (the first command launches it). Syntax: `obsidian <command> param=value flag`; quote values with spaces; `\n` for newlines; `vault=Name` as the first parameter targets a vault; if your terminal's cwd is a vault, that vault is used. `--copy` copies output to the clipboard. Run `obsidian` alone for the TUI with autocomplete and history.

### Command cheat sheet

| Area | Commands |
| --- | --- |
| General | `help [command]`, `version`, `reload`, `restart` |
| Vault | `vault [info=name\|path\|files\|folders\|size]`, `vaults [verbose]`, `vault:open name=…` (TUI) |
| Files | `file [file=\|path=]`, `files [folder= ext= total]`, `folder path= [info=]`, `folders`, `open file= [newtab]`, `create name=\|path= [content= template= overwrite open newtab]`, `read [file=]`, `append content= [file= inline]`, `prepend content=`, `move to=`, `rename name=`, `delete [permanent]` |
| Daily | `daily [paneType=]`, `daily:path`, `daily:read`, `daily:append content= [inline open]`, `daily:prepend content=` |
| Search | `search query= [path= limit= format=text\|json total case]`, `search:context query=` (grep-style `path:line: text`), `search:open [query=]` |
| Tasks | `tasks [file= path= status= total done todo verbose format= active daily]`, `task ref=path:line \| file= line= [status= toggle done todo]` |
| Properties | `properties [file= name= count sort=count format=yaml\|json\|tsv total counts active]`, `property:set name= value= [type= file=]`, `property:read name=`, `property:remove name=`, `aliases`, `tags [sort=count counts total active]`, `tag name= [verbose]` |
| Links | `backlinks [file= counts total format=]`, `links [file= total]`, `unresolved [total counts verbose]`, `orphans [total]`, `deadends [total]` |
| Outline | `outline [file= format=tree\|md\|json total]` |
| Bases | `bases`, `base:views`, `base:create [file= view= name= content= open]`, `base:query file= [view= format=json\|csv\|tsv\|md\|paths]` |
| Bookmarks | `bookmarks [total verbose format=]`, `bookmark file= [subpath= folder= search= url= title=]` |
| Commands/hotkeys | `commands [filter=]`, `command id=`, `hotkeys`, `hotkey id=` |
| Templates | `templates`, `template:read name= [title= resolve]`, `template:insert name=` |
| Unique | `unique [name= content= paneType= open]` |
| Plugins | `plugins [filter=core\|community versions format=]`, `plugins:enabled`, `plugins:restrict on\|off`, `plugin id=`, `plugin:enable id=`, `plugin:disable id=`, `plugin:install id= [enable]`, `plugin:uninstall id=`, `plugin:reload id=` |
| Themes/snippets | `themes`, `theme [name=]`, `theme:set name=`, `theme:install name= [enable]`, `snippets`, `snippets:enabled`, `snippet:enable name=`, `snippet:disable name=` |
| History | `diff [file= from= to= filter=local\|sync]`, `history [file=]`, `history:list`, `history:read version=`, `history:restore version=`, `history:open` |
| Sync | `sync on\|off`, `sync:status`, `sync:history`, `sync:read version=`, `sync:restore version=`, `sync:open`, `sync:deleted` |
| Publish | `publish:site`, `publish:list`, `publish:status [new changed deleted]`, `publish:add [file= changed]`, `publish:remove`, `publish:open` |
| Workspace | `workspace [ids]`, `workspaces`, `workspace:save [name=]`, `workspace:load name=`, `workspace:delete name=`, `tabs [ids]`, `tab:open [group= file= view=]`, `recents` |
| Misc | `random [folder= newtab]`, `random:read`, `web url= [newtab]`, `wordcount [file= words characters]` |
| Developer | `devtools`, `dev:debug on\|off`, `dev:cdp method= params=`, `dev:errors [clear]`, `dev:screenshot path=`, `dev:console [limit= level= clear]`, `dev:css selector= [prop=]`, `dev:dom selector= [attr= css= total text inner all]`, `dev:mobile on\|off`, `eval code=` |

### Scripts

**Morning routine** (shell alias `morning`):

```bash
#!/usr/bin/env bash
obsidian workspace:load name=Planning
obsidian daily
obsidian daily:append content="- $(date +%H:%M) Started the day. Weather: $(curl -s 'wttr.in/?format=%C+%t')"
obsidian tasks daily todo
```

**Quick capture from anywhere** (bind to a global hotkey via your launcher):

```bash
#!/usr/bin/env bash
# usage: cap "text"   → appends to today's Log
obsidian daily:append content="- $(date +%H:%M) $*"
```

**Nightly export of key bases to CSV** (cron):

```bash
#!/usr/bin/env bash
out=~/Backups/obsidian-csv/$(date +%F); mkdir -p "$out"
for b in Accounts Subscriptions People Projects; do
  obsidian base:query file="$b" format=csv > "$out/$b.csv"
done
```

**Create a meeting note from a calendar event** (called by a calendar hook / Shortcut with title and attendee):

```bash
#!/usr/bin/env bash
title="$1"; who="$2"
name="$(date +%F) $title"
obsidian create path="Work/Meetings/$name.md" template=tpl-meeting open
obsidian property:set file="$name" name=attendees value="[[${who}]]" type=list
```

**Vault health report** (weekly):

```bash
#!/usr/bin/env bash
{
  echo "# Vault health $(date +%F)"
  echo "- Files: $(obsidian files total)"
  echo "- Orphans: $(obsidian orphans total)"
  echo "- Dead ends: $(obsidian deadends total)"
  echo "- Unresolved links: $(obsidian unresolved total)"
  echo "- Open tasks: $(obsidian tasks todo total)"
  echo "## Top unresolved"
  obsidian unresolved counts | head -20 | sed 's/^/- /'
} > /tmp/health.md
obsidian create path="Meta/Health $(date +%F).md" content="$(cat /tmp/health.md)" overwrite
```

**Set up a new machine's plugins** (from a list exported with `obsidian plugins:enabled filter=community`):

```bash
for id in templater-obsidian obsidian-tasks-plugin dataview periodic-notes calendar omnisearch obsidian-linter obsidian-style-settings; do
  obsidian plugin:install id="$id" enable
done
```

**JavaScript inside Obsidian from the terminal**: `obsidian eval code="app.vault.getMarkdownFiles().filter(f=>f.path.startsWith('Inbox/')).length"` — anything the plugin API can do. Combine with `dev:screenshot` and `dev:errors` for testing templates and plugins.

## Shell commands plugin

Define commands with variables — `{{file_path:absolute}}`, `{{file_name}}`, `{{title}}`, `{{selection}}`, `{{clipboard}}`, `{{date:YYYY-MM-DD}}`, `{{yaml_value:status}}`, `{{folder_path}}`, `{{vault_path}}`, custom prompt variables — and choose where output goes (notice, current note at cursor, clipboard, a new note, a modal). Assign hotkeys. Examples:

- **Pandoc export** of the current note (Chapter 31).
- **Open the note's folder** in Finder/Explorer.
- **Run a Python script** over the vault (e.g. generate a Base from a CSV; fetch weather into the daily note).
- **Git snapshot**: `git -C "{{vault_path}}" add -A && git -C "{{vault_path}}" commit -qm "snapshot {{date:YYYY-MM-DD HH:mm}}"`.
- **Whisper transcription** of a dropped audio file into the note.
- **hledger/beancount report** into a code block (Chapter 21).
- **Image compression** of a pasted image (`cwebp`).

Security: commands run with your user privileges; do not sync command definitions blindly to machines with different paths; the plugin's "confirm before execution" option is worth enabling for destructive commands.

## Local REST API plugin

Runs an HTTPS server on `localhost:27124` (HTTP on 27123 optional) with an API key. Endpoints: `GET/PUT/POST/PATCH/DELETE /vault/{path}` (read/write/append/patch notes — PATCH can insert under a heading or block), `/periodic/daily/` (today's note), `/search/simple/?query=` and `/search/` (Dataview DQL or JsonLogic), `/commands/` (list/execute), `/open/{path}`, `/active/` (the active note). Uses: Raycast/Alfred extensions, browser bookmarklets, MCP servers for AI assistants (Chapter 30), Home Assistant, n8n/Zapier via a tunnel (careful), scripts from other machines on your LAN.

```bash
curl -sk -H "Authorization: Bearer $OBS_KEY" \
  -H "Content-Type: text/markdown" \
  -X POST "https://127.0.0.1:27124/periodic/daily/" \
  --data-binary "- $(date +%H:%M) logged via REST"
```

With the CLI now in core, the REST API's niche is *remote* and *programmatic* access from tools that cannot shell out.

## Launchers

- **Raycast** (macOS): the Obsidian extension (search notes, create, append to daily, random note, bookmarked notes) plus Script Commands wrapping the CLI. Global hotkey → "Append to daily" is the best capture there is.
- **Alfred** (macOS): the Obsidian workflow; or a `bash` script filter around `obsidian search`.
- **AutoHotkey / PowerToys Run / Flow Launcher / Keypirinha** (Windows): scripts calling `obsidian …` or `start obsidian://…`.
- **Albert / Ulauncher / rofi** (Linux): same.
- **Hookmark** (macOS): bidirectional links between Obsidian notes and files/emails/URLs in other apps (`obsidian://hook-get-address`).
- **Keyboard Maestro / BetterTouchTool / Espanso**: text expansion and macros (Espanso snippets for `;;date`, `;;meet` templates work in any app including Obsidian).

## Apple Shortcuts and Tasker

Chapter 27 covered the mobile side. Desktop Shortcuts (macOS) can run shell scripts (CLI) and AppleScript; a Shortcut in the menu bar "New meeting from selected calendar event" → CLI create is a two-action shortcut. Tasker: `obsidian://` intents, file writes, HTTP requests to the REST API on the LAN.

## Web Clipper

The official browser extension (Chrome, Firefox, Safari, Edge, Brave, Arc; iOS Safari; Android Firefox). Settings:

- **Templates** with **triggers** (URL patterns or schema.org types): a default clipping template, plus specialized ones — `recipe` (schema Recipe → ingredients/steps), `youtube.com` (title, channel, URL, transcript if available), `arxiv.org` (paper metadata), `amazon`/`goodreads` (book metadata → `tpl-book` properties), `github.com` (repo, stars, README summary).
- **Variables**: `{{title}}`, `{{url}}`, `{{author}}`, `{{published}}`, `{{date}}`, `{{content}}` (readability-extracted body), `{{selection}}`, `{{highlights}}`, `{{schema:@Recipe.recipeIngredient}}`, `{{meta:property:og:image}}`, plus filters (`|date:"YYYY-MM-DD"`, `|slice`, `|wikilink`, `|list`, `|strip_tags`, `|markdown`, `|camel`, `|safe_name`…).
- **Properties** section per template → typed frontmatter (`type: source`, `medium: article`, `status: to-read`, `topics: []`).
- **Behavior**: create a new note in a folder, or append to an existing note / today's daily note; note name template (`{{title|safe_name}}`).
- **Highlighter**: highlight on the page; clip only highlights (with context) or highlights + article.
- **Interpreter**: attach a model (OpenAI/Anthropic/Gemini/Ollama local) and add prompt variables to the template: `{{"three bullet summary"}}`, `{{"list people mentioned as wikilinks"}}`, `{{"extract ingredients as a markdown list"}}`. The model fills them at clip time. Use it to arrive pre-distilled; keep prompts short and structural.

Capture lands in `Inbox/` or straight into `Sources/Articles/`; the vault's folder templates do not run (the clipper writes the whole note), so put the full frontmatter in the clipper template.

## Integration recipes

| Integration | Approach |
| --- | --- |
| **Calendar → meeting notes** | Google Calendar plugin (creates notes from events), Full Calendar (ICS view), or a Shortcut/script per event calling the CLI with `template=tpl-meeting`; a cron job each morning that lists today's events into the daily note's `## Agenda` (icalBuddy on macOS, `gcalcli`, or the Google Calendar API). |
| **Email → vault** | Forward to a mailbox polled by a script (IMAP → Markdown → `Inbox/`); Zapier/n8n/Make "email parser → write file to Dropbox folder inside vault" (only if the vault is on a synced folder); Apple Mail rule → Shortcut → file; Hookmark links to messages instead of copying them. |
| **Readwise / Snipd / Kindle** | Readwise Official plugin (highlights → notes with templates); Kindle Highlights plugin; Snipd → Readwise or its own Obsidian export. |
| **Zotero** | Chapter 18. |
| **Strava / Garmin / Apple Health** | Strava API or Health Auto Export → script → `create` workout notes with properties (Chapter 20). |
| **Letterboxd / Goodreads / Trakt / Last.fm** | CSV export → Python script → `type: source` notes; run yearly or on demand. |
| **Todoist / Things / Reminders / TickTick** | Todoist Sync plugin (two-way); Things via URL scheme and a script; Apple Reminders via Shortcuts (read reminders → tasks in the daily note). Most people keep tasks *in* Obsidian and use the external app only for alarms. |
| **Slack / Teams / Discord** | A bot or Zap that posts messages you react to (e.g. 📌) into `Inbox/`; or copy-paste with the Advanced URI bookmarklet. |
| **Browser bookmarks / Pocket / Instapaper** | Export → script → `Sources/Articles/` with `status: to-read`; or switch to the Web Clipper as the single capture path. |
| **Photos** | Monthly: a script copies "favourited this month" photos (downscaled) into `Attachments/photos/YYYY-MM/` and writes embeds into the monthly note. |
| **Weather / location / quotes** | Templater `tp.web.request` in the daily template; or a cron `daily:prepend`. |
| **Home Assistant** | REST API or file writes: sensor summaries into the daily note; a "log energy use" automation. |
| **Git hooks** | Post-commit hook that runs a Linter pass or regenerates a Base/CSV. |
| **AI assistants** | Chapter 30: MCP servers over the vault folder or REST API; Copilot/Smart Connections inside Obsidian; CLI `read`/`search` piped to an LLM CLI. |

## Design principles for automations

1. **Idempotent**: running twice should not duplicate (check for existing note; use `overwrite` deliberately or `append` with a marker).
2. **Type on arrival**: automations write full frontmatter so Bases see the note immediately.
3. **Land in `Inbox/` unless certain**: automated notes with a `source: automation` property, reviewed in the weekly sweep.
4. **Log**: automations append a line to `Meta/Automation Log.md` (`daily:append` to a dedicated note) so failures are visible.
5. **Secrets outside the vault**: API keys in the OS keychain/environment, never in scripts stored in the vault (or `.gitignore` them).
6. **Fail safe**: if Obsidian is not running and the script needs it, the CLI launches it; for unattended jobs, write files instead.

## Key takeaways

- Four surfaces: write files (most robust), `obsidian://` + Advanced URI (open/append/run from anywhere), the Obsidian CLI (full scripting of the running app), and Shell commands / Local REST API (out of and into Obsidian from other tools).
- The CLI cheat sheet covers files, daily notes, search, tasks, properties, links, bases, plugins, sync, publish, workspaces and developer commands; wrap it in shell scripts bound to launcher hotkeys and cron.
- Web Clipper templates with triggers, typed properties and Interpreter prompts make web capture arrive structured and pre-distilled.
- Integration recipes (calendar, email, reading services, fitness, media, tasks, home automation) all reduce to: get data → write typed Markdown → land in Inbox or the right folder.
- Automations should be idempotent, typed on arrival, logged, and keep secrets out of the vault.

## Next

[Chapter 30: AI in Your Vault →](30-ai.md)
