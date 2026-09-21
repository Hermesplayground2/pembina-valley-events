// Pembina Valley Events - Complete rewrite with events.json integration
// Cache-busted: v1789599600

// Configuration
const CONFIG = {
  weatherCacheTTL: 60 * 60 * 1000, // 60 minutes for weather
  weatherApiUrl: 'https://api.open-meteo.com/v1/forecast',
  weatherApiParams: {
    latitude: 49.1833,
    longitude: -97.9339,
    current_weather: true,
    daily: 'weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum',
    timezone: 'America/Winnipeg'
  },
  localCacheKey: 'pembina_events_cache',
  localCacheTTL: 24 * 60 * 60 * 1000 // 24 hours for local events
};

// State
let APP_STATE = {
  events: [],
  allEvents: [],
  featuredEvents: [],
  localEvents: [],
  weatherData: null,
  weatherCacheTime: 0,
  currentFilter: 'all',
  searchQuery: ''
};

// Utility functions
function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return {
    iso: dateStr,
    display: d.toLocaleDateString('en-CA', { weekday: 'long', month: 'short', day: 'numeric' }),
    short: d.toLocaleDateString('en-CA', { weekday: 'short', month: 'short', day: 'numeric' })
  };
}

function parseDateTime(dateStr, timeStr) {
  if (!dateStr) return new Date();
  const d = new Date(dateStr + 'T12:00:00');
  
  if (timeStr) {
    const match = timeStr.match(/(\d{1,2}):(\d{2})\s*(AM|PM)?/i);
    if (match) {
      let hours = parseInt(match[1], 10);
      const minutes = parseInt(match[2], 10);
      const meridiem = match[3] ? match[3].toUpperCase() : null;
      if (meridiem === 'PM' && hours < 12) hours += 12;
      if (meridiem === 'AM' && hours === 12) hours = 0;
      d.setHours(hours, minutes, 0, 0);
    }
  }
  return d;
}

// Event rendering functions
function createEventCard(event, container, options = {}) {
  const item = document.createElement('div');
  item.className = `day-event bubble ${options.className || ''}`;
  item.dataset.category = event.category || 'community';
  item.dataset.date = event.date;
  item.dataset.id = event.id;
  
  const copyText = `${event.title}\n${event.time}`;
  
  item.innerHTML = `
    <a class="event-link" href="${event.link || '#'}" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;">
      <span class="title">${event.title}</span>
    </a>
    <span class="time">${event.time}</span>
    <div class="export-row">
      <button class="copy-btn" data-copy="${copyText.replace(/"/g, '&quot;')}">Copy</button>
    </div>
  `;
  
  container.appendChild(item);
}

function createFeaturedCard(event) {
  const copyText = `${event.title}\n${event.time}`;
  return `
    <div class="featured-card bubble" data-category="${event.category || 'community'}">
      <div class="row">
        <div class="badge-row">
          <span class="date-badge">${event.date || event.day || 'TBD'}</span>
          <span class="cat-badge">${event.category || 'community'}</span>
          ${event.promoted ? '<span class="cat-badge" style="background:#f59e0b;color:#fff">Featured</span>' : ''}
        </div>
      </div>
      <a href="${event.link || '#'}" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;display:block;">
        <div class="title">${event.title}</div>
        <div class="meta">${event.time}</div>
      </a>
      <div class="export-row" style="margin-top:8px;">
        <button class="copy-btn" data-copy="${copyText.replace(/"/g, '&quot;')}">Copy</button>
      </div>
    </div>
  `;
}

// Event management
function filterAndSortEvents(events, query, filter) {
  let filtered = [...events];
  
  // Apply date filter
  if (filter && filter !== 'all') {
    filtered = filtered.filter(e => (e.categories || []).includes(filter) || e.category === filter || 
             (e.location || '').toLowerCase().includes(filter.toLowerCase()));
  }
  
  // Apply search query
  if (query) {
    const q = query.toLowerCase();
    filtered = filtered.filter(e => 
      (e.title && e.title.toLowerCase().includes(q)) ||
      (e.description && e.description.toLowerCase().includes(q)) ||
      (e.time && e.time.toLowerCase().includes(q))
    );
  }
  
  return filtered.sort((a, b) => {
    const dateA = new Date(a.date || '9999-99-99');
    const dateB = new Date(b.date || '9999-99-99');
    return dateA - dateB;
  });
}

