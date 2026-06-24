#!/usr/bin/env python3
"""Generate 54 daily pages from study_library databases.
Each day pulls lecture/practice/exam/method from knowledge DBs,
embeds SVG diagrams, vocabulary, and poems."""
import json, os, re
from datetime import date, timedelta

LIB = 'C:/Users/Tebon/BangMaker/Claw/study_library'
OUT = f'{LIB}/../days'

# ── Load all databases ──
def load_json(path):
    with open(path,'r',encoding='utf-8') as f:
        return json.load(f)

SVGS = load_json(f'{LIB}/svg/diagrams.json')
VOCAB = load_json(f'{LIB}/english/vocab_complete.json')
PHRASES = load_json(f'{LIB}/english/phrases.json')
POEMS = load_json(f'{LIB}/chinese/poems_61.json')

KNOWLEDGE = {}
for subj in ['math','chinese','english','physics','chemistry','politics','history']:
    KNOWLEDGE[subj] = load_json(f'{LIB}/{subj}/knowledge.json')

print(f'Loaded: {len(SVGS)} SVGs, {len(VOCAB)} words, {len(POEMS)} poems')
for k,v in KNOWLEDGE.items():
    sec = len(v.get('sections', v.get('chapters', [])))
    print(f'  {k}: {sec} sections')

# ── Distribute vocab across 54 days ──
import random
random.seed(42)
random.shuffle(VOCAB)
WORDS_PER_DAY = len(VOCAB) // 54 + 1

# ── HTML Templates ──
CSS = '''
:root{--blue:#007aff;--red:#ff3b30;--green:#34c759;--orange:#ff9500;--purple:#af52de;--bg:#f5f5f7;--card:#fff;--text:#1d1d1f;--sub:#86868b}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);line-height:1.8;font-size:14px}
.container{max-width:800px;margin:0 auto;padding:0 12px}
.topbar{background:linear-gradient(135deg,var(--blue),#5856d6);color:#fff;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:100}
.day-card{border:2px solid #e5e5ea;background:var(--card);border-radius:14px;margin-bottom:16px;overflow:hidden}
.dhead{background:linear-gradient(135deg,var(--blue),#5856d6);color:#fff;padding:12px 16px;display:flex;justify-content:space-between;align-items:center}
.dnum{font-size:24px;font-weight:800}.dinfo{text-align:right;font-size:12px;opacity:.9}
.dbody{padding:14px}.goal{background:#fffbf0;border:1px solid #ffd54f;border-radius:8px;padding:8px 12px;margin-bottom:12px;font-size:13px}
.steps{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}
.step{background:#f8f8fa;border-radius:10px;padding:10px 12px}
.step.full{grid-column:1/-1}.step h4{font-size:13px;margin-bottom:6px;display:flex;align-items:center;gap:6px}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block}
p,li{font-size:13px;color:#444;margin:3px 0;line-height:1.7}
.q-block{background:#fff;border:1px solid #e5e5ea;border-radius:8px;padding:8px 10px;margin:5px 0}
.q-num{font-weight:700;color:var(--blue);margin-right:4px}.question{font-size:12px}
.ans-btn{display:inline-block;margin-top:4px;padding:2px 8px;border-radius:10px;border:1px solid var(--blue);color:var(--blue);background:transparent;font-size:11px;cursor:pointer}
.answer{display:none;background:#f0f7ff;padding:6px 10px;border-radius:6px;margin-top:4px;font-size:12px;border-left:3px solid var(--blue)}
.answer.show{display:block}
.tip{background:#f0f7ff;border-left:3px solid var(--blue);padding:6px 10px;margin:5px 0;font-size:12px;border-radius:0 6px 6px 0}
.tip b{color:var(--blue)}
.err-box{background:#fff5f5;border-left:3px solid var(--red);padding:6px 10px;margin:5px 0;font-size:12px;border-radius:0 6px 6px 0}
.check{background:#e8f5e9;border:1px solid #a5d6a7;border-radius:8px;padding:8px 12px;margin:8px 0;font-size:12px}
.summ-table{width:100%;border-collapse:collapse;font-size:12px;margin:5px 0}
.summ-table th,.summ-table td{padding:3px 6px;border:1px solid #e5e5ea}
.summ-table th{background:#f0e6f6;color:var(--purple)}
h3{font-size:15px;display:flex;align-items:center;gap:6px;margin-top:12px}
.vocab-box{background:#f0f0f5;border-radius:8px;padding:10px 12px;margin:8px 0;border:1px solid #e5e5ea}
.vocab-box p{margin:0 0 6px 0;font-size:12px;font-weight:600}
.complete-bar{padding:12px 16px;background:var(--bg);border-top:1px solid #e5e5ea;text-align:center}
.complete-btn{padding:10px 32px;border-radius:24px;border:none;font-size:15px;font-weight:600;cursor:pointer}
.complete-btn.todo{background:var(--blue);color:#fff}
.complete-btn.done{background:#e8f5e9;color:#2e7d32;border:2px solid #a5d6a7}
.nav-links{display:flex;justify-content:space-between;padding:12px 16px;gap:12px}
.nav-links a{padding:8px 16px;border-radius:20px;text-decoration:none;font-size:13px;font-weight:600;flex:1;text-align:center}
.nav-links .prev{background:#e5e5ea;color:#666}
.nav-links .home{background:var(--blue);color:#fff}
.nav-links .next{background:var(--blue);color:#fff}
.svg-wrap{text-align:center;margin:8px 0;background:#fafafa;border-radius:8px;padding:6px}
.svg-wrap svg{max-width:100%;height:auto}
'''

