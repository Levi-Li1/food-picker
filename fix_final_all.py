#!/usr/bin/env python3
"""fix_final_all.py - 将 w2-w9 结构调整为与 w1 一致"""
import re, os

BASE = 'C:/Users/Tebon/BangMaker/Claw'

def fix_file(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # --- 1. Fix dbody+h3 on same line: split them ---
    # <div class="dbody"><h3 → <div class="dbody">\n<h3
    html = html.replace('<div class="dbody"><h3', '<div class="dbody">\n<h3')
    
    # --- 2. Close week-marker properly after wnote ---
    wm = html.find('class="week-marker"')
    wnote = html.find('<div class="wnote">', wm)
    wnote_close = html.find('</div>', wnote)
    after = html[wnote_close+6:]
    dp = after.find('<div class="day-page">')
    if dp < 0: dp = len(after)
    html = html[:wnote_close+6] + '</div>\n' + after[dp:]
    
    # --- 3. Wrap step divs in <div class="steps"> ---
    html = re.sub(r'</h3>\s*<div class="step', '</h3>\n<div class="steps">\n<div class="step', html)
    
    # --- 4. Close steps before <h3> and <div class="check"> ---
    html = re.sub(r'(</div>\s*</div>)\s*(<h3)', r'\1\n</div>\n\2', html)
    html = re.sub(r'(</div>\s*</div>)\s*(<div class="check")', r'\1\n</div>\n\2', html)
    
    # --- 5. Wrap 30词 in step full within steps ---
    # Find each 30词 that's OUTSIDE a step div and move it into the last steps as step full
    # Strategy: find 30词 that appears after steps close (</div>\n</div>) and wrap it
    
    # Find all 30词
    for m in list(re.finditer('今日30词', html)):
        pos = m.start()
        # Check if this 30词 is inside a step div
        before = html[max(0, pos-500):pos]
        # Find last step opening and last steps close
        last_step_open = before.rfind('<div class="step')
        last_steps_open = before.rfind('<div class="steps">')
        last_steps_close = before.rfind('</div>\n</div>')
        
        # If the word box is AFTER steps close but BEFORE next structural element
        if last_steps_close > max(last_step_open, last_steps_open) and last_steps_close > pos - 500:
            # Word box is outside steps - wrap it
            # Find the gray box HTML
            gb_start = html.rfind('<div style="background:#f0f0f5', max(0, pos-100), pos)
            if gb_start < 0:
                continue
            
            # Find gray box end
            after_gb = html[pos:]
            divs = list(re.finditer(r'</div>', after_gb[:10000]))
            gb_end = -1
            for d in divs:
                after_d = after_gb[d.end():d.end()+30].lstrip()
                if after_d.startswith('</div>') or after_d.startswith('<h3') or after_d.startswith('<div class="check"') or after_d.startswith('<!--'):
                    gb_end = pos + d.end()
                    break
            
            if gb_end < 0 and divs:
                gb_end = pos + divs[-1].end()
            if gb_end < pos:
                continue
            
            gray_box = html[gb_start:gb_end]
            wrapped = f'<div class="step full"><h4><span class="dot" style="background:var(--green)"></span>📝 今日30词</h4>\n{gray_box}\n</div>\n'
            
            # Insert BEFORE the steps close
            insert_pos = last_steps_close
            new_section = html[:gb_start] + html[gb_end:]
            new_section = new_section[:insert_pos] + wrapped + new_section[insert_pos:]
            html = new_section
            break  # one fix per iteration (positions shift)
    
    # --- 6. 固/结 → step full ---
    for kw in ['固', '结']:
        for c in ['green', 'purple']:
            html = html.replace(
                f'<div class="step"><h4><span class="dot" style="background:var(--{c})"></span>{kw}',
                f'<div class="step full"><h4><span class="dot" style="background:var(--{c})"></span>{kw}')
    
    # --- 7. Styling ---
    html = html.replace('background:#8e8e93;color:#fff', 'background:var(--blue);color:#fff')
    html = html.replace('\u1d50', '<sup>m</sup>')
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Verify
    d = sum(len(re.findall(r'<div\b[^>]*>', l)) - len(re.findall(r'</div>', l)) for l in html.split('\n'))
    return d


if __name__ == '__main__':
    for fn in ['w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9']:
        fp = os.path.join(BASE, f'{fn}.html')
        d = fix_file(fp)
        ok = '✅' if d == 0 else f'd={d}'
        print(f'{fn}: {ok}')
