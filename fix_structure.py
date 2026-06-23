#!/usr/bin/env python3
"""fix_structure.py - Fix generated w2-w9 files: ensure correct div nesting in day-page sections."""
import re, os

def count_steps(html_section):
    """Count <div class='step' or 'step full' elements"""
    return len(re.findall(r'<div class="step[\s">]', html_section))

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    
    # Find all day-page sections
    day_starts = [m.start() for m in re.finditer(r'<div class="day-page">', html)]
    
    if not day_starts:
        return False
    
    for ds in reversed(day_starts):  # process from end to maintain positions
        # Find end of this day (next day-page or end)
        next_day = html.find('<div class="day-page">', ds + 1)
        de = next_day if next_day > 0 else len(html)
        day_html = html[ds:de]
        
        # Find dbody
        dbody_m = re.search(r'<div class="dbody">', day_html)
        if not dbody_m:
            continue
        
        content_start = dbody_m.end()
        
        # Find h3 positions within day_html (from content_start onward)
        h3_positions = []
        for m in re.finditer(r'<h3\b[^>]*>', day_html):
            if m.start() >= content_start:
                h3_positions.append(m.start())
        
        if len(h3_positions) < 2:
            continue
        
        # Process each non-last section boundary
        fixed_day = list(day_html)
        day_changed = False
        
        for i in range(len(h3_positions) - 1):
            sec_start = h3_positions[i]
            sec_end = h3_positions[i + 1]
            section = day_html[sec_start:sec_end]
            
            # Count trailing </div> before the next h3
            # Look for consecutive </div> at the end of this section
            trailing_before = day_html[:sec_end]
            
            # Find consecutive </div> going backwards from sec_end
            closes = []
            p = sec_end
            while p > sec_start:
                div_pos = trailing_before.rfind('</div>', 0, p)
                if div_pos < 0:
                    break
                # Check what's between this </div> and p: must only be whitespace/comments
                between = day_html[div_pos + len('</div>'):p]
                if between.strip():
                    break
                closes.append(div_pos)
                p = div_pos
            
            actual_closes = len(closes)
            
            # Count step divs in this section
            step_count = count_steps(section)
            expected = step_count + 1  # step closes + steps wrapper close
            
            if actual_closes <= expected:
                continue
            
            # Remove excess </div> (the ones closest to content)
            excess = actual_closes - expected
            for j in range(excess):
                # Remove the /div closest to content (smallest position)
                if closes:
                    pos = min(closes)
                    remove_end = pos + len('</div>')
                    # Also remove whitespace between this and next </div>
                    while remove_end < len(fixed_day) and fixed_day[remove_end] in '\r\n\t ':
                        remove_end += 1
                    for k in range(pos, remove_end):
                        fixed_day[k] = ''
                    closes.remove(pos)
                    day_changed = True
        
        if day_changed:
            new_day = ''.join(fixed_day)
            html = html[:ds] + new_day + html[de:]
    
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


if __name__ == '__main__':
    base = 'C:/Users/Tebon/BangMaker/Claw'
    for fn in ['w2.html', 'w3.html', 'w4.html', 'w5.html', 'w6.html', 'w7.html', 'w8.html', 'w9.html']:
        fp = os.path.join(base, fn)
        if fix_file(fp):
            print(f'  ✅ {fn}')
        else:
            print(f'  -  {fn}')
