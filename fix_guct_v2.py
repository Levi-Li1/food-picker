"""Fix guct.html: remove extra </div> at section boundaries and day ends."""
import re

with open('C:/Users/Tebon/BangMaker/Claw/guct.html', 'r', encoding='utf-8') as f:
    h = f.read()

fixes = 0

# Fix 1: 4 consecutive </div> before <h3 → 3 </div>
# Pattern: </div></div></div></div><h3
# Should be: </div></div></div><h3 (close answer + q-block + step, then h3)
count1 = h.count('</div></div></div></div><h3')
h = h.replace('</div></div></div></div><h3', '</div></div></div><h3')
print(f'Fix 1 (4→3 closes before h3): {count1} occurrences')

# Fix 2: 3 consecutive </div> followed by \n\n<div class="day-page"> → 2 </div>
# Pattern: </div></div></div>\n\n<div class="day-page">
# Should be: </div></div>\n\n<div class="day-page">
count2 = len(re.findall(r'</div></div></div>\n\n<div class="day-page">', h))
h = re.sub(r'</div></div></div>\n\n<div class="day-page">', '</div></div>\n\n<div class="day-page">', h)
print(f'Fix 2 (3→2 closes before day-page): {count2} occurrences')

# Fix 3: 4+ consecutive </div> at very end of file
# Fix 4: Special cases with </div></div></div></div> at inline boundaries
# Check for remaining </div></div></div></div> patterns
remaining_4 = h.count('</div></div></div></div>')
print(f'Remaining 4-closes: {remaining_4}')

# Fix 5: </div></div></div>\n\n at end of sections (not followed by day-page)
count5 = len(re.findall(r'(?<!</div>)</div></div></div>\n\n(?!<div class="day-page">)', h))
print(f'Fix 5 (3 closes at section end, not day-page): {count5}')

# Fix 6: Check week-marker boundaries for extra closes
# Pattern: </div></div></div></div>\n\n<div class="week-marker"
# Should be: </div>\n\n<div class="week-marker" or similar
count6 = len(re.findall(r'</div></div></div></div>\s*\n\s*<div class="week-marker"', h))
h = re.sub(
    r'</div></div></div></div>(\s*\n\s*<div class="week-marker")',
    r'</div></div>\1',
    h
)
print(f'Fix 6 (4 closes before week-marker): {count6} occurrences')

with open('C:/Users/Tebon/BangMaker/Claw/guct.html', 'w', encoding='utf-8') as f:
    f.write(h)

print('\nVerification after fixes:')
# Re-audit
day_starts = [m.start() for m in re.finditer(r'<div class="day-page">', h)]
total = 0
for di, ds in enumerate(day_starts):
    de = day_starts[di+1] if di+1 < len(day_starts) else len(h)
    day = h[ds:de]
    dnum = re.search(r'<div class="dnum">(.*?)</div>', day)
    name = dnum.group(1) if dnum else f'D{di+1}'
    h3s = list(re.finditer(r'<h3[^>]*>(.*?)</h3>', day))
    for i in range(len(h3s)):
        sec = day[h3s[i].end():(h3s[i+1].start() if i+1 < len(h3s) else len(day))]
        o = sec.count('<div'); c = sec.count('</div>'); b = o-c
        if b != 0:
            total += 1
            next_l = h3s[i+1].group(1)[:25] if i+1 < len(h3s) else 'END'
            print(f'  REMAINING: {name} [{h3s[i].group(1)[:25]}]→[{next_l}]: b={b:+d}')

print(f'\nRemaining bugs: {total}')
