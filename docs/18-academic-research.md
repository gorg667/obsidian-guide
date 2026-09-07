# Academic Research

Research adds three hard requirements to the knowledge pipeline: **citations** that must be exact, **PDFs** that must be annotated and findable, and **long documents** (theses, papers, grant proposals) that must be exported in formats reviewers demand. Obsidian handles all three with Zotero as the reference manager, PDF++ for annotation, Pandoc for export, and the idea-note discipline from Chapter 17 for the actual thinking. This chapter is the complete research workflow, from literature search to submitted manuscript.

## The stack

| Job | Tool | Why |
| --- | --- | --- |
| Reference management | **Zotero** (free, open source) + **Better BibTeX** add-on | Citekeys, auto-exported `.bib`/CSL JSON, stable item keys, Obsidian integration |
| Import references & annotations | **Zotero Integration** plugin | Templated literature notes with metadata, abstract, annotations (with colours), links back to Zotero |
| Cite while writing | Zotero Integration's insert-citation, or **Citations** plugin, or plain Pandoc syntax `[@key]` | Pandoc resolves `[@key]` to any CSL style on export |
| PDF reading & annotation | **PDF++** (in Obsidian) or Zotero's reader (annotations import) | PDF++ writes highlights as links into your notes; Zotero keeps annotations in its DB |
| Writing | Obsidian, **Longform** for multi-file manuscripts | Chapter 24 |
| Export | **Pandoc** via the Pandoc plugin / Enhancing Export / Shell commands | DOCX, PDF (LaTeX), HTML, LaTeX with bibliography |
| Math | MathJax in notes, **Latex Suite** for speed | Chapter 3 |
| Figures | Excalidraw, Mermaid, or images from analysis tools | |
| Data & code | Link to repo/notebooks; do not store data in the vault | |

## Zotero setup

1. Install Zotero and the **Better BibTeX** (BBT) add-on.
2. BBT → citekey format, e.g. `auth.lower + year + shorttitle(1,1).lower` → `newport2016deep`. Pin keys so they never change.
3. Right-click your library (or a collection) → *Export Library* → format **Better CSL JSON** (or Better BibLaTeX), tick **Keep updated**, save outside the vault (e.g. `~/Zotero/library.json`). This auto-updating export is what Pandoc reads.
4. Zotero's PDF reader: annotate (highlight colours, notes, image areas); annotations are stored in Zotero and imported by the plugin.
5. Optional: install CSL styles you need; the **Zotero Connector** browser extension for one-click saving of papers.

Colour convention for highlights, so the import template can sort them:

| Colour | Meaning |
| --- | --- |
| Yellow | Key claim / result |
| Green | Method / definition |
| Blue | Connection to my work |
| Red | Disagreement / limitation |
| Purple | Quote worth citing verbatim |

## Zotero Integration plugin

Settings: **Database** = Zotero; **Citation formats**: add one (name `pandoc`, format *Pandoc* → produces `[@key]`) and one formatted-bibliography format; **Import formats**: add "Literature note" with output path `Sources/Papers/{{citekey}}.md`, image output path `Attachments/zotero/`, and a template file (Nunjucks templating):

```markdown
---
type: source
medium: paper
citekey: {{citekey}}
title: "{{title | replace('"', "'")}}"
author: [{% for a in creators %}"[[{{a.firstName}} {{a.lastName}}]]"{% if not loop.last %}, {% endif %}{% endfor %}]
year: {{date | format("YYYY")}}
journal: "{{publicationTitle}}"
doi: {{DOI}}
url: {{url}}
zotero: {{desktopURI}}
status: to-read
rating:
topics: []
tags: [{% for t in allTags %}{{t.tag | replace(" ", "-")}}{% if not loop.last %}, {% endif %}{% endfor %}]
---
> [!abstract]- Abstract
> {{abstractNote}}

[Open in Zotero]({{desktopURI}}) · {% if pdfLink %}[PDF]({{pdfLink}}){% endif %}

## Summary (own words)


## Key claims
{% for a in annotations %}{% if a.color == "#ffd400" %}- {{a.annotatedText}} ([p. {{a.pageLabel}}]({{a.desktopURI}}))
{% endif %}{% endfor %}

## Methods & definitions
{% for a in annotations %}{% if a.color == "#5fb236" %}- {{a.annotatedText}} ([p. {{a.pageLabel}}]({{a.desktopURI}}))
{% endif %}{% endfor %}

## Connections to my work
{% for a in annotations %}{% if a.color == "#2ea8e5" %}- {{a.annotatedText}} ([p. {{a.pageLabel}}]({{a.desktopURI}})){% if a.comment %} — *{{a.comment}}*{% endif %}
{% endif %}{% endfor %}

## Limitations / disagreements
{% for a in annotations %}{% if a.color == "#ff6666" %}- {{a.annotatedText}} ([p. {{a.pageLabel}}]({{a.desktopURI}}))
{% endif %}{% endfor %}

## Quotes
{% for a in annotations %}{% if a.color == "#a28ae5" %}> {{a.annotatedText}} ([p. {{a.pageLabel}}]({{a.desktopURI}}))
{% endif %}{% endfor %}

## Images
{% for a in annotations %}{% if a.imageRelativePath %}![[{{a.imageRelativePath}}]]
{% if a.comment %}{{a.comment}}{% endif %}
{% endif %}{% endfor %}

## Notes
{% persist "notes" %}

{% endpersist %}
```

