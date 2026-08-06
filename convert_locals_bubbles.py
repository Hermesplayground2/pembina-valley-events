from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Convert locals cards to linked bubbles
# Replace the grid-3 locals cards section with bubble links
old_locals = '''        <div class="grid grid-3">
          <div class="card local-card brand-superstore">
            <div class="tag">Grocery</div>
            <h2 style="margin-top:6px;">Real Canadian Superstore</h2>
            <p class="muted">175 Cargill Rd · <a href="https://maps.google.com/?q=Real+Canadian+Superstore+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-coop">
            <div class="tag">Grocery</div>
            <h2 style="margin-top:6px;">Co-op</h2>
            <p class="muted">370 Main St · <a href="https://maps.google.com/?q=Co-op+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-nofrills">
            <div class="tag">Grocery</div>
            <h2 style="margin-top:6px;">No Frills</h2>
            <p class="muted">Winkler · <a href="https://maps.google.com/?q=No+Frils+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-sobeys">
            <div class="tag">Grocery</div>
            <h2 style="margin-top:6px;">Sobeys</h2>
            <p class="muted">Winkler · <a href="https://maps.google.com/?q=Sobeys+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-leevers">
            <div class="tag">Grocery</div>
            <h2 style="margin-top:6px;">Leevers Foods</h2>
            <p class="muted">Winkler · <a href="https://maps.google.com/?q=Leevers+Foods+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-petro">
            <div class="tag">Gas / Fuel</div>
            <h2 style="margin-top:6px;">Co-op Gas Bar</h2>
            <p class="muted">370 Main St · <a href="https://maps.google.com/?q=Co-op+Gas+Bar+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-petro">
            <div class="tag">Gas / Fuel</div>
            <h2 style="margin-top:6px;">Petro Canada</h2>
            <p class="muted">Winkler · <a href="https://maps.google.com/?q=Petro+Canada+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-canadiantire">
            <div class="tag">Gas / Fuel</div>
            <h2 style="margin-top:6px;">Canadian Tire Gas+</h2>
            <p class="muted">Winkler · <a href="https://maps.google.com/?q=Canadian+Tire+Gas+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-coop">
            <div class="tag">Gas / Fuel</div>
            <h2 style="margin-top:6px;">Red River Co-Op</h2>
            <p class="muted">Winkler · <a href="https://maps.google.com/?q=Red+River+Co+Op+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-homehardware">
            <div class="tag">Hardware</div>
            <h2 style="margin-top:6px;">Home Hardware</h2>
            <p class="muted">Winkler · <a href="https://maps.google.com/?q=Home+Hardware+Winkler+MB" target="_blank">Map</a></p>
          </div>
          <div class="card local-card brand-camp">
            <div class="tag">Recreation / Camp</div>
            <h2 style="margin-top:6px;">Winkler Bible Camp</h2>
            <p class="muted">Winkler · <a href="https://maps.google.com/?q=Winkler+Bible+Camp+MB" target="_blank">Map</a></p>
          </div>
        </div>'''

new_locals = '''        <div class="grid grid-3">
          <a class="day-event bubble" href="https://www.realcanadiansuperstore.ca/" target="_blank" rel="noopener"><span class="title">Real Canadian Superstore</span><span class="time">175 Cargill Rd</span></a>
          <a class="day-event bubble" href="https://www.walmart.ca/" target="_blank" rel="noopener"><span class="title">Co-op</span><span class="time">370 Main St</span></a>
          <a class="day-event bubble" href="https://www.nofrills.ca/" target="_blank" rel="noopener"><span class="title">No Frills</span><span class="time">Winkler</span></a>
          <a class="day-event bubble" href="https://www.sobeys.com/" target="_blank" rel="noopener"><span class="title">Sobeys</span><span class="time">Winkler</span></a>
          <a class="day-event bubble" href="https://leeversfoods.ca/" target="_blank" rel="noopener"><span class="title">Leevers Foods</span><span class="time">Winkler</span></a>
          <a class="day-event bubble" href="https://www.co-opfuelefficient.com/" target="_blank" rel="noopener"><span class="title">Co-op Gas Bar</span><span class="time">370 Main St</span></a>
          <a class="day-event bubble" href="https://www.petro-canada.ca/" target="_blank" rel="noopener"><span class="title">Petro Canada</span><span class="time">Winkler</span></a>
          <a class="day-event bubble" href="https://www.canadiantire.ca/" target="_blank" rel="noopener"><span class="title">Canadian Tire Gas+</span><span class="time">Winkler</span></a>
          <a class="day-event bubble" href="https://www.redriverco-op.crs/sites/redriver/" target="_blank" rel="noopener"><span class="title">Red River Co-Op</span><span class="time">Winkler</span></a>
          <a class="day-event bubble" href="https://www.homehardware.ca/" target="_blank" rel="noopener"><span class="title">Home Hardware</span><span class="time">Winkler</span></a>
          <a class="day-event bubble" href="https://winklerbiblecamp.ca/" target="_blank" rel="noopener"><span class="title">Winkler Bible Camp</span><span class="time">Winkler</span></a>
        </div>'''

if old_locals in text:
    text = text.replace(old_locals, new_locals, 1)
    print('Converted locals grid to bubbles')
else:
    print('Locals grid not found')

p.write_text(text, encoding='utf-8')
print('Done')
