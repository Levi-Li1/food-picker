#!/usr/bin/env python3
"""rebuild_all.py - Parse guct.html day sections and rebuild with correct HTML structure."""
import re

def extract_day_sections(day_html):
    """Extract sections from a day's HTML content.
    Returns list of (h3_tag, steps_content) tuples where steps_content is everything
    between this h3 and the next section boundary."""
    sections = []
    
    # Find all h3 positions
    h3_matches = list(re.finditer(r'<h3\b[^>]*>.*?</h3>', day_html, re.DOTALL))
    
    for i, h3 in enumerate(h3_matches):
        h3_tag = h3.group(0)
        start = h3.end()
        end = h3_matches[i+1].start() if i+1 < len(h3_matches) else len(day_html)
        content = day_html[start:end]
        sections.append((h3_tag, content))
    
    return sections

def fix_day_structure(day_content):
    """Fix a single day-page's HTML structure.
    Input: entire day HTML from <div class="day-page"> to end."""
    
    # Find day-page opening and dbody
    day_open = '<div class="day-page">'
    dtop_end = day_content.find('<div class="dbody">')
    if dtop_end < 0:
        return day_content
    
    dtop_html = day_content[:dtop_end + len('<div class="dbody">')]
    remaining = day_content[dtop_end + len('<div class="dbody">'):]
    
    # Find where this day ends: look for </div>\n</div> at the end
    # But first, find all h3 sections
    sections = extract_day_sections(remaining)
    
    if not sections:
        return day_content
    
    # Rebuild: dtop + dbody-open + sections with proper closes + dbody-close + day-close
    rebuilt = dtop_html + '\n'
    
    for i, (h3_tag, scontent) in enumerate(sections):
        rebuilt += h3_tag + '\n'
        
        # Extract steps from content
        # Content may contain <div class="steps">...</div> or just step divs
        # Clean the content: keep everything, but fix closing
        
        # Remove ALL trailing </div> from this section (for non-last sections)
        # Then add back the correct number
        
        cleaned = scontent.rstrip()
        trailing_divs = 0
        while cleaned.endswith('</div>'):
            cleaned = cleaned[:-len('</div>')].rstrip()
            trailing_divs += 1
        
        if i < len(sections) - 1:
            # Non-last section: need to close step divs + steps wrapper
            # Count step divs in the original content
            steps_in_section = len(re.findall(r'<div class="step[\s">]', scontent))
            
            # Number of step div closes needed + 1 for steps wrapper
            if steps_in_section > 0:
                needed_closes = steps_in_section + 1
            else:
                needed_closes = 0  # no steps wrapper
            
            # Check if there's a <div class="check"> that was part of the content
            if 'class="check"' in cleaned:
                needed_closes += 0  # check div closes itself
            
            rebuilt += cleaned
            for _ in range(needed_closes):
                rebuilt += '\n</div>'
            rebuilt += '\n'
        else:
            # Last section: keep original content, don't modify closes
            # The day close will handle dbody+day-page
            rebuilt += cleaned
            # Don't add trailing closes - will be handled by day close
    
    # Close dbody and day-page
    rebuilt += '\n</div>\n</div>'
    
    return rebuilt

def process_week_file(template_html, week_id):
    """Build a clean week HTML file from guct.html content."""
    
    # Find the week marker
    week_start = template_html.find(f'<div class="week-marker" id="w{week_id}">')
    if week_start < 0:
        # Try alternative format
        week_start = template_html.find(f'<div class="week-marker" id="w{week_id}">')
    # If still not found, check id="wN"
    if week_start < 0:
        for wid in range(1, 10):
            week_start = template_html.find(f'<div class="week-marker" id="w{week_id}">')
            if week_start >= 0: break
    
    if week_start < 0:
        print(f'  Week {week_id} marker not found!')
        return None
    
    next_week = template_html.find('<div class="week-marker"', week_start + 1)
    week_end = next_week if next_week > 0 else template_html.rfind('</body>')
    if week_end < 0:
        week_end = len(template_html)
    
    week_content = template_html[week_start:week_end]
    return week_content

