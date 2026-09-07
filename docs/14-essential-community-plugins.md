# Essential Community Plugins

There are well over two thousand community plugins. Perhaps forty matter, and no single vault needs more than about twenty-five. This chapter is a curated, tiered map: what each plugin is for, when you need it, how to configure it, and what to watch out for. Plugins are listed by the name shown in Obsidian's plugin browser. Where two plugins compete, the guide picks one and says why.

## How to think about plugins

- **Every plugin is code with full access to your vault and network.** Obsidian's review process checks for obvious abuse, not for bugs. Prefer plugins that are popular (100k+ downloads), recently updated, and open source with visible issue tracking.
- **Every plugin costs startup time**, especially on mobile. The developer console (++ctrl+shift+i++ → Console) logs plugin load times at startup; more practically, when mobile startup is slow, disable everything and re-enable in halves until you find the culprit.
- **Every plugin is a dependency.** If it stores data only in its own `data.json` (not in your notes), ask what happens when it is abandoned. Kanban, Excalidraw, and Tasks store in Markdown; Spaced Repetition stores review data in your notes as inline text; Tracker and Charts store nothing (they read your notes). Good signs.
- **Core first.** Chapter 9's table of gaps tells you what actually needs a community plugin.
- **Audit quarterly** (Chapter 32): for each enabled plugin, can you name what it does for you this month? If not, disable it.

## Tier 1 — the foundation (install these first)

| Plugin | Purpose | Key config / gotchas |
| --- | --- | --- |
| **Templater** | Dynamic templates, scripting, folder templates | Chapter 11. Turn on *Trigger on new file creation*. |
| **Tasks** | Task metadata and queries | Chapter 13. Set a global query excluding Templates/Archive. |
| **Dataview** | Queries over inline fields, tasks, lists; DataviewJS | Chapter 12. Enable JS queries. Use Bases for plain tables. |
| **Periodic Notes** | Weekly/monthly/quarterly/yearly notes | Match formats to your naming; use with Calendar. |
| **Calendar** | Sidebar month view for daily/weekly notes | Set week start; enable week numbers. |
| **Omnisearch** | Ranked full-text search with fuzzy matching, PDF/OCR | Keep core search too. Enable diacritics ignore. |
| **Linter** | Normalizes formatting and frontmatter on save | Configure: YAML key order, trailing spaces, heading blank lines, `created`/`modified` insertion (optional). Run on the whole vault once, then on save. |
| **Style Settings** | UI for theme/snippet variables | Required by most themes to expose options. |

## Tier 2 — high value for most whole-life vaults

### Capture and creation

| Plugin | Purpose | Notes |
| --- | --- | --- |
| **QuickAdd** | Capture commands, template commands, macros, menus | "Append to today's log", "New book with prompts", "Quick idea to Inbox". Can call Templater. Chapter 11 compares. |
| **Meta Bind** | Input widgets (toggle, select, slider, date, text) bound to properties; buttons | Mobile-friendly daily-note forms; `INPUT[slider(minValue(1),maxValue(10)):mood]`. |
| **Various Complements** | Autocomplete words/phrases from vault and custom dictionaries | Speeds typing of recurring names and terms. |
| **Paste image rename** or **Attachment Management** | Rename pasted images meaningfully; per-note attachment folders | Attachment Management is more complete; either fixes `Pasted image ….png`. |
| **Auto Note Mover** | Move new notes to folders by tag/title rules | Alternative to folder templates when capture lands in Inbox. |
| **Note Refactor** | Extract selections/headings to new notes with templates | Batch version of Note composer. |
| **Advanced URI** | URI actions for everything (open by UID, append to heading, run commands, set frontmatter) | Foundation for external automation. Chapter 29. |

### Organization and navigation

