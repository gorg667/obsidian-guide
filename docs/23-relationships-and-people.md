# Relationships and People

People notes are the most quietly transformative part of a whole-life vault. Not because Obsidian is a good CRM — it is a mediocre one — but because a person note sits in the same graph as your journal, meetings, books, trips, and decisions, so it accumulates a complete, honest record of a relationship without you maintaining anything. This chapter covers the person note, the interaction record that backlinks build for free, the light structure that keeps important relationships from drifting, family history, and the ethics of writing about people.

## The person note

`type: person` in `People/`, from `tpl-person` (Chapter 11). Filename: the full name as you say it; aliases for nicknames and maiden/married names. Properties:

| Property | Purpose |
| --- | --- |
| `relationship` | family / partner / friend / colleague / acquaintance / professional / former |
| `circle` (optional) | inner / close / wider — a coarser tier for the contact cadence |
| `birthday` | date; drives the birthdays view (year can be a placeholder like 1900 if unknown) |
| `met` | date or year; where/how in the body |
| `location` | city; for travel ("who do I know in Lisbon?") |
| `email`, `phone`, `handles` | contact channels (phone optional — your contacts app has it; the vault needs enough to disambiguate) |
| `company`, `role` | for professional contacts (link company notes if useful) |
| `partner`, `children`, `parents` | links — the family graph |
| `last_contact` | date; updated when you actually talk |
| `contact_every` | days; cadence you intend (7 / 30 / 90 / 180 / 365) |
| `photo` | for the cards view |
| `tags` | interests, groups (`#climbing`, `#book-club`) |

Body sections: **About** (who they are to you, what they care about — the human summary), **Interactions** (mostly backlinks; add lines for significant moments), **Gift ideas & preferences** (sizes, allergies, favourites, what you already gave), **Connections** (how you met, mutual friends — links), **Next time** (things to ask, follow up on, tell them).

## The interaction record you never write

Every time a daily note says `coffee with [[Jane Doe]]`, a meeting note lists her in `attendees`, a trip note names her in `companions`, or a book note says `recommended by [[Jane Doe]]` — Jane's backlinks pane grows. Open her note before you meet and read the last five backlinks: the promises, the news, the thing she was worried about. That is the CRM. The only discipline it requires is **linking people's names when you write them**, which the `[[` autocomplete makes nearly free. Unlinked mentions catch the ones you missed.

The "With this person" Base view (Chapter 10) shows meetings; a Dataview list of daily notes mentioning them (`FROM [[Jane Doe]] AND "Journal"`) shows the social history. Both embedded in the person template.

## Keeping relationships from drifting

The problem structure solves: the people who matter most are often the ones you least need to schedule — and so months pass. Two properties fix it: `contact_every` and `last_contact`. The People Base's **Contact due** view lists who is overdue, sorted by how overdue. Review it in the weekly review; pick one or two; message them; update `last_contact` (a cell edit in the Base, or a Templater command "Log contact" that sets the date and appends a line to the daily note).

Cadence guidance (yours will differ): partner/kids — no property needed; parents and siblings — 7–14; inner circle friends — 14–30; close friends — 30–60; wider friends and mentors — 90–180; professional network — 180–365. Reassess yearly; `relationship: former` for people you consciously let go.

**Birthdays**: the Base "Birthdays this month" view plus a monthly-review task "Check birthdays" covers it. For reminders on the day, your calendar app is still better — export once a year via a script or keep birthdays in both.

**Occasions**: anniversaries, kids' birthdays, memorial dates as properties on the person or family note; a `Life/Occasions.base` with a `formula` computing next occurrence.

## Family

`People/Family/` or just `relationship: family`. A **family hub note** (`Family.md`) with a Canvas or Mermaid tree of the closest generations, links to each person, shared traditions, recipes (links), addresses, the family group's logistics.

**Family history**: for genealogy, one person note per ancestor with `born`, `died`, `birthplace`, `parents`/`children` links, sources (links to documents, photos, records), stories. Mermaid or Canvas for trees; the Bases map for birthplaces; a Dataview query for "people born in the 1800s without a death date" — the genealogist's to-do list. Dedicated genealogy software handles GEDCOM and citations better; Obsidian holds the *narrative* — the stories your grandmother told, transcribed interviews (Chapter 30 for voice → text), scanned letters.

