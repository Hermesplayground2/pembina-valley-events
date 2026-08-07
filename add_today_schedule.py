from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Critical checks
critical = {
    'Home': 'id="page-home"' in text,
    'Activities': 'id="page-activities"' in text,
    'Family': 'id="page-family"' in text,
    'Sources': 'id="page-sources"' in text,
    'Contact': 'id="page-contact"' in text,
    'PVBC': 'Aug 12-14' in text,
    'SEO': 'meta name="description"' in text,
    'buildActivityWeek': 'function buildActivityWeek()' in text,
    'buildMonth': 'function buildMonth()' in text,
    'renderFeatured': 'function renderFeatured()' in text,
    'renderFamilyEvents': 'function renderFamilyEvents()' in text,
}
if not all(critical.values()):
    print('Critical missing, abort')
    exit(1)
print('✓ Critical structure intact')

# === STEP 1: Add Today Schedule HTML section ===
old_weekly_section = '''    <section class="section">
      <div class="card card-landscape-calendar">
        <h2>📅 Weekly Schedule</h2>
        <div class="filters">
          <button class="pill active" onclick="filterDailyEvents('all', this)">All</button>
          <button class="pill" onclick="filterDailyEvents('today', this)">Today</button>
          <button class="pill" onclick="filterDailyEvents('tomorrow', this)">Tomorrow</button>
          <button class="pill" onclick="filterDailyEvents('weekend', this)">This Weekend</button>
          <button class="pill" onclick="filterDailyEvents('community', this)">Community</button>
          <button class="pill" onclick="filterDailyEvents('outdoors', this)">Outdoors</button>
          <button class="pill" onclick="filterDailyEvents('family', this)">Family</button>
        </div>
        <div class="cal-header" id="cal-header"></div>
        <div class="day-columns" id="daily-events"></div>
      </div>
    </section>'''

new_weekly_section = '''    <section class="section">
      <div class="card card-landscape-calendar">
        <h2>📅 Weekly Schedule</h2>
        <div class="filters">
          <button class="pill active" onclick="filterDailyEvents('all', this)">All</button>
          <button class="pill" onclick="filterDailyEvents('today', this)">Today</button>
          <button class="pill" onclick="filterDailyEvents('tomorrow', this)">Tomorrow</button>
          <button class="pill" onclick="filterDailyEvents('weekend', this)">This Weekend</button>
          <button class="pill" onclick="filterDailyEvents('community', this)">Community</button>
          <button class="pill" onclick="filterDailyEvents('outdoors', this)">Outdoors</button>
          <button class="pill" onclick="filterDailyEvents('family', this)">Family</button>
        </div>
        <div class="cal-header" id="cal-header"></div>
        <div class="day-columns" id="daily-events"></div>
      </div>
    </section>

    <section class="section">
      <div class="card card-landscape-calendar">
        <h2>📌 Today\'s Schedule</h2>
        <p class="muted" id="today-date-label">Loading today\'s events...</p>
        <div class="spacer"></div>
        <div id="today-events"></div>
      </div>
    </section>'''

if old_weekly_section in text:
    text = text.replace(old_weekly_section, new_weekly_section, 1)
    print('✓ Added Today schedule HTML section')
else:
    print('✗ Weekly section marker not found')

