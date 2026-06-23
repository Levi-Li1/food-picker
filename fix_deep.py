#!/usr/bin/env python3
"""fix_deep.py - Fix h3 at depth ≤0 by removing premature dbody closes.
For each day-page, track depth from dbody open. At each bad h3, 
find and remove the extra </div> that closed dbody too early."""
import re, os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html

    # Process in reverse to maintain positions
    day_starts = [m.start() for m in re.finditer(r'<div class="day-page">', html)]
    
    # Find all day boundaries
    days = []
    for i, ds in enumerate(day_starts):
        next_ds = day_starts[i+1] if i+1 < len(day_starts) else len(html)
        days.append((ds, next_ds))

    total_fixes = 0
    # Process from last to first to maintain positions
    for ds, de in reversed(days):
        day_html = html[ds:de]
        
        # Find dbody position
        dbody_m = re.search(r'<div class="dbody">', day_html)
        if not dbody_m:
            continue
        
        dbody_start = dbody_m.start()
        dbody_content_start = dbody_m.end()
        
        # Track depth from day-page opening
        # day-page open → depth 1
        # dbody open → depth 2
        # At h3: should be at depth 2 (dbody just opened) or 3+ (inside steps)
        
        # Find all h3 positions after dbody
        h3_positions = []
        for m in re.finditer(r'<h3\b', day_html):
            if m.start() >= dbody_content_start:
                h3_positions.append(m.start())
        
        if not h3_positions:
            continue
        
        # Count the full div depth tracking from start of day_html
        # We need absolute depth, not relative
        depth = 0
        line_positions = []  # (char_pos, depth_before_line)
        lines = day_html.split('\n')
        char_pos = 0
        for line in lines:
            line_positions.append((char_pos, depth))
            opens = len(re.findall(r'<div\b[^>]*>', line))
            closes = len(re.findall(r'</div>', line))
            depth += opens - closes
            char_pos += len(line) + 1  # +1 for \n
        
        # Check each h3's depth
        for h3_pos in h3_positions:
            # Find which line contains this h3
            h3_depth = None
            for cp, ld in reversed(line_positions):
                if cp <= h3_pos:
                    h3_depth = ld
                    break
            
            if h3_depth is None or h3_depth >= 2:
                continue  # depth 2 or more is OK
            
            # This h3 is at depth 0 or 1. The dbody was closed too early.
            # Find the last </div> before this h3 that's at the dbody level
            # We need to find where dbody was closed and remove that close
            
            # Search backwards from h3_pos to find the premature dbody close
            # The dbody was at depth 2 when opened, so we're looking for the
            # </div> that took depth from 2 to 1 (or from 3 to 2 if inside steps)
            
            before_h3 = day_html[:h3_pos]
            
            # Find the last </div> that makes depth drop to or below 1
            # Strategy: remove the LAST </div> before this h3 that appears
            # to be the dbody close
            
            # Find all </div> positions before h3
            div_closes = []
            p = 0
            while True:
                p = before_h3.find('</div>', p)
                if p < 0: break
                div_closes.append(p)
                p += len('</div>')
            
            if not div_closes:
                continue
            
            # Calculate depth at each </div>
            # Depth tracking from start of day_html
            for close_pos in reversed(div_closes):
                # Find the depth right before this close
                before_close = day_html[:close_pos]
                d = 0
                # Simple count of opens vs closes before this position
                opens_before = len(re.findall(r'<div\b[^>]*>', before_close))
                closes_before = len(re.findall(r'</div>', before_close))
                depth_before = opens_before - closes_before
                
                # If depth_before is 2 (dbody level) and we're about to close,
                # removing this close would keep dbody open
                if depth_before >= 2:
                    # Found the dbody close! Remove it
                    # Also remove trailing whitespace
                    remove_end = close_pos + len('</div>')
                    while remove_end < len(day_html) and day_html[remove_end] in '\r\n\t ':
                        remove_end += 1
                    
                    # Apply the fix
                    fixed_day = day_html[:close_pos] + day_html[remove_end:]
                    
                    # Update day_html for subsequent h3 checks
                    shift = remove_end - close_pos
                    day_html = fixed_day
                    
                    # Adjust h3_positions after this point
                    for j in range(len(h3_positions)):
                        if h3_positions[j] > close_pos:
                            h3_positions[j] -= shift
                    
                    total_fixes += 1
                    break  # fixed one h3, continue to next
        
        # Apply the fixed day to the full HTML
        if day_html != html[ds:de]:
            html = html[:ds] + day_html + html[de:]

    if total_fixes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    return total_fixes


if __name__ == '__main__':
    base = 'C:/Users/Tebon/BangMaker/Claw'
    for fn in ['w2.html', 'w3.html', 'w4.html', 'w5.html', 'w6.html', 'w7.html', 'w8.html', 'w9.html']:
        fp = os.path.join(base, fn)
        fixes = fix_file(fp)
        if fixes > 0:
            print(f'  ✅ {fn}: {fixes} fixes')
        else:
            print(f'  -  {fn}: no fixes needed')
    
    # Re-verify
    print('\nVerification:')
    for fn in ['w1.html','w2.html','w3.html','w4.html','w5.html','w6.html','w7.html','w8.html','w9.html']:
        with open(os.path.join(base, fn), 'r', encoding='utf-8') as f:
            h = f.read()
        d = 0; bad = 0
        for line in h.split('\n'):
            d += len(re.findall(r'<div\b[^>]*>', line)) - len(re.findall(r'</div>', line))
        ok = '✅' if d == 0 else f'❌ end_d={d}'
        print(f'  {fn}: {ok}')
