#!/usr/bin/env python3
"""fix_w1_only.py - 只修复 w1.html: 添加 showAns/SVG CSS/tips/supplementary days"""
import re

CONTENT = {
    'D1': '<div class="svg-diagram" style="text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px"><svg viewBox="0 0 600 80"><line x1="40" y1="40" x2="560" y2="40" stroke="#333" stroke-width="2"/><polygon points="560,36 570,40 560,44" fill="#333"/><text x="20" y="44" font-size="12">←负</text><text x="570" y="44" font-size="12">正→</text><text x="295" y="35" font-size="14" fill="var(--red)" font-weight="bold">0</text><circle cx="300" cy="40" r="4" fill="var(--red)"/><circle cx="200" cy="40" r="4" fill="var(--blue)"/><text x="195" y="25" font-size="11" fill="var(--blue)">-a</text><text x="195" y="65" font-size="10" fill="#888">|a|</text><circle cx="400" cy="40" r="4" fill="var(--blue)"/><text x="395" y="25" font-size="11" fill="var(--blue)">+a</text><text x="395" y="65" font-size="10" fill="#888">|a|</text></svg><p style="font-size:11px;color:var(--sub)">|a| = a(a≥0), |a| = -a(a<0) → 绝对值是到原点的距离</p></div>\n<div class="tip"><b>💡 有理数运算方法总结</b><br>定符号→算数值→"先乘方再乘除后加减有括号先括号"<br>去绝对值:|a|=a(a≥0),|a|=-a(a<0)<br>遇括号能用分配律的先用分配律</div>',
    'D2': '<div class="tip"><b>💡 整式乘除方法总结</b><br>同底数幂:乘加除减 aᵐ×aⁿ=aᵐ⁺ⁿ,aᵐ÷aⁿ=aᵐ⁻ⁿ|幂的乘方:(aᵐ)ⁿ=aᵐⁿ<br>平方差:(a+b)(a-b)=a²-b²|完全平方:(a±b)²=a²±2ab+b²"首平方尾平方2倍首尾放中央"<br>⚠️(-2)⁴=16≠-2⁴=-16！完全平方中间项2ab最易漏！</div>',
    'D3': '<div class="tip"><b>💡 方程不等式方法总结</b><br>五步法:去分母→去括号→移项变号→合并→系数化1<br>代入vs加减:系数差1倍→加减法;系数为1→代入法<br>不等式:乘除负数必须变号!>变<!口诀"同大取大同小取小"</div>',
    'D4': '<div class="svg-diagram" style="text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px"><svg viewBox="0 0 500 200"><line x1="250" y1="10" x2="250" y2="190" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/><text x="255" y="15" font-size="10" fill="#999">法线</text><line x1="60" y1="120" x2="250" y2="90" stroke="var(--orange)" stroke-width="2"/><polygon points="250,90 240,85 240,95" fill="var(--orange)"/><text x="100" y="100" font-size="11" fill="var(--orange)">入射光线</text><line x1="250" y1="90" x2="440" y2="120" stroke="var(--green)" stroke-width="2"/><polygon points="440,120 430,115 430,125" fill="var(--green)"/><text x="350" y="108" font-size="11" fill="var(--green)">反射光线</text><path d="M 230 70 A 50 50 0 0 1 270 70" fill="none" stroke="var(--red)" stroke-width="1.5"/><text x="255" y="65" font-size="10" fill="var(--red)">θ</text><path d="M 270 70 A 50 50 0 0 1 230 70" fill="none" stroke="var(--red)" stroke-width="1.5"/><text x="235" y="110" font-size="10" fill="var(--red)">θ</text><text x="260" y="170" font-size="11">反射角=入射角（三线共面两线分居）</text></svg></div>\n<div class="tip"><b>💡 光的反射与成像</b><br>反射定律:三线共面|两线分居|反射角=入射角(先画法线!)<br>平面镜成像四特点:等大/等距/垂直/虚像<br>镜面vs漫反射:都遵循反射定律!</div>',
}

# Chinese/English supplements for w1 Day 3
CHINESE_W1_D3_TITLE = '📖 语文 · 古诗文默写+文言文入门（1h）'
CHINESE_W1_D3 = '''<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（20min）</h4>
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
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（10min）</h4><p>📔 抄写三道默写题中易错的字各5遍 📔 默写《天净沙·秋思》</p></div>'''

ENGLISH_W1_D3_TITLE = '🔤 英语 · 一般过去时（1h）'
ENGLISH_W1_D3 = '''<div class="step"><h4><span class="dot" style="background:var(--green)"></span>讲（15min）</h4>
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
</div>'''

