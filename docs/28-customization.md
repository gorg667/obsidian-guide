# Customization — Themes, CSS and Layout

Obsidian's interface is HTML and CSS, which means everything about how it looks is changeable — from a theme you install in one click to a five-line snippet that hides a folder or colours a callout. Customization is partly aesthetics and partly ergonomics: a vault you enjoy looking at is a vault you open. This chapter covers themes worth using, Style Settings, the CSS snippet mechanism with thirty ready-to-paste snippets, per-note styling with `cssclasses`, the 1.13 callout colour change, fonts, icons, and workspace tuning.

## Themes

Settings → Appearance → Themes → *Manage*. Themes are CSS files in `.obsidian/themes/<Name>/theme.css` plus a manifest. One theme active at a time; snippets layer on top.

| Theme | Character | Notes |
| --- | --- | --- |
| **Default** | Clean, neutral, always compatible | Underrated. With a few snippets it is excellent. Migrated to OKLCH colours in 1.13. |
| **Minimal** (kepano) | Refined, minimalist, hugely configurable via Style Settings + the *Minimal Theme Settings* plugin (colour schemes, line widths, image grids, table/checkbox styles, focus mode) | The most popular power-user theme; maintained by Obsidian's CEO. |
| **AnuPpuccin** | Catppuccin colours, rainbow folders, alternate checkboxes, colourful callouts, many layout toggles | Pretty and very configurable; heavier CSS. |
| **Things** | Inspired by the Things app; light, friendly, good checkboxes | Simple and warm. |
| **Border** | Bordered panes, colourful, many Style Settings options | Distinctive. |
| **Catppuccin**, **Tokyo Night**, **Nord**, **Dracula**, **Rosé Pine**, **Everforest** | Colour-scheme ports | Choose to match your terminal/editor. |
| **Prism**, **ITS Theme**, **Primary**, **Shimmering Focus**, **Blue Topaz** | Feature-rich; some add callout types, banners, layouts | Powerful; check maintenance status. |

Advice: start with **Minimal** or **Default** plus snippets. Themes that add many features tend to break with Obsidian updates; the theme's GitHub activity is the health signal.

## Style Settings

The **Style Settings** plugin gives themes and snippets a settings UI: colours, toggles, sliders, fonts, defined by the theme author. Install it before Minimal/AnuPpuccin — without it, most of their options are unreachable.

## CSS snippets

Settings → Appearance → CSS snippets → open the folder (`.obsidian/snippets/`) → drop `.css` files → toggle each on. Snippets apply on top of the theme; they reload instantly; they sync with the vault. Disabling a snippet properly removes styles from pop-out windows (1.13).

### How to find selectors

++ctrl+shift+i++ opens the developer tools; the element picker shows the class of anything you click. Obsidian's CSS variables (`--text-normal`, `--background-primary`, `--accent-h/s/l`, `--font-text-size`, `--callout-color`, …) are documented at docs.obsidian.md → CSS variables, and the CLI has `obsidian dev:css selector=".markdown-preview-view" prop=color` for querying computed styles. Prefer variables over hardcoded values so light/dark modes and themes keep working.

### The snippet library

**Layout and chrome**

```css
/* 01 Hide the status bar */
.status-bar { display: none; }
```

```css
/* 02 Hide the ribbon (use hotkeys) */
.workspace-ribbon.mod-left { display: none; }
```

```css
/* 03 Wider readable line length (default ~700px) */
.markdown-source-view.mod-cm6.is-readable-line-width .cm-sizer,
.markdown-preview-view.is-readable-line-width .markdown-preview-sizer {
  max-width: 880px;
}
```

```css
/* 04 Per-note full width via cssclasses: [wide] */
.wide .markdown-source-view.mod-cm6.is-readable-line-width .cm-sizer,
.wide .markdown-preview-view.is-readable-line-width .markdown-preview-sizer {
  max-width: 100%;
}
```

```css
/* 05 Hide the inline title on notes with cssclasses: [no-title] */
.no-title .inline-title { display: none; }
```

```css
/* 06 Compact file explorer */
.nav-file-title, .nav-folder-title { padding-top: 2px; padding-bottom: 2px; }
.nav-file-title-content, .nav-folder-title-content { font-size: 0.9em; }
```

```css
/* 07 Hide specific folders in the explorer (Templates, Attachments) */
.nav-folder-title[data-path="Templates"],
.nav-folder-title[data-path="Templates"] + .nav-folder-children,
.nav-folder-title[data-path="Attachments"],
.nav-folder-title[data-path="Attachments"] + .nav-folder-children { display: none; }
```

