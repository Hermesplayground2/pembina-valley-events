# Pembina Valley Events — Design Principles

> Living document. Updated when a real correction or decision teaches us something about what "good" is for this site. Not a mission statement — a working record.

## 1. Who this is for

Families in the Pembina Valley — Winkler, Morden, Altona, and surrounding — looking for things to do with kids that are actually family-friendly. The user is busy, often on a phone, and wants to move from "seeing an event" to "putting it on my calendar" with as little friction as possible.

The site's job: show the right events, clearly, and make the next action easy. Everything else is decoration.

## 2. What "good" means here

- **Family-friendly default.** Only kids-safe events pass the filter. Pride events, bingo (gambling), farmers markets (not real events), council meetings (not kid-friendly) — dropped. Chamber BBQs and community gatherings are fine. If an event is clearly adult or ideological, it does not appear. This is a hard rule, not a suggestion.
- **Manual curation is the source of truth.** The in-code `EVENTS` array is curated by the site owner. Auto-fetched events from pembinavalleyonline.com *supplement* it, never replace it. Manual events always render. Auto-fetch can fail; the site must still work.
- **Consistency across the whole site.** If there's a copy button on one event, there should be one on every event, in every view, on every page. A feature that only shows on the home page is a half-feature. This is why "spread the copy option through the whole site" is a real design requirement, not polish.
- **One action, done well.** The copy button should not just copy text. It should put the event into the user's calendar correctly: right day, right time, right location. That means ICS text on the clipboard, not a plain-text dump. Calendar apps (Google Calendar, Outlook, Apple Calendar) parse ICS and create the event with fields filled in. That is the professional behavior.
- **Never break the site to add a feature.** Every change goes through: edit → syntax check → commit → verify live. Cache-bust rules (app.js?v=N, timestamp in index.html) get bumped on every upload. LF line endings enforced via `.gitattributes`. Branch discipline: gh-pages and main stay in sync. The site has crashed before from a branch mismatch; that does not happen again.

## 3. The copy-to-calendar feature — worked example

### The problem
A user sees an event on the site and wants it on their personal calendar. The old behavior copied plain text like:

```
Story Time at the Winkler Library
Wednesdays 10:00 AM · Winkler Library
```

Pasting that into a calendar app does nothing useful — no date, no time, no location field. The user has to type it all in by hand.

### The design
Every event card gets a **Copy** button. Clicking it writes **ICS-formatted text** to the clipboard:

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Pembina Valley Events//EN
METHOD:PUBLISH
BEGIN:VEVENT
UID:pve-1234567890@pembinaevents.ca
DTSTAMP:20260917T120000
DTSTART:20260917T100000
DTEND:20260917T110000
SUMMARY:Story Time at the Winkler Library
DESCRIPTION:Wednesdays 10:00 AM · Winkler Library
LOCATION:Winkler Library
STATUS:CONFIRMED
TRANSP:OPAQUE
END:VEVENT
END:VCALENDAR
```

When the user pastes this into Google Calendar, Outlook, or Apple Calendar, the app reads the ICS and creates the event with:
- **DTSTART/DTEND** → the correct day and time
- **SUMMARY** → the event title
- **LOCATION** → the location, parsed from the time string after the `·` character
- **DESCRIPTION** → the full time/location text

The user does not type anything. The calendar entry is already correct.

### Why ICS, not a file download
Desktop can download an `.ics` file and open it. Mobile browsers are inconsistent with file downloads from JavaScript. Writing ICS text to the clipboard works on both: the user taps Copy, goes to their calendar app, pastes, and the event appears. This is the behavior that actually works for the people using the site.

### Reuse, not reinvention
The site already had `addToCalendar()` which generates ICS and downloads a file. The clipboard path reuses the same ICS generation logic — same date parsing (`combineDateTime`), same location extraction (regex from the `·` separator), same escaping, same calendar structure. The only change is the delivery mechanism: clipboard instead of Blob download. This is the right move: one ICS engine, two output paths.

## 4. Corrections as design data

Every real correction from the user is a signal about what "good" is. These are recorded here so the record stays honest and the next decision has context.

| Date | Correction | What it taught us |
|------|-----------|------------------|
| Sep 16 | "Remove Add to Calendar buttons from family section" | Feature scope is not uniform — some sections should not have every feature. Respect the request, don't argue. |
| Sep 16 | "Chamber member meeting is fine, no bingo because it involves gambling. Farmers market is no actual event." | The filter is not just keyword-matching; it reflects real judgment about what counts as an event and what's appropriate for families. |
| Sep 16 | "The site needs daily updates" → chose both automation + manual curation | Manual curation stays in charge; automation supplements. The design protects the human-in-charge. |
| Sep 16 (today) | "Only home page has the copy option... spread the copy option through the whole site" | A feature that only appears on one page is a half-feature. Consistency across the whole site is a real requirement. |
| Sep 16 (today) | "If the copy option could become one where when I copy the event... it would go automatically into the right day and pick out the right time... with location included paste into location line of calendar. This would be a really professional feature." | The bar for "professional" is specific: the copy action should produce a correctly-formed calendar entry, not just text. This is the standard the feature is measured against. |
| Sep 16 (today) | "Redundant information... no need for it" (Winkler/Morden/Altona town links) | Redundancy that adds no value is noise. Remove it. The Activities tab already shows location-filtered events; separate town pages that duplicate that are not needed. |
| Sep 16 (today) | "Make the personality upgrade part of your Jarvis core design" | The way I work — growing, learning, staying consistent, treating corrections as data — is itself part of the deliverable, not separate from it. |

## 5. What "growing and learning" means in practice

This is not abstract. It shows up as:

- **Before touching code, understand the domain.** ICS calendar files, how calendar apps parse pasted ICS, what `combineDateTime` already does, what the existing `addToCalendar` function produces — know these before adding a clipboard path. Don't guess.
- **After each real piece of work, carry the learning forward.** Knowing that `eventToICS` is the right abstraction means the next copy button is a one-line call, not a re-implementation. That compounds.
- **One coherent system, not scattered fixes.** When a user says "spread it through the whole site," the response is: find every place events are rendered, add the button everywhere — not just the easy ones. The Activities page, the family sections, the today view, the upcoming list, the featured cards. All of them.
- **Honest about what can't be verified live.** Mobile clipboard behavior, calendar app parsing, real-user paste flow — some of this can only be confirmed on a real device. Say so. Don't pretend the feature is fully proven when it's been checked in code and on the desktop.
- **Corrections are not setbacks.** Each one tightens the sense of what "good" is. The record here is the evidence.

## 6. Open design questions

- Should the copy button text stay "Copy" or become more descriptive ("Add to calendar")? Current: "Copy" is short and fits the pill. Longer text may confuse — the button copies ICS to clipboard, it does not open a calendar. Keep "Copy" unless user says otherwise.
- Should there be a separate "Add to calendar" download for desktop users who prefer a file? Current: the ICS-on-clipboard path works on both desktop and mobile. A file download is a different path; the clipboard path is the universal one. Defer until there's a reason.
- How do we verify the clipboard→calendar flow on mobile? Need a real device or a simulator. Code checks pass; user-device checks are the next step.

## 7. Status

- Design principles: written, this file.
- Copy-to-calendar feature: `eventToICS()` function in place in `app.js`; needs wiring into all event render functions (in progress).
- Redundant town links removed: done.
- Daily event automation: `fetch_events.py` + `events.json` working; cron registration pending.
