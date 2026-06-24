#!/usr/bin/env python3
"""Generate 54 daily pages from study_library databases.
Each day: Math + English + rotating subject.
All content from enriched knowledge databases with questions+answers."""
import json, os, random, html
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
CHARS = load_json(f'{LIB}/chinese/chars.json')
IDIOMS = load_json(f'{LIB}/chinese/idioms.json')
XINGSHENG = load_json(f'{LIB}/chinese/xingsheng.json')
YICUOXIE = load_json(f'{LIB}/chinese/yicuoxie.json')
SHICI = load_json(f'{LIB}/chinese/shici.json')
XUCI = load_json(f'{LIB}/chinese/xuci.json')

# ── Load wenyanwen database ──
WENYANWEN = load_json(f'{LIB}/chinese/wenyanwen.json') if os.path.exists(f'{LIB}/chinese/wenyanwen.json') else []

KNOWLEDGE = {}
for subj in ['math','chinese','english','physics','chemistry','politics','history']:
    KNOWLEDGE[subj] = load_json(f'{LIB}/{subj}/knowledge.json')

print(f'Loaded: {len(SVGS)} SVGs, {len(VOCAB)} words, {len(PHRASES)} phrases, {len(POEMS)} poems, {len(CHARS)} chars, {len(IDIOMS)} idioms, {len(XINGSHENG)} xingsheng, {len(YICUOXIE)} yicuoxie, {len(XUCI)} xuci')

# ── Shuffle vocab for distribution ──
random.seed(42)
random.shuffle(VOCAB)
WORDS_PER_DAY = len(VOCAB) // 54 + 1  # ~31 words/day, covers all

# ── Shuffle phrases for distribution ──
random.seed(42)
random.shuffle(PHRASES)
random.shuffle(PHRASES)