// Today's events builder
function buildToday() {
  const container = document.getElementById('today-events');
  const label = document.getElementById('today-date-label');
  if (!container || !label) return;
  
  container.innerHTML = '';
  
  const now = new Date();
  const todayStr = now.toISOString().split('T')[0];
  const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  
  if (label) {
    label.textContent = `${monthNames[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()}`;
  }
  
  const todays = APP_STATE.events.filter(ev => ev.date === todayStr);
  
  if (!todays.length) {
    container.innerHTML = '<p class="muted">No events scheduled for today.</p><div class="spacer"></div>';
    return;
  }
  
  todays.forEach(ev => {
    const el = document.createElement('div');
    el.className = 'day-event bubble';
    el.dataset.category = ev.category || 'community';
    const copyText = `${ev.title}\n${ev.time}`;
    el.innerHTML = `
      <a class="event-link" href="${ev.link || '#'}" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;">
        <span class="title" style="font-weight:600">${ev.title}</span>
      </a>
      <span class="time" style="color:#6b7280; font-size:0.85rem">· ${ev.time}</span>
      <div class="export-row">
        <button class="copy-btn" data-copy="${copyText.replace(/"/g, '&quot;')}">Copy</button>
      </div>
    `;
    container.appendChild(el);
  });
}

// Activity week builder (for Activities page - calendar-style with 2 months)
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
    const evDate = new Date(dateStr + 'T12:00:00');
    if (evDate < today) return;
    if (!eventsByDate[dateStr]) eventsByDate[dateStr] = [];
    eventsByDate[dateStr].push(ev);
  };

  // Load events from APP_STATE
  const allEvents = APP_STATE.events || [];
  allEvents.forEach(ev => {
    if (ev.date >= today.toISOString().split('T')[0]) {
      add(ev.date, ev);
    }
  });

  // Add recurring events for current and next month
  const dow = (y, m, d) => new Date(y, m, d).getDay();
  const fmt = (y, m, d) => `${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;

  for (let monthOffset = 0; monthOffset < monthsToShow; monthOffset++) {
    const month = startMonth + monthOffset;
    const yearForMonth = year + Math.floor(month / 12);
    const actualMonth = month % 12;
    const daysInMonth = new Date(yearForMonth, actualMonth + 1, 0).getDate();
    for (let d = 1; d <= daysInMonth; d++) {
      // Weekly writer's group (Tuesday evenings)
      if (dow(yearForMonth, actualMonth, d) === 2) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: "Writer's Group Meetup", time: 'Tue 6:30 PM · Local Library', link: '#' });
      // Monthly market (first Saturday)
      if (d === 1 || d === 8 || d === 15 || d === 22 || d === 29) {
        if (dow(yearForMonth, actualMonth, d) === 6) add(fmt(yearForMonth, actualMonth, d), { category: 'community', title: 'Local Farmers Market', time: 'Sat 8 AM - 1 PM · Town Square', link: '#' });
      }
    }
  }

  const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const sortedDates = Object.keys(eventsByDate).sort();
  if (!sortedDates.length) {
    body.innerHTML = '<div class=\"muted\" style=\"padding:16px;text-align:center;\">No upcoming events found.</div>';
    return;
  }

  body.innerHTML = '';
  sortedDates.forEach(dateStr => {
    const evDate = new Date(dateStr + 'T12:00:00');
    if (!eventsByDate[dateStr] || !eventsByDate[dateStr].length) return;

    const section = document.createElement('div');
    section.className = 'day-section';

    const dateLabel = document.createElement('div');
        dateLabel.className = 'date-header day-header expanded';
        dateLabel.innerHTML = `<span>${days[evDate.getDay()]}, ${monthNames[evDate.getMonth()].slice(0,3)} ${evDate.getDate()}</span><span class="day-toggle"></span>`;
    dateLabel.dataset.expanded = 'true';
    section.appendChild(dateLabel);

    const list = document.createElement('div');
    list.className = 'event-list';
    eventsByDate[dateStr].forEach(ev => {
      const item = document.createElement('div');
      item.className = 'day-event bubble';
      item.dataset.category = ev.category || 'community';
      const copyText = `${ev.title}\n${ev.time}`;
      item.innerHTML = `<a class=\"event-link\" href=\"${ev.link || '#'}\" target=\"_blank\" rel=\"noopener\" style=\"color:inherit;text-decoration:none;\"><span class=\"title\" style=\"font-weight:600\">${ev.title}</span></a><span class=\"time\" style=\"color:#6b7280; font-size:0.85rem\">${ev.time}</span><div class=\"export-row\"><button class=\"copy-btn\" data-copy=\"${copyText.replace(/\"/g, '&quot;')}\">Copy</button></div>`;
      list.appendChild(item);
    });
    section.appendChild(list);
    body.appendChild(section);
  });
}

