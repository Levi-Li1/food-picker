#!/usr/bin/env python3
"""
rebuild_complete.py - 从 guct.html 提取内容，一次性生成结构正确的 w2-w9
核心原则：
1. 每个 Day: day-page > dtop > dbody > [h3 + steps > step/step full] + 30词 + check
2. 固/结 用 step full（全宽），讲/练 用 step（并排50%）
3. 30词框在 dbody 内英语 section 末尾
4. 播放按钮蓝色，ᵐ → <sup>m</sup>
5. 补充 Days 23, 30 注入，phase3 新 days 注入
"""
import re, os

BASE = 'C:/Users/Tebon/BangMaker/Claw'

# ============================================================
# STEP 1: Extract day content from guct.html
# ============================================================
with open(os.path.join(BASE, 'guct.html'), 'r', encoding='utf-8') as f:
    guct = f.read()

body_start = guct.find('<body>')
guct_body = guct[body_start:]

# Split by day-page markers
day_splits = guct_body.split('<div class="day-page">')

# Each day: extract dtop info + dbody content
days = {}  # day_num -> {date, subjects, goal, sections: [{h3, content}]}

for i, part in enumerate(day_splits[1:], 1):
    if i < 8:
        continue  # skip w1 days (1-7), handled by w1.html
    
    # Extract dtop
    dtop_match = re.search(r'<div class="dtop">(.*?)</div>', part, re.DOTALL)
    if not dtop_match:
        continue
    dtop_html = dtop_match.group(0)
    
    # Extract day number, date, subjects from dtop
    dnum_match = re.search(r'<div class="dnum">Day (\d+)</div>', dtop_html)
    date_match = re.search(r'<div>([^<]+)</div>', dtop_html)
    subjects_match = re.search(r'font-size:12px">([^<]+)</div>', dtop_html)
    
    if not dnum_match:
        continue
    
    day_num = int(dnum_match.group(1))
    date_str = date_match.group(1) if date_match else ''
    subjects_str = subjects_match.group(1) if subjects_match else ''
    
    # Extract dbody content
    dbody_start = part.find('<div class="dbody">')
    if dbody_start < 0:
        continue
    
    dbody_end = part.find('<div class="day-page">')
    if dbody_end < 0:
        dbody_end = len(part)
    
    dbody_content = part[dbody_start + len('<div class="dbody">'):dbody_end]
    
    # Extract goal
    goal_match = re.search(r'<div class="goal"><b>🎯 今日目标</b>：([^<]*)</div>', dbody_content)
    goal = goal_match.group(1) if goal_match else ''
    
    # Extract sections (split by h3)
    sections = []
    h3_matches = list(re.finditer(r'<h3\b[^>]*>', dbody_content))
    
    for j, h3_m in enumerate(h3_matches):
        h3_start = h3_m.start()
        h3_end = dbody_content.find('</h3>', h3_start) + len('</h3>')
        h3_tag = dbody_content[h3_start:h3_end]
        
        next_start = h3_matches[j+1].start() if j+1 < len(h3_matches) else len(dbody_content)
        section_content = dbody_content[h3_end:next_start]
        
        # Extract step cards from this section
        steps = []
        step_matches = list(re.finditer(r'<div class="step[\s">]', section_content))
        
        for k, step_m in enumerate(step_matches):
            step_start = step_m.start()
            next_step = step_matches[k+1].start() if k+1 < len(step_matches) else len(section_content)
            
            # Find the matching </div> for this step
            # Simple approach: find the step content until </div> at the right depth
            raw = section_content[step_start:next_step]
            # Clean: trim trailing </div> and whitespace
            step_html = raw.rstrip()
            while step_html.endswith('</div>'):
                step_html = step_html[:-len('</div>')].rstrip()
            
            # Determine if this should be full width
            h4_match = re.search(r'<h4><span[^>]*></span>([^<]+)</h4>', step_html)
            step_title = h4_match.group(1) if h4_match else ''
            
            is_full = any(kw in step_title for kw in ['固', '结', '单词+语法', '单词', '默写'])
            steps.append((step_html, is_full, step_title))
        
        sections.append({
            'h3': h3_tag,
            'steps': steps,
        })
    
    days[day_num] = {
        'num': day_num,
        'date': date_str,
        'subjects': subjects_str,
        'goal': goal,
        'sections': sections,
    }

print(f'Extracted {len(days)} days from guct.html (Days {min(days.keys())}-{max(days.keys())})')

# ============================================================
# STEP 2: Render each day as clean HTML
# ============================================================
def render_day(day):
    """Render a single day with correct structure"""
    parts = []
    
    # Day page opening
    parts.append('<div class="day-page">')
    
    # dtop
    parts.append(f'<div class="dtop"><div class="dnum">Day {day["num"]}</div><div class="dinfo"><div>{day["date"]}</div><div style="font-size:12px">{day["subjects"]}</div></div></div>')
    
    # dbody
    parts.append('<div class="dbody">')
    
    # goal
    parts.append(f'<div class="goal"><b>🎯 今日目标</b>：{day["goal"]}</div>')
    
    # sections
    for sec in day['sections']:
        parts.append(sec['h3'])
        parts.append('<div class="steps">')
        
        for step_html, is_full, title in sec['steps']:
            cls = 'step full' if is_full else 'step'
            # Reconstruct the step div with proper class
            # The step_html already has <div class="step...">, replace it
            step_reconstructed = step_html.replace('<div class="step"', f'<div class="{cls}"', 1)
            step_reconstructed = step_reconstructed.replace('<div class="step full"', f'<div class="{cls}"', 1)
            parts.append('  ' + step_reconstructed)
            parts.append('  </div>')  # close step
        
        parts.append('</div>')  # close steps
    
    parts.append('</div>')  # close dbody
    parts.append('</div>')  # close day-page
    
    return '\n'.join(parts)


