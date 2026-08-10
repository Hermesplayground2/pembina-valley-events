from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')
idx = text.find('function buildActivityWeek()')
snippet = text[idx:idx+1800]
lines = snippet.splitlines()
for i, line in enumerate(lines[40:70], 41):
    print(f'{i}: {line}')
