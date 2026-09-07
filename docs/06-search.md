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

[Chapter 7: PKM Methodologies Compared →](07-pkm-methodologies.md)
