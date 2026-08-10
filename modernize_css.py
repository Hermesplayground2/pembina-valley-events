import pathlib

p = pathlib.Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Replace the entire CSS block with a modern, polished design system
old_css = '''  :root {
    --bg: #f6f8fb;
    --card: #ffffff;
    --text: #1f2937;
    --muted: #6b7280;
    --accent: #2563eb;
    --accent2: #7c3aed;
    --border: #e5e7eb;
    --success: #16a34a;
    --warning: #d97706;
    --danger: #dc2626;
    --radius: 16px;
    --shadow: rgba(15, 23, 42, 0.08);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.55;
  }
  header {
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    color: white;
    padding: 44px 20px 52px;
    text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }
  header h1 { font-size: 2.3rem; font-weight: 800; letter-spacing: -0.03em; }
  header p { opacity: 0.9; margin-top: 10px; font-weight: 500; font-size: 1.05rem; }
  nav {
    background: white;
    border-bottom: 1px solid var(--border);
    padding: 14px 18px;
    position: sticky;
    top: 0;
    z-index: 100;
  }
  .nav-inner { max-width: 1160px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; }
  .nav-link {
    padding: 9px 15px;
    border-radius: 999px;
    text-decoration: none;
    color: var(--text);
    font-weight: 600;
    font-size: 0.92rem;
    border: 1px solid transparent;
    transition: all 0.2s;
  }
  .nav-link:hover, .nav-link.active { background: #0f172a; color: white; border-color: #0f172a; }
  .container { max-width: 1160px; margin: 0 auto; padding: 28px 18px; }
  .grid { display: grid; gap: 16px; }
  .grid-2 { grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
  .grid-3 { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
  .grid-4 { grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px;
    box-shadow: 0 6px 18px var(--shadow);
    position: relative;
    overflow: hidden;
  }
  .card::before {
    content: "";
    position: absolute;
    inset: 0;
    opacity: 0.12;
    background-size: cover;
    background-position: center;
    pointer-events: none;
  }
  .card-landscape-field::before { background-image: url('https://images.unsplash.com/photo-1500651230702-0e2d8a49d4ad?auto=format&fit=crop&w=1200&q=80'); }
  .card-landscape-activity::before { background-image: url('https://images.unsplash.com/photo-1472396961693-142e6e269027?auto=format&fit=crop&w=1200&q=80'); }
  .card-landscape-calendar::before { background-image: url('https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=80'); }
  .card-landscape-weather::before { background-image: url('https://images.unsplash.com/photo-1592210454351-9043f163ca73?auto=format&fit=crop&w=1200&q=80'); }
  .card h2 { font-size: 1.15rem; font-weight: 700; margin-bottom: 10px; }
  .card .muted { color: var(--muted); font-size: 0.92rem; }
  .section { margin-bottom: 28px; }
  .spacer { height: 18px; }
  .page { display: none; animation: fadeIn 0.25s ease; }
  .page.active { display: block; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
  .pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 12px; border-radius: 999px; font-weight: 700; font-size: 0.85rem;
    background: white; border: 1px solid var(--border); color: var(--text); cursor: pointer;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }
  .pill:hover { transform: translateY(-1px); box-shadow: 0 8px 20px rgba(15,23,42,0.08); }
  .pill.active { background: #0f172a; color: white; border-color: #0f172a; }
  .event-row {
    display: flex; align-items: flex-start; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--border);
  }
  .event-row:last-child { border-bottom: none; }
  .event-date {
    min-width: 56px; text-align: center; padding: 10px 8px; border-radius: 14px; background: #eef2ff; color: #3730a3; font-weight: 800;
  }
  .event-date .month { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em; }
  .event-date .day { font-size: 1.2rem; line-height: 1; margin-top: 2px; }
  .event-title { font-weight: 700; font-size: 0.98rem; }
  .event-meta { color: var(--muted); font-size: 0.85rem; margin-top: 4px; }
  .calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; }
  .calendar-day {
    background: white; border: 1px solid var(--border); border-radius: 14px; padding: 10px; min-height: 90px;
  }
  .calendar-day .day-name { font-weight: 800; font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }
  .calendar-day .day-number { font-weight: 800; font-size: 1.1rem; margin-top: 4px; }
  .calendar-day .day-chip {
    margin-top: 8px; padding: 6px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: 700;
    background: #fef3c7; color: #92400e; border-left: 3px solid #f59e0b;
  }
  .weather-card {
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    color: white; border-radius: var(--radius); padding: 18px;
  }
  .weather-card .temp { font-size: 2.2rem; font-weight: 800; }
  .weather-card .meta { opacity: 0.9; margin-top: 6px; }
  .weekly-wrap { display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; margin-top: 14px; }
  .weekly-day {
    background: rgba(255,255,255,0.12); border-radius: 14px; padding: 10px; text-align: center; backdrop-filter: blur(4px);
  }
  .weekly-day .dow { font-size: 0.7rem; text-transform: uppercase; opacity: 0.8; }
  .weekly-day .date { font-weight: 800; margin-top: 2px; }
  .weekly-day .cond { font-size: 0.78rem; opacity: 0.95; margin-top: 4px; }
  .weekly-day .lo-hi { font-size: 0.75rem; opacity: 0.85; margin-top: 4px; }
  .featured-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }
  .featured-card {
    border: 1px solid var(--border); border-radius: 14px; padding: 14px; background: white;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }
  .featured-card:hover { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(15,23,42,0.1); }
  .featured-card .badge-row { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 8px; }
  .featured-card .title { font-weight: 800; font-size: 1.05rem; margin-bottom: 6px; letter-spacing: -0.01em; }
  .featured-card .meta { color: var(--muted); font-size: 0.88rem; }
  .featured-card .date-badge { display: inline-block; padding: 4px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: 800; background: #eef2ff; color: #3730a3; }
  .featured-card .cat-badge { display: inline-block; padding: 4px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: 800; background: #fef3c7; color: #92400e; }
  .featured-card .row { display:flex; justify-content:space-between; align-items:center; gap:10px; }
  .featured-card .trust { color: var(--muted); font-size: 0.78rem; margin-top: 10px; }
  footer {
    text-align: center; padding: 24px 18px; color: var(--muted); font-size: 0.9rem;
    border-top: 1px solid var(--border); margin-top: 20px;
  }
  @media (max-width: 640px) {
    .grid-2 { grid-template-columns: 1fr; }
    .grid-3 { grid-template-columns: 1fr; }
    .weekly-wrap { grid-template-columns: repeat(2, 1fr); }
    .calendar-grid { grid-template-columns: repeat(2, 1fr); }
    .featured-grid { grid-template-columns: 1fr; }
    header h1 { font-size: 1.7rem; }
    .nav-link { font-size: 0.85rem; padding: 8px 12px; }
    .weather-card .temp { font-size: 1.7rem; }
  }
  @media (max-width: 380px) {
    .calendar-grid { grid-template-columns: 1fr; }
    .weekly-wrap { grid-template-columns: 1fr; }
  }'''