# === STEP 2: Add buildToday function ===
build_today_js = '''
  function buildToday() {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const year = now.getFullYear();
    const month = now.getMonth();
    const dateStr = `${year}-${String(month+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
    
    const container = document.getElementById('today-events');
    const label = document.getElementById('today-date-label');
    if (!container) return;
    
    container.innerHTML = '';
    
    const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    if (label) {
      label.textContent = `${monthNames[month]} ${now.getDate()}, ${year}`;
    }
    
    const events = [];
    
    const add = (title, time, category, link) => {
      events.push({ title, time, category, link });
    };
    
    // Recurring weekly events
    const dow = new Date(year, month, now.getDate()).getDay();
    if (dow === 2) add("Winkler Farmer's Market", "4:00 PM - 6:00 PM · Central Station parking lot", "community", "https://www.pembinavalleyonline.com/events");
    if (month === 7 && dow === 3) add("Concerts in the Park", "7:00 PM · Bethel Heritage Park", "community", "https://www.visitwinkler.ca/concerts-in-the-park");
    
    // Specific date events for August 2025
    if (month === 7 && now.getDate() === 4) add("Catie St. Germain and Brothers Keep", "7:00 PM · Concert Hall", "community", "https://www.visitwinkler.ca");
    if (month === 7 && now.getDate() === 6) add("Morden Farmers Market", "4:00 PM · 8th Street", "community", "https://morden.ca/community-events");
    if (month === 7 && now.getDate() === 7) add("Labour Day - No School", "Prairie Dale School", "family", "https://pds.gvsd.ca/");
    if (month === 7 && now.getDate() === 8) add("Prairie Dale No Classes Admin Day", "Prairie Dale School", "family", "https://pds.gvsd.ca/");
    if (month === 7 && now.getDate() === 9) add("Prairie Dale First Day Grades K-9", "Prairie Dale School", "family", "https://pds.gvsd.ca/");
    if (month === 7 && now.getDate() === 10) add("Prairie Dale First Day Grades 10-12", "Prairie Dale School", "family", "https://pds.gvsd.ca/");
    if (month === 7 && now.getDate() === 12) add("Kidventure Wednesdays", "1:00 PM · Altona EMM Church", "community", "https://altonaemmc.com/");
    if (month === 7 && now.getDate() === 17) add("MCC Blanket Making", "9:30 AM · Morden Mennonite Church", "community", "https://morden.ca/community-events");
    if (month === 7 && now.getDate() === 18) add("Summer Shores Paint & Sip", "6:00 PM · Winkler Arts & Culture", "community", "https://www.visitwinkler.ca");
    if (month === 7 && now.getDate() === 19) add("The Big Canoe", "9:00 AM · Lake Minnewasta", "community", "https://morden.ca/access-event-centre");
    if (month === 7 && now.getDate() === 23) add("Winkler EMMC Worship Service", "10:30 AM · 600 Southview Drive", "family", "http://www.winkleremmc.com/events/");
    if (month === 7 && now.getDate() === 24) add("Morden Council Meeting", "7:00 PM · 500 Stephen St", "community", "https://morden.ca/community-events");
    if (month === 7 && now.getDate() === 25) add("Morden Farmers Market", "4:00 PM · 8th Street", "community", "https://morden.ca/community-events");
    if (month === 7 && now.getDate() === 26) add("Kidventure Wednesdays", "1:00 PM · Altona EMM Church", "community", "https://altonaemmc.com/");
    if (month === 7 && now.getDate() === 29) add("Morden Back40 Music Festival", "Morden, MB", "community", "https://www.backfortymusicfestival.com/");
    if (month === 7 && now.getDate() === 30) add("Winkler EMMC Worship Service", "10:30 AM · 600 Southview Drive", "family", "http://www.winkleremmc.com/events/");
    if (month === 6 && now.getDate() >= 14 && now.getDate() <= 16) add("Plum Coulee Plum Fest", "125th Anniversary · Plum Coulee MB", "community", "http://www.plumfest.com/");
    if (month === 6 && now.getDate() >= 7 && now.getDate() <= 9) add("Winkler Harvest Festival", "Fairgrounds", "community", "https://www.winklerharvestfestival.com/");
    
    // PVBC VBS Aug 12-14
    if (month === 7 && now.getDate() >= 12 && now.getDate() <= 14) add("PVBC Vacation Bible School", "Times vary · Pembina Valley Baptist Church", "faith", "http://www.pembinavalleybaptistchurch.com/");
    
    // Sort by time
    events.sort((a, b) => a.time.localeCompare(b.time));
    
    if (events.length === 0) {
      container.innerHTML = '<p class="muted">No events scheduled for today.</p>';
      return;
    }
    
    events.forEach(ev => {
      const el = document.createElement('a');
      el.className = 'day-event bubble';
      el.href = ev.link || '#';
      el.target = '_blank';
      el.rel = 'noopener';
      el.dataset.category = ev.category;
      el.innerHTML = `<span class="title">${ev.title}</span><span class="time">${ev.time}</span><div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, '&quot;')}" data-time="${ev.time.replace(/"/g, '&quot;')}" data-date="${dateStr}">ICS</button></div>`;
      container.appendChild(el);
    });
  }
'''

# Insert buildToday AFTER buildActivityWeek, before buildMonth
insert_marker = 'function buildMonth()'
if insert_marker in text and 'function buildToday()' not in text:
    insert_pos = text.find(insert_marker)
    text = text[:insert_pos] + build_today_js + '\n' + text[insert_pos:]
    print('✓ Inserted buildToday function before buildMonth')
else:
    print('✗ Could not insert buildToday')

# === STEP 3: Add buildToday() call ===
# Find the init calls at the end
init_marker = 'buildWeek();'
if init_marker in text and 'buildToday();' not in text:
    text = text.replace(init_marker, init_marker + '\n    buildToday();', 1)
    print('✓ Added buildToday() call after buildWeek()')
else:
    print('✗ Could not add buildToday() call')

p.write_text(text, encoding='utf-8')
print('\n✅ Today schedule added successfully')
