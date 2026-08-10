from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Remove the broken export button HTML that uses safeTitle/safeTime
# and replace with just the Google link to avoid JS syntax errors

# Pattern 1: buildWeek - remove the export-row entirely or keep only Google
old1 = '''        const safeTitle = ev.title.replace(/'/g, '''');
        const safeTime = ev.time.replace(/'/g, '''');
        el.innerHTML = `<div class="title">${ev.title}</div><div class="time">${ev.time}</div><div class="export-row"><button class="export-btn" onclick="downloadICS('${safeTitle}','${safeTime}','${dateStr}')">ICS</button><a class="export-btn" href="${gcalWeek}" target="_blank">Google</a></div>`;'''
new1 = '''        el.innerHTML = `<div class="title">${ev.title}</div><div class="time">${ev.time}</div><div class="export-row"><a class="export-btn" href="${gcalWeek}" target="_blank">Google</a></div>`;'''

if old1 in text:
    text = text.replace(old1, new1, 1)
    print('Fixed buildWeek export buttons')
else:
    print('buildWeek pattern not found')

# Pattern 2: buildActivityWeek - same fix
old2 = '''          const safeTitle2 = ev.title.replace(/'/g, '''');
          const safeTime2 = ev.time.replace(/'/g, '''');
          item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div><div class="export-row"><button class="export-btn" onclick="downloadICS('${safeTitle2}','${safeTime2}','${actDate}')">ICS</button><a class="export-btn" href="${gcalAct}" target="_blank">Google</a></div>`;'''
new2 = '''          item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div><div class="export-row"><a class="export-btn" href="${gcalAct}" target="_blank">Google</a></div>`;'''

if old2 in text:
    text = text.replace(old2, new2, 1)
    print('Fixed buildActivityWeek export buttons')
else:
    print('buildActivityWeek pattern not found')

# Pattern 3: renderFamilyEvents - same fix
old3 = '''      const safeFamTitle = ev.title.replace(/'/g, '''');
      const safeFamTime = (ev.time + ' · ' + ev.date).replace(/'/g, '''');
      return `
      <div class="day-event" data-category="${ev.category}">
        <div class="title">${ev.title}</div>'''
new3 = '''      return `
      <div class="day-event" data-category="${ev.category}">
        <div class="title">${ev.title}</div>'''

if old3 in text:
    text = text.replace(old3, new3, 1)
    print('Fixed renderFamilyEvents export buttons')
else:
    print('renderFamilyEvents pattern not found')

# Also remove the broken onclick from family events HTML
old_fam_html = '''      <div class="export-row"><button class="export-btn" onclick="downloadICS('${safeFamTitle}','${safeFamTime}','')">ICS</button><a class="export-btn" href="${gcalFam}" target="_blank">Google</a></div>'''
new_fam_html = '''      <div class="export-row"><a class="export-btn" href="${gcalFam}" target="_blank">Google</a></div>'''

if old_fam_html in text:
    text = text.replace(old_fam_html, new_fam_html, 1)
    print('Fixed family event export HTML')
else:
    print('family export HTML not found')

p.write_text(text, encoding='utf-8')
print('Done')
