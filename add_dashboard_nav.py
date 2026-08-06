import pathlib

p = pathlib.Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Add Dashboard nav link
old_nav = '    <a href="#page-family" class="nav-link" data-page="family">Family</a>'
new_nav = '    <a href="#page-family" class="nav-link" data-page="family">Family</a>\n    <a href="#page-dashboard" class="nav-link" data-page="dashboard">Dashboard</a>'
if old_nav in text and 'data-page="dashboard"' not in text:
    text = text.replace(old_nav, new_nav, 1)
    print('Added Dashboard nav link')
else:
    print('Family nav anchor not found or dashboard already exists')

p.write_text(text, encoding='utf-8')
print('Done')
