from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# 1) Add Local Sponsors section after Featured Events on homepage
old = '''    <section class="section">
      <div class="card card-landscape-calendar">
        <h2>📅 Weekly Schedule</h2>'''

new = '''    <section class="section">
      <div class="card">
        <h2>🤝 Local Sponsors & Partners</h2>
        <p class="muted">Supporting the Pembina Valley community</p>
        <div class="spacer"></div>
        <div class="locals-grid">
          <a class="local-card" href="https://www.visitwinkler.ca" target="_blank" rel="noopener">
            <div class="local-name">City of Winkler</div>
            <div class="local-desc">Official city calendar & recreation</div>
          </a>
          <a class="local-card" href="https://morden.ca/community-events" target="_blank" rel="noopener">
            <div class="local-name">City of Morden</div>
            <div class="local-desc">Community events & programs</div>
          </a>
          <a class="local-card" href="https://www.pembinavalleyonline.com" target="_blank" rel="noopener">
            <div class="local-name">Pembina Valley Online</div>
            <div class="local-desc">Local news & events hub</div>
          </a>
          <a class="local-card" href="https://winklerchamber.com" target="_blank" rel="noopener">
            <div class="local-name">Winkler Chamber</div>
            <div class="local-desc">Business directory & events</div>
          </a>
          <a class="local-card" href="https://pds.gvsd.ca" target="_blank" rel="noopener">
            <div class="local-name">Prairie Dale School</div>
            <div class="local-desc">School calendar & announcements</div>
          </a>
          <a class="local-card" href="https://www.winkler.ca" target="_blank" rel="noopener">
            <div class="local-name">RM of Stanley</div>
            <div class="local-desc">Municipal services & events</div>
          </a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="card card-landscape-calendar">
        <h2>📅 Weekly Schedule</h2>'''

if old in text:
    text = text.replace(old, new, 1)
    print('Added sponsors section')
else:
    print('Sponsors section marker not found')

# 2) Add promoted event tags in featured events and activity renderers
# Update renderFeatured to include promoted tags
old_feat = '''    container.innerHTML = featured.map(ev => `
      <a class="featured-card bubble" href="${ev.link || '#'}" target="_blank" rel="noopener" data-category="${ev.category}">
        <div class="row">
          <div class="badge-row">
            <span class="date-badge">${ev.date}</span>
            <span class="cat-badge">${ev.category}</span>
          </div>
        </div>
        <div class="title">${ev.title}</div>
        <div class="meta">${ev.time}</div>
      </a>
    `).join('');'''

new_feat = '''    container.innerHTML = featured.map(ev => `
      <a class="featured-card bubble" href="${ev.link || '#'}" target="_blank" rel="noopener" data-category="${ev.category}">
        <div class="row">
          <div class="badge-row">
            <span class="date-badge">${ev.date}</span>
            <span class="cat-badge">${ev.category}</span>
            ${ev.promoted ? '<span class="cat-badge" style="background:#f59e0b;color:#fff">Promoted</span>' : ''}
          </div>
        </div>
        <div class="title">${ev.title}</div>
        <div class="meta">${ev.time}</div>
      </a>
    `).join('');'''

if old_feat in text:
    text = text.replace(old_feat, new_feat, 1)
    print('Updated renderFeatured for promoted tags')
else:
    print('renderFeatured marker not found')

# Add promoted flag to some featured events
old_promoted = '''      { category: 'community', title: 'Winkler Harvest Festival', time: 'Aug 7-9 · Winkler Fairgrounds', date: 'Aug 7', link: 'https://www.winklerharvestfestival.com/' },'''
new_promoted = '''      { category: 'community', title: 'Winkler Harvest Festival', time: 'Aug 7-9 · Winkler Fairgrounds', date: 'Aug 7', link: 'https://www.winklerharvestfestival.com/', promoted: true },'''

if old_promoted in text:
    text = text.replace(old_promoted, new_promoted, 1)
    print('Added promoted flag to Harvest Festival')

old_promoted2 = '''      { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Aug 28-30 · Downtown Morden', date: 'Aug 28', link: 'https://cornandapple.com/' },'''
new_promoted2 = '''      { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Aug 28-30 · Downtown Morden', date: 'Aug 28', link: 'https://cornandapple.com/', promoted: true },'''

if old_promoted2 in text:
    text = text.replace(old_promoted2, new_promoted2, 1)
    print('Added promoted flag to Corn & Apple Festival')

# 3) Add affiliate/tracked links in Local Food Deals section
old_deals = '''    <div class="card">
      <h2>🍽 Local Food Deals</h2>
      <p class="muted">Weekly specials from local restaurants</p>
      <div class="spacer"></div>
      <div id="food-deals" class="locals-grid"></div>
    </div>'''

new_deals = '''    <div class="card">
      <h2>🍽 Local Food Deals</h2>
      <p class="muted">Weekly specials from local restaurants</p>
      <div class="spacer"></div>
      <div id="food-deals" class="locals-grid"></div>
      <div class="spacer"></div>
      <p class="muted" style="font-size:0.8rem;opacity:0.8;">Supporting local businesses — deals may change, call ahead to confirm.</p>
    </div>'''

if old_deals in text:
    text = text.replace(old_deals, new_deals, 1)
    print('Updated food deals footer')

# Add affiliate disclaimer before footer
old_footer = '<footer>'
new_footer = '''<div class="section" style="padding: 20px 0 10px;">
      <p class="muted" style="font-size:0.8rem;opacity:0.75;">Some links are affiliate or partner links — pembinaevents.ca may earn a small commission if you book or order through them. You pay the same price.</p>
    </div>

<footer>'''

if old_footer in text:
    text = text.replace(old_footer, new_footer, 1)
    print('Added affiliate disclaimer')

# Add CSS for new sponsor cards
old_css = '.locals-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; }'
new_css = '''.locals-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; }
  .local-card { display: block; padding: 14px; border-radius: 10px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); color: inherit; text-decoration: none; transition: transform .08s ease, background .15s ease; }
  .local-card:hover { transform: translateY(-2px); background: rgba(255,255,255,0.07); }
  .local-name { font-weight: 800; font-size: 0.95rem; margin-bottom: 4px; }
  .local-desc { font-size: 0.82rem; opacity: 0.85; }
  .featured-card .cat-badge { background: rgba(255,255,255,0.12); padding: 2px 8px; border-radius: 999px; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; }'''

if old_css in text:
    text = text.replace(old_css, new_css, 1)
    print('Added sponsor card CSS')

p.write_text(text, encoding='utf-8')
print('Done')
