# Publishing and Sharing

Sooner or later some of the vault wants out: a digital garden of idea notes, a documentation site, a blog, a PDF for a colleague, a shared reading list, a slide deck. Because everything is Markdown, there are many exits — the official Obsidian Publish service, free static-site generators that understand wikilinks, Pandoc for documents, and simple copy-paste. This chapter compares them, walks through the two best free setups (Quartz and Digital Garden), covers export to PDF/DOCX/HTML, slides, and sharing single notes, and ends with the privacy checklist that must precede any publishing.

## Before anything: the boundary

Publishing is the one operation where a mistake is irreversible (search engines cache). Establish the boundary first:

1. **Allow-list, never deny-list.** Publish only notes with `publish: true` (Obsidian Publish honours this property; Quartz/Digital Garden/Enveloppe can be configured to). A deny-list (`Journal/` excluded) fails the first time a private note lands in the wrong folder.
2. **Never publish**: `Journal/`, `Mind/`, `People/`, `Health/`, `Finance/`, `Work/`, `Life/Admin/`, attachments of those.
3. **Check links and embeds**: a public note that embeds `![[Private Note#section]]` publishes that section. Publish tools warn about links to unpublished notes; read the warnings.
4. **Scrub properties**: your schema may include fields you do not want public (`confidence`, `rating` of a person…). Publishing tools can hide frontmatter; verify.
5. **Search the built site** for names and words that should not be there before announcing it.

## Options compared

| Option | Cost | Setup | Wikilinks / embeds | Graph / backlinks / search | Custom domain | Password | Best for |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Obsidian Publish** | ~$8/mo per site (annual) | Minutes; in-app | Full, native | Yes, all | Yes | Yes | Zero-maintenance digital garden or docs; funds Obsidian |
| **Quartz** | Free (GitHub Pages/Cloudflare/Vercel) | 30–60 min; Node + Git | Full (Obsidian flavour, callouts, Mermaid, Bases embeds not rendered) | Graph, backlinks, full-text search, popovers | Yes | No (add via Cloudflare Access) | Best free garden; beautiful; actively maintained |
| **Digital Garden plugin** | Free (Netlify/Vercel) | 20 min; one-click template | Good | Backlinks, graph, search | Yes | No | Simplest free option; publish from inside Obsidian per note |
| **Enveloppe** (→ Hugo/Jekyll/Astro/11ty/MkDocs…) | Free | Depends on SSG | Converts to the SSG's syntax | Depends | Yes | Depends | You already run a static site |
| **MkDocs Material** | Free | 30 min; Python | Via plugins (roamlinks/wikilinks); callouts as admonitions | Search; no graph | Yes | No | Documentation sites (this guide uses it) |
| **Flowershow**, **Perlite**, **Obsidian Web** | Free/varies | Varies | Good | Varies | | | Alternatives with Obsidian-first rendering |
| **Export PDF / DOCX / HTML** | Free | Per document | Resolved at export | n/a | n/a | n/a | Documents for humans |
| **Slides / Advanced Slides** | Free | Per note | Yes | n/a | | | Presentations |
| **Share a note as image / text** | Free | Instant | Rendered | n/a | | | Social, chat |

## Obsidian Publish

Turn on the core plugin, buy a site, choose a site slug (or custom domain). The Publish panel lists changed/new/deleted files with checkboxes; `publish: true` (or per-site "automatically publish" folder rules) preselects. Options: navigation sidebar, search, graph, backlinks, table of contents, reading-time, hover previews, custom CSS (`publish.css` at vault root), custom JS (`publish.js`, paid tier), password protection, `permalink`/`description`/`image`/`cover` properties for URLs and social cards, `publish: false` to exclude, RSS feed. It renders everything Obsidian renders — callouts, Mermaid, embeds, Dataview is **not** executed (static results only; Bases embeds likewise not rendered; paste static tables or use Publish-compatible plugins that bake output). The CLI (`publish:add changed`, `publish:status`) scripts it. Right for people who want a garden with no maintenance and are happy to pay.

## Quartz

