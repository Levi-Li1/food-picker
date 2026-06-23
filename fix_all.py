#!/usr/bin/env python3
"""fix_all.py - fix w1+w2-w9: remove w1 duplicates, apply styling to w2-w9"""
import re

def fix_w1():
    """Rebuild w1 from clean git, apply all fixes, NO duplicates"""
    # Step A: restore w1
    import os
    os.system('cd /c/Users/Tebon/BangMaker/Claw && git checkout 8ccf09a -- w1.html')
    
    with open('C:/Users/Tebon/BangMaker/Claw/w1.html','r',encoding='utf-8') as f:
        html = f.read()
    
    changes = 0
    
    # 1. showAns + SVG CSS
    if 'function showAns' not in html:
        html = html.replace('function speak(text)',
            'function showAns(btn){var a=btn.nextElementSibling;a.classList.toggle("show");btn.textContent=a.classList.contains("show")?"隐藏答案":"点击查看答案";}\nfunction speak(text)')
        changes += 1
    
    if '.svg-diagram{' not in html:
        html = html.replace('</style>',
            '.svg-diagram{text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px}\n.svg-diagram svg{max-width:100%;height:auto}\n</style>')
        changes += 1
    
    # 2. Tips as step full cards inside subject steps grid
    TIPS = {
        'D1_text': '<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>💡 有理数运算方法总结</h4><p style="font-size:13px">定符号→算数值→"先乘方再乘除后加减有括号先括号"<br>去绝对值:|a|=a(a≥0),|a|=-a(a<0)<br>遇括号能用分配律的先用分配律</p></div>\n',
        'D2': '<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>💡 整式乘除方法总结</h4><p style="font-size:13px">同底数幂:乘加除减 a<sup>m</sup>×aⁿ=a<sup>m</sup>⁺ⁿ,a<sup>m</sup>÷aⁿ=a<sup>m</sup>⁻ⁿ|幂的乘方:(a<sup>m</sup>)ⁿ=a<sup>m</sup>ⁿ<br>平方差:(a+b)(a-b)=a²-b²|完全平方:(a±b)²=a²±2ab+b²"首平方尾平方2倍首尾放中央"<br>⚠️(-2)⁴=16≠-2⁴=-16！完全平方中间项2ab最易漏！</p></div>\n',
        'D3': '<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>💡 方程不等式方法总结</h4><p style="font-size:13px">五步法:去分母→去括号→移项变号→合并→系数化1<br>代入vs加减:系数差1倍→加减法;系数为1→代入法<br>不等式:乘除负数必须变号!>变<!口诀"同大取大同小取小"</p></div>\n',
        'D4': '<div class="step full"><h4><span class="dot" style="background:var(--orange)"></span>💡 光的反射与成像</h4><div class="svg-diagram" style="text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px"><svg viewBox="0 0 500 200"><line x1="250" y1="10" x2="250" y2="190" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/><text x="255" y="15" font-size="10" fill="#999">法线</text><line x1="60" y1="120" x2="250" y2="90" stroke="var(--orange)" stroke-width="2"/><polygon points="250,90 240,85 240,95" fill="var(--orange)"/><text x="100" y="100" font-size="11" fill="var(--orange)">入射光线</text><line x1="250" y1="90" x2="440" y2="120" stroke="var(--green)" stroke-width="2"/><polygon points="440,120 430,115 430,125" fill="var(--green)"/><text x="350" y="108" font-size="11" fill="var(--green)">反射光线</text><path d="M 230 70 A 50 50 0 0 1 270 70" fill="none" stroke="var(--red)" stroke-width="1.5"/><text x="255" y="65" font-size="10" fill="var(--red)">θ</text><path d="M 270 70 A 50 50 0 0 1 230 70" fill="none" stroke="var(--red)" stroke-width="1.5"/><text x="235" y="110" font-size="10" fill="var(--red)">θ</text><text x="260" y="170" font-size="11">反射角=入射角（三线共面两线分居）</text></svg></div><p style="margin-top:8px;font-size:13px">反射定律:三线共面|两线分居|反射角=入射角(先画法线!)<br>平面镜成像四特点:等大/等距/垂直/虚像<br>镜面vs漫反射:都遵循反射定律!</p></div>\n',
    }
    
    SVG_D1 = '<div class="svg-diagram" style="text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px"><svg viewBox="0 0 600 80"><line x1="40" y1="40" x2="560" y2="40" stroke="#333" stroke-width="2"/><polygon points="560,36 570,40 560,44" fill="#333"/><text x="20" y="44" font-size="12">←负</text><text x="570" y="44" font-size="12">正→</text><text x="295" y="35" font-size="14" fill="var(--red)" font-weight="bold">0</text><circle cx="300" cy="40" r="4" fill="var(--red)"/><circle cx="200" cy="40" r="4" fill="var(--blue)"/><text x="195" y="25" font-size="11" fill="var(--blue)">-a</text><text x="195" y="65" font-size="10" fill="#888">|a|</text><circle cx="400" cy="40" r="4" fill="var(--blue)"/><text x="395" y="25" font-size="11" fill="var(--blue)">+a</text><text x="395" y="65" font-size="10" fill="#888">|a|</text></svg><p style="font-size:11px;color:var(--sub);text-align:center">|a| = a(a≥0), |a| = -a(a<0) → 绝对值是到原点的距离</p></div>\n'
    
    # Inject tip as step full card in Math (Day1/2/3) or Physics (Day4) steps grid
    tip_config = [(1,0,'D1_text'), (2,0,'D2'), (3,0,'D3'), (4,1,'D4')]
    for day_num, h3_idx, tip_key in tip_config:
        dm = f'<div class="dnum">Day {day_num}</div>'
        ndm = f'<div class="dnum">Day {day_num+1}</div>'
        ds = html.find(dm)
        de = html.find(ndm) if html.find(ndm) > 0 else len(html)
        day = html[ds:de]
        
        h3s = list(re.finditer(r'<h3\b', day))
        if h3_idx >= len(h3s): continue
        target = h3s[h3_idx].start()
        
        gb = '<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">'
        boundary = h3s[h3_idx+1].start() if h3_idx+1 < len(h3s) else (day.find(gb) if day.find(gb)>=0 else day.rfind('</div></div>'))
        if boundary < 0: continue
        
        section = day[target:boundary]
        sc = section.rfind('</div>\n</div>')
        if sc < 0: sc = section.rfind('</div>')
        if sc < 0: continue
        
        abs_pos = ds + target + sc
        html = html[:abs_pos] + TIPS[tip_key] + html[abs_pos:]
        changes += 1
    
    # 3. SVG number line at 1.4
    d1s = html.find('<div class="dnum">Day 1</div>')
    eq = html.find('|a| ≥ 0', d1s)
    if eq > 0:
        mp = html.find('&lt;0时', eq)
        if mp > 0:
            am = html.find('</div>', mp)
            fc = html.find('</div>', am + 6)
            html = html[:fc] + '\n' + SVG_D1 + html[fc:]
            changes += 1
    
    # 4. Day 1 English step → step full
    d1s = html.find('<div class="dnum">Day 1</div>')
    d2s = html.find('<div class="dnum">Day 2</div>')
    day1 = html[d1s:d2s]
    ep = day1.find('第二部分：英语')
    if ep > 0:
        fs = day1[ep:].find('<div class="step">')
        if fs > 0:
            asp = d1s + ep + fs
            html = html[:asp] + '<div class="step full">' + html[asp + len('<div class="step">'):]
            changes += 1
    
    # 5. Day 3 Chinese + English supplements
    d3s = html.find('<div class="dnum">Day 3</div>')
    d4s = html.find('<div class="dnum">Day 4</div>')
    if d3s > 0 and d4s > 0 and '文言文入门' not in html[d3s:d4s]:
        gb = '<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">'
        gb3 = html.find(gb, d3s)
        if gb3 > 0 and gb3 < d4s:
            # Load content from separate file
            from pathlib import Path
            base = Path('C:/Users/Tebon/BangMaker/Claw')
            # Read content from fix_w1_v2.py
            with open(base / 'fix_w1_v2.py', 'r', encoding='utf-8') as ff:
                fw1 = ff.read()
            # Extract CHINESE_D3 and ENGLISH_D3
            chi_start = fw1.find("CHINESE_D3 = '''") + len("CHINESE_D3 = '''")
            chi_end = fw1.find("'''", chi_start)
            CHN = fw1[chi_start:chi_end]
            
            eng_start = fw1.find("ENGLISH_D3 = '''") + len("ENGLISH_D3 = '''")
            eng_end = fw1.find("'''", eng_start)
            ENG = fw1[eng_start:eng_end]
            
            inject = '\n' + CHN + '\n' + ENG + '\n'
            html = html[:gb3] + inject + html[gb3:]
            changes += 1
    
    # 6. Blue buttons + sup m
    html = html.replace('background:#8e8e93;color:#fff', 'background:var(--blue);color:#fff')
    html = html.replace('ᵐ', '<sup>m</sup>')
    
    with open('C:/Users/Tebon/BangMaker/Claw/w1.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'w1: {changes} changes applied')


def fix_all_weeks():
    """Apply styling fixes to all w2-w9 files"""
    import os
    base = 'C:/Users/Tebon/BangMaker/Claw'
    
    for fn in ['w2.html','w3.html','w4.html','w5.html','w6.html','w7.html','w8.html','w9.html']:
        fp = os.path.join(base, fn)
        with open(fp, 'r', encoding='utf-8') as f:
            html = f.read()
        
        c = 0
        # Blue buttons
        count = html.count('background:#8e8e93;color:#fff')
        if count > 0:
            html = html.replace('background:#8e8e93;color:#fff', 'background:var(--blue);color:#fff')
            c += count
        
        # Superscript m
        mcount = html.count('ᵐ')
        if mcount > 0:
            html = html.replace('ᵐ', '<sup>m</sup>')
            c += mcount
        
        if c > 0:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'{fn}: {c} changes ({count} buttons, {mcount} sup m)')
        else:
            print(f'{fn}: no changes needed')


if __name__ == '__main__':
    fix_w1()
    print()
    fix_all_weeks()
