# Core Plugins — Every One, Mastered

Core plugins ship with Obsidian, are maintained by the Obsidian team, work identically on desktop and mobile, and are the most stable foundation you can build on. Many users never look past the defaults and then install a community plugin for something a core plugin already does. This chapter goes through every core plugin (as of 1.13): what it does, the settings that matter, and the non-obvious tricks. Bases gets its own chapter (10) because of its depth.

## Enabling and finding them

Settings → Core plugins (searchable since 1.13). Each has a toggle and, where relevant, a gear for options. Their commands appear in the command palette prefixed by the plugin name; hotkeys are assignable for all of them. Disabled core plugins cost nothing; enabled-but-unused ones cost almost nothing (unlike community plugins).

## Navigation & structure

### File explorer

The tree of files and folders.

- Sort: by name, modified, created (ascending/descending); the sort is saved with the layout (1.10+).
- **Auto reveal current file** (gear) keeps the tree following your active note; turn off if you find it jumpy (since 1.13 it no longer fires while you are renaming).
- Multi-select with ++shift++-click (range) or ++ctrl++-click (toggle); ++alt++-click adds the previously active item to the selection (1.12). Then drag, delete, or move together.
- Copy/paste files with ++ctrl+c++/++ctrl+v++ (1.12); duplicate via context menu.
- Right-click a folder → *New note*, *New canvas*, *New base*, *New folder*, *Set as attachment folder*, *Search in folder*.
- Drag a note into the editor to insert a link. Drag a folder from your OS onto the app to import it with structure (1.13).
- Collapse all / expand all icons at the top; ++esc++ clears selection.
- The explorer honours *Excluded files* only for dimming; to hide folders entirely use a CSS snippet (Chapter 28) or the *Hider* plugin.

### Search

Covered in Chapter 6.

### Quick switcher

Covered in Chapters 2 and 6. Setting worth knowing: *Show existing only* (hides the "create new" suggestion) and *Show attachments* / *Show all file types*.

### Bookmarks

Bookmarks replace the old "Starred" plugin and can bookmark **files, folders, headings, blocks, searches, graph views, and URLs**, organized in nested groups with drag-and-drop. 1.13 added a search box to the pane and keyboard navigation.

Use it for: a "Daily driver" group (Home, this week, current project), "Saved searches" (Chapter 6), "Reference blocks" (the exact paragraph with your Wi-Fi setup, the block with your standard meeting agenda), and per-project groups you delete when the project ends. Bookmarks are stored in `.obsidian/bookmarks.json`; the CLI can add them (`obsidian bookmark file=… subpath=…`).

### Outline

Heading tree of the current note in a sidebar. Click to jump; drag headings to reorder sections (with their content); right-click → rename heading (updates links). Settings: *Auto-follow cursor*, *Show search*. For long notes, pin an Outline tab in the right sidebar and never scroll again. The community *Quiet Outline* adds levels, search-as-you-type, and better styling.

### Tags view

All tags with counts, nested tags collapsible, sort by name or frequency, click to search. Renaming and drag-nesting need **Tag Wrangler**.

### Properties view

Two views: the in-note property editor (managed under Editor → Properties in document) and the **All properties** sidebar view listing every property name in the vault with counts. From the sidebar: rename a property everywhere, change its type, delete it from all notes (1.10). Keyboard: arrows to move, ++backspace++ to delete (1.13). This is your schema-hygiene console.

### Backlinks / Outgoing links

Chapter 4. Settings: *Backlink in document* (footer section on every note), *Show more context*, *Collapse results*.

### Page preview

Hover a link with ++ctrl++ (or without, per setting) to see a popup preview of the target — including the specific heading or block. Works for images, PDFs, and bases. Setting per-context (editor, search, backlinks…). **Hover Editor** (community) upgrades previews into editable floating windows.

### Graph view

Chapter 4.

### Canvas

Chapter 4. Settings: default new-file location for canvases, snap to grid/objects, zoom sensitivity, show label at zoom threshold. Canvas rendering got faster in 1.13.

### Workspaces

