# PROGRESS / WORKLOG — read this first after any context compaction

This file is the single source of truth for the state of this project. If you are an AI
instance resuming work (after context compaction or an account switch), **read this file
fully, then `git log --oneline | head -20`, then `ls docs/`**, and continue from
"Next steps". Keep this file updated and push after every chapter.

## The task (from the user)

Create the best possible, most detailed, comprehensive, in-depth review/guide on how to
master Obsidian and maximize its utility for one's life and everything related to it.
Deliverables: (1) Markdown guide, (2) website adaptation deployed to GitHub Pages.

User answers to clarifying questions:
- Audience: assume basic familiarity with Obsidian; go DEEP. No length ceiling — "as many
  words as you want".
- Scope: include ALL proposed topics, very detailed (fundamentals, methodologies, every
  life domain, plugin deep dives with working code, sync/backup/security, publishing, AI,
  customization/CSS, automation/CLI/URI, performance/migration/troubleshooting, roadmap,
  templates, cheat sheets).
- User wants to use Obsidian for EVERYTHING in life — so the life-domain chapters matter a lot.
- Everything else: my call. "Be as thorough as possible."

Workflow constraints from the user:
- Push straight to `main`. NO branches / PRs.
- Push constantly (workflow may be interrupted by credits running out; last turn is lost).
- Context compaction will happen; document reasoning so the next instance continues seamlessly.

## Decisions taken (do not re-litigate; just continue)

- Site generator: **MkDocs Material** (`mkdocs.yml` at repo root).
- Deployment: the GitHub App token CANNOT push `.github/workflows/*` (no `workflows`
  permission — push was rejected). So we deploy with **`mkdocs gh-deploy --force`**, which
  builds and pushes the static site to the `gh-pages` branch. GitHub Pages must be set to
  serve from branch `gh-pages` / root (try `gh api -X POST repos/gorg667/obsidian-guide/pages
  -f source[branch]=gh-pages -f source[path]=/` at the end; otherwise tell the user to set
  Settings → Pages → Deploy from a branch → gh-pages). The optional Actions workflow is kept
  at `deploy-templates/github-pages-workflow.yml` for the user to move into
  `.github/workflows/` manually if they prefer CI builds.
