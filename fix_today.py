from pathlib import Path
import re
text = Path('main.js').read_text(encoding='utf-8', errors='ignore')

new_today = '''  function buildToday() {
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

    const todays = EVENTS.filter(ev => ev.date === todayStr);

    if (!todays.length) {
      container.innerHTML = '<p class="muted">No events scheduled for today.</p>';
      return;
    }

    todays.forEach(ev => {
      const el = document.createElement('a');
      el.className = 'day-event bubble';
      el.href = ev.link || '#';
      el.target = '_blank';
      el.rel = 'noopener';
      el.dataset.category = ev.category;
      el.innerHTML = `<span class="title">${ev.title}</span><span class="time">· ${ev.time}</span><div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, '&quot;')}" data-time="${ev.time.replace(/"/g, '&quot;')}" data-date="${ev.date}">📅 Add to Calendar</button></div><span style="font-size:0.8rem;color:#8ab4f8;"> · <a href="#page-activities" style="color:#8ab4f8;">View calendar</a></span>`;
      container.appendChild(el);
    });
  }'''

# Match from buildToday to the next top-level function or closing brace at same indent
pattern = r'  function buildToday\(\) \{\n.*?\n  function '
match = re.search(pattern, text, re.DOTALL)
if match:
    text = text[:match.start()] + new_today + '\n  function ' + text[match.end():]
    Path('main.js').write_text(text, encoding='utf-8')
    print('replaced buildToday')
else:
    print('buildToday not found')
