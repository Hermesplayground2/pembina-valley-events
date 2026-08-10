from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# 1) Add downloadICS helper before first function in script
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
if 'function downloadICS' not in text:
    text = text.replace('<script>\n', '<script>\n' + helper, 1)
    print('Added downloadICS helper')

# 2) buildWeek ICS
old = '        el.innerHTML = `<span class="title">${ev.title}</span><span class="time">${ev.time}</span>`;'
new = '        el.innerHTML = `<span class="title">${ev.title}</span><span class="time">${ev.time}</span><div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, \'&quot;\')}" data-time="${ev.time.replace(/"/g, \'&quot;\')}" data-date="">ICS</button></div>`;'
if old in text and 'data-export="ics"' not in text.split('function buildWeek()')[1]:
    text = text.replace(old, new, 1)
    print('Patched buildWeek')

# 3) buildActivityWeek ICS
old = '          item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div>`;'
new = '          item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div><div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, \'&quot;\')}" data-time="${ev.time.replace(/"/g, \'&quot;\')}" data-date="">ICS</button></div>`;'
if old in text and 'data-export="ics"' not in text.split('function buildActivityWeek()')[1]:
    text = text.replace(old, new, 1)
    print('Patched buildActivityWeek')

# 4) renderFamilyEvents ICS
old = '        <div class="time">${ev.time}</div>\n      </a>'
new = '        <div class="time">${ev.time}</div>\n        <div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, \'&quot;\')}" data-time="${ev.time.replace(/"/g, \'&quot;\')}" data-date="">ICS</button></div>\n      </a>'
if old in text and 'data-export="ics"' not in text.split('function renderFamilyEvents()')[1]:
    text = text.replace(old, new, 1)
    print('Patched renderFamilyEvents')

# 5) Global delegated handler
if 'closest(\'[data-export="ics"]\')' not in text:
    text = text.replace(
        '</script>',
        "  document.addEventListener('click', (ev) => {\n    const btn = ev.target.closest('[data-export=\"ics\"]');\n    if (!btn) return;\n    ev.preventDefault();\n    downloadICS(btn.dataset.title || '', btn.dataset.time || '', btn.dataset.date || '');\n  });\n</script>",
        1
    )
    print('Added global ICS handler')

p.write_text(text, encoding='utf-8')
print('Done')
