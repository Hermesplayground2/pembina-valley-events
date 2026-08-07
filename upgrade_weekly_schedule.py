from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Critical structure checks
critical = {
    'Home': 'id="page-home"' in text,
    'Activities': 'id="page-activities"' in text,
    'Family': 'id="page-family"' in text,
    'Sources': 'id="page-sources"' in text,
    'Contact': 'id="page-contact"' in text,
    'PVBC': 'Aug 12-14' in text,
    'JS': 'function buildActivityWeek()' in text,
    'SEO': 'meta name="description"' in text,
}
if not all(critical.values()):
    print('Critical missing, abort')
    exit(1)
print('✓ Critical structure intact')

# === BATCH 1: Fix duplicate events in buildWeek ===
# Remove duplicate Morden Corn & Apple Festival entries
text = text.replace(
    "      if (currentMonth === 7 && d >= 28 && d <= 30) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Downtown Morden · Free', link: 'https://cornandapple.com/' });\n      if (currentMonth === 7 && d >= 28 && d <= 30) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Downtown Morden · Free', link: 'https://cornandapple.com/' });",
    "      if (currentMonth === 7 && d >= 28 && d <= 30) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Downtown Morden · Free', link: 'https://cornandapple.com/' });"
)
print('✓ Removed duplicate Morden Corn & Apple Festival')

# Remove duplicate Morden Farmers Market entries
text = text.replace(
    "      if (currentMonth === 7 && d === 6) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });\n      if (currentMonth === 7 && d === 24) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', link: 'https://morden.ca/community-events' });\n      if (currentMonth === 7 && d === 17) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'MCC Blanket Making', time: '9:30 AM · Morden Mennonite Church', link: 'https://morden.ca/community-events' });\n      if (currentMonth === 7 && d === 19) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta', link: 'https://morden.ca/access-event-centre' });\n      if (currentMonth === 7 && d === 6) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });",
    "      if (currentMonth === 7 && d === 6) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });\n      if (currentMonth === 7 && d === 24) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', link: 'https://morden.ca/community-events' });\n      if (currentMonth === 7 && d === 17) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'MCC Blanket Making', time: '9:30 AM · Morden Mennonite Church', link: 'https://morden.ca/community-events' });\n      if (currentMonth === 7 && d === 19) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta', link: 'https://morden.ca/access-event-centre' });"
)
print('✓ Removed duplicate Morden Farmers Market')

# Remove duplicate Morden Council Meeting
text = text.replace(
    "      if (currentMonth === 7 && d === 24) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', link: 'https://morden.ca/community-events' });\n      if (currentMonth === 7 && d === 17) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'MCC Blanket Making', time: '9:30 AM · Morden Mennonite Church', link: 'https://morden.ca/community-events' });\n      if (currentMonth === 7 && d === 19) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta', link: 'https://morden.ca/access-event-centre' });\n      if (currentMonth === 7 && d === 12) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Kidventure Wednesdays', time: '1:00 PM · Altona EMM Church', link: 'https://altonaemmc.com/' });\n      if (currentMonth === 7 && d === 6) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });\n      if (currentMonth === 7 && d === 8) addIfInWeek(fmt(year, month, d), { category: 'fundraiser', title: 'Fundraising BBQ', time: '11:30 AM · Faith Mission, Winkler', link: 'https://winklerchamber.com/events/' });",
    "      if (currentMonth === 7 && d === 24) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', link: 'https://morden.ca/community-events' });\n      if (currentMonth === 7 && d === 17) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'MCC Blanket Making', time: '9:30 AM · Morden Mennonite Church', link: 'https://morden.ca/community-events' });\n      if (currentMonth === 7 && d === 19) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta', link: 'https://morden.ca/access-event-centre' });\n      if (currentMonth === 7 && d === 12) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Kidventure Wednesdays', time: '1:00 PM · Altona EMM Church', link: 'https://altonaemmc.com/' });\n      if (currentMonth === 7 && d === 6) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });\n      if (currentMonth === 7 && d === 8) addIfInWeek(fmt(year, month, d), { category: 'fundraiser', title: 'Fundraising BBQ', time: '11:30 AM · Faith Mission, Winkler', link: 'https://winklerchamber.com/events/' });"
)
print('✓ Removed duplicate Morden Council Meeting')

# Remove duplicate Morden Back40
text = text.replace(
    "      if (currentMonth === 7 && d === 29) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Back40 Music Festival', time: 'Morden, MB', link: 'https://www.backfortymusicfestival.com/' });\n      if (currentMonth === 7 && d === 24) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', link: 'https://morden.ca/community-events' });",
    "      if (currentMonth === 7 && d === 29) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Back40 Music Festival', time: 'Morden, MB', link: 'https://www.backfortymusicfestival.com/' });\n      if (currentMonth === 7 && d === 24) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', link: 'https://morden.ca/community-events' });"
)
print('✓ Removed duplicate Morden Back40')

# === BATCH 2: Add Today schedule to home page ===
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
    print('✓ Added Today schedule section to home page')
else:
    print('✗ Weekly section marker not found')

# === BATCH 3: Add buildToday function to JS ===
# Find the end of buildWeek function
buildweek_end = text.find('  }', text.find('function buildWeek()'))
buildweek_end = text.find('\n', buildweek_end) + 1

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

# Insert after buildWeek function
if buildweek_end != -1 and build_today_js not in text:
    text = text[:buildweek_end] + build_today_js + '\n' + text[buildweek_end:]
    print('✓ Added buildToday function')
else:
    print('✗ Could not insert buildToday')

# Add buildToday() call after existing buildWeek() call
old_onload = 'buildWeek();'
new_onload = 'buildWeek();\n    buildToday();'
text = text.replace(old_onload, new_onload, 1)
print('✓ Added buildToday() call')

p.write_text(text, encoding='utf-8')
print('\n✅ Weekly schedule upgrade complete')
