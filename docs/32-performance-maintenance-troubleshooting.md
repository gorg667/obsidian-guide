# Performance, Maintenance and Troubleshooting

A vault is a living system; like a garden or a codebase it needs light, regular maintenance or it rots — broken links accumulate, plugins conflict, dashboards slow down, the schema drifts. This chapter gives the maintenance calendar (weekly, monthly, quarterly, yearly), the performance rules for large vaults, a diagnostic procedure for when Obsidian misbehaves, and a table of common symptoms and their causes.

## The maintenance calendar

| Cadence | Tasks | Time |
| --- | --- | --- |
| **Weekly** (in the weekly review) | Inbox to zero; check plugin updates; skim `Meta/Automation Log`; resolve sync conflicts (search `conflict`) | 10 min |
| **Monthly** | Properties view scan for duplicates/typos; schema audit Base (missing `type`, stray `status` values); tags used once; attachments audit (largest, unused); File recovery sanity check; empty `.trash/` if older than 30 days | 20 min |
| **Quarterly** | Plugin audit (can you name what each does this quarter? disable the rest); templates trim; dashboards actually used?; archive `done` projects (move); reinstall the installer if behind; review CSS snippets after theme/Obsidian updates; export Bases to CSV as a fallback | 45 min |
| **Yearly** | Restore test from backup; rotate API keys; reread `Meta/Vault Guide.md` and update; migrate deprecated plugins (e.g. Dataview tables → Bases); Emergency & Legacy export; vault health report (orphans, unresolved, dead ends) | 2 h |

Put these as recurring tasks in `Routines.md` (`🔁 every month on the 1st`), and they surface in the Today view when due.

## Vault hygiene queries and commands

- **Unresolved links** (notes your vault wants): `obsidian unresolved counts` or Dataview's metadataCache script (Chapter 12). Create the top ones; fix typos for the rest.
- **Orphans** (no inlinks): `obsidian orphans`; a Base of `type == "note"` with `file.backlinks.length == 0` (expensive — run rarely) or the Dataview orphan query. Link them into a MOC or delete.
- **Dead ends** (no outlinks): `obsidian deadends`. Idea notes without outlinks are unfinished thinking.
- **Empty and stub notes**: Dataview `WHERE file.size < 200` excluding templates; or Search `-path:Templates` sorted by size (Novel Word Count plugin shows sizes in the explorer).
- **Untyped notes**: Schema audit Base (Chapter 10).
- **Duplicate titles across folders**: a DataviewJS grouping by `file.name` with `length(rows) > 1`.
- **Unused attachments**: Attachments audit Base "Possibly unused"; **Janitor** plugin (orphans, empties, big files, expired) for bulk deletion with confirmation; 1.12's delete-attachments prompt handles the incremental case.
- **Broken embeds/images**: Search `/!\[\[[^\]]+\]\]/` then eyeball; or a DataviewJS that checks `file.embeds` targets against the vault.
- **Tag hygiene**: Tags view sorted by count; Tag Wrangler to merge; property `tags` vs inline consistency.
- **Linter** on the whole vault once a quarter (with a Git commit before) to normalize headings, spacing, YAML order.

## Performance

Obsidian's own limits are high — tens of thousands of notes are fine — but the *sum* of plugins, queries, and attachments is what slows a vault. In order of impact:

1. **Community plugin count and weight.** Each plugin runs at startup; heavy ones (Dataview indexing, Excalidraw, Copilot/Smart Connections embeddings, Omnisearch indexing, Git polling) dominate. Rule: ≤ 25 plugins; on mobile ≤ 12 essential ones (many plugins offer a "disable on mobile" toggle; or keep mobile-specific `community-plugins.json` out of sync).
2. **Live queries per open note.** A dashboard with twenty DataviewJS blocks re-renders every few seconds. Move lists to Bases (lazy, indexed), cap dashboards at ~8 blocks, use `LIMIT`, avoid `file.inlinks` computations over the vault.
3. **Attachments.** Thousands of large images/PDFs slow indexing, sync, and search. Keep the vault under a few GB; compress images (Image Converter → WebP); large media outside the vault (Chapter 8).
4. **Huge single notes.** A 50k-word note with hundreds of embeds is slow to render; split (Note composer) or read in Reading view.
5. **Graph view** on 20k+ notes: filter (`path:`, `-path:Journal`) before opening; lower "text fade threshold"; disable tags/attachments.
6. **Sync method.** iCloud eviction and OneDrive files-on-demand cause stalls; Git on mobile is slow; Obsidian Sync and Remotely Save are light.
7. **Search index.** Omnisearch indexes PDFs/images via Text Extractor — turn off PDF indexing if you have thousands of PDFs.
8. **Installer version.** Newer Electron = faster rendering. Reinstall yearly (Chapter 2).
9. **Excluded files** (Settings → Files & links) reduce noise in search/suggesters but do *not* stop indexing; they help perceived performance in the switcher.
10. **Startup**: *Open daily note on startup* + Homepage loading a heavy dashboard = slow perceived start. Land on a light note.

