from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')
idx = text.find('function buildActivityWeek()')
snippet = text[idx:idx+2600]
for marker in ['item.innerHTML', 'col.appendChild', 'title>${ev.title}', 'time>${ev.time}']:
    if marker in snippet:
        print('buildActivityWeek has:', marker)
idx2 = text.find('function renderFamilyEvents()')
snippet2 = text[idx2:idx2+1800]
for marker in ['title>${ev.title}', 'time>${ev.time}', 'export-row']:
    if marker in snippet2:
        print('renderFamilyEvents has:', marker)
