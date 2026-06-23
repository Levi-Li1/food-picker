#!/usr/bin/env python3
"""one_shot_fix.py - 一次性修复 build_weeks.js 输出的所有问题"""
import re, os

BASE = 'C:/Users/Tebon/BangMaker/Claw'

# Week config (matches build_weeks.js)
WEEK_TOPICS = {
    'w2': '主题：几何入门+全等三角形 · 每天学习时间 4h（数学2h + 物理1h + 英语1h）',
    'w3': '主题：函数入门+力学深化 · 每天学习时间 5h（数学2h + 物理1h + 英语1h + 语文1h）',
    'w4': '主题：几何综合+化学启蒙 · 每天学习时间 5h',
    'w5': '主题：几何证明强化+化学元素 · 每天学习时间 5.5h',
    'w6': '主题：函数提高+力学综合 · 每天学习时间 5h（数学2h + 物理1h + 英语1h + 语文1h）',
    'w7': '主题：中考真题实战 · 每天学习时间 5.5h（真题模拟3-4h + 错题分析1-2h）',
    'w8': '主题：初三新课预习 · 每天学习时间 5h（数学2h + 物理/化学交替1h + 英语1h + 语文1h）',
    'w9': '主题：收尾冲刺 · 错题清零+开学准备 · 每天学习时间 4h',
}

def fix_file(fn):
    fp = os.path.join(BASE, f'{fn}.html')
    with open(fp, 'r', encoding='utf-8') as f:
        h = f.read()
    
    # --- 1. Fix week-marker: nuke everything after wnote text ---
    wm = h.find('class="week-marker"')
    topic = WEEK_TOPICS.get(fn, '')
    end = h.find(topic, wm) + len(topic)
    dp = h.find('<div class="day-page">', end)
    if dp > end:
        h = h[:end] + '</div>\n</div>\n\n' + h[dp:]
    
    # --- 2. Split dbody+h3 on same line ---
    h = h.replace('<div class="dbody"><h3', '<div class="dbody">\n<h3')
    
    # --- 3. Wrap steps: </h3><div class="step → </h3><div class="steps"><div class="step ---
    h = re.sub(r'</h3>\s*<div class="step', '</h3>\n<div class="steps">\n<div class="step', h)
    
    # --- 4. Add steps close before each subsequent <h3> ---
    # Match: </div></div><h3 OR </div></div>\n<h3
    h = re.sub(r'(</div>\s*</div>)\s*(<h3)', r'\1\n</div>\n\2', h)
    
    # Also close steps before <div class="check">
    h = re.sub(r'(</div>\s*</div>)\s*(<div class="check")', r'\1\n</div>\n\2', h)
    
    # --- 5. Fix missing step+steps close on same-line h3 ---
    # Pattern: content...</p></div><h3 → need step close + steps close
    h = re.sub(r'</p></div><h3', '</p></div>\n</div>\n</div>\n<h3', h)
    # Pattern: ...</div><h3 (single close before h3 on same massive line)
    # Only fix this if the line has many opens (indicating inline content)
    # Already handled by fix #4, but some may need step close too
    
    # --- 6. Fix double wrapped steps: </div></div></div></div><h3 → </div></div></div><h3 ---
    h = re.sub(r'(</div>\s*</div>\s*</div>)\s*(</div>)\s*(<h3)', r'\1\n\3', h)
    h = re.sub(r'(</div>\s*</div>\s*</div>)\s*(</div>)\s*(<div class="check")', r'\1\n\3', h)
    
    # --- 7. 固/结 → step full ---
    for kw in ['固', '结']:
        for c in ['green', 'purple']:
            h = h.replace(
                f'<div class="step"><h4><span class="dot" style="background:var(--{c})"></span>{kw}',
                f'<div class="step full"><h4><span class="dot" style="background:var(--{c})"></span>{kw}')
    
    # --- 8. Styling ---
    h = h.replace('background:#8e8e93;color:#fff', 'background:var(--blue);color:#fff')
    h = h.replace('\u1d50', '<sup>m</sup>')
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(h)
    
    return h

# Run fix on all files
results = {}
for fn in ['w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9']:
    html = fix_file(fn)
    d = sum(len(re.findall(r'<div\b[^>]*>', l)) - len(re.findall(r'</div>', l)) for l in html.split('\n'))
    steps = html.count('<div class="steps">')
    ful = html.count('<div class="step full">')
    stray = html[html.find('week-marker'):html.find('<div class="day-page">', html.find('week-marker'))].count('今日30词')
    results[fn] = (d, stray, steps, ful)
    ok = '✅' if d == 0 and stray == 0 else f'd={d}'
    if stray: ok += f' stray={stray}'
    print(f'{fn}: {ok}  steps={steps}  full={ful}')

print('\nDone. All files ready.')
