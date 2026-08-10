from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Ensure Plum Coulee Plum Fest appears in activities
if 'Plum Coulee Plum Fest' not in text.split('function buildActivityWeek')[1]:
    old = "      if (month === 8 && d === 12) add(fmt(year, month, d), { category: 'community', title: 'Kidventure Wednesdays', time: '1:00 PM · Altona EMM Church', link: 'https://altonaemmc.com/' });"
    new = "      if (month === 7 && d >= 14 && d <= 16) add(fmt(year, month, d), { category: 'community', title: 'Plum Coulee Plum Fest', time: '125th Anniversary · Plum Coulee MB', link: 'http://www.plumfest.com/' });\n      if (month === 8 && d === 12) add(fmt(year, month, d), { category: 'community', title: 'Kidventure Wednesdays', time: '1:00 PM · Altona EMM Church', link: 'https://altonaemmc.com/' });"
    if old in text:
        text = text.replace(old, new, 1)
        print('Added Plum Fest to buildActivityWeek')
    else:
        print('buildActivityWeek marker not found')
else:
    print('Plum Fest already in buildActivityWeek')

# Ensure Morden/Altona events exist in activities
missing = []
for term in ['Morden Corn & Apple Festival', 'Morden Back40 Music Festival', 'Morden Council Meeting', 'Morden Farmers Market', 'MCC Blanket Making', 'The Big Canoe']:
    if term not in text.split('function buildActivityWeek')[1]:
        missing.append(term)
if missing:
    print('Missing in buildActivityWeek:', missing)
else:
    print('buildActivityWeek has local events')

# Ensure family events include Plum Coulee
if 'Plum Coulee Plum Fest' not in text.split('function renderFamilyEvents')[1]:
    old = "      { title: 'MCC Blanket Making', date: '1st/3rd Mondays', time: '9:30 AM · Morden Mennonite Church', category: 'family', link: 'https://morden.ca/community-events' }"
    new = "      { title: 'Plum Coulee Plum Fest', date: 'Aug 14-16', time: '125th Anniversary · Plum Coulee', category: 'family', link: 'http://www.plumfest.com/' },\n      { title: 'MCC Blanket Making', date: '1st/3rd Mondays', time: '9:30 AM · Morden Mennonite Church', category: 'family', link: 'https://morden.ca/community-events' }"
    if old in text:
        text = text.replace(old, new, 1)
        print('Added Plum Fest to renderFamilyEvents')
    else:
        print('renderFamilyEvents marker not found')
else:
    print('Plum Fest already in renderFamilyEvents')

p.write_text(text, encoding='utf-8')
print('Done')
