#!/usr/bin/env python3
"""fix_w1_v2.py - 干净版 w1.html 修复：tips 作为 step full 插入步骤网格内"""
import re

# === TIPS CONTENT (wrapped as step full cards) ===
TIPS = {
    'D1': '<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>💡 有理数运算方法总结</h4><div class="svg-diagram" style="text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px"><svg viewBox="0 0 600 80"><line x1="40" y1="40" x2="560" y2="40" stroke="#333" stroke-width="2"/><polygon points="560,36 570,40 560,44" fill="#333"/><text x="20" y="44" font-size="12">←负</text><text x="570" y="44" font-size="12">正→</text><text x="295" y="35" font-size="14" fill="var(--red)" font-weight="bold">0</text><circle cx="300" cy="40" r="4" fill="var(--red)"/><circle cx="200" cy="40" r="4" fill="var(--blue)"/><text x="195" y="25" font-size="11" fill="var(--blue)">-a</text><text x="195" y="65" font-size="10" fill="#888">|a|</text><circle cx="400" cy="40" r="4" fill="var(--blue)"/><text x="395" y="25" font-size="11" fill="var(--blue)">+a</text><text x="395" y="65" font-size="10" fill="#888">|a|</text></svg><p style="font-size:11px;color:var(--sub);text-align:center">|a| = a(a≥0), |a| = -a(a<0) → 绝对值是到原点的距离</p></div><p style="margin-top:8px;font-size:13px">定符号→算数值→"先乘方再乘除后加减有括号先括号"<br>去绝对值:|a|=a(a≥0),|a|=-a(a<0)<br>遇括号能用分配律的先用分配律</p></div>\n',
    'D2': '<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>💡 整式乘除方法总结</h4><p style="font-size:13px">同底数幂:乘加除减 aᵐ×aⁿ=aᵐ⁺ⁿ,aᵐ÷aⁿ=aᵐ⁻ⁿ|幂的乘方:(aᵐ)ⁿ=aᵐⁿ<br>平方差:(a+b)(a-b)=a²-b²|完全平方:(a±b)²=a²±2ab+b²"首平方尾平方2倍首尾放中央"<br>⚠️(-2)⁴=16≠-2⁴=-16！完全平方中间项2ab最易漏！</p></div>\n',
    'D3': '<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>💡 方程不等式方法总结</h4><p style="font-size:13px">五步法:去分母→去括号→移项变号→合并→系数化1<br>代入vs加减:系数差1倍→加减法;系数为1→代入法<br>不等式:乘除负数必须变号!>变<!口诀"同大取大同小取小"</p></div>\n',
    'D4': '<div class="step full"><h4><span class="dot" style="background:var(--orange)"></span>💡 光的反射与成像</h4><div class="svg-diagram" style="text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px"><svg viewBox="0 0 500 200"><line x1="250" y1="10" x2="250" y2="190" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/><text x="255" y="15" font-size="10" fill="#999">法线</text><line x1="60" y1="120" x2="250" y2="90" stroke="var(--orange)" stroke-width="2"/><polygon points="250,90 240,85 240,95" fill="var(--orange)"/><text x="100" y="100" font-size="11" fill="var(--orange)">入射光线</text><line x1="250" y1="90" x2="440" y2="120" stroke="var(--green)" stroke-width="2"/><polygon points="440,120 430,115 430,125" fill="var(--green)"/><text x="350" y="108" font-size="11" fill="var(--green)">反射光线</text><path d="M 230 70 A 50 50 0 0 1 270 70" fill="none" stroke="var(--red)" stroke-width="1.5"/><text x="255" y="65" font-size="10" fill="var(--red)">θ</text><path d="M 270 70 A 50 50 0 0 1 230 70" fill="none" stroke="var(--red)" stroke-width="1.5"/><text x="235" y="110" font-size="10" fill="var(--red)">θ</text><text x="260" y="170" font-size="11">反射角=入射角（三线共面两线分居）</text></svg></div><p style="margin-top:8px;font-size:13px">反射定律:三线共面|两线分居|反射角=入射角(先画法线!)<br>平面镜成像四特点:等大/等距/垂直/虚像<br>镜面vs漫反射:都遵循反射定律!</p></div>\n',
}

