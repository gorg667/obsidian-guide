# Glossary and Resources

Terms used throughout the guide, defined briefly, followed by the resources worth your time: official documentation, the plugin authors' docs that double as tutorials, communities, and the handful of books and essays behind the methodologies.

## Glossary

**Alias** — An alternative name for a note, listed in the `aliases` property; `[[alias]]` resolves to the note and the quick switcher finds it.

**Area** — A domain of life maintained indefinitely (Health, Finances); a `type: area` note carrying a *standard*. From PARA.

**Backlink** — A link *to* the current note from another note; listed in the Backlinks pane. *Linked mentions* are actual links; *unlinked mentions* are plain-text occurrences of the note's name or aliases.

**Base / Bases** — Obsidian's core database feature (1.9+): `.base` files (YAML) or ```base blocks defining filters, formulas, and views (table, cards, list, map, kanban) over notes' properties.

**Block / block ID** — A paragraph, list item, table, callout, or code block that can be addressed with `^id` and linked or embedded as `[[Note#^id]]`.

**Callout** — A styled, optionally collapsible box: `> [!type] Title`. Types are built-in (note, tip, warning…) or custom via CSS.

**Canvas** — Core plugin for infinite spatial boards of cards, notes, media, and web pages; stored as open **JSON Canvas** `.canvas` files.

**CLI (Obsidian CLI)** — Command-line interface (1.12+) controlling the running app: `obsidian <command> param=value`.

**Community plugin** — A third-party plugin installed from Obsidian's directory (or via BRAT); runs with full access to the vault.

**Core plugin** — A plugin shipped with Obsidian and toggled in settings (Daily notes, Templates, Bases, Canvas…).

**cssclasses** — Property listing CSS classes applied to a note's view container for per-note styling.

**Daily note** — The note for a date (`YYYY-MM-DD`), created by the Daily notes core plugin; the guide's universal inbox and log.

**Dataview** — Community plugin providing a query language (DQL) and JavaScript API over notes' metadata, inline fields, tasks and lists.

**DQL** — Dataview Query Language: `TABLE/LIST/TASK/CALENDAR … FROM … WHERE … SORT …`.

**Embed / transclusion** — `![[Note]]`, `![[Note#Heading]]`, `![[Note#^block]]`: renders the target's content live inside the current note.

**Evergreen note** — An atomic, concept-oriented, densely linked note revised over time (Andy Matuschak); the guide's `type: note` with `status: evergreen`.

**File over app** — The principle that your files should outlive any application; Obsidian's design philosophy.

**Fleeting note** — A quick, temporary capture destined to be processed or discarded (Zettelkasten).

**Folder template** — Templater setting that applies a template automatically to new notes created in a given folder.

**Frontmatter** — YAML metadata between `---` fences at the top of a note; the storage format for **properties**.

**Graph view** — Visualization of notes as nodes and links as edges; global or local (neighbourhood of the current note).

**GTD** — Getting Things Done (David Allen): capture, clarify, organize, reflect, engage; projects, next actions, waiting-for, someday/maybe, weekly review.

**Hotkey** — A keyboard shortcut bound to a command; stored in `.obsidian/hotkeys.json`.

**Inline field** — Dataview's `key:: value` syntax in the body of a note; not visible to Bases or core Obsidian.

**Installer version** — The Electron shell version, updated only by reinstalling Obsidian; distinct from the app version.

**Interstitial journaling** — Timestamped one-line log entries at transitions between tasks.

**Keychain** — Obsidian's secret storage (1.11+) for plugin API keys.