// Daily events builder with town filter
function buildDailyEvents() {
  const body = document.getElementById('daily-events');
  if (!body) return;
  
  const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const today = new Date();
  today.setHours(0,0,0,0);
  
  // Weekly schedule starts from tomorrow so today's events are not duplicated
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  
  const rangeEnd = new Date(today);
  rangeEnd.setDate(rangeEnd.getDate() + 7);
  
  // Town filter (no search)
  const activeBtn = document.querySelector('.town-btn.active');
  const filter = activeBtn ? activeBtn.dataset.town : 'all';
  
  // Apply town filter - location is in time field
  let filtered = [...APP_STATE.events];
  if (filter !== 'all') {
    filtered = filtered.filter(e => 
      (e.time || '').toLowerCase().includes(filter.toLowerCase()) ||
      (e.location || '').toLowerCase().includes(filter.toLowerCase())
    );
  }
  
  const upcoming = filtered.filter(ev => {
    const d = new Date(ev.date + 'T12:00:00');
    return d >= tomorrow && d <= rangeEnd;
  });
  
  if (!upcoming.length) {
    body.innerHTML = '<div class="muted" style="padding:16px;text-align:center;">No upcoming events found for the rest of this week.</div>';
    return;
  }
  
  const grouped = {};
  upcoming.forEach(ev => {
    if (!grouped[ev.date]) grouped[ev.date] = [];
    grouped[ev.date].push(ev);
  });
  
  body.innerHTML = '';
  
  Object.keys(grouped).sort().forEach(dateStr => {
    const d = new Date(dateStr + 'T12:00:00');
    const section = document.createElement('div');
    section.className = 'day-section';
    
    const dateLabel = document.createElement('div');
    dateLabel.className = 'date-header day-header expanded';
    dateLabel.innerHTML = `<span>${days[d.getDay()]}, ${monthNames[d.getMonth()].slice(0,3)} ${d.getDate()}</span><span class="day-toggle"></span>`;
    dateLabel.dataset.expanded = 'true';
    section.appendChild(dateLabel);
    
    const list = document.createElement('div');
    list.className = 'event-list';
    
    grouped[dateStr].forEach(ev => {
      createEventCard(ev, list);
    });
    
    section.appendChild(list);
    body.appendChild(section);
  });
}

// Featured events builder
function buildFeatured() {
  const container = document.getElementById('featured-events');
  if (!container) return;
  
  const now = new Date();
  const todayStr = now.toISOString().split('T')[0];
  
  let featured = (APP_STATE.config && APP_STATE.config.featured) || [];
  
  // Filter out any past featured events
  featured = featured.filter(ev => {
    if (!ev.date) return true;
    if (/^\d{4}-\d{2}-\d{2}$/.test(ev.date)) return ev.date >= todayStr;
    return true;
  });
  
  // If no configured featured events or all are past, pick top upcoming events
  if (!featured.length && APP_STATE.events && APP_STATE.events.length) {
    const upcoming = APP_STATE.events.filter(ev => (ev.date || '') >= todayStr);
    const promoted = upcoming.filter(ev => ev.promoted || ev.featured);
    featured = promoted.length ? promoted.slice(0, 3) : upcoming.slice(0, 3);
  }
  
  if (!featured.length) {
    container.innerHTML = '<p class="muted">No featured events at this time.</p>';
    return;
  }
  
  container.innerHTML = featured.map(ev => createFeaturedCard(ev)).join('');
}

// Event search handler
function setupSearch() {
  const searchInput = document.getElementById('event-search');
  if (!searchInput) return;
  
  let timeout;
  searchInput.addEventListener('input', (e) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      buildDailyEvents();
    }, 150);
  });
}

// Town filter handlers
function setupTownFilters() {
  document.querySelectorAll('.town-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.town-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      buildDailyEvents();
    });
  });
}

