
function addToCalendar(title, time, date) {
  let startDate = date ? new Date(date + 'T12:00:00') : new Date();
  let endDate = new Date(startDate);
  let location = '';
  let description = (time || '').trim();

  if (description) {
    const rangeMatch = description.match(/(\d{1,2}:\d{2}\s*(?:AM|PM)?)\s*-\s*(\d{1,2}:\d{2}\s*(?:AM|PM)?)/i);
    if (rangeMatch) {
      startDate = combineDateTime(date, rangeMatch[1]);
      endDate = combineDateTime(date, rangeMatch[2]);
    } else {
      const singleMatch = description.match(/(\d{1,2}:\d{2}\s*(?:AM|PM)?)/i);
      if (singleMatch) {
        startDate = combineDateTime(date, singleMatch[1]);
        endDate = new Date(startDate.getTime() + 60 * 60 * 1000);
      }
    }

    const locMatch = description.match(/·\s*([^·]+?)\s*(?:·|$)/);
    if (locMatch) {
      location = locMatch[1].trim();
    }
  }

  const pad = (n) => String(n).padStart(2, '0');
  const fmt = (d) => d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()) + 'T' + pad(d.getHours()) + pad(d.getMinutes()) + '00';
  const stamp = fmt(new Date());

  const escape = (val) => (val || '').replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\n/g, '\\n');

  const ics = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Pembina Valley Events//EN',
    'METHOD:REQUEST',
    'BEGIN:VEVENT',
    'UID:pembina-' + Date.now() + '@pembinaevents.ca',
    'DTSTAMP:' + stamp,
    'DTSTART:' + fmt(startDate),
    'DTEND:' + fmt(endDate),
    'SUMMARY:' + escape(title || 'Event'),
    'DESCRIPTION:' + escape(description || ''),
    location ? 'LOCATION:' + escape(location) : '',
    'END:VEVENT',
    'END:VCALENDAR'
  ].filter(Boolean).join('\n');

  const blob = new Blob([ics], { type: 'text/calendar;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  
  if (/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
    const newWin = window.open(url, '_blank');
    if (!newWin) {
      const a = document.createElement('a');
      a.href = url;
      a.download = (title || 'event').replace(/[^a-z0-9]+/gi, '_') + '.ics';
      document.body.appendChild(a);
      a.click();
      a.remove();
    }
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  } else {
    const a = document.createElement('a');
    a.href = url;
    a.download = (title || 'event').replace(/[^a-z0-9]+/gi, '_') + '.ics';
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
}

function combineDateTime(dateStr, timeStr) {
  const d = dateStr ? new Date(dateStr + 'T12:00:00') : new Date();
  const match = String(timeStr).match(/(\d{1,2}):(\d{2})\s*(AM|PM)?/i);
  if (!match) return d;
  let hours = parseInt(match[1], 10);
  const minutes = parseInt(match[2], 10);
  const meridiem = match[3] ? match[3].toUpperCase() : null;
  if (meridiem === 'PM' && hours < 12) hours += 12;
  if (meridiem === 'AM' && hours === 12) hours = 0;
  d.setHours(hours, minutes, 0, 0);
  return d;
}


  function renderDashboard() {
    const box = document.getElementById('dashboard-live');
    if (!box) return;
    box.innerHTML = '<p class="muted">Real traffic data comes from your analytics provider.</p><p class="muted">Check your Cloudflare dashboard for live visitor counts, page views, and traffic sources. Numbers should start appearing within 24–48 hours.</p>';
  }

  function buildUpcoming() {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const start = new Date(today);
    const rangeEnd = new Date(start);
    rangeEnd.setDate(start.getDate() + 7);

    const body = document.getElementById('daily-events');
    if (!body) return;
    body.innerHTML = '';

    const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const year = now.getFullYear();
    const month = now.getMonth();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const fmt = (y, m, d) => `${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;

    const items = [];
    const add = (dateStr, ev) => {
      const parts = dateStr.split('-');
      const evDate = new Date(+parts[0], +parts[1] - 1, +parts[2]);
      if (evDate <= today) return;
      if (evDate > rangeEnd) return;
      items.push({ dateStr, ev });
    };

    for (let d = 1; d <= daysInMonth; d++) {
      const dow = new Date(year, month, d).getDay();
      if (dow === 2) add(fmt(year, month, d), { category: 'community', title: "Winkler Farmer's Market", time: 'Tue 4-6 PM · Central Station parking lot', link: 'https://www.pembinavalleyonline.com/events' });
      if (month === 7 && dow === 3) add(fmt(year, month, d), { category: 'community', title: 'Concerts in the Park', time: 'Wed 7:00 PM · Bethel Heritage Park', link: 'https://www.visitwinkler.ca/concerts-in-the-park' });

      if (month === 6 && d === 6) add(fmt(year, month, d), { category: 'community', title: 'Paper Chain Creations', time: '10:30 AM & 1:30 PM · Winkler Library', link: 'https://www.winklerlibrary.ca' });
      if (month === 6 && d === 5) add(fmt(year, month, d), { category: 'community', title: 'Summer Storytime', time: '10:30 AM & 1:30 PM · Winkler Library', link: 'https://www.winklerlibrary.ca' });
      if (month === 7 && d === 4) add(fmt(year, month, d), { category: 'community', title: 'Catie St. Germain and Brothers Keep', time: '7:00 PM · Concert Hall', link: 'https://www.visitwinkler.ca' });
      if (month === 7 && d === 11) add(fmt(year, month, d), { category: 'family', title: 'Finger Painting Workshop', time: '10:30 AM & 1:30 PM · Winkler Library', link: 'https://pembinavalleyonline.com/events/229002' });
      if (month === 7 && d === 13) add(fmt(year, month, d), { category: 'community', title: 'Morden Makerspace Open House', time: '6:00 PM – 8:00 PM · 30 Stephen St, Morden', link: 'https://morden.ca/events/morden-makerspace-open-house' });
      if (month === 7 && d === 13) add(fmt(year, month, d), { category: 'community', title: 'Waffle Breakfast', time: 'Morning · Altona Senior Centre', link: 'https://pembinavalleyonline.com/events' });
      if (month === 7 && d === 13) add(fmt(year, month, d), { category: 'family', title: 'Popsicle Stick Creations', time: '10:30 AM & 1:30 PM · Winkler Library', link: 'https://pembinavalleyonline.com/events/229004' });
      if (month === 7 && d >= 13 && d <= 17) add(fmt(year, month, d), { category: 'sports', title: 'Western Canadian Softball Championships', time: 'Aug 13-17 · Winkler & Morden', link: 'https://pembinavalleyonline.com/articles/u15-central-energy-softball-team-ready-to-welcome-western-canada-to-winkler' });
      if (month === 7 && d === 18) add(fmt(year, month, d), { category: 'community', title: 'Summer Shores Paint & Sip', time: '6:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
      if (month === 8 && d === 18) add(fmt(year, month, d), { category: 'community', title: 'Chamber Member Appreciation BBQ', time: 'Winkler City Hall · 185 Main St', link: 'https://winklerchamber.com/events/' });
      if (month === 7 && d === 7) add(fmt(year, month, d), { category: 'community', title: 'Municipal Forum', time: 'P.W. Enns Centennial Concert Hall', link: 'https://www.winkler.ca/events' });
      if (month === 7 && d === 10) add(fmt(year, month, d), { category: 'family', title: 'Mosaic Tray Workshop', time: '7:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
      if (month === 7 && d === 10) add(fmt(year, month, d), { category: 'family', title: 'Jr. Summer Art Camp (5-8)', time: '9:30 AM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
      if (month === 7 && d === 10) add(fmt(year, month, d), { category: 'family', title: 'Summer Art Camp (9-12)', time: '1:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
      if (month === 7 && d >= 28 && d <= 30) add(fmt(year, month, d), { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Downtown Morden · Free', link: 'https://cornandapple.com/' });
      if (month === 7 && d === 29) add(fmt(year, month, d), { category: 'community', title: 'Morden Back40 Music Festival', time: 'Morden, MB', link: 'https://www.backfortymusicfestival.com/' });
      if (month === 7 && d === 24) add(fmt(year, month, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', link: 'https://morden.ca/community-events' });
      if (month === 7 && d === 17) add(fmt(year, month, d), { category: 'community', title: 'MCC Blanket Making', time: '9:00 AM · Morden Mennonite Church', link: 'https://morden.ca/community-events' });
      if (month === 7 && d === 19) add(fmt(year, month, d), { category: 'family', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta', link: 'https://morden.ca/access-event-centre' });
      if (month === 7 && d === 27) add(fmt(year, month, d), { category: 'family', title: 'Rise & Shine FREE Morning Camp VBS', time: '9:30 AM · Thiessen Residence, 45 Falcon Drive, Morden', link: 'https://pembinavalleyonline.com/events' });
      if (month === 7 && d === 27) add(fmt(year, month, d), { category: 'community', title: 'Pickleball', time: '1:00 PM · Morden Activity Centre, 306 N. Railway St.', link: 'https://morden.ca/community-events' });
      if (month === 7 && d === 27) add(fmt(year, month, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });
      if (month === 7 && d === 27) add(fmt(year, month, d), { category: 'family', title: 'Annual BBQ — Winkler Senior Centre', time: '5:00 PM · 650 Southview Drive', link: 'https://winklerchamber.com/events/' });
      if (month === 7 && d === 6) add(fmt(year, month, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });
      if (month === 7 && d === 8) add(fmt(year, month, d), { category: 'fundraiser', title: 'Fundraising BBQ', time: '11:30 AM · Faith Mission, Winkler', link: 'https://winklerchamber.com/events/' });
      if (month === 8 && d === 9) add(fmt(year, month, d), { category: 'family', title: 'Prairie Dale First Day Grades K-9', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
      if (month === 8 && d === 10) add(fmt(year, month, d), { category: 'family', title: 'Prairie Dale First Day Grades 10-12', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
    }

    items.sort((a, b) => a.dateStr.localeCompare(b.dateStr) || a.ev.time.localeCompare(b.ev.time));

    items.forEach(({ dateStr, ev }) => {
      const evDate = new Date(dateStr + 'T12:00:00');

      const section = document.createElement('div');
      section.className = 'day-section';
      const dateLabel = document.createElement('div');
      dateLabel.className = 'date-label';
      dateLabel.textContent = days[evDate.getDay()] + ', ' + monthNames[evDate.getMonth()].slice(0,3) + ' ' + evDate.getDate();
      section.appendChild(dateLabel);

      const list = document.createElement('div');
      list.className = 'event-list';
      const item = document.createElement('div');
      item.className = 'day-event bubble';
      item.dataset.category = ev.category;
      const copyText = (ev.title + '
' + ev.time).trim();
      item.innerHTML = '<a class="event-link" href="' + ev.link + '" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;"><span class="title">' + ev.title + '</span></a><span class="time">' + ev.time + '</span><button class="copy-btn" data-copy="' + copyText.replace(/"/g, '&quot;') + '">Copy</button>';
      list.appendChild(item);
      section.appendChild(list);
      body.appendChild(section);
    });

    if (!items.length) {
      body.innerHTML = '<div class="muted" style="padding:10px;">No upcoming events in the next 7 days.</div>';
    }
  }


  function buildActivityWeek() {
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

        if (actualMonth === 7 && d === 4) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Catie St. Germain and Brothers Keep', time: '7:00 PM · Concert Hall', link: 'https://www.visitwinkler.ca' });
        if (actualMonth === 7 && d === 10) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Mosaic Tray Workshop', time: '7:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
        if (actualMonth === 7 && d === 10) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Jr. Summer Art Camp (5-8)', time: '9:30 AM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
        if (actualMonth === 7 && d === 10) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Summer Art Camp (9-12)', time: '1:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
        if (actualMonth === 7 && d === 11) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Finger Painting Workshop', time: '10:30 AM & 1:30 PM · Winkler Library', link: 'https://pembinavalleyonline.com/events/229002' });
        if (actualMonth === 7 && d === 13) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Morden Makerspace Open House', time: '6:00 PM – 8:00 PM · 30 Stephen St, Morden', link: 'https://morden.ca/events/morden-makerspace-open-house' });
        if (actualMonth === 7 && d === 13) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Waffle Breakfast', time: 'Morning · Altona Senior Centre', link: 'https://pembinavalleyonline.com/events' });
        if (actualMonth === 7 && d === 13) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Popsicle Stick Creations', time: '10:30 AM & 1:30 PM · Winkler Library', link: 'https://pembinavalleyonline.com/events/229004' });
        if (actualMonth === 7 && d >= 13 && d <= 17) add(fmt(yearForMonth, actualMonth, d), { category: 'sports', title: 'Western Canadian Softball Championships', time: 'Aug 13-17 · Winkler & Morden', link: 'https://pembinavalleyonline.com/articles/u15-central-energy-softball-team-ready-to-welcome-western-canada-to-winkler' });
        if (actualMonth === 7 && d >= 28 && d <= 30) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Downtown Morden · Free', link: 'https://cornandapple.com/' });
        if (actualMonth === 7 && d === 29) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Morden Back40 Music Festival', time: 'Morden, MB', link: 'https://www.backfortymusicfestival.com/' });
        if (actualMonth === 7 && d === 24) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', link: 'https://morden.ca/community-events' });
        if (actualMonth === 7 && d === 17) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'MCC Blanket Making', time: '9:30 AM · Morden Mennonite Church', link: 'https://morden.ca/community-events' });
        if (actualMonth === 7 && d === 19) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta', link: 'https://morden.ca/access-event-centre' });
        if (actualMonth === 7 && d === 27) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Rise & Shine FREE Morning Camp VBS', time: '9:30 AM · Thiessen Residence, 45 Falcon Drive, Morden', link: 'https://pembinavalleyonline.com/events' });
        if (actualMonth === 7 && d === 27) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Pickleball', time: '1:00 PM · Morden Activity Centre, 306 N. Railway St.', link: 'https://morden.ca/community-events' });
        if (actualMonth === 7 && d === 27) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });
        if (actualMonth === 7 && d === 27) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Annual BBQ — Winkler Senior Centre', time: '5:00 PM · 650 Southview Drive', link: 'https://winklerchamber.com/events/' });
        if (actualMonth === 7 && d === 6) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });
        if (actualMonth === 7 && d === 8) add(fmt(yearForMonth, actualMonth, d), { category: 'fundraiser', title: 'Fundraising BBQ', time: '11:30 AM · Faith Mission, Winkler', link: 'https://winklerchamber.com/events/' });
        if (actualMonth === 8 && d === 9) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Prairie Dale First Day Grades K-9', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
        if (actualMonth === 8 && d === 10) add(fmt(yearForMonth, actualMonth, d), { category: 'family', title: 'Prairie Dale First Day Grades 10-12', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
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

    sortedDates.forEach(dateStr => {
      const evDate = new Date(dateStr + 'T12:00:00');

      if (!eventsByDate[dateStr] || !eventsByDate[dateStr].length) return;

      const section = document.createElement('div');
      section.className = 'day-section';
      const dateLabel = document.createElement('div');
      dateLabel.className = 'date-label';
      dateLabel.textContent = days[evDate.getDay()] + ', ' + monthNames[evDate.getMonth()].slice(0,3) + ' ' + evDate.getDate();
      section.appendChild(dateLabel);

      const list = document.createElement('div');
      list.className = 'event-list';
      eventsByDate[dateStr].forEach(ev => {
        const item = document.createElement('div');
        item.className = 'day-event bubble';
        item.dataset.category = ev.category;
        item.innerHTML = '<a class="event-link" href="' + ev.link + '" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;"><span class="title" style="font-weight:600">' + ev.title + '</span></a><span class="time" style="color:#6b7280; font-size:0.85rem">' + ev.time + '</span><span style="font-size:0.8rem;color:#8ab4f8;"> · <a href="#page-activities" style="color:#8ab4f8;">View calendar</a></span>';
        list.appendChild(item);
      });
      section.appendChild(list);
      body.appendChild(section);
    });
  }

  
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
    
    // Specific date events
    if (month === 7 && now.getDate() === 4) add("Catie St. Germain and Brothers Keep", "7:00 PM · Concert Hall", "community", "https://www.visitwinkler.ca");
    if (month === 7 && now.getDate() === 6) add("Morden Farmers Market", "4:00 PM · 8th Street", "community", "https://morden.ca/community-events");
    if (month === 8 && now.getDate() >= 1 && now.getDate() <= 7) add("Labour Day - No School", "Prairie Dale School", "family", "https://pds.gvsd.ca/");
    if (month === 7 && now.getDate() === 8) add("Prairie Dale No Classes Admin Day", "Prairie Dale School", "family", "https://pds.gvsd.ca/");
    if (month === 8 && now.getDate() === 9) add("Prairie Dale First Day Grades K-9", "Prairie Dale School", "family", "https://pds.gvsd.ca/");
    if (month === 8 && now.getDate() === 10) add("Prairie Dale First Day Grades 10-12", "Prairie Dale School", "family", "https://pds.gvsd.ca/");
    if (month === 7 && now.getDate() === 17) add("MCC Blanket Making", "9:30 AM · Morden Mennonite Church", "community", "https://morden.ca/community-events");
    if (month === 7 && now.getDate() === 18) add("Summer Shores Paint & Sip", "6:00 PM · Winkler Arts & Culture", "community", "https://www.visitwinkler.ca");
    if (month === 7 && now.getDate() === 19) add("The Big Canoe", "9:00 AM · Lake Minnewasta", "community", "https://morden.ca/access-event-centre");
    if (month === 7 && now.getDate() === 24) add("Morden Council Meeting", "7:00 PM · 500 Stephen St", "community", "https://morden.ca/community-events");
    if (month === 7 && now.getDate() === 25) add("Morden Farmers Market", "4:00 PM · 8th Street", "community", "https://morden.ca/community-events");
    if (month === 7 && now.getDate() === 27) add("Rise & Shine FREE Morning Camp VBS", "9:30 AM · Thiessen Residence, 45 Falcon Drive, Morden", "family", "https://pembinavalleyonline.com/events");
    if (month === 7 && now.getDate() === 27) add("Pickleball", "1:00 PM · Morden Activity Centre, 306 N. Railway St.", "community", "https://morden.ca/community-events");
    if (month === 7 && now.getDate() === 27) add("Morden Farmers Market", "4:00 PM · 8th Street", "community", "https://morden.ca/community-events");
    if (month === 7 && now.getDate() === 27) add("Annual BBQ — Winkler Senior Centre", "5:00 PM · 650 Southview Drive", "family", "https://winklerchamber.com/events/");
    if (month === 7 && now.getDate() === 29) add("Morden Back40 Music Festival", "Morden, MB", "community", "https://www.backfortymusicfestival.com/");

    

    // Sort by time
    events.sort((a, b) => a.time.localeCompare(b.time));
    
    if (events.length === 0) {
      container.innerHTML = '<p class="muted">No events scheduled for today.</p>';
      return;
    }
    
    events.sort((a, b) => a.time.localeCompare(b.time));
    events.forEach(ev => {
      const el = document.createElement('a');
      el.className = 'day-event bubble';
      el.href = ev.link || '#';
      el.target = '_blank';
      el.rel = 'noopener';
      el.dataset.category = ev.category;
      el.innerHTML = `<span class="title">${ev.title}</span><span class="time">· ${ev.time}</span><div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, '&quot;')}" data-time="${ev.time.replace(/"/g, '&quot;')}" data-date="${dateStr}">📅 Add to Calendar</button></div><span style="font-size:0.8rem;color:#8ab4f8;"> · <a href="#page-activities" style="color:#8ab4f8;">View calendar</a></span>`;
      container.appendChild(el);
    });
  }

function buildMonth() {
    const wrap = document.getElementById('month-wrap');
    if (!wrap) return;
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth();
    const today = now.getDate();
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];

    const eventsByDate = {};
    const add = (dateStr, ev) => {
      const parts = dateStr.split('-');
      const evDate = new Date(+parts[0], +parts[1] - 1, +parts[2]);
      const todayDate = new Date(year, month, today);
      if (evDate < todayDate) return;
      if (!eventsByDate[dateStr]) eventsByDate[dateStr] = [];
      eventsByDate[dateStr].push(ev);
    };

    const fmt = (y, m, d) => `${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;

    for (let d = 1; d <= daysInMonth; d++) {
      const date = new Date(year, month, d);
      const dow = date.getDay();
      const dateStr = fmt(year, month, d);
      if (dow === 2) add(dateStr, { category: 'community', title: "Winkler Farmer's Market", time: 'Tue 4-6 PM · Central Station parking lot', link: 'https://www.pembinavalleyonline.com/events' });
      if (month === 7 && dow === 3) add(dateStr, { category: 'community', title: 'Concerts in the Park', time: 'Wed 7:00 PM · Bethel Heritage Park', link: 'https://www.visitwinkler.ca/concerts-in-the-park' });
      if (month === 6 && d === 6) add(dateStr, { category: 'community', title: 'Paper Chain Creations', time: '10:30 AM & 1:30 PM · Winkler Library', link: 'https://www.winklerlibrary.ca' });
      if (month === 6 && d === 5) add(dateStr, { category: 'community', title: 'Summer Storytime', time: '10:30 AM & 1:30 PM · Winkler Library', link: 'https://www.winklerlibrary.ca' });
      if (month === 7 && d === 4) add(dateStr, { category: 'community', title: 'Catie St. Germain and Brothers Keep', time: '7:00 PM · Concert Hall', link: 'https://www.visitwinkler.ca' });
      if (month === 7 && d === 18) add(dateStr, { category: 'community', title: 'Summer Shores Paint & Sip', time: '6:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
      if (month === 8 && d === 18) add(dateStr, { category: 'community', title: 'Chamber Member Appreciation BBQ', time: 'Winkler City Hall · 185 Main St', link: 'https://winklerchamber.com/events/' });
      if (month === 8 && d === 7) add(dateStr, { category: 'community', title: 'Municipal Forum', time: 'P.W. Enns Centennial Concert Hall', link: 'https://www.winkler.ca/events' });
      if (month === 7 && d === 10) add(dateStr, { category: 'family', title: 'Mosaic Tray Workshop', time: '7:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
      if (month === 7 && d === 10) add(dateStr, { category: 'family', title: 'Jr. Summer Art Camp (5-8)', time: '9:30 AM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
      if (month === 7 && d === 10) add(dateStr, { category: 'family', title: 'Summer Art Camp (9-12)', time: '1:00 PM · Winkler Arts & Culture', link: 'https://www.visitwinkler.ca' });
      if (month === 7 && d >= 28 && d <= 30) add(dateStr, { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Downtown Morden · Free', link: 'https://cornandapple.com/' });
      if (month === 7 && d === 29) add(dateStr, { category: 'community', title: 'Morden Back40 Music Festival', time: 'Morden, MB', link: 'https://www.backfortymusicfestival.com/' });
      if (month === 7 && d === 24) add(dateStr, { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', link: 'https://morden.ca/community-events' });
      if (month === 7 && d === 17) add(dateStr, { category: 'community', title: 'MCC Blanket Making', time: '9:30 AM · Morden Mennonite Church', link: 'https://morden.ca/community-events' });
      if (month === 7 && d === 19) add(dateStr, { category: 'community', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta', link: 'https://morden.ca/access-event-centre' });
      if (month === 7 && d === 27) add(dateStr, { category: 'family', title: 'Rise & Shine FREE Morning Camp VBS', time: '9:30 AM · Thiessen Residence, 45 Falcon Drive, Morden', link: 'https://pembinavalleyonline.com/events' });
      if (month === 7 && d === 27) add(dateStr, { category: 'community', title: 'Pickleball', time: '1:00 PM · Morden Activity Centre, 306 N. Railway St.', link: 'https://morden.ca/community-events' });
      if (month === 7 && d === 27) add(dateStr, { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });
      if (month === 7 && d === 27) add(dateStr, { category: 'family', title: 'Annual BBQ — Winkler Senior Centre', time: '5:00 PM · 650 Southview Drive', link: 'https://winklerchamber.com/events/' });
      if (month === 7 && d === 6) add(dateStr, { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });
      if (month === 7 && d === 8) add(dateStr, { category: 'fundraiser', title: 'Fundraising BBQ', time: '11:30 AM · Faith Mission, Winkler', link: 'https://winklerchamber.com/events/' });
      if (month === 7 && d === 18) add(dateStr, { category: 'family', title: 'Winkler EMMC Church Council Mtg', time: '7:00 PM · 600 Southview Drive', link: 'http://www.winkleremmc.com/events/' });
      if (month === 7 && d === 7) add(dateStr, { category: 'family', title: 'Labour Day - No School', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
      if (month === 7 && d === 8) add(dateStr, { category: 'family', title: 'Prairie Dale No Classes Admin Day', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
      if (month === 8 && d === 9) add(dateStr, { category: 'family', title: 'Prairie Dale First Day Grades K-9', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
      if (month === 8 && d === 10) add(dateStr, { category: 'family', title: 'Prairie Dale First Day Grades 10-12', time: 'Prairie Dale School · pds.gvsd.ca', link: 'https://pds.gvsd.ca/' });
    }

    const grid = document.createElement('div');
    grid.className = 'month-grid';

    const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    const title = document.createElement('div');
    title.style.gridColumn = '1 / -1';
    title.style.fontWeight = '900';
    title.style.fontSize = '1.1rem';
    title.style.marginBottom = '10px';
    title.textContent = monthNames[month] + ' ' + year;
    grid.appendChild(title);

    for (let d = 1; d <= daysInMonth; d++) {
      const dateStr = fmt(year, month, d);
      const dayEvents = eventsByDate[dateStr] || [];
      if (!dayEvents.length) continue;

      const dateLabel = document.createElement('div');
      dateLabel.style.gridColumn = '1 / -1';
      dateLabel.style.fontWeight = '800';
      dateLabel.style.marginTop = '12px';
      dateLabel.textContent = monthNames[month] + ' ' + d;
      grid.appendChild(dateLabel);

      dayEvents.forEach(ev => {
        const bubble = document.createElement('a');
        bubble.className = 'day-event bubble';
        bubble.href = ev.link || '#';
        bubble.target = '_blank';
        bubble.rel = 'noopener';
        bubble.dataset.category = ev.category;
        const copyText = (ev.title + '
' + ev.time).trim();
        bubble.innerHTML = `<span class="title">${ev.title}</span><span class="time">${ev.time}</span><div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/\"/g, '&quot;')}" data-time="${ev.time.replace(/\"/g, '&quot;')}" data-date="${dateStr}">📅 Add to Calendar</button></div><button class="copy-btn" data-copy="${copyText.replace(/\"/g, '&quot;')}">Copy</button>`;
        grid.appendChild(bubble);
      });
    }

    wrap.innerHTML = '';
    wrap.appendChild(grid);
  }

  function activatePage(page) {
    try {
      document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.nav-link').forEach(n => n.classList.remove('active'));
      const el = document.getElementById('page-' + page);
      if (el) el.classList.add('active');
      document.querySelectorAll('.nav-link').forEach(l => {
        if (l.dataset.page === page) l.classList.add('active');
      });
      if (page === 'home') { try { renderFeatured(); } catch (e) { console.error(e); } }
      if (page === 'calendar') { try { buildUpcoming(); } catch (e) { console.error(e); } }
      try { buildToday(); } catch (e) { console.error(e); }
      if (page === 'activities') { try { buildActivityWeek(); } catch (e) { console.error(e); } }
      if (page === 'family') { try { renderFamilyEvents(); } catch (e) { console.error(e); } }
      if (page === 'weather') { try { loadWeather(); } catch (e) { console.error(e); } }
    } catch (e) {
      console.error('activatePage error', e);
      document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
      const home = document.getElementById('page-home');
      if (home) home.classList.add('active');
    }
  }

  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      activatePage(link.dataset.page);
    });
  });

  const initPage = () => {
    try {
      const page = (location.hash || '#home').replace('#page-', '').replace('#', '') || 'home';
      activatePage(page);
    } catch (e) {
      console.error('initPage error', e);
      const el = document.getElementById('page-home');
      if (el) el.classList.add('active');
    }
  };
  window.addEventListener('hashchange', initPage);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPage);
  } else {
    initPage();
  }

  async function loadWeather() {
    try {
      const lat = 49.1833;
      const lon = -97.9339;
      const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America%2FWinnipeg`;
      const res = await fetch(url);
      const data = await res.json();
      const cw = data.current_weather;
      const tempEls = document.querySelectorAll('#temp, #temp2, #heroTemp');
      const condEls = document.querySelectorAll('#condition, #condition2, #heroCondition');
      const locEls = document.querySelectorAll('#location, #location2, #heroLocation');
      const updEls = document.querySelectorAll('#updated, #updated2');
      tempEls.forEach(el => el.textContent = Math.round(cw.temperature) + '°');
      condEls.forEach(el => el.textContent = weatherLabel(cw.weathercode) + ' · Wind: ' + cw.windspeed + ' km/h');
      locEls.forEach(el => el.textContent = 'Pembina, MB');
      updEls.forEach(el => el.textContent = 'Updated: ' + new Date().toLocaleTimeString());
      updateActivities(cw.temperature, cw.windspeed, cw.weathercode);
      updateWeatherPlan(cw.temperature, cw.weathercode);
      if (data.daily) renderWeekly(data.daily);
      setWeatherVideo(cw.weathercode, cw.temperature);
    } catch (e) {
      console.warn('Weather load failed:', e);
      const tempEl = document.getElementById('temp');
      const condEl = document.getElementById('condition');
      const locEl = document.getElementById('location');
      const temp2El = document.getElementById('temp2');
      const cond2El = document.getElementById('condition2');
      const loc2El = document.getElementById('location2');
      const heroTemp = document.getElementById('heroTemp');
      const heroCond = document.getElementById('heroCondition');
      const heroLoc = document.getElementById('heroLocation');
      if (tempEl) tempEl.textContent = '--°';
      if (condEl) condEl.textContent = 'Weather unavailable';
      if (locEl) locEl.textContent = 'Pembina, MB';
      if (temp2El) temp2El.textContent = '--°';
      if (cond2El) cond2El.textContent = 'Weather unavailable';
      if (loc2El) loc2El.textContent = 'Pembina, MB';
      if (heroTemp) heroTemp.textContent = '--°';
      if (heroCond) heroCond.textContent = 'Weather unavailable';
      if (heroLoc) heroLoc.textContent = 'Pembina, MB';
      updateActivities(15, 10, 3);
      updateWeatherPlan(15, 3);
    }
  }

  function weatherLabel(code) {
    if (code === 0) return 'Clear sky';
    if (code <= 3) return 'Partly cloudy';
    if (code <= 48) return 'Foggy';
    if (code <= 67) return 'Rain';
    if (code <= 77) return 'Snow';
    if (code <= 82) return 'Rain showers';
    if (code <= 86) return 'Snow showers';
    if (code <= 99) return 'Thunderstorm';
    return 'Weather';
  }

  function setWeatherVideo(code, temp) {
    const video = document.getElementById('heroWeatherVideo');
    if (!video) return;
    const hour = new Date().getHours();
    const isPrecip = code >= 51 && code <= 99;
    const isClear = code <= 3;
    let src = 'weather-media/day.mp4';
    if (isPrecip) {
      src = 'weather-media/rain.mp4';
    } else if (isClear && (hour < 6 || hour >= 20)) {
      src = 'weather-media/night.mp4';
    } else if (!isClear && (hour < 6 || hour >= 20)) {
      src = 'weather-media/night.mp4';
    }
    if (video.src && video.src.endsWith(src)) return;
    video.style.transition = 'opacity 0.6s ease';
    video.style.opacity = '0';
    setTimeout(() => {
      video.src = src;
      video.play().catch(() => {});
      video.style.opacity = '1';
    }, 600);
  }

  function weatherIconHTML(code) {
    if (code === 0) {
      return '<div class="wi wi-clear"></div>';
    } else if (code <= 3) {
      return '<div class="wi wi-partly-cloudy"></div>';
    } else if (code <= 67) {
      return '<div class="wi wi-rain"></div>';
    } else {
      return '<div class="wi wi-snow"></div>';
    }
  }

  function drawWeatherIcon(wrapId, code) {
    const wrap = document.getElementById(wrapId);
    if (!wrap) return;
    const scene = document.getElementById('weatherScene');
    if (!scene) return;
    scene.setAttribute('style', 'position:relative;width:100%;height:100%;border-radius:24px;overflow:hidden;background:radial-gradient(ellipse at 30% 20%, rgba(245,158,11,0.35) 0%, transparent 55%), radial-gradient(ellipse at 80% 30%, rgba(148,163,184,0.35) 0%, transparent 55%), linear-gradient(160deg, #0b1020 0%, #0f172a 45%, #1e293b 100%);animation:weatherSceneShift 14s ease-in-out infinite;perspective:800px;');
    const icon = document.createElement('div');
    icon.setAttribute('style', 'position:relative;width:100%;height:100%;transform-style:preserve-3d;');
    if (code === 0) {
      const sun = document.createElement('div');
      sun.className = 'sun';
      sun.setAttribute('style', 'position:absolute;top:18px;left:22px;width:54px;height:54px;border-radius:50%;background:radial-gradient(circle at 30% 30%, #fff7d6, #f59e0b);box-shadow:0 0 28px rgba(245,158,11,0.55), 0 0 70px rgba(245,158,11,0.25);animation:sunPulse 2.4s ease-in-out infinite;transform:translateZ(20px);');
      const ray = document.createElement('div');
      ray.className = 'sun-ray';
      ray.setAttribute('style', 'position:absolute;top:18px;left:22px;width:54px;height:54px;border-radius:50%;border:3px solid rgba(251,191,36,0.55);animation:sunPulse 2.4s ease-in-out infinite;transform:translateZ(10px);');
      icon.appendChild(sun);
      icon.appendChild(ray);
    } else if (code <= 3) {
      const sun = document.createElement('div');
      sun.className = 'sun';
      sun.setAttribute('style', 'position:absolute;top:18px;left:22px;width:54px;height:54px;border-radius:50%;background:radial-gradient(circle at 30% 30%, #fff7d6, #f59e0b);box-shadow:0 0 28px rgba(245,158,11,0.55), 0 0 70px rgba(245,158,11,0.25);animation:sunPulse 2.4s ease-in-out infinite;transform:translateZ(20px);');
      const ray = document.createElement('div');
      ray.className = 'sun-ray';
      ray.setAttribute('style', 'position:absolute;top:18px;left:22px;width:54px;height:54px;border-radius:50%;border:3px solid rgba(251,191,36,0.55);animation:sunPulse 2.4s ease-in-out infinite;transform:translateZ(10px);');
      const cloud = document.createElement('div');
      cloud.className = 'cloud';
      cloud.setAttribute('style', 'position:absolute;bottom:26px;right:18px;width:78px;height:32px;background:rgba(226,232,240,0.92);border-radius:999px;box-shadow:0 18px 30px rgba(15,23,42,0.45);animation:cloudDrift 5.5s ease-in-out infinite;transform:translateZ(12px);');
      icon.appendChild(sun);
      icon.appendChild(ray);
      icon.appendChild(cloud);
    } else if (code <= 67) {
      const cloud = document.createElement('div');
      cloud.className = 'cloud';
      cloud.setAttribute('style', 'position:absolute;bottom:26px;right:18px;width:78px;height:32px;background:rgba(226,232,240,0.92);border-radius:999px;box-shadow:0 18px 30px rgba(15,23,42,0.45);animation:cloudDrift 5.5s ease-in-out infinite;transform:translateZ(12px);');
      icon.appendChild(cloud);
      const rain = document.createElement('div');
      rain.className = 'rain';
      rain.setAttribute('style', 'position:absolute;top:10px;left:18px;width:90px;height:80px;');
      for (let i = 0; i < 8; i++) {
        const drop = document.createElement('div');
        drop.className = 'rain-drop';
        drop.setAttribute('style', 'position:absolute;width:3px;height:10px;border-radius:999px;background:linear-gradient(180deg, rgba(125,211,252,0.9), rgba(37,99,235,0.7));left:' + (10 + i * 9) + 'px;animation:rainFall 1.1s linear infinite;animation-delay:' + (i * 0.18) + 's;');
        rain.appendChild(drop);
      }
      icon.appendChild(rain);
    } else {
      const cloud = document.createElement('div');
      cloud.className = 'cloud';
      cloud.setAttribute('style', 'position:absolute;bottom:26px;right:18px;width:78px;height:32px;background:rgba(226,232,240,0.92);border-radius:999px;box-shadow:0 18px 30px rgba(15,23,42,0.45);animation:cloudDrift 5.5s ease-in-out infinite;transform:translateZ(12px);');
      icon.appendChild(cloud);
      const snow = document.createElement('div');
      snow.className = 'snow';
      snow.setAttribute('style', 'position:absolute;top:10px;left:18px;width:90px;height:80px;');
      const flakes = ['❄', '❅', '❆'];
      for (let i = 0; i < 6; i++) {
        const flake = document.createElement('div');
        flake.className = 'snowflake';
        flake.setAttribute('style', 'position:absolute;color:#e2e8f0;font-size:12px;left:' + (14 + i * 11) + 'px;animation:snowFall 2.4s linear infinite;animation-delay:' + (i * 0.35) + 's;');
        flake.textContent = flakes[i % flakes.length];
        snow.appendChild(flake);
      }
      icon.appendChild(snow);
    }
    scene.innerHTML = '';
    scene.appendChild(icon);
  }

  function updateActivities(temp, wind, code) {
    const box = document.getElementById('activities');
    if (!box) return;

    const outdoor = [];
    const indoor = [];

    if (temp >= 22 && wind < 25) outdoor.push({ name: 'Outdoor sports', desc: 'Warm and calm — good for a walk, run, or family outing.' });
    else if (temp >= 10 && wind < 30) outdoor.push({ name: 'Park visit', desc: 'Mild weather — pack a light jacket and enjoy outside.' });
    else outdoor.push({ name: 'Quick walk', desc: 'Cool or breezy — short outdoor movement still works.' });

    if (code >= 51 && code <= 99) indoor.push({ name: 'Indoor focus', desc: 'Rain or storm likely — study, prep lessons, or organize files.' });
    else if (temp < 10 || wind > 35) indoor.push({ name: 'Indoor focus', desc: 'Cold or windy — good for study, baking, or building.' });
    else indoor.push({ name: 'Backup indoor plan', desc: 'Keep a cozy indoor option ready if weather changes.' });

    if (temp >= 18 && code < 50) outdoor.push({ name: 'Outdoor meal', desc: 'Temperature holds — eat outside if you can.' });
    if (wind > 35) outdoor.push({ name: 'Secure outdoor items', desc: 'Strong winds expected — move or tie down loose objects.' });

    const isGoodWeather = code < 51 && temp >= 10 && wind <= 35;
    const primary = isGoodWeather ? outdoor[0] : indoor[0];
    const secondary = isGoodWeather ? indoor[0] : outdoor[0];

    box.innerHTML = `
      <div class="activity highlighted">
        <div class="name">${primary.name}</div>
        <div class="desc">${primary.desc}</div>
      </div>
      ${secondary ? `
      <div class="activity">
        <div class="name">${secondary.name}</div>
        <div class="desc">${secondary.desc}</div>
      </div>
      ` : ''}
    `;
  }

  function updateWeatherPlan(temp, code) {
    const box = document.getElementById('weatherPlan');
    if (!box) return;
    const items = [];
    if (code === 0 && temp >= 20) items.push({ name: 'Morning garden or walk', desc: 'Clear and warm — start outside while it’s fresh.' });
    else if (code <= 3) items.push({ name: 'Flexible plan', desc: 'Clouds but usable — keep outdoor options open.' });
    else if (code <= 67) items.push({ name: 'Indoor focus', desc: 'Rain likely — study, prep lessons, or organize files.' });
    else items.push({ name: 'Indoor focus', desc: 'Keep warm and use the time for focused work.' });
    if (temp >= 18 && code < 50) items.push({ name: 'Sunset break', desc: 'Temperature holds — step out for fresh air in the evening.' });
    box.innerHTML = items.map(i => `<div class="activity"><div class="name">${i.name}</div><div class="desc">${i.desc}</div></div>`).join('');
  }

  function renderWeekly(daily) {
    const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const targets = [document.getElementById('weekly-home')].filter(Boolean);
    if (!targets.length) return;
    if (!daily || !daily.time || !daily.time.length) {
      targets.forEach(el => el.innerHTML = '<div class="muted">Weekly forecast unavailable</div>');
      return;
    }

    const count = Math.min(7, daily.time.length);
    targets.forEach(el => {
      el.innerHTML = '';
      el.setAttribute('style', 'display:block !important;grid:none !important;width:100% !important;max-width:100% !important;overflow:visible !important;');
      const wrap = document.createElement('div');
      wrap.setAttribute('style', 'display:block !important;width:100% !important;max-width:100% !important;overflow-x:auto !important;overflow-y:hidden !important;padding-bottom:8px !important;');
      const row = document.createElement('div');
      row.className = 'forecast-row-inline';
      row.setAttribute('style', 'display:flex !important;flex-wrap:nowrap !important;gap:10px;overflow-x:auto;padding-bottom:8px;scroll-snap-type:x mandatory;width:100% !important;max-width:none !important;');
      wrap.appendChild(row);
      el.appendChild(wrap);

      for (let i = 0; i < count; i++) {
        const date = new Date(daily.time[i] + 'T00:00:00');
        const dayName = days[date.getDay()];
        const monthName = months[date.getMonth()];
        const dayNum = date.getDate();
        const maxT = daily.temperature_2m_max ? Math.round(daily.temperature_2m_max[i]) : '--';
        const minT = daily.temperature_2m_min ? Math.round(daily.temperature_2m_min[i]) : '--';
        const precip = daily.precipitation_sum ? daily.precipitation_sum[i].toFixed(1) : null;
        const precipText = precip === null ? '0.0' : precip;
        const condition = weatherLabel(daily.weathercode[i]);
        const isRain = daily.weathercode[i] && daily.weathercode[i] <= 67;
        const barWidth = Math.min(100, Math.max(20, (maxT - minT) * 12));

        const card = document.createElement('div');
        card.className = 'forecast-card-inline';
        card.setAttribute('data-weather-code', daily.weathercode[i]);
        card.setAttribute('style', 'flex:0 0 auto !important;min-width:120px !important;width:120px !important;background:rgba(255,255,255,0.06) !important;border-radius:20px !important;padding:14px 10px 12px !important;text-align:left !important;color:#e2e8f0 !important;display:flex !important;flex-direction:column !important;gap:6px !important;box-shadow:inset 0 0 0 1px rgba(255,255,255,0.08) !important;transition:transform 0.2s ease !important;border:2px solid rgba(34,211,238,0.4) !important;');

        const dayEl = document.createElement('div');
        dayEl.textContent = dayName;
        dayEl.setAttribute('style', 'font-size:0.75rem;font-weight:800;color:#cbd5e1;letter-spacing:0.08em;text-transform:uppercase;');

        const dateEl = document.createElement('div');
        dateEl.textContent = monthName + ' ' + dayNum;
        dateEl.setAttribute('style', 'font-size:0.68rem;color:#94a3b8;');

        const tempsEl = document.createElement('div');
        tempsEl.textContent = maxT + '° / ' + minT + '°';
        tempsEl.setAttribute('style', 'font-size:0.9rem;font-weight:800;color:#f1f5f9;');

        const barWrap = document.createElement('div');
        barWrap.setAttribute('style', 'display:flex;align-items:center;gap:8px;');
        const bar = document.createElement('div');
        bar.setAttribute('style', 'height:6px;border-radius:999px;background:linear-gradient(90deg, #22d3ee, #f59e0b);opacity:0.9;width:' + barWidth + '%;');
        barWrap.appendChild(bar);

        const condEl = document.createElement('div');
        condEl.textContent = condition;
        condEl.setAttribute('style', 'font-size:0.72rem;color:#cbd5e1;line-height:1.3;');

        const precipEl = document.createElement('div');
        precipEl.textContent = precipText + '%';
        precipEl.setAttribute('style', 'font-size:0.68rem;color:#7dd3fc;');

        card.appendChild(dayEl);
        card.appendChild(dateEl);
        card.appendChild(tempsEl);
        card.appendChild(barWrap);
        card.appendChild(condEl);
        card.appendChild(precipEl);
        row.appendChild(card);
      }

      el.appendChild(row);
    });
  }

  renderDashboard();
  buildUpcoming();
  buildActivityWeek();
  buildMonth();
  renderFeatured();
  renderFamilyEvents();
  loadWeather();

  function renderFeatured() {
    const container = document.getElementById('featured-events');
    if (!container) return;
    const featured = [

      { category: 'family', title: 'Prairie Dale School Events', time: 'Aug-Sep · Pembina, MB', date: 'Aug', link: 'https://pds.gvsd.ca/' },
      { category: 'community', title: 'Chamber Member Appreciation BBQ', time: 'Sep 18 · Winkler City Hall', date: 'Sep 18', link: 'https://winklerchamber.com/events/' },
      { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Aug 28-30 · Downtown Morden', date: 'Aug 28', link: 'https://cornandapple.com/', promoted: true },
      { category: 'community', title: 'Honey Garlic & Maple Syrup Festival', time: 'Second weekend Sep · Manitou, MB', date: 'Sep', link: 'https://hgmsfestival.com/' },
      { category: 'community', title: 'Manitou Ag Fair', time: 'Manitou, MB', date: 'TBD', link: 'https://www.pembina.ca/p/annual-events' },
      { category: 'outdoors', title: 'Raptor Festival', time: 'Spring · La Riviere, MB', date: 'Spring', link: 'https://www.pembina.ca/p/annual-events' },
      { category: 'outdoors', title: 'Outdoor Summer Adventure', time: 'Pembina, MB', date: 'Summer', link: 'https://www.pembina.ca/p/annual-events' },
      { category: 'community', title: 'Morden Back40 Music Festival', time: 'Aug 29 · Morden, MB', date: 'Aug 29', link: 'https://www.backfortymusicfestival.com/' },
      { category: 'community', title: 'The Big Canoe', time: 'Sep 19 · Lake Minnewasta', date: 'Sep 19', link: 'https://morden.ca/access-event-centre' },
    ];

    container.innerHTML = featured.map(ev => `
      <a class="featured-card bubble" href="${ev.link || '#'}" target="_blank" rel="noopener" data-category="${ev.category}">
        <div class="row">
          <div class="badge-row">
            <span class="date-badge">${ev.date}</span>
            <span class="cat-badge">${ev.category}</span>
            ${ev.promoted ? '<span class="cat-badge" style="background:#f59e0b;color:#fff">Promoted</span>' : ''}
          </div>
        </div>
        <div class="title">${ev.title}</div>
        <div class="meta">${ev.time}</div>
        <button class="copy-btn" data-copy="${`${ev.title}
${ev.time}`.replace(/"/g, '&quot;')}">Copy</button>
      </a>
    `).join('');
  }

  function renderFamilyEvents() {
    const schoolBox = document.getElementById('family-school-events');
    const churchBox = document.getElementById('family-church-events');
    const garageBox = document.getElementById('family-garage-events');

    const schoolEvents = [
      { title: 'First Day Grades K-9', date: 'Sep 9 (Wed)', time: 'Prairie Dale School · Winkler', category: 'family', link: 'https://pds.gvsd.ca/' },
      { title: 'First Day Grades 10-12', date: 'Sep 10 (Thu)', time: 'Prairie Dale School · Winkler', category: 'family', link: 'https://pds.gvsd.ca/' },
      { title: 'Whimsical Wonders Art Camp', date: 'Aug 31-Sep 4', time: 'City of Morden · morden.ca', category: 'family', link: 'https://morden.ca/community-events' },
      { title: 'Altona Aquatic Centre', date: 'Summer 2026', time: 'Altona, MB · altona.ca', category: 'family', link: 'https://altona.ca/upcoming-events' }
    ];

    const churchEvents = [
    ];

    const garageEvents = [
      { title: 'Morden Community BBQ Fundraiser', date: 'Aug 8', time: '11:30 AM · Faith Mission, Winkler', category: 'fundraiser', link: 'https://winklerchamber.com/events/' },
      { title: 'Altona Aquatic Centre', date: 'Summer 2026', time: 'Altona, MB · Family fun', category: 'community', link: 'https://altona.ca/upcoming-events' }
    ];

    const renderCard = (ev) => {
      const link = ev.link || '#';
      return `
      <a class="day-event" href="${link}" target="_blank" rel="noopener" data-category="${ev.category || 'family'}">
        <div class="title">${ev.title}</div>
        <div class="time">${ev.date} · ${ev.time}</div>
        <div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, '&quot;')}" data-time="${ev.time.replace(/"/g, '&quot;')}" data-date="${ev.date}">📅 Add to Calendar</button></div>
        <button class="copy-btn" data-copy="${`${ev.title}
${ev.date} · ${ev.time}`.replace(/"/g, '&quot;')}">Copy</button>
      </a>
    `;
    };

    if (schoolBox) schoolBox.innerHTML = schoolEvents.map(renderCard).join('');
    if (churchBox) churchBox.innerHTML = churchEvents.map(renderCard).join('');
    if (garageBox) garageBox.innerHTML = garageEvents.map(renderCard).join('');
  }
  document.addEventListener('click', (ev) => {
    const btn = ev.target.closest('[data-export="ics"]');
    if (!btn) return;
    ev.preventDefault();
    addToCalendar(btn.dataset.title || '', btn.dataset.time || '', btn.dataset.date || '');
  });

  document.addEventListener('click', (ev) => {
    const copyBtn = ev.target.closest('.copy-btn');
    if (!copyBtn) return;
    ev.preventDefault();
    const text = copyBtn.dataset.copy || '';
    if (!navigator.clipboard || !navigator.clipboard.writeText) {
      alert(text);
      return;
    }
    navigator.clipboard.writeText(text).then(() => {
      const original = copyBtn.textContent;
      copyBtn.textContent = 'Copied';
      copyBtn.disabled = true;
      setTimeout(() => {
        copyBtn.textContent = original;
        copyBtn.disabled = false;
      }, 1200);
    }).catch(() => {
      alert(text);
    });
  });

  const eventForm = document.getElementById('event-form');
  if (eventForm) {
    eventForm.addEventListener('submit', (ev) => {
      ev.preventDefault();
      const title = document.getElementById('evt-title').value.trim();
      const date = document.getElementById('evt-date').value;
      const time = document.getElementById('evt-time').value.trim();
      const category = document.getElementById('evt-category').value;
      const link = document.getElementById('evt-link').value.trim();
      const desc = document.getElementById('evt-desc').value.trim();
      if (!title || !date) {
        alert('Please provide an event title and date.');
        return;
      }
      const subject = encodeURIComponent('Event Submission: ' + title);
      const body = encodeURIComponent(
        'Event Title: ' + title + '\\n' +
        'Date: ' + date + '\\n' +
        'Time: ' + (time || 'TBD') + '\\n' +
        'Category: ' + category + '\\n' +
        'Link: ' + (link || 'N/A') + '\\n' +
        'Description: ' + (desc || 'N/A') + '\\n\\nSubmitted from the Pembina Valley Events website.'
      );
      window.location.href = 'mailto:boomsecure@protonmail.com?subject=' + subject + '&body=' + body;
    });
  }
