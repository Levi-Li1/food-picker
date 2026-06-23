#!/usr/bin/env python3
"""fix_words.py - 修复所有 w2-w9 的 30词框：删除stray，将词框包裹在step内"""
import re, os

BASE = 'C:/Users/Tebon/BangMaker/Claw'

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    changes = 0
    
    # 1. Delete ALL stray word boxes (not inside any day-page)
    # A stray word box has no <div class="day-page"> before it
    day_markers = [m.start() for m in re.finditer(r'<div class="day-page">', html)]
    
    # Find all gray boxes
    for m in re.finditer(r'background:#f0f0f5[^>]*>', html):
        pos = m.start()
        # Find the <div that starts this gray box
        div_start = html.rfind('<div', 0, pos)
        if div_start < 0:
            continue
        
        # Check if this is inside a day-page
        inside_day = False
        for dm in day_markers:
            next_dm = html.find('<div class="day-page">', dm + 1)
            if next_dm < 0: next_dm = len(html)
            if dm < div_start < next_dm:
                inside_day = True
                break
        
        if not inside_day:
            # This is a stray word box - remove it
            # Find the end: the 31st </div> (30 words + 1 gray box) or until </div></div>
            after = html[pos:]
            # Find all </div>
            divs = list(re.finditer(r'</div>', after))
            # Each word entry: 2 </div> (word line + example line)
            # We need ~60 </div> for 30 words... but the stray might have fewer
            # Just find the gray box close + surrounding closes
            end_m = re.search(r'(</div>\s*\n\s*){2,}', after[:2000])
            if end_m:
                end_pos = pos + end_m.end()
            else:
                end_pos = pos + after.find('</div>\n</div>\n</div>') + 18
            
            if end_pos > pos:
                html = html[:div_start] + html[end_pos:]
                changes += 1
                print(f'  - Deleted stray word box')
    
    # 2. For word boxes inside days: wrap in <div class="step full">
    # Pattern: gray box after English section's steps close
    # Before gray box: </div></div> (steps close)
    # After gray box: next section or day close
    # Fix: insert <div class="step full"> before gray box, </div> after
    
    day_starts = [m.start() for m in re.finditer(r'<div class="day-page">', html)]
    
    for ds in day_starts:
        de = html.find('<div class="day-page">', ds + 1)
        if de < 0: de = len(html)
        day = html[ds:de]
        
        # Find all gray boxes in this day
        for m in re.finditer(r'background:#f0f0f5[^>]*>', day):
            gb_pos = m.start()
            div_start = day.rfind('<div style="back', 0, gb_pos)
            if div_start < 0:
                div_start = day.rfind('<div', 0, gb_pos)
            if div_start < 0:
                continue
            
            # Check if this gray box is already inside a step
            before_gb = day[:div_start]
            if before_gb.rfind('<div class="step') > before_gb.rfind('</div>\n</div>'):
                continue  # already inside a step
            
            # Find gray box end
            after_gb = day[gb_pos:]
            # Each word entry has 2 </div> (word + example)
            # 30 words = 60 </div>, plus 1 for gray box close = 61
            # But we might have fewer. Find the closing pattern.
            divs_in_gb = list(re.finditer(r'</div>', after_gb[:5000]))
            
            # Find where the gray box section naturally ends
            # Look for: </div>\n\n or </div>\n</div>\n</div>
            gb_close = -1
            for idx, d in enumerate(divs_in_gb):
                after_d = after_gb[d.end():d.end()+20]
                if '</div>' in after_d[:10] or '</h3>' in after_d[:20] or 'class="check"' in after_d[:50] or '<div class="day-page"' in after_d[:50]:
                    gb_close = gb_pos + d.end()
                    break
            
            if gb_close < 0 and divs_in_gb:
                gb_close = gb_pos + divs_in_gb[-1].end()
            
            if gb_close < gb_pos:
                continue
            
            # Wrap the gray box in step full
            gray_box = day[div_start:gb_close]
            abs_start = ds + div_start
            abs_end = ds + gb_close
            
            wrapped = f'<div class="step full"><h4><span class="dot" style="background:var(--green)"></span>今日30词</h4>\n{gray_box}\n</div>'
            
            html = html[:abs_start] + wrapped + html[abs_end:]
            changes += 1
            print(f'  + Wrapped word box in step full')
            break  # one per day, re-scan
    
    if changes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    
    return changes


if __name__ == '__main__':
    for fn in ['w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9']:
        fp = os.path.join(BASE, f'{fn}.html')
        c = fix_file(fp)
        if c > 0:
            print(f'{fn}: {c} changes')
        else:
            print(f'{fn}: no changes')
