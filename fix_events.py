from pathlib import Path
import re
text = Path('main.js').read_text(encoding='utf-8', errors='ignore')

shared = '''  const EVENTS = [
    { date: '2026-08-04', title: 'Catie St. Germain and Brothers Keep', time: '7:00 PM · Concert Hall', category: 'community', link: 'https://www.visitwinkler.ca' },
    { date: '2026-08-06', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', category: 'community', link: 'https://morden.ca/community-events' },
    { date: '2026-08-07', title: 'Municipal Forum', time: 'P.W. Enns Centennial Concert Hall', category: 'community', link: 'https://www.winkler.ca/events' },
    { date: '2026-08-08', title: 'Prairie Dale No Classes Admin Day', time: 'Prairie Dale School', category: 'family', link: 'https://pds.gvsd.ca/' },
    { date: '2026-08-10', title: 'Mosaic Tray Workshop', time: '7:00 PM · Winkler Arts & Culture', category: 'family', link: 'https://www.visitwinkler.ca' },
    { date: '2026-08-10', title: 'Jr. Summer Art Camp (5-8)', time: '9:30 AM · Winkler Arts & Culture', category: 'family', link: 'https://www.visitwinkler.ca' },
    { date: '2026-08-10', title: 'Summer Art Camp (9-12)', time: '1:00 PM · Winkler Arts & Culture', category: 'family', link: 'https://www.visitwinkler.ca' },
    { date: '2026-08-11', title: 'Finger Painting Workshop', time: '10:30 AM & 1:30 PM · Winkler Library', category: 'family', link: 'https://pembinavalleyonline.com/events/229002' },
    { date: '2026-08-13', title: 'Morden Makerspace Open House', time: '6:00 PM – 8:00 PM · 30 Stephen St, Morden', category: 'community', link: 'https://morden.ca/events/morden-makerspace-open-house' },
    { date: '2026-08-13', title: 'Waffle Breakfast', time: 'Morning · Altona Senior Centre', category: 'community', link: 'https://pembinavalleyonline.com/events' },
    { date: '2026-08-13', title: 'Popsicle Stick Creations', time: '10:30 AM & 1:30 PM · Winkler Library', category: 'family', link: 'https://pembinavalleyonline.com/events/229004' },
    { date: '2026-08-13', title: 'Western Canadian Softball Championships', time: 'Aug 13-17 · Winkler & Morden', category: 'sports', link: 'https://pembinavalleyonline.com/articles/u15-central-energy-softball-team-ready-to-welcome-western-canada-to-winkler' },
    { date: '2026-08-17', title: 'MCC Blanket Making', time: '9:30 AM · Morden Mennonite Church', category: 'community', link: 'https://morden.ca/community-events' },
    { date: '2026-08-18', title: 'Summer Shores Paint & Sip', time: '6:00 PM · Winkler Arts & Culture', category: 'community', link: 'https://www.visitwinkler.ca' },
    { date: '2026-08-19', title: 'The Big Canoe', time: '9:00 AM · Lake Minnewasta', category: 'family', link: 'https://morden.ca/access-event-centre' },
    { date: '2026-08-24', title: 'Morden Council Meeting', time: '7:00 PM · 500 Stephen St', category: 'community', link: 'https://morden.ca/community-events' },
    { date: '2026-08-25', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', category: 'community', link: 'https://morden.ca/community-events' },
    { date: '2026-08-27', title: 'Rise & Shine FREE Morning Camp VBS', time: '9:30 AM · Thiessen Residence, 45 Falcon Drive, Morden', category: 'family', link: 'https://pembinavalleyonline.com/events' },
    { date: '2026-08-27', title: 'Pickleball', time: '1:00 PM · Morden Activity Centre, 306 N. Railway St.', category: 'community', link: 'https://morden.ca/community-events' },
    { date: '2026-08-27', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', category: 'community', link: 'https://morden.ca/community-events' },
    { date: '2026-08-27', title: 'Annual BBQ — Winkler Senior Centre', time: '5:00 PM · 650 Southview Drive', category: 'family', link: 'https://winklerchamber.com/events/' },
    { date: '2026-08-29', title: 'Morden Back40 Music Festival', time: 'Morden, MB', category: 'community', link: 'https://www.backfortymusicfestival.com/' },
    { date: '2026-08-30', title: 'Morden Corn & Apple Festival', time: 'Downtown Morden · Free', category: 'community', link: 'https://cornandapple.com/' },
    { date: '2026-09-01', title: 'Labour Day - No School', time: 'Prairie Dale School', category: 'family', link: 'https://pds.gvsd.ca/' },
    { date: '2026-09-07', title: 'Labour Day - No School', time: 'Prairie Dale School', category: 'family', link: 'https://pds.gvsd.ca/' },
    { date: '2026-09-09', title: 'Prairie Dale First Day Grades K-9', time: 'Prairie Dale School', category: 'family', link: 'https://pds.gvsd.ca/' },
    { date: '2026-09-10', title: 'Prairie Dale First Day Grades 10-12', time: 'Prairie Dale School', category: 'family', link: 'https://pds.gvsd.ca/' },
    { date: '2026-09-18', title: 'Chamber Member Appreciation BBQ', time: 'Winkler City Hall · 185 Main St', category: 'community', link: 'https://winklerchamber.com/events/' },
    { date: '2026-09-25', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', category: 'community', link: 'https://morden.ca/community-events' },
    { date: '2026-10-13', title: 'Morden Farmers Market', time: '4:00 PM · 8th Street', category: 'community', link: 'https://morden.ca/community-events' }
  ];
  const isToday = (d) => new Date(d + 'T12:00:00').toDateString() === new Date().toDateString();
'''

text = text.replace('  function buildUpcoming() {', shared + '  function buildUpcoming() {')

Path('main.js').write_text(text, encoding='utf-8')
print('inserted shared EVENTS array')
