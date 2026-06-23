#!/usr/bin/env python3
"""Convert inline answers in 练 steps to q-block format with click-to-reveal."""
import re, glob

def qblock_html(num, question, answer):
    return f'<div class="q-block"><span class="q-num">{num}.</span><span class="question">{question}</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">{answer}</div></div>'

def parse_items(content):
    """Parse HTML like '<p>1. Q1? (A1)</p><p>2. Q2? <b>答</b>：A2 3. Q3</p>'
    into list of (num, question_html, answer_text)."""
    parts = []
    for pm in re.finditer(r'<p>(.*?)</p>', content, re.DOTALL):
        text = pm.group(1).strip()
        if not text: continue
        # Split on sentence-ending punctuation before "N. "
        items = re.split(r'(?<=[。！？.;])\s*(?=\d+\.\s)', text)
        if len(items) <= 1:
            items = re.split(r'\s+(?=\d+\.\s*\S)', text)
        for item in items:
            item = item.strip()
            if not item: continue
            m = re.match(r'(\d+)\.\s*(.*)', item, re.DOTALL)
            if not m: continue
            num, rest = m.group(1), m.group(2).strip()
            q, a = rest, ""
            
            if '<b>答</b>' in rest:
                q, a = rest.split('<b>答</b>', 1)
                q = q.strip().rstrip('：:').strip()
                a = re.sub(r'</?b>', '', a).strip().lstrip('：:').strip()
            elif re.search(r'\([^)]+\)\s*$', rest):
                m2 = re.match(r'(.*)\(([^)]+)\)\s*$', rest)
                if m2:
                    q = m2.group(1).strip()
                    a = m2.group(2).strip()
            elif '→' in rest:
                q, a = rest.rsplit('→', 1)
                q = q.strip().rstrip('→').strip()
                a = a.strip()
            elif '___' in rest:
                m3 = re.findall(r'\(([^)]+)\)', rest)
                a = '；'.join(m3) if m3 else "（见讲解内容）"
                q = re.sub(r'\([^)]+\)', '(    )', rest)
            else:
                a = "（参考上方讲解内容）"
                q = rest
            
            a = a.strip()
            if a.endswith('.'): a = a[:-1]
            q = q.strip().rstrip(';；')
            if '?' not in q and '___' not in q and '？' not in q:
                q += '？'
            parts.append((num, q, a))
    return parts

def convert_step_body(body):
    """Convert <p>-based 练 content to q-blocks."""
    if '<div class="q-block">' in body:
        return None
    if '<p>' not in body:
        return None
    
    items = parse_items(body)
    if not items:
        return None
    
    new = []
    for num, q, a in items:
        new.append(qblock_html(num, q, a))
    return '\n'.join(new)

def find_matching_close(text, start):
    """Find matching </div> for a <div at start."""
    depth = 0
    i = start
    while i < len(text):
        if text[i:i+4] == '<div':
            depth += 1; i += 4
        elif text[i:i+6] == '</div>':
            depth -= 1
            if depth == 0: return i + 6
            i += 6
        else: i += 1
    return -1

def process_html(text):
    """Process entire HTML, converting all 练 steps."""
    modified = False
    
    # Collect all replacements first (old_step_html → new_step_html)
    replacements = []
    
    for lm in re.finditer(r'(<h4>.*?练（\d+min）)</h4>', text):
        h4_end = lm.end()
        
        # Find parent step div
        step_start = text.rfind('<div class="step', 0, lm.start())
        if step_start == -1: continue
        
        step_close = find_matching_close(text, step_start)
        if step_close == -1: continue
        
        step_html = text[step_start:step_close]
        h4_inner_end = step_html.find('</h4>')
        if h4_inner_end == -1: continue
        
        body = step_html[h4_inner_end + 5:]
        if body.endswith('</div>'):
            body = body[:-6]
        body = body.strip()
        
        new_body = convert_step_body(body)
        if new_body is None: continue
        
        old_full_body = step_html[h4_inner_end + 5:]
        new_full_body = '\n' + new_body + '\n'
        if old_full_body.endswith('</div>'):
            new_full_body += '</div>'
        
        new_step = step_html[:h4_inner_end + 5] + new_full_body
        
        if new_step != step_html:
            replacements.append((step_html, new_step))
    
    # Apply replacements in reverse order to preserve positions
    for old, new in reversed(replacements):
        # Find the exact occurrence using the surrounding context
        if old in text:
            text = text.replace(old, new, 1)
            modified = True
    
    return text, modified

# ─── Main ───
for fname in glob.glob('C:/Users/Tebon/BangMaker/Claw/w*.html'):
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    result, mod = process_html(c)
    if mod:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f'{fname}: converted')
    else:
        print(f'{fname}: no changes')

# Also process guct.html
fname = 'C:/Users/Tebon/BangMaker/Claw/guct.html'
with open(fname, 'r', encoding='utf-8') as f:
    c = f.read()
result, mod = process_html(c)
if mod:
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f'{fname}: converted')
else:
    print(f'{fname}: no changes')

print('\nDone!')