// Weather functions
function weatherLabel(code) {
  const labels = {
    0: 'Clear sky',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Overcast',
    45: 'Foggy',
    48: 'Depositing rime fog',
    51: 'Light drizzle',
    61: 'Light rain',
    80: 'Light rain showers',
    95: 'Thunderstorm'
  };
  return labels[code] || 'Weather';
}

// Weather video and weekly forecast
const WEATHER_VIDEO_SRCS = {
  day: 'weather-media/day.mp4?v=1788408739',
  rain: 'weather-media/rain.mp4?v=1788408739',
  night: 'weather-media/night.mp4?v=1788408739'
};
const WEATHER_FRAME_SRCS = {
  day: 'weather-media/day_frame.jpg',
  rain: 'weather-media/rain_frame.jpg',
  night: 'weather-media/night_frame.jpg'
};

function pickWeatherSrc(code, temp) {
  const hour = new Date().getHours();
  const isNight = hour < 6 || hour >= 20;
  const isPrecip = code !== undefined && code !== null && code >= 51 && code <= 99;
  if (isPrecip) return { video: WEATHER_VIDEO_SRCS.rain, frame: WEATHER_FRAME_SRCS.rain };
  if (isNight) return { video: WEATHER_VIDEO_SRCS.night, frame: WEATHER_FRAME_SRCS.night };
  return { video: WEATHER_VIDEO_SRCS.day, frame: WEATHER_FRAME_SRCS.day };
}

function setWeatherVideo(code, temp) {
  const video = document.getElementById('heroWeatherVideo');
  if (!video) return;
  const { video: src } = pickWeatherSrc(code, temp);
  if (video.src && video.src.includes(src.split('/').pop())) {
    if (video.readyState >= 2 && video.paused) {
      video.play().catch(() => {});
    }
    return;
  }
  video.style.transition = 'opacity 0.6s ease';
  video.style.opacity = '0';
  setTimeout(() => {
    video.src = src;
    video.load();
    video.play().then(() => { video.style.opacity = '1'; })
      .catch(() => { video.style.opacity = '0'; });
  }, 600);
}

function forceWeatherVideo(code, temp) {
  const video = document.getElementById('heroWeatherVideo');
  if (!video) return;
  const { video: src } = pickWeatherSrc(code, temp);
  video.style.transition = 'opacity 0.6s ease';
  video.style.opacity = '0';
  setTimeout(() => {
    video.src = src;
    video.load();
    video.play().then(() => { video.style.opacity = '1'; })
      .catch(() => { video.style.opacity = '0.5'; });
  }, 600);
}

