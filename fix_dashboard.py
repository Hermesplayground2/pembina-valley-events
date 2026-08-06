import pathlib

p = pathlib.Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

old_func = '''  function renderDashboard() {
    const viewsBox = document.getElementById('dashboard-views');
    const referrersBox = document.getElementById('dashboard-referrers');
    const trendBox = document.getElementById('dashboard-trend');
    if (!viewsBox && !referrersBox && !trendBox) return;

    fetch('analytics.json')
      .then(r => r.json())
      .then(data => {
        const views = data.views || [];
        const referrers = data.referrers || [];
        const totalViews = views.reduce((s, v) => s + (v.count || 0), 0);
        const totalUniques = views.reduce((s, v) => s + (v.uniques || 0), 0);

        if (viewsBox) {
          viewsBox.innerHTML = ;
        }

        if (referrersBox) {
          referrersBox.innerHTML = referrers.length
            ? referrers.map(r => ).join('')
            : '<p class="muted">No referrer data yet.</p>';
        }

        if (trendBox) {
          trendBox.innerHTML = views.length
            ? views.map(v => {
                const date = new Date(v.timestamp).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
                return ;
              }).join('')
            : '<p class="muted">No trend data yet.</p>';
        }
      })
      .catch(() => {
        if (viewsBox) viewsBox.innerHTML = '<p class="muted">Analytics unavailable.</p>';
        if (referrersBox) referrersBox.innerHTML = '<p class="muted">Analytics unavailable.</p>';
        if (trendBox) trendBox.innerHTML = '<p class="muted">Analytics unavailable.</p>';
      });
  }'''

new_func = '''  function renderDashboard() {
    const viewsBox = document.getElementById('dashboard-views');
    const referrersBox = document.getElementById('dashboard-referrers');
    const trendBox = document.getElementById('dashboard-trend');
    if (!viewsBox && !referrersBox && !trendBox) return;

    fetch('analytics.json')
      .then(r => r.json())
      .then(data => {
        const views = data.views || [];
        const referrers = data.referrers || [];
        const totalViews = views.reduce((s, v) => s + (v.count || 0), 0);
        const totalUniques = views.reduce((s, v) => s + (v.uniques || 0), 0);

        if (viewsBox) {
          viewsBox.innerHTML = '<div class="event-row"><div class="event-date"><div class="month">Views</div><div class="day">' + totalViews + '</div></div><div><div class="event-title">Total page views</div><div class="event-meta">Last 14 days</div></div></div><div class="event-row"><div class="event-date" style="background:#fef3c7;color:#92400e;"><div class="month">Visitors</div><div class="day">' + totalUniques + '</div></div><div><div class="event-title">Unique visitors</div><div class="event-meta">Last 14 days</div></div></div>';
        }

        if (referrersBox) {
          referrersBox.innerHTML = referrers.length
            ? referrers.map(r => '<div class="event-row"><div class="event-date" style="background:#eef2ff;color:#3730a3;"><div class="month">Ref</div><div class="day">' + r.count + '</div></div><div><div class="event-title">' + r.referrer + '</div><div class="event-meta">' + r.uniques + ' unique</div></div></div>').join('')
            : '<p class="muted">No referrer data yet.</p>';
        }

        if (trendBox) {
          trendBox.innerHTML = views.length
            ? views.map(v => {
                const date = new Date(v.timestamp).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
                return '<div class="event-row"><div class="event-date" style="background:#f1f5f9;color:#0f172a;"><div class="month">Day</div><div class="day">' + date + '</div></div><div><div class="event-title">' + v.count + ' views</div><div class="event-meta">' + v.uniques + ' unique</div></div></div>';
              }).join('')
            : '<p class="muted">No trend data yet.</p>';
        }
      })
      .catch(() => {
        if (viewsBox) viewsBox.innerHTML = '<p class="muted">Analytics unavailable.</p>';
        if (referrersBox) referrersBox.innerHTML = '<p class="muted">Analytics unavailable.</p>';
        if (trendBox) trendBox.innerHTML = '<p class="muted">Analytics unavailable.</p>';
      });
  }'''

if old_func in text:
    text = text.replace(old_func, new_func, 1)
    print('Fixed renderDashboard function')
else:
    print('Broken function anchor not found')

p.write_text(text, encoding='utf-8')
print('Done')