Diagnostics: Developer tools → Console shows plugin load times at startup ("Plugin X loaded in N ms" with the debug flag in some builds; otherwise the *Performance* tab profile); `obsidian dev:console level=warn` and `dev:errors` from the CLI; Restricted mode toggles everything off for an A/B test in seconds.

## Troubleshooting procedure

When something is wrong (rendering glitch, command missing, note not saving, plugin error, slow app):

1. **Reload** (`obsidian reload`, or ++ctrl+r++ / *Reload app without saving* command). Fixes most transient glitches.
2. **Check the console** (++ctrl+shift+i++ → Console). Red errors usually name the plugin.
3. **Restricted mode** (Settings → Community plugins, or `obsidian plugins:restrict on`). If the problem vanishes, it is a plugin; since 1.13 you can exit Restricted mode without re-enabling all plugins — re-enable in halves until the culprit appears (bisecting 24 plugins takes 5 rounds).
4. **Disable CSS snippets and switch to the Default theme** for visual problems.
5. **Sandbox vault** (Help → *Open sandbox vault*): a clean vault to test whether the issue is in your configuration or in Obsidian.
6. **Check versions**: app vs installer (Settings → About); update both; read the changelog for breaking changes (e.g. 1.13 `--callout-color`, 1.10 removed light/dark commands).
7. **Check the files**: open the note in a plain text editor — YAML valid? Stray control characters? Merge conflict markers from Git (`<<<<<<<`)? Sync conflict copies?
8. **Check the index**: if links or properties look stale, close and reopen the vault — the metadata cache (stored in IndexedDB per vault, not in the folder) re-indexes on open and Obsidian offers a rebuild when it detects damage. For persistent cache weirdness: *Manage vaults* → remove the vault from the list (not the files) → open the folder again.
9. **File recovery / Sync history / Git** to recover damaged content (Chapter 26).
10. **Forum and plugin issue trackers**: search the exact error text; most have been seen.

## Common symptoms and causes