# === DAY 3 SUPPLEMENTS ===
CHINESE_D3 = '''<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:20px 0 12px">📖 语文 · 古诗文默写+文言文入门（1h）</h3>
<div class="steps">
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（20min）</h4>
<p><b>古诗默写技巧</b>：先理解诗意再背诵。圈出易错字（如"澹澹"不要写成"淡淡"，"竦峙"不要写成"耸峙"）。默写后逐字对照原文，错一字整首重默。</p>
<p><b>文言文基础</b>——中考必考4大句式：</p>
<p>①<b>判断句</b>："……者，……也" / "乃" / "为" → 是<br>
②<b>省略句</b>：补充省略的主语或宾语<br>
③<b>倒装句</b>：宾语前置/状语后置，翻译时调整语序<br>
④<b>被动句</b>："为……所……" / "见……于……"</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>默写训练（20min）</h4>
<div class="q-block"><b>默写1</b>：《天净沙·秋思》马致远<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">枯藤老树昏鸦，小桥流水人家，古道西风瘦马。夕阳西下，断肠人在天涯。</div></div>
<div class="q-block"><b>翻译</b>："学而时习之，不亦说乎"是什么意思？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">学习了然后按时温习，不也是很愉快的吗？——"说"通"悦"，高兴。注意"时"是"按时"不是"时常"！</div></div>
<div class="q-block"><b>判断句式</b>："陈胜者，阳城人也"是什么句式？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">判断句。"……者，……也"是典型的判断句式。翻译：陈胜是阳城人。</div></div>
</div>
<div class="step"><h4><span class="dot" style="background:var(--green)"></span>固（10min）</h4>
<div class="err-box"><b>❗ 默写常见扣分点</b><br>1. 同音错字：如"生"写成"升"、"涯"写成"崖" → 只要错别字就扣分<br>2. 漏字添字：每句必须和原文一字不差<br>3. 字迹潦草：阅卷老师看不清就算错！</div></div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（10min）</h4><p>📔 抄写三道默写题中易错的字各5遍 📔 默写《天净沙·秋思》</p></div>
</div>
'''

ENGLISH_D3 = '''<h3 style="color:var(--green);border-bottom:2px solid var(--green);padding-bottom:6px;margin:20px 0 12px">🔤 英语 · 一般过去时（1h）</h3>
<div class="steps">
<div class="step"><h4><span class="dot" style="background:var(--green)"></span>讲（15min）</h4>
<p><b>一般过去时</b>——表示过去某个时间发生的动作或状态。</p>
<p>结构：<b>主语 + 动词过去式</b></p>
<p>标志词：yesterday, last week/month/year, ...ago, in 2020, just now</p>
<p><b>动词过去式变化</b>：①规则动词+ed（play→played, study→studied, stop→stopped）②不规则动词必须逐个背！</p>
<p><b>常见不规则动词</b>（中考必考15个）：go→went, do→did, have→had, see→saw, eat→ate, come→came, get→got, make→made, take→took, give→gave, buy→bought, think→thought, write→wrote, read→read(读音变), fly→flew</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（30min）</h4>
<div class="q-block"><span class="q-num">1.</span><span class="question">I ___ (go) to Beijing last summer.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">went（一般过去时，go→went）</div></div>
<div class="q-block"><span class="q-num">2.</span><span class="question">He ___ (not see) the movie yesterday.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">didn't see（过去时否定：didn't + 动词原形！易错：很多人写成didn't saw）</div></div>
<div class="q-block"><span class="q-num">3.</span><span class="question">Where ___ you ___ (go) last night?</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">did; go（疑问句：Did + 主语 + 动词原形）</div></div>
<div class="q-block"><span class="q-num">4.</span><span class="question">She ___ (read) three books last month.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">read /red/（read的过去式写法不变但读音变，read/riːd/→read/red/）</div></div>
</div>
</div>
'''