| Plugin | Purpose | Notes |
| --- | --- | --- |
| **Tag Wrangler** | Rename/merge tags, drag to nest | Core cannot rename tags. |
| **Homepage** | Open a chosen note/workspace on launch | Point at `00 Home`. |
| **Recent Files** | Sidebar list of recent files | Simple and constantly used. |
| **Quick Switcher++** | Modes: headings, symbols, related, commands, editors, bookmarks | Replaces the core switcher for power users. |
| **Folder notes** | Click a folder to open its index note; hides the note in the folder | Turns folders into MOCs. |
| **Waypoint** | Auto-generated folder indexes (lists of notes) inside folder notes | Pairs with Folder notes. |
| **Breadcrumbs** | Explicit hierarchies (`up`, `down`, `next`, `same`) via properties, with trail views and graphs | For people who want typed hierarchy on top of links; heavy. Optional. |
| **Iconize** | Icons for folders and notes (Lucide, FontAwesome, emoji) | Cosmetic but genuinely helps scanning the explorer. |
| **Commander** | Add commands to ribbon, toolbar, status bar, tab bar, explorer; hide default items | Tailor the UI without CSS. |
| **Hover Editor** | Page previews become editable floating windows | Excellent for editing a linked note without leaving context. |
| **Strange New Worlds** | Inline reference counts for blocks/headings | Shows what is transcluded where. |

### Writing and editing

| Plugin | Purpose | Notes |
| --- | --- | --- |
| **Editing Toolbar** (or **cMenu**) | Formatting toolbar | Mobile already has one; desktop optional. |
| **Code Editor Shortcuts** | Duplicate line, move line, select word, join lines, transform case… | Fills editor gaps. |
| **Outliner** + **Zoom** | Workflowy-style list manipulation and focus | For outline-heavy thinkers. |
| **Advanced Tables** | Table formulas, navigation, CSV import/export | Core table editing covers basics; keep for formulas. |
| **Table Enhancer** | Excel-like table editing in Live Preview | Alternative to Advanced Tables. |
| **Footnote Shortcut** | Insert/jump footnotes | Academic writers. |
| **Latex Suite** | Snippets and autocompletion for math | Students/scientists. |
| **Typewriter Scroll** | Keep cursor line centred; dim other paragraphs | Focus mode for writers. |
| **Longform** | Manuscript management: scenes, drafts, compile to one document | Novelists and long-form writers (Chapter 24). |
| **Regex Find/Replace** | Vault-wide or note-wide regex replace | Core lacks vault-wide replace. |
| **Text Extractor** | Extract text from images/PDFs for search (used by Omnisearch) | |

### Visual and spatial

| Plugin | Purpose | Notes |
| --- | --- | --- |
| **Excalidraw** | Freehand drawing, diagrams, whiteboards with Obsidian links; scripts library | Huge, excellent, actively developed. Drawings are `.md` files with embedded JSON — searchable and linkable. Chapter 24. |
| **Kanban** | Free-form kanban boards as Markdown | Bases kanban (1.14) for property-driven boards. |
| **Charts** (Obsidian Charts) | Chart.js charts from code blocks or DataviewJS | Chapter 12. |
| **Heatmap Calendar** | Year heatmap from DataviewJS arrays | Habits, mood, workouts. |
| **Tracker** | Charts and stats over daily-note metrics with its own query DSL | Alternative to hand-rolled DataviewJS. |
| **Mind Map** / **Enhancing Mindmap** | Render outlines as mind maps | Niche. |
| **Map View** | Map of notes with `location` properties; geolocation search; routing | Travel, places; Bases map view is the lighter core alternative. |
| **Image Toolkit** / **Image Converter** | Zoom/rotate/convert images; compress on paste | Core 1.13 covers viewing; Converter is useful for WebP compression. |

### Reading, research and learning

| Plugin | Purpose | Notes |
| --- | --- | --- |
| **Book Search** | Create book notes from Google Books/OpenLibrary lookups with a template | Chapter 17. |
| **Zotero Integration** | Import Zotero items and annotations with templates; cite | Chapter 18. |
| **Citations** | Cite from a BibTeX/CSL JSON library | Lighter alternative to Zotero Integration. |
| **PDF++** | PDF annotation with highlights written back as Markdown links; backlink from PDF selections | The best PDF workflow in Obsidian. |
| **Annotator** | Annotate PDFs/EPUBs with Hypothesis-style highlights | Alternative to PDF++. |
| **Spaced Repetition** | Flashcards from notes (`::` / `?` syntax) and note-level review scheduling (SM-2) | Chapter 17. Data stored in-note. |
| **Readwise Official** | Sync Readwise highlights to notes | If you use Readwise. |
| **Kindle Highlights** | Import Kindle highlights | Free alternative for Kindle users. |
| **Media Extended** | Embed and timestamp-link YouTube/local video/audio; notes tied to playback | Lecture and podcast notes. |
| **Web Clipper** (browser extension) | Clip pages to Markdown with templates; highlighter; Interpreter (AI extraction) | Official; not a plugin but essential. Chapter 29. |
| **Surfing** | Enhanced in-app web browsing | Extends core Web viewer; mostly superseded. |

