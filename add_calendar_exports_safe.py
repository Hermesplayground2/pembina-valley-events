from pathlib import Path
import re

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')
if 'downloadICS' in text:
    print('ICS helper already present')
else:
    helper = """function downloadICS(title, time, date) {
      const dt = date ? new Date(date + 'T12:00:00') : new Date();
      const pad = (n) => String(n).padStart(2, '0');
      const dtStr = dt.getFullYear() + pad(dt.getMonth()+1) + pad(dt.getDate()) + 'T120000Z';
      const ics = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'BEGIN:VEVENT',
        'DTSTART;VALUE=DATE:' + dtStr,
        'DTEND;VALUE=DATE:' + dtStr,
        'SUMMARY:' + (title || 'Event'),
        'DESCRIPTION:' + (time || ''),
        'END:VEVENT',
        'END:VCALENDAR'
      ].join('\\n');
      const blob = new Blob([ics], { type: 'text/calendar' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = (title || 'event').replace(/[^a-z0-9]+/gi, '_') + '.ics';
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    }

"""
    text = text.replace('<script>\n', '<script>\n' + helper, 1)
    print('Added downloadICS helper')

# BuildWeek ICS
old = "        el.innerHTML = `<span class=\"title\">${ev.title}</span><span class=\"time\">${ev.time}</span>`;"
new = "        el.innerHTML = `<span class=\"title\">${ev.title}</span><span class=\"time\">${ev.time}</span><div class=\"export-row\"><button class=\"export-btn\" data-export=\"ics\" data-title=\"${ev.title.replace(/\"/g, '&quot;')}\" data-time=\"${ev.time.replace(/\"/g, '&quot;')}\" data-date=\"\">ICS</button></div>`;"
if old in text:
    text = text.replace(old, new)
    print('Patched buildWeek ICS')

# buildActivityWeek ICS
old = "          item.innerHTML = `<div class=\"title\" style=\"font-weight:600\">${ev.title}</div><div class=\"time\" style=\"color:#6b7280; font-size:0.85rem\">${ev.time}</div>`
          col.appendChild(item);"
new = "          item.innerHTML = `<div class=\"title\" style=\"font-weight:600\">${ev.title}</div><div class=\"time\" style=\"color:#6b7280; font-size:0.85rem\">${ev.time}</div><div class=\"export-row\"><button class=\"export-btn\" data-export=\"ics\" data-title=\"${ev.title.replace(/\"/g, '&quot;')}\" data-time=\"${ev.time.replace(/\"/g, '&quot;')}\" data-date=\"\">ICS</button></div>`
          col.appendChild(item);"
if old in text:
    text = text.replace(old, new)
    print('Patched buildActivityWeek ICS')
else:
    print('buildActivityWeek pattern not found')

# renderFamilyEvents ICS
old = """      return `
      <a class="day-event bubble" href="${link}" target="_blank" rel="noopener">
        <div class="title">${ev.title}</div>
        <div class="time">${ev.time}</div>
      </a>
    `;"""
new = """      return `
      <a class="day-event bubble" href="${link}" target="_blank" rel="noopener">
        <div class="title">${ev.title}</div>
        <div class="time">${ev.time}</div>
        <div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, '&quot;')}" data-time="${ev.time.replace(/"/g, '&quot;')}" data-date="">ICS</button></div>
      </a>
    `;"""
if old in text:
    text = text.replace(old, new)
    print('Patched renderFamilyEvents ICS')

# Global delegated ICS click handler if missing
if 'data-export="ics"' in text and 'closest(\'[data-export="ics"]\')' not in text:
    text = text.replace('</script>', "  document.addEventListener('click', (ev) => {\n    const btn = ev.target.closest('[data-export=\"ics\"]');\n    if (!btn) return;\n    ev.preventDefault();\n    downloadICS(btn.dataset.title || '', btn.dataset.time || '', btn.dataset.date || '');\n  });\n</script>", 1)
    print('Added global ICS handler')

p.write_text(text, encoding='utf-8')
print('Done')
