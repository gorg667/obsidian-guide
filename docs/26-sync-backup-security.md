# Sync, Backup and Security

A whole-life vault is, by construction, the most valuable and most sensitive collection of files you own. Three separate problems protect it, and people conflate them constantly: **sync** (the same vault on several devices), **backup** (recovering from loss, corruption, or your own mistakes), and **security** (keeping others out). Sync is not backup. Backup is not security. This chapter gives a decision matrix for sync, a 3-2-1 backup design that works with Obsidian's quirks, and a security posture covering encryption, plugins, URIs, secrets, and sharing.

## Sync

### The options

| Method | Platforms | E2E encrypted | Conflict handling | Version history | Cost | Best for |
| --- | --- | --- | --- | --- | --- | --- |
| **Obsidian Sync** | All (incl. iOS, Android) | Yes | Merges Markdown line-by-line; keeps versions | 1 month (Standard) / 12 months (Plus); per-file restore; 1.13 Sync sidebar view | ~$4–8/mo | Most people; mobile; zero maintenance |
| **iCloud Drive** | macOS, iOS (Windows client is poor) | No (Apple holds keys unless Advanced Data Protection is on) | Duplicates as "conflicted copy"; occasional file eviction | None (Time Machine on Mac) | Included | Apple-only users who accept the risks |
| **Syncthing** | Desktop, Android (no iOS) | Device-to-device TLS; no server | Conflict files `.sync-conflict-…` | File versioning optional | Free | Privacy-focused, Android, self-managed |
| **Git** (Obsidian Git plugin) | Desktop excellent; mobile possible (isomorphic-git, slow, large vaults struggle) | Repo host sees content unless private + trusted; use git-crypt/private repo | Merge conflicts you resolve | Complete, forever | Free/private repo | Developers; also a backup |
| **Remotely Save** | All | Optional E2E (password) | Last-writer-wins with checks; keeps deleted-file trash | Provider's versioning | Free + storage | Cross-platform free sync to S3/WebDAV/Dropbox/OneDrive/GDrive/Box/Nextcloud |
| **Self-hosted LiveSync** | All | Yes | Near-real-time, document-level, handles conflicts with a resolver UI | Configurable | Self-hosted CouchDB (or fly.io/IBM Cloudant free tiers) | Self-hosters wanting real-time sync |
| **Dropbox / OneDrive / Google Drive** | Desktop; mobile via third-party file providers only | No | Conflicted copies; OneDrive "files on demand" breaks indexing | Provider versions | Included/paid | Not recommended as the primary; fine as a backup target |
| **Resilio / rsync / Unison** | Desktop | Varies | Manual | None | Varies | Edge cases |

### Recommendation

- **Default: Obsidian Sync.** It is the only option that is E2E-encrypted, works flawlessly on iOS, merges Markdown intelligently, versions everything, and funds the app. Standard tier suffices for one vault; Plus for multiple vaults, larger attachments, longer history.
- **Free and cross-platform: Remotely Save** with E2E encryption enabled, pointed at any S3-compatible bucket (Backblaze B2 is cheap) or WebDAV (Nextcloud). Set sync to run on start/interval; avoid editing on two devices simultaneously.
- **Self-hosters: Self-hosted LiveSync.**
- **Developers: Git** — but usually as *backup + history* alongside Sync, not as the mobile sync mechanism.
- **Avoid as primary**: iCloud (eviction, conflicts, no Windows), OneDrive (files on demand), Google Drive on mobile.

### Sync hygiene (all methods)

- **Do not sync `.obsidian/workspace.json`** (Obsidian Sync excludes it by default; Git → `.gitignore`; Remotely Save → skip pattern). It changes constantly and is device-specific.
- **Plugins across devices**: Obsidian Sync can sync community plugins and their settings (1.13 warns before enabling because some settings are device-specific — Shell commands paths, Git executable, Local REST API ports). Sync plugins if your devices are similar; otherwise sync `community-plugins.json` and let each device install.
- **Hotkeys, appearance, snippets, core plugin settings**: sync them (Obsidian Sync options; Git includes them naturally).
- **Attachments**: set size limits (Sync: per-type toggles and max size — 1.12 logs skipped files). Large media outside the vault.
- **Never two sync systems on the same folder** (iCloud + Obsidian Sync on one vault is a classic corruption source).
- **Mobile**: iOS vault location must be "On My iPhone" for Obsidian Sync/Remotely Save/LiveSync or "iCloud Drive" for iCloud — not both. Android: any folder; Syncthing folders work.
- **Conflicts**: Obsidian Sync merges; others create conflict copies — search `conflict` weekly and resolve. The **Sync sidebar view** (1.13) and the CLI's `sync:history` / `sync:read` / `sync:restore` and `diff` make comparing versions fast.

