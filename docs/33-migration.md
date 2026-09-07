# Migration — Into and Out of Obsidian

Most people arrive at Obsidian with years of notes somewhere else: Notion, Evernote, Apple Notes, OneNote, Roam, Logseq, Google Keep, Bear, Craft, Airtable, a folder of Word documents. The official **Importer** plugin handles the mechanics for most of them; the hard part is deciding what to bring, how to restructure it into the vault's schema, and cleaning up afterwards. This chapter covers the decision, tool-by-tool import notes, post-import cleanup, and — because "file over app" is a promise you should be able to keep — exporting *out* of Obsidian.

## Decide what to bring

1. **Do not import everything.** Old notes you never open are weight. Import (a) anything you have searched for in the last two years, (b) reference records with lasting value (recipes, admin, people), (c) journals (always — they are irreplaceable), (d) creative work. Leave the rest in a read-only export archive outside the vault (a zip; a `Archive/Imports/` folder excluded from search if you must).
2. **Import into a staging folder** (`Imports/<Source>/`), never straight into the skeleton. Process from there into typed notes over weeks.
3. **Restructure as you process**, not before: give each kept note a `type`, fix links, move to its folder. A note processed is a note you have re-read — the migration doubles as a review.
4. **Keep the source export** until you are sure.

## The Importer plugin (core)

Settings → Core plugins → Importer → *Open Importer*. Choose the format, the export file/folder, and the output folder in the vault. Supported (2026): **Notion** (HTML/Markdown export ZIP; databases become Bases since Nov 2025), **Evernote** (`.enex`), **Apple Notes** (direct on macOS), **Bear** (Markdown/`.bear2bk`), **Roam Research** (JSON), **Google Keep** (Takeout JSON), **Microsoft OneNote** (via Microsoft account), **HTML** (files/folders), **Markdown** (other flavours: Textbundle, Zettlr, etc.), **Airtable** (Aug 2026; tables → Markdown + Bases), and more added over time. Options per importer: preserve folders, attachment folder, convert links.

## Source-by-source notes

### Notion

Export from Notion: Settings → Export all workspace content → **Markdown & CSV** (include subpages, create folders for subpages). Importer converts pages to notes, page links to wikilinks, **databases to Bases** with rows as notes (properties from columns — select/multi-select → text/list, date → date, checkbox → checkbox, relation → links, formula → static values). Cleanup: Notion appends IDs to filenames (`Page abc123.md`) — Importer strips most; check for stragglers; nested toggles become plain text; callouts become blockquotes (convert to `> [!note]` with a regex); embedded databases become links; images land in the attachments folder. Notion's *relations* become link lists — exactly what Bases wants. Formulas need re-implementing as Bases formulas.

### Evernote

Export notebooks as `.enex` (one per notebook keeps structure). Importer converts notes, tags (→ `tags` property), created/updated dates (→ properties), attachments, and internal note links. Cleanup: Evernote's HTML tables and colours simplify; web clips are heavy — decide per note; notebooks become folders (rename to your skeleton); stacks are lost (recreate as MOCs or folders).

### Apple Notes

Importer reads Apple Notes directly on macOS (grant Full Disk Access). Folders → folders, attachments included, checklists → tasks, tables → Markdown tables, links between notes → wikilinks where possible. Cleanup: formatting-heavy notes (colours, fonts) flatten; locked notes must be unlocked first; drawings export as images.

### OneNote

Importer authenticates with Microsoft and pulls notebooks → sections → pages as folders and notes. Ink/drawings become images; page layout (free-positioned boxes) becomes sequential text — review layout-heavy pages manually.

### Roam Research

Export as JSON. Importer maps pages to notes, blocks to list items, `((block refs))` to block embeds where resolvable, `[[links]]` intact, `#tags`, daily notes to a daily-notes folder with your date format, attributes (`key:: value`) to inline fields (convert important ones to properties). Cleanup: outliner-style notes are nested bullets — flatten the ones that are prose; `{{TODO}}` → `- [ ]` (Format converter plugin does bulk conversion).

