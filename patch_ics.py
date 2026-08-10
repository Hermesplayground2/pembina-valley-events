from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Patch buildActivityWeek
old = '          item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div>`;'
new = '          item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div><div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, \'&quot;\')}" data-time="${ev.time.replace(/"/g, \'&quot;\')}" data-date="">ICS</button></div>`;'
if old in text and 'export-row' not in text.split('function buildActivityWeek()')[1]:
    text = text.replace(old, new, 1)
    print('Patched buildActivityWeek')
else:
    print('buildActivityWeek skip')

# Patch renderFamilyEvents
old = '        <div class="time">${ev.time}</div>\n      </a>'
new = '        <div class="time">${ev.time}</div>\n        <div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, \'&quot;\')}" data-time="${ev.time.replace(/"/g, \'&quot;\')}" data-date="">ICS</button></div>\n      </a>'
if old in text and 'export-row' not in text.split('function renderFamilyEvents()')[1]:
    text = text.replace(old, new, 1)
    print('Patched renderFamilyEvents')
else:
    print('renderFamilyEvents skip')

# Global delegated click handler
if 'closest(\'[data-export="ics"]\')' not in text:
    text = text.replace(
        '</script>',
        "  document.addEventListener('click', (ev) => {\n    const btn = ev.target.closest('[data-export=\"ics\"]');\n    if (!btn) return;\n    ev.preventDefault();\n    downloadICS(btn.dataset.title || '', btn.dataset.time || '', btn.dataset.date || '');\n  });\n</script>",
        1
    )
    print('Added global handler')

p.write_text(text, encoding='utf-8')
print('Done')
