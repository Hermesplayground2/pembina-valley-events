from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# 1) Extend Activities page to 2 months
old = '''function buildActivityWeek() {
    const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth();
    const today = new Date(year, month, now.getDate());
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const body = document.getElementById('act-days');
    if (!body) return;
    body.innerHTML = '';

    const eventsByDate = {};
    const add = (dateStr, ev) => {
      const parts = dateStr.split('-');
      const evDate = new Date(+parts[0], +parts[1] - 1, +parts[2]);
      const today = new Date(year, month, now.getDate());
      if (evDate < today) return;
      if (!eventsByDate[dateStr]) eventsByDate[dateStr] = [];
      eventsByDate[dateStr].push(ev);
    };

    const dow = (y, m, d) => new Date(y, m, d).getDay();
    const fmt = (y, m, d) => `${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;

    for (let d = 1; d <= daysInMonth; d++) {'''

new = '''function buildActivityWeek() {
    const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const now = new Date();
    const year = now.getFullYear();
    const startMonth = now.getMonth();
    const today = new Date(year, startMonth, now.getDate());
    const monthsToShow = 2;

    const body = document.getElementById('act-days');
    if (!body) return;
    body.innerHTML = '';

    const eventsByDate = {};
    const add = (dateStr, ev) => {
      const parts = dateStr.split('-');
      const evDate = new Date(+parts[0], +parts[1] - 1, +parts[2]);
      if (evDate < today) return;
      if (!eventsByDate[dateStr]) eventsByDate[dateStr] = [];
      eventsByDate[dateStr].push(ev);
    };

    const dow = (y, m, d) => new Date(y, m, d).getDay();
    const fmt = (y, m, d) => `${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;

    for (let monthOffset = 0; monthOffset < monthsToShow; monthOffset++) {
      const month = startMonth + monthOffset;
      const yearForMonth = year + Math.floor(month / 12);
      const actualMonth = month % 12;
      const daysInMonth = new Date(yearForMonth, actualMonth + 1, 0).getDate();'''

if old in text:
    text = text.replace(old, new, 1)
    print('Extended Activities to 2 months')
else:
    print('Activity builder marker not found')

# 2) Close the month loop properly
old_end = '''    }

    // Render
    const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    const sortedDates = Object.keys(eventsByDate).sort();
    if (!sortedDates.length) {
      body.innerHTML = '<div class=\"muted\" style=\"padding:10px;\">No upcoming events in the next 2 months.</div>';
      return;
    }

    let currentMonth = -1;
    sortedDates.forEach(dateStr => {
      const evDate = new Date(dateStr + 'T12:00:00');
      if (evDate.getMonth() !== currentMonth) {
        currentMonth = evDate.getMonth();
        const header = document.createElement('div');
        header.className = 'month-header';
        header.textContent = monthNames[currentMonth] + ' ' + evDate.getFullYear();
        body.appendChild(header);
      }

      const section = document.createElement('div');
      section.className = 'day-section';
      const dateLabel = document.createElement('div');
      dateLabel.className = 'date-label';
      dateLabel.textContent = days[evDate.getDay()] + ', ' + monthNames[currentMonth].slice(0,3) + ' ' + evDate.getDate();
      section.appendChild(dateLabel);

      const list = document.createElement('div');
      list.className = 'event-list';
      eventsByDate[dateStr].forEach(ev => {
        const item = document.createElement('a');
        item.className = 'day-event bubble';
        item.href = ev.link || '#';
        item.target = '_blank';
        item.rel = 'noopener';
        item.setAttribute('data-category', ev.category);
        item.innerHTML = `<span class=\"title\">${ev.title}</span><span class=\"time\" style=\"color:#6b7280; font-size:0.85rem\">${ev.time}</span>`;
        list.appendChild(item);
      });
      section.appendChild(list);
      body.appendChild(section);
    });
  }'''