```css
/* 08 Colour folders by name */
.nav-folder-title[data-path^="Projects"] { color: #10b981; }
.nav-folder-title[data-path^="Journal"]  { color: #94a3b8; }
.nav-folder-title[data-path^="People"]   { color: #f59e0b; }
.nav-folder-title[data-path^="Mind"]     { color: #a78bfa; }
```

```css
/* 09 Dim the tab bar until hovered */
.workspace-tab-header-container { opacity: 0.5; transition: opacity .2s; }
.workspace-tab-header-container:hover { opacity: 1; }
```

**Typography**

```css
/* 10 Heading sizes and weights (modest hierarchy) */
.markdown-preview-view h1, .cm-header-1 { font-size: 1.7em; font-weight: 700; }
.markdown-preview-view h2, .cm-header-2 { font-size: 1.4em; font-weight: 650; }
.markdown-preview-view h3, .cm-header-3 { font-size: 1.15em; font-weight: 600; }
.markdown-preview-view h4, .cm-header-4 { font-size: 1em; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
```

```css
/* 11 Coloured headings */
.cm-header-2, .markdown-preview-view h2 { color: var(--color-purple); }
.cm-header-3, .markdown-preview-view h3 { color: var(--color-blue); }
```

```css
/* 12 Serif body for reading-heavy vaults */
body { --font-text: "Source Serif 4", "Iowan Old Style", Georgia, serif; }
```

```css
/* 13 Justified text in Reading view */
.markdown-preview-view p { text-align: justify; hyphens: auto; }
```

```css
/* 14 Highlight colour */
.markdown-preview-view mark, .cm-highlight { background: rgba(250, 204, 21, .35); color: inherit; }
```

```css
/* 15 Blockquote as a left-accent bar */
.markdown-preview-view blockquote, .cm-quote { border-left: 3px solid var(--interactive-accent); font-style: normal; }
```

**Links and tags**

```css
/* 16 Distinguish unresolved links */
.cm-s-obsidian span.cm-hmd-internal-link.is-unresolved, .markdown-preview-view a.internal-link.is-unresolved {
  opacity: .6; text-decoration: underline dotted;
}
```

```css
/* 17 Tags as pills */
.tag, .cm-hashtag { background: var(--background-modifier-hover); border-radius: 999px; padding: 0 .5em; font-size: .85em; text-decoration: none; }
```

```css
/* 18 Colour specific tags (Reading view) */
a.tag[href="#waiting"] { background: #fde68a; color: #78350f; }
a.tag[href="#urgent"]  { background: #fecaca; color: #7f1d1d; }
a.tag[href^="#habit/"] { background: #bbf7d0; color: #14532d; }
```

**Callouts** (1.13 change: `--callout-color` takes a full CSS colour, not an RGB triplet)

```css
/* 19–21 Custom callouts */
.callout[data-callout="decision"] { --callout-color: #7c3aed; --callout-icon: lucide-gavel; }
.callout[data-callout="person"]   { --callout-color: #f59e0b; --callout-icon: lucide-user; }
.callout[data-callout="money"]    { --callout-color: #10b981; --callout-icon: lucide-wallet; }
/* 22 Quieter default callouts */
.callout { background: color-mix(in oklch, var(--callout-color) 8%, transparent); }
```

```css
/* 23 Callout without title bar: > [!note|no-title] */
.callout[data-callout-metadata~="no-title"] .callout-title { display: none; }
```

**Tasks and lists**

```css
/* 24 Dim and strike completed tasks */
.markdown-preview-view .task-list-item.is-checked { opacity: .55; }
.markdown-preview-view .task-list-item.is-checked .task-list-item-text { text-decoration: line-through; }
```

```css
/* 25 Basic custom checkbox statuses (themes do more) */
li[data-task="-"] .task-list-item-text { text-decoration: line-through; opacity: .5; }
li[data-task="!"] > input { border-color: #ef4444; }
li[data-task="/"] > input { background: linear-gradient(90deg, var(--interactive-accent) 50%, transparent 50%); }
```

```css
/* 26 Tighter lists */
.markdown-preview-view ul, .markdown-preview-view ol { margin-block: .2em; }
.markdown-preview-view li { margin-block: .1em; }
```

**Tables, images, code**

```css
/* 27 Striped, compact tables with sticky header */
.markdown-preview-view table { font-size: .9em; }
.markdown-preview-view tbody tr:nth-child(even) { background: var(--background-secondary); }
.markdown-preview-view th { position: sticky; top: 0; background: var(--background-primary); }
```

```css
/* 28 Image grid for notes with cssclasses: [gallery] */
.gallery .markdown-preview-view p:has(> img + img) { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 8px; }
.gallery .markdown-preview-view p:has(> img + img) img { width: 100%; height: 200px; object-fit: cover; border-radius: 6px; }
```

