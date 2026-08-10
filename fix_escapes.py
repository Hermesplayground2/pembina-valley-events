from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Replace the broken safeTitle/safeTime lines with clean escapes
# Broken: const safeTitle = ev.title.replace(/'/g, '\\\\'');  // 4 literal backslashes
# Fixed:   const safeTitle = ev.title.replace(/'/g, '\\'');   // 2 literal backslashes
replacements = [
    ("const safeTitle = ev.title.replace(/'/g, '\\\\'');",
     "const safeTitle = ev.title.replace(/'/g, '\\\\'');"),
    ("const safeTime = ev.time.replace(/'/g, '\\\\'');",
     "const safeTime = ev.time.replace(/'/g, '\\\\'');"),
    ("const safeTitle2 = ev.title.replace(/'/g, '\\\\'');",
     "const safeTitle2 = ev.title.replace(/'/g, '\\\\'');"),
    ("const safeTime2 = ev.time.replace(/'/g, '\\\\'');",
     "const safeTime2 = ev.time.replace(/'/g, '\\\\'');"),
    ("const safeFamTitle = ev.title.replace(/'/g, '\\\\'');",
     "const safeFamTitle = ev.title.replace(/'/g, '\\\\'');"),
    ("const safeFamTime = (ev.time + ' · ' + ev.date).replace(/'/g, '\\\\'');",
     "const safeFamTime = (ev.time + ' · ' + ev.date).replace(/'/g, '\\\\'');"),
]

changed = 0
for old, new in replacements:
    if old in text:
        text = text.replace(old, new, 1)
        changed += 1

p.write_text(text, encoding='utf-8')
print('Fixed', changed, 'escape sequences')
