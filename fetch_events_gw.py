#!/usr/bin/env python3
"""
fetch_events_gw.py — fetch events from pembinavalley.gwevents.ca (alternative source).

This site is a mirror/guide for Pembina Valley events with clean HTML,
category pages, and individual event pages with dates and locations.
Accessible without 403 errors (unlike pembinavalleyonline.com).
"""
from __future__ import annotations
import datetime
import json
import re
import sys
import tempfile
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
BASE = "https://pembinavalley.gwevents.ca"
LOG = Path("C:/tmp/pembina_src/logs")
LOG.mkdir(parents=True, exist_ok=True)

def fetch_page(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")

def strip_scripts(html: str) -> str:
    """Remove <script> and <style> blocks INCLUDING their content.

    Stripping tags alone leaves the JavaScript text behind (e.g. inline
    initMap()/google.maps blocks), which then leaks into extracted fields.
    """
    html = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style\b[^>]*>.*?</style>", " ", html, flags=re.S | re.I)
    return html


def sanitize_field(s: str, max_len: int = 160) -> str:
    """Final guard: strip any leaked JS/HTML fragments and cap length."""
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    # Cut off anything from a leaked script marker onward
    s = re.split(r"function\s+\w+\s*\(|google\.maps|var\s+\w+\s*=\s*\{|document\.getElementById", s)[0]
    # Decode HTML entities (handle double-encoding like &amp;amp;#39;)
    for _ in range(3):
        if "&" not in s:
            break
        s = (s.replace("&amp;", "&").replace("&#39;", "'").replace("&apos;", "'")
               .replace("&quot;", '"').replace("&#34;", '"').replace("&nbsp;", " ")
               .replace("&lt;", "<").replace("&gt;", ">"))
    s = re.sub(r"\s+", " ", s).strip()
    # Drop trailing punctuation/spaces
    s = s.strip(" ·,;:-")
    if len(s) > max_len:
        s = s[:max_len].rsplit(" ", 1)[0] + "…"
    return s


def clean_title(raw: str) -> str:
    """Turn a messy listing title into a clean event title.

    Listing pages look like:
      "8:30 AM 18+ Hockey - Icon Arena - $5 drop in fee Meridian Exhibition Centre, 1045 Grandeur Ave, Winkler, MB"
    We want: "18+ Hockey - Icon Arena"
    """
    t = raw or ""
    # Strip leading time
    t = re.sub(r'^\s*\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)\s*', '', t)
    # Strip trailing address: ", 1234 Street, City, MB"
    t = re.sub(r',\s*\d+[^,]*,\s*[A-Za-z .]+,\s*(?:MB|Manitoba)\s*$', '', t, flags=re.I)
    # Strip trailing "City, MB"
    t = re.sub(r',\s*[A-Za-z .]+,\s*(?:MB|Manitoba)\s*$', '', t, flags=re.I)
    # Strip trailing bare "MB"/"Manitoba"
    t = re.sub(r'\s*,?\s*(?:MB|Manitoba)\s*$', '', t, flags=re.I)
    # Strip trailing venue-name fragment (with optional address already gone)
    t = re.sub(r'\s+[A-Z][A-Za-z&\' ]*(?:Centre|Center|Arena|Hall|Park|School|Church|Mall|Library|Museum)\b.*$', '', t)
    # Strip trailing price fragment
    t = re.sub(r'\s*-\s*\$[\d.]+\s*(?:drop\s*in\s*fee)?\s*$', '', t, flags=re.I)
    t = re.sub(r'\s*-\s*\$[\d.]+\s*', ' - ', t)
    return sanitize_field(t, max_len=100)


def polish_title(t: str) -> str:
    """Final title polish: drop trailing price/drop-in fragments."""
    t = t or ""
    t = re.sub(r'\s*[-–]\s*\$[\d.]+\s*(?:drop\s*in\s*fee|per\s*\w+|each)?\s*$', '', t, flags=re.I)
    t = re.sub(r'\s*\(?\s*\$[\d.]+\s*(?:drop\s*in\s*fee)?\s*\)?\s*$', '', t, flags=re.I)
    return sanitize_field(t, max_len=100)


def clean_location(raw: str) -> str:
    """Cut a location string at contact-info noise."""
    if not raw:
        return ""
    loc = raw
    loc = re.split(r'\s*Contact\s*Info\b|\s*Name\s+[A-Z]|\s*Phone\s*\(?\d|\s*Email\b', loc, flags=re.I)[0]
    return sanitize_field(loc, max_len=120)


def extract_events_from_listing(html: str) -> list[dict]:
    """Extract events from a listing page (main page or category page)."""
    html = strip_scripts(html)
    events = []
    # Pattern: /events/ID ... title ... date ... location
    # Events are in <a href="/events/ID"> ... </a> blocks
    for m in re.finditer(r'<a[^>]+href="(/events/(\d+))"[^>]*>(.*?)</a>', html, re.S):
        href = m.group(1)
        event_id = m.group(2)
        text = re.sub(r"<[^>]+>", " ", m.group(3))
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        events.append({
            "id": f"/events/{event_id}",
            "title": text,
            "link": f"{BASE}{href}",
            "_event_id": event_id,
        })
    return events

def extract_event_details(html: str, event_id: str) -> dict:
    """Extract title, date, time, location from an event detail page."""
    html = strip_scripts(html)
    info = {}

    # Prefer the detail page's own <h1> — it is the clean canonical title.
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    if h1:
        t = re.sub(r"<[^>]+>", " ", h1.group(1))
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            info["title"] = t
    
    # Look for date patterns like "Thursday, Oct 22, 2026" or "Saturday, Oct 31, 2026"
    date_match = re.search(r'(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+([A-Z][a-z]{2})\s+(\d{1,2}),?\s+(\d{4})', html)
    if date_match:
        month_str = date_match.group(1)
        day = date_match.group(2)
        year = date_match.group(3)
        months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
        month = months.get(month_str, 1)
        info["date"] = f"{year}-{month:02d}-{int(day):02d}"
    
    # Look for time patterns like "5:00PM" or "7:00 PM" or "9:00am"
    time_match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)', html)
    if time_match:
        hour = int(time_match.group(1))
        minute = time_match.group(2)
        ampm = time_match.group(3).upper()
        # Normalize to 12-hour clock (source sometimes gives "13:00 PM")
        if hour > 12:
            hour -= 12
            ampm = "PM"
        elif hour == 0:
            hour = 12
            ampm = "AM"
        info["time"] = f"{hour}:{minute} {ampm}"
    
    # Look for location after "Location" heading
    loc_match = re.search(r'Location[:\s]*(.*?)(?:Posted|$)', html, re.S)
    if loc_match:
        loc = re.sub(r"<[^>]+>", " ", loc_match.group(1))
        loc = re.sub(r"\s+", " ", loc).strip()
        if loc:
            info["location"] = loc
    
    return info

