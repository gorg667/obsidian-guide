# Home and Life Admin

Life admin is the unglamorous domain that, unmanaged, produces the most stress per hour: the boiler service you forgot, the passport that expired the week before the trip, the document you know you have somewhere, the appliance manual, the plumber's number, the thing you lent someone. A vault handles it with a few typed record notes, a handful of Bases with date-driven views, and recurring tasks. This chapter covers household and maintenance, documents and admin, inventory, vehicles, travel, pets, kids, gifts, contacts, and the digital-legacy document that ties it together.

## Principles

- **One record note per thing that has dates or documents** — appliance, policy, vehicle, passport, lease. Bases turn dates into alerts.
- **Recurring maintenance as recurring tasks** in `Life/Routines.md` or the relevant record note, with `🔁`.
- **Documents as attachments linked from records**, named predictably (`2026-03-lease-flat.pdf`), in `Attachments/admin/<year>/`.
- **The `Emergency & Legacy` note** is the index a trusted person could use. Everything else supports it.

## Folder and types

```text
Life/
├── Admin/
│   ├── Documents/      type: document   passports, IDs, certificates, contracts, leases
│   ├── Insurance/      type: policy
│   ├── Utilities/      type: account (kind: utility) or type: service
│   └── Emergency & Legacy.md
├── Home/
│   ├── Home.md         the property/flat note: address, landlord/mortgage, floor plan, key facts
│   ├── Appliances/     type: asset (subtype: appliance)
│   ├── Maintenance Log.md
│   ├── Pantry.md, Cleaning.md (routines)
│   └── Projects & renovations → Projects/
├── Inventory/          type: asset (electronics, furniture, tools, valuables)
├── Vehicles/           type: vehicle + service log
├── Travel/             type: trip
├── Pets/               type: pet (+ health events)
├── Kids/               per child: milestones, school, health, documents
├── Gifts.md            or type: gift-idea notes
├── Recipes/            (Chapter 20)
├── Habits/, Routines.md
└── Life MOC.md
```

## Home

`Life/Home/Home.md` — the hub: address, purchase/lease details (dates, amounts, links to documents), landlord/agent/mortgage contacts (People), utilities (links), Wi-Fi details (SSID; password in the password manager or a Meld-encrypted block), meter locations and numbers, stopcock and fuse box locations (with a photo), floor plan (image), paint colours and materials (the note you will thank yourself for), neighbours, HOA/building rules, a Base of appliances, a Base of maintenance due, and links to renovation projects.

**Appliances and systems** (`type: asset`, `subtype: appliance`): `bought`, `price`, `merchant`, `model`, `serial`, `warranty_until`, `manual_url` (or embedded PDF), `service_interval_months`, `last_service`, `location`, `status`. Formula `next_service: last_service + (service_interval_months + "M")` → Base view "Service due in 60 days". The boiler, HVAC, water heater, car, bike, dishwasher, and smoke detectors all fit.

**Maintenance log**: `Life/Home/Maintenance Log.md` with dated one-liners (`- 2026-09-02 Boiler serviced, [[Plumber Joe]], €120, next 2027-09`) — searchable, and the backlinks from People (the plumber) make "who did we use last time?" instant. Or one `maintenance` note per job if you want Bases; the log is enough for most homes.

**Recurring chores** in `Routines.md`: filters (🔁 every 3 months), gutters (every year on October 1), smoke alarm test (every month), deep-clean rotation (every week on Saturday), etc. The Today view surfaces them; the "Routines today" query in the daily note groups them.

**Renovations and home projects** are `project` notes with `area: "[[Home]]"`: quotes (Base of `type: quote` or a table), decisions (paint, fixtures — with photos), contractor People notes, before/after photos, costs summed.

## Documents and admin

`type: document`, one note per important document: `kind` (passport/ID/driver licence/birth certificate/marriage certificate/degree/contract/lease/deed/will/visa/vaccination record), `owner` (link, for family), `number` (partial or none — sensitive), `issued`, `expires`, `location` (physical: "safe, blue folder"; digital: link to the scan in `Attachments/admin/`), `renewal_notes` (how to renew, lead time). The Documents Base: "Expiring in 180 days" (passports need lead time), "By owner". Scans in the vault only if the sync is E2E-encrypted; otherwise store scans in an encrypted drive and link.

