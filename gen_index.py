#!/usr/bin/env python3
"""Generate standardized index.html with week-day-subject-wordlist hierarchy."""
import re, glob

weeks = {}
for fname in sorted(glob.glob('C:/Users/Tebon/BangMaker/Claw/w*.html')):
    if 'test' in fname: continue
    wn = int(re.search(r'w(\d)', fname).group(1))
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    
    days = list(re.finditer(r'Day (\d[^<]*)</div>', c))
    week_data = []
    
    for i, dm in enumerate(days):
        dn = dm.group(1)
        de = days[i+1].start() if i+1 < len(days) else len(c)
        chunk = c[dm.start():de]
        
        date_m = re.search(r'<div>([\d月日]+ [\u4e00-\u9fff]+)</div>', chunk)
        date_str = date_m.group(1) if date_m else ''
        
        h3s = re.findall(r'<h3[^>]*>([^<]*)</h3>', chunk)
        subjects = []
        for h in h3s:
            for s in ['数学', '物理', '英语', '化学', '语文', '道法', '历史']:
                if s in h:
                    parts = h.split('\u00b7')
                    topic = parts[-1].strip() if len(parts) > 1 else h.strip()
                    topic = re.sub(r'\uff08[\d.]+h\uff09', '', topic).strip()
                    subjects.append((s, topic))
                    break
        
        has_words = '今日30词' in chunk
        word_count = chunk.count('min-width:80px')
        
        week_data.append({'day': dn, 'date': date_str, 'subjects': subjects,
                         'has_words': has_words, 'word_count': word_count})
    
    weeks[wn] = week_data

week_labels = {
    1: ('第一周（7月1日-7日）', '代数基础回炉'),
    2: ('第二周（7月8日-14日）', '几何入门+全等三角形'),
    3: ('第三周（7月15日-21日）', '函数入门+力学深化'),
    4: ('第四周（7月22日-28日）', '几何综合+化学启蒙'),
    5: ('第五周（7月29日-8月4日）', '几何证明强化+化学元素'),
    6: ('第六周（8月5日-11日）', '函数提高+力学综合'),
    7: ('第七周（8月12日-18日）', '中考真题实战'),
    8: ('第八周（8月19日-25日）', '初三新课预习'),
    9: ('第九周（8月26日-29日）', '收尾冲刺·开学准备'),
}

subj_emoji = {'数学': '📖', '物理': '⚡', '英语': '🔤',
              '化学': '🧪', '语文': '📚', '道法': '⚖️', '历史': '🏛️'}
subj_color = {'数学': 'var(--blue)', '物理': 'var(--orange)', '英语': 'var(--green)',
              '化学': 'var(--purple)', '语文': 'var(--red)', '道法': '#e91e63', '历史': '#795548'}

# HTML template
html_parts = []

