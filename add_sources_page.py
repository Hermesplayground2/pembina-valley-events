import pathlib

p = pathlib.Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Add Sources nav link after Family
old_nav = '    <a href="#page-family" class="nav-link" data-page="family">Family</a>'
new_nav = '    <a href="#page-family" class="nav-link" data-page="family">Family</a>\n    <a href="#page-sources" class="nav-link" data-page="sources">Sources</a>'
if old_nav in text and 'data-page="sources"' not in text:
    text = text.replace(old_nav, new_nav, 1)
    print('Added Sources nav link')
else:
    print('Family nav anchor not found or sources already exists')

# Add Sources page before Dashboard
old_dashboard = '  <div class="page" id="page-dashboard">'
new_sources = '''  <div class="page" id="page-sources">
    <section class="section">
      <h2 class="section-title">📚 Local Event Sources</h2>
      <p class="section-subtitle">Official calendars and event pages from local organizations. These are the sources we monitor for Pembina Valley Events.</p>
      <div class="spacer"></div>

      <div class="grid grid-2">
        <div class="card">
          <h2>🏫 Schools & School Divisions</h2>
          <div class="spacer"></div>
          <div class="event-row"><div class="event-date" style="background:#eef2ff;color:#3730a3;"><div class="month">GVSD</div><div class="day">Cal</div></div><div><div class="event-title"><a href="https://www.gvsd.ca/calendar" target="_blank">Garden Valley School Division</a></div><div class="event-meta">Division-wide calendar</div></div></div>
          <div class="event-row"><div class="event-date" style="background:#eef2ff;color:#3730a3;"><div class="month">PVSD</div><div class="day">Cal</div></div><div><div class="event-title"><a href="https://www.pvsd.ca/" target="_blank">Prairie Valley School Division</a></div><div class="event-muted">Regina-area division calendar</div></div></div>
          <div class="event-row"><div class="event-date" style="background:#eef2ff;color:#3730a3;"><div class="month">PDS</div><div class="day">Cal</div></div><div><div class="event-title"><a href="https://pds.gvsd.ca/" target="_blank">Prairie Dale School</a></div><div class="event-meta">Winkler · K-8 school</div></div></div>
          <div class="event-row"><div class="event-date" style="background:#eef2ff;color:#3730a3;"><div class="month">GVC</div><div class="day">Cal</div></div><div><div class="event-title"><a href="https://gvc.gvsd.ca/calendar" target="_blank">Garden Valley Collegiate</a></div><div class="event-meta">Winkler · High school events</div></div></div>
        </div>

        <div class="card">
          <h2>⛪ Churches & Ministries</h2>
          <div class="spacer"></div>
          <div class="event-row"><div class="event-date" style="background:#fef3c7;color:#92400e;"><div class="month">EMMC</div><div class="day">Ev</div></div><div><div class="event-title"><a href="http://www.winkleremmc.com/events/" target="_blank">Winkler EMMC</a></div><div class="event-meta">Sunday services, church events</div></div></div>
          <div class="event-row"><div class="event-date" style="background:#fef3c7;color:#92400e;"><div class="month">CCM</div><div class="day">Ev</div></div><div><div class="event-title"><a href="https://cc-morden.com/calendar/" target="_blank">Christian Church of Morden</a></div><div class="event-muted">Subscribe to calendar</div></div></div>
          <div class="event-row"><div class="event-date" style="background:#fef3c7;color:#92400e;"><div class="month">PVBC</div><div class="day">Ev</div></div><div><div class="event-title"><a href="https://pvbc.ca/" target="_blank">Pembina Valley Baptist Church</a></div><div class="event-muted">Winkler · VBS & events</div></div></div>
          <div class="event-row"><div class="event-date" style="background:#fef3c7;color:#92400e;"><div class="month">EMM</div><div class="day">Ev</div></div><div><div class="event-title"><a href="https://altonaemmc.com/" target="_blank">Altona EMM Church</a></div><div class="event-muted">Altona · Kidventure & more</div></div></div>
        </div>

        <div class="card">
          <h2>🏙 City & Municipal Events</h2>
          <div class="spacer"></div>
          <div class="event-row"><div class="event-date" style="background:#dcfce7;color:#166534;"><div class="month">MORDEN</div><div class="day">City</div></div><div><div class="event-title"><a href="https://morden.ca/events-festivals" target="_blank">City of Morden Events & Festivals</a></div><div class="event-muted">Annual festivals & city events</div></div></div>
          <div class="event-row"><div class="event-date" style="background:#dcfce7;color:#166534;"><div class="month">MORDEN</div><div class="day">Comm</div></div><div><div class="event-title"><a href="https://morden.ca/community-events" target="_blank">Morden Community Events</a></div><div class="event-muted">Submit events · Council · Fundraisers</div></div></div>
          <div class="event-row"><div class="event-date" style="background:#dcfce7;color:#166534;"><div class="month">ALTONA</div><div class="day">Cal</div></div><div><div class="event-title"><a href="https://altona.ca/upcoming-events" target="_blank">Town of Altona Events</a></div><div class="event-muted">Calendar · Recreation · Community</div></div></div>
          <div class="event-row"><div class="event-date" style="background:#dcfce7;color:#166534;"><div class="month">WINKLER</div><div class="day">City</div></div><div><div class="event-title"><a href="https://www.winkler.ca/events" target="_blank">City of Winkler Events</a></div><div class="event-muted">City-run events & announcements</div></div></div>
        </div>

        <div class="card">
          <h2>🌐 Regional Community Calendars</h2>
          <div class="spacer"></div>
          <div class="event-row"><div class="event-date" style="background:#f1f5f9;color:#0f172a;"><div class="month">PVO</div><div class="day">Ev</div></div><div><div class="event-title"><a href="https://www.pembinavalleyonline.com/events" target="_blank">Pembina Valley Online Events</a></div><div class="event-muted">Regional community calendar</div></div></div>
          <div class="event-row"><div class="event-date" style="background:#f1f5f9;color:#0f172a;"><div class="month">PVO</div><div class="day">GW</div></div><div><div class="event-title"><a href="https://pembinavalley.gwevents.ca/" target="_blank">Pembina Valley Events Guide</a></div><div class="event-muted">Submit events · Browse calendar</div></div></div>
          <div class="event-row"><div class="event-date" style="background:#f1f5f9;color:#0f172a;"><div class="month">AEC</div><div class="day">Rec</div></div><div><div class="event-title"><a href="https://morden.ca/access-event-centre" target="_blank">Access Event Centre</a></div><div class="event-muted">Morden recreation & rentals</div></div></div>
          <div class="event-row"><div class="event-date" style="background:#f1f5f9;color:#0f172a;"><div class="month">PVHS</div><div class="day">Ev</div></div><div><div class="event-title"><a href="https://pvhsociety.ca/events/" target="_blank">Pembina Valley Humane Society</a></div><div class="event-muted">Fundraisers & community events</div></div></div>
        </div>
      </div>

      <div class="spacer"></div>
      <div class="card">
        <h2>🎪 Festivals & Annual Events</h2>
        <div class="spacer"></div>
        <div class="event-row"><div class="event-date" style="background:#fef3c7;color:#92400e;"><div class="month">AUG</div><div class="day">28-30</div></div><div><div class="event-title"><a href="https://cornandapple.com/" target="_blank">Morden Corn & Apple Festival</a></div><div class="event-muted">Manitoba's largest street festival</div></div></div>
        <div class="event-row"><div class="event-date" style="background:#fef3c7;color:#92400e;"><div class="month">AUG</div><div class="day">29</div></div><div><div class="event-title"><a href="https://www.backfortymusicfestival.com/" target="_blank">Morden Back40 Music Festival</a></div><div class="event-muted">Since 1989 · Downtown Morden</div></div></div>
        <div class="event-row"><div class="event-date" style="background:#fef3c7;color:#92400e;"><div class="month">AUG</div><div class="day">7-9</div></div><div><div class="event-title"><a href="https://www.winklerharvestfestival.com/" target="_blank">Winkler Harvest Festival</a></div><div class="event-muted">3 days · Fairgrounds · Free music</div></div></div>
        <div class="event-row"><div class="event-date" style="background:#fef3c7;color:#92400e;"><div class="month">JULY</div><div class="day">Jul</div></div><div><div class="event-title"><a href="https://manitobasunflowerfestival.ca/" target="_blank">Manitoba Sunflower Festival</a></div><div class="event-muted">Altona · Annual since 1964</div></div></div>
        <div class="event-row"><div class="event-date" style="background:#fef3c7;color:#92400e;"><div class="month">AUG</div><div class="day">Aug</div></div><div><div class="event-title"><a href="https://www.plumfest.com/" target="_blank">Plum Fest</a></div><div class="event-muted">Plum Coulee · Summer festival</div></div></div>
        <div class="event-row"><div class="event-date" style="background:#fef3c7;color:#92400e;"><div class="month">SEP</div><div class="day">Sep</div></div><div><div class="event-title"><a href="https://www.threshermensmuseum.com/special-events" target="_blank">Pembina Threshermen's Reunion</a></div><div class="event-muted">Morden/Winkler · Heritage & machinery</div></div></div>
      </div>
    </section>
  </div>

  <div class="page" id="page-dashboard">'''

if old_dashboard in text and 'id="page-sources"' not in text:
    text = text.replace(old_dashboard, new_sources, 1)
    print('Added Sources page before Dashboard')
else:
    print('Dashboard anchor not found or Sources already exists')

p.write_text(text, encoding='utf-8')
print('Done')
