from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
lines = p.read_text(encoding='utf-8').splitlines()

# Remove remaining safeTitle2 line at 978 (0-indexed 977)
if 'safeTitle2' in lines[977]:
    del lines[977]
    print('Removed safeTitle2 line')

# Remove safeFamTitle line - find it dynamically
for i, line in enumerate(lines):
    if 'const safeFamTitle = ev.title.replace' in line:
        del lines[i]
        print(f'Removed safeFamTitle at line {i+1}')
        break

# Fix the remaining onclick downloadICS in family events
for i, line in enumerate(lines):
    if 'onclick="downloadICS' in line and 'safeFamTitle' in line:
        lines[i] = '        <div class="export-row"><a class="export-btn" href="${gcalFam}" target="_blank">Google</a></div>'
        print(f'Fixed family export HTML at line {i+1}')
        break

p.write_text('\n'.join(lines), encoding='utf-8')
print('Done')