with open('C:/Users/Tebon/BangMaker/Claw/w1.html', 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0

# 1. Add showAns + SVG CSS
if 'function showAns' not in html:
    html = html.replace('function speak(text)',
        'function showAns(btn){var a=btn.nextElementSibling;a.classList.toggle("show");btn.textContent=a.classList.contains("show")?"隐藏答案":"点击查看答案";}\nfunction speak(text)')
    changes += 1; print('  + showAns()')

if '.svg-diagram{' not in html:
    html = html.replace('</style>', '.svg-diagram{text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px}\n.svg-diagram svg{max-width:100%;height:auto}\n</style>')
    changes += 1; print('  + SVG CSS')

# 2. Inject tips as step full cards INSIDE the target subject's steps div
# Config: (day_num, target_h3_index, tip_key)
TIP_CONFIG = [
    (1, 0, 'D1'),  # Day 1: Math is 1st h3 (index 0)
    (2, 0, 'D2'),  # Day 2: Math is 1st h3
    (3, 0, 'D3'),  # Day 3: Math is 1st h3
    (4, 1, 'D4'),  # Day 4: Physics is 2nd h3 (index 1)
]

gray_box_marker = '<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">'

for day_num, h3_idx, tip_key in TIP_CONFIG:
    # Find day and its content
    dm = f'<div class="dnum">Day {day_num}</div>'
    ndm = f'<div class="dnum">Day {day_num+1}</div>'
    ds = html.find(dm)
    de = html.find(ndm) if html.find(ndm) > 0 else len(html)
    day = html[ds:de]
    
    # Find subject h3
    h3s = list(re.finditer(r'<h3\b', day))
    if h3_idx >= len(h3s):
        print(f'  ✗ Day {day_num}: only {len(h3s)} h3, need {h3_idx+1}')
        continue
    
    target_h3 = h3s[h3_idx].start()
    
    # Find the boundary: either next h3 or gray box
    if h3_idx + 1 < len(h3s):
        boundary = h3s[h3_idx + 1].start()
    else:
        boundary = day.find(gray_box_marker)
        if boundary < 0:
            boundary = day.rfind('</div></div>')  # fallback: day end
    
    if boundary < 0:
        print(f'  ✗ Day {day_num}: no boundary found')
        continue
    
    # Within target section, find the steps close: </div>\n</div>
    section = day[target_h3:boundary]
    steps_close = section.rfind('</div>\n</div>')
    if steps_close < 0:
        steps_close = section.rfind('</div>')
    
    if steps_close < 0:
        print(f'  ✗ Day {day_num}: no steps close found')
        continue
    
    # Inject BEFORE steps close (inside steps div, as last card in grid)
    abs_pos = ds + target_h3 + steps_close
    injection = TIPS[tip_key]
    html = html[:abs_pos] + injection + html[abs_pos:]
    changes += 1
    print(f'  + Day {day_num}: tip injected inside steps grid')

# 3. Fix Day 1 English word step: change 'step' to 'step full'
# Find Day 1, English h3, first <div class="step"> after it
d1s = html.find('<div class="dnum">Day 1</div>')
d2s = html.find('<div class="dnum">Day 2</div>')
day1 = html[d1s:d2s]

eng_h3_pos = day1.find('第二部分：英语')
if eng_h3_pos > 0:
    after_eng = day1[eng_h3_pos:]
    # Find first <div class="step"> after English h3 (the word step)
    first_step = after_eng.find('<div class="step">')
    if first_step > 0:
        abs_step = d1s + eng_h3_pos + first_step
        html = html[:abs_step] + '<div class="step full">' + html[abs_step + len('<div class="step">'):]
        changes += 1
        print('  + Day 1: English word step → step full')

# 4. Add Day 3 Chinese + English supplements
# Inject AFTER the Math section + tip + check box, BEFORE the 30-word gray box
d3s = html.find('<div class="dnum">Day 3</div>')
d4s = html.find('<div class="dnum">Day 4</div>')
day3 = html[d3s:d4s]

if '文言文入门' not in day3:
    # Find injection point: the </div></div> (steps close) of the Math section
    # Then inject AFTER the check box, BEFORE the gray word box
    # Actually, inject BEFORE the gray box but ensure proper structure
    
    # Find gray box in day3
    gb_pos = day3.find(gray_box_marker)
    if gb_pos > 0:
        # Inject as complete subject blocks before gray box
        inject_block = '\n' + CHINESE_D3 + '\n' + ENGLISH_D3 + '\n'
        abs_gb = d3s + gb_pos
        html = html[:abs_gb] + inject_block + html[abs_gb:]
        changes += 1
        print('  + Day 3: Chinese + English supplements')
    else:
        print('  ✗ Day 3: gray box not found')

# Write
with open('C:/Users/Tebon/BangMaker/Claw/w1.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nDone: {changes} changes')
