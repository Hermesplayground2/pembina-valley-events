"""Extra event sources for pembinaevents.ca.

The main crawler (fetch_events.py) only sees pembinavalleyonline.com.  This
module adds sources that publish machine-readable feeds but are not covered
by that crawl -- starting with the South Central Regional Library, which
exposes its calendar as a standard iCal stream.

Nothing here is required for the site to work: every entry point returns an
empty list on failure so a dead upstream feed can never break the crawl.
"""
from __future__ import annotations

import datetime as _dt
import html as _html
import re
import ssl
import urllib.request
from pathlib import Path
from typing import Any, Iterable

REPO_DIR = Path(__file__).resolve().parent

UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,*/*;q=0.8",
    "Accept-Language": "en-CA,en-US;q=0.9,en;q=0.8",
    "Accept-Encoding": "identity",
}

_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE

SCRL_ICAL = "https://scrl.mb.libraries.coop/?post_type=tribe_events&ical=1&eventDisplay=list"
WINKLER_ARTS_EVENTS = "https://winklerarts.com/events/"
SCRL_SOURCE = "South Central Regional Library"
SCRL_CATEGORY = "community"


def fetch(url: str, timeout: int = 45) -> str:
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=timeout, context=_CTX).read().decode("utf-8", "replace")


def _clean(text: str) -> str:
    """Collapse whitespace and decode entities, including double-escaped ones."""
    previous = None
    text = _html.unescape(text or "")
    while text != previous:
        previous = text
        text = _html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def _unescape_ics(text: str) -> str:
    return (
        (text or "")
        .replace("\\,", ",")
        .replace("\\;", ";")
        .replace("\\n", " ")
        .replace("\\N", " ")
        .replace("\\\\", "\\")
    )


def _unfold(text: str) -> str:
    return re.sub(r"\r?\n[ \t]", "", text)


def scrl_events() -> list[dict[str, Any]]:
    """Parse the SCRL iCal feed into the site's event schema."""
    raw = _unfold(fetch(SCRL_ICAL))
    out: list[dict[str, Any]] = []
    for block in raw.split("BEGIN:VEVENT")[1:]:
        block = block.split("END:VEVENT")[0]
        summary = re.search(r"^SUMMARY:(.*)$", block, re.M)
        start = re.search(r"^DTSTART[^:]*:(\d{8})(?:T(\d{2})(\d{2}))?", block, re.M)
        location = re.search(r"^LOCATION:(.*)$", block, re.M)
        url = re.search(r"^URL:(.*)$", block, re.M)
        uid = re.search(r"^UID:(.*)$", block, re.M)
        if not (summary and start):
            continue
        try:
            day = _dt.datetime.strptime(start.group(1), "%Y%m%d").date()
        except ValueError:
            continue

        clock = ""
        if start.group(2) and start.group(3):
            hour24 = int(start.group(2))
            meridiem = "PM" if hour24 >= 12 else "AM"
            hour = hour24 % 12 or 12
            clock = f"{hour}:{start.group(3)} {meridiem}"

        bits = [b for b in (clock, _clean(_unescape_ics(location.group(1) if location else ""))) if b]
        out.append({
            "id": f"scrl-{_clean(uid.group(1) if uid else summary.group(1))}",
            "title": _clean(_unescape_ics(summary.group(1))),
            "time": " · ".join(bits) if bits else "All day",
            "date": day.isoformat(),
            "link": (url.group(1).strip() if url else "https://scrl.mb.libraries.coop/calendar/"),
            "source": SCRL_SOURCE,
            "category": SCRL_CATEGORY,
            "description": _clean(_unescape_ics(block.split("DESCRIPTION:", 1)[1].split("\n", 1)[0]))
                            if "DESCRIPTION:" in block else "",
        })
    out.sort(key=lambda e: (e["date"], e["time"]))
    return out


def winkler_arts_events() -> list[dict[str, Any]]:
    """Scrape the Winkler Arts + Culture list page (Modern Events Calendar skin).

    MEC emits a month divider (<h5>November 2026</h5>) before each group of
    events, which is the only place the year appears -- the per-event date
    label is just "09 Nov".  Splitting on the divider keeps the year honest.
    """
    page = fetch(WINKLER_ARTS_EVENTS)
    parts = re.split(
        r'<div class="mec-month-divider"[^>]*>\s*<h5[^>]*>([^<]+)</h5>', page
    )
    out: list[dict[str, Any]] = []
    for i in range(1, len(parts) - 1, 2):
        label = _clean(parts[i])
        try:
            month = _dt.datetime.strptime(label, "%B %Y")
        except ValueError:
            continue
        section = parts[i + 1]
        for block in re.split(r'<article class="mec-event-article', section)[1:]:
            head = re.search(
                r'<h3 class="mec-event-title">\s*<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>',
                block,
            )
            day = re.search(r'<span class="mec-start-date-label">([^<]+)</span>', block)
            start = re.search(r'<span class="mec-start-time">([^<]+)</span>', block)
            end = re.search(r'<span class="mec-end-time">([^<]+)</span>', block)
            if not (head and day):
                continue
            try:
                when = _dt.datetime.strptime(
                    f"{_clean(day.group(1))} {month.year}", "%d %b %Y"
                ).date()
            except ValueError:
                continue
            clock = ""
            if start and end:
                clock = f"{_clean(start.group(1))} - {_clean(end.group(1))}"
            elif start:
                clock = _clean(start.group(1))
            out.append({
                "id": f"winkler-arts-{head.group(1).rstrip('/').split('/')[-1]}",
                "title": _clean(head.group(2)),
                "time": clock,
                "date": when.isoformat(),
                "link": head.group(1),
                "source": "Winkler Arts + Culture",
                "category": SCRL_CATEGORY,
                "description": "",
            })
    out.sort(key=lambda e: (e["date"], e["time"]))
    return out


def extra_events() -> list[dict[str, Any]]:
    """Every event from the extra sources, best-effort."""
    events: list[dict[str, Any]] = []
    try:
        events.extend(scrl_events())
    except Exception as exc:  # noqa: BLE001 - upstream feeds come and go
        print(f"[fetch_extra_sources] SCRL feed failed: {exc!r}", flush=True)
    try:
        events.extend(winkler_arts_events())
    except Exception as exc:  # noqa: BLE001
        print(f"[fetch_extra_sources] Winkler Arts scrape failed: {exc!r}", flush=True)
    return events


def merge(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Append extra-source events the crawl did not already carry, then re-sort."""
    have = {(e.get("title", "").strip().lower(), e.get("date")) for e in events}
    added = 0
    for ev in extra_events():
        key = (ev.get("title", "").strip().lower(), ev.get("date"))
        if key in have:
            continue
        events.append(ev)
        have.add(key)
        added += 1
    if added:
        print(f"[fetch_extra_sources] added {added} event(s)", flush=True)
        events.sort(key=lambda e: (e.get("date", ""), e.get("time", "")))
    return events


if __name__ == "__main__":
    for ev in extra_events():
        print(ev["date"], "|", ev["title"], "|", ev["time"])
