from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Remove Weather nav link
text = text.replace('<a href="#" class="nav-link" data-page="weather">Weather</a>\n    ', '')

# Remove Weather page block
start = text.find('<div class="page" id="page-weather">')
end = text.find('<div class="page" id="page-local">')
if start != -1 and end != -1:
    text = text[:start] + text[end:]
else:
    raise SystemExit("Weather/local page markers not found")

p.write_text(text, encoding='utf-8')
print('Removed Weather page and nav link')
