# Mobile

Obsidian on iOS and Android is the same app — same vault, same plugins, same Markdown — running on a smaller screen with a touch keyboard and an operating system that suspends it constantly. Used for what phones are good at (capture, reading, quick edits, checking things off) it is excellent; used for vault administration it is frustrating. This chapter covers setup on each platform, the mobile UI's specific features, workflows tuned for thumbs, OS-level automation (Shortcuts, Tasker, Share Sheet), and performance.

## Setup

### iOS / iPadOS

- Install from the App Store. On first launch choose **Create new vault** (local, "On My iPhone/Obsidian") or **Open folder as vault** (iCloud Drive) or **Set up Obsidian Sync**.
- **Storage location decides your sync method**: iCloud Drive vault → iCloud sync only. Local vault → Obsidian Sync, Remotely Save, or LiveSync. Never combine.
- iPad supports split view and Stage Manager; sidebars behave like desktop in landscape; keyboard shortcuts work with a hardware keyboard (++cmd+p++, ++cmd+o++, etc.).
- Background: iOS suspends the app; sync happens when you open it. Obsidian Sync catches up in seconds; Remotely Save runs on open (set "sync on start").

### Android

- Play Store, F-Droid, or the GitHub APK. Grant **All files access** if you keep the vault outside the app's private storage (recommended — private storage is deleted with the app).
- Vault anywhere on internal storage; **Syncthing** folders work natively (the best free Android sync); Remotely Save and Obsidian Sync also fine.
- Some keyboards (Gboard) autocorrect Markdown syntax; add `[[`, `#`, `- [ ]` to the personal dictionary or use a Markdown-friendly keyboard. **Swiftkey** and **Unexpected Keyboard** are popular among Obsidian users.
- Back gesture closes modals; long-press for context menus.

### Both

