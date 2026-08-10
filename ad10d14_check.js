
  function downloadICS(title, timeText, dateStr) {
    const dt = dateStr || new Date().toISOString().split('T')[0];
    const dtStart = dt.replace(/-/g, '') + 'T000000';
    const dtEnd = dt.replace(/-/g, '') + 'T235900';
    const cleanTitle = (title || '').replace(/[\n\r]/g, ' ').trim();
    const ics = [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//Pembina Valley Events//EN',
      'BEGIN:VEVENT',
      'UID:' + cleanTitle.toLowerCase().replace(/[^a-z0-9]+/g, '-') + '-' + dt + '@pembinaevents.ca',
      'DTSTAMP:' + new Date().toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z',
      'DTSTART;VALUE=DATE:' + dt.replace(/-/g, ''),
      'DTEND;VALUE=DATE:' + dt.replace(/-/g, ''),
      'SUMMARY:' + cleanTitle,
      'DESCRIPTION:' + (timeText || '').replace(/[\n\r]/g, ' '),
      'END:VEVENT',
      'END:VCALENDAR'
    ].join('\r\n');
    const blob = new Blob([ics], { type: 'text/calendar;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'pembina-event-' + dt + '.ics';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function addGoogleCalendarLink(title, timeText, dateStr) {
    const dt = dateStr || new Date().toISOString().split('T')[0];
    const cleanTitle = encodeURIComponent((title || '').replace(/[\n\r]/g, ' ').trim());
    const details = encodeURIComponent((timeText || '').replace(/[\n\r]/g, ' ').trim());
    const dates = dt.replace(/-/g, '') + '/' + dt.replace(/-/g, '');
    return 'https://www.google.com/calendar/render?action=TEMPLATE&text=' + cleanTitle + '&dates=' + dates + '/' + dates + '&details=' + details + '&location=Pembina+Valley%2C+MB';
  }

  function renderDashboard() {
    const viewsBox = document.getElementById('dashboard-views');
    const referrersBox = document.getElementById('dashboard-referrers');
    const trendBox = document.getElementById('dashboard-trend');
    if (!viewsBox && !referrersBox && !trendBox) return;

    fetch('analytics.json')
      .then(r => r.json())
      .then(data => {
        const views = data.views || [];
        const referrers = data.referrers || [];
        const totalViews = views.reduce((s, v) => s + (v.count || 0), 0);
        const totalUniques = views.reduce((s, v) => s + (v.uniques || 0), 0);

        if (viewsBox) {
          viewsBox.innerHTML = '<div class="event-row"><div class="event-date"><div class="month">Views</div><div class="day">' + totalViews + '</div></div><div><div class="event-title">Total page views</div><div class="event-meta">Last 14 days</div></div></div><div class="event-row"><div class="event-date" style="background:#fef3c7;color:#92400e;"><div class="month">Visitors</div><div class="day">' + totalUniques + '</div></div><div><div class="event-title">Unique visitors</div><div class="event-meta">Last 14 days</div></div></div>';
        }

        if (referrersBox) {
          referrersBox.innerHTML = referrers.length
            ? referrers.map(r => '<div class="event-row"><div class="event-date" style="background:#eef2ff;color:#3730a3;"><div class="month">Ref</div><div class="day">' + r.count + '</div></div><div><div class="event-title">' + r.referrer + '</div><div class="event-meta">' + r.uniques + ' unique</div></div></div>').join('')
            : '<p class="muted">No referrer data yet.</p>';
        }

        if (trendBox) {
          trendBox.innerHTML = views.length
            ? views.map(v => {
                const date = new Date(v.timestamp).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
                return '<div class="event-row"><div class="event-date" style="background:#f1f5f9;color:#0f172a;"><div class="month">Day</div><div class="day">' + date + '</div></div><div><div class="event-title">' + v.count + ' views</div><div class="event-meta">' + v.uniques + ' unique</div></div></div>';
              }).join('')
            : '<p class="muted">No trend data yet.</p>';
        }
      })
      .catch(() => {
        if (viewsBox) viewsBox.innerHTML = '<p class="muted">Analytics unavailable.</p>';
        if (referrersBox) referrersBox.innerHTML = '<p class="muted">Analytics unavailable.</p>';
        if (trendBox) trendBox.innerHTML = '<p class="muted">Analytics unavailable.</p>';
      });
  }

  function buildWeek() {
    const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const start = new Date(today);
    start.setDate(today.getDate() - today.getDay());

    const header = document.getElementById('cal-header');
    const body = document.getElementById('daily-events');
    if (!header || !body) return;
    header.innerHTML = '';
    body.innerHTML = '';

    const rangeStart = new Date(start);
    const rangeEnd = new Date(start);
    rangeEnd.setDate(start.getDate() + 6);

    const eventsByDay = [[], [], [], [], [], [], []];

    const addIfInWeek = (dateStr, ev) => {
      const parts = dateStr.split('-');
      const evDate = new Date(+parts[0], +parts[1] - 1, +parts[2]);
      if (evDate >= rangeStart && evDate <= rangeEnd) {
        const diff = Math.round((evDate - start) / 86400000);
        if (diff >= 0 && diff < 7) eventsByDay[diff].push(ev);
      }
    };

    const fmt = (y, m, d) => `${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    const year = now.getFullYear();
    const month = now.getMonth();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    for (let d = 1; d <= daysInMonth; d++) {
      const dow = new Date(year, month, d).getDay();
      if (dow === 2) addIfInWeek(fmt(year, month, d), { category: 'community', title: "Winkler Farmer's Market", time: 'Tue 4-6 PM · Central Station parking lot' });
      if (month === 7 && dow === 3) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Concerts in the Park', time: 'Wed 7:00 PM · Bethel Heritage Park' });
      if (month === 7 && d >= 7 && d <= 9) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Winkler Harvest Festival', time: 'Fairgrounds' });
      if (month === 7 && d === 6) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Paper Chain Creations', time: '10:30 AM & 1:30 PM · Winkler Library' });
      if (month === 7 && d === 5) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Summer Storytime', time: '10:30 AM & 1:30 PM · Winkler Library' });
      if (month === 8 && d === 4) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Catie St. Germain and Brothers Keep', time: '7:00 PM · Concert Hall' });
      if (month === 8 && d === 18) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Summer Shores Paint & Sip', time: '6:00 PM · Winkler Arts & Culture' });
      if (month === 9 && d === 18) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Chamber Member Appreciation BBQ', time: 'Winkler City Hall · 185 Main St' });
      if (month === 9 && d === 7) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Municipal Forum', time: 'P.W. Enns Centennial Concert Hall' });
      if (month === 8 && d === 10) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Mosaic Tray Workshop', time: '7:00 PM · Winkler Arts & Culture' });
      if (month === 8 && d === 10) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Jr. Summer Art Camp (5-8)', time: '9:30 AM · Winkler Arts & Culture' });
      if (month === 8 && d === 10) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Summer Art Camp (9-12)', time: '1:00 PM · Winkler Arts & Culture' });
      if (month === 8 && d === 2) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive' });
      if (month === 7 && d >= 28 && d <= 30 && year === 2026) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Winkler Harvest Festival', time: 'Fairgrounds · Free admission' });
      if (month === 7 && d >= 6 && d <= 9 && year === 2026) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Harvest Festival Events', time: 'Winkler · Various times' });
      if (month === 8 && d >= 28 && d <= 30) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Downtown Morden · Free' });
      if (month === 8 && d === 29) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Back40 Music Festival', time: 'Morden, MB' });
      if (month === 8 && d === 24) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St' });
      if (month === 8 && d === 17) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'MCC Blanket Making', time: '9:30 AM · Morden Mennonite Church' });
      if (month === 8 && d === 19) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta' });
      if (month === 8 && d === 12) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Kidventure Wednesdays', time: '1:00 PM · Altona EMM Church' });
      if (month === 8 && d === 6) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street' });
      if (month === 8 && d === 8) addIfInWeek(fmt(year, month, d), { category: 'fundraiser', title: 'Fundraising BBQ', time: '11:30 AM · Faith Mission, Winkler' });
      if (month === 8 && d === 9) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Harvest Festival Service', time: '10:00 AM · Winkler Park · Winkler EMMC' });
      if (month === 8 && d === 16) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive' });
      if (month === 8 && d === 18) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Church Council Mtg', time: '7:00 PM · 600 Southview Drive' });
      if (month === 8 && d === 23) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive' });
      if (month === 8 && d === 30) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive' });
      if (month === 8 && d === 7) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Labour Day - No School', time: 'Prairie Dale School · pds.gvsd.ca' });
      if (month === 8 && d === 8) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Prairie Dale No Classes Admin Day', time: 'Prairie Dale School · pds.gvsd.ca' });
      if (month === 8 && d === 9) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Prairie Dale First Day Grades K-9', time: 'Prairie Dale School · pds.gvsd.ca' });
      if (month === 8 && d === 10) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Prairie Dale First Day Grades 10-12', time: 'Prairie Dale School · pds.gvsd.ca' });
    }

    for (let i = 0; i < 7; i++) {
      const d = new Date(start);
      d.setDate(start.getDate() + i);
      const isToday = d.getTime() === today.getTime();

      const h = document.createElement('div');
      h.className = 'cal-day-header';
      h.innerHTML = `<div${isToday ? ' class="cal-now"' : ''}>${days[d.getDay()]}</div><div class="cal-date">${months[d.getMonth()]} ${d.getDate()}</div>`;
      header.appendChild(h);

      const col = document.createElement('div');
      col.className = 'day-column';
      col.dataset.day = isToday ? 'Today' : `${days[d.getDay()]} ${months[d.getMonth()]} ${d.getDate()}`;
      body.appendChild(col);

      eventsByDay[i].forEach(ev => {
        const el = document.createElement('div');
        el.className = 'day-event';
        el.dataset.category = ev.category;
        const dateStr = d.toISOString().split('T')[0];
        const gcalWeek = addGoogleCalendarLink(ev.title, ev.time, dateStr);
        const safeTitle = ev.title.replace(/'/g, '\\'');
        const safeTime = ev.time.replace(/'/g, '\\'');
        el.innerHTML = `<div class="title">${ev.title}</div><div class="time">${ev.time}</div><div class="export-row"><button class="export-btn" onclick="downloadICS('${safeTitle}','${safeTime}','${dateStr}')">ICS</button><a class="export-btn" href="${gcalWeek}" target="_blank">Google</a></div>`;
        col.appendChild(el);
      });
    }
  }

  function filterDayActivities(category, btn) {
    const pills = document.querySelectorAll('#act-days .pill');
    pills.forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    document.querySelectorAll('#act-days .day-event').forEach(ev => {
      ev.style.display = (category === 'all' || ev.dataset.category === category) ? '' : 'none';
    });
  }

  function buildActivityWeek() {
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
      if (!eventsByDate[dateStr]) eventsByDate[dateStr] = [];
      eventsByDate[dateStr].push(ev);
    };

    const dow = (y, m, d) => new Date(y, m, d).getDay();
    const fmt = (y, m, d) => `${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;

    for (let d = 1; d <= daysInMonth; d++) {
      if (dow(year, month, d) === 2) add(fmt(year, month, d), { category: 'community', title: 'Winkler Farmer’s Market', time: 'Tue 4-6 PM · Central Station parking lot' });
      if (dow(year, month, d) === 3 && (month === 6 || month === 7)) add(fmt(year, month, d), { category: 'community', title: 'Concerts in the Park', time: 'Wed 7:00 PM · Bethel Heritage Park' });
      if (month === 7 && d >= 7 && d <= 9) add(fmt(year, month, d), { category: 'community', title: 'Winkler Harvest Festival', time: 'Fairgrounds · Aug 7-9' });
      if (month === 8 && d === 18) add(fmt(year, month, d), { category: 'community', title: 'Summer Shores Paint & Sip', time: '6:00 PM · Winkler Arts & Culture' });
      if (month === 8 && d === 4) add(fmt(year, month, d), { category: 'community', title: 'Catie St. Germain and Brothers Keep', time: '7:00 PM · Concert Hall' });
      if (month === 9 && d === 18) add(fmt(year, month, d), { category: 'community', title: 'Chamber Member Appreciation BBQ', time: 'Winkler City Hall · 185 Main St' });
      if (month === 9 && d === 7) add(fmt(year, month, d), { category: 'community', title: 'Municipal Forum', time: 'P.W. Enns Centennial Concert Hall' });
      if (month === 7 && d === 6) add(fmt(year, month, d), { category: 'community', title: 'Paper Chain Creations', time: '10:30 AM & 1:30 PM · Winkler Library' });
      if (month === 7 && d === 5) add(fmt(year, month, d), { category: 'community', title: 'Summer Storytime', time: '10:30 AM & 1:30 PM · Winkler Library' });
      if (month === 8 && d === 10) add(fmt(year, month, d), { category: 'family', title: 'Mosaic Tray Workshop', time: '7:00 PM · Winkler Arts & Culture' });
      if (month === 8 && d === 2) add(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive' });
      if (month === 8 && d === 9) add(fmt(year, month, d), { category: 'family', title: 'Harvest Festival Service', time: '10:00 AM · Winkler Park · Winkler EMMC' });
      if (month === 8 && d === 16) add(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive' });
      if (month === 8 && d === 18) add(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Church Council Mtg', time: '7:00 PM · 600 Southview Drive' });
      if (month === 8 && d === 23) add(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive' });
      if (month === 8 && d === 30) add(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive' });
      if (month === 8 && d === 10) add(fmt(year, month, d), { category: 'family', title: 'Jr. Summer Art Camp (5-8)', time: '9:30 AM · Winkler Arts & Culture' });
      if (month === 8 && d === 10) add(fmt(year, month, d), { category: 'family', title: 'Summer Art Camp (9-12)', time: '1:00 PM · Winkler Arts & Culture' });
      if (month === 8 && d === 7) add(fmt(year, month, d), { category: 'family', title: 'Labour Day - No School', time: 'Prairie Dale School · pds.gvsd.ca' });
      if (month === 8 && d === 8) add(fmt(year, month, d), { category: 'family', title: 'Prairie Dale No Classes Admin Day', time: 'Prairie Dale School · pds.gvsd.ca' });
      if (month === 8 && d === 9) add(fmt(year, month, d), { category: 'family', title: 'Prairie Dale First Day Grades K-9', time: 'Prairie Dale School · pds.gvsd.ca' });
      if (month === 8 && d === 10) add(fmt(year, month, d), { category: 'family', title: 'Prairie Dale First Day Grades 10-12', time: 'Prairie Dale School · pds.gvsd.ca' });
    }

    for (let d = 1; d <= daysInMonth; d++) {
      const date = new Date(year, month, d);
      const isToday = date.getTime() === today.getTime();
      const dateStr = fmt(year, month, d);
      const dayEvents = eventsByDate[dateStr] || [];

      const section = document.createElement('div');
      section.className = 'activity';
      section.style.marginBottom = '12px';
      section.dataset.date = dateStr;
      section.innerHTML = `<div class="name" style="font-size:1.05rem; color:${isToday ? '#dc2626' : 'inherit'}">${days[date.getDay()]} · ${months[date.getMonth()]} ${d}</div>`;

      if (dayEvents.length) {
        const list = document.createElement('div');
        list.style.marginTop = '6px';
        list.style.display = 'flex';
        list.style.flexDirection = 'column';
        list.style.gap = '6px';
        dayEvents.forEach(ev => {
          const item = document.createElement('div');
          item.className = 'day-event';
          item.dataset.category = ev.category;
          item.style.borderLeft = '3px solid #7c3aed';
          item.style.padding = '8px 10px';
          item.style.borderRadius = '0 10px 10px 0';
          item.style.background = '#f8fafc';
          const actDate = section ? section.dataset.date || '' : '';
          const gcalAct = addGoogleCalendarLink(ev.title, ev.time, actDate);
          const safeTitle2 = ev.title.replace(/'/g, '\\'');
          const safeTime2 = ev.time.replace(/'/g, '\\'');
          item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div><div class="export-row"><button class="export-btn" onclick="downloadICS('${safeTitle2}','${safeTime2}','${actDate}')">ICS</button><a class="export-btn" href="${gcalAct}" target="_blank">Google</a></div>`;
          list.appendChild(item);
        });
        section.appendChild(list);
      } else {
        const empty = document.createElement('div');
        empty.className = 'desc';
        empty.textContent = 'No events listed.';
        section.appendChild(empty);
      }

      body.appendChild(section);
    }
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

    const samples = [];
    const add = (day, title) => { if (day >= 1 && day <= daysInMonth) samples.push({ day, title }); };

    for (let d = 1; d <= daysInMonth; d++) {
      const date = new Date(year, month, d);
      const dow = date.getDay();
      const titles = [];
      if (dow === 2) titles.push("Winkler Farmer's Market");
      if (month === 7 && dow === 3) titles.push('Concerts in the Park');
      if (month === 7 && d >= 7 && d <= 9) titles.push('Winkler Harvest Festival');
      if (month === 7 && d === 6) titles.push('Paper Chain Creations');
      if (month === 7 && d === 5) titles.push('Summer Storytime');
      if (month === 8 && d === 4) titles.push('Catie St. Germain');
      if (month === 8 && d === 18) titles.push('Paint & Sip');
      if (month === 9 && d === 18) titles.push('Chamber BBQ');
      if (month === 9 && d === 7) titles.push('Municipal Forum');
      if (month === 8 && d === 10) titles.push('Mosaic Workshop');
      if (month === 8 && d === 10) titles.push('Jr. Art Camp');
      if (month === 8 && d === 10) titles.push('Summer Art Camp');
      if (titles.length) add(d, titles.join(' / '));
    }

    const grid = document.createElement('div');
    grid.className = 'month-grid';

    days.forEach(d => {
      const h = document.createElement('div');
      h.className = 'month-header';
      h.textContent = d;
      grid.appendChild(h);
    });

    for (let i = 0; i < firstDay; i++) {
      const empty = document.createElement('div');
      empty.className = 'month-day empty';
      grid.appendChild(empty);
    }

    for (let d = 1; d <= daysInMonth; d++) {
      const cell = document.createElement('div');
      cell.className = 'month-day';
      const isToday = d === today;
      cell.innerHTML = `<div style="font-weight:${isToday ? '700' : '400'}; color:${isToday ? '#dc2626' : 'inherit'}">${d}</div>`;
      samples.filter(s => s.day === d).forEach(s => {
        const chip = document.createElement('div');
        chip.className = 'chip';
        chip.textContent = s.title;
        cell.appendChild(chip);
      });
      grid.appendChild(cell);
    }

    wrap.innerHTML = '';
    wrap.appendChild(grid);
  }

  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const page = link.dataset.page;
      document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
      document.getElementById('page-' + page).classList.add('active');
      document.querySelectorAll('.nav-link').forEach(n => n.classList.remove('active'));
      link.classList.add('active');
      if (page === 'weather' || page === 'home') loadWeather();
    });
  });

  async function loadWeather() {
    try {
      const lat = 49.1833;
      const lon = -97.9339;
      const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America%2FWinnipeg`;
      const res = await fetch(url);
      const data = await res.json();
      const cw = data.current_weather;
      const tempEls = document.querySelectorAll('#temp, #temp2');
      const condEls = document.querySelectorAll('#condition, #condition2');
      const locEls = document.querySelectorAll('#location, #location2');
      const updEls = document.querySelectorAll('#updated, #updated2');
      tempEls.forEach(el => el.textContent = Math.round(cw.temperature) + '°');
      condEls.forEach(el => el.textContent = weatherLabel(cw.weathercode) + ' · Wind: ' + cw.windspeed + ' km/h');
      locEls.forEach(el => el.textContent = 'Winkler, MB');
      updEls.forEach(el => el.textContent = 'Updated: ' + new Date().toLocaleTimeString());
      drawWeatherIcon('weatherIcon', cw.weathercode);
      drawWeatherIcon('weatherIcon2', cw.weathercode);
      updateActivities(cw.temperature, cw.windspeed, cw.weathercode);
      updateWeatherPlan(cw.temperature, cw.weathercode);
      if (data.daily) renderWeekly(data.daily);
    } catch (e) {
      console.warn('Weather load failed:', e);
      const tempEl = document.getElementById('temp');
      const condEl = document.getElementById('condition');
      const locEl = document.getElementById('location');
      const temp2El = document.getElementById('temp2');
      const cond2El = document.getElementById('condition2');
      const loc2El = document.getElementById('location2');
      if (tempEl) tempEl.textContent = '--°';
      if (condEl) condEl.textContent = 'Weather unavailable';
      if (locEl) locEl.textContent = 'Winkler, MB';
      if (temp2El) temp2El.textContent = '--°';
      if (cond2El) cond2El.textContent = 'Weather unavailable';
      if (loc2El) loc2El.textContent = 'Winkler, MB';
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

  function drawWeatherIcon(canvasId, code) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = 120;
    canvas.height = 120;
    ctx.clearRect(0, 0, 120, 120);
    ctx.fillStyle = '#0f172a';
    if (code === 0) {
      ctx.beginPath(); ctx.arc(60, 55, 22, 0, Math.PI * 2); ctx.fill();
      for (let i = 0; i < 8; i++) { ctx.save(); ctx.translate(60, 55); ctx.rotate(i * Math.PI / 4); ctx.fillRect(46, 28, 4, 14); ctx.restore(); }
    } else if (code <= 3) {
      ctx.beginPath(); ctx.arc(60, 55, 22, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#e5e7eb';
      ctx.beginPath(); ctx.arc(80, 70, 18, 0, Math.PI * 2); ctx.fill();
    } else if (code <= 67) {
      ctx.fillStyle = '#9ca3af';
      ctx.beginPath(); ctx.arc(35, 38, 10, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(55, 28, 12, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(78, 40, 11, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#2563eb';
      ctx.fillRect(28, 70, 60, 8); ctx.fillRect(38, 86, 40, 7); ctx.fillRect(48, 100, 24, 6);
    } else {
      ctx.fillStyle = '#e5e7eb';
      ctx.fillRect(25, 70, 70, 9); ctx.fillRect(35, 88, 50, 8); ctx.fillRect(45, 105, 30, 6);
    }
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

    const items = [outdoor[0], indoor[0]];
    box.innerHTML = items.map(i => `<div class="activity"><div class="name">${i.name}</div><div class="desc">${i.desc}</div></div>`).join('');
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
    const targets = [
      document.getElementById('weekly-home'),
      document.getElementById('weekly-page')
    ].filter(Boolean);

    if (!targets.length) return;
    if (!daily || !daily.time || !daily.time.length) {
      targets.forEach(el => el.innerHTML = '<div class="muted">Weekly forecast unavailable</div>');
      return;
    }

    const count = Math.min(7, daily.time.length);
    let html = '';
    for (let i = 0; i < count; i++) {
      const date = new Date(daily.time[i] + 'T00:00:00');
      const label = days[date.getDay()] + ', ' + months[date.getMonth()] + ' ' + date.getDate();
      const maxT = daily.temperature_2m_max ? Math.round(daily.temperature_2m_max[i]) : '--';
      const minT = daily.temperature_2m_min ? Math.round(daily.temperature_2m_min[i]) : '--';
      const precip = daily.precipitation_sum ? daily.precipitation_sum[i].toFixed(1) : null;
      const condition = weatherLabel(daily.weathercode[i]);
      const precipText = precip === null ? '' : `${precip} mm`;
      html += `<div class="weekly-day"><div class="label">${label}</div><div class="detail">${condition}</div><div class="value">${maxT}° / ${minT}°</div><div class="detail">${precipText}</div></div>`;
    }
    targets.forEach(el => el.innerHTML = html);
  }

  renderDashboard();
  buildWeek();
  buildActivityWeek();
  buildMonth();
  renderFeatured();
  renderFamilyEvents();
  loadWeather();
}

  function renderFeatured() {
    const container = document.getElementById('featured-events');
    if (!container) return;
    const featured = [
      { category: 'community', title: 'Winkler Harvest Festival', time: 'Aug 7-9 · Winkler Fairgrounds', date: 'Aug 7' },
      { category: 'family', title: 'Prairie Dale School Events', time: 'Aug-Sep · Winkler, MB', date: 'Aug' },
      { category: 'community', title: 'Chamber Member Appreciation BBQ', time: 'Sep 18 · Winkler City Hall', date: 'Sep 18' },
      { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Aug 28-30 · Downtown Morden', date: 'Aug 28' },
      { category: 'community', title: 'Morden Back40 Music Festival', time: 'Aug 29 · Morden, MB', date: 'Aug 29' },
      { category: 'community', title: 'The Big Canoe', time: 'Sep 19 · Lake Minnewasta', date: 'Sep 19' },
      { category: 'community', title: 'Altona Kidventure Wednesdays', time: 'Aug 12 · Altona EMM Church', date: 'Aug 12' }
    ];

    container.innerHTML = featured.map(ev => `
    <div class="featured-card" data-category="${ev.category}">
      <div class="row">
        <div class="badge-row">
          <span class="date-badge">${ev.date}</span>
          <span class="cat-badge">${ev.category}</span>
        </div>
      </div>
      <div class="title">${ev.title}</div>
      <div class="meta">${ev.time}</div>
      <div class="export-row"><a class="export-btn" href="${addGoogleCalendarLink(ev.title, ev.time, '')}" target="_blank">Google Calendar</a></div>
    </div>
    `).join('');
  }

  function renderFamilyEvents() {
    const schoolBox = document.getElementById('family-school-events');
    const churchBox = document.getElementById('family-church-events');
    const garageBox = document.getElementById('family-garage-events');

    const schoolEvents = [
      { title: 'Labour Day - No School', date: 'Aug 4 (Mon)', time: 'Prairie Dale School · Winkler', category: 'family' },
      { title: 'Admin Day - No Classes', date: 'Aug 5 (Tue)', time: 'Prairie Dale School · Winkler', category: 'family' },
      { title: 'First Day Grades K-9', date: 'Sep 9 (Wed)', time: 'Prairie Dale School · Winkler', category: 'family' },
      { title: 'First Day Grades 10-12', date: 'Sep 10 (Thu)', time: 'Prairie Dale School · Winkler', category: 'family' },
      { title: 'Whimsical Wonders Art Camp', date: 'Aug 31-Sep 4', time: 'City of Morden · morden.ca', category: 'family' },
      { title: 'Altona Aquatic Centre', date: 'Summer 2026', time: 'Altona, MB · altona.ca', category: 'family' }
    ];

    const churchEvents = [
      { title: 'Winkler EMMC Worship Service', date: 'Aug 2, 16, 23, 30', time: '10:30 AM · 600 Southview Drive', category: 'family' },
      { title: 'Harvest Festival Service', date: 'Aug 9 (Sun)', time: '10:00 AM · Winkler Park', category: 'family' },
      { title: 'Church Council Meeting', date: 'Aug 18 (Tue)', time: '7:00 PM · 600 Southview Drive', category: 'family' },
      { title: 'Kidventure Wednesdays', date: 'Wednesdays', time: '1:00 PM · Altona EMM Church', category: 'family' },
      { title: 'MCC Blanket Making', date: '1st/3rd Mondays', time: '9:30 AM · Morden Mennonite Church', category: 'family' }
    ];

    const garageEvents = [
      { title: 'Weekly Garage Sales', date: 'Aug 3-9', time: 'Multiple addresses · winkler.garagesalejunkie.ca', category: 'community' },
      { title: 'City Wide Garage Sale', date: 'May 23, 2026', time: 'Multiple addresses · Watch for 2027 date', category: 'community' },
      { title: 'Morden City Wide Garage Sale', date: 'Jun 6, 2026', time: 'Morden, MB · Multiple addresses', category: 'community' },
      { title: 'Morden Community BBQ Fundraiser', date: 'Aug 8', time: '11:30 AM · Faith Mission, Winkler', category: 'fundraiser' },
      { title: 'Altona Aquatic Centre', date: 'Summer 2026', time: 'Altona, MB · Family fun', category: 'community' }
    ];

    const renderCard = (ev) => `
      <div class="day-event" data-category="${ev.category}">
        <div class="title">${ev.title}</div>
        <div class="time">${ev.date} · ${ev.time}</div>
      </div>
    `;

    if (schoolBox) schoolBox.innerHTML = schoolEvents.map(renderCard).join('');
    if (churchBox) churchBox.innerHTML = churchEvents.map(renderCard).join('');
    if (garageBox) garageBox.innerHTML = garageEvents.map(renderCard).join('');
  }
