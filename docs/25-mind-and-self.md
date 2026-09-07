# Mind and Self

The last life domain is the one that gives the others direction: what you value, how you decide, what you believe, what you have learned about yourself, and what you want your life to be for. It is also the domain where a plain-text vault you fully own is not merely convenient but necessary — nobody writes honestly about themselves into a company's database. This chapter covers values and principles, the decision journal, mental models and beliefs, therapy and emotional work, the commonplace book, reflection rituals, and the annual review that ties the year together.

## The `Mind/` folder

```text
Mind/
├── Values.md               what matters, ranked, with evidence
├── Principles.md           operating rules you have adopted (and why)
├── Vision.md               the life you are building toward; 3–5 year picture
├── Open Questions.md       Feynman's "favourite problems"
├── Decisions/              type: decision
├── Beliefs/                type: belief — claims about the world/yourself with confidence
├── Models/                 mental models as idea notes (or in Notes/ tagged #model)
├── Reviews/                annual reviews, life audits (or in Journal/Yearly)
├── Therapy/                session notes, exercises, patterns (privacy tier)
├── Commonplace/            quotes and passages by theme (or a single note + Base)
├── Prompts.md              journaling prompts, rotated by Templater
└── Mind MOC.md
```

## Values and principles

**Values** (`Mind/Values.md`): five to eight words with a paragraph each — what it means to you, what it looks like in practice, when you have honoured or betrayed it. Ranked, because conflicts between values are where hard decisions live. Revisit yearly; the diff between years is interesting. Values are *discovered* more than chosen: mine your journal (search for what made you angry, proud, ashamed) and your decisions.

**Principles** (`Mind/Principles.md`, or one note per principle in `Mind/Principles/`): operating rules — "Decide reversible things fast", "Never send the angry email the same day", "Default to the more generous interpretation". Each with: the rule, why (the incident that taught it — link the daily note or decision), exceptions, and a `confidence` or `adopted` date. One note per principle lets other notes link to it (`I broke [[Never send the angry email the same day]]`) and lets a Base show which principles have the most backlinks (the ones you keep needing).

**Vision** (`Mind/Vision.md`): a page describing an ordinary day 3–5 years out, in the present tense, across the areas. Embedded (`![[Vision#…]]`) into the yearly note and read at each quarterly review. Rewritten yearly.

## The decision journal

The highest-leverage practice in this chapter. `type: decision` notes (template in Chapter 11) for decisions that are consequential, hard to reverse, or that you will be asked about: jobs, moves, money, relationships, health choices, projects to start or kill, principles to adopt.

The fields matter because they make the decision *gradable later*:

- **Context** — what was true, what you knew, what you did not know.
- **Options** — including the one you did not take, with trade-offs (a table).
- **Decision & reasoning** — the actual argument.
- **Confidence** (1–10) — your calibration data.
- **Expected outcome** — falsifiable: "by March, X will have happened".
- **What would change my mind** — the pre-registered exit.
- **`review_on`** — six months, a year; the Decisions Base "Due for review" view surfaces it.
- **Review** — filled later: what happened, was the reasoning right (not just the outcome — good decisions have bad outcomes and vice versa), what to learn.

Over years the Base becomes a track record: average confidence vs. outcomes, domains where you decide well or badly, recurring failure modes (a `failure_mode` property: rushed / sunk cost / social pressure / overconfidence / analysis paralysis) — a personal epistemics dataset nobody else has about you. The yearly review reads all decisions of the year.

**Small decisions** do not get notes. The threshold: would I want to know, in a year, why I did this? If yes, five minutes now.

## Beliefs and mental models

**Beliefs** (`type: belief`, `Mind/Beliefs/`): claims about the world or yourself with `confidence` (%), `domain`, `sources` (links), `last_updated`, and a `## Evidence for / against` structure. "I do my best creative work before 10 am — 80%". "Index funds beat my stock picks — 95%". When evidence changes the confidence, update it and log the change — belief revision made visible. A Base sorted by confidence ascending shows what you are unsure about; one sorted by `last_updated` ascending shows what you have not re-examined.

**Mental models** (`Notes/` with `tags: [model]` or `Mind/Models/`): idea notes about thinking tools — inversion, second-order effects, base rates, opportunity cost, regression to the mean — each with a definition in your words, when it applies, when it misleads, and links to decisions where you used it. A `Models MOC` grouped by domain. The value is in the *links from decisions*: a model you have never actually applied is trivia.

**Cognitive patterns** — your own biases and tendencies, noticed in the journal ("I catastrophize on Sunday evenings", "I over-commit when flattered"): one note each in `Mind/Patterns/` with examples (links to daily notes), triggers, and the counter-move. Therapy work often produces these; see below.

## Therapy and emotional work

If you are in therapy or doing structured self-work (CBT, ACT, journaling protocols), the vault is an excellent companion — with the strictest privacy tier (Chapter 26: encrypted sync only, excluded from everything, optionally Meld Encrypt or a separate vault).

- **Session notes** (`type: meeting`, `series: Therapy`, `Mind/Therapy/`): what came up, insights, homework as tasks. Written within an hour of the session.
- **Thought records** (CBT): a template — situation, automatic thought, emotion (0–100), evidence for/against, balanced thought, emotion after. As a note per record or a table in a monthly note; a Base of records with the emotion delta as a formula shows the technique working.
- **Mood and triggers**: the daily `mood` property plus a `[trigger:: …]` inline field when notable; monthly Dataview correlations.
- **Patterns** notes (above) fed by sessions.
- **Values and ACT work**: `Values.md` is literally the ACT values exercise.
- **Gratitude, self-compassion letters, unsent letters**: `Mind/Letters/` — writing you never send. Dated. Read at the annual review, or never.
- **Crisis plan**: `Mind/Safety Plan.md` — warning signs, coping strategies, people to call, professionals, reasons. Written when well; pinned; also exported to the phone.