`{% persist %}` blocks survive re-imports: re-running the import after adding annotations in Zotero updates the annotation sections but keeps your notes. Each annotation links back to the exact page in Zotero (`zotero://open-pdf/…`).

Commands: *Zotero Integration: Literature note* (pick an item from the Zotero picker; creates/updates the note), *Insert citation (pandoc)* (inserts `[@newport2016deep]`), *Insert bibliography*. Hotkey the first two.

## Reading and annotating inside Obsidian (PDF++)

If you prefer to read in Obsidian: keep the PDF in `Attachments/papers/`, open it (PDF++ enhances the built-in viewer), select text → *Copy link to selection* → paste into your literature note: `[[paper.pdf#page=4&selection=12,0,14,20|highlight text]]`. Clicking the link opens the PDF at the highlight. PDF++ can also write highlights into the PDF file, colour-code them, show backlinks *from* the PDF to your notes, and embed page regions as images. Zotero and PDF++ coexist well: Zotero for the library and metadata, PDF++ for reading sessions with notes and PDF side by side.

## Literature review workflow

1. **Search & collect** in Zotero (connector, database exports). Collections per project/theme.
2. **Triage**: skim abstract; tag `to-read` / `skip`. Import only `to-read` items to Obsidian.
3. **Read & annotate** with the colour convention.
4. **Import** → literature note with sorted annotations. Write the **own-words summary** immediately (five minutes; the step everyone skips and regrets).
5. **Extract claims** into idea notes (`Notes/`), each with `sources: ["[[citekey]]"]`. A claim supported by several papers links to all of them — synthesis emerging.
6. **Synthesis matrix**: add properties to the literature notes (`method`, `sample`, `finding`, `quality`) and view them as a Base:

```yaml
filters:
  and: [type == "source", medium == "paper", topics.contains(link("Attention Restoration"))]
views:
  - type: table
    name: Matrix
    order: [file.name, year, method, sample, finding, quality, rating]
    sort: [{property: year, direction: ASC}]
```

7. **Map**: `Maps/<Topic> MOC.md` organizes the idea notes into an argument — themes, tensions, gaps. The gaps section is your research question.
8. **Write** the review from the MOC: outline = MOC headings; paragraphs = idea notes rewritten for the audience; citations = `[@key]` from the `sources` properties.

## Writing with citations

Pandoc citation syntax inside notes:

```markdown
Attention is a limited resource [@kahneman1973attention, p. 12; see also @newport2016deep].
As @kahneman1973attention argues, ...
[-@kahneman1973attention] (year only)
```

Export resolves them with a CSL style and appends the bibliography. While writing, hover previews do not resolve `@keys`; Zotero Integration's picker and a `Sources/Papers/` Base sorted by author help you find them. Convention for drafts: `[[newport2016deep]] [@newport2016deep]` (wikilink for navigation, key for export) with the wikilinks stripped by a filter on export — or keep manuscripts wikilink-free.

## Export with Pandoc

Install Pandoc (and a LaTeX distribution for PDF — TinyTeX is enough). Then the **Pandoc plugin** (export current note to DOCX/PDF/HTML/LaTeX/EPUB with a configured bibliography and CSL), **Enhancing Export** (more options, templates, batch), or **Shell commands** with:

```bash
pandoc "{{file_path:absolute}}" -o "{{file_path:absolute:noext}}.docx" \
  --citeproc --bibliography ~/Zotero/library.json --csl ~/csl/apa.csl \
  --reference-doc ~/templates/journal.docx --lua-filter ~/filters/obsidian-links.lua
```

