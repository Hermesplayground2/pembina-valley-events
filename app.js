
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
    'STATUS:CONFIRMED',
    'TRANSP:OPAQUE',
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

  // Events are loaded from events.json by loadEvents(). No hardcoded list here.
  let EVENTS = [];
  const isToday = (d) => new Date(d + 'T12:00:00').toDateString() === new Date().toDateString();

  const timeToSort = (timeStr) => {
    const t = String(timeStr).trim();
    const hourMatch = t.match(/(\d{1,2})(?::(\d{2}))?\s*(AM|PM)?/i);
    if (!hourMatch) return 9999;
    let hour = parseInt(hourMatch[1], 10);
    const minute = hourMatch[2] ? parseInt(hourMatch[2], 10) : 0;
    const meridiem = hourMatch[3] ? hourMatch[3].toUpperCase() : null;
    if (meridiem === 'PM' && hour < 12) hour += 12;
    if (meridiem === 'AM' && hour === 12) hour = 0;
    return hour * 100 + minute;
  };
  function buildUpcoming() {
    const body = document.getElementById('daily-events');
    if (!body) return;
    body.innerHTML = '';

    const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    const today = new Date();
    today.setHours(0,0,0,0);
    const todayStr = today.getFullYear() + '-' +
      String(today.getMonth() + 1).padStart(2, '0') + '-' +
      String(today.getDate()).padStart(2, '0');
    const rangeEnd = new Date(today);
    rangeEnd.setDate(rangeEnd.getDate() + 6);

    const selectedTown = window._selectedTown || 'all';
    const searchQuery = window._searchQuery || '';
    const upcoming = EVENTS.filter(ev => {
      const d = new Date(ev.date + 'T12:00:00');
      if (d <= today || d > rangeEnd) return false;
      // Town filter
      if (selectedTown !== 'all') {
        const loc = (ev.time || '').toLowerCase();
        if (!loc.includes(selectedTown.toLowerCase())) return false;
      }
      // Search filter
      if (searchQuery) {
        const title = (ev.title || '').toLowerCase();
        const loc = (ev.time || '').toLowerCase();
        if (!title.includes(searchQuery) && !loc.includes(searchQuery)) return false;
      }
      return true;
    }).sort((a, b) => a.date.localeCompare(b.date) || timeToSort(a.time) - timeToSort(b.time));

    const grouped = {};
    upcoming.forEach(ev => {
      if (!grouped[ev.date]) grouped[ev.date] = [];
      grouped[ev.date].push(ev);
    });

    Object.keys(grouped).sort().forEach(dateStr => {
      const d = new Date(dateStr + 'T12:00:00');
      const section = document.createElement('div');
      section.className = 'day-section';
      const dateLabel = document.createElement('div');
      dateLabel.className = 'day-header';
      dateLabel.dataset.expanded = 'false';
      dateLabel.innerHTML = '<span class="day-toggle"></span>' + days[d.getDay()] + ', ' + monthNames[d.getMonth()].slice(0,3) + ' ' + d.getDate() + ' <span class="event-count">' + grouped[dateStr].length + '</span>';
      dateLabel.addEventListener('click', () => {
        const expanded = dateLabel.dataset.expanded === 'true';
        dateLabel.dataset.expanded = String(!expanded);
        dateLabel.classList.toggle('expanded', !expanded);
        list.classList.toggle('hidden-events', expanded);
      });
      section.appendChild(dateLabel);

      const list = document.createElement('div');
      list.className = 'event-list hidden-events';
      grouped[dateStr].sort((a, b) => timeToSort(a.time) - timeToSort(b.time)).forEach(ev => {
        const item = document.createElement('div');
        item.className = 'day-event bubble';
        item.dataset.category = ev.category;
        const copyText = (ev.title + '\n' + ev.time).trim();
        item.innerHTML = '<a class="event-link" href="' + ev.link + '" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;"><span class="title">' + ev.title + '</span></a><span class="time">' + ev.time + '</span><button class="copy-btn" data-copy="' + copyText.replace(/"/g, '&quot;') + '">Copy</button>';
        list.appendChild(item);
      });
      section.appendChild(list);
      body.appendChild(section);
    });

    if (!upcoming.length) {
      body.innerHTML = '<div class="muted" style="padding:10px;">No events in the next 6 days.</div>';
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

    // Merge events from EVENTS array so one-off events appear on Activities page
    EVENTS.forEach(ev => {
      if (ev.date >= fmt(year, startMonth, 1)) {
        const parts = ev.date.split('-');
        const evDate = new Date(+parts[0], +parts[1] - 1, +parts[2]);
        if (evDate >= today) {
          if (!eventsByDate[ev.date]) eventsByDate[ev.date] = [];
          eventsByDate[ev.date].push(ev);
        }
      }
    });

    // No hardcoded events. All content comes from EVENTS (loaded from events.json).

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
      section.dataset.date = dateStr;
      const dateLabel = document.createElement('div');
      dateLabel.className = 'day-header';
      dateLabel.dataset.expanded = 'false';
      dateLabel.innerHTML = '<span class="day-toggle"></span>' + days[evDate.getDay()] + ', ' + monthNames[evDate.getMonth()].slice(0,3) + ' ' + evDate.getDate() + ' <span class="event-count">' + eventsByDate[dateStr].length + '</span>';
      dateLabel.addEventListener('click', () => {
        const expanded = dateLabel.dataset.expanded === 'true';
        dateLabel.dataset.expanded = String(!expanded);
        dateLabel.classList.toggle('expanded', !expanded);
        list.classList.toggle('hidden-events', expanded);
      });
      section.appendChild(dateLabel);

      const list = document.createElement('div');
      list.className = 'event-list hidden-events';
      eventsByDate[dateStr].sort((a, b) => timeToSort(a.time) - timeToSort(b.time)).forEach(ev => {
        const item = document.createElement('div');
        item.className = 'day-event bubble';
        item.dataset.category = ev.category;
        const copyText = (ev.title + '\n' + ev.time).trim();
        item.innerHTML = '<a class="event-link" href="' + ev.link + '" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;"><span class="title">' + ev.title + '</span></a><span class="time">' + ev.time + '</span><button class="copy-btn" data-copy="' + copyText.replace(/"/g, '&quot;') + '">Copy</button>';
        list.appendChild(item);
      });
      section.appendChild(list);
      body.appendChild(section);
    });
  }

  
  function buildToday() {
    const container = document.getElementById('today-events');
    const label = document.getElementById('today-date-label');
    if (!container) return;

    container.innerHTML = '';

    const now = new Date();
    const todayStr = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
    const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    if (label) {
      label.textContent = `${monthNames[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()}`;
    }

    const searchQuery = window._searchQuery || '';
    const todays = EVENTS.filter(ev => ev.date === todayStr && (!searchQuery || (ev.title || '').toLowerCase().includes(searchQuery) || (ev.time || '').toLowerCase().includes(searchQuery)));

    if (!todays.length) {
      container.innerHTML = '<p class="muted">No events scheduled for today.</p>' +
        '<div class="spacer"></div>';
      return;
    }

    todays.forEach(ev => {
      const el = document.createElement('a');
      el.className = 'day-event bubble';
      el.href = ev.link || '#';
      el.target = '_blank';
      el.rel = 'noopener';
      el.dataset.category = ev.category;
      el.innerHTML = `<span class="title">${ev.title}</span><span class="time">· ${ev.time}</span><div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, '&quot;')}" data-time="${ev.time.replace(/"/g, '&quot;')}" data-date="${ev.date}">📅 Add to Calendar</button></div>`;
      container.appendChild(el);
    });
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
      if (page === 'home') { try { renderFeatured(); buildUpcoming(); buildCalendar('home-calendar-container'); } catch (e) { console.error(e); } }
      if (page === 'calendar') { try { buildCalendar('calendar-container'); } catch (e) { console.error(e); } }
      try { buildToday(); } catch (e) { console.error(e); }
      if (page === 'activities') { try { buildActivityWeek(); } catch (e) { console.error(e); } }
      if (page === 'family') { try { renderFamilyEvents(); } catch (e) { console.error(e); } }
      if (page === 'fundraiser') { try { renderFundraisers(); } catch (e) { console.error(e); } }
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

  
  // ── Calendar ──────────────────────────────────────────────────────────────
  // Renders purely from EVENTS (loaded from events.json). No hardcoded data.
  let CAL_YEAR = new Date().getFullYear();
  let CAL_MONTH = new Date().getMonth();
  let CAL_SELECTED = null;

  function buildCalendar(targetId) {
    const container = document.getElementById(targetId || 'calendar-container');
    if (!container) return;
    const scope = targetId || 'calendar-container';

    const now = new Date();
    const monthNames = ['January','February','March','April','May','June','July',
                        'August','September','October','November','December'];
    const dayNames = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];

    const year = CAL_YEAR;
    const month = CAL_MONTH;
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const todayStr = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

    // Build a date->events map from EVENTS
    const eventsByDate = {};
    (Array.isArray(EVENTS) ? EVENTS : []).forEach(ev => {
      if (!ev || !ev.date) return;
      if (!eventsByDate[ev.date]) eventsByDate[ev.date] = [];
      eventsByDate[ev.date].push(ev);
    });

    let html = `<div class="calendar-header">
      <div class="calendar-nav">
        <button class="cal-nav-btn" data-cal-nav="prev" title="Previous month">‹</button>
      </div>
      <div class="calendar-title">${monthNames[month]} ${year}</div>
      <div class="calendar-nav">
        <button class="cal-nav-btn" data-cal-nav="next" title="Next month">›</button>
      </div>
    </div>`;

    html += `<div class="calendar-days-header">`;
    dayNames.forEach(d => { html += `<div class="cal-day-name">${d}</div>`; });
    html += `</div><div class="calendar-grid">`;

    for (let i = 0; i < firstDay; i++) html += `<div class="calendar-day empty"></div>`;

    for (let d = 1; d <= daysInMonth; d++) {
      const dateStr = `${year}-${String(month+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
      const dayEvents = eventsByDate[dateStr] || [];
      const isToday = dateStr === todayStr ? ' today' : '';
      const hasEvents = dayEvents.length > 0 ? ' has-events' : '';
      const isSelected = CAL_SELECTED === dateStr ? ' selected' : '';

      html += `<div class="calendar-day${isToday}${hasEvents}${isSelected}" data-date="${dateStr}">
        <div class="day-number">${d}</div>`;
      dayEvents.slice(0, 3).forEach(ev => {
        html += `<div class="day-chip" data-category="${ev.category || 'community'}">${(ev.title || '').replace(/</g,'&lt;').slice(0,22)}</div>`;
      });
      if (dayEvents.length > 3) {
        html += `<div class="day-chip" data-category="more">+${dayEvents.length - 3} more</div>`;
      }
      html += `</div>`;
    }
    html += `</div>`;

    container.innerHTML = html;

    // Wire navigation (scoped to this container so multiple calendars coexist)
    const prev = container.querySelector('[data-cal-nav="prev"]');
    const next = container.querySelector('[data-cal-nav="next"]');
    if (prev) prev.addEventListener('click', () => { CAL_MONTH--; if (CAL_MONTH < 0) { CAL_MONTH = 11; CAL_YEAR--; } buildCalendar(scope); });
    if (next) next.addEventListener('click', () => { CAL_MONTH++; if (CAL_MONTH > 11) { CAL_MONTH = 0; CAL_YEAR++; } buildCalendar(scope); });

    // Wire day clicks → jump to Activities page and expand that day
    container.querySelectorAll('.calendar-day:not(.empty)').forEach(cell => {
      cell.addEventListener('click', () => {
        const ds = cell.dataset.date;
        CAL_SELECTED = ds;
        // Switch to Activities page and expand the clicked day
        activatePage('activities');
        expandActivityDay(ds);
      });
    });
  }

  // Expand a specific day's section on the Activities page (called from calendar day click)
  function expandActivityDay(dateStr) {
    const section = document.querySelector(`.day-section[data-date="${dateStr}"]`);
    if (!section) return;
    const header = section.querySelector('.day-header');
    const list = section.querySelector('.event-list');
    if (header && list) {
      header.dataset.expanded = 'true';
      header.classList.add('expanded');
      list.classList.remove('hidden-events');
    }
    // Scroll to the section
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // ── Fundraisers ─────────────────────────────────────────────────────────
  const FUNDRAISERS = [
    {
      title: "Help Peter Wolfe get vision-saving eye surgery",
      date: "Ongoing",
      time: "Winkler, MB",
      link: "https://www.gofundme.com/f/help-peter-wolfe-get-vision-saving-eye-surgery",
      description: "Peter and Anna Wolfe from Winkler. Peter has lost 80% vision in one eye and needs surgery within two weeks to save his eyesight.",
      source: "GoFundMe",
      category: "medical"
    },
    {
      title: "Tragic Car Accident Takes Father, Leaves Children in Winkler",
      date: "Ongoing",
      time: "Winkler, MB",
      link: "https://www.gofundme.com/f/tragic-car-accident-takes-father-leaves-children-in-winkler",
      description: "For Miriam & Samuel James-Decker family. Father Samuel died in a car accident March 7, 2026, leaving 5 children from teen to infant.",
      source: "GoFundMe",
      category: "emergency"
    },
    {
      title: "Big Brothers Big Sisters of the Pembina Valley — Bike for Kids",
      date: "Annual event",
      time: "Altona to Gretna, MB",
      link: "https://canadahelps.org/en/charities/big-brothersbig-sisters-of-mordenwinkler-and-district-inc/p2p/bike-for-kids",
      description: "Annual trail ride along the Trans-Canada Trail from Altona to Gretna. Raises money for mentoring programs for kids.",
      source: "CanadaHelps",
      category: "charity"
    },
    {
      title: "Pembina Valley Humane Society — Highway 3.14 BBQ Competition",
      date: "September 6, 2026",
      time: "Suncatch, Morden, MB",
      link: "https://www.canadahelps.org/en/charities/pembina-valley-humane-society-inc/events/highway-314-bbq-competition",
      description: "BBQ competition between Chef Ryan Wiebe (Winkler) and Chef Colin Fehr (Morden), plus live bands. Tickets $30.",
      source: "CanadaHelps",
      category: "charity"
    },
    {
      title: "United Way Pembina Valley 2026 Campaign",
      date: "September 2026",
      time: "Winkler, Morden, Stanley",
      link: "https://www.unitedwaypembinavalley.ca/",
      description: "Raising $115,000 for 23 local non-profits. All funds stay in the region.",
      source: "United Way",
      category: "charity"
    },
    {
      title: "Pembina Valley Pregnancy Care Centre — Fundraiser Meal",
      date: "October 24, 2026",
      time: "Pembina Threshermen's Museum, between Winkler and Morden",
      link: "https://www.pembinavalleyonline.com/articles/meatballs-and-mashed-potatoes-helping-raise-funds-for-local-families",
      description: "Drive-thru lunch and supper fundraiser. Supports free services in Winkler, Morden, and Altona.",
      source: "Local",
      category: "charity"
    }
  ];

  function renderFundraisers() {
    const box = document.getElementById('fundraiser-list');
    if (!box) return;
    box.innerHTML = '';

    FUNDRAISERS.forEach(fr => {
      const card = document.createElement('div');
      card.className = 'day-event bubble';
      card.style.marginBottom = '12px';
      card.style.padding = '14px';

      const badgeColor = fr.category === 'medical' ? '#dc2626' : fr.category === 'emergency' ? '#f59e0b' : '#10b981';
      const badgeText = fr.category === 'medical' ? 'Medical' : fr.category === 'emergency' ? 'Emergency' : 'Charity';

      card.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;">
          <div style="flex:1;">
            <div style="font-weight:800;font-size:0.95rem;color:#f1f5f9;">${fr.title.replace(/</g,'&lt;')}</div>
            <div style="color:#6b7280;font-size:0.82rem;margin-top:4px;">${fr.time} · ${fr.date}</div>
            <div style="color:#94a3b8;font-size:0.82rem;margin-top:6px;line-height:1.5;">${fr.description.replace(/</g,'&lt;')}</div>
          </div>
          <div style="text-align:right;flex-shrink:0;">
            <span style="display:inline-block;padding:3px 10px;border-radius:999px;font-size:0.7rem;font-weight:800;background:${badgeColor};color:#0f172a;">${badgeText}</span>
            <div style="margin-top:6px;font-size:0.68rem;color:#64748b;">${fr.source}</div>
          </div>
        </div>
        <div class="export-row" style="margin-top:10px;">
          <a class="export-btn" href="${fr.link}" target="_blank" rel="noopener" style="text-decoration:none;">Visit Fundraiser</a>
        </div>
      `;
      box.appendChild(card);
    });
  }

  function renderSearchBar() {
    // Add search input if not already present
    const nav = document.querySelector('.nav-inner');
    if (!nav || document.getElementById('event-search')) return;
    const searchHtml = '<input type="text" id="event-search" placeholder="Search events..." autocomplete="off" style="padding:8px 14px;border-radius:999px;border:1px solid rgba(255,255,255,0.15);background:rgba(255,255,255,0.05);color:#e2e8f0;font-size:0.85rem;outline:none;max-width:220px;">';
    nav.insertAdjacentHTML('beforeend', searchHtml);
    const searchInput = document.getElementById('event-search');
    searchInput.addEventListener('input', (e) => {
      window._searchQuery = e.target.value.toLowerCase();
      buildUpcoming();
      buildToday();
    });
  }

  // Town filter button delegation
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('town-btn')) {
      const town = e.target.dataset.town;
      window._selectedTown = town;
      // Update active state
      document.querySelectorAll('.town-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.town === town);
      });
      buildUpcoming();
    }
  });

  // Search bar wiring
  function initSearch() {
    const searchInput = document.getElementById('event-search');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        window._searchQuery = e.target.value.toLowerCase().trim();
        buildUpcoming();
        buildToday();
      });
    }
  }
