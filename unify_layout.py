#!/usr/bin/env python3
"""Unify layout: non-English sections = all step full (full-width stack, matching W1 standard).
Runs as pipeline step after convert_to_qblock.py."""
import re, glob

def process_file(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c
    
    # Collect all replacements first (to avoid position shift bug)
    replacements = []
    
    days = list(re.finditer(r'<div class="day-page">', c))
    for i, dm in enumerate(days):
        day_end = days[i+1].start() if i+1 < len(days) else len(c)
        day = c[dm.start():day_end]
        
        h3s = list(re.finditer(r'<h3[^>]*>(.*?)</h3>', day))
        
        for j, h3 in enumerate(h3s):
            if '英语' in h3.group(1):
                continue
            
            sec_start = dm.start() + h3.end()
            next_h3_end = dm.start() + h3s[j+1].start() if j+1 < len(h3s) else day_end
            check_pos = c.find('<div class="check">', sec_start, next_h3_end)
            sec_end = check_pos if check_pos > 0 else next_h3_end
            
            section = c[sec_start:sec_end]
            new_section = section.replace('<div class="step">', '<div class="step full">')
            new_section = new_section.replace('step full full', 'step full')
            
            if new_section != section:
                replacements.append((sec_start, sec_end, new_section))
    
    # Apply in reverse order
    count = 0
    for start, end, new_text in reversed(replacements):
        c = c[:start] + new_text + c[end:]
        count += 1
    
    if c != orig:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(c)
        return True, count
    return False, 0

# Run on all w*.html
total = 0
for fname in sorted(glob.glob('C:/Users/Tebon/BangMaker/Claw/w*.html')):
    if 'test' in fname: continue
    mod, count = process_file(fname)
    if mod:
        print(f'{fname}: {count} sections unified')
        total += count
    else:
        print(f'{fname}: already unified')

print(f'\nTotal sections unified: {total}')