def day_template(num, month, day, wd, subjects, goal, body, check, prev, next_):
    prev_h = f'<a href="day{prev:03d}.html" class="prev">← Day {prev}</a>' if prev else '<span></span>'
    next_h = f'<a href="day{next_:03d}.html" class="next">Day {next_} →</a>' if next_ else '<span></span>'
    js = '''<script>
function speak(t){if(window.speechSynthesis){window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(t);u.lang="en-US";u.rate=0.7;window.speechSynthesis.speak(u);}}
function showAns(b){var a=b.nextElementSibling;a.classList.toggle("show");b.textContent=a.classList.contains("show")?"隐藏答案":"展开答案";}
function toggleComplete(dn){var btn=document.getElementById("cbtn");if(btn.classList.contains("todo")){localStorage.setItem("day_"+dn+"_done","true");btn.className="complete-btn done";btn.textContent="已完成";}else{localStorage.setItem("day_"+dn+"_done","false");btn.className="complete-btn todo";btn.textContent="标记完成";}}
window.onload=function(){if(localStorage.getItem("day_'''+str(num)+'''_done")==="true"){var btn=document.getElementById("cbtn");btn.className="complete-btn done";btn.textContent="已完成";}}
</script>'''
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>暑假逆袭 · Day {num}</title><style>{CSS}</style></head><body>
<div class="topbar"><span class="title">Day {num} · {month}月{day}日 {wd}</span><a href="../index.html">📋 目录</a></div>
<div class="container">
<div class="day-card"><div class="dhead"><div class="dnum">Day {num}</div><div class="dinfo"><div>{month}月{day}日 {wd}</div><div>{subjects}</div></div></div>
<div class="dbody"><div class="goal"><b>今日目标</b>：{goal}</div>{body}<div class="check"><b>今日达标检查</b>：<br>{check}</div></div>
<div class="complete-bar"><button id="cbtn" class="complete-btn todo" onclick="toggleComplete({num})">标记完成</button></div></div>
<div class="nav-links">{prev_h}<a href="../index.html" class="home">📋 目录</a>{next_h}</div></div>{js}</body></html>'''

# ── Content Builders ──
CM = {'b':'var(--blue)','o':'var(--orange)','g':'var(--green)','p':'var(--purple)','r':'var(--red)','l':'#9c27b0','k':'#795548','e':'#e91e63'}
C = {'math':'b','english':'g','chinese':'r','physics':'o','chemistry':'p','politics':'e','history':'k'}
EMOJI = {'math':'📖','english':'🔤','chinese':'📖','physics':'⚡','chemistry':'🧪','politics':'🏛️','history':'📜'}

def h3(subj, text):
    c = C.get(subj,'b'); e = EMOJI.get(subj,'')
    return f'<h3 style="color:{CM[c]};border-bottom:2px solid {CM[c]};padding-bottom:6px;margin:16px 0 12px">{e} {text}</h3>'

def sh(title, color, body, full=True):
    return f'<div class="step{" full" if full else ""}"><h4><span class="dot" style="background:{CM[color]}"></span>{title}</h4>{body}</div>'

def sts(*a): return f'<div class="steps">{"".join(a)}</div>'
def qb(n,q,a): return f'<div class="q-block"><span class="q-num">{n}.</span><span class="question">{q}</span><button class="ans-btn" onclick="showAns(this)">展开答案</button><div class="answer">{a}</div></div>'
def qbs(its): return ''.join(qb(n,q,a) for n,q,a in its)
def tip(t): return f'<div class="tip"><b>方法</b>：{t}</div>'

def recitation_block(author, title):
    items = [f"{author}: {title}全诗背诵","重点字词释义","作者背景常识"]
    rows = ''.join(f'<tr><td style="font-size:12px">{r}</td><td>□ □</td></tr>' for r in items)
    return f'<table class="summ-table"><tr><th>背诵内容</th><th>已背/已默</th></tr>{rows}</table>'

def svg_block(name):
    """Embed SVG diagram by name."""
    if name in SVGS:
        return f'<div class="svg-wrap">{SVGS[name]["svg"]}</div>'
    return ''

def vocab_block(words):
    h = '<div class="vocab-box"><p style="font-weight:700">📖 今日词汇（词典格式）</p>'
    for i,(w,ipa,pos,meaning,ex,trans) in enumerate(words):
        h += f'<div style="display:flex;align-items:flex-start;gap:4px;padding:3px 0;border-bottom:1px solid #eee;font-size:12px"><span style="color:#999;min-width:18px;font-size:10px">{i+1}.</span><b style="color:#1d1d1f;min-width:65px">{w}</b><button onclick="speak(\'{w}\')" style="border:none;background:var(--blue);color:#fff;border-radius:50%;width:20px;height:20px;cursor:pointer;font-size:8px">▶</button><span style="color:var(--sub);font-size:11px;min-width:50px">{ipa}</span><span style="color:var(--purple);font-size:11px;min-width:20px">{pos}</span><span style="color:var(--text);min-width:35px">{meaning}</span><span style="font-size:10px;color:#666">{ex}</span></div>'
    return h+'</div>'

def recite_block(items):
    rows = ''.join(f'<tr><td style="font-size:12px">{r}</td><td>□ □</td></tr>' for r in items)
    return f'<table class="summ-table"><tr><th>背诵内容</th><th>已背/已默</th></tr>{rows}</table>'

def find_topic(subj, topic_name):
    """Find a topic from the knowledge database by name."""
    k = KNOWLEDGE.get(subj, {})
    sections = k.get('sections', k.get('chapters', []))
    for s in sections:
        for t in s.get('topics', []):
            if topic_name in t['name']:
                return t
    return None

def build_subject_section(subj, topic_name, extra_lecture='', extra_practice=None, svg_names=None):
    """Build a complete subject section: lecture + practice + method + SVG."""
    topic = find_topic(subj, topic_name)
    if not topic:
        return ''
    
    steps_list = []
    
    # Lecture step
    lecture = topic.get('lecture', '')
    if lecture:
        body = f'<p>{lecture}</p>'
        if extra_lecture:
            body += f'<p>{extra_lecture}</p>'
        if svg_names:
            for sn in svg_names:
                body += svg_block(sn)
        steps_list.append(sh('讲（20min）',C.get(subj,'b'), body, True))
    
    # Practice steps
    practice = topic.get('practice', [])
    if practice:
        all_practice = list(practice)
        if extra_practice:
            all_practice.extend(extra_practice)
        items = [(i+1, p, '(参考答案见讲解内容)') for i,p in enumerate(all_practice[:5])]
        steps_list.append(sh('A组·基础练', 'g', qbs(items), True))
    
    if len(all_practice) > 5:
        items = [(i+1, p, '(参考答案见讲解内容)') for i,p in enumerate(all_practice[5:10])]
        steps_list.append(sh('B组·进阶练', 'o', qbs(items), True))
    
    # Exam practice
    exam = topic.get('exam_practice', [])
    if exam:
        items = [(i+1, e, '(参考历年真题解析)') for i,e in enumerate(exam[:3])]
        steps_list.append(sh('C组·中考真题', 'r', qbs(items), True))
    
    # Method summary
    method = topic.get('method', '')
    if method:
        steps_list.append(sh('方法总结', 'p', tip(method), True))
    
    return sts(*steps_list)

# ── 54-DAY SCHEDULE ──
# Auto-scheduler: each day has Math + English + rotating subject (Chinese/Physics/Chemistry/Politics/History)
DAILY_SUBJECTS = ['math','english']  # Every day has math and english
ROTATING = ['chinese','chinese','physics','chinese','chemistry','chinese','politics','history','physics']

def get_topic(subj, week, day):
    """Get topic from knowledge database for given subject and week."""
    k = KNOWLEDGE.get(subj, {})
    sections = k.get('sections', k.get('chapters', []))
    all_topics = []
    for sec in sections:
        for t in sec.get('topics', []):
            all_topics.append(t['name'])
    if not all_topics:
        return ''
    # Distribute topics across weeks
    idx = (week * 6 + day) % len(all_topics)
    return all_topics[idx]

# ── Generate all 54 days ──
def generate_all():
    start_date = date(2026, 6, 29)
    WD_CN = ['周一','周二','周三','周四','周五','周六']
    
    os.makedirs(OUT, exist_ok=True)
    
    for day_num in range(1, 55):
        w = (day_num-1)//6
        d = (day_num-1)%6
        dt = start_date + timedelta(weeks=w, days=d)
        month, day, wd = dt.month, dt.day, WD_CN[d]
        prev_d = day_num-1 if day_num>1 else None
        next_d = day_num+1 if day_num<54 else None
        
        # Build sessions for this day
        sessions = []
        subjects_today = []
        
        # Math (every day)
        math_topic = get_topic('math', w, d)
        sessions.append(('math', math_topic, '', [], None))
        subjects_today.append('📖')
        
        # English (every day)
        eng_topic = get_topic('english', w, d)
        sessions.append(('english', eng_topic, '', [], None))
        subjects_today.append('🔤')
        
        # Rotating subject
        rot_subj = ROTATING[w % len(ROTATING)]
        rot_topic = get_topic(rot_subj, w, d)
        sessions.append((rot_subj, rot_topic, '', [], None))
        subjects_today.append(EMOJI.get(rot_subj, ''))
        
        # Build goal and check
        goal = f'系统学习{math_topic} / {eng_topic} / {rot_topic}'
        check = f'掌握{math_topic}核心概念 □ 完成英语练习 □ {rot_topic}理解 □ 今日词汇背完 □'

# ── Generate all 54 days ──
def gen_index():
    total = 54
    idx = '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>暑假54天逆袭计划</title><style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;background:#f5f5f7;font-size:14px;line-height:1.8}
.hero{background:linear-gradient(135deg,#007aff,#5856d6);color:#fff;padding:28px 20px;text-align:center}
.hero h1{font-size:24px}
.hero .stats{margin:10px 0;font-size:13px}
.progress-bar{height:5px;background:rgba(255,255,255,.3);border-radius:3px;margin:8px auto;max-width:400px;overflow:hidden}
.progress-fill{height:100%;background:#34c759;border-radius:3px;transition:width .5s}
.week-card{background:#fff;border-radius:14px;margin:12px;overflow:hidden}
.week-header{background:linear-gradient(135deg,#007aff,#5856d6);color:#fff;padding:8px 14px;font-weight:700;font-size:15px;display:flex;justify-content:space-between}
.week-header .sun{font-size:11px;font-weight:400;opacity:.7}
.day-grid{display:grid;grid-template-columns:repeat(6,1fr)}
.day-item{text-decoration:none;color:#1d1d1f;padding:8px 4px;text-align:center;border-right:1px solid #eee;border-bottom:1px solid #eee;position:relative}
.day-item:nth-child(6n){border-right:none}.day-item:hover{background:#f0f7ff}
.day-item .dnum{font-size:14px;font-weight:700;color:#007aff}
.day-item .dsub{font-size:10px;color:#888}.day-item .dwd{font-size:9px;color:#bbb}
.day-item .status{position:absolute;top:3px;right:4px;font-size:13px}
.day-item .done{color:#34c759}.day-item .todo{color:#ddd}
.footer{text-align:center;color:#86868b;font-size:11px;padding:20px}
@media(max-width:500px){.day-grid{grid-template-columns:repeat(3,1fr)}.day-item:nth-child(6n){border-right:1px solid #eee}.day-item:nth-child(3n){border-right:none}}
</style></head><body>
<div class="hero"><h1>暑假54天逆袭计划</h1><p>6月29日-8月29日 · 周一至周六学习 · 周日休息</p>
<div class="stats"><span id="completed-count">已完成 0/54</span></div>
<div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div></div>
<div class="container">'''
    base = date(2026, 6, 29)
    for w in range(9):
        sun = base + timedelta(weeks=w, days=6)
        idx += f'<div class="week-card"><div class="week-header"><span>第{"一二三四五六七八九"[w]}周</span><span class="sun">☀️ {sun.month}/{sun.day}休息</span></div><div class="day-grid">'
        for d in range(6):
            dn = w*6+d+1; dt = base+timedelta(weeks=w, days=d)
            idx += f'<a href="days/day{dn:03d}.html" class="day-item"><div class="dnum">Day {dn}</div><div class="dsub">{dt.month}/{dt.day}</div><div class="status todo" id="s{dn}">○</div></a>'
        idx += '</div></div>'
    idx += '''</div>
<script>
function update(){for(var i=1,total=54,done=0;i<=total;i++){var e=document.getElementById("s"+i);if(localStorage.getItem("day_"+i+"_done")==="true"){e.className="status done";e.textContent="✓";done++;}else{e.className="status todo";e.textContent="○";}}
document.getElementById("completed-count").textContent="已完成 "+done+"/54";document.getElementById("progress-fill").style.width=Math.round(done/54*100)+"%";}
window.onload=update;window.addEventListener("storage",update);
</script></body></html>'''
    with open(f'{LIB}/../index.html','w',encoding='utf-8') as f:
        f.write(idx)
    print(f'Index generated ({len(idx)} bytes)')

gen_index()

gen_index()