**Link (wikilink / Markdown link)** — `[[Note]]` (Obsidian's default) or `[text](Note.md)`.

**Literature note** — Notes on what a source says, in your words, with references; the guide's `type: source` note body.

**Live Preview** — The editing mode that renders Markdown except where the cursor is; alternatives are Source mode and Reading view.

**LYT** — Linking Your Thinking (Nick Milo): MOCs, the Home note, ACCESS folders, fluid frameworks.

**MOC (Map of Content)** — A note that curates links to other notes on a topic with commentary and order; created when a cluster of notes demands navigation.

**MCP** — Model Context Protocol; servers that expose your vault (files or REST API) to AI clients.

**Note type** — The `type` property's value (`project`, `person`, `source`…), driving templates, Bases and dashboards.

**Obsidian Publish / Sync** — Obsidian's paid services for publishing notes as a website and for end-to-end encrypted synchronization.

**PARA** — Projects, Areas, Resources, Archive (Tiago Forte): organizing by actionability.

**Periodic notes** — Daily, weekly, monthly, quarterly, yearly notes; the Periodic Notes plugin manages the non-daily ones.

**Permanent note** — Zettelkasten's own-words idea note, written for the future; the guide's `type: note`.

**Progressive summarization** — Layered distillation on revisit: bold → highlight → summary (Tiago Forte).

**Properties** — Typed key–value metadata (text, list, number, checkbox, date, datetime) stored as frontmatter, edited in the property editor, queried by Bases and Dataview.

**Quick switcher** — Fuzzy file/alias finder (++ctrl+o++); also creates notes.

**Restricted mode** — Setting that disables all community plugins; the first diagnostic step.

**Snippet (CSS)** — A `.css` file in `.obsidian/snippets/` toggled in Appearance settings.

**Spaced repetition** — Review scheduling that grows intervals for remembered items (SM-2, FSRS); Spaced Repetition plugin or Anki.

**Stack tabs** — Sliding-pane layout of a tab group (Andy Matuschak-style).

**Tag** — `#tag` or `#nested/tag`, in text or the `tags` property; a lightweight cross-cutting label.

**Tasks (plugin)** — Community plugin adding due/scheduled/start dates, recurrence, priorities, dependencies and a query language to checkbox items.

**Templater** — Community plugin for dynamic templates with JavaScript (`<% %>`), prompts, file operations and folder templates.

**Unresolved link** — A link to a note that does not exist yet; dimmed; creatable by clicking.

**URI (obsidian://)** — URL scheme to open, create, append to, or search notes from outside Obsidian; extended by the Advanced URI plugin.

**Vault** — A folder Obsidian opens as a workspace; contains notes, attachments and `.obsidian/` configuration.

**Weekly review** — The GTD ritual of clearing inboxes, reviewing every project and list, and planning the week; the guide's highest-leverage habit.

**Workspace (layout)** — The arrangement of panes, tabs and sidebars; saved/loaded by the Workspaces core plugin.

**Zettelkasten** — Luhmann's slip-box method: atomic notes in your own words, linked with reasons, structure emerging bottom-up.

## Official resources

- **Obsidian Help** — help.obsidian.md / obsidian.md/help: the reference for every core feature; the Bases section (syntax, functions, views) is essential.
- **Changelog & roadmap** — obsidian.md/changelog, obsidian.md/roadmap: read release notes for breaking changes (CSS variables, removed commands, new APIs).
- **Developer docs** — docs.obsidian.md: plugin API, CSS variables, theme guide, submission guidelines, settings API migration.
- **Obsidian CLI reference** — obsidian.md/help/cli.
- **Web Clipper** — obsidian.md/clipper (templates, variables, Interpreter).
- **JSON Canvas spec** — jsoncanvas.org.
- **Obsidian sample plugin** — github.com/obsidianmd/obsidian-sample-plugin.
- **Obsidian Importer** — help pages per source (Notion, Evernote, Airtable…).
- **kepano/obsidian-skills** — Agent Skills for Markdown, properties, Bases, JSON Canvas and the CLI (github.com/kepano/obsidian-skills).

## Plugin documentation worth reading as tutorials

- **Tasks** — publish.obsidian.md/tasks: the best plugin docs in the ecosystem; the "Queries" and "Getting started" sections teach task management, not just syntax.
- **Dataview** — blacksmithgu.github.io/obsidian-dataview: DQL reference, functions, DataviewJS API; the examples pages.
- **Templater** — silentvoid13.github.io/Templater: every `tp.*` function with examples; user scripts; settings.
- **Excalidraw** — the plugin's GitHub wiki and Zsolt Viczián's videos.
- **Minimal theme** — minimal.guide: also a good general reference for what CSS can change.
- **Meta Bind**, **QuickAdd**, **Zotero Integration**, **PDF++**, **Longform**, **Spaced Repetition** — each has a docs site linked from its plugin page; read them once fully.
- **Quartz** — quartz.jzhao.xyz; **Digital Garden** — dg-docs.ole.dev.

## Communities

- **Obsidian Forum** (forum.obsidian.md) — the canonical place for help, feature requests, bug reports, and long-form "share & showcase" threads; search before asking.
- **Obsidian Discord** — real-time help, plugin-dev channels, theme channels.
- **r/ObsidianMD** — showcases, questions, plugin announcements; high volume, variable quality.
- **Obsidian Hub** (publish.obsidian.md/hub) — community-maintained guides, plugin categories, showcase vaults.
- **Plugin repositories** — each plugin's GitHub Issues/Discussions is where bugs are actually fixed.
- **Linking Your Thinking** community and workshops (Nick Milo) for MOC-centred practice.

## Books and essays behind the methods

- Sönke Ahrens, *How to Take Smart Notes* — the Zettelkasten method for modern readers.
- Niklas Luhmann, "Communicating with Slip Boxes" (essay) — the original argument.
- Andy Matuschak, *Evergreen notes* (public notes at notes.andymatuschak.org) — the clearest statement of how to write notes that stay valuable.
- Nick Milo, *Linking Your Thinking* materials — MOCs, ACCESS, fluid frameworks.
- Tiago Forte, *Building a Second Brain* — CODE, PARA, progressive summarization.
- David Allen, *Getting Things Done* — the action-management system.
- Ryder Carroll, *The Bullet Journal Method* — rapid logging, migration, reflection.
- Johnny Noble, *Johnny.Decimal* (johnnydecimal.com) — numbered organization for documents.
- Cal Newport, *Deep Work* and *A World Without Email* — attention as the scarce resource; context for why capture must be fast and review must be scheduled.
- James Clear, *Atomic Habits* — habit design that maps onto routines and daily-note checkboxes.
- Annie Duke, *Thinking in Bets* — the case for decision journals and confidence calibration.
- Steph Ango (kepano), "File over app" and related essays (stephango.com) — Obsidian's philosophy from its CEO.

## Keeping current

Obsidian ships a notable release every few months. A light routine: skim the changelog on each update (five minutes); once a quarter, check the roadmap and the plugin update notes for plugins you depend on; once a year, revisit this guide's chapters on Bases, automation, and AI — the three areas moving fastest.

## Closing

A vault is not a productivity system, a database, or a digital garden — it is all of those when needed and none of them when not, because underneath it is a folder of text you own, linked the way your life is actually connected. Build the skeleton, keep the daily note, do the weekly review, and let the rest grow. The point was never the notes; it was the life they help you notice, decide, and remember.

---

*Back to the [start](index.md) · [Single-file edition (GUIDE.md)](https://github.com/gorg667/obsidian-guide/blob/main/GUIDE.md)*
