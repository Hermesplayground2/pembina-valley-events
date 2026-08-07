from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# 1) Hide email in contact form
old_contact = '''<form class="contact-form" action="mailto:Boomsecure@protonmail.com" method="post" enctype="text/plain">
          <input type="text" name="name" placeholder="Your name" required>
          <input type="email" name="email" placeholder="Your email" required>
          <textarea rows="4" name="message" placeholder="Message" required></textarea>
          <button type="submit">Send message</button>
        </form>
        <p class="muted" style="margin-top:10px;">Messages open your email app and are sent to Boomsecure@protonmail.com.</p>'''
new_contact = '''<form class="contact-form" action="mailto:boomsecure@protonmail.com" method="post" enctype="text/plain">
          <input type="text" name="name" placeholder="Your name" required>
          <input type="email" name="email" placeholder="Your email" required>
          <textarea rows="4" name="message" placeholder="Message" required></textarea>
          <button type="submit">Send message</button>
        </form>
        <p class="muted" style="margin-top:10px;">Messages open your email app and are sent to the site owner.</p>'''
if old_contact in text:
    text = text.replace(old_contact, new_contact, 1)
    print('Updated contact form to hide email')

# 2) Rename sponsors to Locals and move to bottom
old_section = '''    <section class="section">
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
    </section>'''

new_section = '''    <section class="section">
      <div class="card">
        <h2>🤝 Locals</h2>
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
    </section>'''

if old_section in text:
    text = text.replace(old_section, new_section, 1)
    print('Renamed sponsors to Locals')
    # Move to bottom
    text = text.replace(old_section, '', 1)
    old_end = '</div>\n\n<footer>'
    new_end = '</div>\n\n' + new_section + '\n<footer>'
    if old_end in text:
        text = text.replace(old_end, new_end, 1)
        print('Moved Locals to bottom')

p.write_text(text, encoding='utf-8')
print('Done')