**Utilities and services**: `type: account` (`kind: utility`) or `type: service`: provider, account number (partial), `contract_ends`, `notice_period_days`, `cost`, `billing`, `login_hint`, contact. Formula `switch_by: contract_ends - (notice_period_days + "d")` → a view of contracts to review. Also appear in Subscriptions if you type them there (Chapter 21) — choose one home.

**Insurance**: `type: policy` — insurer, kind (home/contents/car/health/life/travel/liability), `policy_no` (partial), `premium`, `billing`, `renews`, `excess`, coverage summary, claim phone, documents. Base: "Renewing in 60 days"; claims as `maintenance`-style dated entries or a `## Claims` table.

**Official correspondence**: tax office, city, immigration — one note per matter (`type: case`, `status`, `deadline`, documents, timeline of letters/calls). Deadlines as tasks.

## Inventory

`type: asset` for anything you would list in an insurance claim or want to find: electronics, furniture, tools, instruments, art, jewellery, bikes. Properties as for appliances plus `category`, `estimated_value`, `photo`. Base views: "By category with Sum(price)", "By room" (group by `location`), "Warranty active". The purchase note from Chapter 21 and the asset note are the same note (`type: purchase` vs `type: asset` — pick `asset` with a `purchased` date; use `status: sold/gifted/broken` to retire).

**Lending**: `lent_to` (link) and `lent_on` properties on an asset → a Base view of things out on loan. Small but satisfying.

**Digital assets**: domains (`renews`, registrar), software licences (`key` in the password manager, `purchased`, `version`), cloud storage plans — as `asset` or `subscription`.

## Vehicles

`Life/Vehicles/<Car>.md`, `type: vehicle`: make/model/year, `plate`, `vin`, `bought`, `price`, `insurance` (link to policy), `registration_renews`, `inspection_due`, `service_interval_km`, `odometer` (updated at services), `tyres` (type, date), documents. Body: `## Service log` table (date, km, work, garage link, cost) or `type: maintenance` notes with `vehicle` link if you want Bases across vehicles. Formula `inspection_in: (inspection_due - today()) / 86400000` → alert view. Fuel logs belong in an app unless you are curious for a month.

Bikes, boats, e-scooters: same type, fewer fields.

## Travel

`type: trip` in `Life/Travel/`: `destination`, `country`, `start`, `end`, `status` (idea/planned/booked/done), `companions` (links), `budget`, `spent`, `photo`, `lat`/`long` for the Bases map view. Body sections: **Bookings** (flights, hotels, cars — confirmation numbers partial, times, links to PDFs), **Itinerary** (day-by-day; each day can link a daily note), **Packing list** (checkboxes; copied from `Templates/frag-packing-<kind>` fragments), **Research** (links to places, restaurants, clipped articles — Web Clipper with a `travel` template), **Budget** (table), **Journal** (or just link the daily notes of the trip), **Afterwards** (what worked, what to do differently, photos of the month).

Bases: cards gallery of trips by year (with `photo`), a "Planned & booked" table with days-until-start, a map of everywhere you have been (`type == "trip" && status == "done"` with lat/long), Sum of `spent` by year.

Place notes (`type: place`, `city`, `country`, `kind`: restaurant/museum/hotel/hike, `rating`, `visited` dates, `lat`/`long`) build a personal atlas over time; trips link to them; the map view shows them all. Wishlist places get `status: want`.

Packing fragments: `frag-packing-city-3-days`, `frag-packing-hiking`, `frag-packing-baby` — checklists included by Templater into the trip note when created (`tp.system.suggester` picks the kind).

## Pets