### Git setup (Obsidian Git)

```gitignore
# .gitignore at vault root
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
.trash/
.DS_Store
# optional: keep plugin data but not caches
.obsidian/plugins/*/cache*
```

Plugin settings: auto backup every N minutes (commit), auto pull on startup, auto push after commit, commit message with `{{date}}` template, "pull before push". Desktop uses your system `git` (with credentials configured — SSH keys or a credential helper). Mobile uses isomorphic-git with a personal access token; workable for vaults under a few hundred MB, slow beyond. Use a **private** repository; treat the host (GitHub/GitLab/Gitea) as able to read your notes unless you add **git-crypt** or keep the repo on your own server. Branches are unnecessary; if a merge conflict appears, resolve in Source mode (conflict markers) and commit.

Git also gives you a **complete history forever** and `git log -p Journal/Daily/2026-09-06.md` archaeology. Even Obsidian Sync users often add a nightly Git commit as a backup layer.

## Backup

Sync propagates mistakes instantly — a deleted folder disappears everywhere. Backup is separate. Design: **3-2-1** — three copies, two media, one off-site — adapted:

| Layer | What | Recovers from |
| --- | --- | --- |
| **File recovery** (core) | Snapshots of edited files every 5 min for N days (raise to 30–90) | Bad edits, plugin damage to a note |
| **Sync version history** | Obsidian Sync (1–12 months) / Git history / provider versions | Deleted or overwritten files, cross-device errors |
| **`.trash/`** | Obsidian's trash folder (setting: move to Obsidian trash) | Accidental deletes; empty it quarterly, not weekly |
| **Local automated backup** | Time Machine / Windows File History / restic / Borg / `rsync` snapshots of the vault folder, hourly or daily | Disk failure, ransomware (if versions are immutable), mass corruption |
| **Off-site backup** | The Git remote, and/or a nightly `tar` of the vault to encrypted cloud storage (restic → B2/S3, Arq, Duplicati, Kopia) | House fire, theft, account lockout |
| **Cold copy** | Quarterly zip to an external drive or USB kept elsewhere; yearly export to PDF of the Emergency & Legacy note and key records | Everything else, including your own death (Chapter 22) |

Practical notes:

- Back up the **whole vault folder including `.obsidian/`** — the config is part of the system.
- Test restores twice a year: pick a note, restore it from each layer.
- Backups must be **versioned** (snapshots), not a mirror — a mirror faithfully copies your deletion.
- Encrypt off-site backups (restic/Borg/Kopia/Arq do by default).
- A script with the **Obsidian CLI** can export Bases to CSV nightly (`obsidian base:query file=Accounts format=csv > backup/accounts.csv`) for a spreadsheet-readable fallback of key records.
- `File recovery` data lives in the app's IndexedDB, *not* in the vault — it does not sync or back up; it is a per-device safety net only.

## Security

### Threat model, briefly

