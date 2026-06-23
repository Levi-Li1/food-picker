#!/usr/bin/env python3
"""fix_guct.py - 修复 guct.html 中 day section 间的 dbody 提前闭合问题"""
import re

fpath = 'C:/Users/Tebon/BangMaker/Claw/guct.html'
with open(fpath, 'r', encoding='utf-8') as f:
    html = f.read()

body_start = html.find('<body>')
before = html[:body_start + len('<body>')]
body = html[body_start + len('<body>'):]

# Split by day-page
days = body.split('<div class="day-page">')
fixed_body = days[0]  # content before first day

total_fixes = 0

for day_num, day_html in enumerate(days[1:], 1):
    # Find dbody boundaries
    dbody_match = re.search(r'<div class="dbody">', day_html)
    if not dbody_match:
        fixed_body += '<div class="day-page">' + day_html
        continue
    
    dbody_start = dbody_match.end()
    
    # Find day closing: last </div>\n</div> before next day-page or EOF
    next_day = day_html.find('<div class="day-page">')
    search_end = next_day if next_day > 0 else len(day_html)
    
    # Find the last consecutive </div>'s before end of search (day closing)
    day_close_search = day_html[:search_end]
    
    # The day always ends with: ...</div>\n</div> (close dbody, close day-page)
    # But there might also be a check div or other content before the close
    # We need to find where dbody content ends and the closing begins
    
    # Find h3 sections within dbody
    h3_matches = list(re.finditer(r'<h3\b[^>]*>', day_html[dbody_start:search_end]))
    
    if len(h3_matches) < 2:
        fixed_body += '<div class="day-page">' + day_html
        continue
    
    # Process the dbody content to fix section boundaries
    dbody_content = day_html[dbody_start:search_end]
    h3_positions = [m.start() for m in h3_matches]  # relative to dbody_content
    
    # For each section boundary (between two consecutive h3s):
    # Count step divs in the first section and adjust its trailing closes
    fixed_content = list(dbody_content)  # work with char list for editing
    
    for i in range(len(h3_positions) - 1):
        sec_start = h3_positions[i]
        sec_end = h3_positions[i + 1]
        section = dbody_content[sec_start:sec_end]
        
        # Count step div openings in this section
        step_count = len(re.findall(r'<div class="step[\s">]', section))
        
        # Expected trailing closes = step_count (each step) + 1 (steps wrapper)
        # But we need to find the actual trailing </div> count
        
        # Find the trailing </div> sequence right before the next h3
        # Work backwards from sec_end to find consecutive </div> tokens
        before_next = dbody_content[:sec_end]
        trailing_divs = []
        pos = sec_end
        while pos > sec_start:
            # Search backwards for </div>
            div_pos = before_next.rfind('</div>', 0, pos)
            if div_pos < 0:
                break
            # Check if there's significant non-div content between this </div> and pos
            between = dbody_content[div_pos + len('</div>'):pos]
            if between.strip() and '<h3' not in between:
                break  # non-empty content before this </div>
            trailing_divs.append(div_pos)
            pos = div_pos
        
        actual_closes = len(trailing_divs)
        
        if actual_closes <= step_count + 1:
            continue  # already correct
        
        # Need to fix: remove excess </div> tags
        # Which ones to remove? The first ones (closest to content) that aren't step closes
        # Strategy: remove (actual_closes - expected) </div> tags
        excess = actual_closes - (step_count + 1)
        
        # Remove the excess closes (starting from the ones closest to content)
        for _ in range(excess):
            # Find the first </div> in the trailing sequence (closest to content)
            idx = min(trailing_divs)
            # Remove this </div> and any following whitespace
            end_idx = idx + len('</div>')
            while end_idx < len(fixed_content) and fixed_content[end_idx] in ' \t\r\n':
                end_idx += 1
            # Mark for removal
            for j in range(idx, end_idx):
                fixed_content[j] = ''
            trailing_divs.remove(idx)
            total_fixes += 1
    
    # Reconstruct the fixed day
    fixed_dbody = ''.join(fixed_content)
    fixed_day = '<div class="day-page">' + day_html[:dbody_start] + fixed_dbody + day_html[search_end:]
    fixed_body += fixed_day

# Handle trailing content after last day (if any)
last_day_start = body.rfind('<div class="day-page">')
if last_day_start >= 0:
    last_day = body[last_day_start:]
    # Find the end of the last day
    last_close = last_day.rfind('</div>\n</div>')
    if last_close >= 0:
        trailing = last_day[last_close + len('</div>\n</div>'):]
        fixed_body += trailing

# Write fixed guct.html
fixed_html = before + fixed_body
with open(fpath, 'w', encoding='utf-8') as f:
    f.write(fixed_html)

print(f'Fixed {total_fixes} excess </div> tags across section boundaries')

# Verify
with open(fpath, 'r', encoding='utf-8') as f:
    vhtml = f.read()

vbody = vhtml[vhtml.find('<body>'):]
vdays = vbody.split('<div class="day-page">')
remaining_bugs = 0
for day_num, day_h in enumerate(vdays[1:], 1):
    dm = re.search(r'<div class="dbody">', day_h)
    if not dm: continue
    dbs = dm.end()
    search_e = day_h.find('<div class="day-page">')
    if search_e < 0: search_e = len(day_h)
    
    h3s = list(re.finditer(r'<h3\b[^>]*>', day_h[dbs:search_e]))
    for i in range(len(h3s)-1):
        sec = day_h[dbs+h3s[i].start():dbs+h3s[i+1].start()]
        sc = len(re.findall(r'<div class="step[\s">]', sec))
        # Count trailing </div>
        before_next = day_h[:dbs+h3s[i+1].start()]
        td = 0
        p = dbs + h3s[i+1].start()
        while p > dbs + h3s[i].start():
            dp = before_next.rfind('</div>', 0, p)
            if dp < 0: break
            between = day_h[dp+len('</div>'):p]
            if between.strip() and '<h3' not in between: break
            td += 1
            p = dp
        if td > sc + 1:
            remaining_bugs += 1
            print(f'  ⚠️ Day {day_num}, h3 {i+1}→{i+2}: {td} closes, expected ≤{sc+1}')

print(f'Remaining bugs: {remaining_bugs}')
print('✅ guct.html fixed!' if remaining_bugs == 0 else '❌ Still have bugs')
