#!/usr/bin/env python3
"""
fetch_events.py — daily auto-fetch of Pembina Valley events.

Pulls from pembinavalleyonline.com/events (the only source that returns
real HTML; morden.ca / winklerchamber.com / visitwinkler.ca are 403/empty).

Outputs events.json into the pembina-clone repo root.  Served by GitHub
Pages at https://pembinaevents.ca/events.json and loaded at runtime by
app.js (merged with the in-code EVENTS array).

Filter (per user values — common sense, fact, reality; Bible true; kids-friendly):
  - Pride     → drop (ideological)
  - Bingo     → drop (gambling)
  - Farmers Market → drop (not an actual event)
  - Council Meeting → drop (civic, not kids-friendly)
  - Everything else passes.

Reliable:
  - Parses each page independently (no concatenated-blob split bugs).
  - Event matching is order-independent (href and class can appear in any order).
  - Stops fetching once the 14-day window is covered or 30 pages fetched.
  - On any failure the previous events.json is untouched.
  - Atomic write via temp file + rename.
  - Rejects files < 500 bytes (likely failed parse) and restores previous.
  - Skips commit/push when content is byte-identical to what is already committed.
"""

from __future__ import annotations
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Any

REPO_DIR = Path(__file__).resolve().parent
EVENTS_JSON = REPO_DIR / "events.json"
LOG_PREFIX = "[fetch_events]"

# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

DROP_TERMS = [
    "pride",
    "bingo",
    "farmers market",
    "council meeting",
]


def should_keep(event: dict[str, Any]) -> bool:
    combined = f"{(event.get('title') or '')} {(event.get('description') or '')}".lower()
    for term in DROP_TERMS:
        if term in combined:
            return False
    return True


# HTML entity decoder — turns &#39; → ', &amp; → &, etc.
try:
    import html as _html_mod
    unescape = _html_mod.unescape
except ImportError:
    def unescape(text: str) -> str:
        return text


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def fetch_page(url: str) -> str:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-CA,en-US;q=0.9,en;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return data.decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

# Match <a> tags and capture attributes + inner HTML.  Attribute order
# in the HTML is href-first, so a fixed-order regex fails — this one
# captures the full attribute string and we filter afterward.
A_TAG_RE = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.S)

# Day-block header: captures the full date string inside <h2>.
DAY_HEADER_RE = re.compile(
    r"<div class=\"day\">\s*<h2>(.*?)</h2>", re.S
)

TITLE_RE = re.compile(r"<h3[^>]*>(.*?)</h3>", re.S)
TIME_RE = re.compile(r"<p>\s*(\d{1,2}(?::\d{2})?\s*(?:AM|PM)?)\s*</p>", re.I)
LOCATION_RE = re.compile(
    r'<div[^>]*id="location"[^>]*>\s*<p>(.*?)</p>', re.S
)

# Description: real event text lives in the article-body <p> tags.
ARTICLE_BODY_RE = re.compile(r'<div class="article-body">(.*?)</div>\s*<div class="', re.S)
DESC_P_RE = re.compile(r'<p>(.*?)</p>', re.S)

def _extract_description(html: str) -> str:
    """Pull the human-readable description from an event page's article-body."""
    m = ARTICLE_BODY_RE.search(html)
    if not m:
        return ""
    body = m.group(1)
    # Drop the event-info block (Location heading + address + map embed) so the
    # address paragraph does not leak into the description text.
    body = re.sub(r'<div class="event-info">[\s\S]*?</div>\s*</div>', '', body, flags=re.S)
    parts: list[str] = []
    for pm in DESC_P_RE.finditer(body):
        raw = pm.group(1)
        # Skip ad injection <p> blocks.
        if "gpt-ad" in raw.lower():
            continue
        clean = _clean_text(raw)
        if not clean:
            continue
        # Skip location-only paragraphs (the map <p> repeats the address).
        if clean.lower() in ("location",):
            continue
        parts.append(clean)
    return " ".join(parts)


