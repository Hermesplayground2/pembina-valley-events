from pathlib import Path
import re
text = Path('main.js').read_text(encoding='utf-8', errors='ignore')

new_upcoming = '''  function buildUpcoming() {
    const body = document.getElementById('daily-events');
    if (!body) return;
    body.innerHTML = '';

    const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    const today = new Date();
    today.setHours(0,0,0,0);
    const rangeEnd = new Date(today);
    rangeEnd.setDate(rangeEnd.getDate() + 7);

    const upcoming = EVENTS.filter(ev => {
      const d = new Date(ev.date + 'T12:00:00');
      return d >= today && d <= rangeEnd;
    }).sort((a, b) => a.date.localeCompare(b.date) || a.time.localeCompare(b.time));

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
      dateLabel.className = 'date-label';
      dateLabel.textContent = days[d.getDay()] + ', ' + monthNames[d.getMonth()].slice(0,3) + ' ' + d.getDate();
      section.appendChild(dateLabel);

      const list = document.createElement('div');
      list.className = 'event-list';
      grouped[dateStr].forEach(ev => {
        const item = document.createElement('div');
        item.className = 'day-event bubble';
        item.dataset.category = ev.category;
        const copyText = (ev.title + '\\n' + ev.time).trim();
        item.innerHTML = '<a class="event-link" href="' + ev.link + '" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;"><span class="title">' + ev.title + '</span></a><span class="time">' + ev.time + '</span><button class="copy-btn" data-copy="' + copyText.replace(/"/g, '&quot;') + '">Copy</button>';
        list.appendChild(item);
      });
      section.appendChild(list);
      body.appendChild(section);
    });

    if (!upcoming.length) {
      body.innerHTML = '<div class="muted" style="padding:10px;">No upcoming events in the next 7 days.</div>';
    }
  }'''

# Find the buildUpcoming function and replace it
# Match from "function buildUpcoming() {" to the next "  function ..." at same indent
pattern = r'  function buildUpcoming\(\) \{\n.*?\n  function '
match = re.search(pattern, text, re.DOTALL)
if match:
    text = text[:match.start()] + new_upcoming + '\n  function ' + text[match.end():]
    Path('main.js').write_text(text, encoding='utf-8')
    print('replaced buildUpcoming')
else:
    print('buildUpcoming not found')
