from pathlib import Path
p = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html')
text = p.read_text(encoding='utf-8')

# === SAFE DESIGN UPGRADE: append new style block at end ===
# This only adds CSS; it does not change JS or HTML structure.

# 1. Add enhanced CSS variables block before </style>
old_style_end = '''</style>'''

new_style_end = '''  /* Enhanced design system */
  :root {
    --category-community: #2563eb;
    --category-family: #059669;
    --category-outdoors: #0891b2;
    --category-faith: #7c3aed;
    --category-promoted: #d97706;
    --category-fundraiser: #dc2626;
  }
  body {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%);
    line-height: 1.65;
  }
  header {
    padding: 40px 20px 56px;
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
  }
  header h1 {
    font-size: clamp(1.9rem, 4.2vw, 2.8rem);
    font-weight: 900;
    letter-spacing: -0.04em;
  }
  header p {
    opacity: 0.95;
    margin-top: 12px;
    font-weight: 500;
    font-size: clamp(1rem, 1.8vw, 1.15rem);
  }
  .card {
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
  }
  .card:hover {
    transform: translateY(-3px);
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.12);
    border-color: rgba(37,99,235,0.25);
  }
  .nav-link.active {
    background: var(--accent);
    color: white;
    border-color: var(--accent);
    box-shadow: 0 2px 10px rgba(37,99,235,0.35);
  }
  .section { padding: 26px 18px; }
  h2 { font-size: 1.25rem; font-weight: 800; margin-bottom: 12px; letter-spacing: -0.01em; }
  .muted { line-height: 1.65; }
  .pill {
    font-weight: 700;
    transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
  }
  .pill:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(15,23,42,0.12);
  }
  @media (max-width: 640px) {
    .card { padding: 18px; }
    header { padding: 32px 18px 44px; }
  }
</style>'''

if old_style_end in text:
    text = text.replace(old_style_end, new_style_end, 1)
    print('✓ Appended enhanced design system CSS')
else:
    print('✗ Could not locate </style> safely')
    exit(1)

p.write_text(text, encoding='utf-8')
print('Done')
