from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Replace inline onclick handlers with data attributes and a global click handler
# This avoids all the string escaping issues

# 1) Replace buildWeek export buttons
old_week = """        const dateStr = d.toISOString().split('T')[0];
        const gcalWeek = addGoogleCalendarLink(ev.title, ev.time, dateStr);
        const safeTitle = ev.title.replace(/'/g, '\\\\''');
        const safeTime = ev.time.replace(/'/g, '\\\\''');
        el.innerHTML = `<div class="title">${ev.title}</div><div class="time">${ev.time}</div><div class="export-row"><button class="export-btn" onclick="downloadICS('${safeTitle}','${safeTime}','${dateStr}')">ICS</button><a class="export-btn" href="${gcalWeek}" target="_blank">Google</a></div>`;"""

new_week = """        const dateStr = d.toISOString().split('T')[0];
        const gcalWeek = addGoogleCalendarLink(ev.title, ev.time, dateStr);
        el.innerHTML = `<div class="title">${ev.title}</div><div class="time">${ev.time}</div><div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, '&quot;')}" data-time="${ev.time.replace(/"/g, '&quot;')}" data-date="${dateStr}">ICS</button><a class="export-btn" href="${gcalWeek}" target="_blank">Google</a></div>`;"""

if old_week in text:
    text = text.replace(old_week, new_week, 1)
    print('Patched buildWeek export buttons')
else:
    print('buildWeek not found')

# 2) Replace buildActivityWeek export buttons
old_act = """          const actDate = section ? section.dataset.date || '' : '';
          const gcalAct = addGoogleCalendarLink(ev.title, ev.time, actDate);
          const safeTitle2 = ev.title.replace(/'/g, '\\\\''');
          const safeTime2 = ev.time.replace(/'/g, '\\\\''');
          item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div><div class="export-row"><button class="export-btn" onclick="downloadICS('${safeTitle2}','${safeTime2}','${actDate}')">ICS</button><a class="export-btn" href="${gcalAct}" target="_blank">Google</a></div>`;"""

new_act = """          const actDate = section ? section.dataset.date || '' : '';
          const gcalAct = addGoogleCalendarLink(ev.title, ev.time, actDate);
          item.innerHTML = `<div class="title" style="font-weight:600">${ev.title}</div><div class="time" style="color:#6b7280; font-size:0.85rem">${ev.time}</div><div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, '&quot;')}" data-time="${ev.time.replace(/"/g, '&quot;')}" data-date="${actDate}">ICS</button><a class="export-btn" href="${gcalAct}" target="_blank">Google</a></div>`;"""

if old_act in text:
    text = text.replace(old_act, new_act, 1)
    print('Patched buildActivityWeek export buttons')
else:
    print('buildActivityWeek not found')

# 3) Replace renderFeatured export buttons
old_feat = """      <div class="export-row"><a class="export-btn" href="${addGoogleCalendarLink(ev.title, ev.time, '')}" target="_blank">Google Calendar</a></div>"""
new_feat = """      <div class="export-row"><a class="export-btn" href="${addGoogleCalendarLink(ev.title, ev.time, '')}" target="_blank">Google Calendar</a></div>"""

if old_feat in text:
    text = text.replace(old_feat, new_feat, 1)
    print('Kept renderFeatured export button')
else:
    print('renderFeatured not found')

# 4) Replace renderFamilyEvents export buttons
old_fam = """      <div class="export-row"><button class="export-btn" onclick="downloadICS('${safeFamTitle}','${safeFamTime}','')">ICS</button><a class="export-btn" href="${gcalFam}" target="_blank">Google</a></div>"""
new_fam = """      <div class="export-row"><button class="export-btn" data-export="ics" data-title="${ev.title.replace(/"/g, '&quot;')}" data-time="${(ev.time + ' · ' + ev.date).replace(/"/g, '&quot;')}" data-date="">ICS</button><a class="export-btn" href="${gcalFam}" target="_blank">Google</a></div>"""

if old_fam in text:
    text = text.replace(old_fam, new_fam, 1)
    print('Patched renderFamilyEvents export buttons')
else:
    print('renderFamilyEvents not found')

# 5) Add global click handler for export buttons
old_handler = """  document.querySelectorAll('.nav-link').forEach(link => {"""
new_handler = """  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-export="ics"]');
    if (!btn) return;
    e.preventDefault();
    downloadICS(btn.dataset.title || '', btn.dataset.time || '', btn.dataset.date || '');
  });

  document.querySelectorAll('.nav-link').forEach(link => {"""

if old_handler in text and 'data-export="ics"' not in text.split(old_handler)[0]:
    text = text.replace(old_handler, new_handler, 1)
    print('Added global ICS click handler')
else:
    print('nav handler not found or already added')

p.write_text(text, encoding='utf-8')
print('Done')
