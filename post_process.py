#!/usr/bin/env python3
"""
post_process.py - 全面后处理 w2-w9：删除stray词框、加steps容器、固/结全宽、按钮蓝色、sup m
在 build_weeks.js 生成后运行
"""
import re, os, sys

BASE = 'C:/Users/Tebon/BangMaker/Claw'

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # --- Fix 1: Delete stray content between week-marker and first day-page ---
    # Find the week-marker div and remove everything between its close and first day-page
    wk = html.find('class="week-marker"')
    if wk > 0:
        # Find week-marker closing: wnote close + week-marker close
        wnote = html.find('<div class="wnote">', wk)
        if wnote > 0:
            wnote_close = html.find('</div>', wnote)
            wk_close = html.find('</div>', wnote_close + 6)
            fd = html.find('<div class="day-page">', wk_close)
            if fd > wk_close:
                stray = html[wk_close + 6:fd].strip()
                if stray:
                    html = html[:wk_close + 6] + '\n' + html[fd:]
    
    # --- Fix 2: Remove orphan 30词 between days (not inside dbody) ---
    # These appear as stray gray boxes that got separated from their parent day
    # Pattern: after </div></div> (day close), before next <div class="day-page">
    day_markers = [m.start() for m in re.finditer(r'<div class="day-page">', html)]
    for i in range(len(day_markers) - 1):
        between = html[day_markers[i]:day_markers[i+1]]
        # Find the day close: last </div>\n</div> before next day-page
        day_close = between.rfind('</div>\n</div>')
        if day_close > 0:
            after_close = between[day_close + len('</div>\n</div>'):]
            if '今日30词' in after_close or 'background:#f0f0f5' in after_close:
                # Remove stray content between days
                abs_start = day_markers[i] + day_close + len('</div>\n</div>')
                abs_end = day_markers[i+1]
                html = html[:abs_start] + '\n' + html[abs_end:]
    
    # --- Fix 3: Wrap step divs in <div class="steps"> ---
    # Pattern: </h3><div class="step → </h3>\n<div class="steps">\n<div class="step
    html = re.sub(r'</h3><div class="step', '</h3>\n<div class="steps">\n<div class="step', html)
    
    # Close steps wrapper before next h3 or check
    def add_steps_close(m):
        return m.group(1) + '\n</div>\n' + m.group(2)
    
    html = re.sub(r'(</div>\s*</div>)\s*(<h3)', add_steps_close, html)
    html = re.sub(r'(</div>\s*</div>)\s*(<div class="check")', add_steps_close, html)
    
    # --- Fix 4: 固/结 → step full ---
    for kw in ['固', '结']:
        # Pattern: <div class="step"><h4><span ...>固</span>...</h4>
        old = f'<div class="step"><h4><span class="dot" style="background:var(--green)"></span>{kw}'
        new = f'<div class="step full"><h4><span class="dot" style="background:var(--green)"></span>{kw}'
        html = html.replace(old, new)
        
        old2 = f'<div class="step"><h4><span class="dot" style="background:var(--purple)"></span>{kw}'
        new2 = f'<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>{kw}'
        html = html.replace(old2, new2)
    
    # --- Fix 5: Styling ---
    html = html.replace('background:#8e8e93;color:#fff', 'background:var(--blue);color:#fff')
    html = html.replace('ᵐ', '<sup>m</sup>')
    
    # --- Fix 6: Balance divs ---
    # Remove excess </div></div> patterns that may have been created
    # After adding steps closes, some places may have double closes
    html = re.sub(r'(</div>\s*</div>\s*</div>)\s*(</div>)\s*(<h3)', r'\1\n\3', html)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Verify
    d = 0
    bad_h3 = 0
    for line in html.split('\n'):
        d += len(re.findall(r'<div\b[^>]*>', line)) - len(re.findall(r'</div>', line))
        if '<h3' in line and d <= 0:
            bad_h3 += 1
    
    steps = html.count('<div class="steps">')
    full = html.count('<div class="step full">')
    
    return d, bad_h3, steps, full


if __name__ == '__main__':
    results = {}
    for fn in ['w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9']:
        fp = os.path.join(BASE, f'{fn}.html')
        d, bad, steps, full = fix_file(fp)
        results[fn] = (d, bad, steps, full)
        ok = '✅' if d == 0 and bad == 0 else f'❌'
        print(f'{fn}: d={d}, h3≤0={bad}, steps={steps}, full={full} {ok}')