### Logseq

No dedicated importer needed — Logseq is Markdown. Copy `pages/` and `journals/` into a staging folder. Convert: `property:: value` at page top → YAML (a small script is the most reliable way); journal filenames `2026_09_06.md` → `2026-09-06.md`; `{{embed ((uuid))}}` block refs → Obsidian block IDs (imperfect; many become plain links); `- ` top-level bullets on every line → flatten prose; `#[[Tag with spaces]]` → `[[Tag with spaces]]` or `#tag_with_spaces`; `TODO`/`DOING`/`DONE` keywords → task syntax (Format converter helps).

### Google Keep

Takeout → JSON. Importer maps notes, labels → tags, colours → a property, checklists → tasks, pinned/archived → properties, attachments. Keep notes are small; many belong in `Inbox/` for triage or straight into typed records (shopping lists → delete; recipes → `type: recipe`).

### Bear, Craft, Ulysses, iA Writer, Drafts, Simplenote, Standard Notes, Joplin, Zettlr, Typora, Dendron, Foam, Athens

All Markdown-ish: export to Markdown/Textbundle and use the Markdown importer or copy files. Fix each app's dialect: Bear's `#tag/nested` and `::highlight::`; Craft's blocks and `craftdocs://` links; Ulysses's `++`/`::` marks; Joplin's `:/resource-id` links and metadata; Dendron/Foam are already Obsidian-compatible (Dendron hierarchies `a.b.c.md` → folders or keep); Zettlr's ID-based links → aliases.

### Airtable, Notion databases, spreadsheets, CSV

Airtable importer (2026) and Notion's database import produce **one note per row with properties plus a Base**. For arbitrary CSV/Excel: a short script (Python with `csv`/`pandas`) writes one Markdown file per row with YAML from the columns and a `.base` for the table; or the **Dataview** `csv()` source for read-only viewing without conversion; or the JSON/CSV importer plugins in the community directory. Decide column → property types up front (Chapter 5 naming rules).

### Word / Google Docs / PDFs

Pandoc: `pandoc doc.docx -t gfm --extract-media=Attachments -o doc.md` (batch with a loop). Google Docs → download as DOCX first (or Markdown export, which Docs supports natively now). PDFs: keep as attachments and write notes *about* them; OCR/extraction only for text you need searchable (Text Extractor for Omnisearch).

### Email

Not a notes migration; selectively export the emails that are actually notes (recipes you sent yourself, decisions) via a script (IMAP → Markdown) or by forwarding into a capture pipeline (Chapter 29).

### Todoist / Things / Trello / Asana

Export (CSV/JSON) → script → tasks with `📅` dates into project notes, or into a single `Imports/Tasks.md` to triage. Most old tasks should be deleted, not migrated. Boards → Kanban plugin notes or Bases kanban with a `status` property.

### Another Obsidian vault

Copy the folder. Merging two vaults: copy notes into `Imports/OtherVault/`, resolve filename collisions (unique names!), merge templates and snippets by hand, reconcile property schemas (rename with the Properties view), then move notes into the skeleton. Plugins: enable the union, then audit.

## Post-import cleanup

1. **Filenames**: strip IDs and forbidden characters; ensure uniqueness (a DataviewJS duplicate-title query); apply naming conventions (dates for events, claims for ideas).
2. **Frontmatter**: add `type` to everything (a Base "Missing type" view; Bases table paste to set a column; or a script/agent); convert inline `key:: value` to YAML where they are real properties; normalize date formats to ISO (Linter can); rename properties to `snake_case` (Properties view rename).
3. **Links**: run *Unlinked mentions* passes on key notes; fix unresolved links (`obsidian unresolved counts`); convert Markdown links to wikilinks if you prefer (*Format converter* or the **Link Converter** plugin); check that aliases cover old titles.
4. **Formatting**: `> [!note]` callouts from blockquotes with markers; task syntax; heading levels (imported H1s inside bodies conflict with inline titles — demote); remove HTML residue (`<div>`, `<span style>`) with regex replace; tables.
5. **Attachments**: move into `Attachments/`; rename meaningful ones; delete unused (Janitor).
6. **Tags**: consolidate (Tag Wrangler); convert entity tags to links (`#john` → `[[John Smith]]`).
7. **Folders**: move processed notes from `Imports/` into the skeleton in batches; delete `Imports/` when empty.
8. **Commit** (Git) after each batch; the migration is the best time to have version control.

