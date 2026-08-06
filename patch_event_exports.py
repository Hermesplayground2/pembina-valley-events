import pathlib

p = pathlib.Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Find and patch buildWeek day-event block
marker = "el.innerHTML = `<div class=\"title\">${ev.title}</div><div class=\"time\">${ev.time}</div>`;"
if marker in text and 'export-row' not in text.split(marker)[0]:
    replacement = (
        "const dateStr = d.toISOString().split('T')[0];\n"
        "        const gcalWeek = addGoogleCalendarLink(ev.title, ev.time, dateStr);\n"
        "        el.innerHTML = `<div class=\\\"title\\\">${ev.title}</div><div class=\\\"time\\\">${ev.time}</div><div class=\\\"export-row\\\"><button class=\\\"export-btn\\\" onclick=\\\"downloadICS('${ev.title.replace(/'/g, '\\\\'')}','${ev.time.replace(/'/g, '\\\\'')}','${dateStr}')\\\">ICS</button><a class=\\\"export-btn\\\" href=\\\"${gcalWeek}\\\" target=\\\"_blank\\\">Google</a></div>`;"
    )
    text = text.replace(marker, replacement, 1)
    print('Patched buildWeek export buttons')
else:
    print('buildWeek anchor not found or already patched')

# Find and patch buildActivityWeek item block
marker2 = 'item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div>`;'
if marker2 in text and 'export-row' not in text.split(marker2)[0]:
    replacement2 = (
        "const actDate = section ? section.dataset.date || '' : '';\n"
        "          const gcalAct = addGoogleCalendarLink(ev.title, ev.time, actDate);\n"
        "          item.innerHTML = `<div class=\\\"title\\\" style=\\\"font-weight:600\\\">${ev.title}</div><div class=\\\"time\\\" style=\\\"color:#6b7280; font-size:0.85rem\\\">${ev.time}</div><div class=\\\"export-row\\\"><button class=\\\"export-btn\\\" onclick=\\\"downloadICS('${ev.title.replace(/'/g, '\\\\'')}','${ev.time.replace(/'/g, '\\\\'')}','${actDate}')\\\">ICS</button><a class=\\\"export-btn\\\" href=\\\"${gcalAct}\\\" target=\\\"_blank\\\">Google</a></div>`;"
    )
    text = text.replace(marker2, replacement2, 1)
    print('Patched buildActivityWeek export buttons')
else:
    print('buildActivityWeek anchor not found or already patched')

p.write_text(text, encoding='utf-8')
print('Done')