None of this replaces a clinician; all of it makes sessions more productive and progress visible.

## The commonplace book

A centuries-old practice: collecting passages that struck you, by theme. In Obsidian: `Mind/Commonplace/` with one note per **theme** (Attention, Courage, Grief, Craft, Money) holding quotes with sources (`— [[Author]], [[Book]] p. 45`), or one note per **quote** (`type: quote`: `author`, `source`, `themes`, `text`) with a Base grouped by theme. The per-quote approach is heavier but lets a Random note surface one quote a day and lets a person/book note show its quotes via backlinks. Either way: quotes are for *re-reading*, so build a re-reading ritual — the daily note's random quote widget (DataviewJS picks from `type: quote`), or the monthly review opens one theme.

## Reflection rituals

The periodic-notes ladder (Chapter 15) carries the schedule; this domain supplies the *content* for the reflective sections:

| Cadence | Prompt set |
| --- | --- |
| Daily (evening) | Went well · could improve · grateful · (optional) what did I avoid today? |
| Weekly | Three wins · one lesson · one change · who helped me · what drained me · what did I learn about myself |
| Monthly | Area standards met? · one principle I honoured, one I broke · a belief that shifted · a decision to log · what am I avoiding? |
| Quarterly | Direction check against Vision · what to stop · what surprised me · energy audit (what gave/took energy — from the daily `energy` data) |
| Yearly | The annual review (below) |

**Prompted journaling**: `Mind/Prompts.md` — a list of 50–100 prompts; a Templater user script picks one deterministically by day-of-year for the daily note ("What would I do today if I were not afraid?" appears on the same day every year — you get to compare answers). Sources for prompts: the *Five-Minute Journal*, Stoic journaling (morning intention, evening review), *Atomic Habits* reflection questions, your therapist.

**Stoic evening review** (Seneca/Epictetus): what did I do badly, what did I do well, what did I leave undone — three lines, template-ready.

## The annual review

Late December or the first week of January; half a day; a template in the yearly note (Chapter 15 gave the prompt list). The mind-and-self parts specifically:

1. **Read the year**: skim the twelve monthly notes; read every decision note of the year and grade the reasoning; read the beliefs updated this year; read the letters.
2. **Values check**: for each value, one example of honouring it and one of betraying it this year. Re-rank if needed.
3. **Principles**: which were used (backlinks count)? Any to add from this year's lessons? Any to retire?
4. **Patterns**: which recurred? Which improved?
5. **Themes**: the year in three words; the story you would tell about it; what it was *for*.
6. **Next year**: theme, 3–7 goals (numeric where possible), what to stop, what to protect, the vision paragraph revised.
7. **Gratitude list**: people (linked), events, luck.
8. **Letter to next year's self**: sealed in `Mind/Letters/2027 from 2026.md`, opened by a task `📅 2027-12-20`.

A **life audit** every few years (or at a transition): a longer version across all areas with 1–10 scores and a Canvas of the "wheel of life"; compare with the previous audit.

## Mind dashboard (`Mind MOC.md`)

```markdown
## Decisions due for review
![[Decisions.base#Due for review]]
## Open decisions
![[Decisions.base#Open]]
## Beliefs not re-examined in a year
```base
filters: {and: [type == "belief", last_updated < today() - "365d"]}
views: [{type: table, name: Stale, order: [file.name, confidence, last_updated]}]
```
## Least confident beliefs
```base
filters: {and: [type == "belief"]}
views: [{type: table, name: Uncertain, order: [file.name, confidence, domain], sort: [{property: confidence, direction: ASC}], limit: 10}]
```
## Principles most needed (by backlinks)
(Dataview: FROM "Mind/Principles" SORT length(file.inlinks) DESC LIMIT 10)
## Quote of the day
(DataviewJS random from type == "quote")
## Open questions
![[Open Questions]]
## Values · Principles · Vision
[[Values]] · [[Principles]] · [[Vision]] · [[Safety Plan]]
```

## Privacy, again

`Mind/` and `Journal/` are the two folders that must never leak. Excluded from Publish and any shared vault by default; synced only end-to-end encrypted (Obsidian Sync, Remotely Save with E2E, LiveSync); device disk encryption on; optionally Meld Encrypt for therapy notes and letters; a separate vault if the main vault is ever shared. Chapter 26 has the mechanics. The freedom to write honestly depends on knowing it is safe.

## Anti-patterns

- Values copied from a list. Mine your own journal and decisions.
- Decision notes only for decisions that went well. Log before the outcome is known — that is the point.
- Beliefs without confidence numbers. Vague beliefs cannot be updated.
- Mental-model collections never linked from a real decision. Trivia.
- Reflection prompts so numerous you skip them. Three at each cadence.
- Reading none of it back. The annual review is the reading.

## Key takeaways

- `Mind/` holds values (ranked, evidenced), principles (one note each, backlinkable), vision (embedded upward), open questions, decisions, beliefs, models, patterns, therapy work, a commonplace book, and prompts.
- The decision journal — context, options, reasoning, confidence, falsifiable expectation, review date, later grading — is the single highest-leverage practice here.
- Beliefs with confidence and last-updated dates make belief revision visible; models earn their place only when linked from decisions.
- Reflection content rides the periodic-notes ladder with three prompts per cadence; the annual review reads the year's decisions, beliefs, letters and values.
- This is the most private material you own; protect it accordingly.

## Next

[Chapter 26: Sync, Backup and Security →](26-sync-backup-security.md)