def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] fetch_events_gw.py starting")
    
    # 1. Fetch main page
    print("  fetching main page...")
    main_html = fetch_page(BASE)
    events = extract_events_from_listing(main_html)
    print(f"  main page: {len(events)} events")
    
    # 2. Fetch category pages for more events
    categories = ["community", "fundraising", "music_art", "sports", "family"]
    seen_ids = {e["_event_id"] for e in events}
    for cat in categories:
        url = f"{BASE}/categories/{cat}"
        try:
            print(f"  fetching category: {cat}...")
            html = fetch_page(url)
            cat_events = extract_events_from_listing(html)
            for ev in cat_events:
                if ev["_event_id"] not in seen_ids:
                    events.append(ev)
                    seen_ids.add(ev["_event_id"])
            print(f"    {cat}: +{len(cat_events)} events (total: {len(events)})")
        except Exception as e:
            print(f"    {cat}: error {e}")
    
    # 3. Fetch details for each event
    print(f"  fetching details for {len(events)} events...")
    enriched = []
    for i, ev in enumerate(events):
        try:
            detail_html = fetch_page(ev["link"])
            details = extract_event_details(detail_html, ev["_event_id"])
            
            # Prefer the detail page's clean <h1> title; fall back to cleaned listing title
            title = polish_title(details.get("title", "")) or polish_title(clean_title(ev["title"]))
            time_str = sanitize_field(details.get("time", ""), max_len=40)
            location = clean_location(details.get("location", ""))
            date = details.get("date", "")
            
            # Build time field: "9:00 AM · Location"
            if time_str and location:
                time_field = f"{time_str} · {location}"
            elif time_str:
                time_field = time_str
            elif location:
                time_field = location
            else:
                time_field = ""
            
            # Detect category from URL or content
            category = "community"  # default
            if "fundraising" in ev["link"].lower() or "fundraiser" in title.lower():
                category = "fundraising"
            elif "music" in title.lower() or "art" in title.lower():
                category = "music_art"
            elif "sport" in title.lower() or "hockey" in title.lower() or "skate" in title.lower():
                category = "sports"
            
            enriched.append({
                "id": ev["id"],
                "title": title,
                "time": time_field,
                "date": date,
                "link": ev["link"],
                "source": "pembinavalley.gwevents.ca",
                "category": category,
            })
            
            if (i + 1) % 10 == 0:
                print(f"    {i+1}/{len(events)} details fetched")
        except Exception as e:
            print(f"    error fetching {ev['link']}: {e}")
            # Still include the event with what we have
            enriched.append({
                "id": ev["id"],
                "title": ev["title"],
                "time": "",
                "date": "",
                "link": ev["link"],
                "source": "pembinavalley.gwevents.ca",
                "category": "community",
            })
    
    # 4. Filter: only events with dates, drop past events, drop gambling/pride
    today = datetime.date.today()
    window_end = today + datetime.timedelta(days=60)
    filtered = []
    dropped = []
    for ev in enriched:
        if not ev["date"]:
            continue
        try:
            d = datetime.date.fromisoformat(ev["date"])
        except ValueError:
            continue
        if d < today:
            dropped.append(f"{ev['title'][:40]} ({ev['date']})")
            continue
        if d > window_end:
            dropped.append(f"{ev['title'][:40]} ({ev['date']}) beyond window")
            continue
        title_lower = ev["title"].lower()
        if any(term in title_lower for term in ["bingo", "pride", "council meeting", "farmers market"]):
            dropped.append(f"{ev['title'][:40]} (filtered)")
            continue
        filtered.append(ev)
    
    print(f"  kept: {len(filtered)}, dropped: {len(dropped)}")
    for d in dropped[:5]:
        print(f"    dropped: {d}")
    
    # 5. Deduplicate by title+date
    seen = set()
    unique = []
    for ev in filtered:
        key = (ev["title"].lower().strip(), ev["date"])
        if key not in seen:
            seen.add(key)
            unique.append(ev)
    
    print(f"  unique events: {len(unique)}")
    
    # 6. Write events.json
    output = {
        "last_updated": datetime.datetime.now().isoformat(),
        "generated_by": "fetch_events_gw.py",
        "source": "pembinavalley.gwevents.ca",
        "filter": {"drop_terms": ["bingo", "pride", "council meeting", "farmers market"]},
        "events": unique,
    }
    
    out_path = Path("C:/tmp/pembina_src/events.json")
    # Windows-safe atomic write (can't rename over existing file)
    tmp_path = out_path.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    # Remove existing file first on Windows
    if out_path.exists():
        out_path.unlink()
    tmp_path.rename(out_path)
    
    print(f"  wrote {out_path} ({out_path.stat().st_size} bytes, {len(unique)} events)")
    
    # 7. Commit and push
    import subprocess
    subprocess.run(["git", "add", "events.json"], cwd="C:/tmp/pembina_src", check=True)
    subprocess.run(["git", "commit", "-m", f"auto: update events.json ({len(unique)} events, {datetime.date.today()})"], cwd="C:/tmp/pembina_src", check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd="C:/tmp/pembina_src", check=True)
    print("  committed and pushed")
    
    print(f"[{timestamp}] done")

if __name__ == "__main__":
    main()