new_css = '''  :root {
    --bg: #f1f5f9;
    --card: #ffffff;
    --text: #0f172a;
    --muted: #64748b;
    --accent: #2563eb;
    --accent-2: #7c3aed;
    --border: #e2e8f0;
    --success: #16a34a;
    --warning: #d97706;
    --danger: #ef4444;
    --radius: 20px;
    --shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  body {
    font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: radial-gradient(circle at top left, #eef2ff, #f1f5f9 40%, #e2e8f0 100%);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
  }
  header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #2563eb 100%);
    color: white;
    padding: 52px 20px 64px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  header::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.15) 100%);
    pointer-events: none;
  }
  header h1 { font-size: clamp(1.8rem, 4vw, 2.6rem); font-weight: 900; letter-spacing: -0.04em; }
  header p { opacity: 0.92; margin-top: 12px; font-weight: 500; font-size: clamp(0.95rem, 1.6vw, 1.1rem); }
  nav {
    background: rgba(255,255,255,0.85);
    border-bottom: 1px solid var(--border);
    padding: 14px 18px;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
  }
  .nav-inner { max-width: 1160px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; }
  .nav-link {
    padding: 9px 14px;
    border-radius: 999px;
    text-decoration: none;
    color: var(--text);
    font-weight: 700;
    font-size: 0.92rem;
    border: 1px solid transparent;
    transition: all 0.2s ease;
    background: white;
    box-shadow: 0 1px 0 rgba(15,23,42,0.04);
  }
  .nav-link:hover { transform: translateY(-1px); box-shadow: 0 8px 20px rgba(15,23,42,0.08); border-color: var(--border); }
  .nav-link.active { background: #0f172a; color: white; border-color: #0f172a; }
  .container { max-width: 1160px; margin: 0 auto; padding: 28px 18px; }
  .grid { display: grid; gap: 16px; }
  .grid-2 { grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
  .grid-3 { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
  .grid-4 { grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px;
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .card:hover { transform: translateY(-2px); box-shadow: 0 18px 40px rgba(15,23,42,0.1); }
  .card::before {
    content: "";
    position: absolute;
    inset: 0;
    opacity: 0.10;
    background-size: cover;
    background-position: center;
    pointer-events: none;
  }
  .card-landscape-field::before { background-image: url('https://images.unsplash.com/photo-1500651230702-0e2d8a49d4ad?auto=format&fit=crop&w=1200&q=80'); }
  .card-landscape-activity::before { background-image: url('https://images.unsplash.com/photo-1472396961693-142e6e269027?auto=format&fit=crop&w=1200&q=80'); }
  .card-landscape-calendar::before { background-image: url('https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=80'); }
  .card-landscape-weather::before { background-image: url('https://images.unsplash.com/photo-1592210454351-9043f163ca73?auto=format&fit=crop&w=1200&q=80'); }
  .card h2 { font-size: 1.15rem; font-weight: 800; margin-bottom: 10px; letter-spacing: -0.01em; }
  .card .muted { color: var(--muted); font-size: 0.92rem; }
  .section { margin-bottom: 28px; }
  .spacer { height: 18px; }
  .page { display: none; animation: fadeIn 0.35s ease; }
  .page.active { display: block; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
  .pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 12px; border-radius: 999px; font-weight: 700; font-size: 0.85rem;
    background: white; border: 1px solid var(--border); color: var(--text); cursor: pointer;
    transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
  }
  .pill:hover { transform: translateY(-1px); box-shadow: 0 8px 20px rgba(15,23,42,0.08); }
  .pill.active { background: #0f172a; color: white; border-color: #0f172a; }
  .event-row {
    display: flex; align-items: flex-start; gap: 12px; padding: 14px 0; border-bottom: 1px solid var(--border);
    transition: background 0.15s ease;
  }
  .event-row:last-child { border-bottom: none; }
  .event-row:hover { background: #f8fafc; }
  .event-date {
    min-width: 60px; text-align: center; padding: 12px 8px; border-radius: 16px; background: #eef2ff; color: #3730a3; font-weight: 900;
    box-shadow: inset 0 0 0 1px rgba(55,48,163,0.12);
  }
  .event-date .month { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; }
  .event-date .day { font-size: 1.25rem; line-height: 1; margin-top: 3px; }
  .event-title { font-weight: 800; font-size: 1rem; }
  .event-meta { color: var(--muted); font-size: 0.88rem; margin-top: 5px; }
  .calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; }
  .calendar-day {
    background: white; border: 1px solid var(--border); border-radius: 16px; padding: 12px; min-height: 100px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .calendar-day:hover { transform: translateY(-2px); box-shadow: 0 14px 30px rgba(15,23,42,0.08); }
  .calendar-day .day-name { font-weight: 900; font-size: 0.72rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; }
  .calendar-day .day-number { font-weight: 900; font-size: 1.2rem; margin-top: 6px; }
  .calendar-day.today .day-number { color: #2563eb; }
  .calendar-day .day-chip {
    margin-top: 10px; padding: 7px 9px; border-radius: 12px; font-size: 0.75rem; font-weight: 800;
    background: #fffbeb; color: #92400e; border-left: 4px solid #f59e0b;
    box-shadow: 0 2px 8px rgba(245,158,11,0.12);
  }
  .weather-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #2563eb 100%);
    color: white; border-radius: var(--radius); padding: 20px;
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
  }
  .weather-card::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(255,255,255,0), rgba(255,255,255,0.15));
    pointer-events: none;
  }
  .weather-card .temp { font-size: 2.4rem; font-weight: 900; letter-spacing: -0.03em; }
  .weather-card .meta { opacity: 0.92; margin-top: 6px; font-weight: 500; }
  .weekly-wrap { display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; margin-top: 16px; }
  .weekly-day {
    background: rgba(255,255,255,0.14); border-radius: 16px; padding: 12px; text-align: center; backdrop-filter: blur(6px);
    border: 1px solid rgba(255,255,255,0.18);
  }
  .weekly-day .dow { font-size: 0.7rem; text-transform: uppercase; opacity: 0.85; font-weight: 800; letter-spacing: 0.08em; }
  .weekly-day .date { font-weight: 900; margin-top: 4px; }
  .weekly-day .cond { font-size: 0.8rem; opacity: 0.95; margin-top: 5px; font-weight: 700; }
  .weekly-day .lo-hi { font-size: 0.75rem; opacity: 0.85; margin-top: 4px; }
  .featured-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }
  .featured-card {
    border: 1px solid var(--border); border-radius: 18px; padding: 16px; background: white;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 1px 0 rgba(15,23,42,0.04);
  }
  .featured-card:hover { transform: translateY(-3px); box-shadow: 0 18px 40px rgba(15,23,42,0.12); }
  .featured-card .badge-row { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px; }
  .featured-card .title { font-weight: 900; font-size: 1.05rem; margin-bottom: 6px; letter-spacing: -0.01em; }
  .featured-card .meta { color: var(--muted); font-size: 0.9rem; }
  .featured-card .date-badge { display: inline-block; padding: 5px 11px; border-radius: 999px; font-size: 0.75rem; font-weight: 900; background: #eef2ff; color: #3730a3; }
  .featured-card .cat-badge { display: inline-block; padding: 5px 11px; border-radius: 999px; font-size: 0.75rem; font-weight: 900; background: #fef3c7; color: #92400e; }
  .featured-card .row { display:flex; justify-content:space-between; align-items:center; gap:10px; }
  .featured-card .trust { color: var(--muted); font-size: 0.78rem; margin-top: 10px; }
  .cta-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
  .cta {
    padding: 10px 14px; border-radius: 14px; font-weight: 800; font-size: 0.9rem;
    background: white; border: 1px solid var(--border); color: var(--text); text-decoration: none;
    transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
  }
  .cta:hover { transform: translateY(-1px); box-shadow: 0 10px 24px rgba(15,23,42,0.08); background: #0f172a; color: white; border-color: #0f172a; }
  footer {
    text-align: center; padding: 26px 18px; color: var(--muted); font-size: 0.92rem;
    border-top: 1px solid var(--border); margin-top: 24px;
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(10px);
  }
  @media (max-width: 640px) {
    .grid-2 { grid-template-columns: 1fr; }
    .grid-3 { grid-template-columns: 1fr; }
    .weekly-wrap { grid-template-columns: repeat(2, 1fr); }
    .calendar-grid { grid-template-columns: repeat(2, 1fr); }
    .featured-grid { grid-template-columns: 1fr; }
    header h1 { font-size: 1.7rem; }
    .nav-link { font-size: 0.85rem; padding: 8px 12px; }
    .weather-card .temp { font-size: 1.8rem; }
    .card { padding: 16px; }
  }
  @media (max-width: 380px) {
    .calendar-grid { grid-template-columns: 1fr; }
    .weekly-wrap { grid-template-columns: 1fr; }
  }'''

if old_css in text:
    text = text.replace(old_css, new_css, 1)
    print('Replaced CSS with modern design system')
else:
    print('CSS anchor not found')

p.write_text(text, encoding='utf-8')
print('Done')
