# Finance

Money is the domain where "plain text you own" matters most and where Obsidian is least obviously suited — it is not a spreadsheet, not a bank aggregator, not accounting software. The right design uses Obsidian for what it does well (records, decisions, subscriptions, net-worth snapshots, financial narrative, documents) and delegates transaction-level bookkeeping to a tool built for it — or, for the plain-text purists, to a ledger format that Obsidian can host and query. This chapter covers both paths and the Bases/Dataview dashboards that make the numbers visible.

## Choose your depth

| Level | What lives in Obsidian | Tool for the rest |
| --- | --- | --- |
| **Light** (most people) | Subscriptions, big purchases, accounts registry, net-worth snapshots (monthly), financial decisions, tax notes, documents index | Bank app + a budgeting app (YNAB, Actual, a spreadsheet) |
| **Medium** | Above + a monthly budget note with actuals typed in, + expense log of *notable* transactions | Same |
| **Full plain-text** | Above + every transaction in a **plain-text accounting** ledger (Ledger/hledger/Beancount) stored in the vault | The ledger CLI for reports; Obsidian for editing, notes, and dashboards |

The guide's default is **Light with a monthly snapshot** — it captures 90% of the value (you know what you own, owe, pay for, and decided) at 5% of the effort. Full plain-text is excellent if you enjoy it.

## Folder and types

```text
Finance/
├── Accounts/          type: account     one per bank/broker/loan/card
├── Subscriptions/     type: subscription
├── Purchases/         type: purchase    notable purchases (warranty, receipts)
├── Snapshots/         type: networth    monthly: 2026-09.md
├── Budgets/           yearly/monthly budget notes
├── Taxes/             per tax year: documents index, notes, deadlines
├── Decisions/         (or Mind/Decisions with area: Finances)
├── Ledger/            (full path only) main.ledger / *.beancount
└── Finances MOC.md
Areas/Finances.md      the area note
```

## Accounts registry

`type: account`, one note per account: `institution`, `kind` (checking/savings/brokerage/retirement/credit/loan/mortgage/crypto/cash), `currency`, `owner`, `opened`, `closed`, `rate` (interest %), `status`, `login_hint` (never the password — a pointer to your password manager entry), `statements_url`, `notes`. Body: why the account exists, fees, quirks, beneficiaries, what to do with it in an emergency. An Accounts Base grouped by `kind` is your financial map — the document your partner or executor needs (Chapter 22, digital legacy).

## Subscriptions

The single most valuable finance Base. `type: subscription`: `cost`, `currency`, `billing` (monthly/yearly), `renews` (next date), `status` (active/cancelled/trial), `category` (software/media/utilities/insurance/fitness/…), `account` (link to the paying account), `cancel_url`, `shared_with`. The Base (Chapter 10) shows normalized monthly/yearly cost with `Sum` summaries and a "Renewing in 30 days" view. Review at the monthly snapshot: anything unused → cancel, `status: cancelled`, note the date. Annual subscriptions get a task `📅` one week before renewal.

## Purchases and warranties

For anything over a threshold you set (say €100) or with a warranty: `type: purchase`: `date`, `item`, `price`, `merchant`, `category`, `account`, `warranty_until`, `serial`, `receipt` (embed of the PDF/photo in `Attachments/receipts/`), `manual_url`, `location` (where it lives at home), `status` (owned/sold/gifted/broken). This doubles as the **home inventory** (Chapter 22) and the insurance claim list. Base views: "Warranty expiring in 90 days", "By category with Sum", "Owned electronics".

## Monthly snapshot (net worth)

`Finance/Snapshots/2026-09.md`, `type: networth`, created from a template on the first weekend of the month:

```markdown
---
type: networth
date: 2026-09-01
cash: 
investments: 
retirement: 
property: 
other_assets: 
debts: 
---
# Snapshot <% tp.date.now("YYYY-MM") %>

## Balances
| Account | Balance |
| --- | --- |
<%* for (const a of app.vault.getMarkdownFiles().filter(f => f.path.startsWith("Finance/Accounts/"))) tR += `| [[${a.basename}]] | |\n`; %>

## Month
- Income:
- Spend:
- Saved / invested:
- Notable: 

## Notes
```

Bases formula `net: cash + investments + retirement + property + other_assets - debts` with a Base sorted by date gives the net-worth series; `Range` summary shows the year's change. Chart it with Obsidian Charts from a DataviewJS array if you like a line. Ten minutes a month; the most motivating finance habit there is.

## Budget