- Run `mkdocs gh-deploy --force -q` after every few chapters (it's fast) so the live site
  is never far behind `main`.
- Structure: one Markdown file per chapter in `docs/` named `NN-slug.md`, each starting
  with exactly one `# H1`. `docs/index.md` is the landing page. `scripts/build_guide.py`
  concatenates chapters (in nav order) into a root `GUIDE.md` (single-file edition).
  Run it before committing when chapters change: `python3 scripts/build_guide.py`.
- Style: English; direct, opinionated, practical; heavy on concrete examples, code
  blocks (Dataview DQL/DataviewJS, Templater, Bases YAML, Tasks queries, CSS, CLI, URI),
  MkDocs admonitions (`!!! tip`, `!!! warning`, `!!! note`, `!!! example`, `???
  "collapsible"`), tables, and Mermaid diagrams. No images (keeps repo light & reliable).
- Obsidian version baseline: **1.13.x (July/Aug 2026)**. Facts verified from
  obsidian.md changelog/roadmap/help in this session:
  - 1.9 (Aug 2025): **Bases** core plugin (.base files; table/cards views; filters,
    formulas; embedded via ```base code blocks).
  - 1.10 (Nov 2025): Bases Group by, table Summaries, List view, Bases API (plugins can add
    view types — official Maps plugin), keyboard nav, copy/paste; new list functions
    reduce/mean/stddev/median, html(), random(); "Toggle light/dark mode" command replaced
    the two separate ones; Properties core plugin enabled by default; Notion importer → Bases.
  - 1.11 (Jan 2026): **Keychain** (secret storage for plugin API keys).
  - 1.12 (Feb 2026): **Obsidian CLI** (`obsidian <command> param=value flag`; TUI; commands
    for daily, search, tasks, bases, properties, plugins, sync, publish, dev tools, eval);
    image resize by drag; automatic attachment cleanup prompt; Bases search toolbar, drag &
    drop import; Canvas backlinks detection; `unique` URI action; file explorer copy/paste.
  - 1.13 (Jul 2026): searchable Settings in new window w/ keyboard nav; full-screen image
    viewer + keyboard image resize (+/-/0); URI confirmation dialog w/ allow list; Sync
    plugin-sync warning; Bookmarks search; Mermaid render confirmation banner; folder drag
    import; `--callout-color` now expects a full CSS color (breaking for CSS snippets);
    OKLCH base colors; iOS Share Sheet (mobile 1.13); Airtable importer (Aug 2026).
  - Web Clipper (browser extension, 2024) + Interpreter (natural-language extraction).
  - Web viewer core plugin (1.8, Dec 2024).
  - Pricing (2026): Sync from ~$4/mo annual ($5 monthly) Standard; Publish $8/site/mo
    annual ($10 monthly). Commercial license $50/user/year; personal use free.
  - Bases syntax reference & full function list were fetched (see chapter 12 for the
    distilled version). `this` semantics: in main area = base file; embedded = embedding
    note; sidebar = active file.

## Chapter plan (nav order). Status legend: [ ] todo, [~] in progress, [x] done+pushed

Part I — Foundations
- [x] 00 index.md — landing page: what this is, how to read it, TOC, who it's for
- [x] 01-philosophy.md — Why Obsidian; file-over-app; local-first; plain text; the mental
      model (vault = folder, note = file, links = graph, properties = metadata); what
      Obsidian is bad at; the 4 layers of mastery
- [x] 02-setup-and-interface.md — installation on all platforms, vault design decisions,
      settings audit (every setting that matters + recommended values), interface anatomy,
      workspace layouts, tabs/splits/stacked tabs, hotkeys philosophy, command palette,
      quick switcher, Settings search (1.13), Restricted mode, multiple vaults strategy
- [x] 03-markdown-and-editing.md — Obsidian-flavored Markdown exhaustive: headings, lists,
      tasks, callouts (all types + custom + foldable), tables, footnotes, math, Mermaid,
      code blocks, comments, highlights, HTML, embeds of everything, block IDs, editing
      tricks, multi-cursor, Vim mode, Live Preview vs Source vs Reading, formatting menu,
      image handling (1.12/1.13)
- [x] 04-links-and-graph.md — wikilinks vs markdown links, aliases, heading/block links,
      embeds, backlinks, outgoing links, unlinked mentions, link maintenance, Graph view
      (filters, groups, colors, local graph), Canvas deep dive + JSON Canvas
- [x] 05-properties-tags-and-metadata.md — properties (all types), YAML gotchas, tags vs
      properties vs folders vs links (decision framework), nested tags, aliases, cssclasses,
      Global Properties view, schema design for a life vault
- [x] 06-search.md — full search operator reference, regex, embedded search, saved
      searches, search in Bases/Dataview comparison, Omnisearch

Part II — Systems & methodology
- [x] 07-pkm-methodologies.md — Zettelkasten, Evergreen notes, LYT/MOCs, PARA, CODE/Second
      Brain, Johnny.Decimal, GTD, ACCESS, Progressive summarization; comparison matrix;
      hybrid recommended system; anti-patterns
- [x] 08-vault-architecture.md — the recommended reference vault: folder tree, naming
      conventions, note types & their schemas, template set, inbox → process flow, MOC
      hierarchy, attachments policy, archive policy, multi-vault vs single vault

Part III — Core plugins mastery
- [x] 09-core-plugins.md — every core plugin: what/when/settings/tricks (Daily notes,
      Templates, Backlinks, Bookmarks, Canvas, Command palette, File recovery, Note
      composer, Outline, Page preview, Properties view, Publish, Quick switcher, Random
      note, Slash commands, Slides, Sync, Tags view, Templates, Unique note creator, Web
      viewer, Word count, Workspaces, Footnotes view, Importer, Bases, Format converter)
- [x] 10-bases.md — Bases deep dive: .base format, views (table/cards/list/map), filters,
      formulas, functions reference (condensed), summaries, groupBy, `this`, embedded
      bases, 25+ ready-made bases for life domains, Bases vs Dataview, migration
- [x] 11-templates-and-templater.md — core Templates → Templater: syntax, tp.* modules,
      user scripts, dynamic commands, folder templates, prompts/suggesters, 30+ templates
- [x] 12-dataview.md — DQL (TABLE/LIST/TASK/CALENDAR, FROM/WHERE/SORT/GROUP BY/FLATTEN),
      inline fields, functions, DataviewJS, dv.* API, performance, 50+ queries for life
      domains, common errors
- [x] 13-tasks-and-time.md — Tasks plugin (syntax, emoji signifiers, queries, recurrence,
      dependencies, custom statuses), Periodic Notes, Calendar, Day Planner, Kanban,
      Full Calendar, Reminder; complete task management system design
- [x] 14-essential-community-plugins.md — curated tiers: must-have, situational, avoid;
      per plugin: purpose, config, gotchas (QuickAdd, Excalidraw, Omnisearch, Linter,
      Advanced Tables, Style Settings, Commander, Homepage, Various Complements, Editing
      Toolbar, Iconize, Recent Files, Auto Note Mover, Note Refactor, Tag Wrangler,
      Janitor, Text Generator, Buttons, Meta Bind, Map View, Media Extended, PDF++,
      Annotator, Zotero Integration, Citations, Pandoc, Enveloppe, Shell commands,
      Advanced URI, Local REST API, Git, Remotely Save, Self-hosted LiveSync, Spaced
      Repetition, Flashcards, Book Search, Kindle Highlights, Readwise, Hover Editor,
      Sliding panes, Minimal theme settings, Numerals, Tracker, Heatmap Calendar, Charts,
      Projects, DB Folder, Breadcrumbs, Waypoint, Folder notes, Supercharged links…)

Part IV — Obsidian for everything in life (one section per domain, each with: purpose,
note types & schema, templates, Bases/Dataview dashboards, workflows, plugins, pitfalls)
- [x] 15-daily-notes-and-journaling.md — daily/weekly/monthly/quarterly/yearly notes,
      journaling frameworks, mood/energy tracking, interstitial journaling, reviews
- [x] 16-tasks-projects-goals.md — full GTD-style system: inbox, projects, areas, goals,
      OKRs, someday/maybe, waiting-for, weekly review, dashboards, habit loops
- [x] 17-knowledge-learning.md — reading system (books/articles/papers), literature
      notes → permanent notes, spaced repetition, courses, language learning, skills
- [x] 18-academic-research.md — Zotero pipeline, citations, PDF annotation, literature
      reviews, thesis writing, Pandoc export, LaTeX
- [x] 19-work-and-career.md — meeting notes, people/CRM, 1:1s, decision logs, project
      docs, career journal, brag document, job search
- [x] 20-health-fitness-food.md — workout logs, nutrition, recipes/meal planning, medical
      records, symptoms, sleep, quantified-self dashboards
- [x] 21-finance.md — budgets, expenses, subscriptions, net worth, investments log,
      taxes, purchases/warranties; Bases & Dataview money dashboards
- [x] 22-home-life-admin.md — household, maintenance, documents, inventory, travel
      planning, vehicles, pets, kids, gifts, contacts, digital legacy
- [x] 23-relationships-and-people.md — people notes, interaction log, birthdays,
      gratitude, family history, "personal CRM" the right way
- [x] 24-creativity-writing-media.md — long-form writing (Longform), worldbuilding,
      idea capture, music/movies/games logs, photography, hobbies
- [x] 25-mind-and-self.md — values, principles, reflection, therapy notes, decision
      journal, mental models, commonplace book, quotes, annual review

Part V — Power user
- [x] 26-sync-backup-security.md — Sync vs iCloud vs Syncthing vs Git vs Remotely Save vs
      LiveSync (matrix), mobile specifics, conflict handling, backup 3-2-1, encryption,
      plugin security, Keychain, URI allow list
- [x] 27-mobile.md — iOS/Android setup, mobile-friendly workflows, Share Sheet (1.13),
      Shortcuts/Tasker automation, mobile toolbar, quick capture
- [x] 28-customization.md — themes (best), Style Settings, CSS snippets (30+ snippets),
      cssclasses, callout styling (new --callout-color), fonts, icons, workspace tuning
- [x] 29-automation-and-integrations.md — Obsidian URI (all actions), Advanced URI,
      Obsidian CLI (full command cheat sheet + scripts), Shell commands, Local REST API,
      Hookmark, Raycast/Alfred, Apple Shortcuts, Tasker, Zapier/n8n, email-to-vault,
      calendar sync, Readwise, Web Clipper (templates, Interpreter)
- [ ] 30-ai.md — Copilot, Smart Connections, Text Generator, local LLMs (Ollama), MCP
      servers for Obsidian, Claude/ChatGPT desktop + CLI + REST, Web Clipper Interpreter,
      prompts library, privacy considerations, what AI is actually good for in PKM
- [ ] 31-publishing-and-sharing.md — Publish, Quartz, Digital Garden, MkDocs, Hugo,
      export to PDF/Word (Pandoc), Slides, sharing single notes
- [ ] 32-performance-maintenance-troubleshooting.md — large vaults, plugin audit,
      indexing, attachments, broken links, orphan cleanup, Linter, File recovery,
      common error patterns, debugging (CLI dev tools), safe mode
- [ ] 33-migration.md — from Notion, Evernote, Roam, Logseq, Apple Notes, OneNote,
      Google Keep, Bear, Craft, Airtable; importer; cleanup afterwards; exporting out
- [ ] 34-plugin-development-primer.md — enough to write your own plugin: scaffold,
      API basics, Bases view API, CLI dev commands, publishing to the directory

Part VI — Reference
- [ ] 35-mastery-roadmap.md — 30/60/90-day & 1-year roadmap, weekly exercises,
      self-assessment checklist, maturity model
- [ ] 36-templates-library.md — all templates in one place, copy-paste ready
- [ ] 37-cheatsheets.md — hotkeys, Markdown, search operators, Dataview, Bases
      functions, Templater, Tasks, CLI, URI
- [ ] 38-resources-and-glossary.md — glossary, curated resources, communities

## Conventions for writing chapters

- Start with `# Title`, then a 2–4 sentence "What you'll get from this chapter" intro,
  then `## In this chapter` bullet list is optional. End each chapter with
  `## Key takeaways` and `## Next` (link to next chapter).
- Use `!!! tip "..."`, `!!! warning "..."`, `!!! note`, `!!! example`, `!!! danger`,
  `??? info "..."` (collapsible).
- Code fences: ```dataview, ```dataviewjs, ```base, ```yaml, ```markdown, ```css,
  ```bash, ```javascript, ```tasks, ```mermaid. NOTE: Because MkDocs superfences renders
  unknown languages fine, ```dataview is OK. For ```base use `yaml` highlighting with a
  comment line `# (.base file)` OR just ```yaml.
- Escape nothing weird: MkDocs treats `[[wikilinks]]` as literal text (fine). But inside
  tables the `|` char must be escaped as `\|`.
- Templater tags `<% %>` are fine in code blocks. Do NOT put raw `<% %>` outside code.
- Aim for 2,500–6,000+ words per chapter depending on topic. Depth over fluff.
- After finishing a chapter: add it to `nav` in mkdocs.yml, run
  `python3 scripts/build_guide.py`, `mkdocs build --strict` (if mkdocs installed
  locally — it is, via pip), update this file, commit, push.

## Commit/push routine (every chapter)

```bash
cd /home/user/webapp && python3 scripts/build_guide.py && mkdocs build --strict -q && \
git add -A && git commit -m "docs: <chapter>" && git push origin main && mkdocs gh-deploy --force -q
```

## Status log

- IMPORTANT: enabling GitHub Pages via API returned 403 (token lacks permission). The
  `gh-pages` branch exists and is populated by `mkdocs gh-deploy --force`. The USER must
  do once: repo Settings → Pages → Source "Deploy from a branch" → branch `gh-pages`,
  folder `/ (root)`. Tell them in the final message.
- Sandbox/account switch happened after ch03; ch04 was lost and rewritten. Lesson: commit
  IMMEDIATELY after each Write, never batch.

- 2026-09-06: Repo scaffolded (mkdocs.yml, workflow, build script, PROGRESS.md). Research
  done on Obsidian 1.9–1.13 changelogs, Bases syntax/functions, CLI reference.

## Next steps

1. Write docs/index.md (landing page).
2. Write chapters in order 01 → 38. Update nav + this file after each.
3. At the end: verify GH Pages workflow succeeded (gh run list), try enabling Pages via
   `gh api -X POST repos/gorg667/obsidian-guide/pages -f build_type=workflow`, write
   README.md pointing to site + GUIDE.md, final message to user with URLs and the
   Settings → Pages instruction as fallback.
