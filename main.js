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
  return `
    <a class="featured-card bubble" href="${event.link || '#'}" target="_blank" rel="noopener" data-category="${event.category}">
      <div class="row">
        <div class="badge-row">
          <span class="date-badge">${event.date || event.day || 'TBD'}</span>
          <span class="cat-badge">${event.category || 'community'}</span>
          ${event.promoted ? '<span class="cat-badge" style="background:#f59e0b;color:#fff">Featured</span>' : ''}
        </div>
      </div>
      <div class="title">${event.title}</div>
      <div class="meta">${event.time}</div>
      <button class="copy-btn" data-copy="${`${event.title}\n${event.time}`.replace(/"/g, '&quot;')}">Copy</button>
    </a>
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
    const el = document.createElement('a');
    el.className = 'day-event bubble';
    el.href = ev.link || '#';
    el.target = '_blank';
    el.rel = 'noopener';
    el.dataset.category = ev.category;
    const copyText = `${ev.title}\n${ev.time}`;
    el.innerHTML = `
      <span class="title">${ev.title}</span>
      <span class="time">· ${ev.time}</span>
      <div class="export-row">
        <button class="copy-btn" data-copy="${copyText.replace(/"/g, '&quot;')}">Copy</button>
      </div>
    `;
    container.appendChild(el);
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
    return d >= today && d <= rangeEnd;
  });
  
  if (!upcoming.length) {
    body.innerHTML = '<div class="muted" style="padding:16px;text-align:center;">No upcoming events found.</div>';
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
    dateLabel.className = 'date-label';
    dateLabel.textContent = `${days[d.getDay()]}, ${monthNames[d.getMonth()].slice(0,3)} ${d.getDate()}`;
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
  
  // Use featured from events.json or fall back to hardcoded
  const featured = (APP_STATE.config && APP_STATE.config.featured) || [
    { title: 'Pembina Valley Ribfest', date: 'Sep 11-13', time: 'Winkler', category: 'community', link: 'https://pembinavalleyonline.com/', featured: true },
    { title: 'Morden POP CULTURE EXPO', date: 'Sep 19-20', time: 'Access Event Centre, Morden', category: 'community', link: 'https://pembinavalleyonline.com/events/227194' }
  ];
  
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

async function loadWeather() {
  const heroCond = document.getElementById('heroCondition');
  const tempEls = () => document.querySelectorAll('#temp, #temp2, #heroTemp');
  const condEls = () => document.querySelectorAll('#condition, #condition2, #heroCondition');
  const updEls = () => document.querySelectorAll('#updated, #updated2');
  
  const apply = (temp, cond, loc, upd) => {
    tempEls().forEach(el => el.textContent = temp);
    condEls().forEach(el => el.textContent = cond);
    updEls().forEach(el => el.textContent = loc);
    if (upd) {
      updEls().forEach(el => el.textContent = `Updated: ${upd}`);
    }
  };
  
  // Check cache first
  const cached = localStorage.getItem(CONFIG.localCacheKey + '_weather');
  if (cached) {
    try {
      const cachedData = JSON.parse(cached);
      if (Date.now() - cachedData.timestamp < CONFIG.weatherCacheTTL) {
        const cw = cachedData.data.current_weather;
        apply(Math.round(cw.temperature) + '°', weatherLabel(cw.weathercode), 'Pembina, MB', new Date(cachedData.timestamp).toLocaleTimeString());
        return;
      }
    } catch (e) {}
  }
  
  const fallback = () => {
    apply('--°', 'Weather unavailable', 'Pembina, MB', '');
    if (heroCond) heroCond.textContent = 'Weather unavailable';
  };
  
  const fallbackTimer = setTimeout(fallback, 5000);
  
  try {
    const params = new URLSearchParams(CONFIG.weatherApiParams);
    const url = `${CONFIG.weatherApiUrl}?${params}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);
    
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    clearTimeout(fallbackTimer);
    
    const data = await res.json();
    
    // Cache successful response
    localStorage.setItem(CONFIG.localCacheKey + '_weather', JSON.stringify({
      timestamp: Date.now(),
      data: data
    }));
    
    const cw = data.current_weather;
    apply(Math.round(cw.temperature) + '°', weatherLabel(cw.weathercode), 'Pembina, MB', new Date().toLocaleTimeString());
  } catch (e) {
    clearTimeout(fallbackTimer);
    fallback();
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

// Copy button handler (handles all copy buttons across pages)
document.addEventListener('click', (ev) => {
  const copyBtn = ev.target.closest('.copy-btn');
  if (copyBtn) {
    ev.preventDefault();
    const text = copyBtn.dataset.copy || '';
    if (!text) return;
    
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
    
    const original = copyBtn.textContent;
    copyBtn.textContent = 'Copied';
    copyBtn.disabled = true;
    setTimeout(() => {
      copyBtn.textContent = original;
      copyBtn.disabled = false;
    }, 1200);
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
    if (page === 'home') { try { buildFeatured(); } catch (e) {} }
    try { buildToday(); } catch (e) {}
    if (page === 'activities' || page === 'calendar') { try { buildDailyEvents(); } catch (e) {} }
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