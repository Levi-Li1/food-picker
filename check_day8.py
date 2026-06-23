#!/usr/bin/env python3
"""Check Day 8 - line-based regex tracking"""
import re

with open('C:/Users/Tebon/BangMaker/Claw/w2.html', 'r', encoding='utf-8') as f:
    html = f.read()

dp = html.find('<div class="day-page">')
next_dp = html.find('<div class="day-page">', dp+1)
day = html[dp:next_dp]

depth = 0
for line in day.split('\n'):
    o = len(re.findall(r'<div\b[^>]*>', line))
    c = len(re.findall(r'</div>', line))
    
    shown = False
    for tag in ['class="day-page"', 'class="dbody"', 'class="dtop"', '<h3', 'class="steps"', 'class="step"', 'class="check"', 'class="goal"']:
        if tag in line:
            d_before = depth
            s = line.strip()[:140]
            print(f'd={d_before:2d} {s}')
            shown = True
            break
    
    if not shown:
        for tag in ['今日30词', 'svg-diagram', '▶ 按钮听发音']:
            if tag in line:
                print(f'd={depth:2d} 💬 {line.strip()[:120]}')
                shown = True
                break
    
    if not shown and depth <= 3:
        d_after = depth + o - c
        if d_after < depth or (c > 0 and d_after <= 3):
            print(f'd={depth:2d}↘{d_after} ({c}x</div>)')
    
    depth = depth + o - c

print(f'\nFinal depth: {depth}')