`Finance/Budgets/2026.md`: a table of categories × planned monthly amount; the monthly snapshot records actuals per category (typed from the bank/budget app's summary). A DataviewJS block compares planned vs actual for the month. Keep categories to ~12. If you use YNAB/Actual, do not duplicate the envelope logic — just paste the month's category totals.

## Expense log (medium depth)

If you want *notable* transactions searchable without full bookkeeping: a single `Finance/Ledger/2026 Expenses.md` note with one line per item — `- 2026-09-03 Dentist [amount:: 120] [cat:: health] [acct:: Checking]` — queried by the Dataview monthly-by-category query from Chapter 12. Or one `type: expense` note per item if you want Bases (heavier; only for big items). Do not try to log every coffee this way; that is what the full ledger is for.

## Full plain-text accounting

**Ledger**, **hledger**, and **Beancount** are double-entry accounting systems whose data is a text file:

```text
2026-09-03 * "Dentist" "Check-up"
  Expenses:Health:Dental      120.00 EUR
  Assets:Bank:Checking
```

Why this belongs in Obsidian: the ledger file lives in the vault (`Finance/Ledger/main.beancount`), is versioned with the rest, edited with syntax highlighting (the **Ledger** plugin adds a transaction form, autocompletion of accounts/payees, and a dashboard; Beancount users use a code block with `beancount` highlighting and the **Shell commands** plugin to run `bean-report`/`fava`), and its reports can be rendered into notes via Shell commands (`hledger balance -M` → output into a code block in the monthly snapshot).

Import: banks export CSV; hledger/beancount have importers with rules files; a Shell command or CLI script runs the import and appends to the ledger. Reconcile monthly.

Who should do this: people who like it. The reward is complete, queryable, permanent financial history in a format that will open in 2050. The cost is 15–30 minutes a week.

## Investments

A `Finance/Investments.md` note (or the Finances area note) with the *policy*: allocation targets, rebalancing rules, contribution schedule, what you will not do. Holdings: a table per account updated at the monthly snapshot (ticker, units, value) or left to the broker app with only totals in the snapshot. Investment **decisions** (buy/sell/change allocation) as `decision` notes with `area: Finances` — the review-after-six-months property is precisely what investing needs. Do not track prices in Obsidian.

## Taxes

`Finance/Taxes/2026.md`: deadlines as tasks (`📅`), a checklist of documents needed (with links to `Attachments/tax/2026/` as they arrive), a table of deductible items logged through the year (pull from purchases with `deductible: true` via a Base view), notes on decisions and the accountant's advice, and the final filed return PDF linked. A yearly template pre-fills the checklist. Recurring task in `Routines.md`: "Photograph and file receipts" weekly.

## Debts and loans

`type: account` with `kind: loan`, plus `principal`, `rate`, `term_months`, `payment`, `payoff_date`. A payoff plan as a table; extra payments logged; a `decision` note if you change strategy. The Accounts Base's loans view with `Sum` of balances is the debt dashboard.

## Insurance

`Life/Admin/Insurance/` (Chapter 22) or `Finance/`: one note per policy: `insurer`, `policy_no`, `kind`, `premium`, `billing`, `renews`, `coverage` summary, `claim_phone`, documents linked. A Base view "Renewing in 60 days"; premiums also appear in the Subscriptions total if you type them as subscriptions with `category: insurance` — do one or the other, not both.

## Financial decisions and narrative

The part no app does: **why**. Big purchases, job/comp choices, rent-vs-buy, moving money between accounts, changing allocation, taking a loan — each a `decision` note with context, options, reasoning, expected outcome, review date. Over years this is a record of your financial judgement improving (or not). Link decisions from the yearly review.

The yearly note's Finances section: net worth change, savings rate, biggest expenses, subscriptions trimmed, decisions made, one paragraph of narrative, and next year's targets as `goal` notes with numeric `target`/`current`.

## Shared finances

With a partner: a shared vault or shared folder synced between two people (Obsidian Sync supports it; Remotely Save with a shared bucket; or Git). Keep it to the shared parts — accounts registry, subscriptions, snapshots, big decisions. Personal spending stays personal.

## Dashboards

**Finances area note**:

```markdown
## Standard
Savings rate ≥ 20% · emergency fund 6 months · no card debt · net worth snapshot monthly · taxes filed by …

## Subscriptions
![[Subscriptions.base#Active]]
![[Subscriptions.base#Renewing in 30 days]]

## Net worth
```base
filters: {and: [type == "networth"]}
formulas:
  net: 'cash + investments + retirement + property + other_assets - debts'
views:
  - type: table
    name: Series
    order: [file.name, formula.net, cash, investments, debts]
    sort: [{property: date, direction: DESC}]
    limit: 13
    summaries: {formula.net: Range}
```

## Warranties expiring
```base
filters: {and: [type == "purchase", warranty_until >= today(), warranty_until <= today() + "90d"]}
views: [{type: list, name: Expiring, order: [file.name, warranty_until, merchant]}]
```

## Open finance tasks
```tasks
not done
path includes Finance
sort by due
```

## Decisions
```base
filters: {and: [type == "decision", area == link("Finances")]}
views: [{type: table, name: Decisions, order: [file.name, date, status, review_on], sort: [{property: date, direction: DESC}]}]
```
```

## Security

- Never store passwords, full card numbers, or account numbers beyond the last four digits. Point to the password manager.
- Statements and tax documents in `Attachments/` are sensitive: E2E-encrypted sync only; consider **Meld Encrypt** for the accounts registry or a separate encrypted vault for finance if the main vault is shared or published.
- The emergency/legacy document (Chapter 22) tells a trusted person *where* things are, not *how to get in*.

## Anti-patterns

- Rebuilding a budgeting app in Dataview. Use a budgeting app; keep the narrative and records in Obsidian.
- Tracking prices or daily balances. Monthly snapshots.
- A subscriptions list that is never reviewed. Embed it in the monthly template.
- Receipts as a shoebox. Photograph weekly into `Attachments/receipts/YYYY/` and link from purchase notes.

## Key takeaways

- Pick a depth: Light (records + monthly snapshot) is the default; full plain-text accounting (Ledger/hledger/Beancount in the vault) for those who enjoy it.
- Accounts registry, subscriptions (with monthly/yearly Sum), purchases with warranties/receipts, monthly net-worth snapshots, taxes per year, and decision notes are the core types.
- Bases summaries and formulas make subscriptions totals, net-worth series, and warranty alerts free; Dataview handles inline expense logs.
- Obsidian's unique contribution to finance is the *why*: decisions with review dates and the yearly narrative.
- Never store secrets; encrypt or separate sensitive finance material.

## Next

[Chapter 22: Home and Life Admin →](22-home-life-admin.md)