| Symptom | Likely cause → fix |
| --- | --- |
| Properties show a warning icon / render as text | Invalid YAML (unquoted `[[link]]`, colon in value, tab indentation, frontmatter not on line 1) → fix in Source mode |
| Property type mismatch (date shows as text) | Type set vault-wide for that name differs → Properties view → change type, or rename |
| Template variables not replaced (`{{date}}` literal) | Core Templates syntax processed by Templater (or vice versa) → convert template to one syntax; check Templater's "trigger on new file creation" |
| Templater folder template not applied | Folder path mismatch (case-sensitive) or file created by a plugin that bypasses creation hooks → check settings; some plugins need "Templater: replace templates in the active file" after creation |
| Dataview shows no results | `FROM` path/case wrong; property stored as string vs number; inline field not recognized (needs `::`); note in a folder Dataview cannot see (none exist; but Excluded files do not matter) |
| Bases view empty | Filter typo; expression starting with `!` unquoted; property name with hyphen needs `note["a-b"]`; date compared to string |
| Tasks query shows nothing | Global filter (e.g. `#task`) required and missing; tasks in code blocks; global query excluding the path |
| Links break after moving files | *Automatically update internal links* off; files moved outside Obsidian; shortest-path ambiguity → enable setting, move inside Obsidian, keep unique names |
| Duplicate notes `Note 1.md`, `conflicted copy` | Sync conflicts (iCloud/Dropbox/Remotely Save) → merge manually; use one sync method |
| Sync stuck / files missing on one device | Size limits (Sync logs skipped files), file type filters, paused sync, iOS vault location mismatch |
| Images not showing | Attachment path changed; `![[img.png]]` vs path link; external image blocked; case-sensitive filesystem on Linux/Android |
| Slow startup | Too many plugins; Dataview indexing; huge vault on slow storage; Homepage loading a heavy note |
| High CPU at idle | Sync icon spinning (fixed 1.13), Git auto-backup interval too short, a plugin polling, a DataviewJS loop |
| Mermaid not rendering | 1.13 one-time confirmation banner not accepted; syntax error (check at mermaid.live); Mermaid version differences |
| Callout colours wrong after update | 1.13 `--callout-color` now needs a full CSS colour → update snippets |
| Light/dark hotkey stopped working | 1.10 replaced separate commands with *Toggle light/dark mode* → rebind |
| CLI `obsidian: command not found` | Installer < 1.12.7; PATH not registered; terminal not restarted; Linux `~/.local/bin` not in PATH; macOS symlink missing (`sudo ln -sf /Applications/Obsidian.app/Contents/MacOS/obsidian-cli /usr/local/bin/obsidian`) |
| URI does nothing | 1.13 confirmation dialog dismissed/denied → Settings → manage URI allow list; vault name wrong; URL encoding |
| Plugin settings lost after sync | Sync excluded plugin data; device-specific settings overwritten → decide per plugin what to sync |
| Note reverted to older content | Two devices edited offline; last writer won → recover from Sync history/File recovery; avoid offline dual edits |
| Rendering differs Live Preview vs Reading | Some syntax only renders in one (nested fences, HTML blocks, certain plugins) → check in Reading view before publishing |
| Excalidraw drawing shows as text | Plugin disabled or file opened as Markdown → enable; right-click → Open as Excalidraw |
| Vault won't open / crashes on launch | Installer too old (1.13 shows an explicit error); corrupt `.obsidian/workspace.json` (delete it); a plugin crashing at load (temporarily rename `.obsidian/community-plugins.json` to disable all, then re-enable in halves) |

## Keeping the system, not just the files, healthy

- **`Meta/Vault Guide.md`**: how the vault works — folders, types, conventions, plugins and why, dashboards, rituals. Update when you change something. It is the document a future you (or an agent) reads first.
- **`Meta/Plugin List.md`**: each plugin, its purpose, its settings worth remembering, and the date you last confirmed it earns its place. The CLI can regenerate the raw list (`obsidian plugins:enabled versions`).
- **`Meta/Changelog.md`**: dated one-liners of system changes ("2026-09: moved Reading list from Dataview to Bases"). Cheap and invaluable when something feels different.
- **`Meta/Query Library.md`**, **`Meta/Prompts/`**, **`Templates/`**: your code; version it (Git).
- **Freeze the architecture**: change the skeleton at most yearly. Move fast inside it; move slowly on it.

## When to rebuild

Almost never. Symptoms that justify a restructure: you cannot find things you know you wrote; every capture requires a decision; dashboards you built are never opened; the schema has three synonyms for everything. Even then: *migrate*, do not restart — write the new schema, batch-update properties (Bases table paste, an agent with Git, a script), move folders inside Obsidian so links update, archive rather than delete. A fresh vault throws away the backlink history that is the whole point.

## Key takeaways

- Maintenance is a calendar: weekly inbox/updates/conflicts, monthly schema and attachment hygiene, quarterly plugin/template/dashboard audit and archiving, yearly restore test and vault guide update.
- Performance is dominated by plugin weight, live queries per note, and attachments; Bases over DataviewJS, ≤ 25 plugins (≤ 12 on mobile), media outside the vault, installer updated.
- Troubleshoot in order: reload → console → Restricted mode bisect → snippets/theme → sandbox vault → versions/changelog → the files themselves → recovery layers.
- Keep `Meta/` documentation (vault guide, plugin list, changelog, query library) current — it is the system's memory.
- Migrate, never restart.

## Next

[Chapter 33: Migration — Into and Out of Obsidian →](33-migration.md)
