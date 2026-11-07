"""Curated local events that the crawlers do not carry.

The fetchers only see pembinavalleyonline.com and gwevents.ca. Programs run by
the City of Morden recreation department are not listed on either, so they are
maintained by hand in `manual_events.json` and merged into every fetch.

Two shapes are supported:

  fixed date   {"date": "2026-11-24", ...}
  recurring    {"weekdays": [2], ...}   -> next occurrence computed at merge
               time, so an ongoing weekly program never silently drops off
               the site once its representative date passes.

Dedup rule matches the rest of the pipeline: same title + same date = one record.
"""
from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any, Iterable

REPO_DIR = Path(__file__).resolve().parent
MANUAL_EVENTS_JSON = REPO_DIR / "manual_events.json"

# Monday=0 .. Sunday=6, matching datetime.date.weekday()
WEEKDAYS = {
    "mon": 0, "monday": 0,
    "tue": 1, "tues": 1, "tuesday": 1,
    "wed": 2, "weds": 2, "wednesday": 2,
    "thu": 3, "thur": 3, "thurs": 3, "thursday": 3,
    "fri": 4, "friday": 4,
    "sat": 5, "saturday": 5,
    "sun": 6, "sunday": 6,
}


def _today() -> datetime.date:
    """Manitoba-local today, matching fetch_events.site_today()."""
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo("America/Winnipeg")).date()
    except Exception:
        return datetime.date.today()


def next_occurrence(weekdays: Iterable[int],
                    today: datetime.date | None = None) -> datetime.date:
    """Earliest date >= today whose weekday is in `weekdays`."""
    today = today or _today()
    wanted = {int(d) for d in weekdays}
    for offset in range(7):
        candidate = today + datetime.timedelta(days=offset)
        if candidate.weekday() in wanted:
            return candidate
    return today


def load_manual(today: datetime.date | None = None) -> list[dict[str, Any]]:
    """Read the curated list, resolving recurring entries to a concrete date."""
    if not MANUAL_EVENTS_JSON.exists():
        return []
    try:
        raw = json.loads(MANUAL_EVENTS_JSON.read_text(encoding="utf-8"))
    except Exception:
        return []
    today = today or _today()
    out: list[dict[str, Any]] = []
    for entry in raw.get("events", []):
        ev = dict(entry)
        if not ev.get("date"):
            days = ev.pop("weekdays", None)
            if not days:
                continue
            nums: list[int] = []
            for d in days:
                if isinstance(d, int) and 0 <= d <= 6:
                    nums.append(d)
                elif isinstance(d, str) and d.strip().lower() in WEEKDAYS:
                    nums.append(WEEKDAYS[d.strip().lower()])
            if not nums:
                continue
            ev["date"] = next_occurrence(nums, today).isoformat()
        ev.setdefault("source", "local_curation")
        out.append(ev)
    return out


def merge(events: list[dict[str, Any]],
          today: datetime.date | None = None) -> list[dict[str, Any]]:
    """Append curated events the crawl did not already carry, then re-sort.

    Mutates and returns `events`. A recurring entry whose computed date already
    exists is skipped, so running twice on the same day is a no-op.
    """
    have = {(e.get("title", "").strip().lower(), e.get("date")) for e in events}
    added = 0
    for ev in load_manual(today):
        key = (ev.get("title", "").strip().lower(), ev.get("date"))
        if key in have:
            continue
        events.append(ev)
        have.add(key)
        added += 1
    if added:
        events.sort(key=lambda e: (e.get("date", ""), e.get("time", "")))
    return events