html_parts.append('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>初二升初三 · 暑假60天逆袭计划 · 总览</title>
<style>
:root{--blue:#007aff;--red:#ff3b30;--green:#34c759;--orange:#ff9500;--purple:#af52de;--bg:#f5f5f7;--card:#fff;--text:#1d1d1f;--sub:#86868b}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);line-height:1.7;font-size:14px}
.container{max-width:1100px;margin:0 auto;padding:16px}
h1{text-align:center;font-size:28px;padding:24px 0 4px}
.subtitle{text-align:center;color:var(--sub);font-size:13px;margin-bottom:8px}
nav{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.95);backdrop-filter:blur(20px);border-bottom:1px solid #e5e5ea;padding:8px 0;margin-bottom:16px}
nav a{padding:6px 12px;border-radius:8px;text-decoration:none;font-weight:600;font-size:12px;background:#e5e5ea;color:#666;margin:0 2px}
nav a.active{background:var(--blue);color:#fff}
nav .nav-inner{max-width:1100px;margin:0 auto;display:flex;align-items:center;gap:4px;padding:0 16px;flex-wrap:wrap}

.week-card{background:var(--card);border-radius:16px;margin-bottom:20px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.06)}
.week-header{background:linear-gradient(135deg,var(--blue),var(--purple));color:#fff;padding:16px 20px;display:flex;justify-content:space-between;align-items:center}
.week-header h2{font-size:20px}
.week-header .wtheme{font-size:13px;opacity:.85}
.week-body{padding:16px}
.day-row{display:grid;grid-template-columns:80px 100px 1fr 80px;gap:8px;align-items:center;padding:10px 12px;border-bottom:1px solid #f0f0f5;font-size:13px}
.day-row:last-child{border-bottom:none}
.day-row:hover{background:#f8f8fa;border-radius:8px}
.day-num{font-weight:700;color:var(--blue);font-size:15px}
.day-date{color:var(--sub);font-size:12px}
.day-subjects{display:flex;gap:4px;flex-wrap:wrap}
.subj-tag{padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600}
.day-words{text-align:center;font-size:11px;color:var(--sub)}
.day-words .has{color:var(--green);font-weight:600}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:20px}
.stat-card{background:var(--card);border-radius:12px;padding:16px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.04)}
.stat-card .num{font-size:32px;font-weight:800;color:var(--blue)}
.stat-card .label{font-size:12px;color:var(--sub);margin-top:4px}
.footer{text-align:center;color:var(--sub);font-size:12px;padding:20px}
</style>
</head>
<body>
<nav><div class="nav-inner">
<span style="font-weight:700;font-size:15px;margin-right:8px">📚 暑假逆袭计划</span>
''')

for wn in range(1, 10):
    html_parts.append(f'<a href="w{wn}.html">第{wn}周</a>')
html_parts.append('<a href="kaogang.html">🧠 考纲</a>')
html_parts.append('<a href="index.html" class="active">📋 总览</a>')
html_parts.append('</div></nav>\n<div class="container">\n')
html_parts.append('<h1>📋 60天逆袭计划 · 总览</h1>\n')
html_parts.append('<p class="subtitle">初二升初三暑假 · 全科系统复习+初三预习</p>\n')

# Stats
total_d = sum(len(w) for w in weeks.values())
total_w = sum(sum(d['word_count'] for d in w) for w in weeks.values())
total_wl = sum(sum(1 for d in w if d['has_words']) for w in weeks.values())

html_parts.append('<div class="stats">\n')
html_parts.append(f'<div class="stat-card"><div class="num">{total_d}</div><div class="label">总天数</div></div>\n')
html_parts.append(f'<div class="stat-card"><div class="num">9</div><div class="label">总周数</div></div>\n')
html_parts.append(f'<div class="stat-card"><div class="num">{total_wl}</div><div class="label">含词表天数</div></div>\n')
html_parts.append(f'<div class="stat-card"><div class="num">{total_w}</div><div class="label">词条总数</div></div>\n')
html_parts.append(f'<div class="stat-card"><div class="num">349</div><div class="label">练习题数</div></div>\n')
html_parts.append(f'<div class="stat-card"><div class="num">7</div><div class="label">覆盖科目</div></div>\n')
html_parts.append('</div>\n')

# Week cards
for wn in range(1, 10):
    if wn not in weeks:
        continue
    label, theme = week_labels[wn]
    wd = weeks[wn]
    
    html_parts.append('<div class="week-card">\n')
    html_parts.append(f'<div class="week-header"><h2>📅 第{wn}周</h2><span class="wtheme">{label} · {theme}</span></div>\n')
    html_parts.append('<div class="week-body">\n')
    
    for d in wd:
        subj_tags = ''
        for s, _ in d['subjects']:
            subj_tags += f'<span class="subj-tag" style="color:{subj_color.get(s,"#666")}">{subj_emoji.get(s,"")} {s}</span>'
        
        words_html = f'<span class="has">📝 {d["word_count"]}词</span>' if d['has_words'] else '<span style="color:#ccc">—</span>'
        
        html_parts.append('<div class="day-row">')
        html_parts.append(f'<span class="day-num">Day {d["day"]}</span>')
        html_parts.append(f'<span class="day-date">{d["date"]}</span>')
        html_parts.append(f'<span class="day-subjects">{subj_tags}</span>')
        html_parts.append(f'<span class="day-words">{words_html}</span>')
        html_parts.append('</div>\n')
    
    # Week summary stats
    week_w = sum(d['word_count'] for d in wd)
    week_wl = sum(1 for d in wd if d['has_words'])
    html_parts.append(f'<div style="text-align:right;padding:8px 12px 0;font-size:11px;color:var(--sub)">本周: {len(wd)}天 · {week_wl}天含词表 · {week_w}词条</div>\n')
    
    html_parts.append('</div></div>\n')

html_parts.append('<div class="footer">📚 每天进步一点点，60天后你会感谢现在努力的自己</div>\n')
html_parts.append('</div></body></html>')

with open('C:/Users/Tebon/BangMaker/Claw/index.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_parts))

print(f'index.html created: {len(weeks)} weeks, {total_d} days, {total_w} words')