**Partner**: a shared vault or folder for the logistical parts (Chapter 22: home, kids, finances, trips); personal reflections about the relationship stay in your journal or `Mind/`. A `## Us` section in the yearly review — things you did together, what you want next year — is a good ritual.

**Kids**: Chapter 22's per-child folders; plus `Memories.md` per child. Interview them yearly with the same ten questions; record and transcribe.

## Friends and community

- **Groups**: a `group` note (`type: group`: book club, climbing crew, alumni) with members (links), cadence, history, and the Base of meetings/events with `group` link. Person notes list their groups via backlinks.
- **Events**: `type: event` (dinner, party, trip) with `attendees` — same shape as a meeting note; the person's backlinks include them.
- **Introductions**: when you connect two people, a line in both notes; a `introduced` list property if you enjoy graph queries.
- **Hospitality**: a `Hosting.md` note — who has been over, what you cooked (link recipes), dietary needs (also on person notes). Prevents serving the same dish twice and forgetting the vegetarian.

## Professional network

Chapter 19 covers colleagues and the warm network. Additions: `type: company` notes (people link to them; company note's backlinks list everyone you know there); `source` of the contact (conference, intro by X); `can_help_with` / `i_can_help_with` free-text — the fields that make a network reciprocal.

## Difficult relationships and boundaries

The vault is a safe place to think. A person note can hold a `## Boundaries` or `## Patterns` section — what tends to happen, what you decided to do about it (a `decision` note), how the last conversation went. Written calmly once, it prevents relitigating each time. Keep such notes in the journal's privacy tier.

## Gratitude and appreciation

A `## Appreciation` section in person notes, or a weekly-review prompt "who helped me this week?" with links — and then *tell them*. A Dataview query of people linked from `Gratitude` sections over the year is a beautiful thing to read in December.

## People dashboard (`Areas/Relationships.md` or `People MOC.md`)

```markdown
## Contact due
![[People.base#Contact due]]

## Birthdays this month
![[People.base#Birthdays this month]]

## Recently in touch
```base
filters: {and: [type == "person", last_contact >= today() - "14d"]}
views: [{type: list, name: Recent, order: [file.name, last_contact], sort: [{property: last_contact, direction: DESC}]}]
```

## Who's in [[Lisbon]]?
```base
filters: {and: [type == "person", location == "Lisbon"]}
views: [{type: list, name: Lisbon, order: [file.name, relationship]}]
```

## Groups
[[Book club]] · [[Climbing crew]] · [[Family]]

## Directory
![[People.base#Directory]]
```

## Capture habits

- Link names in daily notes and meeting notes. Always.
- After a meaningful conversation: one line in their note (or in the daily note with their link), `last_contact` updated, `## Next time` topped up.
- When they mention something (a book, a trip, a worry): capture in `## Next time` or as a task `Ask [[Jane]] about the Lisbon trip ⏳ 2026-09-20`.
- New person met: `tpl-new` → Person; fill `met` and `About` while you remember.
- Mobile: a QuickAdd "Log contact" capture — pick person (suggester), type a line → appended to their note and today's note, `last_contact` set.

## Ethics and privacy

You are writing about people who did not consent. Rules that keep it decent:

1. Write what *you* would be comfortable with them reading. Facts, your feelings, your plans — yes. Cruelty, gossip, others' secrets told in confidence — no.
2. Health, legal, and financial details about others only when you need them for care (kids, parents) — and in the privacy tier.
3. Never publish `People/`. Exclude it from Publish and shared vaults by default.
4. Sync only E2E-encrypted.
5. If someone asks what you have written about them, you should be able to show them.

## Anti-patterns

- Turning the vault into a full CRM with pipelines and scores for friends. Two properties (`contact_every`, `last_contact`) are the whole system.
- Person notes without links from anywhere — the interaction record only builds if you link names when writing.
- Copying your phone's contacts into notes. Only people you will write about.
- Never opening the note before a conversation — the payoff step.

## Key takeaways

- A person note plus the habit of linking names gives you a complete relationship record from backlinks, for free.
- `contact_every` + `last_contact` + one Base view is the entire anti-drift system; review weekly, message one or two people.
- Family gets a hub, history notes hold stories rather than genealogy data, shared logistics go in a shared vault, reflections stay private.
- Groups, events, hosting, gift ideas and `## Next time` sections make you the friend who remembers.
- Write about people as if they might read it; never publish or share `People/`.

## Next

[Chapter 24: Creativity, Writing and Media →](24-creativity-writing-media.md)