Save/load layouts (Chapter 2). *Save layout*, *Load layout*, *Manage workspaces* commands; keep 3–5 named ones. CLI: `workspace:save`, `workspace:load name=…`.

### Web viewer

Since 1.8. Opens external links in an in-app browser tab (desktop). Settings: open external links in-app or in the default browser; search engine; whether to save browsing history. Useful when researching (highlight text → *Save to note*, *Copy link to selection*), and you can embed a web page in Canvas. Ad blocking is not included; heavy sites are slow. For clipping, the Web Clipper browser extension (Chapter 29) is better.

## Creating & editing

### Daily notes

The most-used core plugin. Settings: **Date format** (`YYYY-MM-DD` — never anything else), **New file location** (`Journal/Daily`), **Template file** (`Templates/tpl-daily`), **Open daily note on startup**. Commands: *Open today's daily note* (hotkey it), *Open previous/next daily note* (great for reading back through the week). The template's `{{date}}`, `{{time}}`, `{{title}}` placeholders work with core Templates; Templater can be set to process the daily note instead. For weekly/monthly/quarterly/yearly you need **Periodic Notes** (community) or Templater-generated notes. The CLI has `daily`, `daily:append`, `daily:prepend`, `daily:read`, `daily:path`.

### Templates

Insert a template file into the current note at the cursor. Settings: template folder, date format (`YYYY-MM-DD`), time format (`HH:mm`). Placeholders: `{{title}}`, `{{date}}`, `{{time}}`, `{{date:YYYY-MM-DD HH:mm}}` (Moment.js format). That is the whole feature. It is enough for simple vaults, and *Templater* (Chapter 11) supersedes it entirely for anything dynamic. Keep both enabled: core Templates is what the Daily notes plugin, the CLI (`template:insert`, `create template=…`) and the Unique note creator use by default.

### Unique note creator

Creates a note whose name is a timestamp (`YYYYMMDDHHmm` by default — set your own format) in a chosen folder with a chosen template. This is the Zettelkasten-ID workflow; also useful for quick capture when you do not want to think of a title (the title becomes an alias or H1 later). Since 1.13 it links to its own settings when it cannot find the template. The 1.12 `unique` URI action and the CLI `unique` command trigger it externally.

### Note composer

Three commands: **Extract current selection** (moves selected text to a new note, replaces with link/embed/nothing), **Extract this heading** (right-click a heading), **Merge entire file with…** (appends/prepends the current note into another and redirects links). Settings control the replacement text and whether extracted heading links are rewritten (1.13 does this automatically). This is how daily-note scribbles become idea notes without copying and pasting.

### Slash commands

Type `/` at the start of a line (or anywhere, depending on setting) to search and run any command inline. Configure the trigger character. Mobile users love it; desktop users mostly use the palette.

### Format converter

Converts legacy syntaxes (Roam-style `#[[tag]]`, `__bold__` variants, `{{TODO}}` tasks, etc.) after an import. Run once, then disable.

### Footnotes view

A sidebar listing the current note's footnotes; click to jump between reference and definition. Academic writers turn it on; everyone else can leave it off.

### Slides

Turns a note into a presentation: `---` separates slides; the *Start presentation* command shows it full screen with arrow-key navigation. Minimal styling, no speaker notes. For real talks use the **Advanced Slides** community plugin (reveal.js with themes, fragments, speaker view, PDF export) — but core Slides is enough for a 5-slide stand-up.

### Word count

Status bar word/character count; counts the selection when text is selected. Click for details. CLI: `wordcount`.

### Random note

Opens a random note (optionally limited to a folder via the CLI `random folder=Notes`). The cheapest possible spaced-review system: hit it three times a day and read old ideas. Use with the **Smart Random Note** plugin to restrict to a search query (e.g. `type: note status: seedling`).

## Data & files

### File recovery

Snapshots every changed file at an interval (default 5 minutes) and keeps them for N days (default 7). Settings → File recovery → *Snapshot interval*, *History length* — raise to 30+ days; the storage cost is small (it lives in IndexedDB, not your vault). Recover via the *Open file recovery* command or the CLI (`history`, `history:read`, `history:restore version=…`, `diff file=… from=1`). It is not a backup (it lives on the device) but it saves you from bad edits and plugin mishaps constantly.

