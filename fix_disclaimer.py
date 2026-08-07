from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Remove standalone disclaimer block outside Locals
old = '''</div>

<div class="section" style="padding: 20px 0 10px;">
      <p class="muted" style="font-size:0.8rem;opacity:0.75;">Some links are affiliate or partner links — pembinaevents.ca may earn a small commission if you book or order through them. You pay the same price.</p>
    </div>

    <section class="section">
      <div class="card">
        <h2>🤝 Locals</h2>'''

new = '''</div>

    <section class="section">
      <div class="card">
        <h2>🤝 Locals</h2>'''

if old in text:
    text = text.replace(old, new, 1)
    print('Removed standalone disclaimer')
else:
    print('Standalone disclaimer not found')

# Add disclaimer at bottom of Locals section
old_locals_end = '''          <a class="local-card" href="https://www.winkler.ca" target="_blank" rel="noopener">
            <div class="local-name">RM of Stanley</div>
            <div class="local-desc">Municipal services & events</div>
          </a>
        </div>
      </div>
    </section>'''

new_locals_end = '''          <a class="local-card" href="https://www.winkler.ca" target="_blank" rel="noopener">
            <div class="local-name">RM of Stanley</div>
            <div class="local-desc">Municipal services & events</div>
          </a>
        </div>
        <div class="spacer"></div>
        <p class="muted" style="font-size:0.8rem;opacity:0.75;">Some links are affiliate or partner links — pembinaevents.ca may earn a small commission if you book or order through them. You pay the same price.</p>
      </div>
    </section>'''

if old_locals_end in text:
    text = text.replace(old_locals_end, new_locals_end, 1)
    print('Added disclaimer inside Locals section')
else:
    print('Locals end marker not found')

p.write_text(text, encoding='utf-8')
print('Done')

# Verify
count = text.count('affiliate or partner links')
print(f'Disclaimer count: {count}')
