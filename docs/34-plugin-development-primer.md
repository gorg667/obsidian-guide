# Plugin Development Primer

At some point the plugin you want does not exist, or exists and does one thing wrong. Obsidian plugins are TypeScript, the API is well documented, the sample plugin builds in a minute, and — since 1.12 — the CLI lets you reload, inspect, screenshot and script the running app from the terminal, which makes the develop-test loop (and AI-assisted development) fast. This chapter is enough to go from zero to a working personal plugin, with pointers to the Bases view API and the settings API, and the steps to publish to the community directory.

## What a plugin is

A folder in `.obsidian/plugins/<id>/` containing `manifest.json` (id, name, version, minAppVersion, description, author, `isDesktopOnly`), `main.js` (compiled from your TypeScript), and optionally `styles.css` and `data.json` (settings). Obsidian loads `main.js`, instantiates your class extending `Plugin`, and calls `onload()`. Everything you can do is exposed through the `app` object: `app.vault` (files), `app.metadataCache` (links, tags, frontmatter, headings, blocks), `app.workspace` (leaves, views, active file), `app.fileManager` (rename with link updates, `processFrontMatter`), plus UI primitives (`Modal`, `Notice`, `Setting`, `SuggestModal`, `ItemView`, `MarkdownRenderer`, editor extensions via CodeMirror 6).

## Setup in ten minutes

1. Install Node.js (LTS).
2. Clone the sample: `git clone https://github.com/obsidianmd/obsidian-sample-plugin my-plugin` (or "Use this template" on GitHub) into a *test vault's* `.obsidian/plugins/my-plugin/`.
3. `npm install`, then `npm run dev` (esbuild watches and rebuilds `main.js`).
4. In Obsidian (test vault, Restricted mode off): Settings → Community plugins → enable "Sample Plugin". Or `obsidian plugin:enable id=my-plugin`.
5. Edit `main.ts`; on save, `obsidian plugin:reload id=my-plugin` (or the **Hot Reload** dev plugin reloads automatically when `main.js` changes).
6. `obsidian devtools` opens the console; `obsidian dev:errors` and `obsidian dev:console level=error` show what broke without leaving the terminal.

Read `docs.obsidian.md` → *Plugins* → Getting started, Anatomy of a plugin, then the API reference as needed. The `obsidian.d.ts` type definitions are the real documentation — hover in your editor.

## Anatomy: a small real plugin

A plugin that adds a command "Log contact" — pick a person, append a line to their note and to today's daily note, set `last_contact` — the mobile-friendly capture from Chapter 23, as a plugin instead of a Templater script.

```typescript
import { App, Plugin, PluginSettingTab, Setting, SuggestModal, TFile, Notice, moment } from "obsidian";

interface Settings { peopleFolder: string; dailyFolder: string; dateFormat: string; }
const DEFAULTS: Settings = { peopleFolder: "People", dailyFolder: "Journal/Daily", dateFormat: "YYYY-MM-DD" };

export default class LogContact extends Plugin {
  settings: Settings;

  async onload() {
    this.settings = Object.assign({}, DEFAULTS, await this.loadData());
    this.addCommand({
      id: "log-contact",
      name: "Log contact with a person",
      callback: () => new PersonPicker(this.app, this).open(),
    });
    this.addSettingTab(new LogContactSettings(this.app, this));
  }

  people(): TFile[] {
    return this.app.vault.getMarkdownFiles().filter(f => f.path.startsWith(this.settings.peopleFolder + "/"));
  }

  async log(person: TFile, text: string) {
    const today = moment().format(this.settings.dateFormat);
    // 1. set last_contact
    await this.app.fileManager.processFrontMatter(person, fm => { fm.last_contact = today; });
    // 2. append to the person note
    await this.app.vault.append(person, `\n- ${today} — ${text}`);
    // 3. append to the daily note (create if missing)
    const dailyPath = `${this.settings.dailyFolder}/${today}.md`;
    let daily = this.app.vault.getAbstractFileByPath(dailyPath);
    if (!(daily instanceof TFile)) daily = await this.app.vault.create(dailyPath, `---\ntype: daily\ndate: ${today}\n---\n`);
    await this.app.vault.append(daily as TFile, `\n- ${moment().format("HH:mm")} Contact with [[${person.basename}]]: ${text}`);
    new Notice(`Logged contact with ${person.basename}`);
  }

  async saveSettings() { await this.saveData(this.settings); }
}

class PersonPicker extends SuggestModal<TFile> {
  constructor(app: App, private plugin: LogContact) { super(app); this.setPlaceholder("Who did you talk to?"); }
  getSuggestions(q: string) { return this.plugin.people().filter(f => f.basename.toLowerCase().includes(q.toLowerCase())); }
  renderSuggestion(f: TFile, el: HTMLElement) { el.createEl("div", { text: f.basename }); }
  async onChooseSuggestion(f: TFile) {
    const text = await promptText(this.app, `Note about ${f.basename}`);
    if (text !== null) await this.plugin.log(f, text);
  }
}

class LogContactSettings extends PluginSettingTab {
  constructor(app: App, private plugin: LogContact) { super(app, plugin); }
  display() {
    const { containerEl } = this; containerEl.empty();
    new Setting(containerEl).setName("People folder").addText(t => t.setValue(this.plugin.settings.peopleFolder)
      .onChange(async v => { this.plugin.settings.peopleFolder = v; await this.plugin.saveSettings(); }));
    new Setting(containerEl).setName("Daily notes folder").addText(t => t.setValue(this.plugin.settings.dailyFolder)
      .onChange(async v => { this.plugin.settings.dailyFolder = v; await this.plugin.saveSettings(); }));
  }
}

// minimal text prompt modal
import { Modal } from "obsidian";
function promptText(app: App, title: string): Promise<string | null> {
  return new Promise(resolve => {
    const m = new (class extends Modal {
      onOpen() {
        this.titleEl.setText(title);
        const input = this.contentEl.createEl("input", { type: "text" }); input.style.width = "100%"; input.focus();
        input.addEventListener("keydown", e => { if (e.key === "Enter") { resolve(input.value); this.close(); } });
      }
      onClose() { resolve(null); }
    })(app);
    m.open();
  });
}
```