`type: pet`: species, breed, `born`, `chip`, vet (People link), insurance (link), food and dose, medications, vaccination table with `next_due`, weight log, quirks. Health events as `health-event` notes with `patient` = the pet (reuse Chapter 20's type). Recurring tasks: flea/worm treatment 🔁, vaccinations from `next_due`. A photo. If the pet has a sitter, the note *is* the handover document — export to PDF.

## Kids

Per child, `Life/Kids/<Name>/`: `<Name>.md` hub (birth details, documents links, doctor, school, allergies, sizes — clothes and shoes, updated twice a year, a lifesaver), `Milestones.md` (dated list — first words, first steps, lost teeth), `School/` (year notes: teacher, class, schedule, contacts, reports linked), `Health/` (health events with `patient`), `Memories.md` (quotes, funny things said — the note you will treasure most), photos monthly in the monthly note. Documents (passport, birth certificate) as `document` notes with `owner`. Babysitter/handover note exportable to PDF. Consider a separate shared vault with the co-parent for this folder.

## Gifts and occasions

`Life/Gifts.md`: a section per person with `- [ ] idea` items and `given:: date` inline fields on given ones; or `## Gift ideas` in each person note (Chapter 23) — the person-note approach wins because the idea surfaces when you look them up. Occasions: birthdays from People `birthday` (Base view "this month"), anniversaries as `anniversary` property on the couple's or the relationship's note, holidays as recurring tasks (`🔁 every year on December 1: plan gifts`). A `Gifts Given.md` log prevents repeats.

## Contacts and service providers

Plumber, electrician, GP, dentist, vet, accountant, cleaner, mechanic, babysitter: `type: person`, `relationship: professional`, `service` property, `rating`, `last_used`, `phone`. Base grouped by `service`. Their backlinks (maintenance log, health events, vehicle service) show history. This replaces the sticky note on the fridge.

## The emergency & legacy note

`Life/Admin/Emergency & Legacy.md` — the index someone else could follow if you were incapacitated. It links, it does not contain secrets:

- Who to call (family, doctor, lawyer, accountant, employer HR).
- Where documents are (physical locations; which folder in the vault; which cloud).
- Accounts registry (link to the Base), insurance (link), subscriptions to cancel (link), utilities (link), vehicles, home facts.
- Password manager: which one, and where the emergency access/recovery kit is (not the master password).
- Digital estate: email, social accounts, domains, 2FA device location, this vault's location and sync.
- Pets: care instructions (link). Kids: school, guardians, routines (link).
- Wishes: will location, medical directives, funeral preferences if you have them.

Export to PDF yearly (the yearly review template has a task for it); give a copy to the trusted person; keep the source in the vault. Chapter 26 covers the vault's own legacy (how someone opens it).

## Life admin dashboard (`Areas/Home.md` or `Life MOC.md`)

```markdown
## Due soon
```base
formulas:
  when: 'if(expires, expires, if(renews, renews, if(inspection_due, inspection_due, "")))'
filters:
  and:
    - 'type == "document" || type == "policy" || type == "vehicle" || type == "subscription"'
    - 'formula.when && formula.when <= today() + "90d"'
views:
  - type: table
    name: Next 90 days
    order: [file.name, type, formula.when]
    sort: [{property: formula.when, direction: ASC}]
```

## Service due
(Appliances Base: next_service ≤ today + 60d)

## Routines this week
```tasks
not done
path includes Routines
happens this week
```

## Trips
![[Trips.base#Planned & booked]]

## Out on loan
(Assets Base: lent_to not empty)

## Providers
(People Base: relationship == professional, grouped by service)

## Records
[[Home]] · [[Emergency & Legacy]] · [[Maintenance Log]] · [[Gifts]] · [[Pantry]]
```

## Anti-patterns

- Scanning every piece of paper into the vault. Scan what has a date or a legal function; recycle the rest.
- One "Admin" note with 300 lines. Typed records + Bases.
- Maintenance in your head. `🔁` tasks and the service-due view.
- Storing passwords, full card/account numbers, or scans in an unencrypted synced vault.
- Never exporting the emergency note. It exists for someone who cannot open Obsidian.

## Key takeaways

- One typed record note per thing with dates or documents — appliances, documents, policies, utilities, vehicles, assets, trips, pets — and Bases date-driven views turn them into alerts.
- Recurring maintenance and chores live as 🔁 tasks; the maintenance log and provider People notes hold history via backlinks.
- Travel gets trip notes with bookings, itinerary, packing fragments, budget, and a personal atlas of place notes on a map.
- Kids and pets get hub notes that double as handover documents.
- The Emergency & Legacy note is the index for someone else — export yearly, contain no secrets.

## Next

[Chapter 23: Relationships and People →](23-relationships-and-people.md)
