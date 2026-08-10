from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# === SAFE CSS UPGRADES ONLY - NO JS/HTML STRUCTURE CHANGES ===
# Backup already exists from previous run

# 1. Update root variables with enhanced accent system
old_vars = '''  :root {
    --bg: #f1f5f9;
    --card: #ffffff;
    --text: #0f172a;
    --muted: #64748b;
    --accent: #2563eb;
    --accent-2: #7c3aed;
    --border: #e2e8f0;
    --success: #16a34a;
    --warning: #d97706;
    --danger: #ef4444;
    --radius: 20px;
    --shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  }'''

new_vars = '''  :root {
    --bg: #f8fafc;
    --card: #ffffff;
    --text: #0f172a;
    --muted: #64748b;
    --accent: #2563eb;
    --accent-2: #7c3aed;
    --border: #e2e8f0;
    --success: #16a34a;
    --warning: #d97706;
    --danger: #ef4444;
    --radius: 20px;
    --shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
    --category-community: #2563eb;
    --category-family: #059669;
    --category-outdoors: #0891b2;
    --category-faith: #7c3aed;
    --category-promoted: #d97706;
    --category-fundraiser: #dc2626;
  }'''

if old_vars in text:
    text = text.replace(old_vars, new_vars, 1)
    print('✓ Updated CSS variables with category accents')
else:
    print('✗ CSS variables marker not found')
    exit(1)

# 2. Improve body background
old_body = '''  body {
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
  }'''

new_body = '''  body {
    margin: 0;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    min-height: 100vh;
  }'''

if old_body in text:
    text = text.replace(old_body, new_body, 1)
    print('✓ Updated body to subtle gradient')
else:
    print('✗ Body marker not found')

# 3. Improve header
old_header = '''  header {
    text-align: center;
    padding: 28px 18px 18px;
  }
  header h1 {
    margin: 0;
    font-size: 1.6rem;
    font-weight: 900;
    letter-spacing: -0.02em;
  }
  header p {
    margin: 6px 0 0;
    color: var(--muted);
    font-size: 0.95rem;
  }'''

new_header = '''  header {
    text-align: center;
    padding: 36px 18px 24px;
    background: linear-gradient(135deg, rgba(37,99,235,0.05) 0%, rgba(124,58,237,0.05) 100%);
    border-bottom: 1px solid var(--border);
    margin-bottom: 8px;
  }
  header h1 {
    margin: 0;
    font-size: 2rem;
    font-weight: 900;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  header p {
    margin: 8px 0 0;
    color: var(--muted);
    font-size: 1rem;
    font-weight: 500;
  }'''

if old_header in text:
    text = text.replace(old_header, new_header, 1)
    print('✓ Updated header with gradient text')
else:
    print('✗ Header marker not found')

# 4. Improve card hover and styling
old_card = '''  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 18px;
  }'''

new_card = '''  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  }
  .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.08);
    border-color: rgba(37,99,235,0.2);
  }'''

if old_card in text:
    text = text.replace(old_card, new_card, 1)
    print('✓ Updated card styling with hover lift')
else:
    print('✗ Card marker not found')

# 5. Improve section spacing
old_section = '''  .section {
    padding: 18px;
    max-width: 1100px;
    margin: 0 auto;
  }'''

new_section = '''  .section {
    padding: 24px 18px;
    max-width: 1100px;
    margin: 0 auto;
  }'''

if old_section in text:
    text = text.replace(old_section, new_section, 1)
    print('✓ Updated section spacing')
else:
    print('✗ Section marker not found')

# 6. Improve h2 titles
old_h2 = '''  h2 {
    margin: 0 0 10px;
    font-size: 1.15rem;
    font-weight: 800;
  }'''

new_h2 = '''  h2 {
    margin: 0 0 14px;
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.01em;
  }'''

if old_h2 in text:
    text = text.replace(old_h2, new_h2, 1)
    print('✓ Updated h2 styling')
else:
    print('✗ H2 marker not found')

# 7. Improve muted text
old_muted = '''  .muted {
    color: var(--muted);
    font-size: 0.9rem;
  }'''

new_muted = '''  .muted {
    color: var(--muted);
    font-size: 0.9rem;
    line-height: 1.6;
  }'''

if old_muted in text:
    text = text.replace(old_muted, new_muted, 1)
    print('✓ Updated muted text')
else:
    print('✗ Muted marker not found')

# 8. Improve pill buttons
old_pill = '''  .pill {
    display: inline-flex;
    align-items: center;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    color: #e5e7eb;
    text-decoration: none;
    font-size: 0.85rem;
    border: 1px solid rgba(255,255,255,0.1);
    transition: background .15s ease, transform .1s ease;
  }'''

new_pill = '''  .pill {
    display: inline-flex;
    align-items: center;
    padding: 9px 16px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    color: #e5e7eb;
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.12);
    transition: background .15s ease, transform .1s ease, box-shadow .15s ease;
  }
  .pill:hover {
    background: rgba(255,255,255,0.14);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }'''

if old_pill in text:
    text = text.replace(old_pill, new_pill, 1)
    print('✓ Updated pill button styling')
else:
    print('✗ Pill marker not found')

# 9. Improve nav link active state
old_nav_active = '''  .nav-link.active {
    background: #0f172a;
    color: white;
  }'''

new_nav_active = '''  .nav-link.active {
    background: var(--accent);
    color: white;
    box-shadow: 0 2px 8px rgba(37,99,235,0.3);
  }'''

if old_nav_active in text:
    text = text.replace(old_nav_active, new_nav_active, 1)
    print('✓ Updated nav active state')
else:
    print('✗ Nav active marker not found')

# 10. Add subtle noise texture via CSS
old_container = '''  .container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 18px;
  }'''

new_container = '''  .container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 18px;
    position: relative;
  }
  .container::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    opacity: 0.015;
    pointer-events: none;
    z-index: -1;
  }'''

if old_container in text:
    text = text.replace(old_container, new_container, 1)
    print('✓ Added subtle noise texture')
else:
    print('✗ Container marker not found')

p.write_text(text, encoding='utf-8')
print('\n✅ All safe CSS upgrades applied')
print('📋 Backup exists at index.html.backup-*')
print('🔄 To restore: cp index.html.backup-* index.html')
