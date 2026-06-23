"""Fix remaining section boundary bugs in guct.html.
For each bug, fix is at the boundary between two h3s or at end of day.
b>0: add </div>   b<0: remove </div>
"""
import re

with open('C:/Users/Tebon/BangMaker/Claw/guct.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Collect all fixes (position, operation, count)
fixes = []

day_starts = [m.start() for m in re.finditer(r'<div class="day-page">', h)]

for di, ds in enumerate(day_starts):
    de = day_starts[di+1] if di+1 < len(day_starts) else len(h)
    day = h[ds:de]
    
    h3s = list(re.finditer(r'<h3[^>]*>(.*?)</h3>', day))
    if not h3s: continue
    
    dnum = re.search(r'<div class="dnum">(.*?)</div>', day)
    name = dnum.group(1) if dnum else f'Day{di+1}'
    
    for i in range(len(h3s)):
        h3_end_abs = ds + h3s[i].end()
        
        if i+1 < len(h3s):
            section_end_abs = ds + h3s[i+1].start()
        else:
            section_end_abs = de
        
        section = h[h3_end_abs:section_end_abs]
        balance = section.count('<div') - section.count('</div>')
        
        if balance == 0:
            continue
        
        next_label = h3s[i+1].group(1)[:30] if i+1 < len(h3s) else 'END'
        
        if balance > 0:
            # Need to add </div> at the boundary
            # Find the position right before the next h3 or day end
            insert_pos = section_end_abs
            # Back up past whitespace
            while insert_pos > h3_end_abs and h[insert_pos-1] in ' \n\r\t':
                insert_pos -= 1
            fixes.append((insert_pos, 'add', balance, f'{name} +{balance} [{h3s[i].group(1)[:25]}]→[{next_label}]'))
        
        elif balance < 0:
            # Need to remove </div> from the boundary area
            remove_count = -balance
            
            # Count trailing </div> at the very end of the section
            # Walk backwards from section_end_abs, counting consecutive </div>
            pos = section_end_abs
            trailing_divs = []
            while pos > h3_end_abs:
                # Skip whitespace backwards
                if pos > 0 and h[pos-1] in ' \n\r\t':
                    pos -= 1
                    continue
                # Check for </div>
                if pos >= 6 and h[pos-6:pos] == '</div>':
                    trailing_divs.append(pos - 6)
                    pos -= 6
                else:
                    break
            
            # Remove min(remove_count, len(trailing_divs)) from the end
            to_remove = min(remove_count, len(trailing_divs))
            for j in range(to_remove):
                fixes.append((trailing_divs[j], 'remove', 1, 
                            f'{name} -1 [{h3s[i].group(1)[:25]}]→[{next_label}]'))

# Apply fixes from end to start
fixes.sort(key=lambda x: x[0], reverse=True)

count_add = 0
count_remove = 0
applied = []

for pos, op, n, desc in fixes:
    if op == 'add':
        insert = '</div>\n' * n
        h = h[:pos] + insert + h[pos:]
        count_add += n
        applied.append(desc)
    elif op == 'remove':
        # Remove 6 chars (</div>) at pos
        h = h[:pos] + h[pos+6:]
        count_remove += 1
        applied.append(desc)

with open('C:/Users/Tebon/BangMaker/Claw/guct.html', 'w', encoding='utf-8') as f:
    f.write(h)

print(f'Added {count_add} </div>, removed {count_remove} </div>')
print(f'Total fixes: {len(applied)}')
for a in applied[:30]:
    print(f'  {a}')
if len(applied) > 30:
    print(f'  ... and {len(applied)-30} more')

# Final verification
day_starts2 = [m.start() for m in re.finditer(r'<div class="day-page">', h)]
remaining = 0
for di, ds in enumerate(day_starts2):
    de = day_starts2[di+1] if di+1 < len(day_starts2) else len(h)
    day = h[ds:de]
    h3s = list(re.finditer(r'<h3[^>]*>(.*?)</h3>', day))
    for i in range(len(h3s)):
        sec = day[h3s[i].end():(h3s[i+1].start() if i+1 < len(h3s) else len(day))]
        if sec.count('<div') - sec.count('</div>') != 0:
            remaining += 1

print(f'\nRemaining bugs: {remaining}')
