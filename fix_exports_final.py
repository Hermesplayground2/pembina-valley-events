from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
lines = p.read_text(encoding='utf-8').splitlines()

# Fix 1: buildWeek - replace lines 888-890 with clean Google-only export row
lines[887] = '        el.innerHTML = `<div class="title">${ev.title}</div><div class="time">${ev.time}</div><div class="export-row"><a class="export-btn" href="${gcalWeek}" target="_blank">Google</a></div>`;'
del lines[888]  # safeTime
del lines[888]  # safeTitle

# Fix 2: buildActivityWeek - replace lines 980-982 with clean Google-only export row
lines[978] = '          item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div><div class="export-row"><a class="export-btn" href="${gcalAct}" target="_blank">Google</a></div>`;'
del lines[979]  # safeTime2
del lines[979]  # safeTitle2

# Fix 3: renderFamilyEvents - remove safeFamTitle/safeFamTime and fix export row
lines[1282] = '      return `'
lines[1283] = '      <div class="day-event" data-category="${ev.category}">'
lines[1288] = '        <div class="export-row"><a class="export-btn" href="${gcalFam}" target="_blank">Google</a></div>'

p.write_text('\n'.join(lines), encoding='utf-8')
print('Fixed all broken export buttons')
