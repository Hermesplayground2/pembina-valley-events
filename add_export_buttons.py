import pathlib

p = pathlib.Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# 1) buildWeek day-event export buttons
old1 = 'el.innerHTML = `<div class="title">${ev.title}</div><div class="time">${ev.time}</div>`;'
new1 = ("const gcalWeek = addGoogleCalendarLink(ev.title, ev.time, d.toISOString().split('T')[0]);\n"
        "        el.innerHTML = `<div class=\"title\">${ev.title}</div><div class=\"time\">${ev.time}</div><div class=\"export-row\"><button class=\"export-btn\" onclick=\"downloadICS('${ev.title.replace(/'/g, '\\'')}','${ev.time.replace(/'/g, '\\'')}','${d.toISOString().split('T')[0]}')\">ICS</button><a class=\"export-btn\" href=\"${gcalWeek}\" target=\"_blank\">Google</a></div>`;")
if old1 in text and 'export-row' not in text.split(old1)[0]:
    text = text.replace(old1, new1, 1)
    print('Patched buildWeek export buttons')
else:
    print('buildWeek anchor not found or already patched')

# 2) buildActivityWeek day-event export buttons
old2 = 'item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div>`;'
new2 = ("const dateStr = section ? section.dataset.date || '' : '';\n"
        "          const gcalAct = addGoogleCalendarLink(ev.title, ev.time, dateStr);\n"
        "          item.innerHTML = `<div class=\"title\" style=\"font-weight:600\">${ev.title}</div><div class=\"time\" style=\"color:#6b7280; font-size:0.85rem\">${ev.time}</div><div class=\"export-row\"><button class=\"export-btn\" onclick=\"downloadICS('${ev.title.replace(/'/g, '\\'')}','${ev.time.replace(/'/g, '\\'')}','${dateStr}')\">ICS</button><a class=\"export-btn\" href=\"${gcalAct}\" target=\"_blank\">Google</a></div>`;")
if old2 in text and 'export-row' not in text.split(old2)[0]:
    text = text.replace(old2, new2, 1)
    print('Patched buildActivityWeek export buttons')
else:
    print('buildActivityWeek anchor not found or already patched')

# 3) renderFeatured export buttons
old3 = '<div class="meta">${ev.time}</div>'
new3 = '<div class="meta">${ev.time}</div><div class="export-row"><a class="export-btn" href="${gcalFeat}" target="_blank">Google Calendar</a></div>'
if old3 in text and 'gcalFeat' not in text:
    text = text.replace(old3, new3, 1)
    print('Patched renderFeatured export button')
else:
    print('renderFeatured export anchor not found or already patched')

# 4) renderFamilyEvents export buttons
old4 = '<div class="event-meta">${ev.time}</div>'
new4 = '<div class="event-meta">${ev.time}</div><div class="export-row"><button class="export-btn" onclick="downloadICS(\'${ev.title.replace(/\'/g, "\\\\\'")}\',\'${ev.time.replace(/\'/g, "\\\\\'")}\',\'\')">ICS</button><a class="export-btn" href="${gcalFam}" target="_blank">Google</a></div>'
if old4 in text and 'export-row' not in text.split(old4)[0]:
    text = text.replace(old4, new4, 1)
    print('Patched renderFamilyEvents export buttons')
else:
    print('renderFamilyEvents export anchor not found or already patched')

# 5) Add dataset.date for activity sections
old5 = 'section.innerHTML = `<div class="name"'
new5 = "section.dataset.date = dateStr;\n      section.innerHTML = `<div class=\"name\""
if old5 in text and 'section.dataset.date' not in text:
    text = text.replace(old5, new5, 1)
    print('Added activity section dataset.date')
else:
    print('Activity section anchor not found or already patched')

p.write_text(text, encoding='utf-8')
print('Done')