Handling Obsidian syntax on export:

- **Wikilinks** → a Lua filter strips or converts them, or keep manuscripts wikilink-free.
- **Embeds** `![[section]]` → Longform's compile step or a preprocessing script expands them.
- **Callouts** → become blockquotes; acceptable, or filter them.
- **Highlights** `==x==` → `-f markdown+mark` or strip.
- **Images** `![[fig.png|400]]` → `![](Attachments/fig.png){width=400px}` via filter, or write Markdown image syntax in manuscripts.
- **Math** and **footnotes** work as-is.
- **Cross-references** (figures, sections, equations): `pandoc-crossref` (`{#fig:one}`, `[@fig:one]`).

Keep a `Templates/pandoc/` folder with the reference DOCX (styles), CSL files, and filters; they are part of the vault.

## Thesis / long manuscript structure

```text
Projects/PhD Thesis/
├── Thesis.md                 ← hub: outline, status, deadlines, supervisor meetings (Base), decision log
├── Chapters/
│   ├── 01 Introduction.md
│   ├── 02 Literature Review.md
│   ├── 03 Methods.md
│   ├── 04 Results.md
│   ├── 05 Discussion.md
│   └── 06 Conclusion.md
├── Data notes/               ← what each dataset is, where it lives, how processed (not the data)
└── (Longform project index)
```

- **Longform** manages chapter order, per-scene word counts and targets, and compiles to a single document with front matter — then Pandoc. Daily word goals with visible progress.
- Chapter notes embed idea notes' blocks during drafting; rewrite to prose before submission.
- `Thesis.md` holds a Base of `type: meeting` with `project: "[[PhD Thesis]]"`, a Tasks query for the project, milestones with due dates, and a **decision log** (why this method, why this framing) — reviewers ask, and future-you forgets.
- Versioning: Git (Chapter 26) with a tag per submitted draft; File recovery/Sync for minute-level history.

## Experiments, lab notebooks, fieldwork

- One note per experiment/session: `type: experiment`, `date`, `project`, `hypothesis`, `protocol` (link), `status`, `outcome`. Body: setup, timestamped observations, results (tables, embedded figures), interpretation, next steps.
- Protocols as versioned notes; experiments link to the version used.
- `Experiments.base` grouped by project with outcome and date.
- Data lives in a proper store (repo, LabArchives, S3); the note holds paths/URLs and checksums.
- Fieldwork: mobile daily notes with a `location` property (Share Sheet / Map View) and photos; Bases map view later.

## Collaboration with non-Obsidian colleagues

- Export DOCX for tracked changes; bring comments back manually (or `pandoc --track-changes=all` on the way in).
- Publish site or Quartz garden for read-only access to your notes (Chapter 31).
- Zotero group libraries for shared references; Obsidian notes stay yours.
- Overleaf for LaTeX-first co-authoring: write in Obsidian, export LaTeX, paste; or keep the paper in Overleaf and only the *thinking* in Obsidian. Do not fight the co-authors' tool.

## Research dashboard

```markdown
## Reading queue (papers)
![[Papers.base#To read]]
## Recently imported
![[Papers.base#Recent]]
## Claims with a single source
(Dataview: type = note AND length(sources) < 2 AND contains(topics, [[This Topic]]))
## Manuscript status
(Longform word counts; Tasks: path includes "PhD Thesis")
## Supervisor meetings
![[Meetings.base#By project]]
## Deadlines
(Tasks: path includes "PhD Thesis", has due date, sort by due)
```

## Key takeaways

- Zotero + Better BibTeX is the reference backbone; Zotero Integration imports templated literature notes with colour-sorted annotations that link back to the exact PDF page; `{% persist %}` keeps your notes across re-imports.
- Read with a colour convention, write the own-words summary immediately, extract claims into idea notes with `sources`, build a synthesis matrix as a Base, and let the MOC become the review's outline.
- Cite with `[@key]`; export with Pandoc plus a Lua filter for wikilinks/embeds and a reference DOCX/CSL; Longform compiles multi-file manuscripts.
- Theses are projects with chapter notes, a hub holding meetings/tasks/decisions, and Git tags per draft.
- Experiments are typed notes pointing at data stored elsewhere; collaborators get exports, Publish sites or Zotero groups — not your vault.

## Next

[Chapter 19: Work and Career →](19-work-and-career.md)
