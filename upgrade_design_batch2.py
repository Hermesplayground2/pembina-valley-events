from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# === SAFE DESIGN UPGRADE BATCH 2 ===
# Verify critical structure first
critical_checks = {
    'Home page': 'id="page-home"' in text,
    'Activities page': 'id="page-activities"' in text,
    'Locals page': 'id="page-local"' in text,
    'Family page': 'id="page-family"' in text,
    'Sources page': 'id="page-sources"' in text,
    'Contact page': 'id="page-contact"' in text,
    'PVBC VBS Aug 12-14': 'Aug 12-14' in text,
    'buildActivityWeek JS': 'function buildActivityWeek()' in text,
    'SEO meta description': 'meta name="description"' in text,
    'Canonical URL': 'rel="canonical"' in text,
}

all_critical = all(critical_checks.values())
print('Critical structure check:')
for k, v in critical_checks.items():
    print(f'  {"✓" if v else "✗"} {k}')

if not all_critical:
    print('\n✗ Critical structure missing - aborting upgrade')
    exit(1)

print('\n✓ All critical elements present, proceeding with upgrade...')

# === BATCH 2: Enhanced visual design ===

# 1. Improve featured card styling
old_featured = '''  .featured-card {
    border: 1px solid var(--border); border-radius: 18px; padding: 16px; background: white;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 1px 0 rgba(15,23,42,0.04);
  }
  .featured-card:hover { transform: translateY(-3px); box-shadow: 0 18px 40px rgba(15,23,42,0.12); }'''

new_featured = '''  .featured-card {
    border: 1px solid var(--border); border-radius: 20px; padding: 18px; background: white;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    box-shadow: 0 2px 8px rgba(15,23,42,0.06);
    position: relative;
    overflow: hidden;
  }
  .featured-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    opacity: 0;
    transition: opacity 0.25s ease;
  }
  .featured-card:hover { 
    transform: translateY(-4px); 
    box-shadow: 0 20px 50px rgba(15,23,42,0.15);
    border-color: rgba(37,99,235,0.25);
  }
  .featured-card:hover::before { opacity: 1; }'''

if old_featured in text:
    text = text.replace(old_featured, new_featured, 1)
    print('✓ Enhanced featured card styling')
else:
    print('✗ Featured card marker not found')

# 2. Improve event row styling
old_event_row = '''  .event-row {
    display: flex; align-items: flex-start; gap: 12px; padding: 14px 0; border-bottom: 1px solid var(--border);
    transition: background 0.15s ease;
  }
  .event-row:last-child { border-bottom: none; }'''

new_event_row = '''  .event-row {
    display: flex; align-items: flex-start; gap: 14px; padding: 16px 0; border-bottom: 1px solid var(--border);
    transition: background 0.2s ease, padding-left 0.2s ease;
  }
  .event-row:last-child { border-bottom: none; }
  .event-row:hover { 
    background: linear-gradient(90deg, rgba(37,99,235,0.03) 0%, transparent 100%);
    padding-left: 8px;
    border-radius: 8px;
  }'''

if old_event_row in text:
    text = text.replace(old_event_row, new_event_row, 1)
    print('✓ Enhanced event row hover')
else:
    print('✗ Event row marker not found')

# 3. Improve day-event bubble styling
old_day_event = '''  .day-event {
    border-radius: 999px;
    padding: 10px 14px;
    background: white;
    border: 1px solid var(--border);
    box-shadow: 0 1px 0 rgba(15,23,42,0.04);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    text-decoration: none;
    color: inherit;
    display: block;
  }
  .day-event:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(15,23,42,0.08);
    border-color: var(--border);
  }'''

new_day_event = '''  .day-event {
    border-radius: 999px;
    padding: 11px 16px;
    background: white;
    border: 1px solid var(--border);
    box-shadow: 0 2px 6px rgba(15,23,42,0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    text-decoration: none;
    color: inherit;
    display: block;
    font-weight: 600;
  }
  .day-event:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(15,23,42,0.1);
    border-color: var(--accent);
  }'''

if old_day_event in text:
    text = text.replace(old_day_event, new_day_event, 1)
    print('✓ Enhanced day-event bubble styling')
else:
    print('✗ Day-event marker not found')

# 4. Improve calendar day styling
old_cal_day = '''  .calendar-day {
    background: white; border: 1px solid var(--border); border-radius: 16px; padding: 12px; min-height: 100px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .calendar-day:hover { transform: translateY(-2px); box-shadow: 0 14px 30px rgba(15,23,42,0.08); }'''

new_cal_day = '''  .calendar-day {
    background: white; border: 1px solid var(--border); border-radius: 18px; padding: 14px; min-height: 110px;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    position: relative;
  }
  .calendar-day:hover { 
    transform: translateY(-3px); 
    box-shadow: 0 16px 35px rgba(15,23,42,0.1);
    border-color: rgba(37,99,235,0.2);
  }'''

if old_cal_day in text:
    text = text.replace(old_cal_day, new_cal_day, 1)
    print('✓ Enhanced calendar day styling')
else:
    print('✗ Calendar day marker not found')

# 5. Improve footer
old_footer = '''  footer {
    text-align: center; padding: 26px 18px; color: var(--muted); font-size: 0.92rem;
    border-top: 1px solid var(--border); margin-top: 24px;
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(10px);
  }'''

new_footer = '''  footer {
    text-align: center; padding: 28px 18px; color: var(--muted); font-size: 0.92rem;
    border-top: 1px solid var(--border); margin-top: 32px;
    background: linear-gradient(180deg, rgba(255,255,255,0.8) 0%, rgba(241,245,249,0.9) 100%);
    backdrop-filter: blur(12px);
  }'''

if old_footer in text:
    text = text.replace(old_footer, new_footer, 1)
    print('✓ Enhanced footer styling')
else:
    print('✗ Footer marker not found')

# 6. Improve Sources/Locals grid cards
old_locals_grid = '''  .locals-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; }
  .local-card { display: block; padding: 14px; border-radius: 10px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); color: inherit; text-decoration: none; transition: transform .08s ease, background .15s ease; }
  .local-card:hover { transform: translateY(-2px); background: rgba(255,255,255,0.07); }'''

new_locals_grid = '''  .locals-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; }
  .local-card { 
    display: block; padding: 16px; border-radius: 14px; background: rgba(255,255,255,0.04); 
    border: 1px solid rgba(255,255,255,0.08); color: inherit; text-decoration: none; 
    transition: transform 0.2s ease, background 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  }
  .local-card:hover { 
    transform: translateY(-3px); 
    background: rgba(255,255,255,0.08);
    border-color: rgba(255,255,255,0.15);
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  }'''

if old_locals_grid in text:
    text = text.replace(old_locals_grid, new_locals_grid, 1)
    print('✓ Enhanced locals grid styling')
else:
    print('✗ Locals grid marker not found')

p.write_text(text, encoding='utf-8')
print('\n✅ Batch 2 design upgrades applied successfully')
