# Work and Career

Work generates more notes than any other domain — meetings, decisions, people, documents, one-on-ones, projects — and most of them are lost within a month in email threads and chat scrollback. A vault that captures them turns you into the person who remembers what was decided, who said what, and why. This chapter covers the work-side capture points (meetings, people, decisions, docs), the career layer (brag document, feedback, job search, career journal), and the confidentiality decisions that come first.

## Confidentiality first

Decide before you write a single work note:

| Situation | Design |
| --- | --- |
| Employer permits personal tools; no regulated data | `Work/` folder in the main vault, `area: "[[Career]]"`; exclude `Work/` from Publish/shares; sync only via E2E-encrypted means |
| Employer prohibits external storage of company data, or you handle regulated data (health, finance, legal) | **Separate work vault** on the work machine only, no personal sync; same templates. When you leave, the vault leaves with the laptop |
| Contractor / multiple clients | One vault, `Work/<Client>/` subfolders and a `client` property; or one vault per client if contracts require |

Rule of thumb: names of colleagues and the *fact* that a meeting happened are usually fine in a personal vault; customer data, unreleased numbers, and anything under NDA are not. When in doubt, the work vault.

## Meetings

The meeting note is the single highest-value work artifact. Template in Chapter 11; the fields and why:

- **`date`** — obvious; also makes the Meetings Base sortable.
- **`attendees`** — list of `[[People]]` links. Each person's note now shows every meeting they were in (backlinks) and the "With this person" Base view.
- **`project`** — link; the project note shows its meetings.
- **`decisions`** — list; the reason meetings exist. Also written as prose under `## Decisions`.
- **`next_meeting`** — date, for the follow-up.
- **Agenda / Notes / Decisions / Actions** — actions as tasks with `👤 Name` for others, plain for you, `📅` dates where promised.

Workflow: create the note *before* the meeting (agenda items accumulate — see person agendas below), take notes in it during, spend two minutes after tidying decisions and actions. Naming `YYYY-MM-DD Topic` keeps them chronological and unique.

**Recurring meetings** (weekly team sync): one note per occurrence, not one growing note — Bases and backlinks work per file. A `series` property (`series: "Team sync"`) groups them.

**Agendas for the next conversation**: in a person's note or a project note, a `## Next time` list; the meeting template can pull it in (Templater: read the person's note, extract the section). Simpler: a Tasks query in the meeting note `path includes People/Jane` + `heading includes Next time`.

**Calendar integration**: the Google Calendar plugin or Full Calendar can create meeting notes from events; an Apple Shortcut / Raycast script can call `obsidian create name="2026-09-06 Alpha kickoff" template=tpl-meeting` (CLI) from a calendar event. Chapter 29.

## People at work

