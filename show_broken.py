from pathlib import Path

# Read the file
text = Path(r'C:\Users\vikto\Documents\Wilson\website\index.html').read_text(encoding='utf-8')

# Find and show the exact broken lines
for i, line in enumerate(text.splitlines(), 1):
    if 'safeTitle' in line or 'safeTime' in line or 'safeFamTitle' in line or 'safeFamTime' in line:
        print(f'Line {i}: {repr(line)}')
        # Show the exact replacement
        if "replace(/'/g, '\\\\'');" in line:
            fixed = line.replace("replace(/'/g, '\\\\'');", "replace(/'/g, '\\\\'\"'\"');")
            print(f'  -> {repr(fixed)}')
