from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')
lines = text.splitlines()

# Fix 1: remove the extra } before renderFeatured
for i, line in enumerate(lines):
    if line.strip() == '}' and i + 1 < len(lines) and 'function renderFeatured' in lines[i + 1]:
        print('Removing extra } at line', i + 1)
        del lines[i]
        break

# Fix 2: remove duplicate day-event line in renderFamilyEvents
for i, line in enumerate(lines):
    if '<div class="day-event" data-category="${ev.category}">' in line:
        if i + 1 < len(lines) and '<div class="day-event" data-category="${ev.category}">' in lines[i + 1]:
            print('Removing duplicate day-event at line', i + 1)
            del lines[i + 1]
            break

# Fix 3: remove duplicate export-row line
for i, line in enumerate(lines):
    if '<div class="export-row"><a class="export-btn" href="${gcalFam}" target="_blank">Google</a></div>' in line:
        if i + 1 < len(lines) and '<div class="export-row"><a class="export-btn" href="${gcalFam}" target="_blank">Google</a></div>' in lines[i + 1]:
            print('Removing duplicate export-row at line', i + 1)
            del lines[i + 1]
            break

p.write_text('\n'.join(lines), encoding='utf-8')
print('Done')
