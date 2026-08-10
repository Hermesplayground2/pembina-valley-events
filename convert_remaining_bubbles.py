from pathlib import Path

p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Convert remaining locals subsections to linked bubbles
replacements = {
    '🍕 Fast Food & Pizza Specials': '''          <a class="day-event bubble" href="https://www.pizza73.com/" target="_blank" rel="noopener"><span class="title">Pizza 73</span><span class="time">2-for-1 medium pizza special</span></a>
          <a class="day-event bubble" href="https://www.dominos.ca/" target="_blank" rel="noopener"><span class="title">Domino's Pizza</span><span class="time">Mix & match deals</span></a>
          <a class="day-event bubble" href="https://www.papajohns.ca/" target="_blank" rel="noopener"><span class="title">Papa John's</span><span class="time">Large pizza specials</span></a>
          <a class="day-event bubble" href="https://www.mcdonalds.com/" target="_blank" rel="noopener"><span class="title">McDonald's</span><span class="time">Fast food · Winkler</span></a>
          <a class="day-event bubble" href="https://www.kfc.ca/" target="_blank" rel="noopener"><span class="title">KFC</span><span class="time">Fast food · Winkler</span></a>
          <a class="day-event bubble" href="https://www.awrestaurants.com/" target="_blank" rel="noopener"><span class="title">A&W</span><span class="time">Fast food · Winkler</span></a>''',
    '🎉 Special Events': '''          <a class="day-event bubble" href="https://www.winklerharvestfestival.com/" target="_blank" rel="noopener"><span class="title">Winkler Harvest Festival</span><span class="time">Aug 7-9 · Fairgrounds</span></a>
          <a class="day-event bubble" href="https://www.visitwinkler.ca/concerts-in-the-park" target="_blank" rel="noopener"><span class="title">Concerts in the Park</span><span class="time">Wed 7:00 PM · Bethel Heritage Park</span></a>''',
    '🤝 Fundraisers': '''          <a class="day-event bubble" href="https://winklerchamber.com/events/" target="_blank" rel="noopener"><span class="title">Winkler Food Bank Drive</span><span class="time">Local charity drive</span></a>
          <a class="day-event bubble" href="https://winklerbiblecamp.ca/" target="_blank" rel="noopener"><span class="title">Winkler Bible Camp Fundraiser</span><span class="time">Community support</span></a>
          <a class="day-event bubble" href="https://pds.gvsd.ca/" target="_blank" rel="noopener"><span class="title">Local School Fundraiser</span><span class="time">Prairie Dale School area</span></a>''',
    '🍽 Local Food Deals': '''          <a class="day-event bubble" href="https://www.google.com/maps/search/?api=1&query=Buttercup+Cafe+Winkler+MB" target="_blank" rel="noopener"><span class="title">Buttercup Cafe</span><span class="time">Local favorite</span></a>
          <a class="day-event bubble" href="https://www.google.com/maps/search/?api=1&query=Charley+B%27s+Winkler+MB" target="_blank" rel="noopener"><span class="title">Charley B's</span><span class="time">Classic grill & ice cream</span></a>
          <a class="day-event bubble" href="https://www.google.com/maps/search/?api=1&query=SUSHISMITH+Winkler+MB" target="_blank" rel="noopener"><span class="title">SUSHISMITH</span><span class="time">Sushi</span></a>
          <a class="day-event bubble" href="https://www.google.com/maps/search/?api=1&query=Flavors+of+Mexico+Winkler+MB" target="_blank" rel="noopener"><span class="title">Flavors of Mexico</span><span class="time">Mexican</span></a>
          <a class="day-event bubble" href="https://www.google.com/maps/search/?api=1&query=Iceburg+Drive+in+Winkler+MB" target="_blank" rel="noopener"><span class="title">Iceburg Drive-in</span><span class="time">Drive-in classics</span></a>
          <a class="day-event bubble" href="https://www.google.com/maps/search/?api=1&query=Chuck%27s+Roadhouse+Winkler+MB" target="_blank" rel="noopener"><span class="title">Chuck's Roadhouse</span><span class="time">Steak & burgers</span></a>
          <a class="day-event bubble" href="https://www.google.com/maps/search/?api=1&query=Ralph%27s+German+Restaurant+Winkler+MB" target="_blank" rel="noopener"><span class="title">Ralph's German Restaurant</span><span class="time">German cuisine</span></a>
          <a class="day-event bubble" href="https://www.google.com/maps/search/?api=1&query=Toppers+Family+Restaurant+Winkler+MB" target="_blank" rel="noopener"><span class="title">Toppers Family Restaurant</span><span class="time">Family dining</span></a>
          <a class="day-event bubble" href="https://www.google.com/maps/search/?api=1&query=Mulligan%27s+Restaurant+Winkler+MB" target="_blank" rel="noopener"><span class="title">Mulligan's Restaurant & Lounge</span><span class="time">Pub fare</span></a>'''
}

for heading, bubble_block in replacements.items():
    start = text.find(f'<h2>{heading}</h2>')
    if start == -1:
        print(f'Missing {heading}')
        continue
    section_start = text.rfind('<div class="grid grid-3">', 0, start)
    section_end = text.find('</div>', section_start) + 6
    old_section = text[section_start:section_end]
    if '<div class="grid grid-3">' in old_section and '<div class="card local-card' in old_section:
        new_section = '<div class="grid grid-3">\n' + bubble_block + '\n        </div>'
        text = text.replace(old_section, new_section, 1)
        print(f'Converted {heading}')
    else:
        print(f'Skipped {heading}: already converted or different structure')

# Remove past events
past_events = [
    'Tree Lighting Ceremony',
    'Christmas Glow in the Country',
    "City Wide Garage Sale",
    'Morden City Wide Garage Sale',
]

for evt in past_events:
    if evt in text:
        text = text.replace(evt, '', 1)
        print(f'Removed past event: {evt}')
    else:
        print(f'Past event not found: {evt}')

p.write_text(text, encoding='utf-8')
print('Done')