### Sync, backup, publishing

| Plugin | Purpose | Notes |
| --- | --- | --- |
| **Git** (Obsidian Git) | Auto commit/push/pull; history view; diff | Chapter 26. Desktop-strong; mobile works with caveats. |
| **Remotely Save** | Sync to S3/WebDAV/Dropbox/OneDrive/Google Drive with optional E2E encryption | Best free cross-platform sync. |
| **Self-hosted LiveSync** | CouchDB-based near-real-time sync with E2E encryption | For self-hosters; the most "Obsidian Sync-like" free option. |
| **Enveloppe** (ex Publisher) | Push selected notes to a GitHub repo for static-site publishing | Chapter 31. |
| **Digital Garden** | Publish notes via a Netlify/Vercel template | Chapter 31. |
| **Pandoc Plugin** / **Enhancing Export** | Export to DOCX/PDF/HTML/LaTeX via Pandoc | Chapter 31. |
| **Advanced Slides** | reveal.js presentations from notes | |

### Automation and integration

| Plugin | Purpose | Notes |
| --- | --- | --- |
| **Shell commands** | Run shell commands from Obsidian with variables; output to note | Desktop. Chapter 29. |
| **Local REST API** | HTTP API to read/write/search the vault (with API key) | Foundation for external scripts, MCP servers, Raycast. Chapter 29/30. |
| **Buttons** | Buttons that run commands/templates/links inside notes | Meta Bind also does buttons; pick one. |
| **Hotkeys for specific files** / **Hotkeys++** | Open specific notes with hotkeys; extra editor commands | |
| **Obsidian Tasks Calendar Wrapper** / **Tasks Calendar** | Calendar rendering of Tasks | |
| **Todoist Sync** / **TickTick** | Two-way sync with external task apps | If your team uses one. |
| **Google Calendar** | View/create GCal events inside Obsidian | OAuth setup required. |
| **Terminal** | Embedded terminal pane (desktop) | Pairs with the Obsidian CLI. |

### AI

| Plugin | Purpose | Notes |
| --- | --- | --- |
| **Copilot** | Chat with your vault (RAG), inline edits, custom prompts; supports OpenAI/Anthropic/Gemini/Ollama | Chapter 30. |
| **Smart Connections** | Embedding-based related notes + chat | Local embeddings option. |
| **Text Generator** | Prompt templates that generate into notes | |

API keys belong in **Keychain** (Obsidian 1.11+) where plugins support it, not in `data.json`.

## Tier 3 — situational (install when the need is concrete)

