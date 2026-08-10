from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# 1) Make weather widget much more prominent on homepage
old = '        <div class="card card-landscape-weather">'
new = '        <div class="card card-landscape-weather" style="border: 3px solid #60a5fa; box-shadow: 0 0 40px rgba(59,130,246,0.35);">'
if old in text:
    text = text.replace(old, new, 1)
    print('Updated weather card border')

old = '.weather-card .temp { font-size: 3.6rem; font-weight: 900; letter-spacing: -0.05em; text-shadow: 0 2px 12px rgba(0,0,0,0.35); }'
new = '.weather-card .temp { font-size: 4.8rem; font-weight: 900; letter-spacing: -0.06em; text-shadow: 0 4px 24px rgba(0,0,0,0.5); }'
if old in text:
    text = text.replace(old, new, 1)
    print('Increased weather temp size')

old = '.weather-card .meta { opacity: 1; margin-top: 10px; font-weight: 800; font-size: 1.2rem; text-shadow: 0 1px 8px rgba(0,0,0,0.35); }'
new = '.weather-card .meta { opacity: 1; margin-top: 12px; font-weight: 900; font-size: 1.4rem; text-shadow: 0 2px 12px rgba(0,0,0,0.45); }'
if old in text:
    text = text.replace(old, new, 1)
    print('Increased weather meta size')

# 2) Add missing Morden/Plum/Altona events to buildActivityWeek
old = "      if (month === 8 && d === 12) add(fmt(year, month, d), { category: 'community', title: 'Kidventure Wednesdays', time: '1:00 PM · Altona EMM Church', link: 'https://altonaemmc.com/' });"
new = """      if (month === 7 && d >= 14 && d <= 16) add(fmt(year, month, d), { category: 'community', title: 'Plum Coulee Plum Fest', time: '125th Anniversary · Plum Coulee MB', link: 'http://www.plumfest.com/' });
      if (month === 8 && d >= 28 && d <= 30) add(fmt(year, month, d), { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Downtown Morden · Free', link: 'https://cornandapple.com/' });
      if (month === 8 && d === 29) add(fmt(year, month, d), { category: 'community', title: 'Morden Back40 Music Festival', time: 'Morden, MB', link: 'https://www.backfortymusicfestival.com/' });
      if (month === 8 && d === 24) add(fmt(year, month, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', link: 'https://morden.ca/community-events' });
      if (month === 8 && d === 17) add(fmt(year, month, d), { category: 'community', title: 'MCC Blanket Making', time: '9:30 AM · Morden Mennonite Church', link: 'https://morden.ca/community-events' });
      if (month === 8 && d === 19) add(fmt(year, month, d), { category: 'community', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta', link: 'https://morden.ca/access-event-centre' });
      if (month === 8 && d === 6) add(fmt(year, month, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });
      if (month === 8 && d === 12) add(fmt(year, month, d), { category: 'community', title: 'Kidventure Wednesdays', time: '1:00 PM · Altona EMM Church', link: 'https://altonaemmc.com/' });"""
if old in text and 'Plum Coulee Plum Fest' not in text.split('function buildActivityWeek')[1]:
    text = text.replace(old, new, 1)
    print('Added local events to buildActivityWeek')
else:
    print('buildActivityWeek skip')

# 3) Add missing Morden events to buildWeek
old = "      if (month === 8 && d === 29) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Back40 Music Festival', time: 'Morden, MB', link: 'https://www.backfortymusicfestival.com/' });"
new = "      if (month === 8 && d >= 28 && d <= 30) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Downtown Morden · Free', link: 'https://cornandapple.com/' });\n      if (month === 8 && d === 29) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Back40 Music Festival', time: 'Morden, MB', link: 'https://www.backfortymusicfestival.com/' });\n      if (month === 8 && d === 24) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', link: 'https://morden.ca/community-events' });\n      if (month === 8 && d === 17) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'MCC Blanket Making', time: '9:30 AM · Morden Mennonite Church', link: 'https://morden.ca/community-events' });\n      if (month === 8 && d === 19) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta', link: 'https://morden.ca/access-event-centre' });\n      if (month === 8 && d === 6) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', link: 'https://morden.ca/community-events' });"
if old in text:
    text = text.replace(old, new, 1)
    print('Added Morden events to buildWeek')
else:
    print('buildWeek Morden skip')

# 4) Verify featured events include Plum Fest
if 'Plum Coulee Plum Fest' not in text.split('function renderFeatured')[1]:
    print('renderFeatured missing Plum Fest')
else:
    print('renderFeatured has Plum Fest')

p.write_text(text, encoding='utf-8')
print('Done')