async function loadWeather() {
  const heroCond = document.getElementById('heroCondition');
  const heroTemp = document.getElementById('heroTemp');
  const tempEls = () => document.querySelectorAll('#temp, #temp2, #heroTemp');
  const condEls = () => document.querySelectorAll('#condition, #condition2, #heroCondition');
  const updEls = () => document.querySelectorAll('#updated, #updated2');

  const apply = (temp, cond, upd) => {
    tempEls().forEach(el => { if (el) el.textContent = temp; });
    condEls().forEach(el => { if (el) el.textContent = cond; });
    updEls().forEach(el => { if (el) el.textContent = upd; });
  };

  const fallback = () => {
    apply('--°', 'Weather unavailable', 'Updated: --');
    if (heroCond) heroCond.textContent = 'Weather unavailable';
    forceWeatherVideo(3, 15);
  };

  const fallbackTimer = setTimeout(fallback, 10000);

  try {
    const cached = localStorage.getItem(CONFIG.localCacheKey + '_weather');
    if (cached) {
      try {
        const cachedData = JSON.parse(cached);
        if (Date.now() - cachedData.timestamp < CONFIG.weatherCacheTTL) {
          const cw = cachedData.data.current_weather;
          const { video } = pickWeatherSrc(cw.weathercode, cw.temperature);
          apply(Math.round(cw.temperature) + '°', weatherLabel(cw.weathercode), `Updated: ${new Date(cachedData.timestamp).toLocaleTimeString()}`);
          if (heroCond) heroCond.textContent = weatherLabel(cw.weathercode);
          setWeatherVideo(cw.weathercode, cw.temperature);
          return;
        }
      } catch (e) {}
    }

    const params = new URLSearchParams(CONFIG.weatherApiParams);
    const url = `${CONFIG.weatherApiUrl}?${params}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);

    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    clearTimeout(fallbackTimer);

    const data = await res.json();

    localStorage.setItem(CONFIG.localCacheKey + '_weather', JSON.stringify({
      timestamp: Date.now(),
      data: data
    }));

    const cw = data.current_weather;
    const { video } = pickWeatherSrc(cw.weathercode, cw.temperature);
    apply(Math.round(cw.temperature) + '°', weatherLabel(cw.weathercode), `Updated: ${new Date().toLocaleTimeString()}`);
    if (heroCond) heroCond.textContent = weatherLabel(cw.weathercode);
    setWeatherVideo(cw.weathercode, cw.temperature);

    // Weekly forecast
    if (data.daily) renderWeekly(data.daily);
  } catch (e) {
    clearTimeout(fallbackTimer);
    fallback();
  }
}

function renderWeekly(daily) {
  const container = document.getElementById('weather-forecast');
  if (!container) return;
  if (!daily || !daily.time || !daily.time.length) {
    container.innerHTML = '<div class="muted">Weekly forecast unavailable</div>';
    return;
  }

  const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const count = Math.min(7, daily.time.length);

  container.innerHTML = '';
  const wrap = document.createElement('div');
  wrap.className = 'weekly-wrap';
  container.appendChild(wrap);

  for (let i = 0; i < count; i++) {
    const date = new Date(daily.time[i] + 'T00:00:00');
    const dayName = days[date.getDay()];
    const monthName = months[date.getMonth()];
    const dayNum = date.getDate();
    const maxT = daily.temperature_2m_max ? Math.round(daily.temperature_2m_max[i]) : '--';
    const minT = daily.temperature_2m_min ? Math.round(daily.temperature_2m_min[i]) : '--';
    const condition = weatherLabel(daily.weathercode[i]);
    const precip = daily.precipitation_sum ? daily.precipitation_sum[i].toFixed(1) : '0.0';

    const card = document.createElement('div');
    card.className = 'weekly-day';
    card.innerHTML = `
      <div class="dow">${dayName}</div>
      <div class="date">${monthName} ${dayNum}</div>
      <div class="cond">${condition}</div>
      <div class="lo-hi">${maxT}° / ${minT}°</div>
      <div style="font-size:0.7rem;color:#38bdf8;margin-top:2px;">Precip: ${precip}%</div>
    `;
    wrap.appendChild(card);
  }
}

// Load events from JSON
async function loadEvents() {
  try {
    const response = await fetch('/events.json?v=' + Date.now());
    if (response.ok) {
      const data = await response.json();
      
      // Store config for featured events
      APP_STATE.config = {
        featured: data.featured,
        last_updated: data.last_updated,
        source: data.source
      };
      
      // Load events from JSON
      const jsonEvents = data.events || [];
      
      // Merge with local events (higher priority)
      APP_STATE.events = [...APP_STATE.localEvents, ...jsonEvents];
      APP_STATE.allEvents = [...APP_STATE.localEvents, ...jsonEvents];
      
      // Update last updated display
      if (data.last_updated) {
        const lastUpdEl = document.getElementById('last-updated');
        if (lastUpdEl) {
          const updDate = new Date(data.last_updated);
          lastUpdEl.textContent = `Last updated: ${updDate.toLocaleDateString()} ${updDate.toLocaleTimeString()}`;
        }
      }
      
      return true;
    }
  } catch (e) {
    console.warn('Could not load events.json:', e);
  }
  return false;
}

// Initialize
async function init() {
  try {
    // Load local events first (higher priority)
    const localResponse = await fetch('/local_events.json?v=' + Date.now());
    if (localResponse.ok) {
      const localData = await localResponse.json();
      APP_STATE.localEvents = localData.events || [];
    }
    
    // Load from events.json
    await loadEvents();
    
    // Build UI
    buildFeatured();
    buildToday();
    buildDailyEvents();
    
    // Setup handlers
    setupSearch();
    setupTownFilters();
    await loadWeather();
    
    console.log('App initialized with', APP_STATE.events.length, 'events');
  } catch (e) {
    console.error('Init error:', e);
    document.getElementById('js-error-banner')?.classList.remove('hidden');
  }
}

// Family events renderer
function renderFamilyEvents() {
  const schoolBox = document.getElementById('family-school-events');
  const churchBox = document.getElementById('family-church-events');
  const garageBox = document.getElementById('family-garage-events');
  if (!schoolBox && !churchBox && !garageBox) return;

  const now = new Date();
  const todayStr = now.toISOString().split('T')[0];
  const all = (APP_STATE.events || []).filter(ev => (ev.date || '') >= todayStr);

  const schoolEvents = all.filter(ev => {
    const cat = (ev.category || '').toLowerCase();
    const cats = (ev.categories || []).map(c => c.toLowerCase());
    const title = (ev.title || '').toLowerCase();
    return cat === 'family' || cat === 'education' || cats.includes('family') || cats.includes('education') || title.includes('school') || title.includes('kids') || title.includes('youth') || title.includes('skating');
  });

  const churchEvents = all.filter(ev => {
    const cat = (ev.category || '').toLowerCase();
    const cats = (ev.categories || []).map(c => c.toLowerCase());
    const title = (ev.title || '').toLowerCase();
    return cat === 'faith' || cat === 'church' || cat === 'spiritual' || cats.includes('faith') || cats.includes('church') || title.includes('church') || title.includes('bible') || title.includes('worship') || title.includes('supper') || title.includes('camp');
  });

  const garageEvents = all.filter(ev => {
    const cat = (ev.category || '').toLowerCase();
    const title = (ev.title || '').toLowerCase();
    return cat === 'fundraiser' || cat === 'market' || title.includes('garage') || title.includes('sale') || title.includes('market') || title.includes('fundraiser');
  });

  const renderList = (box, events, emptyText) => {
    if (!box) return;
    if (!events.length) {
      box.innerHTML = `<p class="muted" style="font-size:0.85rem;padding:8px 0;">${emptyText}</p>`;
      return;
    }
    box.innerHTML = '';
    events.slice(0, 6).forEach(ev => {
      createEventCard(ev, box);
    });
  };

  renderList(schoolBox, schoolEvents, 'No upcoming school or youth events scheduled.');
  renderList(churchBox, churchEvents, 'No upcoming church gatherings scheduled.');
  renderList(garageBox, garageEvents, 'No upcoming community sales or fundraisers.');
}

// Copy button handler (handles all copy buttons across pages)
document.addEventListener('click', (ev) => {
  // Day toggle (minimize/expand) for day sections
  const dayHeader = ev.target.closest('.day-header');
  if (dayHeader && !ev.target.closest('.copy-btn')) {
    ev.preventDefault();
    const list = dayHeader.nextElementSibling;
    if (list && list.classList.contains('event-list')) {
      const expanded = dayHeader.classList.toggle('expanded');
      list.classList.toggle('hidden-events', !expanded);
    }
    return;
  }
  
  const copyBtn = ev.target.closest('.copy-btn');
  if (copyBtn) {
    ev.preventDefault();
    ev.stopPropagation();
    const text = copyBtn.dataset.copy || '';
    if (!text) return;
    
    const doFeedback = () => {
      const original = copyBtn.textContent;
      copyBtn.textContent = 'Copied';
      copyBtn.disabled = true;
      setTimeout(() => {
        copyBtn.textContent = original;
        copyBtn.disabled = false;
      }, 1200);
    };

    const fallbackCopy = (str) => {
      try {
        const ta = document.createElement('textarea');
        ta.value = str;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.focus();
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      } catch (e) {}
    };

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(doFeedback).catch(() => {
        fallbackCopy(text);
        doFeedback();
      });
    } else {
      fallbackCopy(text);
      doFeedback();
    }
  }
});

// Navigation
function activatePage(page) {
  try {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-link').forEach(n => n.classList.remove('active'));
    const el = document.getElementById('page-' + page);
    if (el) el.classList.add('active');
    document.querySelectorAll('.nav-link').forEach(l => {
      if (l.dataset.page === page) l.classList.add('active');
    });
    if (page === 'home') { 
      try { buildFeatured(); buildToday(); buildDailyEvents(); } catch (e) {} 
    }
    if (page === 'activities' || page === 'calendar') { try { buildActivityWeek(); } catch (e) {} }
    if (page === 'family') { try { renderFamilyEvents(); } catch (e) {} }
    if (page === 'weather') { loadWeather(); }
  } catch (e) {
    console.error('activatePage error', e);
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
    const el = document.getElementById('page-home');
    if (el) el.classList.add('active');
  }
};

window.addEventListener('hashchange', initPage);

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

// Export functions for debugging
window.pembinaEvents = {
  state: () => APP_STATE,
  refresh: init,
  buildToday,
  buildDailyEvents,
  buildFeatured
};