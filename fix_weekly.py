from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

marker_start = "function buildWeek() {"
marker_end = "function filterDayActivities(category, btn) {"
start = text.find(marker_start)
end = text.find(marker_end)
if start == -1 or end == -1:
    raise SystemExit("Markers not found")

old_block = text[start:end]
new_block = '''function buildWeek() {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const start = new Date(today);
    start.setDate(today.getDate() - today.getDay());

    const header = document.getElementById('cal-header');
    const body = document.getElementById('daily-events');
    if (!header || !body) return;
    header.innerHTML = '';
    body.innerHTML = '';

    const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const year = now.getFullYear();
    const month = now.getMonth();
    const rangeStart = new Date(start);
    const rangeEnd = new Date(start);
    rangeEnd.setDate(start.getDate() + 6);
    const eventsByDay = [[], [], [], [], [], [], []];

    const addIfInWeek = (dateStr, ev) => {
      const parts = dateStr.split('-');
      const evDate = new Date(+parts[0], +parts[1] - 1, +parts[2]);
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      if (evDate < today) return;
      if (evDate >= rangeStart && evDate <= rangeEnd) {
        const diff = Math.round((evDate - start) / 86400000);
        if (diff >= 0 && diff < 7) eventsByDay[diff].push(ev);
      }
    };

    const fmt = (y, m, d) => `${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    for (let d = 1; d <= daysInMonth; d++) {
      const dow = new Date(year, month, d).getDay();
      if (dow === 2) addIfInWeek(fmt(year, month, d), { category: 'community', title: "Winkler Farmer's Market", time: 'Tue 4-6 PM · Central Station parking lot', link: 'https://www.pembinavalleyonline.com/events' });
      if (month === 7 && dow === 3) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Concerts in the Park', time: 'Wed 7:00 PM · Bethel Heritage Park', link: 'https://www.visitwinkler.ca/concerts-in-the-park' });
      if (month === 7 && d >= 7 && d <= 9) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Winkler Harvest Festival', time: 'Fairgrounds', link: 'https://www.winklerharvestfestival.com/' });
      if (month === 7 && d === 6) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Paper Chain Creations', time: '10:30 AM & 1:30 PM · Winkler Library', link: 'https://www.winklerlibrary.ca' });
      if (month === 7 && d === 5) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Summer Storytime', time: '10:30 AM & 1:30 PM · Winkler Library', link: 'https://www.winklerlibrary.ca' });
      if (month === 8 && d === 4) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Catie St. Germain and Brothers Keep', time: '7:00 PM · Concert Hall', link: 'https://www.visitwinkler.ca' });
      if (month === 8 && d === 18) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Summer Shores Paint & Sip', time: '6:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
      if (month === 9 && d === 18) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Chamber Member Appreciation BBQ', time: 'Winkler City Hall · 185 Main St', link: 'https://winklerchamber.com/events/' });
      if (month === 9 && d === 7) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Municipal Forum', time: 'P.W. Enns Centennial Concert Hall', link: 'https://www.winkler.ca/events' });
      if (month === 8 && d === 10) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Mosaic Tray Workshop', time: '7:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
      if (month === 8 && d === 10) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Jr. Summer Art Camp (5-8)', time: '9:30 AM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
      if (month === 8 && d === 10) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Summer Art Camp (9-12)', time: '1:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
      if (month === 8 && d === 2) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive', link: 'http://www.winkleremmc.com/events/' });
      if (month === 8 && d >= 28 && d <= 30) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Downtown Morden · Free', link: 'https://cornandapple.com/' });
      if (month === 8 && d === 29) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Back40 Music Festival', time: 'Morden, MB', link: 'https://www.backfortymusicfestival.com/' });
      if (month === 8 && d === 24) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', link: 'https://morden.ca/community-events' });
      if (month === 8 && d === 17) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'MCC Blanket Making', time: '9:30 AM · Morden Mennonite Church', link: 'https://morden.ca/community-events' });
      if (month === 8 && d === 19) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta', link: 'https://morden.ca/access-event-centre' });
      if (month === 8 && d === 12) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Kidventure Wednesdays', time: '1:00 PM · Altona EMM Church', link: 'https://altonaemmc.com/' });
      if (month === 8 && d === 6) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });
      if (month === 8 && d === 8) addIfInWeek(fmt(year, month, d), { category: 'fundraiser', title: 'Fundraising BBQ', time: '11:30 AM · Faith Mission, Winkler', link: 'https://winklerchamber.com/events/' });
      if (month === 8 && d === 9) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Harvest Festival Service', time: '10:00 AM · Winkler Park · Winkler EMMC', link: 'http://www.winkleremmc.com/events/' });
      if (month === 8 && d === 16) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive', link: 'http://www.winkleremmc.com/events/' });
      if (month === 8 && d === 18) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Church Council Mtg', time: '7:00 PM · 600 Southview Drive', link: 'http://www.winkleremmc.com/events/' });
      if (month === 8 && d === 23) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive', link: 'http://www.winkleremmc.com/events/' });
      if (month === 8 && d === 30) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive', link: 'http://www.winkleremmc.com/events/' });
      if (month === 8 && d === 7) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Labour Day - No School', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
      if (month === 8 && d === 8) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Prairie Dale No Classes Admin Day', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
      if (month === 8 && d === 9) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Prairie Dale First Day Grades K-9', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
      if (month === 8 && d === 10) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Prairie Dale First Day Grades 10-12', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
    }

    for (let i = 0; i < 7; i++) {
      const dayEvents = eventsByDay[i];
      if (!dayEvents.length) continue;

      const d = new Date(start);
      d.setDate(start.getDate() + i);
      const dateLabel = document.createElement('div');
      dateLabel.style.gridColumn = '1 / -1';
      dateLabel.style.fontWeight = '800';
      dateLabel.style.marginTop = '12px';
      dateLabel.textContent = days[d.getDay()] + ' · ' + months[d.getMonth()] + ' ' + d.getDate();
      header.appendChild(dateLabel);

      dayEvents.forEach(ev => {
        const el = document.createElement('a');
        el.className = 'day-event bubble';
        el.href = ev.link || '#';
        el.target = '_blank';
        el.rel = 'noopener';
        el.dataset.category = ev.category;
        el.innerHTML = `<span class="title">${ev.title}</span><span class="time">${ev.time}</span>`;
        body.appendChild(el);
      });
    }
  }
'''

if old_block not in text:
    raise SystemExit("Old block not found exactly")

text = text.replace(old_block, new_block)
p.write_text(text, encoding='utf-8')
print('Updated buildWeek')