```css
/* 29 Rounded, bordered images */
.markdown-preview-view img, .cm-content img { border-radius: 6px; border: 1px solid var(--background-modifier-border); }
```

```css
/* 30 Code block font size and line-height */
.markdown-preview-view pre, .cm-s-obsidian .HyperMD-codeblock { font-size: .85em; line-height: 1.5; }
```

**Dashboard styling** (`cssclasses: [dashboard]`)

```css
/* 31 Dashboard look */
.dashboard .inline-title { display: none; }
.dashboard .markdown-preview-view h2 { font-size: 1.05em; text-transform: uppercase; letter-spacing: .05em; color: var(--text-muted); border-bottom: 1px solid var(--background-modifier-border); }
.dashboard .bases-view { font-size: .9em; }
```

Multi-column layouts: the **Multi-Column Markdown** plugin, or Minimal's side-by-side callouts, or raw `<div>` grids (Markdown inside `<div>` renders in Reading view when separated by blank lines).

**Bases**

```css
/* 32 Denser Bases tables (class names may change between versions — inspect first) */
.bases-view .bases-table-cell { padding: 2px 6px; }
```

## Per-note styling with `cssclasses`

```yaml
---
cssclasses: [wide, no-title, dashboard]
---
```

Classes are added to the note's view container (editor and reading), so any snippet scoped `.classname …` applies to that note only. A standard set: `wide`, `no-title`, `dashboard`, `gallery`, `serif`, `print`. Minimal ships many built-ins (`wide-page`, `img-grid`, `table-max`, `cards` — which renders Dataview tables as cards).

## Fonts

Settings → Appearance → Font: interface, text, monospace. Fonts must be installed on each device (mobile uses system fonts plus installed profiles on iOS). Good text fonts for notes: Inter, iA Writer Quattro/Duo, Source Serif, Literata, Atkinson Hyperlegible; monospace: JetBrains Mono, Fira Code, IBM Plex Mono. Keep line-height ~1.5–1.6.

## Icons

**Iconize**: icons on folders and files (Lucide, FontAwesome, emoji, custom SVG packs), in the tab and inline title, with per-folder inheritance. Ten minutes on top-level folders pays back in scanning speed. Emoji in folder names also works without a plugin — `📥 Inbox`, `📅 Journal` — but complicates paths in queries (`file.inFolder("📥 Inbox")`). Iconize keeps paths clean.

## Workspace tuning

- **Default layout**: left sidebar File explorer + Search + Bookmarks; right sidebar Backlinks + Outline + Calendar + Properties (+ a sidebar Base for related items). Collapse sidebars when writing.
- **Stack tabs** for research; **pinned tabs** for Home and the weekly note; **pop-out** a reference note to a second monitor.
- **Workspaces** per mode (Chapter 2); switch via CLI or hotkeys.
- **Zoom**: ++ctrl+plus++/++ctrl+minus++ per window; Appearance → Zoom level for the base.
- **Hide UI you never use**: Commander removes ribbon/tab-bar/status items; snippets 01–02 hide bars entirely.
- **Window frame**: Appearance → Window frame style: *Hidden* for the cleanest look.

## Print and export styling

Export to PDF uses the theme's print CSS. A `print` snippet tunes typography for paper:

```css
@media print {
  .print .markdown-preview-view { font-size: 11pt; }
  .print .callout { break-inside: avoid; }
}
```

Export as PDF from the command palette (paper size, margins, downscale). For Word/HTML, Pandoc (Chapter 31).

## Debugging CSS

- Snippet not applying: `.css` extension, toggle on, no syntax error (devtools console shows warnings), specificity (theme may win — add a parent class or `!important` as a last resort).
- After Obsidian updates, check the changelog's *Developers* section for CSS variable changes (1.13: `--callout-color`, OKLCH base colours, `corner-shape`).
- Keep snippets small and named by purpose so you can toggle them individually.
- Theme + many snippets + many plugins = rendering slowness on mobile; test.

## Key takeaways

- Start from Default or Minimal with Style Settings; add small purpose-named CSS snippets rather than a heavy theme.
- The devtools element picker and Obsidian's CSS variables are all you need; prefer variables so themes and dark mode keep working.
- `cssclasses` gives per-note layouts (wide, dashboard, gallery, no-title) with zero plugins.
- Custom callouts (`--callout-color` as a full CSS colour since 1.13) and folder colours/icons give a vault identity and scanning speed.
- Tune the workspace and check the changelog's developer notes after updates.

## Next

[Chapter 29: Automation and Integrations →](29-automation-and-integrations.md)
