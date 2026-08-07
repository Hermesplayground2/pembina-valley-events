from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Critical structure checks
critical = {
    'Home page': 'id="page-home"' in text,
    'Activities page': 'id="page-activities"' in text,
    'Family page': 'id="page-family"' in text,
    'Sources page': 'id="page-sources"' in text,
    'Contact page': 'id="page-contact"' in text,
    'PVBC VBS': 'Aug 12-14' in text,
    'buildActivityWeek': 'function buildActivityWeek()' in text,
    'SEO meta': 'meta name="description"' in text,
}
if not all(critical.values()):
    print('Critical structure missing, aborting')
    exit(1)
print('✓ Critical structure intact')

# 1. Remove Monthly Schedule from home page
old_monthly = '''    <section class="section">
      <div class="card card-landscape-calendar">
        <h2>🗓 Monthly Schedule</h2>
        <div class="month-wrap" id="month-wrap"></div>
      </div>
    </section>'''

if old_monthly in text:
    text = text.replace(old_monthly, '', 1)
    print('✓ Removed Monthly Schedule from home page')
else:
    print('✗ Monthly Schedule marker not found')

# 2. Remove Locals navigation link
old_nav = '''    <a href="#" class="nav-link" data-page="local">Locals</a>'''
if old_nav in text:
    text = text.replace(old_nav, '', 1)
    print('✓ Removed Locals nav link')
else:
    print('✗ Locals nav marker not found')

# 3. Remove entire Locals page section
old_locals_page = '''  <div class="page" id="page-local">
    <section class="section">
      <div class="card">
        <h2>🏪 Locals</h2>
        <p class="muted">Winkler, MB spots, services, and food deals.</p>
        <div class="spacer"></div>'''

if old_locals_page in text:
    # Find the end of the locals page section
    start_idx = text.find(old_locals_page)
    # Find the next page div or closing div
    rest = text[start_idx:]
    # Find the end of this page section
    end_search = rest.find('  </div>\r\n\r\n  <div class="page"', 10)
    if end_search == -1:
        end_search = rest.find('  </div>\r\n\r\n</div>', 10)
    
    if end_search != -1:
        end_idx = start_idx + end_search + len('  </div>')
        removed = text[start_idx:end_idx]
        text = text[:start_idx] + text[end_idx:]
        print(f'✓ Removed Locals page section ({len(removed)} chars)')
    else:
        print('✗ Could not find Locals page end boundary')
else:
    print('✗ Locals page marker not found')

p.write_text(text, encoding='utf-8')
print('\nDone')
