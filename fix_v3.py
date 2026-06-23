"""Fix w2-w9: inline step split + move English word list inside 讲 step.
Processes English sections from END to START to avoid position shifts.
"""
import re

def find_matching_close(text, start_pos):
    """Find the matching </div> position for a <div at start_pos."""
    depth = 1
    i = text.find('>', start_pos) + 1
    while i < len(text):
        if text[i:i+4] == '<div':
            depth += 1
            i += 4
        elif text[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                return i
            i += 6
        else:
            i += 1
    return -1

def find_div_open_before_attr(text, search_start, attr):
    """Find <div opening tag position before attr substring."""
    pos = text.find(attr, search_start)
    if pos == -1:
        return -1
    return text.rfind('<div', 0, pos + len(attr))

for wnum in range(2, 10):
    fname = f'C:/Users/Tebon/BangMaker/Claw/w{wnum}.html'
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            h = f.read()
    except FileNotFoundError:
        continue
    
    # --- Fix 1: Split inline steps ---
    h = h.replace('</div><div class="step"', '</div>\n<div class="step"')
    h = h.replace('</div><div class="step full"', '</div>\n<div class="step full"')
    
    # --- Fix 2: Split dbody+h3 on same line ---
    h = h.replace('<div class="dbody"><h3', '<div class="dbody">\n<h3')
    
    # --- Fix 3: Find all English h3 sections ---
    # Match h3 tags whose TEXT content contains 英语 (no HTML inside)
    english_sections = []
    for m in re.finditer(r'<h3[^>]*>([^<]*英语[^<]*)</h3>', h):
        english_sections.append({
            'h3_start': m.start(),
            'h3_end': m.end(),
            'h3_text': m.group(1)
        })
    
    if not english_sections:
        print(f'w{wnum}: no English h3 sections found')
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(h)
        continue
    
    english_fixes = 0
    
    # Process from LAST to FIRST
    for sec in reversed(english_sections):
        h3_start = sec['h3_start']
        h3_end = sec['h3_end']
        
        # Find steps container after h3
        steps_pos = h.find('<div class="steps">', h3_end)
        if steps_pos == -1:
            continue
        
        # Find the first <div class="step" (NOT step full) after steps
        # The 讲 step should be class="step" (we'll change to step full)
        pat = re.compile(r'<div class="step">', re.DOTALL)
        step_match = pat.search(h, steps_pos)
        if not step_match:
            # Check if already step full
            pat_full = re.compile(r'<div class="step full">', re.DOTALL)
            step_match = pat_full.search(h, steps_pos)
            if step_match:
                continue  # Already correct
        
        if not step_match:
            continue
        
        step_open = step_match.start()
        
        # Find the 讲 step's closing </div>
        step_close = find_matching_close(h, step_open)
        if step_close == -1:
            continue
        
        # Find word list after h3
        wl_open = find_div_open_before_attr(h, h3_end, 'background:#f0f0f5')
        if wl_open == -1:
            continue
        
        # Word list must be AFTER the 讲 step close
        if wl_open <= step_close:
            continue
        
        # Find word list's matching close
        wl_close = find_matching_close(h, wl_open)
        if wl_close == -1:
            continue
        
        # Extract components
        wl_content = h[wl_open:wl_close + 6]  # include the closing </div>
        
        # Reconstruct:
        before_step_close = h[:step_close]
        between_step_and_wl = h[step_close:wl_open]
        after_wl = h[wl_close + 6:]
        
        # Change class="step"> to class="step full"> in the step opening
        old_class = 'class="step">'
        new_class = 'class="step full">'
        class_pos = before_step_close.rfind(old_class, step_open)
        if class_pos != -1:
            before_step_close = (before_step_close[:class_pos] + new_class + 
                               before_step_close[class_pos + len(old_class):])
        
        # Reassemble
        h = before_step_close + wl_content + between_step_and_wl + after_wl
        english_fixes += 1
        print(f'  w{wnum}: Fixed "{sec["h3_text"][:50]}"')
    
    if english_fixes > 0:
        print(f'w{wnum}: {english_fixes} English sections fixed')
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(h)

print('Done!')