### Importer

Imports from Notion (including databases → Bases, since Nov 2025), Evernote (.enex), Apple Notes, Bear, Roam Research (JSON), Google Keep, OneNote, Microsoft OneNote, HTML, Markdown variants, Airtable (Aug 2026), and more. Chapter 33 covers migration end-to-end.

### Sync

The paid Obsidian Sync service; end-to-end encrypted; selective sync of folders and settings/plugins/themes; version history (up to a year on Plus); multiple vaults. Settings: what to sync (images, audio, video, PDFs, other types, size limits — since 1.12 Sync logs skipped-too-large files), which settings to sync (appearance, hotkeys, core plugins, community plugins + their data; 1.13 warns before syncing community plugins because plugin data can be device-specific). The Sync view in the sidebar (1.13) shows recent changes with context menus, drag-and-drop, multi-select, and delete. The CLI adds `sync`, `sync:status`, `sync:history`, `sync:read`, `sync:restore`, `sync:deleted`. Chapter 26 compares Sync with alternatives.

### Publish

The paid Obsidian Publish service: choose notes to publish, get a hosted site with graph, search, backlinks, and custom domain. `publish: true/false` property controls inclusion; `permalink`, `description`, `image` customize pages. CLI: `publish:add`, `publish:remove`, `publish:status`, `publish:site`. Chapter 31 covers Publish and free alternatives.

## Interface

### Command palette

++ctrl+p++. Settings → *Pinned commands* puts your favourites on top. Recent commands rise automatically. Type a few letters of each word to fuzzy match. ++ctrl+n++/++ctrl+p++ move through suggestions on all platforms (1.13).

### Bases

Chapter 10. Enabled by default on new vaults; older vaults need to toggle it on.

## Core plugin combinations worth stealing

- **Daily notes + Templates + Note composer** = capture-in-daily-note, extract-to-idea-note.
- **Bookmarks (search) + Backlinks in document** = a review workflow with no plugins.
- **Random note + Outline** = resurfacing old notes and skimming them quickly.
- **Workspaces + Canvas** = a "Planning" layout with a project board.
- **File recovery + Sync history + CLI `diff`** = three layers of undo.
- **Unique note creator + Slash commands** = mobile quick capture without thinking.
- **Web viewer + Canvas** = research board with live web pages beside your notes.

## What core plugins cannot do (so you know what to install)

| Need | Core answer | Community answer |
| --- | --- | --- |
| Weekly/monthly/quarterly notes | none | Periodic Notes, or Templater |
| Dynamic templates (prompts, dates math, logic) | Templates placeholders only | Templater, QuickAdd |
| Task queries with due dates/recurrence | Search operators `task-todo:` | Tasks |
| Computed tables with inline fields | Bases (properties only) | Dataview |
| Rename tags | none | Tag Wrangler |
| Kanban boards | Bases (no kanban view) | Kanban plugin, or Bases + a Kanban view plugin |
| Spaced repetition | Random note (crude) | Spaced Repetition |
| Calendar widget | none | Calendar, Full Calendar |
| Git sync | none | Git |
| Drawings | Canvas (boxes/arrows) | Excalidraw |
| Per-folder auto templates | none | Templater folder templates |
| Vault-wide find & replace | none | Regex Find/Replace |
| Hide folders | Excluded files (dims only) | CSS / Hider |

## Key takeaways

- Core plugins are stable, mobile-safe, and free of maintenance risk — exhaust them before installing community alternatives.
- The highest-value ones for a whole-life vault: Daily notes, Templates, Bookmarks, Backlinks, Outline, Properties view, Note composer, File recovery, Workspaces, Bases, Canvas, Random note.
- Raise File recovery's history length; bookmark your searches; hotkey today's daily note; learn Note composer's extract/merge.
- Know the gaps (periodic notes, dynamic templates, task queries, computed tables, tag renaming, Git) so you install exactly the community plugins that fill them.

## Next

[Chapter 10: Bases — the Native Database →](10-bases.md)