const initPage = () => {
    initSearch();
    try {
      const page = (location.hash || '#home').replace('#page-', '').replace('#', '') || 'home';
      activatePage(page);
    } catch (e) {
      console.error('initPage error', e);
      const el = document.getElementById('page-home');
      if (el) el.classList.add('active');
    }

    // Wire "Back to Calendar" button on Activities page
    const backBtn = document.getElementById('back-to-calendar');
    if (backBtn) {
      backBtn.addEventListener('click', () => {
        activatePage('calendar');
      });
    }
  };

  async function loadEvents() {
    try {
      const res = await fetch('/events.json', { cache: 'no-store' });
      if (!res.ok) throw new Error('events.json HTTP ' + res.status);
      const data = await res.json();
      const raw = data.events || data;
      if (!Array.isArray(raw)) throw new Error('events.json not an array');
      EVENTS = raw.map(e => ({
        date: e.date,
        title: e.title,
        time: e.time || '',
        category: e.category || 'community',
        link: e.link || '#'
      }));
      console.log('Loaded ' + EVENTS.length + ' events from events.json');
      updateLastUpdated();
    } catch (err) {
      console.warn('events.json load failed, using fallback:', err);
    }
  }
  window.addEventListener('hashchange', initPage);

  function updateLastUpdated() {
    const el = document.getElementById('last-updated');
    if (!el) return;
    const now = new Date();
    const hh = String(now.getHours()).padStart(2,'0');
    const mm = String(now.getMinutes()).padStart(2,'0');
    el.textContent = 'Last updated ' + hh + ':' + mm;
  }

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      loadEvents().then(initPage).catch(err => { console.error('events load failed, using fallback', err); initPage(); });
    });
  } else {
    loadEvents().then(initPage).catch(err => { console.error('events load failed, using fallback', err); initPage(); });
  }

  const WEATHER_IMAGES = {
    clear: 'weather-media/day_frame.jpg',
    cloudy: 'weather-media/day_frame.jpg',
    rain: 'weather-media/rain_frame.jpg',
    night: 'weather-media/night_frame.jpg',
    fallback: 'weather-media/day_frame.jpg'
  };

  function pickWeatherImage(code, temp) {
    const hour = new Date().getHours();
    const isNight = hour < 6 || hour >= 20;
    const isPrecip = code >= 51 && code <= 99;
    if (isPrecip) return WEATHER_IMAGES.rain;
    if (isNight) return WEATHER_IMAGES.night;
    if (code <= 3) return WEATHER_IMAGES.clear;
    return WEATHER_IMAGES.cloudy;
  }

  let weatherCache = null;
  let weatherCacheTime = 0;
  const WEATHER_CACHE_TTL = 10 * 60 * 1000; // 10 minutes

  async function loadWeather() {
    const heroCond = document.getElementById('heroCondition');
    const tempEls = () => document.querySelectorAll('#temp, #temp2, #heroTemp');
    const condEls = () => document.querySelectorAll('#condition, #condition2, #heroCondition');
    const locEls = () => document.querySelectorAll('#location, #location2, #heroLocation');
    const updEls = () => document.querySelectorAll('#updated, #updated2');

    const apply = (temp, cond, loc, upd) => {
      tempEls().forEach(el => el.textContent = temp);
      condEls().forEach(el => el.textContent = cond);
      locEls().forEach(el => el.textContent = loc);
      updEls().forEach(el => el.textContent = upd);
    };

    const fallback = (code) => {
      apply('--°', 'Weather unavailable', 'Pembina, MB', '');
      updateActivities(15, 10, 3);
      updateWeatherPlan(15, 3);
      setWeatherVideo(3, 15);
      if (heroCond) heroCond.textContent = 'Weather unavailable';
      const imgSrc = pickWeatherImage(code || 3, 15);
      const heroImg = document.getElementById('heroWeatherImage');
      if (!heroImg) {
        const img = document.createElement('img');
        img.id = 'heroWeatherImage';
        img.alt = 'Weather';
        img.setAttribute('style', 'position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;opacity:0.85;transition:opacity 0.6s ease;');
        const scene = document.getElementById('weatherScene');
        const video = document.getElementById('heroWeatherVideo');
        if (scene && video) scene.insertBefore(img, video);
      }
      const targetImg = document.getElementById('heroWeatherImage');
      if (targetImg) {
        targetImg.src = imgSrc;
        targetImg.style.opacity = '1';
      }
    };

    // Guaranteed fallback after 5 seconds regardless of network state
    const fallbackTimer = setTimeout(() => fallback(3), 5000);

    try {
      // Use cached weather data if available and fresh
      if (weatherCache && (Date.now() - weatherCacheTime) < WEATHER_CACHE_TTL) {
        console.log('Using cached weather data');
        const cw = weatherCache.current_weather;
        apply(Math.round(cw.temperature) + '°', weatherLabel(cw.weathercode) + ' · Wind: ' + cw.windspeed + ' km/h', 'Pembina, MB', 'Updated: ' + new Date(weatherCacheTime).toLocaleTimeString());
        updateActivities(cw.temperature, cw.windspeed, cw.weathercode);
        updateWeatherPlan(cw.temperature, cw.weathercode);
        if (weatherCache.daily) renderWeekly(weatherCache.daily);
        setWeatherVideo(cw.weathercode, cw.temperature);
        return;
      }

      const lat = 49.1833;
      const lon = -97.9339;
      const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America%2FWinnipeg`;
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 8000);
      const res = await fetch(url, { signal: controller.signal });
      clearTimeout(timeoutId);
      clearTimeout(fallbackTimer);
      const data = await res.json();
      
      // Cache successful response
      weatherCache = data;
      weatherCacheTime = Date.now();
      const cw = data.current_weather;
      apply(Math.round(cw.temperature) + '°', weatherLabel(cw.weathercode) + ' · Wind: ' + cw.windspeed + ' km/h', 'Pembina, MB', 'Updated: ' + new Date().toLocaleTimeString());
      updateActivities(cw.temperature, cw.windspeed, cw.weathercode);
      updateWeatherPlan(cw.temperature, cw.weathercode);
      if (data.daily) renderWeekly(data.daily);
      setWeatherVideo(cw.weathercode, cw.temperature);
    } catch (e) {
      clearTimeout(fallbackTimer);
      console.warn('Weather fallback triggered:', e);
      fallback(3);
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
    let src = 'weather-media/day.mp4?v=1788408739';
    if (isPrecip) {
      src = 'weather-media/rain.mp4?v=1788408739';
    } else if (isClear && (hour < 6 || hour >= 20)) {
      src = 'weather-media/night.mp4?v=1788408739';
    } else if (!isClear && (hour < 6 || hour >= 20)) {
      src = 'weather-media/night.mp4?v=1788408739';
    }
    const currentSrc = video.src ? video.src.split('/').pop() : '';
    if (currentSrc && currentSrc.endsWith(src.split('/').pop())) return;
    video.style.transition = 'opacity 0.6s ease';
    video.style.opacity = '0';
    setTimeout(() => {
      video.src = src;
      video.load();
      const playPromise = video.play();
      if (playPromise !== undefined) {
        playPromise.then(() => {
          video.style.opacity = '1';
        }).catch(() => {
          video.style.opacity = '0';
          const overlay = document.getElementById('heroWeatherOverlay');
          if (overlay) overlay.style.opacity = '1';
        });
      }
      video.addEventListener('error', () => {
        const img = document.getElementById('heroWeatherImage');
        if (!img) {
          const fallbackImg = document.createElement('img');
          fallbackImg.id = 'heroWeatherImage';
          fallbackImg.alt = 'Weather';
          fallbackImg.src = 'weather-media/day_frame.jpg';
          fallbackImg.setAttribute('style', 'position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;opacity:0.85;transition:opacity 0.6s ease;');
          const scene = document.getElementById('weatherScene');
          if (scene) scene.insertBefore(fallbackImg, video);
        } else {
          img.style.opacity = '1';
        }
        video.style.opacity = '0';
        const overlay = document.getElementById('heroWeatherOverlay');
        if (overlay) overlay.style.opacity = '1';
      }, { once: true });
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
    const targets = [document.getElementById('weather-forecast')].filter(Boolean);
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

  try {
    const started = loadWeather();
    if (started && typeof started.then === 'function') {
    } else {
    }
  } catch (e) {
  }

  function renderFeatured() {
    const container = document.getElementById('featured-events');
    if (!container) return;
    const now = new Date();
    now.setHours(0,0,0,0);
    // Only show upcoming events from events.json, not "TBD", "Spring", etc.
    const featured = EVENTS.filter(ev => {
      const d = new Date(ev.date + 'T12:00:00');
      return d >= now && ev.date && ev.date.match(/^\d{4}-\d{2}-\d{2}$/);
    }).sort((a, b) => a.date.localeCompare(b.date)).slice(0, 6);

    if (!featured.length) {
      container.innerHTML = '<div class="muted" style="padding:14px;">No featured events coming up — check back soon!</div>';
      return;
    }

    container.innerHTML = featured.map(ev => `
      <a class="featured-card bubble" href="${ev.link || '#'}" target="_blank" rel="noopener" data-category="${ev.category}">
        <div class="row">
          <div class="badge-row">
            <span class="date-badge">${ev.date}</span>
            <span class="cat-badge">${ev.category}</span>
          </div>
        </div>
        <div class="title">${ev.title}</div>
        <div class="meta">${ev.time}</div>
        <button class="copy-btn" data-copy="${`${ev.title}\n${ev.time}`.replace(/"/g, '&quot;')}">Copy</button>
      </a>
    `).join('');
  }

  function renderFamilyEvents() {
    const schoolBox = document.getElementById('family-school-events');
    const churchBox = document.getElementById('family-church-events');
    const garageBox = document.getElementById('family-garage-events');

    // Family page: derive from EVENTS by category — no hardcoded entries.
    const schoolEvents  = EVENTS.filter(e => /school|first day|grad/i.test(e.title));
    const churchEvents  = EVENTS.filter(e => /church|ministry/i.test(e.title));
    const garageEvents  = EVENTS.filter(e => /garage|sale/i.test(e.title));

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
    if (!text) return;
    const fallback = () => {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); } catch (e) { /* ignore */ }
      document.body.removeChild(ta);
      const original = copyBtn.textContent;
      copyBtn.textContent = 'Copied';
      copyBtn.disabled = true;
      setTimeout(() => {
        copyBtn.textContent = original;
        copyBtn.disabled = false;
      }, 1200);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => {
        const original = copyBtn.textContent;
        copyBtn.textContent = 'Copied';
        copyBtn.disabled = true;
        setTimeout(() => {
          copyBtn.textContent = original;
          copyBtn.disabled = false;
        }, 1200);
      }).catch(fallback);
    } else {
      fallback();
    }
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