new_end = '''    }

    // Render
    const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    const sortedDates = Object.keys(eventsByDate).sort();
    if (!sortedDates.length) {
      body.innerHTML = '<div class=\"muted\" style=\"padding:10px;\">No upcoming events in the next 2 months.</div>';
      return;
    }

    let currentMonth = -1;
    let currentYear = -1;
    sortedDates.forEach(dateStr => {
      const evDate = new Date(dateStr + 'T12:00:00');
      if (evDate.getMonth() !== currentMonth || evDate.getFullYear() !== currentYear) {
        currentMonth = evDate.getMonth();
        currentYear = evDate.getFullYear();
        const header = document.createElement('div');
        header.className = 'month-header';
        header.textContent = monthNames[currentMonth] + ' ' + currentYear;
        body.appendChild(header);
      }

      const section = document.createElement('div');
      section.className = 'day-section';
      const dateLabel = document.createElement('div');
      dateLabel.className = 'date-label';
      dateLabel.textContent = days[evDate.getDay()] + ', ' + monthNames[currentMonth].slice(0,3) + ' ' + evDate.getDate();
      section.appendChild(dateLabel);

      const list = document.createElement('div');
      list.className = 'event-list';
      eventsByDate[dateStr].forEach(ev => {
        const item = document.createElement('a');
        item.className = 'day-event bubble';
        item.href = ev.link || '#';
        item.target = '_blank';
        item.rel = 'noopener';
        item.setAttribute('data-category', ev.category);
        item.innerHTML = `<span class=\"title\">${ev.title}</span><span class=\"time\" style=\"color:#6b7280; font-size:0.85rem\">${ev.time}</span>`;
        list.appendChild(item);
      });
      section.appendChild(list);
      body.appendChild(section);
    });
  }'''

if old_end in text:
    text = text.replace(old_end, new_end, 1)
    print('Updated render block')
else:
    print('Render block marker not found')

# 3) Add SEO meta tags
if '<meta name="description"' not in text:
    old_title = '<title>Pembina Valley Events</title>'
    new_title = '''<meta name="description" content="Pembina Valley Events - Local events, activities, and community happenings in Winkler, Morden, Altona, Plum Coulee, and surrounding Manitoba areas. Weather, weekly schedule, monthly calendar, family activities, and local sponsors.">
<meta name="keywords" content="Pembina Valley events, Winkler events, Morden events, Altona events, Manitoba community events, local activities, Winkler weather, Pembina Valley calendar">
<meta property="og:title" content="Pembina Valley Events">
<meta property="og:description" content="Local events, activities, and community happenings in the Pembina Valley region of Manitoba.">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Pembina Valley Events">
<meta name="twitter:description" content="Local events, activities, and community happenings in the Pembina Valley region of Manitoba.">
<link rel="canonical" href="https://pembinaevents.ca/">
<title>Pembina Valley Events</title>'''
    if old_title in text:
        text = text.replace(old_title, new_title, 1)
        print('Added SEO meta tags')
    else:
        print('Title tag not found')

# 4) Improve visual attractiveness
# Add better styling for cards and layout
old_css = '''  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 18px;
  }'''

new_css = '''  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
    transition: transform .2s ease, box-shadow .2s ease;
  }
  .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  }'''

if old_css in text:
    text = text.replace(old_css, new_css, 1)
    print('Updated card styling')

# Improve pill buttons
old_pill = '''  .pill {
    display: inline-flex;
    align-items: center;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    color: #e5e7eb;
    text-decoration: none;
    font-size: 0.85rem;
    border: 1px solid rgba(255,255,255,0.1);
    transition: background .15s ease, transform .1s ease;
  }'''

new_pill = '''  .pill {
    display: inline-flex;
    align-items: center;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    color: #e5e7eb;
    text-decoration: none;
    font-size: 0.85rem;
    border: 1px solid rgba(255,255,255,0.1);
    transition: background .15s ease, transform .1s ease, box-shadow .15s ease;
  }
  .pill:hover {
    background: rgba(255,255,255,0.12);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  }'''

if old_pill in text:
    text = text.replace(old_pill, new_pill, 1)
    print('Updated pill button styling')

# Improve CTA buttons
old_cta = '''  .cta-btn {
    display: inline-flex;
    align-items: center;
    padding: 12px 18px;
    border-radius: 10px;
    background: rgba(255,255,255,0.08);
    color: #e5e7eb;
    text-decoration: none;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,0.12);
    transition: background .15s ease, transform .1s ease;
  }'''

new_cta = '''  .cta-btn {
    display: inline-flex;
    align-items: center;
    padding: 12px 18px;
    border-radius: 10px;
    background: rgba(255,255,255,0.08);
    color: #e5e7eb;
    text-decoration: none;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,0.12);
    transition: background .15s ease, transform .1s ease, box-shadow .15s ease;
  }
  .cta-btn:hover {
    background: rgba(255,255,255,0.15);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
  }'''

if old_cta in text:
    text = text.replace(old_cta, new_cta, 1)
    print('Updated CTA button styling')

p.write_text(text, encoding='utf-8')
print('Done')