- Settings → **Appearance → Mobile**: quick-action (swipe down) command, ribbon items, and the **mobile toolbar** — the row of buttons above the keyboard. Configure it (Settings → Toolbar) with 8–12 actions: toggle checkbox, indent/outdent, insert link, insert template, Tasks: create/edit, insert timestamp (Templater), undo/redo, toggle bold, heading, Daily note. The toolbar is the mobile command palette.
- **Pull-down gesture** on the editor runs a configurable command (default: command palette; set to *Quick switcher* or *Open today's daily note*).
- **Tab switcher** (1.7+): a grid of open tabs; swipe to close.
- Sync **hotkeys/appearance/core settings** from desktop, but be selective with plugins (below).

## What mobile does well

- **Capture**: daily note, quick switcher create, Share Sheet (iOS 1.13), share intent (Android), voice dictation, camera → paste image.
- **Reading**: Reading view, embedded Bases, dashboards (light ones), PDFs (built-in viewer), Publish-like browsing of your own notes.
- **Ticking**: tasks in queries, habit checkboxes, Meta Bind sliders/toggles.
- **Light editing**: fixing a line, adding a log entry, a property value.
- **Bases**: table and cards views render well; inline editing works; kanban (1.14) on a phone is cramped but usable on tablet.
- **Canvas**: view and light editing on tablet; awkward on phone.

## What to avoid on mobile

- Heavy DataviewJS dashboards (slow to render, battery-hungry).
- Vault-wide refactors (renames are fine; moving folders and mass edits are not).
- Plugin installation/configuration (do it on desktop; sync).
- Git as the sync method for big vaults (isomorphic-git is slow; works for small vaults).
- Excalidraw complex drawings on phone (fine on tablet with pencil).

## The mobile capture kit

### Daily note as the landing page

Settings → Daily notes → *Open daily note on startup*; or Homepage plugin → today's note on mobile only (it has a separate mobile setting). Template: light on queries (one Tasks query, no DataviewJS), Meta Bind sliders for mood/energy, a `## Log` section.

### Log line command

QuickAdd capture "Log": target today's daily note, insert under `## Log`, format `- {{DATE:HH:mm}} {{VALUE}}`. Add to the mobile toolbar. Two taps and dictation → a timestamped entry.

### Quick task

QuickAdd capture "Task" → today's `## Plan` as `- [ ] {{VALUE}}`; or the Tasks plugin's *Create or edit task* on the toolbar (the modal has date pickers — much easier than emoji on a phone).

### Share Sheet (iOS, Obsidian 1.13)

Share text, links, images, or files from any app to Obsidian **without opening the app**. Configure **Locations** in Settings → Share: each location defines a vault, a folder or "daily note", and a template with variables (`{{title}}`, `{{url}}`, `{{content}}`, `{{date}}`, `{{selection}}`). Typical locations: "Inbox" (new note in `Inbox/` with a clipping template), "Today" (append to the daily note's `## Notes`), "Reading list" (create in `Sources/Articles/` with `status: to-read`). Shared images land in Attachments with an embed.

### Android share intent

Obsidian appears in the share menu; shared text/links open a new note (or, with **Advanced URI**/**Tasker** flows, can be appended to a target). Third-party: **Obsidian Share** style apps, Tasker with `obsidian://` URIs, or the **Telegram Sync** plugin for a Telegram-to-vault capture channel that works from any device.

### Voice

System dictation into the log line is the simplest. Better: record a voice memo, transcribe (Whisper via a Shortcut, Otter, or the **Whisper** plugin on desktop later), and land the text in `Inbox/`. Chapter 30 covers pipelines.

### Photos

Camera → share to Obsidian (Share Sheet) → today's note. Or paste from the clipboard in the editor. Attachment Management renames on desktop later; on mobile, filenames are timestamps — acceptable.

### Web Clipper on mobile

The extension works in **Safari on iOS** (as a Safari extension), **Firefox/Kiwi/Edge on Android**; Chrome Android does not support extensions. Alternatively share the URL to Obsidian via Share Sheet with a template that stores the URL for desktop clipping later.

## Reading and reviewing on mobile

- **Reading view by default** for a review session (Settings → Editor → Default view for new tabs: Reading, on mobile only via a mobile-specific setting or a CSS snippet).
- **Bases**: pin a "Today" and "Contact due" view as bookmarks; the bookmarks pane is one tap from the ribbon.
- **Random note** on the toolbar for commute reviews of idea notes.
- **Spaced Repetition** flashcards review works on mobile — a two-minute queue session.
- **Outline pane** for long notes; **fold all** to skim.

## Templater and QuickAdd on mobile

Both work. Templater's *Trigger on new file creation* applies templates on mobile too; user scripts run (they are JS; `tp.system.prompt/suggester` render as modals). Shell-command functions do not (no shell). QuickAdd captures and template commands are the backbone of thumb capture; assign them to the toolbar via **Commander** (which can add any command to the mobile toolbar) or QuickAdd's own toolbar option.

## OS automation

### iOS Shortcuts

Shortcuts can:

- Open URLs: `obsidian://new?vault=Main&name=Inbox/Quick&content=...` (URL-encode content) — the built-in URI (Chapter 29). With **Advanced URI**: `obsidian://adv-uri?vault=Main&daily=true&heading=Log&data=- 14:32 text&mode=append`.
- Write files directly to the vault folder if the vault is in "On My iPhone/Obsidian" (the *Save File* action to the Obsidian folder) — no Obsidian launch needed; the app indexes on next open. This is how to build "append to daily note without opening Obsidian" reliably.
- Chain: *Dictate Text* → *Save File* to `Inbox/`; *Get Current Location* → text → daily note; *Health samples* (sleep) → daily note property via a small text transform; *Calendar events today* → daily note `## Agenda`.
- Run from the Action button, back tap, widgets, Siri, or automations (time of day, arriving at a location: "when I leave the gym, ask for workout RPE and write a workout note").

### Android Tasker / Automate

Same idea: `obsidian://` intents, direct file writes to the vault folder (Tasker's *Write File*), triggers (time, location, NFC tag on the fridge → open Pantry note). **Termux** on Android can run scripts against the vault folder (and Git); **Syncthing** keeps it in sync.

### Widgets

No official widget. iOS: a Shortcuts widget with your capture shortcuts; Scriptable widgets can *read* a note (e.g. today's tasks) from the Obsidian folder and display it. Android: Tasker/KWGT widgets can do similar; some third-party "Markdown note widget" apps can display a file from the vault.

## Performance on mobile

- Startup time is dominated by plugin count and vault size. Under 20 plugins and under ~10k notes is comfortable; beyond, prune.
- Disable heavy desktop-only plugins on mobile: many have a mobile toggle in their settings; or use a `.obsidian` **profile per device** (Obsidian Sync can exclude plugin sync; Git can ignore `community-plugins.json` per device — advanced).
- Dataview indexing on open is the usual culprit; Bases are cheaper.
- Attachments: keep the vault under a few GB; exclude video from sync.
- Turn off *Auto reveal current file* in File explorer if the tree is huge.
- iOS: if the app is killed in the background, unsaved edits are lost only in the last second or two — Obsidian saves continuously; nonetheless, avoid switching away mid-sentence during a long edit.

## Mobile-specific settings worth setting

| Setting | Recommendation |
| --- | --- |
| Appearance → Font size | Larger than desktop (18–20) |
| Editor → Readable line length | On |
| Mobile toolbar | 8–12 curated actions |
| Pull-down quick action | Open today's daily note or Quick switcher |
| Daily notes → Open on startup | On (mobile is capture-first) |
| Files & links → Confirm deletion | On (fat fingers) |
| Spellcheck | System |
| Community plugins | Only what mobile needs: Templater, Tasks, QuickAdd, Meta Bind, Calendar, Periodic Notes, Omnisearch (optional), Spaced Repetition; consider disabling Dataview-heavy dashboards |

## Tablet as a middle ground

iPad/Android tablets with a keyboard are near-desktop: sidebars, split panes, Canvas, Excalidraw with a stylus, PDF++ annotation (excellent with a pencil), long-form writing. Use a separate workspace layout; Obsidian keeps mobile and desktop layouts separately.

## Key takeaways

- Mobile is for capture, reading, and ticking; administration stays on desktop.
- Configure the mobile toolbar and pull-down action, land on the daily note, and build a capture kit: log line, quick task, Share Sheet/share intent locations, voice, photos.
- Keep mobile templates and dashboards light; prefer Bases over DataviewJS; prune plugins.
- OS automation (Shortcuts/Tasker) can write to the vault folder or fire `obsidian://` URIs — daily-note appends without opening the app.
- Tablets with keyboards are a legitimate primary device; phones are not.

## Next

[Chapter 28: Customization — Themes, CSS and Layout →](28-customization.md)
