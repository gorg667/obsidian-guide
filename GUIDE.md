# The Complete Obsidian Mastery Guide

> Single-file edition. Generated automatically from the chapter files in `docs/` by `scripts/build_guide.py`. The web edition lives at <https://gorg667.github.io/obsidian-guide/>.

## Table of contents

1. [Philosophy and Mental Model](#philosophy-and-mental-model)
2. [Setup, Settings and Interface](#setup-settings-and-interface)
3. [Markdown and Editing Mastery](#markdown-and-editing-mastery)
4. [Links, Backlinks, Graph and Canvas](#links-backlinks-graph-and-canvas)
5. [Properties, Tags and Metadata Design](#properties-tags-and-metadata-design)
6. [Search Mastery](#search-mastery)
7. [PKM Methodologies Compared](#pkm-methodologies-compared)
8. [Vault Architecture — the Reference Design](#vault-architecture-the-reference-design)
9. [Core Plugins — Every One, Mastered](#core-plugins-every-one-mastered)

---

# Philosophy and Mental Model

Most people who "fail" with Obsidian do not fail because of a missing feature. They fail because they carry a mental model from another tool — Notion's databases, Evernote's notebooks, Apple Notes' folders — and fight Obsidian instead of using it. This chapter installs the correct mental model. Everything later in the guide builds on it.

## What Obsidian actually is

Strip away the marketing and Obsidian is four things stacked on top of each other:

1. **A folder of plain-text files on your disk.** The vault is a directory. Every note is a `.md` file. Attachments are ordinary files. Configuration is JSON in a hidden `.obsidian/` folder. Nothing is stored in a proprietary database. You can open the folder in Finder or Explorer, `grep` it, back it up with any tool, or point another editor at it.
2. **A Markdown editor with a live-rendering mode.** It is a good editor — multi-cursor, Vim mode, folding, a formatting menu, tables, callouts — but it is still fundamentally editing text.
3. **A link-and-metadata index.** Obsidian scans your vault and builds an in-memory index of links, backlinks, tags, properties, headings and blocks. The graph view, backlinks pane, Bases, and every query plugin read from this index.
4. **A plugin platform.** Core plugins (shipped with the app, toggleable) and community plugins (open-source, installed from a directory) extend all three layers above. The app itself is Electron on desktop and Capacitor on mobile, and plugins are JavaScript with full access to the vault and the UI.

```mermaid
flowchart TB
    subgraph L4[Layer 4 — Plugins]
      P1[Core plugins] --- P2[Community plugins] --- P3[Themes & CSS]
    end
    subgraph L3[Layer 3 — Index]
      I1[Links & backlinks] --- I2[Tags & properties] --- I3[Headings & blocks]
    end
    subgraph L2[Layer 2 — Editor]
      E1[Live Preview] --- E2[Source mode] --- E3[Reading view]
    end
    subgraph L1[Layer 1 — Files on disk]
      F1[notes/*.md] --- F2[attachments/*] --- F3[.obsidian/ config] --- F4[*.base / *.canvas]
    end
    L4 --> L3 --> L2 --> L1
```

The reason this matters: **the file layer is the truth**. Everything above it is a view. If Obsidian disappeared tomorrow you would lose nothing but convenience. This is the "file over app" principle that Obsidian's CEO Steph Ango has written about, and it has practical consequences throughout this guide: prefer formats and conventions that survive without Obsidian, and treat plugins as accelerators, not as the place where your data lives.

## The five primitives

Everything you will ever build in Obsidian is a combination of five primitives. Learn to see them.

### 1. Notes (files)

A note is a file. Its **title is its filename**. This is more consequential than it sounds:

- Filenames cannot contain `/ \ : * ? " < > |` and Obsidian also forbids `#`, `^`, `[`, `]` and `|` in note names because they conflict with link syntax.
- Renaming a note is a filesystem rename, and Obsidian rewrites every link that points to it (if the setting is on — keep it on).
- Two notes cannot share a name in the same folder, but *can* share a name in different folders — which makes `[[Name]]` links ambiguous. Avoid this.
- Because the title is the filename, "what should I call this note?" is a real design decision. The methodology chapter covers naming conventions in depth.

A note optionally has **properties** (YAML frontmatter), a body of Markdown, and any number of headings and blocks that can be addressed individually.

### 2. Links

A link is a pointer from one note to another: `[[Target]]`, `[[Target#Heading]]`, `[[Target#^blockid]]`, or `[[Target|Shown text]]`. Links are the connective tissue of a vault and the thing Obsidian does better than any competitor. Key properties:

- **Links are bidirectional in the index.** Write `[[Berlin]]` in your travel note and the Berlin note's backlinks pane now shows the travel note — with no action on your part.
- **Links can point to notes that don't exist yet.** They render dimmer and become real the moment you click them. This lets you link *first* and write *later*, which is the core of "bottom-up" knowledge building.
- **Unlinked mentions** surface places where a note's name appears as plain text, offering one-click linking.
- **Embeds** are links with a `!` prefix: `![[Target]]` shows the target's content inline. You can embed notes, headings, blocks, images, PDFs (with page numbers), audio, video, canvases, and bases.

### 3. Tags

`#tag` and `#nested/tag`, in the body or in the `tags` property. Tags are lightweight, cross-cutting labels. They are cheap to add and cheap to query. They are also the most over-used primitive by beginners; Chapter 5 gives a decision framework for tags vs properties vs links vs folders.

### 4. Properties (metadata)

Structured `key: value` data at the top of a note in YAML. Since Obsidian 1.4 they have typed UI (text, list, number, checkbox, date, datetime), and since 1.9 they are the fuel for Bases. Properties turn a pile of notes into a *database* without leaving plain text. A note with:

```yaml
---
type: book
author: "[[Cal Newport]]"
status: reading
rating: 4
started: 2026-08-14
tags: [productivity, focus]
---
```

…is simultaneously a readable page and a row in any table you care to build.

### 5. Folders

Folders are the physical location of a file. They are the primitive people over-invest in first and regret later, because a note can live in only one folder while it can have unlimited links, tags, and properties. Folders still matter — for attachment routing, for templates that auto-apply per folder, for Bases filters like `file.inFolder("Projects")`, and for keeping the file explorer sane — but they should be *few and stable*.

## The three ways to organize, and why you need all of them

There are three fundamentally different organizing strategies, and mature vaults use all three deliberately:

| Strategy | Primitive | Strengths | Weaknesses | Use it for |
| --- | --- | --- | --- | --- |
| **Hierarchy** | Folders | Familiar, physical, works with any tool, supports per-folder automation | One location per note; deep trees rot; encourages filing over thinking | A small number of top-level "kinds of thing" (e.g. `Notes`, `Journal`, `Projects`, `Sources`, `Templates`, `Attachments`) |
| **Network** | Links, MOCs | Emergent structure; supports multiple contexts; serendipity via backlinks | Needs active tending; can become an undifferentiated hairball | Ideas, concepts, people, projects — anything with relationships |
| **Attributes** | Tags, properties | Precise filtering and sorting; enables dashboards; machine-readable | Requires discipline and a schema; meaningless without queries | Status, type, dates, ratings, categories — anything you want to *query* |

The single most useful habit is to ask, for each note, "which of these strategies does this note need?" A meeting note needs attributes (date, attendees, project) and links (to the people and the project) but no special folder. A permanent idea note needs links above all. A recipe needs attributes (cuisine, time, servings) and belongs to one obvious folder.

## Bottom-up vs top-down

Two schools argue about how to build a vault.

**Top-down** designs the structure first: folders, templates, property schemas, MOCs, dashboards. Then notes are filed into it. This is how most productivity content online approaches Obsidian and it produces beautiful screenshots. Its failure mode is a cathedral with no congregation — an elaborate system you stop using after three weeks because maintaining it is a job.

**Bottom-up** writes notes first, links freely, and lets structure emerge. When a cluster of notes becomes noticeable, you create a Map of Content (MOC) to index it. When a pattern of properties recurs, you formalize a template. This is the Zettelkasten / LYT lineage. Its failure mode is a swamp — thousands of notes with no way in.

The guide's position: **structure the containers top-down, let the content grow bottom-up.** Decide your folder skeleton, your note types, your property schema, and your naming conventions up front (Chapter 8 gives you a complete one). Then within that skeleton, write and link without asking permission from your system. Create MOCs and dashboards only when the volume of notes demands them.

## Two modes of use: retrieval and thinking

Obsidian serves two very different jobs and you should know which one you are doing at any moment.

**Retrieval** is "where did I put that?" — the Wi-Fi password, the recipe, the meeting decision, the article you clipped. Retrieval wants *predictability*: consistent names, consistent properties, consistent locations, good search. Bases, properties, folders, and search are the tools. Over-linking retrieval notes wastes time.

**Thinking** is "what do I believe about this?" — ideas, arguments, decisions, syntheses. Thinking wants *connection*: links to related ideas, backlinks that surface forgotten context, writing in your own words, revisiting. Links, MOCs, the local graph, and daily notes are the tools. Over-structuring thinking notes kills them.

A "whole life" vault contains both, and one of the reasons it is worth putting *everything* in Obsidian is that the boundary is porous: a retrieval note (a book you read) becomes a thinking note (what you took from it), and thinking notes feed action (a project). Keeping them in one place with one link syntax is the actual killer feature.

## What Obsidian is bad at (and what to do about it)

Honesty about limits saves months.

- **Real-time collaboration.** Two people editing the same note simultaneously is not a thing. Obsidian Sync supports multiple users on one vault, but with last-writer-wins at the file level (with version history to recover). For team wikis and shared docs, use something else and link to it.
- **Relational data with joins.** Bases and Dataview are excellent for single-table views over notes. Multi-table relational queries are possible (DataviewJS) but awkward. If you need a real database — an inventory with thousands of SKUs, accounting — use one, and keep the *narrative* in Obsidian.
- **Heavy attachments.** Obsidian stores files fine, but a vault with 50 GB of video syncs badly and indexes slowly. Keep large media outside the vault and link to it, or in a separate vault.
- **Rich text fidelity.** Markdown cannot represent every formatting nuance of a Word document. If you need pixel-perfect documents, write in Obsidian and export via Pandoc.
- **Structured forms and input validation.** Plugins like Meta Bind get you far, but there is no native form builder.
- **Mobile power features.** Mobile Obsidian is remarkably complete, but plugins with heavy UI, huge vaults, and Git-based sync are painful on phones. Design mobile workflows for *capture and reading*, not administration.
- **Being a calendar or email client.** It can display calendars (plugins) and you can email into it (automation), but it should not replace them.

## Principles that survive every chapter

These come up again and again. Internalizing them now makes the rest of the guide faster.

!!! tip "1. Plain text is the API"
    Any feature that stores its data as human-readable text in your notes (properties, tasks, inline fields, callouts) is durable and portable. Any feature that stores data in `.obsidian/plugins/*/data.json` is convenient but fragile. Prefer the former for anything you would grieve losing.

!!! tip "2. Titles are links"
    Because the filename is both the title and the link target, name notes the way you would *refer to them in a sentence*. `[[Cal Newport]]` reads naturally; `[[newport_cal_author]]` does not. Aliases handle synonyms.

!!! tip "3. Friction goes at the exit, not the entrance"
    Capturing must be near-zero-friction (hotkey, template, mobile share sheet). Processing — deciding where a note lives, what it links to — can be batched later in a review. Systems that demand perfect filing at capture time die.

!!! tip "4. Query, don't file"
    If you find yourself maintaining a list by hand — "all open projects", "books to read", "recent meetings" — stop. That list should be a Base or a Dataview query driven by properties. Hand-maintained lists are always out of date.

!!! tip "5. One vault unless you have a reason"
    Links do not cross vaults. Search does not cross vaults. Every split costs you connections. Legitimate reasons to split: legal separation (work confidentiality), radically different sync requirements, or a vault that is really a project (a book manuscript, a shared family vault). "It feels cleaner" is not a reason.

!!! tip "6. Plugins are power tools — count them"
    Every plugin is code running with full access to your files, load time on mobile, and a maintenance dependency. A healthy vault has 10–25 community plugins that you can each name the purpose of. Chapter 14 gives tiers; Chapter 32 gives an audit routine.

!!! tip "7. Build for the tired version of you"
    You will use the vault at 11 pm, on a phone, after a bad day. Templates, hotkeys, and dashboards exist so the system works when your willpower does not.

## The four layers of mastery

It helps to know where you are and what comes next. Most users plateau at layer 2.

| Layer | You can… | Typical signs | This guide's chapters |
| --- | --- | --- | --- |
| **1. Editor** | Write Markdown, make links, use folders, search | Vault looks like a fancier Apple Notes | 2, 3, 4 |
| **2. Networker** | Use backlinks deliberately, MOCs, daily notes, tags, a few plugins | Graph view has recognizable clusters | 5, 6, 7, 9 |
| **3. Systems builder** | Design property schemas, templates, Bases/Dataview dashboards, task system, reviews | You *query* your vault; you rarely make lists by hand | 8, 10–13, 15–25 |
| **4. Operator** | Automate with CLI/URI/scripts, integrate external apps and AI, customize the UI, write small plugins, maintain and migrate at scale | The vault is your life's control panel and it runs itself | 26–34 |

The [Mastery Roadmap](35-mastery-roadmap.md) turns this into a schedule.

## Key takeaways

- Obsidian is a folder of text files plus an index plus plugins. The files are the truth; everything else is a view.
- Five primitives — notes, links, tags, properties, folders — combine into every system you will build. Learn to see them.
- Use hierarchy for containers, network for ideas, attributes for anything you will query. Mature vaults use all three deliberately.
- Structure containers top-down; let content grow bottom-up.
- Know whether a note is for *retrieval* or *thinking* and organize accordingly.
- Prefer plain-text-stored features, query instead of filing, keep one vault, count your plugins, and design for your tired self.

## Next

[Chapter 2: Setup, Settings and Interface →](#setup-settings-and-interface)

---

# Setup, Settings and Interface

A vault configured thoughtfully in the first hour saves hundreds of small frustrations later. This chapter is a complete audit: every setting that materially affects how you work, what to set it to and why, plus the interface anatomy and keyboard-first habits that separate fluent users from clickers.

## Installation and installer versions

Obsidian has two version numbers and confusing them causes real problems.

- **App version** (e.g. 1.13.4) — the JavaScript application. Updates automatically in-app on desktop; via the store on mobile.
- **Installer version** — the Electron shell (Chromium + Node) the app runs in. It only updates when you **download and reinstall from obsidian.md**. Check it under **Settings → General → About** ("Installer version").

!!! warning "Reinstall the installer at least once a year"
    Features like the Obsidian CLI require installer 1.12.7+, Bases performance improved with newer Electron builds, and several rendering bugs are installer-level. Reinstalling does not touch your vault. On Windows use the same edition (system vs. per-user) you originally installed to avoid two copies.

| Platform | Recommended install | Notes |
| --- | --- | --- |
| Windows | Official installer from obsidian.md | winget (`winget install Obsidian.Obsidian`) also works and tracks installer versions. |
| macOS | Official DMG or `brew install --cask obsidian` | Universal build; Apple Silicon native. |
| Linux | AppImage (most portable), Flatpak, Snap, or `.deb` | Flatpak and Snap sandbox file access; the CLI and some sync tools work best with AppImage or `.deb`. If using Flatpak, grant filesystem access with Flatseal to your vault folder. |
| iOS/iPadOS | App Store | Vault location: "On My iPhone/Obsidian" (local) or iCloud Drive. See [Sync](26-sync-backup-security.md). |
| Android | Play Store, F-Droid, or GitHub APK | Grant "All files access" for vaults outside app storage. |

## Where to put the vault

Decide this once. Moving later is possible but annoying.

- **Local disk, non-synced folder** — fastest, safest for plugins, zero conflicts. Use if you sync with Obsidian Sync, Git, or Remotely Save (they handle sync themselves).
- **iCloud Drive / OneDrive / Dropbox / Google Drive folder** — works on desktop; on mobile only iCloud is natively supported by Obsidian (iOS). Risks: "files on demand" placeholders (OneDrive) break indexing; conflicts create duplicate files; `.obsidian/` config churn triggers constant re-upload. If you must, exclude nothing and turn off "files on demand" for the vault folder.
- **Syncthing folder** — excellent on desktop and Android; not available on iOS.
- **Network drive / NAS** — avoid. Latency makes the editor sluggish and file watchers unreliable. Obsidian 1.13 warns when loading HTML resources from network paths for the same reason.

Chapter 26 has the full sync matrix.

## Vault-level decisions before you write

1. **One vault or several?** One, unless you have a hard reason (Chapter 1, principle 5). You *can* keep a scratch vault for experimenting with plugins.
2. **Attachment folder.** Set **Settings → Files and links → Default location for new attachments** to *In the folder specified below* → `Attachments` (or `_attachments`, `zz-attachments` to sort last). Never leave it as "vault root" or "same folder as current file" unless you like clutter.
3. **Link format.** *Wikilinks* (`[[Note]]`) are the Obsidian default, faster to type, and every plugin understands them. *Markdown links* (`[Note](Note.md)`) are more portable to other tools and required by some publishing pipelines. For the path style, **Shortest path when possible** produces clean `[[Note]]` links but is only safe if you keep filenames unique across the vault; **Absolute path in vault** produces `[[Folder/Note]]` and is unambiguous but noisier; **Relative path to file** breaks when notes move. Recommendation for a whole-life vault: Wikilinks on, unique filenames enforced by convention, shortest path.
4. **New note location.** *Same folder as current file* is the least surprising once you have a folder skeleton; combined with an `Inbox` folder as your default landing zone for quick capture.
5. **Naming convention.** Decide capitalisation (Title Case vs sentence case) and whether dates are `YYYY-MM-DD`. Decide now; consistency matters more than the choice.

## The complete settings audit

Settings are searchable since 1.13 (++ctrl+comma++ then type). Below, every setting that matters, grouped as Obsidian groups them. Defaults are fine where a setting is not listed.

### General

| Setting | Recommended | Why |
| --- | --- | --- |
| Automatic updates | On | Security and Bases/CLI improvements ship often. |
| Command line interface | On (desktop) | Enables `obsidian` CLI — see Chapter 29. Follow the prompt to register PATH. |
| Language | Your choice | Affects UI only, not your notes. |

### Editor

| Setting | Recommended | Why |
| --- | --- | --- |
| Default editing mode | Live Preview | WYSIWYG-ish while still Markdown. Switch to Source with ++ctrl+e++ (toggle) when you need to see raw syntax. |
| Default view for new tabs | Editing view | Reading view is for consumption; you are mostly writing. |
| Show line numbers | Off (on for code-heavy notes via `cssclasses`) | Noise for prose. |
| Readable line length | On | ~700px measure; disable per note with a CSS class if you need wide tables. |
| Strict line breaks | Off | With off, a single newline renders as a line break (like most note apps). With on, you need two spaces or a blank line — stricter CommonMark. Off is friendlier; on is more portable. Pick and never change (it changes how existing notes render). |
| Properties in document | Visible | Shows the typed property editor. "Source" shows raw YAML; "Hidden" hides it. |
| Show indentation guides | On | Helps with nested lists and tasks. |
| Fold heading / Fold indent | On | You will use folding constantly in long notes. |
| Spellcheck | On; add languages | Right-click → Add to dictionary for your jargon. |
| Auto pair brackets / Markdown syntax | On | Typing `[[` yields `[[]]`. |
| Smart indent lists | On | Tab/Shift-Tab indent list items. |
| Vim key bindings | Off unless you are a Vim user | If you are, it is remarkably complete (see Chapter 3). |
| Auto convert HTML | On | Pasting from the web becomes Markdown. |
| Indent using tabs / Tab size | Spaces, 4 (or tabs) | Some plugins (Tasks, Dataview) were historically picky about mixed indentation. Consistency is what matters. |

### Files and links

| Setting | Recommended | Why |
| --- | --- | --- |
| Confirm file deletion | On | Your trash is one accidental ++del++ away. |
| Deleted files | Move to Obsidian trash (`.trash` folder) | Recoverable within the vault; system trash is the alternative. Chapter 32 covers File Recovery. |
| Always update internal links | On | The reason renaming is safe. |
| Automatically delete attachments | Ask every time (1.12+) | When you delete a note, Obsidian offers to delete attachments only that note used. |
| Default location for new notes | Same folder as current file, *or* a fixed `Inbox` | See above. |
| New link format | Shortest path when possible (unique names) | See above. |
| Use Wikilinks | On | Toggle off only for portability requirements. |
| Detect all file extensions | Off (on temporarily to find stray files) | Otherwise your explorer shows `.DS_Store` and friends. |
| Default location for new attachments | In the folder specified below → `Attachments` | See above. |
| Excluded files | Add `Templates/`, `Attachments/`, `Archive/` if noisy | Excluded files are dimmed in search/suggestions/graph but still linkable and still indexed. Use it liberally for templates so `[[` suggestions are not polluted. |

### Appearance

| Setting | Recommended | Why |
| --- | --- | --- |
| Base color scheme | Adapt to system | Toggle command exists (1.10 replaced the separate light/dark commands with a single **Toggle light/dark mode**). |
| Accent color | Your call | Also used by links and selection. |
| Font size | 16 (desktop) | Zoom with ++ctrl+plus++ / ++ctrl+minus++ as needed. |
| Interface / text / monospace font | System UI; a good reading font (e.g. Inter, iA Writer Duo, Source Serif); JetBrains Mono / Fira Code | Fonts must be installed on each device. |
| Quick font size adjustment | On | ++ctrl++ + scroll. |
| Show inline title | On | The filename rendered as an H1 at the top; means you do not put `# Title` in the body. |
| Show tab title bar | On (desktop) | Off saves vertical space, but you lose the breadcrumb. |
| Ribbon | Reorder / hide items you never click | Right-click the ribbon → Configure. |
| Native menus (macOS) | Off | Obsidian's own menus are more consistent across platforms. |
| Window frame | Hidden (native title bar off) | Less chrome. |
| Zoom level | 100% | |
| Themes / CSS snippets | See Chapter 28 | |

### Hotkeys

Chapter 37 has the complete default list. The philosophy: leave defaults alone unless they conflict, and add hotkeys for the ~15 commands you use hourly. Non-negotiable additions for most people:

| Command | Suggested hotkey | Reason |
| --- | --- | --- |
| Toggle left / right sidebar | ++ctrl+alt+left++ / ++ctrl+alt+right++ (or click) | Focus mode on demand. |
| Open today's daily note | ++ctrl+shift+d++ | Your home base. |
| Insert template | ++alt+t++ | Constantly used until Templater takes over. |
| Toggle reading view | ++ctrl+e++ (default) | |
| Focus on last note / Focus on tab group | | Useful with split panes. |
| Move current file to another folder | ++ctrl+shift+m++ | Processing your inbox. |
| Add file property | ++ctrl+semicolon++ | Metadata without leaving the keyboard. |
| Toggle bullet / checkbox | ++ctrl+l++ (default toggles checkbox) | |
| Navigate back / forward | ++alt+left++ / ++alt+right++ | Web-browser habits. |
| Search in all files | ++ctrl+shift+f++ | |
| Open command palette | ++ctrl+p++ | |
| Open quick switcher | ++ctrl+o++ | |
| Toggle Bases view / Open Bases | | Once you build dashboards. |

!!! tip "Hotkeys are stored in `.obsidian/hotkeys.json`"
    Sync that file (Obsidian Sync can sync hotkeys; Git syncs everything) so your muscle memory survives device changes.

### Core plugins

Turn on: File explorer, Search, Quick switcher, Graph view, Backlinks, Outgoing links, Canvas, Daily notes, Templates, Note composer, Command palette, Bookmarks, Outline, Word count, File recovery, Page preview, Properties view, Tags view, Bases, Slash commands (optional), Unique note creator (if you use Zettelkasten IDs), Workspaces (once you have layouts), Web viewer (if you want in-app browsing), Random note (for serendipitous review), Importer (when migrating), Footnotes view (if you write academically), Sync/Publish (if subscribed), Slides (rarely). Chapter 9 details each.

### Community plugins

Turn off **Restricted mode**. Since 1.13 you can exit Restricted mode *without* re-enabling plugins, which is useful for debugging. Install nothing yet; Chapter 14 curates. The **Check for updates** button is in this tab — do it weekly.

### Sync / Publish

See Chapters 26 and 31. Notable 1.13 behaviour: Sync warns before syncing plugins between devices (because plugin data can be device-specific), and the status-bar icon no longer spins to save battery.

## Interface anatomy

```mermaid
flowchart LR
    subgraph Window
      direction LR
      R[Ribbon<br/>vertical icon bar] --- LS[Left sidebar<br/>File explorer · Search · Bookmarks · Tags]
      LS --- M[Main area<br/>Tab groups · splits · stacked tabs]
      M --- RS[Right sidebar<br/>Backlinks · Outgoing links · Outline · Properties · Calendar · local Graph]
    end
    SB[Status bar: word count · sync · plugins]
```

**Ribbon.** Vertical strip of icons on the far left. Every core and community plugin can add one. Right-click → hide the ones you never click; the actions remain in the command palette.

**Sidebars.** Both hold *tabs of views*. Drag any view between sidebars or into the main area (a Backlinks view in the main area is a legitimate way to review connections). Collapse with the small arrows or hotkeys. Pin a sidebar tab to keep it visible.

**Main area.** Tabs, like a browser. Split any tab horizontally/vertically (right-click the tab → Split, or drag it to an edge). A *tab group* is a set of tabs sharing a pane. **Stacked tabs** (right-click tab header → Stack tabs) turns a group into Andy Matuschak-style sliding cards — outstanding for research where you open six notes from one MOC.

**Status bar.** Bottom right: word/character count, backlink count, sync status, plugin indicators. Click items for menus. Hide with CSS if you prefer minimal.

**Tab title bar / inline title.** The breadcrumb (folder › note) and the note's H1-like title. Click the breadcrumb to navigate the folder; click the inline title to rename.

**Settings window.** Since 1.13 opens in a separate window with search and keyboard navigation (arrows to move, ++enter++ to open, ++ctrl+f++ to focus search). Disable "Open settings in new window" under Interface if you prefer the modal.

**Pop-out windows.** Drag a tab out of the app to make it a standalone window (desktop). Useful for a reference note on a second monitor.

## Navigation you should do from the keyboard

The fluent-user baseline. Everything else is optional; these are not.

- **Command palette** ++ctrl+p++ — type any command. Pin favourites (Settings → Command palette) to the top. Also try `>` prefix in Quick switcher.
- **Quick switcher** ++ctrl+o++ — fuzzy-find by filename. Type a new name and ++enter++ to create. ++shift+enter++ creates even if a fuzzy match exists. ++ctrl+enter++ opens in a new tab. Since 1.12 results can be dragged.
- **Search** ++ctrl+shift+f++ — full-text with operators (Chapter 6). ++ctrl+f++ searches within the current note.
- **Follow link under cursor** ++alt+enter++ (or ++ctrl+enter++ to open in a new tab). Hover with ++ctrl++ for a page preview.
- **Back / forward** ++alt+left++ / ++alt+right++ (++cmd+bracket-left++ / ++cmd+bracket-right++ on mac).
- **Go to next/previous tab** ++ctrl+tab++ / ++ctrl+shift+tab++; go to tab N ++ctrl+1++ … ++ctrl+9++.
- **Close tab** ++ctrl+w++; **reopen closed tab** ++ctrl+shift+t++.
- **Toggle sidebars** — assign hotkeys.
- **Reveal current file in navigation** — assign; essential in big trees.
- **Fold/unfold** ++ctrl+up++ / ++ctrl+down++ at heading; **Fold all / Unfold all** commands.
- **Focus on editor** ++esc++ from most panes.

## Workspaces and layouts

The **Workspaces** core plugin saves the entire layout (which panes, which files, which sidebar tabs) under a name and restores it in one command. Build three or four:

- **Writing** — single pane, sidebars collapsed, Outline in right sidebar.
- **Planning** — daily note left, task dashboard right, Calendar in sidebar.
- **Research** — stacked tabs in main, Backlinks + local Graph on the right.
- **Review** — weekly note, project Base, Habit tracker.

Save with *Workspaces: Save layout*, load with *Workspaces: Load layout*. The Obsidian CLI can load them (`obsidian workspace:load name=Planning`), which means a shell alias or a Raycast/Alfred/AutoHotkey script can put you in a mode instantly. Chapter 29 shows this.

!!! note "Workspaces + mobile"
    Mobile has its own layout; workspaces are per-device. The **Workspaces Plus** community plugin adds a switcher and per-workspace settings on desktop.

## Multiple vaults strategy (if you really need it)

- Vaults are completely isolated: separate plugins, settings, index. Cross-vault links use `obsidian://open?vault=Other&file=Note` URIs (they work but feel foreign).
- Share configuration between vaults with a symlink of `.obsidian/` subfolders (snippets, themes) — fragile with sync; do it only on a single machine.
- **Change vault…** (renamed *Manage vaults* in 1.12) lists vaults; the **Open vault…** command (1.12) opens another vault while keeping the current one open. The CLI accepts `vault=Name` as the first parameter.

## First-hour checklist

- [ ] Installer updated; app updated.
- [ ] Vault created in a sensible location; sync approach chosen (Chapter 26).
- [ ] Attachments folder set; excluded files set; link format decided.
- [ ] Editor: Live Preview, readable line length, folding, spellcheck, indentation guides.
- [ ] Appearance: theme (Chapter 28), inline title on, fonts.
- [ ] Core plugins enabled per list above; Restricted mode off.
- [ ] Hotkeys added for daily note, insert template, sidebars, move file, add property.
- [ ] Folder skeleton created (Chapter 8) with `Inbox`, `Templates`, `Attachments` at minimum.
- [ ] Templates folder set in **Templates** core plugin settings; Daily notes folder + format set.
- [ ] `.obsidian/` backed up (Chapter 26).

## Key takeaways

- App version and installer version are different; reinstall the installer periodically.
- Put the vault on a local disk unless your sync method requires a synced folder; avoid network drives.
- Decide attachments folder, link format, new-note location, and naming convention in the first hour.
- Learn the ten keyboard navigation commands; they are the difference between using Obsidian and living in it.
- Use Workspaces (and later the CLI) to switch between purpose-built layouts.

## Next

[Chapter 3: Markdown and Editing Mastery →](#markdown-and-editing-mastery)

---

# Markdown and Editing Mastery

Obsidian speaks a specific dialect: CommonMark plus GitHub-Flavored Markdown extensions plus its own additions (wikilinks, embeds, callouts, block IDs, comments, highlights, properties). Knowing the entire dialect — including the odd corners — lets you write faster, produce notes that render the way you intend, and understand why a query or plugin behaves the way it does. This chapter is the complete reference plus the editing techniques that make writing in Obsidian genuinely fast.

## The three views

| View | Shortcut | What it shows | Use it for |
| --- | --- | --- | --- |
| **Live Preview** | default editing mode | Rendered Markdown that turns into raw syntax where your cursor is | 90% of writing |
| **Source mode** | toggle via command *Toggle Live Preview/Source mode* (assign a hotkey) | Raw text, syntax highlighted | Fixing tables, YAML, nested structures, stubborn formatting |
| **Reading view** | ++ctrl+e++ | Fully rendered, read-only; embeds, queries and Bases render fully | Reading, reviewing dashboards, copying rendered text |

!!! tip "Two-pane editing"
    Right-click a tab → *Open linked view* → *Open in reading view* gives you a side-by-side render that follows your scroll. Useful for complex tables and Mermaid.

In Reading view, if nothing is selected, ++ctrl+c++ copies the *full source* of the note (1.10+). Copying from the editor includes HTML formatting on the clipboard (1.12+) so pasting into Google Docs preserves headings and bold.

## Headings and structure

```markdown
# H1 — avoid in body if "Show inline title" is on (the filename is your H1)
## H2 — main sections
### H3 — subsections
#### H4 …up to ###### H6
```

- Headings are link targets: `[[Note#Heading]]`. Renaming a heading does **not** update links to it automatically unless you rename via the Outline pane or the right-click *Rename* on the heading, which does.
- Headings are foldable (Settings → Editor → Fold heading). ++ctrl+up++/++ctrl+down++ fold/unfold at cursor.
- The Outline pane and the *Go to heading* commands (community: Quiet Outline, or the core Outline view) navigate by heading.
- **Note composer** (core) can *extract* a heading's section into a new note and leave a link or embed behind. Since 1.13 it also rewrites links inside the extracted section to be relative to their new home.

## Paragraphs and line breaks

With **Strict line breaks off** (recommended), a single ++enter++ renders as a line break. With it on, you need two trailing spaces, a backslash `\`, or a blank line. Paragraphs are separated by a blank line either way. ++shift+enter++ inserts a hard break `<br>`-equivalent regardless of setting.

## Emphasis and inline formatting

| Syntax | Result | Notes |
| --- | --- | --- |
| `*italic*` or `_italic_` | *italic* | ++ctrl+i++ |
| `**bold**` or `__bold__` | **bold** | ++ctrl+b++ |
| `***bold italic***` | ***bold italic*** | |
| `~~strike~~` | ~~strike~~ | |
| `==highlight==` | ==highlight== | Obsidian-specific; searchable; styled per theme |
| `` `code` `` | `code` | Inline code; ++ctrl+`++ in some themes/plugins |
| `<u>underline</u>` | <u>underline</u> | No Markdown syntax; use HTML |
| `<sup>2</sup>` / `<sub>2</sub>` | superscript / subscript | HTML |
| `<kbd>Ctrl</kbd>` | keyboard key | HTML; themes style it |
| `<mark>text</mark>` | highlight | Alternative to `==` |
| `<span style="color:red">red</span>` | inline colour | Works but is not portable; prefer CSS classes |
| `%%hidden%%` | (nothing) | Obsidian **comment** — invisible in Reading view and Publish; visible in edit modes. Multi-line: `%%` on its own lines. Always exactly two `%`. |

The **formatting menu** (right-click or the mobile toolbar) offers all of these plus tables and lists for when you forget syntax.

## Lists

```markdown
- Unordered with hyphen (preferred), * or +
    - Nested with 4 spaces or a tab (be consistent — Settings → Editor → Indent using tabs)
1. Ordered
2. Numbers auto-renumber in Live Preview
   1. Nested ordered
- [ ] Task
- [x] Completed task
- [-] Cancelled (rendered by many themes; Tasks plugin treats as cancelled)
- [/] In progress (theme-dependent; see custom checkboxes below)
```

Editing power:

- ++tab++ / ++shift+tab++ indent/outdent list items (Smart indent lists on).
- ++alt+up++ / ++alt+down++ **move line up/down** — with a list item, moves the whole item (and its children with the *Outliner* plugin).
- ++ctrl+enter++ on a task toggles its checkbox; ++ctrl+l++ cycles bullet → checkbox → checked.
- ++enter++ on an empty list item ends the list.
- *Toggle bullet list*, *Toggle numbered list* commands convert selected paragraphs.
- The **Outliner** community plugin adds workflowy-style behaviours (drag-reorder, fold, select whole subtree); **Zoom** focuses on a single subtree.

**Custom checkbox statuses.** `- [?]`, `- [!]`, `- [>]`, `- [<]`, `- [i]`, `- [*]`, `- ["]`, `- [l]`, `- [b]`, `- [S]`, `- [I]`, `- [p]`, `- [c]`, `- [f]`, `- [k]`, `- [w]`, `- [u]`, `- [d]` are all just characters in brackets. Themes like Minimal and AnuPpuccin style many of them (question, important, forwarded, scheduled, info, star, quote, location, bookmark, savings, idea, pros, cons, fire, key, win, up, down). The Tasks plugin can map each to a status type (Todo / In Progress / Done / Cancelled / Non-task). The CLI's `tasks status="?"` filters by them.

## Tables

```markdown
| Column | Aligned right | Centered |
| --- | ---: | :---: |
| Cell | 12.50 | yes |
| Pipe in cell needs escaping \| like this | | |
```

- Live Preview has a table editor: click a cell to edit; ++tab++ moves right; ++enter++ moves down; right-click a cell for insert/delete row/column, align, move. The formatting menu → *Insert table* creates one.
- Inside a cell, `\|` is a literal pipe; `<br>` is a line break.
- Links inside tables work, including embeds (they render small).
- The **Advanced Tables** plugin adds spreadsheet-like formulas (`<!-- TBLFM: @>$3=sum(@I..@-1) -->`), auto-formatting, Excel-style navigation. Since core table editing improved, Advanced Tables is mainly for formulas and CSV import/export.
- Large data tables belong in Bases, not Markdown tables (Chapter 10). Markdown tables are for small, hand-written matrices.

## Blockquotes and callouts

```markdown
> Quote line
> — Attribution
```

**Callouts** are Obsidian's boxed, coloured, optionally collapsible blocks:

```markdown
> [!note] Optional title
> Body. Supports **Markdown**, [[links]], lists, code, nested callouts.

> [!tip]- Collapsed by default (minus sign)
> Hidden until clicked.

> [!warning]+ Expanded by default but collapsible (plus sign)
> Content.

> [!custom-type] Unknown types fall back to "note" styling and can be styled with CSS
```

Built-in types and aliases: `note`, `abstract`/`summary`/`tldr`, `info`, `todo`, `tip`/`hint`/`important`, `success`/`check`/`done`, `question`/`help`/`faq`, `warning`/`caution`/`attention`, `failure`/`fail`/`missing`, `danger`/`error`, `bug`, `example`, `quote`/`cite`.

Custom callouts via CSS snippet (note the **1.13 change**: `--callout-color` now takes a full CSS colour, not an RGB triplet):

```css
.callout[data-callout="decision"] {
  --callout-color: #7c3aed;
  --callout-icon: lucide-gavel;
}
```

Callouts are the right tool for: summaries at the top of long notes, decision records, warnings inside procedures, foldable "details" sections, and dashboard sections (embed a Dataview query inside a callout). Do not use them as your only structure — headings remain the navigable unit.

## Code

````markdown
Inline `code`.

```python
def hello():
    print("fenced code block with language for syntax highlighting")
```

~~~
Tildes also fence.
~~~
````

- Language identifiers follow Prism.js names: `js`, `ts`, `python`, `bash`/`sh`, `yaml`, `json`, `css`, `html`, `sql`, `rust`, `go`, `java`, `c`, `cpp`, `csharp`, `powershell`, `markdown`, `latex`, `mermaid`, `dataview`, `dataviewjs`, `tasks`, `base`, `query` (embedded search), `meta-bind`, `button`, etc. Plugins register their own.
- Code blocks show a **Copy** button on hover in Reading view.
- Indented code (4 spaces) also works but is fragile in lists.
- To show a triple-backtick block *inside* Markdown (like this guide does), fence the outer block with four backticks or tildes.
- Line numbers in code: not native; the *Code Styler* plugin adds numbering, titles, folding, and highlighting lines.

## Links, embeds and block references

Covered in depth in Chapter 4; the syntax summary:

```markdown
[[Note]]                      wikilink
[[Note|Display text]]         alias display
[[Note#Heading]]              heading link
[[Note#Heading#Subheading]]   nested heading path
[[Note#^blockid]]             block link
[[#Heading]]                  heading in the current note
[Display](Note.md)            markdown link (URL-encode spaces as %20)
[Display](<Note with spaces.md>)  angle brackets avoid encoding
[Display](https://example.com)    external link
<https://example.com>         autolink
![[Note]]                     embed whole note
![[Note#Heading]]             embed a section
![[Note#^blockid]]            embed a block
![[image.png]]                embed image
![[image.png|300]]            image width 300px
![[image.png|300x200]]        width x height
![[document.pdf#page=5]]      PDF at page 5
![[document.pdf#height=600]]  PDF viewer height
![[audio.mp3]]  ![[video.mp4]]  media players
![[Drawing.canvas]]           embed a canvas
![[Tracker.base]]             embed a base
![[Tracker.base#ViewName]]    embed a specific base view
![Alt](https://example.com/img.png)   external image
![200](https://example.com/img.png)   external image sized (1.13+, Reading view)
```

Block IDs: type `^` followed by an identifier at the end of any paragraph/list item/table/callout: `Some paragraph. ^my-id`. Obsidian generates random ones (`^a1b2c3`) when you type `[[Note#^` and choose a block. IDs must be letters, numbers and hyphens.

## Footnotes

```markdown
Claim that needs a source.[^1] Inline footnote.^[This is written inline.]

[^1]: The footnote text. Can be multiple paragraphs if indented.
```

Footnotes render as superscripts with hover preview and a list at the bottom of Reading view. The **Footnotes view** core plugin (2025) shows them in a sidebar. Named footnotes `[^smith2020]` are fine.

## Math

```markdown
Inline: $E = mc^2$

Block:
$$
\int_0^\infty e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}
$$
```

MathJax 3. Most LaTeX math works; `\begin{aligned}`, `\begin{cases}`, matrices, `\text{}`. Currency: `$5 and $10` can trigger math — write `\$5` or enable *Auto pair Markdown syntax* awareness; the **Latex Suite** plugin adds snippets and autocompletion for heavy users.

## Diagrams: Mermaid

````markdown
```mermaid
flowchart LR
    A[Capture] --> B[Process] --> C[Organize] --> D[Review]
```
````

Supported: flowchart, sequenceDiagram, classDiagram, stateDiagram, erDiagram, gantt, pie, gitGraph, mindmap, timeline, quadrantChart, xychart-beta, sankey-beta, C4. Mermaid version 11.13 as of Obsidian 1.13. Obsidian 1.13 shows a one-time banner asking to confirm rendering Mermaid in a vault (a security measure). Internal links inside Mermaid nodes work via `click A "obsidian://open?file=Note"` with a URI, or with the `class A internal-link` trick:

````markdown
```mermaid
flowchart LR
    A[Project Alpha] --> B[Weekly Review]
    class A,B internal-link
```
````

(The node text must equal the note name.)

## HTML

Obsidian renders a safe subset of inline HTML: `<div>`, `<span>`, `<br>`, `<details><summary>`, `<img>`, `<iframe>` (with restrictions), `<table>`, `<kbd>`, `<sup>`, `<sub>`, `<u>`, `<center>` (deprecated but works), `<font>`, `<mark>`, `<abbr title="">`. Scripts are stripped. Markdown *inside* HTML blocks is not rendered unless the block is simple inline HTML on a single line.

`<iframe src="https://…">` embeds web pages (YouTube, maps, Google Docs). Obsidian 1.10 fixed YouTube "Error 153" embeds. The Web viewer core plugin is usually better for browsing.

## Escaping

Backslash escapes any Markdown character: `\*not italic\*`, `\[\[not a link\]\]`, `\#not-a-tag`, `\|`, `\$`. Inside code spans nothing needs escaping. To show `[[wikilink]]` literally in prose, use a code span or escape the first bracket.

## Properties (frontmatter) syntax essentials

Full treatment in Chapter 5. Syntax reminders that trip people:

```yaml
---
title: "Colons: need quotes if the value contains a colon"
aliases:
  - Alias One
  - Alias Two
tags: [one, two/nested]         # or a bulleted list; no leading #
date: 2026-09-06                # date type
created: 2026-09-06T14:30:00    # datetime type
rating: 4                       # number
done: false                     # checkbox
author: "[[Cal Newport]]"       # link — MUST be quoted
related:
  - "[[Note A]]"
  - "[[Note B]]"
url: https://example.com
description: >-
  Multi-line folded text
  continues here.
cssclasses: [wide, no-inline-title]
---
```

- Frontmatter must start on line 1 with `---` and end with `---`.
- Wikilinks in YAML must be quoted or YAML sees a list.
- Since 1.13, text and list properties render Markdown links.
- Duplicate values in list properties are allowed (1.10+).

## Editing techniques that compound

### Selection and multi-cursor

- ++alt++ + click adds a cursor. ++ctrl+d++ (in many setups) or the *Add next occurrence* command via CodeMirror… Obsidian's built-in: ++alt+click++ for extra cursors; ++ctrl+shift+l++ style "select all occurrences" is not native — use *Find and replace* (++ctrl+h++) or the **Multi-cursor** behaviours from plugins like *Code Editor Shortcuts* (adds duplicate line, select word, expand selection, join lines, transform case, etc.).
- ++shift+alt+up++ / ++down++ **duplicate line** — with Code Editor Shortcuts.
- ++ctrl+shift+k++ delete line (plugin) — native is *Delete paragraph*.
- Double-click selects a word; triple-click a paragraph.
- ++ctrl+a++ selects all; inside an embedded Base cell (1.13) it now selects the cell text.

### Find and replace

- ++ctrl+f++ in-note find with match highlighting; ++ctrl+h++ find & replace within the note; supports regex (toggle in the panel).
- Vault-wide search & replace: not native. Use the **Regex Find/Replace** plugin, or VS Code / `sed` on the vault folder (safe because files are plain text — close Obsidian or let it reindex).

### Moving and restructuring

- ++alt+up++/++alt+down++ move line. *Swap line up/down* commands.
- **Note composer**: *Extract current selection* (to a new note, leaving a link), *Merge entire file with…* (append/prepend another note and redirect links). Configure whether it leaves a link, an embed, or nothing.
- **Note Refactor** plugin: extract by heading in bulk, with templates for the new note.
- Drag headings in the **Outline** pane to reorder sections (Outline supports drag-and-drop reordering).
- Drag a file from the explorer into the editor to insert a link; hold ++alt++ (mac: ++shift++?) to insert an embed — behaviour is platform-dependent; alternatively type `![[`.
- Drag text out to another pane to move it.

### Paste behaviours

- Pasting HTML converts to Markdown (setting). ++ctrl+shift+v++ pastes as plain text.
- Pasting an image from the clipboard saves it to the attachments folder as `Pasted image YYYYMMDDHHMMSS.png` and inserts an embed. Rename immediately (right-click → Rename) or use the **Paste image rename** or **Attachment Management** plugins to auto-name by note title.
- Pasting a URL onto selected text makes a Markdown link (with the *Paste URL into selection* plugin; native as of recent versions when text is selected).
- Since 1.13, dragging a folder into the app imports it preserving structure.

### Images

- Resize in Live Preview by dragging the corner (1.12); double-click the corner to reset.
- Select an image with keyboard (1.13); ++plus++/++minus++ resize, ++0++ reset, ++enter++ edit, ++tab++ edit size, ++del++ removes.
- Click or the Zoom button opens the **full-screen viewer** (1.13), navigable between all images in the note; drag to pan; swipe down to dismiss on mobile.
- Right-click → *Copy image* (1.12).
- `![[image.png|200]]` sizes by width. Alignment: not native — use `cssclasses` or the *Image Converter* plugin.

### Slash commands and autocompletion

- The **Slash commands** core plugin: type `/` at line start to search commands inline. Set a trigger character you rarely type.
- `[[` autocompletes notes and aliases; `[[Note#` headings; `[[Note#^` blocks; `#` tags; `[!` callout types; `:emoji:` with the *Emoji Shortcodes* plugin; property names when editing YAML.
- **Various Complements** adds word/phrase autocompletion from your vault and custom dictionaries.
- **Templater** commands run on trigger (Chapter 11).

### Vim mode

Turn on in Settings → Editor. Coverage: normal/insert/visual/visual-line, `:` Ex commands (`:w`, `:noh`, `:s`, `:%s`, `:image grow|shrink|reset` in 1.13 for images with counts), motions, text objects, registers, marks, `.` repeat, search `/`, macros. Missing: some plugins' UI ignore Vim; folding commands differ. The **Vimrc Support** plugin loads a `.obsidian.vimrc` with mappings (`imap jk <Esc>`), `exmap` for Obsidian commands (`exmap back obcommand app:go-back`), and `unmap`. Vim + Obsidian is a legitimate power setup for people who already think in Vim; everyone else should skip it.

### Focus and typewriter modes

- **Toggle sidebars** for focus.
- Community: *Typewriter Scroll* (keeps the cursor line centred, dims other paragraphs), *Focus Mode*, *Stille*.
- *Readable line length* off + zoom for presentation-style reading.

### Word count and reading time

Status bar word count (core Word count plugin) counts the selection when text is selected. *Better Word Count* adds character/sentence/page counts and per-folder totals; *Novel Word Count* shows counts in the file explorer.

## Rendering gotchas worth knowing

- A line starting with `#` followed by a space is a heading; without a space it is a tag. `#1` is not a tag (tags cannot be all-numeric); `#2026-goals` is fine.
- `*` at the start of a line starts a list; to start a paragraph with an asterisk, escape it.
- Numbered lists that start with a number other than 1 render starting from that number.
- Four spaces of indentation on a non-list line creates a code block. This bites when pasting.
- Two callouts in a row need a blank line between them or they merge.
- An embed inside a list item renders with the list indentation (fixed in 1.13).
- `%%%%` is *not* a special comment — comments are exactly two `%` (clarified in 1.13).
- Trailing `\` at end of line forces a line break (CommonMark).
- HTML comments `<!-- -->` are hidden in Reading view but *do* get published/exported; `%% %%` comments do not.

## Key takeaways

- Live Preview for writing, Source for surgery, Reading for consumption; learn the toggles.
- Callouts, block IDs, embeds with sizes, footnotes, math and Mermaid are all part of the core dialect — no plugin needed.
- Keep frontmatter YAML valid: quote wikilinks and colon-containing values.
- Invest in list-manipulation hotkeys, multi-cursor, Note composer, and paste behaviours; those are where minutes per day are saved.
- Know the rendering gotchas so notes render as intended in Obsidian, on Publish, and in other tools.

## Next

[Chapter 4: Links, Backlinks, Graph and Canvas →](#links-backlinks-graph-and-canvas)

---

# Links, Backlinks, Graph and Canvas

Linking is the feature that justifies Obsidian's existence. Everything else — Markdown editing, properties, plugins — exists in other tools. What Obsidian does uniquely well is make the *connections between notes* first-class: cheap to create, automatically bidirectional, navigable, queryable, and visualizable. This chapter covers the full mechanics of links, how to use backlinks as a thinking tool rather than a curiosity, how to make the Graph view actually useful, and how Canvas turns links into spatial thinking.

## Link anatomy

```markdown
[[Target]]
[[Target|Displayed text]]
[[Target#Heading]]
[[Target#Heading|Displayed]]
[[Target#^blockid]]
[[Target#^blockid|Displayed]]
[[Folder/Target]]                (path link — needed when names collide)
[[Target.md]]                    (extension optional for .md; required for other types: [[file.pdf]])
[[#Heading in this note]]
[[##Heading search across vault]]  (typing ## in the [[ suggester searches all headings)
```

### Resolution rules

When you write `[[Target]]` Obsidian looks for a file named `Target.md` (case-insensitive) anywhere in the vault. If there is exactly one, the link resolves. If there are several, the "shortest path" setting decides: Obsidian picks one (the closest) and you probably did not want that — hence the guide's insistence on unique filenames. If there is none, the link is **unresolved**: rendered dimmer, listed in the Graph as a hollow node, and creatable with one click. `obsidian unresolved` (CLI) lists them all.

A link also resolves against **aliases**: if a note has `aliases: [CN]` in properties, `[[CN]]` resolves to it and the suggester shows the alias. Aliased links display the alias text.

### Aliases in depth

```yaml
---
aliases:
  - Cal Newport
  - Newport
  - C. Newport
---
```

Uses: people's nicknames, acronyms (`[[Getting Things Done]]` ↔ `GTD`), singular/plural (`Habit` / `Habits`), translations, old titles after a rename (keep the old name as an alias so `[[Old Name]]` in other tools still resolves). The **Unlinked mentions** pane matches aliases too, so adding aliases retroactively finds more connections.

### Display text and piping

`[[Target|text]]` shows *text*. Common idioms:

- Grammatical fit: `we discussed [[Deep Work|deep work]] yesterday`.
- Hiding folders: `[[People/Jane Doe|Jane]]`.
- Semantic hint: `[[2026-09-06|today's note]]`.

Renaming a note updates the target but keeps your display text. This is why *aliases* are for identity and *display text* is for grammar.

### Heading and block links

Heading links `[[Note#Heading]]` break silently if the heading is renamed by editing the text (Obsidian does not track heading identity). Renaming through the Outline pane's context menu or the heading's right-click *Rename* **does** update links. Nested headings can be pathed `[[Note#H2#H3]]`.

Block links `[[Note#^id]]` are stable across edits because the ID travels with the block. Blocks can be paragraphs, list items, tables, callouts, code blocks, and math blocks. For paragraphs and list items the `^id` goes at the end of the line. For tables, code blocks, callouts and math blocks, put `^id` on its own line directly below the block, separated from it by a blank line. The suggester (`[[Note#^`) searches block text and creates IDs on demand.

!!! tip "Block links as the atomic unit"
    A note is often too coarse to reference. "The third principle in my Values note" is a block. Long-form writers and researchers should get comfortable with `![[Source#^claim-3]]` transclusion — you keep one source of truth and quote it wherever needed.

### Markdown-style links

`[text](Target.md)` and `[text](Target.md#Heading)` are supported and updated on rename. Spaces must be `%20`-encoded or the path wrapped in `<angle brackets>`. Choose Markdown links only if you plan to publish through a tool that does not understand wikilinks (many static-site generators handle both now — Quartz, MkDocs with a plugin, Hugo with a shortcode). Toggle *Use Wikilinks* off to make the suggester insert Markdown links.

### External links and URIs

`[text](https://…)`, bare `https://…` autolinks, and `obsidian://` URIs. Obsidian 1.13 shows a **confirmation dialog** before running any `obsidian://` URI action (choose *Don't ask again* to allow-list it). Links to local files: `[Report](file:///Users/me/report.pdf)` opens in the system app; on 1.12+ a confirmation dialog appears for external apps and a warning for executables.

## Embeds (transclusion)

`![[…]]` renders the target inline and stays live: edit the source, and every embed updates. Embedded notes show a link icon to jump to the source; embedded sections show just that section; embedded blocks show just the block (with its list children for list items).

Design patterns:

- **Single source of truth.** Keep your goals in `Goals.md` and embed `![[Goals#2026]]` into the yearly note, quarterly notes, and weekly template.
- **Dashboards.** A `Home.md` note that is nothing but embeds of Bases, Dataview queries, and sections of other notes.
- **Templates that embed guidance.** A meeting template embeds `![[Meeting Checklist]]` so the checklist lives in one place.
- **Embedded search**: a `query` code block renders live search results:

````markdown
```query
tag:#waiting -path:Archive
```
````

Embed limits: embeds nest but Obsidian stops rendering recursion at a few levels; a note embedding itself shows an error. Embedding a heading includes everything until the next heading of the same or higher level. Embeds do not render inside tables well (small) and do not render in properties.

## Backlinks: the thinking tool

The **Backlinks** core plugin shows, for the current note, every note that links to it (*Linked mentions*) and every note that contains its name or aliases as plain text (*Unlinked mentions*). Configure it in the right sidebar and/or **Backlinks in document** (Settings → Backlinks) which appends a backlinks section at the bottom of every note — excellent for reading-heavy vaults.

Backlinks turn a flat pile of notes into a graph *without you doing anything*. The practical implications:

1. **Write forward, harvest backward.** In your daily note, link liberally to people, projects, and concepts. Weeks later, opening the project note shows every day you touched it. Opening a person's note shows every meeting and mention. You never "filed" anything.
2. **Hub notes get built by their backlinks.** A note titled `Decision Fatigue` may have three paragraphs of your own writing and forty backlinks from books, articles, and journal entries. The backlinks *are* the content. Periodically promote the best backlinked context into the note body (this is what "progressive" Zettelkasten practice looks like in Obsidian).
3. **Unlinked mentions are a to-do list for connection.** Click *Link* next to each unlinked mention to convert plain text into a link. Do this in a weekly review for your most important hub notes.
4. **Backlink context is searchable.** The backlinks pane has a filter box and can sort. In a Base, `file.backlinks` gives the list (expensive — prefer `file.hasLink(this.file)` on the other side). In Dataview, `file.inlinks`.

!!! tip "Backlinks panel tricks"
    *Collapse results* to see just note names. *Show more context* to see the whole paragraph. Right-click the pane → *Open in main area* to give it space. The **Strange New Worlds** plugin shows inline counts of how many notes reference each block/heading right in the editor.

## Outgoing links

The **Outgoing links** core plugin lists links *from* the current note plus its unlinked mentions of other notes' names. Useful during writing to sanity-check that you linked everything relevant, and for finding candidates to link (each unlinked candidate has a Link button).

## Link maintenance

- **Rename** a note (++f2++ in file explorer, or click the inline title) — links update vault-wide if *Automatically update internal links* is on. Prefer renaming inside Obsidian, not in Finder/Explorer.
- **Move** with drag or *Move current file to another folder* — links update (path links) or are unaffected (shortest path).
- **Merge**: Note composer → *Merge entire file with…* redirects links to the surviving note.
- **Delete**: links become unresolved (dim). The CLI's `obsidian unresolved counts verbose` finds them; `orphans` lists notes with no incoming links; `deadends` lists notes with no outgoing links. The Dataview query below does the same inside Obsidian:

```dataview
TABLE length(file.inlinks) AS "Inlinks", length(file.outlinks) AS "Outlinks"
FROM ""
WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0 AND !contains(file.folder, "Templates")
SORT file.mtime DESC
```

- **Janitor** plugin: finds orphans, empty notes, big attachments, and unused attachments for bulk cleanup. Obsidian 1.12's *Automatically delete attachments* prompt handles the common case when deleting a note.

## The Graph view

The global graph (++ctrl+g++ or the ribbon) shows every note as a node and every link as an edge. As shipped it is a hairball. Making it useful takes 10 minutes of configuration and then it becomes a genuine analytical tool.

### Filters

- **Search** field accepts full search syntax: `path:Projects`, `tag:#person`, `-path:Journal`, `file:2026`. Combine with `OR`.
- **Tags** toggle shows tags as nodes (usually off — too many edges).
- **Attachments** off; **Existing files only** on to hide unresolved links (or off to *see* what you keep referring to without creating — a great "notes I should write" finder).
- **Orphans** toggle shows/hides unlinked notes.

### Groups (colours)

Add a group per note type using search queries and pick a colour:

| Query | Colour idea |
| --- | --- |
| `path:Journal` | grey (many, low importance) |
| `tag:#person` or `["type":person]` | orange |
| `["type":project]` | green |
| `path:Sources` | blue |
| `tag:#moc` | purple, and bump node size via display |
| `["status":active]` | bright accent |

Groups evaluate in order; the first match wins. Property-based queries (`["type":project]`) make groups resilient to folder changes.

### Display and forces

Node size: **by link count** so hubs stand out. Arrows on for direction. **Center force** low and **repel force** high to spread clusters. **Link distance** medium. Text fade threshold so labels appear on zoom.

### Local graph

The **local graph** (command *Open local graph*, or the icon in a note's more-options menu) shows the current note's neighbourhood at depth 1–5. Put it in the right sidebar and it follows your active note. Depth 2 with *Incoming/Outgoing* both on is the sweet spot for "what is this idea connected to". It is also the best way to spot a MOC candidate: if the local graph at depth 1 already has 30+ nodes, that note deserves a curated map.

### What the graph is actually for

- **Finding clusters without hubs.** Dense clumps with no large node in the middle are topics you think about but never summarized → create a MOC.
- **Spotting isolated islands.** Groups of notes disconnected from the main body — usually an imported dump or a project that never got linked into Areas.
- **Time-lapse.** The timeline slider at the bottom (with the play button) animates your vault's growth by file creation date; great for annual reviews.
- **Presentation and motivation.** It looks good. That is a legitimate use.

What it is *not* for: navigation. You will not find a note by clicking around a 5,000-node graph. Use search and MOCs.

### Saving graph configurations

Bookmarks (core) can bookmark a *graph view with its settings*. Create one per configuration (Overview, Projects only, People network).

## Canvas

Canvas (core, since 1.1; open `.canvas` JSON format) is an infinite spatial board holding **cards** (freeform text), **notes** (embedded vault notes, live), **media** (images, PDFs, audio), **web pages** (embedded web viewer), and **groups**, connected by labelled arrows. It is where links become *spatial* — position and proximity carry meaning that a list cannot.

### Fundamentals

- Create: right-click in File explorer → New canvas, or the ribbon icon. Double-click empty space to add a card; drag from the bottom toolbar; drag notes in from the explorer.
- ++ctrl+scroll++ zoom, ++space+drag++ or middle mouse to pan; select and ++ctrl+g++ to group; ++alt+drag++ to duplicate; hover a card edge and drag to create an arrow; double-click an arrow to label it.
- Card colours (6 presets + custom hex); groups have labels and colours; **Zoom to selection**, **Zoom to fit**.
- Narrow to a heading: a note card can display only a section via its menu (*Narrow to heading/block*).
- **Convert card to file** turns a scratch card into a real note; the card becomes a note embed.
- Canvas cards are searchable (Search finds text in `.canvas` files); since 1.12 links inside canvases appear as **backlinks** and count in the graph, so a canvas that references `[[Project X]]` shows up in Project X's backlinks.
- Export: *Export as image* (PNG with transparent or themed background). Embedding `![[Board.canvas]]` in a note renders a live, zoomable view.
- Presentation: with cards arranged, use *Canvas: Zoom to next/previous group* — a lightweight slide deck.

### Patterns that work

| Use case | Layout |
| --- | --- |
| **Project planning** | Goal card top-centre; milestone groups left→right; task notes inside groups; arrows for dependencies. |
| **Decision making** | Options as columns; pros/cons as coloured cards; embedded evidence notes; a decision card at the bottom linking to the Decision log. |
| **Literature review / synthesis** | Source notes on the left, claim cards in the middle, thesis on the right; arrows labelled "supports"/"contradicts". |
| **Weekly review board** | Embedded daily notes for the week in a row, a Base of open tasks, a reflection card. Rebuild weekly from a template (Templater can generate canvas JSON). |
| **Life map / Areas** | One group per Area of life with its key notes embedded; this is a *visual MOC* and a good home screen. |
| **Course notes** | Lectures in chronological row; concept cards linked across lectures. |
| **Relationships map** | People notes as nodes; arrows labelled with relationship. Beware of privacy if the vault is synced. |
| **Storyboarding / writing** | Scenes as cards, arcs as groups, characters embedded from notes. |

### Canvas vs Excalidraw vs Graph

- **Canvas**: structured spatial arrangement of *notes*; live embeds; open JSON; searchable and backlinked. Best for planning and synthesis.
- **Excalidraw** (plugin): freehand drawing, diagrams, sketches, whiteboarding, with Obsidian links inside drawings. Best for visual thinking, diagrams, hand-drawn explanations.
- **Graph**: automatic, not editable, analytical.

Many mature vaults use all three: Excalidraw for drawings embedded in notes, Canvas for project boards, Graph for periodic analysis.

### JSON Canvas

The `.canvas` format is documented at jsoncanvas.org: a `nodes` array (type `text`, `file`, `link`, `group`; each with id, x, y, width, height, color) and an `edges` array (fromNode, toNode, fromSide, toSide, label). Because it is plain JSON, scripts can generate canvases — a Templater or Python script that lays out this month's daily notes in a grid, or a project board from a Base query. Other apps (Kinopio, Logseq forks, various web tools) read the format.

## Linking strategy: how much is too much

- Link **nouns you will want to revisit**: people, projects, places, concepts, sources, decisions. Not every word.
- A link to a note that does not exist is a promise; unresolved links accumulate. Either create the note (even one line) or accept that the graph shows the promise. Periodically review unresolved links with high counts — they are notes your vault is asking you to write.
- Prefer **links over tags** for anything that could have content of its own. `#cal-newport` cannot hold a biography; `[[Cal Newport]]` can.
- Use **MOCs** (Chapter 7) when a topic has more than ~15 related notes. The MOC is a curated, ordered, annotated list of links — something backlinks alone cannot provide.
- Add a **`## Related`** section at the bottom of thinking notes for links that do not fit the prose. Keep it short; if it grows, it is a MOC.

## Key takeaways

- Links resolve by filename and alias; keep names unique and use aliases for synonyms, display text for grammar.
- Block references (`^id`) are the stable atomic unit; headings are convenient but fragile when renamed by editing.
- Backlinks are the payoff: write forward, harvest backward, and promote backlink context into hub notes over time.
- Configure the Graph (filters, property-based groups, size by links) and use the local graph at depth 2 as a daily tool; the global graph is for analysis, not navigation.
- Canvas is spatial linking with an open JSON format; use it for planning, decisions, synthesis, and visual maps of your life's areas.

## Next

[Chapter 5: Properties, Tags and Metadata Design →](#properties-tags-and-metadata-design)

---

# Properties, Tags and Metadata Design

Metadata is what turns a folder of notes into a database you can query. In Obsidian that means **properties** (typed YAML frontmatter), **tags**, and to a lesser extent **inline fields** (a Dataview convention). Get the schema right and Bases, Dataview, templates, and dashboards all become trivial. Get it wrong — fifteen synonyms for the same status, tags that should be links, dates as free text — and every query becomes a cleanup job. This chapter covers the mechanics precisely, then gives a decision framework and a concrete schema for a whole-life vault.

## Properties: mechanics

Properties live in YAML frontmatter between `---` fences at the very top of a note. Since Obsidian 1.4 there is a typed editor (Settings → Editor → *Properties in document*: Visible / Source / Hidden); since 1.9 properties are the fuel for Bases; since 1.10 the Properties core plugin is on by default.

### Types

| Type | YAML example | Notes |
| --- | --- | --- |
| **Text** | `title: My note` | Default. Since 1.13, renders Markdown links inside. |
| **List** | `tags: [a, b]` or bulleted list | Each item a text (or link). Duplicates allowed since 1.10. |
| **Number** | `rating: 4.5` | Sortable and summable in Bases. |
| **Checkbox** | `done: true` | `true`/`false`; `null` (indeterminate) sorts with false. |
| **Date** | `date: 2026-09-06` | ISO `YYYY-MM-DD`; date picker in UI. |
| **Date & time** | `created: 2026-09-06T14:30:00` | ISO 8601; timezone offsets parsed since 1.10. |

The **type is per property name, vault-wide** (stored in `.obsidian/types.json`). If `rating` is a number in one note it is a number everywhere. Change a type via the property's icon menu → *Property type*. Since 1.13 the menu makes clear whether a type was inferred or set manually. When Obsidian cannot parse a value as the declared type it shows a warning icon — this is how you find `rating: four`.

### Reserved / special properties

| Property | Effect |
| --- | --- |
| `tags` | Tags (no `#`). `tag` singular also works but do not mix. |
| `aliases` | Alternative names for links and the quick switcher. |
| `cssclasses` | Adds CSS classes to the note's view container for per-note styling (`cssclass` singular is legacy). |
| `publish` | `true`/`false` controls Obsidian Publish inclusion. |
| `permalink` | Custom URL slug on Publish. |
| `description`, `image`, `cover` | Used by Publish for social metadata. |
| `title` | *Not* special in Obsidian (filename is the title) but used by some plugins and publishers. |

### Editing properties

- The property editor: click the value; ++tab++ moves between fields; type a new key name in the empty row; the suggester offers existing keys and values.
- **Add file property** command (assign a hotkey) and **Add property in current file** via the command palette.
- Right-click a key → *Rename* (only this note) or use the **Properties view** (sidebar, core) to see every property in the vault with counts, rename or delete vault-wide (1.10+), and change types. ++backspace++ deletes selected properties in that view (1.13).
- The CLI: `obsidian property:set name=status value=active`, `property:read`, `property:remove`, `properties counts sort=count` — see Chapter 29.
- Templater and QuickAdd write properties at note creation (Chapter 11). Meta Bind renders input widgets bound to properties inside the note body.

### YAML rules that bite

```yaml
---
# Comments are allowed.
title: "Meeting: kickoff"        # colon in value → quote it
author: "[[Jane Doe]]"           # wikilink → MUST quote, or YAML reads a nested list
links:
  - "[[Note A]]"
  - "[[Note B]]"
tags:
  - project/alpha                # no leading #; nested via /
  - meeting
status: active                   # plain word, fine
score: 08                        # leading zero → string, not number! use 8
version: 1.0                     # number; "1.0" would be text
time: 14:30                      # YAML may parse as sexagesimal number → quote "14:30"
yes_field: yes                   # YAML 1.1 turns yes/no/on/off into booleans → quote
empty:                           # null; Bases treats as empty
multiline: |
  Preserved
  line breaks
folded: >-
  Joined into
  one line
---
```

- Frontmatter must begin on **line 1**. A blank line before `---` makes it plain text.
- Indentation is spaces, never tabs.
- Unknown structures (nested objects) are preserved but shown as raw text in the editor; Bases can read them with `note.obj.key`.
- Obsidian rewrites the frontmatter when you edit via UI; it preserves key order but may reformat lists. If exact formatting matters (e.g. for another tool), edit in Source mode.

### Properties vs inline fields

Dataview introduced **inline fields**: `key:: value` anywhere in the body, or `[key:: value]` inline, or `(key:: value)` hidden-key. They are *not* properties: Obsidian core ignores them, Bases cannot see them, and search treats them as text. Use them only for data that genuinely belongs at a specific line (e.g. `- 07:30 wake [mood:: 7]` in a daily log that Dataview will chart). For everything else, use properties.

## Tags: mechanics

- `#tag` in body text or `tags: [tag]` in properties. Both count identically for search, the Tags view, Bases `file.tags`, and Dataview `file.tags`.
- Nested: `#area/health/sleep`. Searching `tag:#area/health` matches children. `file.hasTag("area")` in Bases matches nested tags too.
- Allowed characters: letters, numbers, `_`, `-`, `/`. Cannot be all digits. Case-insensitive for matching but the Tags view shows the first-seen casing — pick one.
- Click a tag to search for it. The **Tags view** (core) lists all tags with counts, nesting, and sort options; drag-and-drop nesting is via the **Tag Wrangler** plugin, which also renames tags vault-wide (core cannot).
- Escape a literal hash with `\#`.
- Tags in `%% comments %%` still count as tags. Tags in code blocks do not.

## The decision framework: folder, tag, property or link?

The most common structural mistake is using the wrong primitive. Use this table.

| Question about the data | Use | Example |
| --- | --- | --- |
| Is it the **kind** of note, with one value, driving templates and dashboards? | **Property `type`** (and usually a folder) | `type: meeting`, `type: person`, `type: book` |
| Does it have a **fixed set of values** you will filter/sort by? | **Property** | `status: active`, `priority: 2`, `rating: 4` |
| Is it a **date or number**? | **Property** (typed) | `due: 2026-10-01`, `cost: 49.99` |
| Could the value **have its own note** with content? | **Link** (in a property if structured, in text if narrative) | `project: "[[Alpha]]"`, `author: "[[Cal Newport]]"` |
| Is it a **cross-cutting, informal label** used for quick filtering across many types? | **Tag** | `#review`, `#idea`, `#favorite`, `#urgent` |
| Is it a **state of the note itself** (workflow) rather than of its subject? | **Tag** or `status` property | `#inbox`, `#to-process`, `#stub` |
| Does it determine **where attachments and templates apply**, or need physical separation? | **Folder** | `Journal/`, `Templates/`, `Attachments/`, `Archive/` |
| Is it a **hierarchy of topics**? | **Links to MOCs**, not nested tags or deep folders | `[[Health MOC]]` ← `[[Sleep MOC]]` |

Rules of thumb:

1. **If you would ever want to write a sentence about it, it is a link, not a tag.** Tags cannot hold content; notes can.
2. **If you would ever sort by it, it is a property.** Tags are booleans; properties have values.
3. **Tags are for verbs and adjectives; links are for nouns.** `#todo`, `#unclear`, `#favorite` vs `[[Berlin]]`, `[[Stoicism]]`.
4. **Folders are for the machine, not for meaning.** Attachments route to them; templates apply per folder; sync/publish exclude them. Beyond ~10 top-level folders you are filing, not thinking.
5. **Prefer one `type` property over one folder per type.** A folder per type *also* works — and Bases can filter by either — but properties survive when you move notes.

## Designing the schema for a whole-life vault

A schema is the list of property names, their types, and their allowed values. Write it down in a note (`Meta/Schema.md`) and keep it current — future you and every template depend on it.

### Universal properties (every note type)

```yaml
type: <note type>          # required; drives everything
created: 2026-09-06        # date; Templater fills
tags: []                   # optional labels
aliases: []                # optional
```

Do **not** add `modified` — `file.mtime` already exists and hand-maintained modified dates are always wrong. Do not add `title` unless a publishing tool needs it.

### Type catalogue

The recommended note types for a whole-life vault, with their extra properties. Every later chapter builds on this list.

| `type` | Extra properties | Folder (suggested) |
| --- | --- | --- |
| `daily` | `date` (date), `mood` (number 1–5), `energy` (number), `sleep_h` (number), `weight` (number, optional), `highlights` (list) | `Journal/Daily` |
| `weekly` / `monthly` / `quarterly` / `yearly` | `period_start`, `period_end` (date) | `Journal/Weekly`… |
| `project` | `status` (idea/active/on-hold/done/dropped), `area` (link), `start`, `due`, `completed` (dates), `priority` (1–3), `goal` (link) | `Projects` |
| `area` | `review_cadence` (weekly/monthly/quarterly), `standard` (text: what "good" looks like) | `Areas` |
| `goal` | `horizon` (year/quarter/life), `status`, `area` (link), `metric` (text), `target` (number), `current` (number), `due` | `Goals` |
| `task-note` (only for tasks big enough to have a page) | `status`, `project` (link), `due` | inside project folder |
| `person` | `relationship` (family/friend/colleague/acquaintance/professional), `birthday` (date), `email`, `phone`, `company` (link), `location`, `last_contact` (date), `contact_every` (number, days), `tags` | `People` |
| `meeting` | `date`, `attendees` (list of links), `project` (link), `decisions` (list), `next_meeting` (date) | `Work/Meetings` |
| `source` (umbrella) with `medium`: `book` / `article` / `paper` / `podcast` / `video` / `course` | `author` (list of links), `url`, `medium`, `status` (to-read/reading/read/abandoned), `rating` (1–5), `started`, `finished` (dates), `pages`, `isbn`/`doi`, `cover` (url), `topics` (list of links) | `Sources/<medium>` |
| `note` (permanent/evergreen idea) | `status` (seedling/budding/evergreen), `topics` (list of links), `sources` (list of links) | `Notes` |
| `moc` | `area` (link) | `Maps` |
| `recipe` | `cuisine`, `course` (breakfast/main/dessert…), `servings` (number), `prep_min`, `cook_min` (numbers), `rating`, `ingredients` (list), `last_made` (date), `tags` | `Life/Recipes` |
| `workout` | `date`, `kind` (strength/run/bike/swim/yoga…), `duration_min`, `distance_km`, `calories`, `rpe` (1–10), `exercises` (in body as table) | `Health/Workouts` |
| `health-event` | `date`, `kind` (symptom/appointment/medication/lab), `provider` (link), `severity` | `Health/Log` |
| `transaction` or `expense` | `date`, `amount` (number), `currency`, `category`, `account` (link), `merchant`, `recurring` (checkbox) | `Finance/Transactions` (or a single ledger note with inline table) |
| `subscription` | `cost`, `billing` (monthly/yearly), `renews` (date), `status`, `cancel_url` | `Finance/Subscriptions` |
| `asset` / `item` | `purchased` (date), `price`, `warranty_until` (date), `serial`, `location`, `manual` (link/url) | `Life/Inventory` |
| `trip` | `destination`, `start`, `end`, `status` (idea/planned/booked/done), `budget`, `companions` (links) | `Life/Travel` |
| `decision` | `date`, `status` (open/decided/reviewed), `options` (list), `chosen` (text), `review_on` (date), `confidence` (1–10) | `Mind/Decisions` |
| `habit` | `cadence` (daily/weekly), `active` (checkbox), `start` (date), `why` (text) | `Life/Habits` |
| `template` | none (excluded folder) | `Templates` |

You will not use all of these. Start with `daily`, `project`, `area`, `person`, `source`, `note`, `meeting`, and add as domains come online.

### Controlled vocabularies

For every property whose value is a category, decide the allowed values and write them in the schema note. The property editor's value suggester shows existing values, which nudges consistency, but it does not enforce. Options for enforcement:

- **Templates** pre-fill the property with a default so you rarely type it.
- **Meta Bind** renders a dropdown (`INPUT[inlineSelect(option(active), option(done)):status]`) bound to the property.
- **Linter** plugin can normalize casing and order of properties on save.
- **Bases** views with `status != "active" && status != "done" && …` filter surface typos.
- A periodic **schema audit** query (below).

```dataview
TABLE WITHOUT ID status, length(rows) AS "count"
FROM ""
WHERE type = "project"
GROUP BY status
```

Any row with an unexpected `status` value is a typo to fix.

### Naming properties

- `snake_case` or `kebab-case`? Either; Bases and Dataview accept both, but Dataview *also* auto-generates a sanitized alias (`sleep-hours` → `sleep-hours` and `sleephours`), and Bases requires `note["sleep-hours"]` bracket syntax for hyphens in some contexts. **`snake_case` avoids all of it.** Lowercase always.
- Singular for single values (`author`), plural for lists (`topics`, `attendees`).
- Dates end in a noun that says what they are: `due`, `start`, `finished`, `renews`, `last_contact`. Avoid a bare `date` except on notes that *are* a date (daily notes, meetings, transactions).
- Prefer a `type` property over multiple boolean properties (`is_project: true`).

### Migrating and refactoring metadata

- Rename a property everywhere: **Properties view** → right-click → Rename. Or the CLI/scripting. Or a careful `sed` across the vault while Obsidian is closed.
- Convert tags to a property: search `tag:#book`, then for each file add `type: book` — tedious by hand; Templater/QuickAdd macros, the **Metadata Menu** plugin (bulk field editing), or a short Python script over the folder do it in minutes.
- Merge synonyms (`status: doing` → `active`): Dataview query to list offenders, fix in Bases table view by editing cells inline (Bases table cells are editable and support copy/paste and undo since 1.10 — select a column of wrong values, paste the right one).

## Bases and Dataview see the same data

Both read frontmatter. Differences that matter for schema design:

| | Bases | Dataview |
| --- | --- | --- |
| Reads properties | yes | yes |
| Reads inline fields `key:: value` | no | yes |
| Reads tasks | no (only via plugins' views) | yes (`TASK` queries) |
| Edits values in place | yes (table cells) | no (read-only; DataviewJS can write via API) |
| Lists inside properties | `list.contains()`, `map`, `filter` | `contains()`, `map`, `filter` |
| Links in properties | Link objects; `author == this`, `authors.contains(this)` | Link objects; `contains(author, this.file.link)` |

Design for the intersection: typed properties, links quoted, lists for multi-values, nothing important in inline fields.

## Metadata hygiene routine

Monthly, 15 minutes:

1. Open the **Properties view**; scan for near-duplicates (`Status` vs `status`, `tag` vs `tags`); rename or delete.
2. Run the schema audit query per major type; fix stray values inline in a Base table.
3. Check for notes missing `type` (`WHERE !type` in Dataview, or a Base filter `type.isEmpty()`), and fix or archive.
4. Check the Tags view for tags used once — convert to a link, a property value, or delete.

## Key takeaways

- Properties are typed, vault-wide by name, and the substrate for Bases, Dataview, templates and dashboards; keep the YAML valid (quote links and colons).
- Tags are booleans for adjectives and workflow states; links are for nouns; properties are for anything you sort or filter; folders are for the machine.
- Write down a schema — a `type` property on every note plus a small, controlled set of typed properties per type — and enforce it with templates, Bases views and a monthly audit.
- Use `snake_case`, plural names for lists, and meaningful date names.
- Design for the intersection of Bases and Dataview: properties, not inline fields.

## Next

[Chapter 6: Search Mastery →](#search-mastery)

---

# Search Mastery

Obsidian's search is far more capable than the box suggests. It has a full operator language, regular expressions, property queries, block and section scoping, and it can be embedded live inside notes. Combined with the Quick switcher, Omnisearch, and the CLI, retrieval in a 10,000-note vault takes seconds — if you know the syntax. This chapter is the complete reference plus the workflows built on it.

## Where search happens

| Tool | Scope | Opens with |
| --- | --- | --- |
| **Search** (core, left sidebar) | Full text of all files, with operators | ++ctrl+shift+f++ |
| **Quick switcher** | Filenames, aliases (fuzzy); headings with `#`; not content | ++ctrl+o++ |
| **In-note find** | Current note only | ++ctrl+f++ (replace: ++ctrl+h++) |
| **Command palette** | Commands | ++ctrl+p++ |
| **Settings search** (1.13) | Settings by name/description | ++ctrl+comma++ then type |
| **Bookmarks search** (1.13) | Your bookmarks | Bookmarks pane filter |
| **Bases search toolbar** (1.12) | Rows of the current base | Magnifier in the base toolbar |
| **Omnisearch** (plugin) | Full text with BM25 ranking, typo tolerance, PDF/image OCR | its own hotkey |
| **Obsidian CLI** | `obsidian search query="…"`, `search:context` for grep-style output | terminal |

## Search operators (core)

Terms are ANDed by default; matching is case-insensitive unless you toggle the `Aa` (match case) button in the search pane — case sensitivity is a toggle, not an operator. Quoted phrases match exactly.

| Syntax | Meaning | Example |
| --- | --- | --- |
| `word` | contains word | `retrospective` |
| `"exact phrase"` | phrase match | `"weekly review"` |
| `a b` | both (AND) | `budget 2026` |
| `a OR b` | either | `sleep OR insomnia` |
| `-a` | not | `meeting -cancelled` |
| `(a OR b) c` | grouping | `(run OR bike) -rest` |
| `file:` | filename contains | `file:2026-09` |
| `path:` | path contains (folders) | `path:Projects/Alpha` |
| `content:` | body only (excludes filename/path/props) | `content:"open question"` |
| `tag:` | tag (nested included) | `tag:#person` or `tag:person` |
| `line:(a b)` | both terms on the same line | `line:(decision approved)` |
| `block:(a b)` | both in the same block (paragraph/list item) | `block:(TODO urgent)` |
| `section:(a b)` | both under the same heading | `section:(Risks mitigations)` |
| `task:` | inside any task | `task:call` |
| `task-todo:` | inside an unchecked task | `task-todo:invoice` |
| `task-done:` | inside a checked task | `task-done:invoice` |
| `[property]` | note has property | `[due]` |
| `[property:value]` | property equals/contains value | `[status:active]`, `["type":book]` |
| `/regex/` | regular expression (JS flavour) | `/\b20\d\d-\d\d-\d\d\b/` |

Notes on property search:

- Quote keys with spaces or special characters: `["sleep hours":7]`.
- Matching is substring for text (`[author:Newport]` matches `Cal Newport`), exact for numbers/booleans.
- Lists: `[tags:reading]` matches any element. `[attendees:"[[Jane Doe]]"]` matches a link — quote the brackets.
- Presence: `[due]`; absence: `-[due]`.
- Property search cannot do ranges (`due > today`). Use Bases or Dataview for that.

Regex specifics: JavaScript regex; forward slashes inside must be escaped `\/`; `\d`, `\w`, `\b`, lookaheads work; multi-line matching is per line. Regex can combine with operators: `path:Journal /\[mood:: [1-3]\]/` finds low-mood days recorded as inline fields.

## Search pane features

- **Match case** (`Aa`), **Explain search term** (shows how the query parsed — use it when results surprise you), **Collapse results**, **Show more context**, and **Sort** (file name, modified time, created time — each ascending or descending).
- **Copy search results** (the `…` menu) copies results as a Markdown list of links, optionally with context — instant MOC or reading list.
- Results show heading and block context; click a match to open at that line.
- **Search history**: press ++down++ in an empty search box.
- Drag the search view into the main area for a wide, persistent results list.
- `path:` defaults to substring; anchor to the root with the folder name at the start — there is no `^` anchor for paths, so avoid folder names that are substrings of others (`Notes` and `Meeting Notes`).

## Embedded (live) searches

A `query` code block renders results inside a note, updating live:

````markdown
```query
tag:#waiting -path:Archive
```
````

Where embedded search beats Dataview/Bases: full-text matches (Bases/Dataview only see metadata and tasks), phrase and regex hunts, and "find every mention of X" widgets on a person or project note:

````markdown
## Mentions elsewhere
```query
"Project Alpha" -file:"Project Alpha" -path:Templates
```
````

Limits: no sorting or column control, results are a match list, and each block re-runs when visible (fine for a handful per note).

## Saved searches and bookmarks

Bookmark a search: run it, then in the Bookmarks pane choose *Bookmark current search*, or drag the search into the Bookmarks view. Bookmarks can be grouped in folders; since 1.13 the Bookmarks pane has its own search. Build a "Saved searches" bookmark group: `Inbox to process`, `Waiting for`, `Stubs (<50 words)`, `Untyped notes`, `Recent decisions`.

## Quick switcher tricks

- Fuzzy across filename **and aliases**; results ordered by recency and match quality.
- Type text and press ++shift+enter++ to **create** a note with that name even if a similar note exists; ++ctrl+enter++ opens in a new tab; ++ctrl+alt+enter++ in a new split.
- `#heading` searches headings across the vault (in the `[[` link suggester too).
- Since 1.12 you can drag a result out of the switcher into the editor (insert link) or a pane.
- **Quick Switcher++** (plugin) adds modes: `@` symbols in current note, `/` related items, `:` commands, `#` headings, `+` starred/bookmarks, and editor-tab switching.
- The default switcher ignores excluded folders (Settings → Files and links → Excluded files) — the right place to hide `Templates/` and `Attachments/` from your `[[` suggestions.

## Omnisearch (plugin) — when to add it

Core search is exact-token; Omnisearch is a ranked engine (BM25 via MiniSearch) with prefix and fuzzy matching, weighting of title/headings/tags, PDF text extraction, image OCR (via Text Extractor), and a "vault-wide" and "in-file" mode. It excels at "I remember roughly what it said" queries and typos. It does **not** replace core search for operators, regex, or property queries — keep both. Enable *Ignore diacritics* and set *Weight of headings* higher if you write structured notes.

## Search-driven workflows

**Inbox processing.** Saved search `path:Inbox`; open each result, decide (link, type, move), done when the search is empty.

**Weekly review sweep.** Saved searches: `task-todo:` inside `path:Journal` for stray tasks in daily notes; `[status:waiting]`; `tag:#followup`; `/\?\?/` for open questions you marked with `??`.

**Retroactive linking.** Search a note's title as a phrase (`"Cal Newport" -file:"Cal Newport"`) to see mentions, then use the Backlinks pane's unlinked mentions to convert them. The **Various Complements** or **Auto Link** plugins can automate.

**Content audit.** `-[type] -path:Templates -path:Journal` finds notes missing a `type`; `/^\s*$/` inside a `file:` scope finds empties; the *Novel word count* plugin plus `sort by size` finds stubs.

**Date hunts.** `/\b2026-09-\d\d\b/ -path:Journal` finds every September date mention outside the journal — a way to reconstruct a timeline.

**Task archaeology.** `task-done:` with `path:Journal/Daily` and a `"Project Alpha"` term shows every completed task that mentioned the project across all daily notes.

## Search vs Bases vs Dataview: choosing

| Need | Tool |
| --- | --- |
| Find text/phrases/regex anywhere | **Search** |
| Table of notes filtered/sorted by properties, editable | **Bases** |
| Table with computed columns, group by, inline fields, tasks | **Dataview** (or Bases formulas for property-only cases) |
| List of tasks across notes with due dates | **Tasks plugin** queries |
| "Which notes mention X" widget on a note | Embedded **Search** or Backlinks |
| Fuzzy / typo-tolerant discovery | **Omnisearch** |
| Scripted/batch queries from the terminal | **CLI** `search`, `search:context`, `base:query` |

## Key takeaways

- Learn the operator set — `path:`, `file:`, `tag:`, `line:`/`block:`/`section:`, `task-todo:`, `[prop:value]`, `/regex/` — and use *Explain search term* when results surprise you.
- Embedded `query` blocks give live, full-text widgets that Bases and Dataview cannot.
- Bookmark your recurring searches; they are the backbone of inbox processing and weekly review.
- Quick switcher is for names and aliases; Omnisearch adds ranked fuzzy discovery; the CLI adds scripting. Keep core search for precision.

## Next

[Chapter 7: PKM Methodologies Compared →](#pkm-methodologies-compared)

---

# PKM Methodologies Compared

Every popular knowledge-management method — Zettelkasten, PARA, LYT, GTD, Johnny.Decimal, Building a Second Brain — was designed for a specific problem and a specific kind of person. Adopting one wholesale usually means adopting its blind spots too. This chapter explains each method faithfully, shows exactly how it maps onto Obsidian primitives, states what it is good and bad at, and then assembles a hybrid that works for someone who wants to run *all* of life in one vault. Chapter 8 turns that hybrid into a concrete folder tree and templates.

## The problems the methods solve

Before the methods, the problems. Any system for a whole life must handle five distinct jobs:

1. **Capture** — get things out of your head and off the web with minimal friction.
2. **Action** — track commitments (tasks, projects, goals) and surface the right ones at the right time.
3. **Reference** — store and retrieve facts, documents, and records.
4. **Knowledge** — develop understanding: read, connect, write, revisit.
5. **Reflection** — journal, review, and course-correct.

| Method | Capture | Action | Reference | Knowledge | Reflection |
| --- | :-: | :-: | :-: | :-: | :-: |
| Zettelkasten | ○ | – | – | ●●● | ○ |
| Evergreen notes | ○ | – | – | ●●● | ○ |
| LYT / MOCs | ○ | ○ | ● | ●●● | ○ |
| PARA | ● | ●● | ●●● | ○ | ○ |
| CODE / Second Brain | ●●● | ● | ●● | ●● | ○ |
| GTD | ●●● | ●●● | ● | – | ●● |
| Johnny.Decimal | – | – | ●●● | – | – |
| Bullet Journal / Daily notes | ●● | ●● | – | ○ | ●●● |
| Periodic reviews (weekly/quarterly/annual) | – | ●● | – | ○ | ●●● |

No single method covers the row. That is the argument for a hybrid.

## Zettelkasten

**Origin.** Niklas Luhmann's slip-box: ~90,000 index cards, each one idea, each numbered so that it could be placed *next to* related cards (branching IDs like `21/3a7`), each linking to others by number. Popularized for digital use by Sönke Ahrens' *How to Take Smart Notes*.

**Core rules.**

- **Atomicity**: one idea per note, so it can be linked from many contexts.
- **Own words**: rewrite, never copy — the rewriting *is* the thinking.
- **Link with reasons**: every link says *why* it connects ("contradicts", "generalizes", "example of").
- **Note types**: *fleeting* (scratch, discard within days), *literature* (what a source says, with page refs), *permanent* (your ideas, written for your future self), plus *structure/hub notes* (entry points).
- **No categories up front**: structure emerges from links.

**In Obsidian.** Permanent notes live in one flat folder (`Notes/`), titled as *claims* rather than topics (`Attention is the scarce resource, not time` rather than `Attention`). Links carry context in the sentence around them. Fleeting notes go to daily notes or `Inbox/`. Literature notes live with their source. Structure notes are MOCs. Unique IDs (`202609061430`) via the **Unique note creator** core plugin are *optional* — Obsidian resolves links by title, so IDs mainly help when titles change often or when you want chronology in the filename. Most Obsidian users drop the numeric IDs and keep the rest.

**Strengths.** Unmatched for generating original thinking over years; scales because atomic notes stay relevant; forces understanding.

**Weaknesses.** Useless for tasks, records, and admin. Overhead is real — proper permanent notes take 10–30 minutes each. Purists' insistence on IDs and folder-less-ness confuses newcomers. Many people build a Zettelkasten and never *use* it because there is no output driving the input.

**Verdict.** Adopt the *note-making discipline* (atomic, own words, linked with reasons, claim-titles) for the knowledge job. Ignore the rest.

## Evergreen notes (Andy Matuschak)

A modern restatement of Zettelkasten principles for digital tools: notes should be *atomic*, *concept-oriented* (about concepts, not sources or projects), *densely linked*, and *evergreen* — revised over time rather than written once. Matuschak adds "prefer associative ontologies to hierarchical taxonomies" and "write notes for yourself by default, disregarding audience". He also popularized the *stacked panes* reading interface that Obsidian's Stack tabs reproduces.

**In Obsidian.** Same as Zettelkasten in practice. The practical addition is a `status` property on idea notes — `seedling` → `budding` → `evergreen` — which lets a Base show you which ideas to develop next. Stack tabs for exploration.

**Verdict.** The best short articulation of *how to write* notes that stay valuable. Read Matuschak's public notes on the subject once; they are the manual.

## LYT — Linking Your Thinking (Nick Milo)

**Core idea.** Networks of notes need *navigational* structures that are not folders: **Maps of Content (MOCs)** — notes that curate links to other notes, with commentary, in a deliberate order. MOCs are created *when the pressure of related notes demands it* ("mental squeeze point"), not in advance. A **Home note** sits at the top; MOCs link down to notes and up to Home; notes link laterally. The **ACCESS** folder scheme (Atlas, Calendar, Cards, Extras, Sources, Spaces) is Milo's suggested skeleton: *Atlas* for maps, *Calendar* for time-based notes, *Cards* for ideas, *Extras* for templates and attachments, *Sources* for external material, *Spaces* for areas/projects/efforts. LYT also emphasizes "fluid frameworks" — structure that can be reorganized cheaply because it is made of links.

**In Obsidian.** MOCs are ordinary notes with `type: moc`. A `Home.md` with links to top-level MOCs (and, in a modern vault, embedded Bases for tasks and projects). The local graph and backlinks find MOC candidates. Nothing is prescribed about properties or tasks.

**Strengths.** The single most useful structural idea for an Obsidian vault after links themselves. MOCs make big vaults navigable without deep folders. ACCESS is a sane, shallow folder skeleton.

**Weaknesses.** Thin on action management and records; MOCs need periodic gardening or they rot; "fluid" can become "never decided".

**Verdict.** Adopt MOCs completely. Use ACCESS or a close variant as the top-level folder skeleton (Chapter 8 does).

## PARA — Projects, Areas, Resources, Archive (Tiago Forte)

**Core idea.** Organize *everything* — notes, files, tasks — into four buckets by **actionability**: **Projects** (goal with a deadline), **Areas** (standards to maintain indefinitely: Health, Finances, Career), **Resources** (topics of interest), **Archive** (inactive items from the other three). The same four folders appear in every tool you use. Items move between buckets as their status changes — a Resource becomes a Project when you commit to doing something with it.

**In Obsidian.** Four top-level folders, or a `type` property with those values, or both. PARA maps nicely onto the `project`/`area` note types with `status` and `area` links from Chapter 5. "Move to Archive" is a status change (`status: done`) plus, optionally, a folder move; a Base view with `status != "done"` makes the folder move unnecessary.

**Strengths.** Dead simple; the Project/Area distinction is genuinely clarifying ("is this something I finish, or something I maintain?"); it forces you to *have* a project list, which is where most productivity failures start.

**Weaknesses.** Designed around folders and moving things, which fights Obsidian's link-centric nature — a note about *Sleep* is a Resource, an Area (Health), and relevant to a Project (Fix insomnia) all at once. "Resources" becomes a landfill. Nothing about how to write notes or think.

**Verdict.** Adopt the *vocabulary* and the Projects/Areas split as note types and dashboards. Do not literally move files between four folders; use `status` and links instead.

## CODE / Building a Second Brain (Tiago Forte)

**Core idea.** The workflow layer over PARA: **Capture** (only what resonates), **Organize** (by actionability — PARA), **Distill** (progressive summarization: bold the key passages, then highlight the best of the bold, then write an executive summary at the top — layers you add *on revisit*, not at capture), **Express** (produce output; "intermediate packets" — reusable chunks of past work).

**In Obsidian.** Capture via Web Clipper, mobile share sheet, daily note. Distill with `**bold**` and `==highlight==` layers plus a `> [!summary]` callout at the top of source notes. Express via writing notes that embed blocks (`![[Source#^key-claim]]`) from distilled sources.

**Strengths.** Progressive summarization is a practical, low-guilt way to process the firehose — you invest in a note only when you return to it, so attention follows actual use. "Intermediate packets" reframes notes as reusable assets.

**Weaknesses.** Bias toward *collecting*; many Second Brains are huge and unread. Weak on original thinking compared to Zettelkasten.

**Verdict.** Adopt progressive summarization for source notes and the "express" mindset that every capture should eventually feed an output.

## GTD — Getting Things Done (David Allen)

**Core idea.** The complete action-management system: **Capture** everything into inboxes; **Clarify** each item (actionable? what's the next action? is it a project?); **Organize** into lists — Next Actions (by context), Projects (anything requiring >1 action), Waiting For, Someday/Maybe, Calendar (hard landscape), Reference; **Reflect** with a **Weekly Review** (empty inboxes, review every list, review calendar, update projects); **Engage** by choosing actions by context, time, energy, priority. The **Horizons of Focus** (runway actions → projects → areas of responsibility → 1–2 year goals → 3–5 year vision → purpose/principles) connect daily action to life direction.

**In Obsidian.** Inbox = `Inbox/` folder plus tasks captured in the daily note. Projects = `type: project` notes with a `## Next actions` list. Next Actions = tasks with `#context` tags or emoji signifiers, surfaced by a **Tasks** query. Waiting For = tasks tagged `#waiting` or with a `👤` delegate convention. Someday/Maybe = projects with `status: someday`. Calendar = due/scheduled dates on tasks, optionally synced to a real calendar. Weekly Review = a weekly note template with the checklist embedded. Horizons = `area` and `goal` notes.

**Strengths.** The only method here that fully solves *Action*. The weekly review is the highest-leverage habit in personal productivity. The "next action" question dissolves procrastination on vague projects.

**Weaknesses.** Says nothing about knowledge; the full system is heavy for people with few commitments; contexts (`@phone`, `@office`) matter less in a laptop-everywhere world.

**Verdict.** Adopt: inboxes, next-action thinking, project list, waiting-for, someday/maybe, the weekly review, horizons (as `area` and `goal` notes). Chapter 16 builds the whole thing.

## Johnny.Decimal

**Core idea.** A numbering system for reference material: at most 10 **areas** (`10-19 Finance`), each with at most 10 **categories** (`11 Banking`), each with numbered **IDs** (`11.01 Current account`). Everything has one place, the number is short enough to remember, and the same numbers are used in files, email folders, and paper.

**In Obsidian.** Folder names prefixed with numbers, or a `jd` property. Works for the *Reference* job (documents, admin records) and for people who like fixed shelves.

**Strengths.** Ends "where does this go?" for admin material; numbers sort predictably everywhere; excellent for shared or cross-tool file systems.

**Weaknesses.** Hierarchical and rigid — exactly what links make unnecessary for ideas. 10×10 limits are arbitrary. Adds cognitive load for every new item.

**Verdict.** Optional. Useful for the `Life/Admin` and documents corner of the vault (and your actual filesystem); pointless for notes that live by links.

## Bullet Journal and daily-note methods

**Core idea.** (Ryder Carroll) A dated log where tasks, events, and notes are rapid-logged with symbols; monthly and future logs; **migration** — periodically rewriting unfinished tasks forward, which forces a decision about each. Digital equivalent: the **daily note** as the default landing page for everything, with structure extracted later.

**In Obsidian.** The Daily notes core plugin (or Periodic Notes for weekly/monthly/quarterly/yearly). Tasks written in the daily note are surfaced by Tasks/Dataview queries so they never need manual migration. **Interstitial journaling** — timestamped one-liners throughout the day (`- 14:32 finished the draft; switching to email`) — provides a record and a focus ritual. Chapter 15 goes deep.

**Verdict.** Adopt the daily note as the *universal inbox and log*. Let queries do migration.

## Other frameworks worth knowing

- **Progressive summarization** — see CODE.
- **Cornell / Feynman / Zettel-style literature notes** — techniques for the *reading* stage; Chapter 17.
- **Digital Gardening** — publishing notes publicly as they grow, with maturity labels; Chapter 31.
- **12 Favorite Problems** (Feynman, via Forte) — a note listing the open questions you care about; every capture is checked against them. Cheap and powerful as a filter.
- **OKRs / 12-Week Year / Quarterly planning** — goal frameworks that slot into the `goal` type; Chapter 16.
- **Commonplace book** — quotes and passages by theme; a `Mind/Commonplace` MOC in Chapter 25.
- **Hipster PDA / Pocket notebook** — analog capture feeding the daily note; fine.

## Anti-patterns (things that look like systems but kill vaults)

1. **Folder taxonomies deeper than three levels.** Every level is a decision at filing time and a dead end at retrieval time.
2. **Tag explosion.** Hundreds of tags used once. Tags should be a short, stable vocabulary; everything else is a link or a property.
3. **Template maximalism.** Twenty-property templates that take longer to fill than the note takes to write. Start with 3–5 properties; add when a query needs one.
4. **Dashboard-first.** Building elaborate Dataview dashboards before there is data. Build the dashboard when the hand-maintained list becomes annoying.
5. **Collector's fallacy.** Clipping hundreds of articles that are never read. Add a `status: to-read` and a Base that shows the pile; if it grows unbounded, stop clipping and start deleting.
6. **Plugin churn.** Rebuilding the system around every new plugin. Freeze the architecture; evaluate plugins against it.
7. **Perfectionist processing.** Refusing to write until you know where a note goes. Write in the daily note; process later.
8. **Single-method zealotry.** "A real Zettelkasten has no folders" / "PARA says move it to Archive". The vault is yours.
9. **No review ritual.** Every method above assumes periodic review. Without it, all of them decay into a pile within months.
10. **Copying someone's vault.** Downloaded showcase vaults encode *their* life. Take ideas; build your own.

## The hybrid this guide recommends

Combine the strongest component of each method for each job:

```mermaid
flowchart TB
    subgraph Capture
      C1[Daily note = universal inbox] --> C2[Inbox folder for clipped/shared items]
    end
    subgraph Action["Action (GTD)"]
      A1[Projects & Areas as typed notes] --> A2[Tasks in notes with due/scheduled] --> A3[Tasks/Bases dashboards] --> A4[Weekly review]
    end
    subgraph Knowledge["Knowledge (Zettelkasten + Evergreen + LYT)"]
      K1[Source notes with progressive summarization] --> K2[Atomic idea notes in own words] --> K3[MOCs when clusters form] --> K4[Home note]
    end
    subgraph Reference["Reference (PARA vocabulary + light JD)"]
      R1[Typed record notes: people, recipes, assets, transactions] --> R2[Bases views instead of folders]
    end
    subgraph Reflection["Reflection (BuJo + periodic notes)"]
      F1[Daily → Weekly → Monthly → Quarterly → Yearly notes] --> F2[Decision journal, annual review]
    end
    Capture --> Action & Knowledge & Reference
    Reflection --> Action & Knowledge
```

Concretely:

| Job | Method borrowed | Obsidian implementation |
| --- | --- | --- |
| Capture | GTD inboxes, BuJo daily log, CODE "capture what resonates" | Daily note as default target; `Inbox/` folder for clipped/shared items; mobile quick-capture template |
| Action | GTD wholesale; PARA's Project/Area distinction; OKR-style goals | `project`, `area`, `goal` note types; Tasks plugin with due/scheduled/priority; Bases views for project portfolio; weekly review template |
| Reference | PARA vocabulary; Johnny.Decimal only for documents | Typed record notes (`person`, `recipe`, `asset`, `subscription`…) with properties; Bases tables as the "folders"; a few real folders |
| Knowledge | Zettelkasten discipline; Evergreen maturity; LYT MOCs; CODE progressive summarization | `Sources/` with distilled highlights; `Notes/` atomic claims with `status` maturity; `Maps/` MOCs created at squeeze points; `Home.md` |
| Reflection | BuJo, periodic notes, decision journals, annual review | Periodic Notes hierarchy with templates that roll up (weekly embeds/links dailies, monthly summarizes weeklies…); `decision` notes; yearly review template |

The folder skeleton that hosts this is a lightly modified ACCESS; Chapter 8 gives it in full.

## How to choose your emphasis

Everyone's vault leans one way. Decide yours explicitly:

- **Knowledge-heavy** (researcher, writer, student): invest in `Sources/`, `Notes/`, MOCs, spaced repetition, Zotero. Keep action management minimal — a project list and a weekly review.
- **Action-heavy** (manager, founder, parent running a household): invest in projects, tasks dashboards, people notes, meeting notes, periodic reviews. Keep knowledge as a curated reading pipeline.
- **Records-heavy** (life admin, health tracking, finances): invest in typed record notes and Bases; templates and quick-capture on mobile matter most.
- **Reflection-heavy** (journaling, self-development): invest in the periodic-notes hierarchy, mood/energy properties, decision journal, and the reviews.

The whole-life vault needs all four, but you will start with one, and the others come online over months. The [Roadmap](35-mastery-roadmap.md) sequences this.

## Key takeaways

- Methods solve different jobs: Zettelkasten/Evergreen/LYT → knowledge; GTD → action; PARA → vocabulary for projects vs areas; CODE → capture and distillation; BuJo/periodic notes → reflection; Johnny.Decimal → documents.
- Take the strongest component of each: daily-note capture, GTD action management with a weekly review, atomic idea notes with MOCs, typed record notes viewed through Bases, and a periodic-notes reflection ladder.
- Avoid the anti-patterns: deep folders, tag explosion, template and dashboard maximalism, the collector's fallacy, plugin churn, and no review ritual.
- Decide which of knowledge/action/records/reflection you are emphasizing first; the rest follows.

## Next

[Chapter 8: Vault Architecture — the Reference Design →](#vault-architecture-the-reference-design)

---

# Vault Architecture — the Reference Design

This chapter is the blueprint. It gives a complete, opinionated vault design for someone who wants to run their whole life in Obsidian: the folder tree, naming conventions, the note-type catalogue with schemas, the flow of information from capture to archive, the MOC hierarchy, and the policies for attachments and archiving. Every domain chapter in Part IV assumes this design (and says how to adapt it). You can copy it wholesale or take pieces; either way, write your own version down in a `Meta/Vault Guide.md` note so the design survives your memory.

## Design goals

1. **Shallow.** No more than two folder levels in daily use. Depth comes from links and Bases, not folders.
2. **Typed.** Every note has a `type` property. Dashboards, templates, and queries key off it.
3. **Capture-first.** There is always an obvious, zero-decision place to put something: the daily note or `Inbox/`.
4. **Query, don't file.** Lists of things are Bases/Dataview views over properties, never hand-maintained.
5. **Portable.** Nothing essential lives only in a plugin's `data.json`. Folder names and properties make sense without Obsidian.
6. **Mobile-sane.** Capture and reading work on a phone with a handful of plugins; administration happens on desktop.

## The folder tree

```text
Vault/
├── 00 Home.md                  ← the front door (dashboard)
├── Inbox/                      ← unprocessed captures (clips, shares, quick notes)
├── Journal/
│   ├── Daily/                  ← 2026-09-06.md
│   ├── Weekly/                 ← 2026-W36.md
│   ├── Monthly/                ← 2026-09.md
│   ├── Quarterly/              ← 2026-Q3.md
│   └── Yearly/                 ← 2026.md
├── Projects/                   ← one note per project (or one subfolder per big project)
├── Areas/                      ← one note per area of life + area MOCs
├── Goals/                      ← goal notes (year / quarter / life)
├── People/                     ← one note per person
├── Sources/                    ← things other people made
│   ├── Books/
│   ├── Articles/
│   ├── Papers/
│   ├── Podcasts/
│   ├── Videos/
│   └── Courses/
├── Notes/                      ← your atomic ideas (Zettelkasten "permanent notes")
├── Maps/                       ← MOCs (maps of content)
├── Work/                       ← meetings, decisions, docs (or a separate vault if confidentiality demands)
│   ├── Meetings/
│   └── Docs/
├── Life/                       ← records: admin, home, travel, recipes, inventory, habits
│   ├── Admin/
│   ├── Home/
│   ├── Travel/
│   ├── Recipes/
│   ├── Inventory/
│   └── Habits/
├── Health/
│   ├── Workouts/
│   └── Log/
├── Finance/
│   ├── Accounts/
│   ├── Subscriptions/
│   └── Ledger/
├── Mind/                       ← reflection: decisions, values, principles, quotes, reviews
├── Bases/                      ← .base files (dashboards)
├── Canvases/
├── Templates/                  ← excluded from search/suggestions
├── Scripts/                    ← Templater user scripts, CSS snippets source, misc
├── Attachments/                ← everything binary (auto-routed)
├── Archive/                    ← mirrors the top-level structure for finished/inactive items
└── Meta/                       ← Vault Guide.md, Schema.md, Plugin list.md, Changelog.md
```

Why this shape:

- It is **ACCESS-adjacent** (Atlas→Maps, Calendar→Journal, Cards→Notes, Extras→Templates/Attachments/Scripts, Sources→Sources, Spaces→Projects/Areas/Work/Life…) but names folders by *what is inside* so they make sense without reading Nick Milo.
- **Projects, Areas, Goals, People** are top-level because they are the nouns every other note links to; you want them visible and quick to reach.
- **Life/Health/Finance** are separate from Areas: `Areas/Health.md` is the *area note* (standards, goals, review cadence); `Health/` holds the *records*. This distinction keeps the area note readable.
- **Work** is separate so it can be excluded from Publish, moved to its own vault, or deleted when you change jobs.
- **`00 Home.md`** sorts first; the numeric prefix is the only one in the vault.
- **Bases/** collects `.base` files so they are easy to find and embed; embedded bases in notes are fine too.
- **Archive/** mirrors the structure so moving something is mechanical and finding it later is predictable. Archiving is a *status change first*, a move second (see policy below).

!!! tip "Adapting"
    Fewer folders is always fine. A minimal variant: `Inbox, Journal, Notes, Sources, Projects, People, Life, Templates, Attachments, Archive`. Add a folder only when a Base filter by `type` is not enough — usually because of attachment routing, templates-per-folder, or publish/sync exclusion.

## Naming conventions

| Thing | Convention | Example |
| --- | --- | --- |
| Daily note | `YYYY-MM-DD` | `2026-09-06` |
| Weekly | `YYYY-[W]WW` (ISO week) | `2026-W36` |
| Monthly | `YYYY-MM` | `2026-09` |
| Quarterly | `YYYY-[Q]Q` | `2026-Q3` |
| Yearly | `YYYY` | `2026` |
| Project | Imperative or noun phrase, Title Case | `Launch Newsletter`, `Kitchen Renovation` |
| Area | Single noun, Title Case | `Health`, `Finances`, `Career`, `Family` |
| Goal | Outcome statement, optionally with year | `Run a Half Marathon 2027` |
| Person | Full name as you would say it | `Jane Doe`; aliases for nicknames |
| Source | Title of the work (no author) | `Deep Work`; author is a property + link |
| Idea note | A declarative claim in sentence case | `Constraints increase creativity` |
| MOC | Topic + " MOC" (or "Map") | `Sleep MOC`, `Stoicism Map` |
| Meeting | `YYYY-MM-DD Topic` | `2026-09-06 Alpha kickoff` |
| Decision | `YYYY-MM-DD Decision - Topic` or claim | `2026-09-06 Decision - Switch to Fastmail` |
| Recipe | Dish name | `Shakshuka` |
| Workout | `YYYY-MM-DD Kind` | `2026-09-06 Strength A` |
| Templates | `tpl-<type>` | `tpl-project`, `tpl-daily` |
| Bases | `<Noun> Base` or purpose | `Projects.base`, `Reading List.base` |
| Attachments | `<note-slug>-<description>.<ext>` or `YYYYMMDD-<desc>` | `kitchen-renovation-floorplan.png` |

Rules:

- **Unique names across the vault.** If two things want the same name, disambiguate with a qualifier in the title (`Alpha (project)` / `Alpha (person)`) — or better, rename one.
- **No dates in idea-note titles; always dates in event-note titles.**
- **Title Case for nouns (people, projects, sources); sentence case for claims.** It signals the note type at a glance.
- **Avoid special characters** (`: / \ | # ^ [ ] ?`) — Obsidian forbids most of them anyway; `&` and `'` are fine but hurt URLs on Publish.
- **Do not put the type in the filename** (`Project - Alpha`). The `type` property and the folder carry that.

## Note types and schemas (the catalogue)

Chapter 5 listed the schema; here are the *templates' skeletons* for the core types. Full Templater versions are in Chapters 11 and 36.

### Daily note

```markdown
---
type: daily
date: 2026-09-06
mood:
energy:
sleep_h:
tags: []
---
« [[2026-09-05]] | [[2026-W36]] | [[2026-09-07]] »

## Plan
- [ ]

## Log
- 07:10

## Notes

## Gratitude / reflection
```

### Project

```markdown
---
type: project
status: active          # idea | active | on-hold | done | dropped
area: "[[Career]]"
goal:
priority: 2             # 1 high · 2 normal · 3 low
start: 2026-09-01
due:
completed:
tags: []
---
## Outcome
One sentence: what "done" looks like.

## Next actions
- [ ]

## Log
- 2026-09-01 — Kicked off.

## Notes & links

## Review
Last reviewed: 2026-09-06
```

### Area

```markdown
---
type: area
review_cadence: monthly
standard: "Sleep 7.5h avg, train 3×/week, resting HR < 60"
tags: []
---
## Why this matters

## Current standard
(what "good enough" looks like — the bar you maintain)

## Active projects
```base
filters:
  and:
    - type == "project"
    - status == "active"
    - area == this
views:
  - type: table
    name: Active
    order: [file.name, due, priority]
```

## Habits & routines

## Related maps
```

### Person

```markdown
---
type: person
relationship: friend    # family | friend | colleague | acquaintance | professional
birthday:
email:
phone:
company:
location:
last_contact:
contact_every: 60       # days
tags: []
---
## About

## Interactions
(Backlinks from daily notes and meetings do most of the work; add a line here for significant events.)

## Gift ideas / preferences

## Family & connections
```

### Source (book example)

```markdown
---
type: source
medium: book            # book | article | paper | podcast | video | course
author: ["[[Cal Newport]]"]
status: reading         # to-read | reading | read | abandoned
rating:
started: 2026-08-14
finished:
url:
isbn:
topics: ["[[Focus]]", "[[Productivity]]"]
tags: []
---
> [!summary] In one paragraph
> (fill in after finishing)

## Key ideas (own words, one per bullet → candidates for [[Notes]])
-

## Highlights & notes
(progressive summarization: **bold** the important, ==highlight== the essential)

## Quotes
```

### Idea note

```markdown
---
type: note
status: seedling        # seedling | budding | evergreen
topics: []
sources: []
tags: []
---
(The claim in the title, argued in 1–5 paragraphs, in your own words. Link generously, with reasons.)

## Related
-
```

### MOC

```markdown
---
type: moc
area:
tags: [moc]
---
> [!abstract] Scope
> What this map covers and how it is organized.

## Start here
-

## Core ideas
-

## Sources
-

## Open questions
-

## Unsorted (recent notes tagged/linked here)
```dataview
LIST FROM [[]] AND -"Maps" WHERE type = "note" SORT file.ctime DESC LIMIT 20
```
```

### Meeting

```markdown
---
type: meeting
date: 2026-09-06
attendees: ["[[Jane Doe]]"]
project: "[[Launch Newsletter]]"
decisions: []
next_meeting:
tags: []
---
## Agenda
## Notes
## Decisions
## Actions
- [ ] 👤 Jane —
- [ ] Me —
```

### Decision

```markdown
---
type: decision
date: 2026-09-06
status: decided         # open | decided | reviewed
confidence: 7
review_on: 2027-03-06
options: []
chosen:
tags: []
---
## Context
## Options considered
## Decision & reasoning
## Expected outcome (falsifiable)
## Review (fill on review_on)
```

## The flow: capture → process → organize → use → archive

```mermaid
flowchart LR
    A[Capture<br/>daily note · Inbox · share sheet · web clipper · CLI] --> B[Process<br/>daily/weekly: type it, link it, move it]
    B --> C[Organize<br/>lives in its folder with properties]
    C --> D[Use<br/>Bases · dashboards · MOCs · search · reviews]
    D --> E[Archive<br/>status: done → Archive/ mirror]
    D -->|insights| F[Notes/ · Maps/]
```

**Capture** — four entrances, all zero-decision:

1. *Daily note* (hotkey): tasks, log lines, fleeting ideas, links to people and projects as they come up.
2. *Inbox/* (default new-note location for quick switcher creates, Web Clipper, mobile Share Sheet, `obsidian create` from scripts).
3. *Directly typed* when the type is obvious (a new person, a new recipe) via a QuickAdd/Templater command that asks for the type and files it.
4. *Automated* (Readwise export, calendar → meeting notes, email-to-vault) landing in `Inbox/` or the correct folder with properties pre-filled.

**Process** — daily (5 min) or weekly (30 min): open `Inbox/` (a Base sorted by ctime), for each item: give it a `type` (template), link it to its project/area/person/topic, move it to its folder (or delete it). Tasks written in daily notes need no processing — queries surface them. Ideas noted in the daily note that deserve their own page get extracted (Note composer) into `Notes/`.

**Organize** — the folder + properties are the organization. Nothing else to do.

**Use** — `00 Home.md` is the daily entry (embedded Bases: today's tasks, active projects, people to contact, reading in progress; links to this week's note and top MOCs). Area notes are the monthly entry. MOCs are the knowledge entry. Search for everything else.

**Archive** — see policy below.

## The MOC hierarchy

```mermaid
flowchart TB
    H[00 Home] --> A1[Areas MOC] & K[Knowledge MOC] & L[Life MOC] & P[Projects Base]
    A1 --> Health[Health MOC] & Career[Career MOC] & Fin[Finances MOC] & Fam[Family MOC]
    K --> T1[Topic MOC: Focus] & T2[Topic MOC: Stoicism] & T3[Topic MOC: Systems thinking]
    T1 --> N1[Idea notes...]
    L --> Home2[Home & Admin MOC] & Travel[Travel MOC] & Food[Food MOC]
```

- **Home** links to ≤ 12 things. If it needs more, add a level.
- **Area MOCs** (one per area) combine the area note's standards with links to its projects, habits, records bases, and topic MOCs.
- **Topic MOCs** curate idea notes and sources on a subject. Create one when ~15 notes cluster (local graph tells you).
- **Life MOCs** index records: recipes, travel, home. Often just an embedded Base plus a few links.
- Every MOC links *up* to its parent in a first line (`Up: [[Knowledge MOC]]`) so navigation works both ways; the **Breadcrumbs** plugin can formalize this if you like hierarchies.

## Attachments policy

- Everything binary goes to `Attachments/` (setting). One flat folder is fine up to a few thousand files; beyond that, `Attachments/YYYY/` via the **Attachment Management** or **Custom Attachment Location** plugins.
- Rename pasted images at paste time (`Pasted image 2026….png` is unsearchable). Plugins: *Paste image rename*, *Attachment Management* (auto-renames to `<note>-<n>`).
- PDFs of sources go to `Attachments/` and are *embedded* in the source note (`![[book.pdf#page=12]]`); annotations live in the note (PDF++ writes highlights as links).
- Large media (video, raw photos, datasets) live **outside** the vault (cloud drive or NAS) and are linked with `file:///` or `https://` links; the vault stays small enough to sync to a phone.
- Exclude `Attachments/` in *Excluded files* so it never pollutes search or the `[[` suggester.
- Monthly: the **Janitor** plugin (or 1.12's delete-attachments prompt as you go) removes orphans.

## Archive policy

1. **Status first.** When a project finishes: `status: done`, `completed: <date>`. Bases and dashboards already hide it. Do this immediately.
2. **Move later.** Quarterly, move `done`/`dropped` projects, finished trips, past years' meetings, etc. into `Archive/<mirrored path>`. Links keep working (shortest-path or auto-update).
3. **Never archive** People, Sources, Notes, Maps, or Areas — they are timeless. A person you lost contact with gets `relationship: former`; a dead source is still a source.
4. **Journal is never moved.** `Journal/Daily/` grows forever; years of daily notes are the point.
5. **Exclude `Archive/`** from search suggestions if it gets noisy (it still searches when you use `path:Archive`).

## Templates set

The minimum: `tpl-daily`, `tpl-weekly`, `tpl-monthly`, `tpl-quarterly`, `tpl-yearly`, `tpl-project`, `tpl-area`, `tpl-goal`, `tpl-person`, `tpl-source`, `tpl-note`, `tpl-moc`, `tpl-meeting`, `tpl-decision`. Domain-specific (`tpl-recipe`, `tpl-workout`, `tpl-trip`, `tpl-subscription`…) get added as domains come online. Chapter 11 implements them with Templater (folder templates auto-apply: new note in `People/` → `tpl-person`), Chapter 36 collects them.

## Bases set (dashboards)

Kept in `Bases/`, embedded where needed:

| Base | Filter | Views |
| --- | --- | --- |
| `Inbox.base` | `file.inFolder("Inbox")` | table by ctime |
| `Projects.base` | `type == "project"` | Active (table), By area (grouped), Timeline (sorted by due), Done this year |
| `People.base` | `type == "person"` | Contact due (`last_contact + contact_every days < today()`), Birthdays this month, By relationship |
| `Reading.base` | `type == "source"` | To read, Reading, Finished by year (cards with covers) |
| `Ideas.base` | `type == "note"` | Seedlings to develop, Evergreens, Recently touched |
| `Meetings.base` | `type == "meeting"` | This week, By project |
| `Decisions.base` | `type == "decision"` | Open, Due for review |
| `Recipes.base` | `type == "recipe"` | Cards by cuisine, Not made in 60 days |
| `Subscriptions.base` | `type == "subscription"` | Active with monthly cost sum, Renewing in 30 days |
| `Workouts.base` | `type == "workout"` | Last 30 days, By kind with duration sums |
| `Habits.base` | `type == "habit"` | Active |

Chapter 10 provides the YAML for all of these.

## The Home note

```markdown
---
type: moc
cssclasses: [dashboard]
---
# Home
**Today:** [[<% tp.date.now("YYYY-MM-DD") %>]] · **Week:** [[<% tp.date.now("YYYY-[W]WW") %>]] · [[Weekly Review]]

## Today's tasks
```tasks
not done
(due before tomorrow) OR (scheduled before tomorrow)
sort by priority
```

## Active projects
![[Projects.base#Active]]

## People to reach out to
![[People.base#Contact due]]

## Reading
![[Reading.base#Reading]]

## Maps
[[Areas MOC]] · [[Knowledge MOC]] · [[Life MOC]] · [[Inbox.base|Inbox]]
```

(The `<% %>` date is a Templater snippet — the Home note is regenerated daily by a Templater "startup template", or use the **Homepage** plugin to open it on launch and Dataview inline `= date(today)` for the date.)

## Multi-vault vs single vault (final word)

Single vault for personal life. Consider a second vault only for: an employer's confidential material (legal/contractual separation), a shared vault with family or a team (different sync permissions), or a publish-only vault (a digital garden built from copied notes). If you split, keep the *same* folder skeleton and templates in both so muscle memory transfers.

## Setting it up in 30 minutes

1. Create the folders (copy the tree; delete what you will not use this quarter).
2. Settings: attachments → `Attachments/`; new notes → `Inbox/`; excluded files → `Templates/`, `Attachments/`, `Archive/`; Templates folder → `Templates/`; Daily notes → `Journal/Daily`, format `YYYY-MM-DD`, template `tpl-daily`.
3. Install Templater, Tasks, Dataview (Chapter 14 tiers) — three plugins are enough to start.
4. Paste the templates above into `Templates/` (Templater versions in Chapter 11).
5. Create `00 Home.md`, `Areas/` notes for your 5–8 areas, and one project note per active project.
6. Create `Projects.base` and `Inbox.base` (Chapter 10) and embed them in Home.
7. Write today's daily note. Stop building. Use it for two weeks before adding anything.

## Key takeaways

- Shallow, typed, capture-first, query-not-file, portable, mobile-sane — every decision in the design follows from these six goals.
- The folder tree is ACCESS-shaped with plain names; Projects/Areas/Goals/People are top-level nouns; records (Life/Health/Finance) are separate from area notes; Archive mirrors the tree.
- Naming: dates for events, claims for ideas, Title Case for nouns, unique names always, no type in filenames.
- Four capture entrances (daily note, Inbox, typed create, automation), one processing ritual, Bases as the organization layer, Home → Area/Topic/Life MOCs as the navigation layer.
- Archive by status first, move quarterly; never archive people, sources, ideas, maps or the journal.
- Set it up in 30 minutes, then use it for two weeks before building more.

## Next

[Chapter 9: Core Plugins — Every One, Mastered →](#core-plugins-every-one-mastered)

---

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

---