Fifty lines, and it works on mobile. The pattern — command → modal → vault/frontmatter operations → Notice — covers most personal plugins.

## The API you will use most

| Area | Calls |
| --- | --- |
| Files | `vault.getMarkdownFiles()`, `getFiles()`, `getAbstractFileByPath()`, `read()`/`cachedRead()`, `modify()`, `append()`, `create()`, `createFolder()`, `delete()`/`trash()`, `rename()` (prefer `fileManager.renameFile` to update links), `adapter.exists()`, `appendBinary()` (1.12) |
| Frontmatter | `fileManager.processFrontMatter(file, fm => {...})` — the only safe way to edit properties |
| Metadata | `metadataCache.getFileCache(file)` → `frontmatter`, `headings`, `links`, `embeds`, `tags`, `blocks`, `listItems`, `sections`; `resolvedLinks`, `unresolvedLinks`; `getFirstLinkpathDest(link, sourcePath)`; events `changed`, `resolved` |
| Workspace | `getActiveFile()`, `getLeaf(true).openFile(file)`, `activeEditor?.editor` (CodeMirror wrapper: `getSelection`, `replaceSelection`, `getCursor`, `getLine`, `setLine`), `registerView`, `getLeavesOfType`, `revealLeaf`, events `file-open`, `active-leaf-change`, `layout-ready` (`app.workspace.onLayoutReady`) |
| Commands | `addCommand({id, name, callback \| editorCallback \| checkCallback, hotkeys})` |
| UI | `Notice`, `Modal`, `SuggestModal`, `FuzzySuggestModal`, `Setting` (text, toggle, dropdown, slider, button, search), `Menu`, `ItemView` for sidebar/main panes, `MarkdownRenderer.render()` to render Markdown into an element, `addRibbonIcon`, `addStatusBarItem`, `registerMarkdownCodeBlockProcessor(lang, (source, el, ctx) => …)` (your own code blocks), `registerMarkdownPostProcessor` (Reading view transforms), `registerEditorExtension` (CM6) |
| Lifecycle | `registerEvent`, `registerDomEvent`, `registerInterval` — all auto-cleaned on unload; never leave timers/listeners unregistered |
| Settings | `loadData()`/`saveData()` → `data.json`; `PluginSettingTab`; 1.13 **declarative settings API** so your settings appear in the new searchable Settings (migration guide on docs.obsidian.md) |
| Secrets | **Keychain** (1.11+) via the secret storage API — store API keys there, not in `data.json` |
| Network | `requestUrl()` (CORS-free) rather than `fetch` |
| Mobile | `Platform.isMobile`, `isDesktopOnly` in manifest if you use Node/Electron APIs |

## Bases view API (1.10+)

Plugins can register **new view types for Bases** — the official **Maps** plugin is the reference implementation. Sketch:

```typescript
this.registerBasesView("my-timeline", {
  name: "Timeline",
  icon: "calendar-range",
  factory: (controller, containerEl) => new TimelineView(controller, containerEl),
  options: (config) => ([ /* view option definitions shown in the view settings UI */ ]),
});
```

Your view class receives the query results (files with their evaluated properties/formulas) and renders them; it re-renders on data change; it can read/write its own keys in the view config (that is how Maps stores lat/long property names). Note the 1.12 breaking change: `BaseOption#shouldHide` no longer receives the config — read options from `BasesViewRegistration.options`. Ideas worth building: timeline, calendar, gallery with lightbox, chart (bar/line from a numeric property), tree by a parent link, gantt from start/due.

## Code block processors — the cheapest custom "view"

