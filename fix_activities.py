from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Find buildActivityWeek function boundaries
idx = text.find('function buildActivityWeek()')
end_idx = text.find('function buildMonth()')
before = text[:idx]
after = text[end_idx:]

new_func = '''function buildActivityWeek() {
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
      const daysInMonth = new Date(yearForMonth, actualMonth + 1, 0).getDate();
      for (let d = 1; d <= daysInMonth; d++) {
        if (dow(yearForMonth, actualMonth, d) === 2) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: "Winkler Farmer's Market", time: 'Tue 4-6 PM · Central Station parking lot', link: 'https://www.pembinavalleyonline.com/events' });
        if (actualMonth === 6 && dow(yearForMonth, actualMonth, d) === 3) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Concerts in the Park', time: 'Wed 7:00 PM · Bethel Heritage Park', link: 'https://www.visitwinkler.ca/concerts-in-the-park' });
        if (actualMonth === 6 && d >= 5 && d <= 6) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Summer Storytime', time: '10:30 AM & 1:30 PM · Winkler Library', link: 'https://www.winklerlibrary.ca' });
        if (actualMonth === 6 && d === 6) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Paper Chain Creations', time: '10:30 AM & 1:30 PM · Winkler Library', link: 'https://www.winklerlibrary.ca' });
        if (actualMonth === 6 && d >= 7 && d <= 9) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Winkler Harvest Festival', time: 'Fairgrounds', link: 'https://www.winklerharvestfestival.com/' });
        if (actualMonth === 7 && d === 4) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Catie St. Germain and Brothers Keep', time: '7:00 PM · Concert Hall', link: 'https://www.visitwinkler.ca' });
        if (actualMonth === 7 && d === 10) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Mosaic Tray Workshop', time: '7:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
        if (actualMonth === 7 && d === 10) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Jr. Summer Art Camp (5-8)', time: '9:30 AM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
        if (actualMonth === 7 && d === 10) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Summer Art Camp (9-12)', time: '1:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
        if (actualMonth === 7 && d >= 3 && d <= 7) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'PVBC Vacation Bible School', time: 'Ages 5-12 · Winkler MB', link: 'http://www.pembinavalleybaptistchurch.com/ministries/children-s-ministries/vbs/' });
        if (actualMonth === 7 && d === 2) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive', link: 'http://www.winkleremmc.com/events/' });
        if (actualMonth === 6 && d >= 14 && d <= 16) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Plum Coulee Plum Fest', time: '125th Anniversary · Plum Coulee MB', link: 'http://www.plumfest.com/' });
        if (actualMonth === 7 && d >= 28 && d <= 30) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Downtown Morden · Free', link: 'https://cornandapple.com/' });
        if (actualMonth === 7 && d === 29) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Morden Back40 Music Festival', time: 'Morden, MB', link: 'https://www.backfortymusicfestival.com/' });
        if (actualMonth === 7 && d === 24) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', link: 'https://morden.ca/community-events' });
        if (actualMonth === 7 && d === 17) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'MCC Blanket Making', time: '9:30 AM · Morden Mennonite Church', link: 'https://morden.ca/community-events' });
        if (actualMonth === 7 && d === 19) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta', link: 'https://morden.ca/access-event-centre' });
        if (actualMonth === 7 && d === 6) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });
        if (actualMonth === 7 && d === 12) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Kidventure Wednesdays', time: '1:00 PM · Altona EMM Church', link: 'https://altonaemmc.com/' });
        if (actualMonth === 7 && d === 8) add(fmt(yearForMonth, actualMonth, d), { category: 'fundraiser', title: 'Fundraising BBQ', time: '11:30 AM · Faith Mission, Winkler', link: 'https://winklerchamber.com/events/' });
        if (actualMonth === 7 && d === 9) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Harvest Festival Service', time: '10:00 AM · Winkler Park · Winkler EMMC', link: 'http://www.winkleremmc.com/events/' });
        if (actualMonth === 7 && d === 16) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive', link: 'http://www.winkleremmc.com/events/' });
        if (actualMonth === 7 && d === 18) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Winkler EMMC Church Council Mtg', time: '7:00 PM · 600 Southview Drive', link: 'http://www.winkleremmc.com/events/' });
        if (actualMonth === 7 && d === 23) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive', link: 'http://www.winkleremmc.com/events/' });
        if (actualMonth === 7 && d === 30) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive', link: 'http://www.winkleremmc.com/events/' });
        if (actualMonth === 7 && d === 7) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Labour Day - No School', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
        if (actualMonth === 7 && d === 8) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Prairie Dale No Classes Admin Day', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
        if (actualMonth === 7 && d === 9) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Prairie Dale First Day Grades K-9', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
        if (actualMonth === 7 && d === 10) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Prairie Dale First Day Grades 10-12', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
        if (actualMonth === 8 && d === 18) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Summer Shores Paint & Sip', time: '6:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
        if (actualMonth === 8 && d === 18) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Chamber Member Appreciation BBQ', time: 'Winkler City Hall · 185 Main St', link: 'https://winklerchamber.com/events/' });
        if (actualMonth === 8 && d === 7) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Municipal Forum', time: 'P.W. Enns Centennial Concert Hall', link: 'https://www.winkler.ca/events' });
      }
    }

    const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    const sortedDates = Object.keys(eventsByDate).sort();
    if (!sortedDates.length) {
      body.innerHTML = '<div class="muted" style="padding:10px;">No upcoming events in the next 2 months.</div>';
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
        item.dataset.category = ev.category;
        item.innerHTML = '<span class="title" style="font-weight:600">' + ev.title + '</span><span class="time" style="color:#6b7280; font-size:0.85rem">' + ev.time + '</span>';
        list.appendChild(item);
      });
      section.appendChild(list);
      body.appendChild(section);
    });
  }

  function buildMonth() {'''

text = before + new_func + after
p.write_text(text, encoding='utf-8')
print('Rewrote buildActivityWeek cleanly')
