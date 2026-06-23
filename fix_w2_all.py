#!/usr/bin/env python3
"""fix_w2_all.py - 修复 w2.html 三个问题"""
import re

with open('C:/Users/Tebon/BangMaker/Claw/w2.html', 'r', encoding='utf-8') as f:
    html = f.read()

# === FIX 1: Remove stray word box between week-marker and first day ===
wk = html.find('class="week-marker"')
fd = html.find('<div class="day-page">', wk)
between = html[wk:fd]
gb_start = between.find('<div style="background:#f0f0f5')
if gb_start > 0:
    after = between[gb_start:]
    # Find 3 consecutive </div> on separate lines (gray box close + 2 closes)
    m = re.search(r'</div>\s*\n\s*</div>\s*\n\s*</div>', after)
    if m:
        gb_end = gb_start + m.end()
        html = html[:wk+gb_start] + html[wk+gb_end:]
        print('✅ Fix 1: Removed stray word box')

# === FIX 2: Fix Day 9/10/11 30词 - remove bare <div> before word boxes ===
for dn in [9, 10, 11]:
    dm = f'<div class="dnum">Day {dn}</div>'
    ndm = f'<div class="dnum">Day {dn+1}</div>'
    ds = html.find(dm)
    de = html.find(ndm) if html.find(ndm) > 0 else -1
    if de < 0: de = html.find('<div class="day-page">', ds+1)
    if de < 0: de = len(html)
    
    words = html.find('今日30词', ds)
    if 0 < words < de:
        # Find pattern: </div></div></div><div><div><div style="background
        # Replace with: </div></div><div style="background
        pat = '</div></div></div><div><div><div style="background:#f0f0f5'
        fix = '</div></div><div style="background:#f0f0f5'
        if pat in html[words-200:words+10]:
            html = html.replace(pat, fix)
            print(f'✅ Fix 2: Day {dn} 30词 depth fixed')

# === FIX 3: Add <div class="steps"> wrappers + close them properly ===
# Step A: Wrap steps: </h3><div class="step → </h3>\n<div class="steps">\n<div class="step
html = re.sub(r'</h3><div class="step', '</h3>\n<div class="steps">\n<div class="step', html)
step_wraps_added = len(re.findall(r'<div class="steps">', html))
print(f'  Steps wrappers added: {step_wraps_added}')

# Step B: Close steps before each <h3>
# Pattern: </div></div><h3 → </div></div></div><h3 (add steps close)
html = re.sub(r'(</div>\s*</div>)\s*(<h3)', r'\1\n</div>\n\2', html)

# Step C: Close steps before <div class="check">
html = re.sub(r'(</div>\s*</div>)\s*(<div class="check")', r'\1\n</div>\n\2', html)

print('✅ Fix 3: Added steps wrappers + closes')

# === CLEANUP: Fix double-close issues ===
# After adding steps closes, some sections may have: </div></div></div></div><h3
# (step + steps + steps close + h3) should be: </div></div></div><h3
html = re.sub(r'(</div>\s*</div>\s*</div>)\s*(</div>)\s*(<h3)', r'\1\n\3', html)
html = re.sub(r'(</div>\s*</div>\s*</div>)\s*(</div>)\s*(<div class="check")', r'\1\n\3', html)

# Apply blue buttons + sup m
html = html.replace('background:#8e8e93;color:#fff', 'background:var(--blue);color:#fff')
html = html.replace('\u1d50', '<sup>m</sup>')

with open('C:/Users/Tebon/BangMaker/Claw/w2.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Verify
d = 0
for line in html.split('\n'):
    d += len(re.findall(r'<div\b[^>]*>', line)) - len(re.findall(r'</div>', line))

# Check issue 1: stray words
wk2 = html.find('class="week-marker"')
fd2 = html.find('<div class="day-page">', wk2)
stray = html[wk2:fd2].count('今日30词')

print(f'\n=== VERIFY ===')
print(f'end_depth={d}')
print(f'stray words between week-marker and first day: {stray}')
steps_ct = html.count('<div class="steps">')
print(f'steps wrappers: {steps_ct}')

# Check Day 9 30词 depth
for dn in [9, 10, 11]:
    dm = f'<div class="dnum">Day {dn}</div>'
    ndm = f'<div class="dnum">Day {dn+1}</div>'
    ds = html.find(dm)
    de = html.find(ndm) if html.find(ndm) > 0 else -1
    if de < 0: de = html.find('<div class="day-page">', ds+1)
    if de < 0: de = len(html)
    words = html.find('今日30词', ds)
    if words > 0 and words < de:
        before = html[ds:words]
        depth = 0
        for line in before.split('\n'):
            depth += len(re.findall(r'<div\b[^>]*>', line)) - len(re.findall(r'</div>', line))
        print(f'Day {dn} 30词 depth: {depth}')