Automation help: Linter (bulk formatting/YAML), Format converter (syntax), Regex Find/Replace (vault-wide regex), Metadata Menu (bulk property edits), Bases tables (paste a property down a column), the Obsidian CLI (`property:set` in a loop), and — with care and Git — a coding agent (Chapter 30) for "add `type: recipe` to every note in Imports/Keep that has an Ingredients heading".

## Migration plan (realistic)

| Week | Do |
| --- | --- |
| 0 | Set up the skeleton, templates, Bases (Chapter 8). Export from the old tool; keep the export. |
| 1 | Import into `Imports/<Source>/`. Do not touch the skeleton with it. Start using Obsidian for *new* notes immediately. |
| 2–6 | Process 20–50 imported notes a day during the daily review: type, link, move, or delete. Journals first (bulk move with a script to `Journal/Daily/` after renaming), records second, ideas last (they need reading). |
| 6+ | Whatever remains in `Imports/` after six weeks is, by revealed preference, not needed: zip it to the archive outside the vault, delete the folder. |

Living in both tools "for a while" is the common failure; set a date and stop writing in the old one on day one.

## Exporting out of Obsidian

The promise: your notes are Markdown; leaving is trivial. Almost.

- **Plain Markdown consumers** (VS Code, iA Writer, Zettlr, Logseq, Foam, GitHub, any static-site generator): copy the folder. Wikilinks `[[Note]]` and embeds `![[…]]` are the non-standard parts; convert with **Link Converter**/**Format converter** or a script to `[Note](Note.md)` and `![](Attachments/x.png)`; callouts `> [!note]` are GitHub-compatible (GitHub renders them); `==highlights==` and `%%comments%%` are Obsidian-only — regex to `<mark>` / strip.
- **Properties**: YAML frontmatter is standard; other tools may ignore types (dates as strings are fine).
- **Bases** (`.base`) and **Canvas** (`.canvas`, open JSON Canvas spec) have growing but not universal support; export Bases views to CSV (`obsidian base:query format=csv`) as a fallback; Canvas has third-party renderers.
- **Plugin-specific syntax** (Dataview blocks, Templater tags, Tasks emoji, Excalidraw JSON, Kanban markers) will not render elsewhere: bake Dataview results to static Markdown before leaving (a script using the Local REST API or DataviewJS to write results), export Excalidraw drawings to SVG/PNG, keep Tasks emoji (they are just text), leave Kanban as its Markdown lists.
- **To Notion/Evernote/etc.**: they import Markdown/HTML; Pandoc to HTML preserves the most.
- **To a book/PDF**: Longform compile + Pandoc (Chapters 18, 24).
- **To the future**: a yearly zip of the vault plus a `README` describing the conventions — readable without any app.

## Key takeaways

- Import selectively into a staging folder; process into typed notes over weeks; archive the rest outside the vault; stop writing in the old tool on day one.
- The Importer plugin covers Notion (with databases → Bases), Evernote, Apple Notes, OneNote, Roam, Keep, Bear, HTML, Markdown variants, Airtable; Markdown-based apps need only dialect fixes; spreadsheets become notes-plus-Base via a script.
- Cleanup: filenames, `type` on everything, properties normalized, links fixed, formatting converted, attachments organized, tags consolidated — with Linter, Format converter, Regex Find/Replace, Bases tables, the CLI, and Git.
- Leaving is copying a folder plus converting wikilinks and baking plugin-generated content; Bases export to CSV; Canvas is open JSON.

## Next

[Chapter 34: Plugin Development Primer →](34-plugin-development-primer.md)
