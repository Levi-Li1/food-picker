#!/usr/bin/env python3
"""
rebuild_v2.py - 从 build_weeks.js 输出提取内容，用 w1 结构模板重建每个 day。
原则：不再修复旧 HTML，而是提取内容 + 用干净模板渲染。
"""
import re, os

BASE = 'C:/Users/Tebon/BangMaker/Claw'

def extract_day_content(day_html):
    """从 build_weeks.js 生成的 day HTML 中提取结构化内容"""
    result = {
        'date': '', 'subjects': '', 'goal': '',
        'sections': [],  # [{h3, steps: [{title, content, is_full}]}]
        'check': '',
        'word_box': '',
    }
    
    # Extract dtop info
    date_m = re.search(r'<div>([^<]+)</div>', day_html)
    subjects_m = re.search(r'font-size:12px">([^<]+)</div>', day_html)
    if date_m: result['date'] = date_m.group(1)
    if subjects_m: result['subjects'] = subjects_m.group(1)
    
    # Extract goal
    goal_m = re.search(r'<div class="goal"><b>🎯 今日目标</b>：([^<]*)</div>', day_html)
    if goal_m: result['goal'] = goal_m.group(1)
    
    # Find dbody content
    dbody_start = day_html.find('<div class="dbody">')
    if dbody_start < 0:
        return result
    
    dbody_content = day_html[dbody_start + len('<div class="dbody">'):]
    
    # Split by h3 sections
    h3_splits = re.split(r'(<h3\b[^>]*>.*?</h3>)', dbody_content)
    
    # h3_splits[0] = content before first h3
    # h3_splits[1] = first h3 tag
    # h3_splits[2] = content after first h3 until next h3
    # etc.
    
    sections = []
    i = 1  # skip content before first h3 (should be goal)
    while i + 1 < len(h3_splits):
        h3_tag = h3_splits[i]
        content = h3_splits[i + 1]
        
        # Extract step cards from this content
        steps = []
        step_splits = re.split(r'(<div class="step[\s"][^>]*>)', content)
        
        current_step_html = ''
        current_step_open = ''
        in_step = False
        
        for part in step_splits:
            if part.startswith('<div class="step'):
                if in_step:
                    # Close previous step
                    steps.append(extract_step(current_step_open, current_step_html))
                current_step_open = part
                current_step_html = part
                in_step = True
            elif in_step:
                current_step_html += part
        
        if in_step and current_step_html:
            steps.append(extract_step(current_step_open, current_step_html))
        
        if steps:
            sections.append({'h3': h3_tag, 'steps': steps})
        
        i += 2
    
    # Handle content after last h3 (check div, word box)
    if i < len(h3_splits):
        remaining = h3_splits[i] if i < len(h3_splits) else ''
        
        # Extract check
        check_m = re.search(r'<div class="check">(.*?)</div>', remaining, re.DOTALL)
        if check_m:
            result['check'] = '<div class="check">' + check_m.group(1) + '</div>'
        
        # Extract word box
        wb_m = re.search(r'(<div style="background:#f0f0f5[^>]*>.*?</div>\s*</div>\s*</div>)', remaining, re.DOTALL)
        if wb_m:
            result['word_box'] = wb_m.group(1)
        else:
            wb_m = re.search(r'(<div style="background:#f0f0f5[^>]*>.*?</div>)', remaining, re.DOTALL)
            if wb_m:
                result['word_box'] = wb_m.group(1)
    
    result['sections'] = sections
    return result


def extract_step(open_tag, full_html):
    """Extract step title and content"""
    title_m = re.search(r'<h4><span[^>]*></span>([^<]+)</h4>', full_html)
    title = title_m.group(1) if title_m else ''
    
    is_full = 'step full' in open_tag or 'step-full' in open_tag
    if not is_full:
        is_full = any(kw in title for kw in ['固', '结', '单词', '默写', '方法总结'])
    
    # Extract content between h4 close and step close
    h4_end = full_html.find('</h4>')
    if h4_end > 0:
        content = full_html[h4_end + 5:].rstrip()
        # Remove trailing </div> (step close)
        while content.endswith('</div>'):
            content = content[:-6].rstrip()
    else:
        content = full_html
    
    return {'title': title, 'content': content, 'is_full': is_full}


def render_day(day, num):
    """Render a day with w1-standard structure"""
    lines = []
    lines.append('<div class="day-page">')
    
    # dtop
    lines.append(f'<div class="dtop"><div class="dnum">Day {num}</div><div class="dinfo"><div>{day["date"]}</div><div style="font-size:12px">{day["subjects"]}</div></div></div>')
    
    # dbody
    lines.append('<div class="dbody">')
    
    # goal (if exists)
    if day['goal']:
        lines.append(f'<div class="goal"><b>🎯 今日目标</b>：{day["goal"]}</div>')
    
    # sections
    for sec in day['sections']:
        lines.append(sec['h3'])
        lines.append('<div class="steps">')
        
        for step in sec['steps']:
            cls = 'step full' if step['is_full'] else 'step'
            title_color = 'var(--green)' if '固' in step['title'] else ('var(--purple)' if '结' in step['title'] else 'var(--blue)')
            if '物理' in sec['h3']: title_color = 'var(--orange)'
            
            lines.append(f'<div class="{cls}"><h4><span class="dot" style="background:{title_color}"></span>{step["title"]}</h4>')
            lines.append(step['content'])
            lines.append('</div>')  # close step
        
        lines.append('</div>')  # close steps
    
    # word box (if exists, put it in last section or as standalone)
    if day['word_box']:
        lines.append(day['word_box'])
    
    # check (if exists)
    if day['check']:
        lines.append(day['check'])
    
    lines.append('</div>')  # close dbody
    lines.append('</div>')  # close day-page
    
    return '\n'.join(lines)


