from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Remove leftover old card HTML after bubble replacements in Locals page
removals = [
    '''          <div class="card local-card brand-event">
            <div class="tag">Festival</div>
            <h2 style="margin-top:6px;">Winkler Harvest Festival</h2>
            <p class="muted">Aug 7 - 9 · Fairgrounds · <a href="https://www.visitwinkler.ca/harvest-festival" target="_blank">Details</a></p>
          </div>
          <div class="card local-card brand-event">
            <div class="tag">Music</div>
            <h2 style="margin-top:6px;">Concerts in the Park</h2>
            <p class="muted">Wednesdays in July & Aug · Bethel Park · <a href="https://www.visitwinkler.ca/concerts-in-the-park" target="_blank">Details</a></p>
          </div>
          <div class="card local-card brand-event">
            <div class="tag">Holiday</div>
            <h2 style="margin-top:6px;"></h2>
            <p class="muted">Late Nov / Early Dec · Bethel Park · <a href="https://www.visitwinkler.ca/tree-lighting-ceremony" target="_blank">Details</a></p>
          </div>
          <div class="card local-card brand-event">
            <div class="tag">Christmas</div>
            <h2 style="margin-top:6px;"></h2>
            <p class="muted">December · Winkler Bible Camp · <a href="https://www.christmasglowinthecountry.com/" target="_blank">Details</a></p>
          </div>''',
    '''          <div class="card local-card brand-fund">
            <div class="tag">Charity</div>
            <h2 style="margin-top:6px;">Winkler Food Bank Drive</h2>
            <p class="muted">Drop-off donations at local grocery stores · <a href="https://www.winklerfoodbank.ca" target="_blank">Info</a></p>
          </div>
          <div class="card local-card brand-fund">
            <div class="tag">Fundraiser</div>
            <h2 style="margin-top:6px;">Winkler Bible Camp Fundraiser</h2>
            <p class="muted">Support camp programs and scholarships · <a href="https://winklerbiblecamp.ca" target="_blank">Info</a></p>
          </div>
          <div class="card local-card brand-fund">
            <div class="tag">Community</div>
            <h2 style="margin-top:6px;">Local School Fundraiser</h2>
            <p class="muted">Check with Prairie Dale and WCRC schools · <a href="https://www.winkler.ca" target="_blank">Info</a></p>
          </div>''',
    '''          <div class="card local-card brand-pizza">
            <div class="tag">Pizza</div>
            <h2 style="margin-top:6px;">Pizza 73</h2>
            <p class="muted">2-for-1 medium pizza special · <a href="https://maps.google.com/?q=Pizza+73+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-pizza">
            <div class="tag">Pizza</div>
            <h2 style="margin-top:6px;">Domino's Pizza</h2>
            <p class="muted">Mix & match deals · <a href="https://maps.google.com/?q=Domino%27s+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-pizza">
            <div class="tag">Pizza</div>
            <h2 style="margin-top:6px;">Papa John's</h2>
            <p class="muted">Large pizza specials · <a href="https://maps.google.com/?q=Papa+John%27s+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-fast">
            <div class="tag">Fast Food</div>
            <h2 style="margin-top:6px;">McDonald's</h2>
            <p class="muted">Value meal combos · <a href="https://maps.google.com/?q=McDonald%27s+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-fast">
            <div class="tag">Fast Food</div>
            <h2 style="margin-top:6px;">KFC</h2>
            <p class="muted">Family bucket deals · <a href="https://maps.google.com/?q=KFC+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-fast">
            <div class="tag">Fast Food</div>
            <h2 style="margin-top:6px;">A&W</h2>
            <p class="muted">Mozzarella burger special · <a href="https://maps.google.com/?q=A%26W+Winkler+MB" target="_blank">Map</a></p>
          </div>'''
]

for block in removals:
    if block in text:
        text = text.replace(block, '', 1)
        print('Removed leftover card block')
    else:
        print('Block not found')

p.write_text(text, encoding='utf-8')
print('Cleanup done')