**Templater alternatives**: none needed. **Sliding Panes**: superseded by core Stack tabs. **Calendar alternatives**: **Big Calendar**, **Full Calendar** (Chapter 13). **Habit trackers**: **Habit Tracker 21**, or roll your own with tasks + Heatmap Calendar (Chapter 20). **Journaling**: **Journals** plugin (structured multi-journal setup; alternative to Periodic Notes). **Focus**: **Focus Mode**, **Stille**, **ProZen**. **Numbers**: **Numerals** (inline calculator blocks), **Math Calculator**. **Finances**: **Ledger** (plain-text accounting in Obsidian), **Beancount** helpers. **Languages**: **Language Tool Integration** (grammar), **Translate**. **Music**: **Chords**, **abcjs**. **Timelines**: **Timeline**, **Chronos Timeline**. **Diagrams**: **PlantUML**, **Diagrams.net**, **D2**. **Reading**: **Reading Time**, **Novel Word Count**. **Vim**: **Vimrc Support**. **Privacy**: **Password Protect** (folder-level, cosmetic), **Meld Encrypt** (real in-note encryption). **Databases**: **DB Folder**, **Projects** — largely superseded by Bases. **Search**: **Better Search Views**. **Files**: **File Tree Alternative**, **Hider**, **Explorer Hider**. **Canvas**: **Advanced Canvas** (more node types, presentation mode, encapsulate), **Canvas Mindmap**. **Emoji**: **Emoji Shortcodes**, **Icon Shortcodes**. **Sorting**: **Custom File Explorer Sorting**. **Colors**: **Colored Text**, **Highlightr**. **Links**: **Auto Link Title**, **Link Favicon**, **Supercharged Links** (style links by properties — great for people/projects colouring). **Frontmatter**: **Metadata Menu** (schema enforcement and bulk edit — powerful if you want strict types), **Update time on edit** (maintains `modified`; only if you truly need it). **Daily notes**: **Daily Note Outline**, **Day Planner** (Chapter 13). **Templates**: **Templater** alone suffices. **Random**: **Smart Random Note**. **Telegram**: **Telegram Sync** (capture from Telegram to vault). **Email**: no good plugin — use automation (Chapter 29).

## Avoid or retire

- Plugins abandoned for 2+ years with open crash issues (check the repo).
- Anything that "syncs settings across devices" outside Obsidian Sync/Git — fragile.
- Duplicates: two toolbars, two calendars, two AI chats. Pick one.
- **Sliding Panes**, **Starred**, **Settings Search**, **Table of Contents**, **Better Word Count** where core covers it (Stack tabs, Bookmarks, 1.13 Settings search, Outline, Word count).
- Cosmetic plugins that inject heavy CSS/JS on every render if you notice lag.

## Recommended starting sets

**Minimal (8):** Templater, Tasks, Periodic Notes, Calendar, Omnisearch, Linter, Style Settings, Homepage.

**Whole-life standard (~20):** Minimal + Dataview, QuickAdd, Meta Bind, Tag Wrangler, Recent Files, Excalidraw, Book Search, PDF++, Spaced Repetition, Heatmap Calendar, Git or Remotely Save, Advanced URI, Attachment Management, Commander, Iconize.

**Researcher add-ons:** Zotero Integration, Citations, Pandoc, Latex Suite, Footnote Shortcut, Longform.

**Automation add-ons:** Shell commands, Local REST API, Buttons, Terminal, Copilot or Smart Connections.

## Installing, updating, and configuring safely

- Install from Settings → Community plugins → Browse; or paste a GitHub URL into **BRAT** (Beta Reviewers Auto-update Tool) for pre-release plugins — use BRAT sparingly and only for plugins you trust.
- Update weekly (*Check for updates*). Read release notes for plugins that touch your files (Linter, Tasks, Templater).
- Plugin settings live in `.obsidian/plugins/<id>/data.json`. Back them up; they are part of your system. Sync selectively (1.13 warns about syncing plugins because some settings are device-specific — e.g. Shell commands, Git paths).
- The CLI: `obsidian plugins:enabled`, `plugin:install id=… enable`, `plugin:disable id=…`, `plugins:restrict on` — scriptable plugin management for setting up a new device (Chapter 29).
- When something breaks: Settings → Community plugins → *Restricted mode* (or CLI `plugins:restrict on`); since 1.13 you can leave restricted mode without re-enabling everything, so bisect by re-enabling in halves.

## Key takeaways

- Fewer, better plugins: Tier 1 (8) is the foundation, Tier 2 fills concrete gaps, Tier 3 only when a real need appears.
- Prefer plugins that store data in your notes (Tasks, Kanban, Excalidraw, Spaced Repetition) over ones that keep it in `data.json`.
- Bases has retired the database plugins; core has retired Sliding Panes, Starred, Settings Search and basic word count.
- Audit quarterly, update weekly, back up `.obsidian/plugins`, and know how to bisect with Restricted mode.

## Next

[Chapter 15: Daily Notes and Journaling →](15-daily-notes-and-journaling.md)