def build_week(wid, config):
    """Build a complete week file"""
    # Read the generated file from build_weeks.js
    fp = os.path.join(BASE, f'{wid}.html')
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Extract CSS, nav, script from w1.html
    with open(os.path.join(BASE, 'w1.html'), 'r', encoding='utf-8') as f:
        w1 = f.read()
    
    body_idx = w1.find('<body>')
    css_header = w1[:body_idx + 6]
    script = w1[w1.rfind('<script>function'):w1.rfind('</script>') + 9]
    
    # Build nav
    labels = ['第一周','第二周','第三周','第四周','第五周','第六周','第七周','第八周','第九周']
    nav_links = ''
    for i in range(9):
        wl = f'w{i+1}'
        active = wl == wid
        nav_links += f'<a href="{wl}.html" style="padding:6px 10px;border-radius:8px;text-decoration:none;font-weight:600;font-size:11px;background:{"var(--blue)" if active else "#e5e5ea"};color:{"#fff" if active else "#666"}">{labels[i]}</a>'
    
    nav = f'''<nav>
<div style="max-width:1000px;margin:0 auto;display:flex;align-items:center;gap:8px;padding:0 16px;flex-wrap:wrap">
<span class="title">📚 暑假逆袭计划</span>
<div style="display:flex;gap:4px;flex-wrap:wrap;align-items:center">{nav_links}<a href="kaogang.html" style="padding:6px 10px;border-radius:8px;text-decoration:none;font-weight:600;font-size:11px;background:#e5e5ea;color:#666">🧠 考纲</a></div>
<a href="index.html" style="font-size:12px;color:var(--sub);text-decoration:none;margin-left:auto">📋 总览</a>
</div>
</nav>'''
    
    # Week-marker
    wk_marker = f'<div class="week-marker" id="{wid}">{config["label"]}<div class="wnote">{config["note"]}</div></div>'
    
    # Process each day in the generated file
    days_html = ''
    day_starts = [m.start() for m in re.finditer(r'<div class="day-page">', html)]
    
    # Extract day numbers
    day_nums = []
    for m in re.finditer(r'<div class="dnum">Day (\d+)</div>', html):
        day_nums.append(int(m.group(1)))
    
    for i, ds in enumerate(day_starts):
        de = day_starts[i + 1] if i + 1 < len(day_starts) else len(html)
        day_html = html[ds:de]
        
        dn = day_nums[i] if i < len(day_nums) else 0
        
        # Extract structured content
        day_content = extract_day_content(day_html)
        
        # Render with clean structure
        if day_content['sections']:
            clean_day = render_day(day_content, dn)
            days_html += '\n' + clean_day + '\n'
    
    # Assembly
    output = f'{css_header}\n{nav}\n\n<div class="container">\n{wk_marker}\n{days_html}\n</div>\n{script}\n\n</body>\n</html>'
    
    # Styling
    output = output.replace('background:#8e8e93;color:#fff', 'background:var(--blue);color:#fff')
    output = output.replace('\u1d50', '<sup>m</sup>')
    
    # Write
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(output)
    
    # Verify
    d = sum(len(re.findall(r'<div\b[^>]*>', l)) - len(re.findall(r'</div>', l)) for l in output.split('\n'))
    steps = output.count('<div class="steps">')
    return d, steps


WEEK_CONFIG = {
    'w2': {'label': '📅 第二周（7月8日-14日）', 'note': '主题：几何入门+全等三角形 · 每天学习时间 4h（数学2h + 物理1h + 英语1h）'},
    'w3': {'label': '📅 第三周（7月15日-21日）', 'note': '主题：函数入门+力学深化 · 每天学习时间 5h（数学2h + 物理1h + 英语1h + 语文1h）'},
    'w4': {'label': '📅 第四周（7月22日-28日）', 'note': '主题：几何综合+化学启蒙 · 每天学习时间 5h'},
    'w5': {'label': '📅 第五周（7月29日-8月4日）', 'note': '主题：几何证明强化+化学元素 · 每天学习时间 5.5h'},
    'w6': {'label': '📅 第六周（8月5日-11日）', 'note': '主题：函数提高+力学综合 · 每天学习时间 5h（数学2h + 物理1h + 英语1h + 语文1h）'},
    'w7': {'label': '📅 第七周（8月12日-18日）', 'note': '主题：中考真题实战 · 每天学习时间 5.5h（真题模拟3-4h + 错题分析1-2h）'},
    'w8': {'label': '📅 第八周（8月19日-25日）', 'note': '主题：初三新课预习 · 每天学习时间 5h（数学2h + 物理/化学交替1h + 英语1h + 语文1h）'},
    'w9': {'label': '📅 第九周（8月26日-29日）', 'note': '主题：收尾冲刺 · 错题清零+开学准备 · 每天学习时间 4h'},
}

if __name__ == '__main__':
    for wid, cfg in WEEK_CONFIG.items():
        d, steps = build_week(wid, cfg)
        ok = '✅' if d == 0 else f'd={d}'
        print(f'{wid}: {ok}  steps={steps}')
    print('\nDone.')