def _strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def _clean_text(text: str) -> str:
    text = _strip_tags(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _parse_date(text: str) -> datetime.date | None:
    for fmt in (
        "%A, %B %d, %Y",
        "%A, %B %d %Y",
        "%a, %b %d, %Y",
        "%A, %B %d,%Y",
    ):
        try:
            return datetime.datetime.strptime(text.strip(), fmt).date()
        except ValueError:
            continue
    return None


def iter_event_wraps(body: str):
    """
    Yield (href, inner_html) for each <a> that has class="event-wrap"
    and an href starting with /events/.  Order-independent.
    """
    for m in A_TAG_RE.finditer(body):
        attrs = m.group(1)
        if 'class="event-wrap"' not in attrs:
            continue
        href_m = re.search(r'href="([^"]+)"', attrs)
        if not href_m:
            continue
        href = href_m.group(1)
        if not href.startswith("/events/"):
            continue
        yield href, m.group(2)


def parse_single_page(html: str, max_age_days: int = 14) -> list[dict[str, Any]]:
    """
    Parse ONE page.  Returns events whose dates fall within `max_age_days`
    of today.
    """
    events: list[dict[str, Any]] = []
    today = datetime.date.today()
    window_end = today + datetime.timedelta(days=max_age_days)
    seen_ids: set[str] = set()

    # Split on day headers to get (header, body) pairs.
    parts = DAY_HEADER_RE.split(html)
    for i in range(1, len(parts), 2):
        header_text = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""

        day_date = _parse_date(header_text)
        if day_date is None:
            continue
        if day_date < today:
            continue
        if day_date > window_end:
            continue

        for href, inner in iter_event_wraps(body):
            link_match = re.search(r"/events/(\d+)", href)
            event_id = f"/events/{link_match.group(1)}" if link_match else href
            if event_id in seen_ids:
                continue
            seen_ids.add(event_id)

            title_m = TITLE_RE.search(inner)
            title = unescape(_clean_text(title_m.group(1))) if title_m else ""

            time_m = TIME_RE.search(inner)
            time_str = time_m.group(1).strip() if time_m else ""

            loc_m = LOCATION_RE.search(inner)
            location = unescape(_clean_text(loc_m.group(1))) if loc_m else ""

            time_display = f"{time_str} · {location}" if location else time_str

            # Fetch the event page once to pull the real description text.
            try:
                page_html = fetch_page(f"https://www.pembinavalleyonline.com{event_id}")
                description = _extract_description(page_html)
            except Exception:
                description = ""

            events.append({
                "id": event_id,
                "title": title,
                "time": time_display,
                "date": day_date.isoformat(),
                "link": f"https://www.pembinavalleyonline.com{event_id}",
                "source": "pembinavalleyonline.com",
                "description": description,
            })

    events.sort(key=lambda e: (e["date"], e["time"]))
    return events


def fetch_events(max_days: int = 14, max_pages: int = 30) -> list[dict[str, Any]]:
    """
    Fetch up to `max_pages` pages, parse each, return events in the
    next `max_days`.
    """
    all_events: list[dict[str, Any]] = []
    today = datetime.date.today()
    window_end = today + datetime.timedelta(days=max_days)
    seen_ids: set[str] = set()
    seen_title_date: set[tuple[str, str]] = set()
    pages_fetched = 0

    for page in range(1, max_pages + 1):
        url = f"https://www.pembinavalleyonline.com/events?page={page}"
        try:
            html = fetch_page(url)
        except Exception as exc:
            log(f"fetch page {page} failed: {exc}")
            continue

        pages_fetched += 1
        page_events = parse_single_page(html, max_age_days=max_days)
        log(f"page {page}: {len(page_events)} events in window")

        new_count = 0
        for e in page_events:
            if e["id"] in seen_ids:
                continue
            seen_ids.add(e["id"])
            # Title+date dedup: skip when the same title (case-insensitive)
            # already appears on the same date (source-site duplicates like
            # two "KINDNESS HORSE CAMP" pages for the same event).
            key = (e["title"].strip().lower(), e["date"])
            if key in seen_title_date:
                continue
            seen_title_date.add(key)
            all_events.append(e)
            new_count += 1

        if new_count == 0:
            log(f"page {page}: no new events — stopping")
            break

        if page_events:
            latest = max(
                datetime.date.fromisoformat(e["date"]) for e in page_events
            )
            if latest >= window_end:
                log(f"page {page} reached {latest} — window covered")
                break

    all_events.sort(key=lambda e: (e["date"], e["time"]))
    log(f"fetched {pages_fetched} pages, {len(all_events)} unique events")
    return all_events


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def load_existing() -> dict[str, Any] | None:
    if not EVENTS_JSON.exists():
        return None
    try:
        with EVENTS_JSON.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return None


def write_json(data: dict[str, Any]) -> bool:
    try:
        fd, tmp_path = tempfile.mkstemp(
            suffix=".tmp", prefix="events", dir=REPO_DIR
        )
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp_path, EVENTS_JSON)
        return True
    except OSError as exc:
        log(f"write failed: {exc}")
        return False


