import pathlib

p = pathlib.Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Add missing renderFeatured function before renderFamilyEvents
old = '  function renderFamilyEvents() {'
new = '''  function renderFeatured() {
    const container = document.getElementById('featured-events');
    if (!container) return;
    const featured = [
      { category: 'community', title: 'Winkler Harvest Festival', time: 'Aug 7-9 · Winkler Fairgrounds', date: 'Aug 7' },
      { category: 'family', title: 'Prairie Dale School Events', time: 'Aug-Sep · Winkler, MB', date: 'Aug' },
      { category: 'community', title: 'Chamber Member Appreciation BBQ', time: 'Sep 18 · Winkler City Hall', date: 'Sep 18' },
      { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Aug 28-30 · Downtown Morden', date: 'Aug 28' },
      { category: 'community', title: 'Morden Back40 Music Festival', time: 'Aug 29 · Morden, MB', date: 'Aug 29' },
      { category: 'community', title: 'The Big Canoe', time: 'Sep 19 · Lake Minnewasta', date: 'Sep 19' },
      { category: 'community', title: 'Altona Kidventure Wednesdays', time: 'Aug 12 · Altona EMM Church', date: 'Aug 12' }
    ];

    container.innerHTML = featured.map(ev => `
      <div class="featured-card" data-category="${ev.category}">
        <div class="row">
          <div class="badge-row">
            <span class="date-badge">${ev.date}</span>
            <span class="cat-badge">${ev.category}</span>
          </div>
        </div>
        <div class="title">${ev.title}</div>
        <div class="meta">${ev.time}</div>
      </div>
    `).join('');
  }

  function renderFamilyEvents() {'''
if old in text and 'function renderFeatured()' not in text:
    text = text.replace(old, new, 1)
    print('Added renderFeatured()')
else:
    print('renderFeatured already exists or anchor not found')

# Add Morden/Altona events to buildWeek
old_week = "      if (month === 8 && d === 2) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive' });"
new_week = """      if (month === 8 && d === 2) addIfInWeek(fmt(year, month, d), { category: 'family', title: 'Winkler EMMC Worship Service', time: '10:30 AM · 600 Southview Drive' });
      if (month === 7 && d >= 28 && d <= 30 && year === 2026) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Winkler Harvest Festival', time: 'Fairgrounds · Free admission' });
      if (month === 7 && d >= 6 && d <= 9 && year === 2026) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Harvest Festival Events', time: 'Winkler · Various times' });
      if (month === 8 && d >= 28 && d <= 30) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Corn & Apple Festival', time: 'Downtown Morden · Free' });
      if (month === 8 && d === 29) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Back40 Music Festival', time: 'Morden, MB' });
      if (month === 8 && d === 24) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St' });
      if (month === 8 && d === 17) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'MCC Blanket Making', time: '9:30 AM · Morden Mennonite Church' });
      if (month === 8 && d === 19) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta' });
      if (month === 8 && d === 12) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Kidventure Wednesdays', time: '1:00 PM · Altona EMM Church' });
      if (month === 8 && d === 6) addIfInWeek(fmt(year, month, d), { category: 'community', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street' });
      if (month === 8 && d === 8) addIfInWeek(fmt(year, month, d), { category: 'fundraiser', title: 'Fundraising BBQ', time: '11:30 AM · Faith Mission, Winkler' });"""
if old_week in text:
    text = text.replace(old_week, new_week, 1)
    print('Added Morden/Altona to buildWeek')
else:
    print('Week anchor not found')

# Update site title to reflect regional coverage
old_title = 'Pembina Valley Events - Family Fix Deploy'
new_title = 'Pembina Valley Events — Winkler · Morden · Altona'
if old_title in text:
    text = text.replace(old_title, new_title, 1)
    print('Updated site title')
else:
    print('Title not found')

p.write_text(text, encoding='utf-8')
print('Done')
