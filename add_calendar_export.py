import pathlib

p = pathlib.Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# Add ICS helper near the top of the script block, before renderDashboard
old = '''  function renderDashboard() {'''
new = '''  function downloadICS(title, timeText, dateStr) {
    const dt = dateStr || new Date().toISOString().split('T')[0];
    const dtStart = dt.replace(/-/g, '') + 'T000000';
    const dtEnd = dt.replace(/-/g, '') + 'T235900';
    const cleanTitle = (title || '').replace(/[\\n\\r]/g, ' ').trim();
    const ics = [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//Pembina Valley Events//EN',
      'BEGIN:VEVENT',
      'UID:' + cleanTitle.toLowerCase().replace(/[^a-z0-9]+/g, '-') + '-' + dt + '@pembinaevents.ca',
      'DTSTAMP:' + new Date().toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z',
      'DTSTART;VALUE=DATE:' + dt.replace(/-/g, ''),
      'DTEND;VALUE=DATE:' + dt.replace(/-/g, ''),
      'SUMMARY:' + cleanTitle,
      'DESCRIPTION:' + (timeText || '').replace(/[\\n\\r]/g, ' '),
      'END:VEVENT',
      'END:VCALENDAR'
    ].join('\\r\\n');
    const blob = new Blob([ics], { type: 'text/calendar;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'pembina-event-' + dt + '.ics';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function addGoogleCalendarLink(title, timeText, dateStr) {
    const dt = dateStr || new Date().toISOString().split('T')[0];
    const cleanTitle = encodeURIComponent((title || '').replace(/[\\n\\r]/g, ' ').trim());
    const details = encodeURIComponent((timeText || '').replace(/[\\n\\r]/g, ' ').trim());
    const dates = dt.replace(/-/g, '') + '/' + dt.replace(/-/g, '');
    return 'https://www.google.com/calendar/render?action=TEMPLATE&text=' + cleanTitle + '&dates=' + dates + '/' + dates + '&details=' + details + '&location=Pembina+Valley%2C+MB';
  }

  function renderDashboard() {'''

if old in text and 'function downloadICS' not in text:
    text = text.replace(old, new, 1)
    print('Added ICS + Google Calendar helpers')
else:
    print('Helper anchor not found or already added')

p.write_text(text, encoding='utf-8')
print('Done')