# Main execution
if __name__ == '__main__':
    import os
    base = 'C:/Users/Tebon/BangMaker/Claw'
    
    # Read guct.html
    with open(os.path.join(base, 'guct.html'), 'r', encoding='utf-8') as f:
        guct = f.read()
    
    body_start = guct.find('<body>')
    guct_body = guct[body_start:]
    
    # Process each day directly from guct
    # Split by day-page markers
    day_parts = guct_body.split('<div class="day-page">')
    
    # Rebuild each day
    rebuilt_days = []
    for i, part in enumerate(day_parts[1:], 1):
        day_html = '<div class="day-page">' + part
        # Find where this day ends (next day or end)
        next_day = day_html.find('<div class="day-page">', 1)
        if next_day < 0:
            next_day = len(day_html)
        single_day = day_html[:next_day]
        
        fixed_day = fix_day_structure(single_day)
        rebuilt_days.append((i, fixed_day))
    
    print(f'Rebuilt {len(rebuilt_days)} days')
    
    # Now create w2-w9 files using the existing build_weeks.js approach
    # but with the rebuilt day structures
    # Actually, let me just write each week file directly
    
    # Read w1.html for CSS/header/script template
    with open(os.path.join(base, 'w1.html'), 'r', encoding='utf-8') as f:
        w1 = f.read()
    
    body_idx = w1.find('<body>')
    w1_css = w1[:body_idx + 6]
    script = w1[w1.rfind('<script>function'):w1.rfind('</script>')+9]
    
    # Week config
    weeks = {
        1: ('w1', '📅 第一周（7月1日-7日）', '主题：代数基础回炉 · 每天学习时间 4h（数学2h + 英语1h + 语文/物理交替1h）', range(1, 8)),
        2: ('w2', '📅 第二周（7月8日-14日）', '主题：几何入门+全等三角形 · 每天学习时间 4h（数学2h + 物理1h + 英语1h）', range(8, 13)),
        3: ('w3', '📅 第三周（7月15日-21日）', '主题：函数入门+力学深化 · 每天学习时间 5h（数学2h + 物理1h + 英语1h + 语文1h）', range(13, 19)),
        4: ('w4', '📅 第四周（7月22日-28日）', '主题：几何综合+化学启蒙 · 每天学习时间 5h', range(19, 25)),
        5: ('w5', '📅 第五周（7月29日-8月4日）', '主题：几何证明强化+化学元素 · 每天学习时间 5.5h', range(25, 30)),
        6: ('w6', '📅 第六周（8月5日-11日）', '主题：函数提高+力学综合 · 每天学习时间 5h（数学2h + 物理1h + 英语1h + 语文1h）', range(30, 36)),
        7: ('w7', '📅 第七周（8月12日-18日）', '主题：中考真题实战 · 每天学习时间 5.5h', range(36, 43)),
        8: ('w8', '📅 第八周（8月19日-25日）', '主题：初三新课预习 · 每天学习时间 5h', range(43, 49)),
        9: ('w9', '📅 第九周（8月26日-29日）', '主题：收尾冲刺 · 错题清零+开学准备 · 每天学习时间 4h', range(49, 53)),
    }
    
    # Navigation
    def make_nav(current_w):
        week_labels = ['第一周','第二周','第三周','第四周','第五周','第六周','第七周','第八周','第九周']
        links = ''
        for i in range(9):
            wl = f'w{i+1}'
            active = wl == current_w
            links += f'<a href="{wl}.html" style="padding:6px 10px;border-radius:8px;text-decoration:none;font-weight:600;font-size:11px;background:{"var(--blue)" if active else "#e5e5ea"};color:{"#fff" if active else "#666"}">{week_labels[i]}</a>'
        return f'''<nav>
<div style="max-width:1000px;margin:0 auto;display:flex;align-items:center;gap:8px;padding:0 16px;flex-wrap:wrap">
<span class="title">📚 暑假逆袭计划</span>
<div style="display:flex;gap:4px;flex-wrap:wrap;align-items:center">{links}<a href="kaogang.html" style="padding:6px 10px;border-radius:8px;text-decoration:none;font-weight:600;font-size:11px;background:#e5e5ea;color:#666">🧠 考纲</a></div>
<a href="index.html" style="font-size:12px;color:var(--sub);text-decoration:none;margin-left:auto">📋 总览</a>
</div>
</nav>'''
    
    # Write week files
    for wk_num in range(1, 10):
        wid, label, note, day_range = weeks[wk_num]
        
        days_html = ''
        for day_num in day_range:
            if day_num <= len(rebuilt_days):
                days_html += '\n' + rebuilt_days[day_num - 1][1] + '\n'
        
        out = f'{w1_css}\n{make_nav(wid)}\n\n<div class="container">\n<div class="week-marker" id="{wid}">{label}<div class="wnote">{note}</div></div>\n{days_html}\n</div>\n{script}\n\n</body>\n</html>'
        
        filepath = os.path.join(base, f'{wid}.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(out)
        
        # Verify
        d = 0
        for line in out.split('\n'):
            d += len(re.findall(r'<div\b[^>]*>', line)) - len(re.findall(r'</div>', line))
        status = '✅' if d == 0 else f'❌ d={d}'
        print(f'{wid}.html: {len(out)}B, {status}')
    
    print('\nDone rebuilding all weeks!')
