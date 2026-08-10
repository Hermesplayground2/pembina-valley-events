from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# 1) buildActivityWeek ICS
old = '          item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div>`;'
new = '          item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div><div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, \'&quot;\')}" data-time="${ev.time.replace(/"/g, \'&quot;\')}" data-date="">ICS</button></div>`;'
if old in text and 'export-row' not in text.split('function buildActivityWeek()')[1]:
    text = text.replace(old, new, 1)
    print('Patched buildActivityWeek ICS')
else:
    print('buildActivityWeek skipped')

# 2) renderFamilyEvents ICS
old = '        <div class="time">${ev.time}</div>\n      </a>'
new = '        <div class="time">${ev.time}</div>\n        <div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, \'&quot;\')}" data-time="${ev.time.replace(/"/g, \'&quot;\')}" data-date="">ICS</button></div>\n      </a>'
if old in text and 'export-row' not in text.split('function renderFamilyEvents()')[1]:
    text = text.replace(old, new, 1)
    print('Patched renderFamilyEvents ICS')
else:
    print('renderFamilyEvents skipped')

# 3) Global delegated click handler for ICS buttons
handler = "  document.addEventListener('click', (ev) => {\n    const btn = ev.target.closest('[data-export=\"ics\"]');\n    if (!btn) return;\n    ev.preventDefault();\n    downloadICS(btn.dataset.title || '', btn.dataset.time || '', btn.dataset.date || '');\n  });\n</script>"
if "data-export=\"ics\"" in text and "closest('[data-export=\"ics\"]')" not in text:
    text = text.replace('</script>', handler, 1)
    print('Added global ICS handler')

p.write_text(text, encoding='utf-8')
print('Done')