def file_changed_since_commit(path: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "diff", "--quiet", "HEAD", "--", str(path)],
            cwd=REPO_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.returncode != 0
    except Exception:
        return True


# ---------------------------------------------------------------------------
# Git
# ---------------------------------------------------------------------------

def git_commit_push(path: Path, message: str) -> bool:
    try:
        subprocess.run(
            ["git", "add", "--renormalize", str(path)],
            cwd=REPO_DIR, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=REPO_DIR, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "push", "origin", "gh-pages"],
            cwd=REPO_DIR, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "push", "origin", "gh-pages:main"],
            cwd=REPO_DIR, check=True, capture_output=True,
        )
        return True
    except subprocess.CalledProcessError as exc:
        log(f"git failed: {exc}")
        if exc.stderr:
            log(f"stderr: {exc.stderr.decode(errors='replace')[:500]}")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{LOG_PREFIX} {ts} {msg}", flush=True)


def run() -> int:
    log("start")

    log("fetching pages")
    raw_events = fetch_events(max_days=14, max_pages=30)
    log(f"raw events in window: {len(raw_events)}")

    kept = [e for e in raw_events if should_keep(e)]
    dropped = len(raw_events) - len(kept)
    log(f"kept: {len(kept)}, dropped: {dropped}")
    for e in raw_events:
        if not should_keep(e):
            log(f"  dropped: {e['title']!r} ({e['date']})")

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    output: dict[str, Any] = {
        "last_updated": now_iso,
        "generated_by": "fetch_events.py",
        "source": "pembinavalleyonline.com/events",
        "filter": {"drop_terms": DROP_TERMS},
        "events": kept,
    }

    if not write_json(output):
        log("FAILED to write events.json — keeping previous")
        return 1

    new_size = EVENTS_JSON.stat().st_size
    log(f"wrote events.json ({new_size} bytes, {len(kept)} events)")

    if new_size < 500:
        log(f"WARNING: events.json is only {new_size} bytes — restoring previous")
        try:
            subprocess.run(
                ["git", "checkout", "HEAD", "--", str(EVENTS_JSON)],
                cwd=REPO_DIR, check=True, capture_output=True,
            )
        except Exception:
            pass
        return 1

    if not file_changed_since_commit(EVENTS_JSON):
        log("no change vs committed — skipping commit/push")
        return 0

    msg = (
        f"auto: update events.json ({len(kept)} events, "
        f"{datetime.date.today().isoformat()})"
    )
    log("committing and pushing")
    if not git_commit_push(EVENTS_JSON, msg):
        log("git commit/push FAILED — events.json written locally, not pushed")
        return 1

    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(run())