with open('C:/Users/Tebon/BangMaker/Claw/w1.html', 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0

# 1. Add showAns function (before speak function)
if 'function showAns' not in html:
    html = html.replace(
        'function speak(text)',
        'function showAns(btn){var a=btn.nextElementSibling;a.classList.toggle("show");btn.textContent=a.classList.contains("show")?"隐藏答案":"点击查看答案";}\nfunction speak(text)'
    )
    changes += 1
    print('  + Added showAns() function')

# 2. Add SVG diagram CSS
if '.svg-diagram{' not in html:
    html = html.replace(
        '</style>',
        '.svg-diagram{text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px}\n.svg-diagram svg{max-width:100%;height:auto}\n</style>'
    )
    changes += 1
    print('  + Added .svg-diagram CSS')

# 3. Inject SVG/tips for Days 1-4
# Strategy: find the target subject's h3, then find the section boundary (next h3, or gray box),
# find the last </div></div> (steps close) within that range, inject after it.

# Day-specific config: (target_h3_index, subject_name)
# Day 1: Math is 1st h3, boundary is 2nd h3 (English)
# Day 2: Math is 1st h3, boundary is 2nd h3 (Physics)
# Day 3: Math is 1st h3, boundary is gray box (English has no h3)
# Day 4: Physics is 2nd h3, boundary is gray box (English has no h3)

TIPS_CONFIG = [
    (1, 0, '数学 · 有理数', '有理数运算方法总结'),
    (2, 0, '数学 · 整式乘除', '整式乘除方法总结'),
    (3, 0, '数学 · 方程', '方程不等式方法总结'),
    (4, 1, '物理 · 光的反射', '光的反射与成像'),
]

gray_box_start = '<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">'

for day_num, h3_idx, subject_hint, check_phrase in TIPS_CONFIG:
    dkey = f'D{day_num}'
    if dkey not in CONTENT:
        continue
    
    # Find Day N section
    day_marker = f'<div class="dnum">Day {day_num}</div>'
    day_pos = html.find(day_marker)
    if day_pos == -1:
        print(f'  ✗ Day {day_num}: marker not found')
        continue
    
    # Find next day boundary
    next_day_pos = html.find('<div class="dnum">Day', day_pos + len(day_marker))
    search_end = next_day_pos if next_day_pos > 0 else len(html)
    day_content = html[day_pos:search_end]
    
    # Check if already injected
    if check_phrase in day_content:
        print(f'  - Day {day_num}: content already injected, skipping')
        continue
    
    # Find all h3 tags within this day
    h3_matches = list(re.finditer(r'<h3\b[^>]*>', day_content))
    
    if h3_idx >= len(h3_matches):
        print(f'  ✗ Day {day_num}: h3 index {h3_idx} out of range (has {len(h3_matches)})')
        continue
    
    target_h3_start = h3_matches[h3_idx].start()
    
    # Determine the boundary (end of target section)
    # If there's a next h3, use it. Otherwise, use the gray box.
    if h3_idx + 1 < len(h3_matches):
        boundary_pos = h3_matches[h3_idx + 1].start()
    else:
        boundary_pos = day_content.find(gray_box_start)
        if boundary_pos < 0:
            boundary_pos = day_content.rfind('</div></div>')  # fallback: end of day
    
    if boundary_pos < 0:
        print(f'  ✗ Day {day_num}: cannot find section boundary')
        continue
    
    # Within the target section, find the last </div></div> (steps close)
    between = day_content[target_h3_start:boundary_pos]
    steps_close = between.rfind('</div>\n</div>')
    if steps_close < 0:
        steps_close = between.rfind('</div>')
        # Try to find a pair
        if steps_close >= 0:
            prev = between.rfind('</div>', 0, steps_close - 2)
            if prev >= 0:
                steps_close = prev
    
    if steps_close < 0:
        print(f'  ✗ Day {day_num}: cannot find steps close in section')
        continue
    
    # Inject after the steps close
    abs_inject = day_pos + target_h3_start + steps_close + len('</div>\n</div>')
    injection = '\n' + CONTENT[dkey] + '\n'
    html = html[:abs_inject] + injection + html[abs_inject:]
    changes += 1
    print(f'  + Day {day_num}: injected tip after {subject_hint} section')

# Re-define gray_box_start for Chinese/English supplement injection
gray_box_start = '<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">'

# 4. Add Chinese and English supplements for Day 3 (add_supplements_v2.js w1 part)
# Find Day 3 section
day3_marker = '<div class="dnum">Day 3</div>'
day3_pos = html.find(day3_marker)
day4_marker = '<div class="dnum">Day 4</div>'
day4_pos = html.find(day4_marker)
day3_content = html[day3_pos:day4_pos]

# Add Chinese section for Day 3
if '文言文' not in day3_content and '古诗文默写' not in day3_content:
    # Find injection point: before the gray box (word list)
    gray_pos = day3_content.find(gray_box_start)
    if gray_pos > 0:
        abs_pos = day3_pos + gray_pos
        chi_block = f'<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:20px 0 12px">{CHINESE_W1_D3_TITLE}</h3>\n<div class="steps">\n{CHINESE_W1_D3}\n</div>\n\n'
        html = html[:abs_pos] + chi_block + html[abs_pos:]
        changes += 1
        print('  + Day 3: added Chinese (古诗文+文言文入门)')
        
        # Recalculate positions
        day3_pos = html.find(day3_marker)
        day4_pos = html.find(day4_marker)
        day3_content = html[day3_pos:day4_pos]

# Add English grammar for Day 3
if '一般过去时' not in day3_content and '过去时' not in day3_content:
    gray_pos = day3_content.find(gray_box_start)
    if gray_pos > 0:
        abs_pos = day3_pos + gray_pos
        eng_block = f'<h3 style="color:var(--green);border-bottom:2px solid var(--green);padding-bottom:6px;margin:20px 0 12px">{ENGLISH_W1_D3_TITLE}</h3>\n<div class="steps">\n{ENGLISH_W1_D3}\n</div>\n\n'
        html = html[:abs_pos] + eng_block + html[abs_pos:]
        changes += 1
        print('  + Day 3: added English (一般过去时)')

# Write result
with open('C:/Users/Tebon/BangMaker/Claw/w1.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nDone: {changes} changes made to w1.html')