# ── CSS ──
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
.check{background:#e8f5e9;border:1px solid #a5d6a7;border-radius:8px;padding:8px 12px;margin:8px 0;font-size:12px}
.summ-table{width:100%;border-collapse:collapse;font-size:12px;margin:5px 0}
.summ-table th,.summ-table td{padding:3px 6px;border:1px solid #e5e5ea}
.summ-table th{background:#f0e6f6;color:var(--purple)}
h3{font-size:15px;display:flex;align-items:center;gap:6px;margin-top:12px}
.vocab-box{background:#f0f0f5;border-radius:8px;padding:10px 12px;margin:8px 0;border:1px solid #e5e5ea}
.vocab-box p{margin:0 0 6px 0;font-size:12px;font-weight:600}
.phrases-box{background:#f5f0ff;border-radius:8px;padding:10px 12px;margin:8px 0;border:1px solid #d0c0e8}
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

# ── Color / Emoji maps ──
CM = {'b':'var(--blue)','o':'var(--orange)','g':'var(--green)','p':'var(--purple)','r':'var(--red)','k':'#795548','e':'#e91e63'}
C  = {'math':'b','english':'g','chinese':'r','physics':'o','chemistry':'p','politics':'e','history':'k'}
EMOJI = {'math':'📖','english':'🔤','chinese':'📖','physics':'⚡','chemistry':'🧪','politics':'🏛️','history':'📜'}
SUBJ_CN = {'math':'数学','english':'英语','chinese':'语文','physics':'物理','chemistry':'化学','politics':'政治','history':'历史'}

# ── Helper functions ──
def h3(subj, text):
    c = C.get(subj,'b'); e = EMOJI.get(subj,'')
    return f'<h3 style="color:{CM[c]};border-bottom:2px solid {CM[c]};padding-bottom:6px;margin:16px 0 12px">{e} {text}</h3>'

def sh(title, color, body, full=True):
    return f'<div class="step{" full" if full else ""}"><h4><span class="dot" style="background:{CM[color]}"></span>{title}</h4>{body}</div>'

def sts(*a): return f'<div class="steps">{"".join(a)}</div>'

def qb(n, q, a):
    """Question block: number + question + button + hidden answer."""
    q = html.escape(str(q))
    a = html.escape(str(a))
    return f'<div class="q-block"><span class="q-num">{n}.</span><span class="question">{q}</span><button class="ans-btn" onclick="showAns(this)">展开答案</button><div class="answer">{a}</div></div>'

def qbs(items):
    """items = list of (n, q, a) tuples."""
    return ''.join(qb(n, str(q), str(a)) for n,q,a in items)

def tip(t): return f'<div class="tip"><b>方法</b>：{t}</div>'

def svg_block(name):
    if name in SVGS:
        return f'<div class="svg-wrap">{SVGS[name]["svg"]}</div>'
    return ''

def vocab_block(words):
    h = '<div class="vocab-box"><p style="font-weight:700">📖 今日词汇（词典格式）</p>'
    for i, w in enumerate(words):
        wi, ipa, pos, meaning, ex, trans = w if len(w) >= 6 else (w[0],'','','','','')
        # SVG play button (consistent rendering across all platforms)
        btn = f'<button onclick="speak(\'{wi}\')" style="border:none;background:var(--blue);color:#fff;border-radius:50%;width:22px;height:22px;cursor:pointer;padding:0;display:inline-flex;align-items:center;justify-content:center;vertical-align:middle;flex-shrink:0" title="点击发音">{chr(9654)}</button>'
        h += f'<div style="display:flex;align-items:flex-start;gap:4px;padding:4px 0;border-bottom:1px solid #eee;font-size:12px">'
        h += f'<span style="color:#999;min-width:18px;font-size:10px;line-height:22px">{i+1}.</span>'
        h += f'<b style="color:#1d1d1f;min-width:65px;line-height:22px">{wi}</b>'
        h += f'<span style="color:var(--purple);font-size:11px;min-width:20px;line-height:22px">{pos}</span>'
        h += f'<span style="color:var(--text);min-width:35px;line-height:22px">{meaning}</span>'
        h += f'<span style="color:var(--sub);font-size:11px;line-height:22px">/ {ipa} /</span>'
        h += f'{btn}'
        h += f'<span style="font-size:10px;color:#666;line-height:22px">{ex} ({trans})</span>'
        h += '</div>'
    return h + '</div>'

def phrases_block(phrases):
    if not phrases:
        return ''
    h = '<div class="phrases-box"><p style="font-weight:700">🔗 今日短语搭配</p>'
    for i, p in enumerate(phrases):
        h += f'<div style="padding:2px 0;font-size:12px"><b>{p[0]}</b> /{p[1]}/ {p[2]} {p[3]} — {p[4]}</div>'
    return h + '</div>'

def chinese_base_block(chars_list, idioms_list, xingsheng_item, yicuoxie_item, shici_item, xuci_item):
    """Daily Chinese fundamental block: 5 词语 + 5 成语"""
    # Extract SHICI data based on type rotation
    shici_type = shici_item['type']  # 通假字/古今异义/一词多义/词类活用
    shici_entries = shici_item['entries']  # list of entries
    
    h = '<div class="vocab-box" style="background:#fff8f0;border-color:#e8d5b7">'
    h += '<p style="font-weight:700;color:#b45309;font-size:14px">📝 今日语文基础积累（5词语 + 5成语）</p>'
    
    # ── 5 词语 ──
    h += '<table class="summ-table" style="margin-top:6px"><tr><th style="width:12%">类型</th><th style="width:18%">内容</th><th style="width:70%">详解</th></tr>'
    
    # 1. 多音字 (1个)
    if chars_list and len(chars_list) > 0:
        ch = chars_list[0]
        h += f'<tr><td style="font-size:11px;color:#b45309">多音字</td><td style="font-weight:700;font-size:13px">{ch[0]}</td>'
        h += f'<td style="font-size:11px">音: <span style="color:var(--red)">{ch[1]}</span> · 义: {ch[3]} · 例: {ch[4]}</td></tr>'
    
    # 2. 形声字 (1个)
    if xingsheng_item:
        xs = xingsheng_item
        h += f'<tr><td style="font-size:11px;color:#b45309">形声字</td><td style="font-weight:700;font-size:13px">{xs[0]}</td>'
        h += f'<td style="font-size:11px">音: {xs[1]} · 形旁(义): {xs[2]} · 声旁(音): {xs[3]} · {xs[4]}</td></tr>'
    
    # 3. 易错字 (1个)
    if yicuoxie_item:
        yc = yicuoxie_item
        h += f'<tr><td style="font-size:11px;color:#b45309">易错字</td><td style="font-weight:700;font-size:13px">{yc[0]}</td>'
        h += f'<td style="font-size:11px">音: {yc[1]} · 义: {yc[2]} · <span style="color:var(--red)">区别: {yc[3]}</span></td></tr>'
    
    # 4. 实词 (1个, 轮转类型)
    for se in shici_entries:
        h += f'<tr><td style="font-size:11px;color:#b45309">{shici_type}</td><td style="font-weight:700;font-size:13px">{se[0]}</td>'
        h += f'<td style="font-size:11px">{"音: "+se[1]+" · " if len(se)>1 and se[1] else ""}{se[2]} · 例: {se[3] if len(se)>3 else ""}</td></tr>'
    
    # 5. 虚词 (1个)
    if xuci_item:
        xu = xuci_item
        h += f'<tr><td style="font-size:11px;color:#b45309">虚词</td><td style="font-weight:700;font-size:13px">{xu[0]}</td>'
        h += f'<td style="font-size:11px">{xu[1]} — {xu[2]} · 例: {xu[3]} · <span style="color:var(--blue)">{xu[4]}</span></td></tr>'
    
    h += '</table>'
    
    # ── 5 成语 ──
    h += '<div style="font-weight:600;color:#b45309;font-size:12px;margin-top:10px;margin-bottom:4px">📖 成语（5个）</div>'
    for i, idm in enumerate(idioms_list):
        if len(idm) >= 5:
            h += f'<div style="padding:3px 0;font-size:11px;border-bottom:1px dotted #e8d5b7">'
            h += f'<b style="color:#1d1d1f;font-size:12px">{i+1}.{idm[0]}</b> '
            h += f'<span style="color:var(--sub)">{idm[1]}</span> — {idm[2]}'
            if idm[4]:
                h += f' · <span style="color:var(--red);font-size:10px">⚠{idm[4]}</span>'
            h += '</div>'
    
    return h + '</div>'

def recite_block(items):
    rows = ''.join(f'<tr><td style="font-size:12px">{r}</td><td>□ □</td></tr>' for r in items)
    return f'<table class="summ-table"><tr><th>背诵内容</th><th>已背/已默</th></tr>{rows}</table>'

def recitation_block(title, author, full_text='', keywords='', author_bg='', famous_lines=''):
    """Enhanced poem recitation: full text + key words + author background + famous lines."""
    h = f'<div class="vocab-box" style="background:#fef9f0;border-color:#e8d5b7">'
    h += f'<p style="font-weight:700;color:#b45309;font-size:14px">📜 今日古诗背诵：{title} — {author}</p>'
    
    # Full poem text (collapsible)
    if full_text:
        safe_text = full_text.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_text\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开全文 ▶\':\'收起全文 ▲\';" style="background:var(--blue);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px">展开全文 ▶</button>'
        h += f'<div id="poem_text" style="display:none;background:#fffbf0;padding:8px 12px;border-radius:8px;margin:6px 0;border:1px dashed #e8d5b7;white-space:pre-line;font-size:14px;line-height:2;color:#4a3728">{full_text}</div>'
    
    # Key word explanations (collapsible)
    if keywords:
        safe_kw = keywords.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_words\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开字词释义 📖\':\'收起字词释义 ▲\';" style="background:var(--orange);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px">展开字词释义 📖</button>'
        h += f'<div id="poem_words" style="display:none;background:#fff8f0;padding:8px 12px;border-radius:8px;margin:6px 0;border:1px dashed #e8d5b7;font-size:12px;line-height:1.8;color:#795548">{keywords}</div>'
    
    # Author background (collapsible)
    if author_bg:
        safe_bg = author_bg.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_author\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开作者背景 📝\':\'收起作者背景 ▲\';" style="background:var(--purple);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px">展开作者背景 📝</button>'
        h += f'<div id="poem_author" style="display:none;background:#faf0ff;padding:8px 12px;border-radius:8px;margin:6px 0;border:1px dashed #d0c0e8;font-size:12px;line-height:1.8;color:#6b4c8a">{author_bg}</div>'
    
    # Famous lines (collapsible)
    if famous_lines:
        safe_fl = famous_lines.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_famous\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开千古名句 🌟\':\'收起名句 ▲\';" style="background:#e91e63;color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px">展开千古名句 🌟</button>'
        h += f'<div id="poem_famous" style="display:none;background:#fef0f7;padding:8px 12px;border-radius:8px;margin:6px 0;border:1px dashed #e8b7c8;font-size:12px;line-height:1.8;color:#6b1e3a">{famous_lines}</div>'
    
    # Checkbox table
    items = [f'{author}: 《{title}》全诗背诵','重点字词释义掌握','作者背景常识了解','千古名句解析']
    rows = ''.join(f'<tr><td style="font-size:12px">{r}</td><td>□ □</td></tr>' for r in items)
    h += f'<table class="summ-table" style="margin-top:8px"><tr><th>背诵内容</th><th>已背/已默</th></tr>{rows}</table>'
    
    return h + '</div>'
    """Enhanced poem recitation: full text + key words + author background."""
    h = f'<div class="vocab-box" style="background:#fef9f0;border-color:#e8d5b7">'
    h += f'<p style="font-weight:700;color:#b45309;font-size:14px">📜 每日古诗背诵：{title} — {author}</p>'
    
    # Full poem text (collapsible)
    if full_text:
        safe_text = full_text.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_text\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开全文 ▶\':\'收起全文 ▲\';" style="background:var(--blue);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px 0">展开全文 ▶</button>'
        h += f'<div id="poem_text" style="display:none;background:#fffbf0;padding:8px 12px;border-radius:8px;margin:6px 0;border:1px dashed #e8d5b7;white-space:pre-line;font-size:14px;line-height:2;color:#4a3728">{full_text}</div>'
    
    # Key word explanations (collapsible)
    if keywords:
        safe_kw = keywords.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_words\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开字词释义 📖\':\'收起字词释义 ▲\';" style="background:var(--orange);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px 4px">展开字词释义 📖</button>'
        h += f'<div id="poem_words" style="display:none;background:#fff8f0;padding:8px 12px;border-radius:8px;margin:6px 0;border:1px dashed #e8d5b7;font-size:12px;line-height:1.8;color:#795548">{keywords}</div>'
    
    # Author background (collapsible)
    if author_bg:
        safe_bg = author_bg.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_author\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开作者背景 📝\':\'收起作者背景 ▲\';" style="background:var(--purple);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px 4px">展开作者背景 📝</button>'
        h += f'<div id="poem_author" style="display:none;background:#faf0ff;padding:8px 12px;border-radius:8px;margin:6px 0;border:1px dashed #d0c0e8;font-size:12px;line-height:1.8;color:#6b4c8a">{author_bg}</div>'
    
    # Checkbox table
    items = [f'{author}: 《{title}》全诗背诵','重点字词释义掌握','作者背景常识了解']
    rows = ''.join(f'<tr><td style="font-size:12px">{r}</td><td>□ □</td></tr>' for r in items)
    h += f'<table class="summ-table" style="margin-top:8px"><tr><th>背诵内容</th><th>已背/已默</th></tr>{rows}</table>'
    
    return h + '</div>'

# ── Extract question text from mixed formats ──
def get_q(item):
    """item is either dict {q:..., a:...} or plain string."""
    if isinstance(item, dict):
        return item.get('q', str(item))
    return str(item)

def get_a(item):
    if isinstance(item, dict):
        return item.get('a', '')
    return ''

# ── Find topic by name ──
def find_topic(subj, topic_name):
    k = KNOWLEDGE.get(subj, {})
    sections = k.get('sections', k.get('chapters', []))
    for s in sections:
        for t in s.get('topics', []):
            if topic_name in t['name']:
                return t
    return None

# ── Build subject section from database ──
def build_subject_section(subj, topic_name, extra_lecture='', extra_practice=None, svg_names=None):
    topic = find_topic(subj, topic_name)
    if not topic:
        return ''
    steps_list = []
    
        # Lecture
    lecture = topic.get('lecture', '')
    if lecture:
        body = f'<div class="lecture-expanded">{lecture}</div>'
        if extra_lecture:
            body += f'<p>{extra_lecture}</p>'
        if svg_names:
            for sn in svg_names:
                body += svg_block(sn)
        steps_list.append(sh('讲（20min）', C.get(subj,'b'), body, True))
    
    # Practice (handle both dict and string formats)
    practice = topic.get('practice', [])
    if practice:
        all_p = list(practice)
        if extra_practice:
            all_p.extend(extra_practice)
        
        # Group A (first 5)
        items_a = [(i+1, get_q(p), get_a(p)) for i,p in enumerate(all_p[:5])]
        steps_list.append(sh('A组·基础练', 'g', qbs(items_a), True))
        
        # Group B (next 5)
        if len(all_p) > 5:
            items_b = [(i+1, get_q(p), get_a(p)) for i,p in enumerate(all_p[5:10])]
            steps_list.append(sh('B组·进阶练', 'o', qbs(items_b), True))
    
    # Exam practice
    exam = topic.get('exam_practice', [])
    if exam:
        items_e = [(i+1, get_q(e), get_a(e)) for i,e in enumerate(exam[:3])]
        steps_list.append(sh('C组·中考真题', 'r', qbs(items_e), True))
    
    # Method
    method = topic.get('method', '')
    if method:
        steps_list.append(sh('方法总结', 'p', tip(method), True))
    
    return sts(*steps_list)

# ── SVG names per subject topic ──
SVG_MAP = {
    'math': {
        '有理数与实数': ['math_number_line'],
        '整式与因式分解': [],
        '分式与二次根式': [],
        '一元一次方程与方程组': ['math_quadratic_formula'],
        '不等式（组）': [],
        '一次函数': ['math_functions'],
        '二次函数': ['math_parabola'],
        '反比例函数': [],
        '三角形（全等+相似+勾股）': ['math_triangle','math_pythagorean'],
        '四边形': [],
        '圆': ['math_circle'],
        '统计量与概率': ['math_coordinate'],
    },
    'physics': {
        '磁现象与磁场': ['physics_magnet'],
        '电生磁（电磁铁）': ['physics_magnet'],
        '热机与效率': ['physics_engine'],
        '内能与热量': ['physics_engine'],
        '压强': ['physics_pressure_float'],
        '浮力': ['physics_pressure_float'],
        '光的反射定律': ['physics_reflection'],
        '凸透镜成像规律': ['physics_lens'],
        '受力分析': ['physics_forces'],
        '电路基础': ['physics_circuit'],
        '简单机械': ['physics_lever'],
    },
    'chemistry': {
        '金属': ['chem_metal_order'],
        '酸碱盐': ['chem_ph_scale'],
        '燃烧与灭火': ['chem_fire_triangle'],
        '空气与氧气': ['chem_fire_triangle'],
        '物理变化与化学变化': ['chem_molecule'],
        '元素与原子': ['chem_atom'],
        '溶液': ['chem_ph_scale'],
    },
    'history': {
        '列强侵略与民族危机': ['history_timeline'],
        '新民主主义革命': ['history_timeline'],
        '近代化的探索': ['history_timeline'],
        '世界史': ['history_world_timeline'],
    },
}

# ── Schedule (block-based: 2 consecutive days per topic) ──
# 语数英每天必有，每个知识点集中攻克2天，理化政史循环穿插
DAILY = ['math','english','chinese']
ROTATING = ['physics','chemistry','politics','history']

def get_topic(subj, day_num, block_size=2):
    """Block-based topic distribution: each topic gets `block_size` consecutive days.
    For rotating subjects, uses occurrence count (rounds) so no topic is skipped."""
    k = KNOWLEDGE.get(subj, {})
    sections = k.get('sections', k.get('chapters', []))
    all_topics = []
    for sec in sections:
        for t in sec.get('topics', []):
            all_topics.append(t['name'])
    if not all_topics:
        return ''
    
    if subj in DAILY:
        # DAILY subjects: every block counts contiguously
        block_idx = ((day_num - 1) // block_size) % len(all_topics)
    else:
        # ROTATING subjects: only count the rounds (each subject appears once per len(ROTATING) blocks)
        # occurrence = which complete round of rotating subjects we've done
        # E.g. physics appears on block 0,4,8,... → occurrence = block//4
        occurrence = ((day_num - 1) // block_size) // len(ROTATING)
        block_idx = occurrence % len(all_topics)
    
    return all_topics[block_idx]

def get_poems(day_num, count=2):
    """Return `count` poems for a given day (ensures 100% coverage)."""
    if not POEMS:
        return []
    result = []
    for i in range(count):
        idx = ((day_num - 1) * 2 + i) % len(POEMS)
        p = POEMS[idx]
        if len(p) >= 2:
            result.append({
                'title': p[0] if len(p)>0 else '',
                'author': p[1] if len(p)>1 else '',
                'full_text': p[4] if len(p)>4 else '',
                'keywords': p[5] if len(p)>5 else '',
                'author_bg': p[6] if len(p)>6 else '',
                'famous_lines': p[7] if len(p)>7 else '',
            })
    return result

# ── Day template ──
def day_template(num, month, day, wd, subjects, goal, body, check, prev, next_):
    prev_h = f'<a href="day{prev:03d}.html" class="prev">← Day {prev}</a>' if prev else '<span></span>'
    next_h = f'<a href="day{next_:03d}.html" class="next">Day {next_} →</a>' if next_ else '<span></span>'
    js = f'''<script>
function speak(t){{if(window.speechSynthesis){{window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(t);u.lang="en-US";u.rate=0.7;window.speechSynthesis.speak(u);}}}}
function showAns(b){{var a=b.nextElementSibling;a.classList.toggle("show");b.textContent=a.classList.contains("show")?"隐藏答案":"展开答案";}}
function toggleComplete(dn){{var btn=document.getElementById("cbtn");if(btn.classList.contains("todo")){{localStorage.setItem("day_"+dn+"_done","true");btn.className="complete-btn done";btn.textContent="已完成";}}else{{localStorage.setItem("day_"+dn+"_done","false");btn.className="complete-btn todo";btn.textContent="标记完成";}}}}
window.onload=function(){{if(localStorage.getItem("day_{num}_done")==="true"){{var btn=document.getElementById("cbtn");btn.className="complete-btn done";btn.textContent="已完成";}}}}
</script>'''
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>暑假逆袭 · Day {num}</title><style>{CSS}</style></head><body>
<div class="topbar"><span class="title">Day {num} · {month}月{day}日 {wd}</span><a href="../index.html">📋 目录</a></div>
<div class="container">
<div class="day-card"><div class="dhead"><div class="dnum">Day {num}</div><div class="dinfo"><div>{month}月{day}日 {wd}</div><div>{subjects}</div></div></div>
<div class="dbody"><div class="goal"><b>今日目标</b>：{goal}</div>{body}<div class="check"><b>今日达标检查</b>：<br>{check}</div></div>
<div class="complete-bar"><button id="cbtn" class="complete-btn todo" onclick="toggleComplete({num})">标记完成</button></div></div>
<div class="nav-links">{prev_h}<a href="../index.html" class="home">📋 目录</a>{next_h}</div></div>{js}</body></html>'''

# ── Generate all 54 days ──
def generate_all():
    start_date = date(2026, 6, 29)
    WD_CN = ['周一','周二','周三','周四','周五','周六']
    os.makedirs(OUT, exist_ok=True)
    
    for day_num in range(1, 55):
        w = (day_num - 1) // 6      # week index 0-8
        d = (day_num - 1) % 6       # day in week 0-5
        dt = start_date + timedelta(weeks=w, days=d)
        month_num, day_num_dt, wd = dt.month, dt.day, WD_CN[d]
        prev_d = day_num - 1 if day_num > 1 else None
        next_d = day_num + 1 if day_num < 54 else None
        
        # Get topics for today (block-based: 2 days per topic)
        math_topic = get_topic('math', day_num)
        eng_topic  = get_topic('english', day_num)
        chi_topic  = get_topic('chinese', day_num)
        rot_subj   = ROTATING[(day_num - 1) % len(ROTATING)]  # rotate every day among 4 subjects
        rot_topic  = get_topic(rot_subj, day_num, block_size=1)
        
        # Get vocabulary for today
        vi = (day_num - 1) * WORDS_PER_DAY
        todays_vocab = VOCAB[vi : vi + WORDS_PER_DAY]
        
        # Get phrases (spread ~1 per day, 47 phrases / 54 days)
        pi = (day_num - 1) % len(PHRASES)
        todays_phrase = [PHRASES[pi]] if PHRASES else []
        
        # Build subject sections
        body_parts = []
        check_items = []
        
        # 1. Math section
        svg_list = SVG_MAP.get('math', {}).get(math_topic, [])
        body_parts.append(h3('math', f'数学 · {math_topic}'))
        body_parts.append(build_subject_section('math', math_topic, svg_names=svg_list))
        check_items.append(f'{math_topic}理解 □')
        check_items.append(f'数学练习完成 □')
        
        # 2. English section
        body_parts.append(h3('english', f'英语 · {eng_topic}'))
        body_parts.append(build_subject_section('english', eng_topic))
        check_items.append(f'{eng_topic}练习 □')
        
        # Vocabulary block (EVERY day)
        body_parts.append(vocab_block(todays_vocab))
        check_items.append(f'今日词汇({len(todays_vocab)}词)背完 □')
        
        # Phrases block (spread across days)
        body_parts.append(phrases_block(todays_phrase))
        
        # 3. Chinese section (EVERY day)
        body_parts.append(h3('chinese', f'语文 · {chi_topic}'))
        body_parts.append(build_subject_section('chinese', chi_topic))
        check_items.append(f'{chi_topic}理解 □')
        
        # 4. Poem + Wenyanwen recitation (EVERY day, both covered)
        # Poems: 2 per day × 54 = 108 slots → 67 poems covered 100% + repeats
        poems_today = get_poems(day_num, 2)
        for pi, poem in enumerate(poems_today):
            pid_suffix = f'_{day_num}_{pi}'
            title = poem['title']
            author = poem['author']
            full_text = poem['full_text']
            keywords = poem['keywords']
            author_bg = poem['author_bg']
            famous_lines = poem['famous_lines']
            h = f'<div class="vocab-box" style="background:#fef9f0;border-color:#e8d5b7">'
            h += f'<p style="font-weight:700;color:#b45309;font-size:14px">📜 古诗{pi+1}：{title} — {author}</p>'
            if full_text:
                h += f'<button onclick="var t=document.getElementById(\'pt{pid_suffix}\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开全文 ▶\':\'收起全文 ▲\';" style="background:var(--blue);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px">展开全文 ▶</button>'
                h += f'<div id="pt{pid_suffix}" style="display:none;background:#fffbf0;padding:8px 12px;border-radius:8px;margin:6px 0;border:1px dashed #e8d5b7;white-space:pre-line;font-size:14px;line-height:2;color:#4a3728">{full_text}</div>'
            if keywords:
                h += f'<button onclick="var t=document.getElementById(\'pw{pid_suffix}\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开字词释义 📖\':\'收起字词释义 ▲\';" style="background:var(--orange);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px">展开字词释义 📖</button>'
                h += f'<div id="pw{pid_suffix}" style="display:none;background:#fff8f0;padding:8px 12px;border-radius:8px;margin:6px 0;border:1px dashed #e8d5b7;font-size:12px;line-height:1.8;color:#795548">{keywords}</div>'
            if author_bg:
                h += f'<button onclick="var t=document.getElementById(\'pa{pid_suffix}\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开作者背景 📝\':\'收起作者背景 ▲\';" style="background:var(--purple);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px">展开作者背景 📝</button>'
                h += f'<div id="pa{pid_suffix}" style="display:none;background:#faf0ff;padding:8px 12px;border-radius:8px;margin:6px 0;border:1px dashed #d0c0e8;font-size:12px;line-height:1.8;color:#6b4c8a">{author_bg}</div>'
            if famous_lines:
                h += f'<button onclick="var t=document.getElementById(\'pf{pid_suffix}\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开千古名句 🌟\':\'收起名句 ▲\';" style="background:#e91e63;color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px">展开千古名句 🌟</button>'
                h += f'<div id="pf{pid_suffix}" style="display:none;background:#fef0f7;padding:8px 12px;border-radius:8px;margin:6px 0;border:1px dashed #e8b7c8;font-size:12px;line-height:1.8;color:#6b1e3a">{famous_lines}</div>'
            h += '</div>'
            body_parts.append(h)
            check_items.append(f'《{title}》背诵 □')
        
        # Wenyanwen: 54 days / 23 texts = each ~2.3 times for reinforcement
        if WENYANWEN:
            ww_idx = (day_num - 1) % len(WENYANWEN)
            ww = WENYANWEN[ww_idx]
            ww_title = ww[0] if len(ww)>0 else ''
            ww_author = f'{ww[1]} ({ww[2]})' if len(ww)>2 else ''
            ww_text = ww[3] if len(ww)>3 else ''
            ww_words = ww[4] if len(ww)>4 else ''
            ww_bg = ww[5] if len(ww)>5 else ''
            body_parts.append(f'<div class="vocab-box" style="background:#f0f4ff;border-color:#b8c8e0">'
                f'<p style="font-weight:700;color:#3b5998;font-size:14px">📜 今日文言文背诵：{ww_title} — {ww_author}</p>'
                f'<button onclick="var t=document.getElementById(\'ww_text_{day_num}\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开原文全文 ▼\':\'收起原文 ▲\';" style="background:#3b5998;color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:11px;margin:4px">展开原文全文 ▼</button>'
                f'<div id="ww_text_{day_num}" style="display:none;white-space:pre-line;font-size:13px;line-height:2;color:#2a3a5c;padding:8px;background:#fff;border-radius:6px">{ww_text}</div>'
                f'<button onclick="var t=document.getElementById(\'ww_words_{day_num}\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开字词释义 📖\':\'收起字词释义 ▲\';" style="background:var(--orange);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:11px;margin:4px">展开字词释义 📖</button>'
                f'<div id="ww_words_{day_num}" style="display:none;padding:6px 10px;font-size:12px;line-height:1.8;color:#795548">{ww_words}</div>'
                f'<button onclick="var t=document.getElementById(\'ww_bg_{day_num}\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开作者背景 📝\':\'收起作者背景 ▲\';" style="background:var(--purple);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:11px;margin:4px">展开作者背景 📝</button>'
                f'<div id="ww_bg_{day_num}" style="display:none;padding:6px 10px;font-size:12px;line-height:1.8;color:#6b4c8a">{ww_bg}</div>'
                f'<table class="summ-table" style="margin-top:8px"><tr><th>背诵内容</th><th>已背/已默</th></tr>'
                f'<tr><td style="font-size:12px">{ww_title}全文背诵</td><td>□ □</td></tr>'
                f'<tr><td style="font-size:12px">重点字词释义掌握</td><td>□ □</td></tr>'
                f'<tr><td style="font-size:12px">作者背景+主旨了解</td><td>□ □</td></tr></table></div>')
            check_items.append(f'《{ww_title}》文言背诵 □')
        
        # Chinese words accumulation (EVERY day: 5 词语 + 5 成语)
        ci = (day_num - 1) % len(CHARS)
        ii = (day_num - 1) * 5 % len(IDIOMS)
        xi = (day_num - 1) % len(XINGSHENG)
        yi = (day_num - 1) % len(YICUOXIE)
        
        # SHICI: rotate through 通假字/古今异义/一词多义/词类活用
        shici_types = list(SHICI.keys())
        si_type = shici_types[(day_num - 1) % len(shici_types)]
        si_list = SHICI[si_type]
        si_idx = (day_num - 1) % len(si_list)
        
        # XUCI: rotate through 虚词 keys (之/而/以/于/其/为/乃/则/焉/乎)
        xuci_keys = list(XUCI.keys())
        xu_key = xuci_keys[(day_num - 1) % len(xuci_keys)]
        xu_list = XUCI[xu_key]
        xu_idx = (day_num - 1) % len(xu_list)
        
        # Build items for today
        todays_chars = [CHARS[ci]] if CHARS else []
        todays_xingsheng = XINGSHENG[xi] if XINGSHENG else None
        todays_yicuoxie = YICUOXIE[yi] if YICUOXIE else None
        todays_shici = {'type': si_type, 'entries': [si_list[si_idx]]}
        todays_xuci = xu_list[xu_idx] if xu_list else None
        
        # 5 idioms
        todays_idioms = []
        for j in range(5):
            idx_val = (ii + j) % len(IDIOMS)
            if IDIOMS:
                todays_idioms.append(IDIOMS[idx_val])
        
        body_parts.append(chinese_base_block(todays_chars, todays_idioms, todays_xingsheng, todays_yicuoxie, todays_shici, todays_xuci))
        check_items.append(f'今日5词语+5成语掌握 □')
        
        # 5. Rotating subject section
        svg_list_rot = SVG_MAP.get(rot_subj, {}).get(rot_topic, [])
        body_parts.append(h3(rot_subj, f'{SUBJ_CN.get(rot_subj, rot_subj)} · {rot_topic}'))
        body_parts.append(build_subject_section(rot_subj, rot_topic, svg_names=svg_list_rot))
        check_items.append(f'{rot_topic}理解 □')
        
        body = '\n'.join(body_parts)
        
        # Goal
        goal = f'系统学习{math_topic} / {eng_topic} / {chi_topic} / {rot_topic}'
        
        # Check
        check = '\n'.join(c for c in check_items)
        
        # Subjects header
        subjects_str = f'📖+🔤+📖+{EMOJI.get(rot_subj, "")}'
        
        # Generate HTML
        html = day_template(day_num, month_num, day_num_dt, wd,
                           subjects_str, goal, body, check,
                           prev_d, next_d)
        
        # Write file
        fname = f'day{day_num:03d}.html'
        fpath = f'{OUT}/{fname}'
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f'  Day {day_num:2d}: {month_num}/{day_num_dt} {wd} | '
              f'📖 {math_topic} | 🔤 {eng_topic} | 📖 {chi_topic} | {EMOJI.get(rot_subj,rot_subj)} {rot_topic} | '
              f'词汇{len(todays_vocab)}词')
    
    print(f'\nGenerated {54} daily pages in {OUT}/')

# ── Generate index page ──
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
            dn = w*6+d+1
            dt = base+timedelta(weeks=w, days=d)
            idx += f'<a href="days/day{dn:03d}.html" class="day-item"><div class="dnum">Day {dn}</div><div class="dsub">{dt.month}/{dt.day}</div><div class="status todo" id="s{dn}">○</div></a>'
        idx += '</div></div>'
    idx += '''</div>
<script>
function update(){for(var i=1,total=54,done=0;i<=total;i++){var e=document.getElementById("s"+i);if(localStorage.getItem("day_"+i+"_done")==="true"){e.className="status done";e.textContent="✓";done++;}else{e.className="status todo";e.textContent="○";}}
document.getElementById("completed-count").textContent="已完成 "+done+"/54";document.getElementById("progress-fill").style.width=Math.round(done/54*100)+"%";}
window.onload=update;window.addEventListener("storage",update);
</script></body></html>'''
    idx_path = f'{LIB}/../index.html'
    with open(idx_path,'w',encoding='utf-8') as f:
        f.write(idx)
    print(f'Index generated ({os.path.getsize(idx_path)} bytes)')

# ── Link Checker ──
def check_links():
    """Verify all navigation links are working."""
    print('\n🔗 Checking navigation links...')
    errors = []
    
    # Check index.html has all 54 day links
    idx_path = f'{LIB}/../index.html'
    if os.path.exists(idx_path):
        with open(idx_path,'r',encoding='utf-8') as f:
            idx_content = f.read()
        for d in range(1, 55):
            link = f'days/day{d:03d}.html'
            if link not in idx_content:
                errors.append(f'Index: missing link to {link}')
    else:
        errors.append('Index: index.html not found')
    
    # Check each day page
    for d in range(1, 55):
        dp = f'{OUT}/day{d:03d}.html'
        if not os.path.exists(dp):
            errors.append(f'Day {d}: file not found')
            continue
        
        with open(dp,'r',encoding='utf-8') as f:
            content = f.read()
        
        # Check home link
        if '../index.html' not in content:
            errors.append(f'Day {d}: missing ../index.html link')
        
        # Check prev/next links
        if d > 1:
            prev_link = f'day{d-1:03d}.html'
            if prev_link not in content:
                errors.append(f'Day {d}: missing prev link {prev_link}')
        if d < 54:
            next_link = f'day{d+1:03d}.html'
            if next_link not in content:
                errors.append(f'Day {d}: missing next link {next_link}')
    
    if errors:
        print(f'  ❌ Found {len(errors)} link errors:')
        for e in errors:
            print(f'    {e}')
    else:
        print(f'  ✅ All {54} days + index links verified OK')
    
    return errors

# ── Syllabus / 考纲映射页面 ──
def gen_syllabus():
    """Generate syllabus.html mapping every knowledge point to its Day(s)."""
    print('\n📋 Generating syllabus page...')
    
    # Build reverse mapping: topic -> list of day numbers
    mapping = {}
    for subj in KNOWLEDGE:
        mapping[subj] = {}
        k = KNOWLEDGE[subj]
        sections = k.get('sections', k.get('chapters', []))
        for s in sections:
            for t in s.get('topics', []):
                mapping[subj][t['name']] = []
    
    # Simulate the schedule exactly
    start_date = date(2026, 6, 29)
    WD_CN = ['周一','周二','周三','周四','周五','周六']
    
    for day_num in range(1, 55):
        w = (day_num - 1) // 6
        d = (day_num - 1) % 6
        dt = start_date + timedelta(weeks=w, days=d)
        
        math_topic = get_topic('math', day_num)
        eng_topic  = get_topic('english', day_num)
        chi_topic  = get_topic('chinese', day_num)
        rot_subj   = ROTATING[(day_num - 1) % len(ROTATING)]  # rotate every day
        rot_topic  = get_topic(rot_subj, day_num, block_size=1)
        
        # Record
        for subj, topic in [('math', math_topic), ('english', eng_topic), 
                             ('chinese', chi_topic), (rot_subj, rot_topic)]:
            if subj in mapping and topic in mapping[subj]:
                mapping[subj][topic].append(day_num)
    
    # Build HTML
    SUBJ_COLORS = {
        'math': '#007aff', 'chinese': '#ff3b30', 'english': '#34c759',
        'physics': '#ff9500', 'chemistry': '#af52de', 'politics': '#e91e63', 'history': '#795548'
    }
    
    body_rows = ''
    total_topics = 0
    for subj in ['math','chinese','english','physics','chemistry','politics','history']:
        subj_cn = SUBJ_CN.get(subj, subj)
        color = SUBJ_COLORS.get(subj, '#333')
        
        # Section header
        body_rows += f'<tr style="background:#f5f5f7"><td colspan="4" style="font-weight:700;font-size:15px;color:{color};padding:10px 14px">📚 {subj_cn}</td></tr>'
        
        topics = mapping.get(subj, {})
        for topic_name, days in topics.items():
            total_topics += 1
            # Format days as links
            if days:
                day_links = ', '.join(f'<a href="days/day{d:03d}.html" style="color:{color}">Day {d}</a>' for d in days)
            else:
                day_links = '<span style="color:#ccc">—</span>'
            
            body_rows += f'<tr><td style="padding:6px 14px;font-size:13px">{topic_name}</td>'
            body_rows += f'<td style="padding:6px;font-size:12px;color:#888">{len(days)}天</td>'
            body_rows += f'<td style="padding:6px;font-size:11px">{day_links}</td>'
            go_link = f'<a href="days/day{days[0]:03d}.html" class="go-btn">▶</a>' if days else '<span style="color:#ccc">—</span>'
            body_rows += f'<td style="padding:6px;text-align:center">{go_link}</td></tr>'
    
    html = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>考纲知识点索引 · 暑假逆袭计划</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;background:#f5f5f7;font-size:14px;line-height:1.8;color:#1d1d1f}}
.hero{{background:linear-gradient(135deg,#5856d6,#007aff);color:#fff;padding:20px;text-align:center}}
.hero h1{{font-size:20px;margin-bottom:4px}}
.container{{max-width:900px;margin:0 auto;padding:12px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05)}}
th{{background:#f0f0f5;padding:8px 14px;font-size:12px;color:#666;text-align:left}}
tr{{border-bottom:1px solid #eee}}
tr:hover{{background:#f8f8ff}}
a{{text-decoration:none;font-weight:600}}
a:hover{{text-decoration:underline}}
.go-btn{{display:inline-block;width:28px;height:24px;line-height:24px;text-align:center;border-radius:12px;background:#007aff;color:#fff!important;font-size:11px}}
.nav-bar{{background:#fff;padding:10px 14px;margin-bottom:12px;border-radius:8px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
.nav-bar a{{padding:6px 14px;border-radius:16px;margin:0 3px;font-size:12px;background:#f0f0f5;color:#666}}
.nav-bar a:hover{{background:#007aff;color:#fff}}
.footer{{text-align:center;color:#86868b;font-size:11px;padding:20px}}
</style></head><body>
<div class="hero"><h1>📋 考纲知识点索引</h1><p>共 {total_topics} 个知识点 · 暑假54天全覆盖</p></div>
<div class="container">
<div class="nav-bar">
<a href="index.html">🏠 首页</a>
<a href="#math">📖 数学</a><a href="#chinese">📖 语文</a><a href="#english">🔤 英语</a>
<a href="#physics">⚡ 物理</a><a href="#chemistry">🧪 化学</a><a href="#politics">🏛️ 政治</a><a href="#history">📜 历史</a>
</div>
<table>
<tr><th style="width:35%">知识点</th><th style="width:8%">天数</th><th style="width:50%">覆盖日期 (点击跳转)</th><th style="width:7%">去</th></tr>
{body_rows}
</table>
</div>
<div class="footer">暑假逆袭计划 · 考纲索引 · 共 {total_topics} 个知识点</div>
</body></html>'''
    
    syllabus_path = f'{LIB}/../syllabus.html'
    with open(syllabus_path,'w',encoding='utf-8') as f:
        f.write(html)
    print(f'  ✅ Syllabus page generated ({os.path.getsize(syllabus_path)} bytes): {syllabus_path}')

# ── Main ──
if __name__ == '__main__':
    generate_all()
    gen_index()
    errors = check_links()
    gen_syllabus()
    print(f'\n{"="*60}')
    print(f'  生成完成: 54天页面 + index + syllabus')
    print(f'  链接检查: {"✅ 全部正常" if not errors else f"❌ {len(errors)}个错误"}')
    print(f'{"="*60}')