Who might read your vault? A thief with your laptop (disk encryption solves it); a cloud provider or a subpoena (E2E encryption solves it); malware or a malicious plugin (plugin discipline and OS security); someone you share a vault with (vault boundaries); a URI or link that triggers actions (1.13's confirmation dialogs); future you locked out (recovery planning).

### Device and disk

- Full-disk encryption on every device (FileVault, BitLocker, LUKS; iOS/Android default). Non-negotiable for a vault with journal and finance.
- Strong device passcodes; auto-lock; Obsidian mobile does not have its own lock, so the device lock *is* the vault lock. (Third-party "lock" plugins are cosmetic — the files are plain text on disk regardless.)

### Encryption in transit and at rest in the cloud

- Obsidian Sync: E2E with your password; **write down the encryption password** — Obsidian cannot recover it. Losing it means re-uploading the vault.
- Remotely Save: enable E2E; same warning.
- LiveSync: E2E passphrase; same warning.
- Git: private repo is *access control*, not encryption; add git-crypt for sensitive folders or accept the host's trust model.
- iCloud: Advanced Data Protection makes iCloud Drive E2E; otherwise Apple holds keys.

### Encrypting inside the vault

- **Meld Encrypt**: encrypts selected text or whole notes with a password (AES); encrypted notes show a decrypt button; searchable only when decrypted. Right for therapy notes, letters, the accounts registry — a handful of notes, not the whole vault (that is what disk/sync encryption is for).
- **Separate encrypted vault** (e.g. on a Cryptomator/VeraCrypt volume, or an encrypted disk image) for material you never want in the main vault's sync at all.
- Do not put passwords, recovery codes, or private keys in *any* note, encrypted or not. Password managers exist for a reason; the note links to the manager entry name.

### Plugins

Plugins run with full Node/Electron privileges on desktop: they can read every file, make network requests, and run processes. Mitigations: install only from the community directory (reviewed) or BRAT for well-known authors; prefer popular, open-source, maintained; read the permissions-equivalent (does a "table formatter" need network access? check the repo); avoid plugins that require pasting API keys into plain settings — use ones that support **Keychain** (1.11+, OS-level secret storage); keep plugins updated; review the list quarterly. **Restricted mode** disables all community plugins instantly if something looks wrong (1.13: exit without re-enabling all). Untrusted vaults: when opening a vault you did not create (a downloaded showcase), Obsidian 1.13 warns about the plugins it contains — keep Restricted mode on until you have read them.

### URIs, links, and external content

- `obsidian://` URIs can run actions (open, create, append, run commands via Advanced URI). 1.13 shows a **confirmation dialog** per action with an allow list — keep it on; allow only actions you use from trusted automations.
- 1.12+: confirmation when opening files in external apps; warning for executables.
- 1.13: warning before loading HTML resources from network drives; one-time confirmation before rendering **Mermaid** in a vault (Mermaid can embed links).
- Web Clipper content is Markdown; `<iframe>`s and scripts are neutralized by Obsidian's renderer, but be aware that a note can embed a remote image whose server logs the fetch (tracking pixel) — Obsidian fetches external images when rendering. Clip images locally if it matters.
- DataviewJS and Templater run arbitrary JavaScript from *your notes*. A note someone sends you with a `dataviewjs` block is executable code. Do not paste untrusted notes into a vault with JS plugins enabled; or paste them into a Restricted-mode scratch vault first.

### Secrets and API keys

AI plugins, Zotero, Readwise, Todoist, Local REST API all need keys. Prefer plugins that use **Keychain** (Settings → Keychain shows stored secrets). For plugins that store keys in `data.json`, know that Sync/Git will propagate them — exclude those files from Git (`.obsidian/plugins/<id>/data.json` in `.gitignore`) or accept the risk of a private repo. Rotate keys when a device is lost.

### Sharing a vault

- **With a partner/family**: a *separate shared vault* (Obsidian Sync supports multiple collaborators per vault on Plus/with shared vaults; Remotely Save with a shared bucket; LiveSync shared DB; Git with both as collaborators). Never share your main vault — the journal and Mind folders should not be one misclick from view.
- **Read-only sharing**: Publish (Chapter 31) with a password, or export PDF/HTML.
- **Work**: separate vault when confidentiality requires (Chapter 19).

### Recovery planning

- Write the sync encryption password, Git credentials, and backup encryption keys into your password manager, and the *existence and location* of the vault into the Emergency & Legacy note (Chapter 22).
- Keep one unencrypted-at-rest but disk-encrypted cold copy somewhere a trusted person can reach with instructions.
- Practice opening the vault on a fresh device from backups once a year — it exposes every missing credential.

## Checklist

- [ ] Sync method chosen; only one system on the vault folder; `workspace.json` excluded.
- [ ] Sync/backup encryption passwords stored in the password manager.
- [ ] File recovery history raised to 30+ days.
- [ ] Automated local versioned backup of the vault folder (incl. `.obsidian/`).
- [ ] Off-site encrypted backup (Git remote and/or restic-style) running nightly.
- [ ] Quarterly cold copy; yearly restore test.
- [ ] Full-disk encryption on all devices.
- [ ] Plugin list reviewed; API keys in Keychain where possible; `data.json` with secrets excluded from Git.
- [ ] URI confirmation on; allow list minimal.
- [ ] Sensitive folders (Journal, Mind, Health, Finance, People) excluded from Publish/shared vaults; Meld Encrypt or a separate vault for the most sensitive.
- [ ] Emergency & Legacy note updated and exported.

## Key takeaways

- Sync, backup, and security are three problems. Obsidian Sync (or Remotely Save with E2E / LiveSync) for sync; versioned local + off-site encrypted backups plus File recovery, history, and trash for backup; disk encryption, E2E sync, plugin discipline, URI confirmations, Keychain, and vault boundaries for security.
- Never run two sync systems on one folder; exclude `workspace.json`; keep large media out.
- Git is the best *history and backup* layer even if you sync another way.
- Encrypt a few notes with Meld Encrypt; encrypt everything at rest with the disk and in transit with E2E; put secrets in a password manager, never in notes.
- Plan recovery: passwords written down, restore tested yearly, the vault's existence documented for someone else.

## Next

[Chapter 27: Mobile →](27-mobile.md)