`type: person`, `relationship: colleague`, plus work-specific properties: `company`, `team`, `role`, `manager` (link), `reports` (list of links), `timezone`, `slack`, `started` (date). The note body: how to work well with them, what they care about, personal details they shared (kids' names, hobbies — the human layer), and the `## Next time` agenda. Backlinks supply the interaction history automatically.

**One-on-ones** (if you manage or are managed): a `1:1` meeting series per person with a template: wins since last time, blockers, feedback both ways, growth topic, actions. A Base filtered `series == "1:1"` grouped by attendee shows cadence gaps (`Latest` summary of `date`). Keep sensitive performance notes in the work vault if you have one.

**Org map**: a Canvas of people notes with reporting lines, refreshed quarterly; or Breadcrumbs with `manager` properties for an auto hierarchy.

## Decisions

`type: decision` notes (Chapter 25 has the full method) for anything that took a meeting to decide or that you will be asked about in six months: architecture choices, vendor selection, hiring, process changes. Properties `date`, `status`, `options`, `chosen`, `confidence`, `review_on`; body: context, options with trade-offs, decision and reasoning, expected outcome, review. Linked from the meeting where it happened and the project it affects. A `Decisions.base` per project is a **decision log** — the artifact that makes you look organized when leadership asks "why did we…".

Architecture Decision Records (ADRs) are exactly this; if your team keeps ADRs in a repo, mirror the ones you own in your vault with a link.

## Documents and knowledge

`Work/Docs/`: your working documents — proposals, plans, specs, retrospectives, runbooks — drafted in Markdown and exported (Pandoc → DOCX/Google Docs paste; 1.12+ copies rich text to the clipboard so pasting into Docs keeps formatting). Properties: `type: doc`, `doc_kind` (proposal/spec/plan/retro/runbook/howto), `status` (draft/review/final/superseded), `project`, `audience`. A Base view "Docs in review" reminds you to chase.

**Runbooks and how-tos**: the highest-return work notes — "how to rotate the API key", "how to run the monthly report". Each saves an hour next quarter. Tag `#howto`, keep steps as numbered lists with code blocks, date the last verification.

**Team knowledge** belongs in the team's wiki. Your vault holds *your* understanding of it: links to the wiki pages, your annotations, your mental model. Do not duplicate the wiki.

## Projects at work

Same `project` type with `area: "[[Career]]"` (or the work vault's areas: Team, Product, Platform…). Extra properties: `stakeholders` (links), `status_report` cadence, `ticket` URL. The project note's `## Log` becomes your status-report source: a Dataview or Tasks query of what was done this week, plus the log lines, is a status update in 90 seconds.

Weekly status template (in the weekly note's work section or a `Work/Status/` note):

```markdown
## Status — <% tp.date.now("YYYY-[W]WW") %>
### Done
```tasks
done this week
path includes Work
short mode
```
### Next
```tasks
not done
path includes Work
happens next week
short mode
```
### Blockers / needs
- 
```

## The career layer

### Brag document

`Work/Career/Brag Document 2026.md` — a running record of accomplishments with dates, impact, evidence links (the doc, the meeting where it was praised, the metric). Update weekly during the review (one line). This is the raw material for performance reviews, promotion cases, and CVs, and it corrects the recency bias of "what did I do this year?". Structure: by quarter, or by theme (delivery, leadership, learning, collaboration).

### Feedback log

`Work/Career/Feedback.md` — every piece of feedback received, dated, sourced, with your reflection. Patterns emerge over a year that no single review shows. Feedback *given* can live in the person's note.

### Career journal

Monthly, three prompts in the monthly note's Career area check-in: what energized me; what drained me; what did I learn. Yearly: a `Career` area review — am I growing, am I paid fairly (link to comp research), what is the next role, what skills does it need (→ goals).

### Skills and learning

Skills as `goal` notes (Chapter 16/17) with courses as sources and projects as practice. A `Work/Career/Skills Matrix.md` table (skill × level × evidence × plan) reviewed yearly.

### Network

People notes with `relationship: professional` and `contact_every`. Former colleagues are the network that finds you your next job; the People Base's contact-due view is how you keep them warm without a CRM subscription. After each conversation: one line in their note, `last_contact` updated.

### Job search (when it happens)

`Projects/Job Search 2027/` with:

- `Companies/<Company>.md` (`type: company`, `status`: interested/applied/interviewing/offer/rejected/declined, `role`, `source`, `contact` links, `salary_range`, `applied` date).
- A `Job Search.base` kanban (1.14) or table grouped by `status` — the pipeline.
- `Interviews/YYYY-MM-DD Company Round.md` as meeting notes with `company` link, questions asked, your answers, follow-ups.
- Preparation notes: `Stories.md` (STAR stories drawn from the brag document), `Questions to ask.md`, `Compensation.md` (research + your numbers).
- Offers compared in a Base: base, bonus, equity, benefits, commute, growth — with formula columns for total comp.

### Comp and benefits records

`Life/Admin/` or `Finance/`: offer letters, comp history (a table with dates), benefits enrolment decisions, equity grants and vesting schedule (a Base with `vests` dates → "vesting in 90 days" view). Handy at review time and tax time.

## Freelancers and founders

Add: `type: client` notes (contacts, rates, contracts linked from `Life/Admin/Contracts/`, active projects Base), `type: invoice` records (or a ledger note — Chapter 21) with `client`, `amount`, `issued`, `due`, `paid` → an Invoices Base with "Unpaid" and "Overdue" views and `Sum` summaries; time tracking per project (Simple Time Tracker blocks in project notes; export CSV for invoicing); a pipeline Base for leads (`status`: lead/proposal/won/lost). Founders: investor CRM (people with `relationship: investor`, `stage`, `last_contact`), board meeting notes as meetings with `series: "Board"`, a metrics note updated weekly.

## Work dashboard

```markdown
## Today at work
```tasks
not done
path includes Work
(due before tomorrow) OR (scheduled before tomorrow)
sort by urgency
```
## Waiting on others
```tasks
not done
path includes Work
description includes 👤
group by filename
```
## Meetings this week
![[Meetings.base#This week]]
## Active work projects
```base
filters: {and: [type == "project", status == "active", area == link("Career")]}
views: [{type: table, name: Active, order: [file.name, due, priority, stakeholders]}]
```
## 1:1s overdue
(Base: series == "1:1", grouped by attendee, Latest(date) summary — eyeball gaps)
## Docs in review
```base
filters: {and: [type == "doc", status == "review"]}
views: [{type: list, name: Review, order: [file.name, audience, file.mtime]}]
```
```

## Anti-patterns

- Meeting notes that are transcripts. Capture decisions and actions; a recording/transcript tool can hold the rest (link it).
- One giant note per project that becomes unnavigable. Meetings, decisions, and docs are separate typed notes linked to the project.
- Work tasks without owners or dates. `👤` and `📅` or it did not happen.
- Mixing NDA material into a synced personal vault. Decide the vault boundary first.
- Skipping the brag document because "I'll remember". You will not.

## Key takeaways

- Decide the confidentiality boundary (folder vs. separate vault) before anything else.
- Meeting notes with `attendees`, `project`, `decisions`, and 👤-tagged actions are the core capture; people notes and project notes get their history from them automatically.
- Decision notes are your decision log; runbooks are your highest-return documents; the weekly status writes itself from tasks and project logs.
- The career layer — brag document, feedback log, career journal, skills matrix, warm network, job-search pipeline as a Base — is what turns a work vault into a career asset.
- Freelancers add clients, invoices, time tracking and a pipeline; founders add investors, board notes and metrics.

## Next

[Chapter 20: Health, Fitness and Food →](20-health-fitness-food.md)