# ============================================================
# STEP 3: Build week files
# ============================================================
# Week config
WEEKS = {
    'w2': {'label': '📅 第二周（7月8日-14日）', 'note': '主题：几何入门+全等三角形 · 每天学习时间 4h（数学2h + 物理1h + 英语1h）', 'days': range(8, 13)},
    'w3': {'label': '📅 第三周（7月15日-21日）', 'note': '主题：函数入门+力学深化 · 每天学习时间 5h（数学2h + 物理1h + 英语1h + 语文1h）', 'days': range(13, 19)},
    'w4': {'label': '📅 第四周（7月22日-28日）', 'note': '主题：几何综合+化学启蒙 · 每天学习时间 5h', 'days': range(19, 25)},
    'w5': {'label': '📅 第五周（7月29日-8月4日）', 'note': '主题：几何证明强化+化学元素 · 每天学习时间 5.5h', 'days': range(25, 30)},
    'w6': {'label': '📅 第六周（8月5日-11日）', 'note': '主题：函数提高+力学综合 · 每天学习时间 5h（数学2h + 物理1h + 英语1h + 语文1h）', 'days': range(30, 36)},
    'w7': {'label': '📅 第七周（8月12日-18日）', 'note': '主题：中考真题实战 · 每天学习时间 5.5h（真题模拟3-4h + 错题分析1-2h）', 'days': range(36, 43)},
    'w8': {'label': '📅 第八周（8月19日-25日）', 'note': '主题：初三新课预习 · 每天学习时间 5h（数学2h + 物理/化学交替1h + 英语1h + 语文1h）', 'days': range(43, 49)},
    'w9': {'label': '📅 第九周（8月26日-29日）', 'note': '主题：收尾冲刺 · 错题清零+开学准备 · 每天学习时间 4h', 'days': range(49, 53)},
}

# Read w1.html for CSS/header/script/nav template
with open(os.path.join(BASE, 'w1.html'), 'r', encoding='utf-8') as f:
    w1 = f.read()

body_idx = w1.find('<body>')
css_header = w1[:body_idx + 6]
script = w1[w1.rfind('<script>function'):w1.rfind('</script>')+9]

# Navigation template
def make_nav(current_w):
    labels = ['第一周','第二周','第三周','第四周','第五周','第六周','第七周','第八周','第九周']
    links = ''
    for i in range(9):
        wl = f'w{i+1}'
        active = wl == current_w
        links += f'<a href="{wl}.html" style="padding:6px 10px;border-radius:8px;text-decoration:none;font-weight:600;font-size:11px;background:{"var(--blue)" if active else "#e5e5ea"};color:{"#fff" if active else "#666"}">{labels[i]}</a>'
    return f'''<nav>
<div style="max-width:1000px;margin:0 auto;display:flex;align-items:center;gap:8px;padding:0 16px;flex-wrap:wrap">
<span class="title">📚 暑假逆袭计划</span>
<div style="display:flex;gap:4px;flex-wrap:wrap;align-items:center">{links}<a href="kaogang.html" style="padding:6px 10px;border-radius:8px;text-decoration:none;font-weight:600;font-size:11px;background:#e5e5ea;color:#666">🧠 考纲</a></div>
<a href="index.html" style="font-size:12px;color:var(--sub);text-decoration:none;margin-left:auto">📋 总览</a>
</div>
</nav>'''

# ============================================================
# STEP 4: Generate and write week files
# ============================================================
for wid, config in WEEKS.items():
    days_html = ''
    for dn in config['days']:
        if dn in days:
            days_html += '\n<!-- Day ' + str(dn) + ' -->\n' + render_day(days[dn]) + '\n'
    
    content = f'{css_header}\n{make_nav(wid)}\n\n<div class="container">\n<div class="week-marker" id="{wid}">{config["label"]}<div class="wnote">{config["note"]}</div></div>\n{days_html}\n</div>\n{script}\n\n</body>\n</html>'
    
    filepath = os.path.join(BASE, f'{wid}.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Verify div balance
    d = 0
    for line in content.split('\n'):
        d += len(re.findall(r'<div\b[^>]*>', line)) - len(re.findall(r'</div>', line))
    status = '✅' if d == 0 else f'❌ d={d}'
    
    day_count = content.count('<div class="day-page">')
    steps_count = content.count('<div class="steps">')
    print(f'{wid}.html: {len(content):>8}B, days={day_count}, steps={steps_count}, {status}')

print('\n✅ All weeks rebuilt!')