For personal use, a code block processor is often enough and much simpler than a view:

```typescript
this.registerMarkdownCodeBlockProcessor("streak", async (source, el, ctx) => {
  const tag = source.trim();                       // e.g. #habit/meditate
  const files = this.app.vault.getMarkdownFiles().filter(f => f.path.startsWith("Journal/Daily/")).sort((a,b) => b.basename.localeCompare(a.basename));
  let streak = 0;
  for (const f of files) {
    const cache = this.app.metadataCache.getFileCache(f);
    const item = cache?.listItems?.find(li => li.task !== undefined && (cache.tags ?? []).some(t => t.tag === tag && t.position.start.line === li.position.start.line));
    if (item && item.task !== " ") streak++; else break;
  }
  el.createEl("strong", { text: `${tag}: ${streak}-day streak` });
});
```

Now ` ```streak\n#habit/meditate\n``` ` renders a live streak anywhere — a DataviewJS-free widget that also works with Dataview disabled.

## Testing with the CLI

```bash
obsidian plugin:reload id=my-plugin
obsidian dev:errors clear
obsidian command id=my-plugin:log-contact          # trigger your command
obsidian dev:screenshot path=/tmp/after.png         # what does it look like?
obsidian dev:dom selector=".my-plugin-view" text    # inspect rendered DOM
obsidian eval code="app.plugins.plugins['my-plugin'].settings"
obsidian dev:mobile on                               # emulate mobile layout
```

This loop is what makes AI-assisted plugin development practical: an agent edits `main.ts`, reloads, runs the command, reads `dev:errors`, screenshots, iterates — all from the terminal (Chapter 30). Add a test vault fixture (a few notes with known properties) in the repo.

## Good citizenship

- **Never block the UI**: async file operations; debounce on `metadataCache.on("changed")`.
- **Clean up**: use `register*` helpers so unload is complete (the "reload plugin" loop will show leaks fast).
- **Respect the vault**: modify frontmatter via `processFrontMatter`; rename via `fileManager`; do not write files on load without user action.
- **Mobile**: test with `dev:mobile on`; avoid Node modules unless `isDesktopOnly`.
- **Settings**: sensible defaults; migrate old settings shapes; use Keychain for secrets; adopt the declarative settings API so users can search your settings (1.13).
- **Styling**: use Obsidian CSS variables; scope your classes (`.my-plugin-…`); support light/dark.
- **Performance**: `cachedRead` over `read`; avoid scanning the whole vault on every keystroke; index once, listen for changes.
- **Security**: no remote code loading; no telemetry without opt-in; declare network use in the README (the review checks).

## Publishing to the community directory

1. Repo public on GitHub with `manifest.json`, `main.js`, `styles.css` (optional) attached to a **GitHub release** whose tag equals the manifest `version` (a GitHub Action in the sample repo builds and attaches them).
2. `README.md` with what it does, screenshots, settings, and any network/disk behaviour; `LICENSE` (MIT is conventional); `versions.json` mapping plugin versions to `minAppVersion`.
3. Follow the **developer policies** and **submission guidelines** (docs.obsidian.md): unique id (no "obsidian" in the name), no default hotkeys that clash, sentence-case UI text, no `innerHTML` with untrusted content, no `console.log` spam, async where required, mobile compatibility declared honestly.
4. Fork `obsidianmd/obsidian-releases`, add your entry to `community-plugins.json`, open a PR; an automated bot checks the release; a human reviews (days to weeks); address feedback.
5. Updates: bump `manifest.json` and `versions.json`, tag a release; Obsidian picks it up. Until accepted, users can install via **BRAT** with your repo URL.

## Themes and snippets as "plugins"

A theme is a repo with `theme.css` + `manifest.json`, submitted to `community-css-themes.json` the same way. Many "I wish Obsidian looked like…" needs are a snippet (Chapter 28), not a plugin; many "I wish Obsidian did…" needs are a Templater script or a code block processor. Reach for a full plugin when you need a command with UI, a view, an editor extension, or distribution to others.

## Key takeaways

- A plugin is a TypeScript class in `.obsidian/plugins/<id>/`; the sample repo, `npm run dev`, and `obsidian plugin:reload` give a fast loop; the CLI's dev commands (`dev:errors`, `dev:screenshot`, `dev:dom`, `eval`, `dev:mobile`) make testing — and agent-assisted development — practical.
- Most personal plugins are: command → modal → `vault`/`processFrontMatter` operations → Notice; code block processors are the cheapest custom widgets; Bases view API for new database views.
- Use `register*` for cleanup, `processFrontMatter` for properties, `fileManager` for renames, `requestUrl` for network, Keychain for secrets, the declarative settings API, and Obsidian CSS variables.
- Publish via a GitHub release + PR to `obsidian-releases` following the developer policies; BRAT for beta distribution.

## Next

[Chapter 35: The Mastery Roadmap →](35-mastery-roadmap.md)