Quartz (jackyzha0/quartz, v4) is a Node-based SSG designed for Obsidian vaults: wikilinks, embeds, callouts, Mermaid, LaTeX, highlights, tags, folder pages, backlinks, graph view, full-text search, popovers, dark mode, RSS, sitemap, OG images, comments (giscus), analytics — all as configurable plugins.

Setup:

```bash
git clone https://github.com/jackyzha0/quartz.git my-garden && cd my-garden
npm i
npx quartz create        # choose "Symlink" or "Copy" pointing at a folder of publishable notes
```

Point `content/` at a **publish folder** rather than the whole vault — either a symlink to a `Public/` folder in your vault, or a script that copies notes with `publish: true` (a 20-line Python/Node script, or Enveloppe, or Quartz's own `ExplicitPublish` filter plugin which honours `publish: true` across the whole vault — the safer allow-list approach; then `content/` can symlink the vault). Configure `quartz.config.ts` (site title, base URL, theme, plugins) and `quartz.layout.ts` (sidebar components). Build and preview: `npx quartz build --serve`. Deploy: `npx quartz sync` pushes to GitHub; a provided GitHub Actions workflow publishes to GitHub Pages; or Cloudflare Pages/Vercel/Netlify build from the repo. Custom domain via the host.

Notes: Quartz renders Obsidian Markdown faithfully but does **not** execute Dataview/Bases; bake dynamic content (a script that runs `obsidian base:query format=md` and writes a static table before build — the CLI makes this easy). Keep attachments the public notes need in the published tree; avoid publishing your whole `Attachments/` folder.

## Digital Garden plugin

Install the plugin; click "Deploy" on the template repo (creates a GitHub repo + Netlify/Vercel site from an 11ty template); paste a GitHub token and repo name into the plugin. Then per note: set `dg-publish: true` (and optionally `dg-home: true` for the landing page, `dg-permalink`, `dg-hide`, `dg-pinned`), and run *Digital Garden: Publish single note* or *Publish multiple notes*. The plugin pushes Markdown to the repo; the host rebuilds. Features: backlinks, graph, search, themes (uses your Obsidian theme's CSS optionally), Dataview **is** rendered at publish time (the plugin bakes query results), Excalidraw, transclusions. The least technical free option and the only free one that bakes Dataview for you.

## Enveloppe (formerly Obsidian Publisher)

For people who already run Hugo/Jekyll/Astro/Eleventy/Docusaurus/MkDocs: Enveloppe pushes selected notes (by property or folder) to a GitHub repo, converting wikilinks to Markdown links, moving attachments, rewriting paths, optionally converting callouts and Dataview output to static text. Configure the repo, branch, folder mapping, and conversion rules once; publish from the file menu. Your SSG does the rest.

## MkDocs Material

Documentation-style sites (this guide is one): Python `mkdocs` with the Material theme, `docs/` as source, GitHub Pages via `mkdocs gh-deploy` or Actions. Obsidian compatibility: use Markdown links (or the `mkdocs-roamlinks`/`mkdocs-ezlinks` plugins for wikilinks), callouts map to admonitions with a small conversion (or the `mkdocs-callouts` plugin), Mermaid works via `pymdownx.superfences`. Best when the output is a *manual* rather than a garden.

## Exporting documents

**PDF**: *Export to PDF* command (Chromium rendering of Reading view; options for page size, margins, downscale; uses print CSS — Chapter 28). Good for single notes; Mermaid renders (1.10 fixed PDF Mermaid export). For multi-note documents, Longform compile → one note → PDF, or Pandoc.

**DOCX / HTML / LaTeX / EPUB**: **Pandoc** (Chapter 18 for citations). Pandoc plugin: right-click → Export as → format. Enhancing Export: templates, batch, Lua filters for wikilinks/embeds/callouts, custom commands. Shell commands: full control.

```bash
pandoc note.md -o note.docx --reference-doc=styles.docx --lua-filter=wikilinks.lua --resource-path=.:Attachments
pandoc note.md -o note.html -s --embed-resources --css=export.css
```

**Rich text copy**: 1.12+ copies HTML to the clipboard from the editor; paste into Google Docs/Word/email keeps headings, lists, bold, links. For quick sharing this beats exporting.

**Markdown copy**: *Copy* in Reading view with no selection copies the note source (1.10+). Or the raw file.

## Slides

**Slides** (core): `---` between slides; *Start presentation*. Minimal. **Advanced Slides**: reveal.js with themes, layouts (`<grid>`), fragments, speaker notes and view, background images, embeds, export to HTML/PDF, live preview. Write talks as notes (with idea notes embedded), present from Obsidian, export the HTML deck to share. Canvas "zoom to next group" is a third, informal option for walkthroughs.

## Sharing single notes and snippets

- **Screenshot/image**: **Obsidian Share as Gist**, **Share Note** (uploads an encrypted rendered copy with a link), or export PDF; **Image Export**-type plugins render a note to PNG for social posts.
- **Share Note plugin**: one command → public URL of the rendered note (with theme), optionally encrypted; delete when done. The fastest way to send someone a note.
- **GitHub Gist**: the Share as Gist plugin; renders Markdown on GitHub (wikilinks show raw).
- **Publish password-protected site** for a small audience.
- **Print** for the person who wants paper.

## Sharing a vault or folder with people

Collaborative editing: a **shared vault** via Obsidian Sync (multiple users, Plus), Git (collaborators), LiveSync (shared DB), Remotely Save (shared bucket). Works for asynchronous collaboration with clear ownership of notes; not for simultaneous editing of the same paragraph. Structure shared vaults exactly like personal ones (skeleton + templates) so collaborators inherit conventions; add a `README.md`/`Vault Guide.md` at the root.

Read-only: Publish or Quartz with Cloudflare Access (email allow-list) in front for a private garden; or export.

## Publishing workflow that stays safe

1. Notes destined for publication live anywhere but carry `publish: true` (or `dg-publish: true`), set deliberately — never by template default.
2. A `Public.base` view (`publish == true`) is your publication list; review it monthly.
3. Before pushing: run the publish tool's unpublished-links check; grep the output folder for forbidden folder names and personal names (a Shell command or a script).
4. Publish tool with an allow-list filter (Publish's property, Quartz `ExplicitPublish`, Digital Garden's flag, Enveloppe's property filter).
5. After publishing: open the live site in a private window; use the site's search for names/words that should not be there.
6. Keep the site repo separate from the vault repo (if you version both) so vault history never leaks via Git.

## Digital gardening practices

- **Maturity labels** on notes (`status: seedling/budding/evergreen`) shown on the page — readers know what is tentative.
- **Dates**: `created` and a "last tended" (`file.mtime` rendered) per note.
- **No pressure to finish**: gardens are explicitly unfinished; the value is thinking in public.
- **Link generously within the garden**; keep private links private (the tool will strip them or show them as plain text — check).
- **An index/MOC as the home page**, a "start here", an "about this garden" explaining the labels.
- **RSS** so people can follow; a "recently tended" list.
- **Comments** (giscus via GitHub Discussions) or an email — the conversations are the reward.

## Key takeaways

- Establish an allow-list boundary (`publish: true`) before publishing anything; never publish the journal, mind, people, health, finance, work or admin folders; check embeds and links; search the live site.
- Obsidian Publish for zero-maintenance; Quartz for the best free garden; Digital Garden for the simplest free path (and baked Dataview); Enveloppe to feed an existing static site; MkDocs Material for manuals.
- Pandoc (with Lua filters) for DOCX/HTML/LaTeX; Export to PDF for single notes; rich-text copy for quick sharing; Share Note for one-off links; Advanced Slides for talks.
- Shared vaults work for asynchronous collaboration with conventions; read-only sharing via Publish/Quartz with access control.
- Gardens are unfinished by design: label maturity, show dates, start with a MOC, offer RSS and a way to talk.

## Next

[Chapter 32: Performance, Maintenance and Troubleshooting →](32-performance-maintenance-troubleshooting.md)
