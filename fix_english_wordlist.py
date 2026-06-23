"""Fix English section: move word list inside the 讲 step, make it step full."""
import re

for wnum in range(2, 10):
    fname = f'C:/Users/Tebon/BangMaker/Claw/w{wnum}.html'
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            h = f.read()
    except FileNotFoundError:
        continue
    
    original = h
    fixed_count = 0
    
    # Find all English h3 sections
    for m in re.finditer(r'<h3[^>]*?>(.*?英语.*?)</h3>', h):
        h3_pos = m.start()
        h3_end = m.end()
        h3_text = m.group(1)
        
        # Find the steps container after this h3
        steps_start = h.find('<div class="steps">', h3_end)
        if steps_start == -1:
            continue
        
        # Find the first step (讲) after steps_start
        first_step = h.find('<div class="step">', steps_start)
        if first_step == -1:
            first_step = h.find('<div class="step full">', steps_start)
        if first_step == -1:
            continue
        
        # Find the word list after the h3
        wl_start = h.find('background:#f0f0f5', h3_end)
        if wl_start == -1:
            continue
        
        # Backtrack to find the opening <div for the word list
        wl_div_open = h.rfind('<div', 0, wl_start)
        if wl_div_open == -1:
            continue
        
        # Find matching close for the word list div
        # Count nesting from wl_div_open
        depth = 0
        wl_div_close = -1
        i = wl_div_open
        while i < len(h):
            tag = h[i:i+5]
            if h[i:i+4] == '<div':
                # Only count structural divs
                if h[i:i+5] != '<div ' and h[i:i+5] != '<div>':
                    pass  # Not a div tag
                else:
                    depth += 1
                    i += 4
                    continue
            
            if h[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    wl_div_close = i + 6
                    break
                i += 6
                continue
            
            i += 1
        
        if wl_div_close == -1 or wl_div_close <= wl_start:
            continue
        
        # Extract the word list content (including the opening div)
        wl_content = h[wl_div_open:wl_div_close]
        
        # Find the opening tag of the first step (讲)
        step_tag_end = h.find('>', first_step) + 1
        
        # Now we need to find where the 讲 step closes
        # The 讲 step is the first step inside this steps container
        # We need to find its matching </div>
        
        # Strategy: count div nesting from step_tag_end
        depth = 1  # We're inside the step div
        step_close = -1
        i = step_tag_end
        while i < len(h):
            if h[i:i+4] == '<div':
                depth += 1
                i += 4
                continue
            if h[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    step_close = i
                    break
                i += 6
                continue
            i += 1
        
        if step_close == -1 or step_close <= step_tag_end:
            continue
        
        # Verify: the word list should be AFTER the 讲 step close (currently)
        if wl_div_open < step_close:
            # Word list is already inside the step? Skip
            continue
        
        # NEW APPROACH: 
        # 1. Remove the word list from its current position
        # 2. Insert it before the 讲 step's closing </div>
        # 3. Change class="step"> to class="step full"> for 讲
        
        # Cut out word list
        before_wl = h[:wl_div_open]
        after_wl = h[wl_div_close:]
        
        # Check what's between step_close and wl_div_open
        # This should just be structural div closes (</div> for 练 step, </div> for steps)
        
        # Remove the word list
        h_temp = before_wl + after_wl
        
        # Now recalculate positions in h_temp
        # Find the 讲 step in h_temp
        first_step2 = h_temp.find('<div class="step">', steps_start)
        if first_step2 == -1:
            first_step2 = h_temp.find('<div class="step full">', steps_start)
        if first_step2 == -1:
            continue
        
        # Find the 讲 step's closing </div>
        step_tag_end2 = h_temp.find('>', first_step2) + 1
        depth = 1
        step_close2 = -1
        i = step_tag_end2
        while i < len(h_temp):
            if h_temp[i:i+4] == '<div':
                depth += 1
                i += 4
                continue
            if h_temp[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    step_close2 = i
                    break
                i += 6
                continue
            i += 1
        
        if step_close2 == -1:
            continue
        
        # Insert word list before the 讲 step's closing </div>
        h_final = h_temp[:step_close2] + wl_content + h_temp[step_close2:]
        
        # Change class="step" to class="step full" for the 讲 step
        # The 讲 step should now be class="step full"
        old_tag = '<div class="step">'
        new_tag = '<div class="step full">'
        # Only change the FIRST occurrence after steps_start
        steps_end_pos = h_final.find('<div class="steps">', steps_start)
        if steps_end_pos >= 0:
            tag_pos = h_final.find(old_tag, steps_end_pos)
            if tag_pos >= 0:
                h_final = h_final[:tag_pos] + new_tag + h_final[tag_pos+len(old_tag):]
        
        h = h_final
        fixed_count += 1
        print(f'  w{wnum}: Fixed English section "{h3_text[:50]}..."')
    
    if fixed_count > 0:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(h)
        print(f'w{wnum}: {fixed_count} English sections fixed')
    else:
        print(f'w{wnum}: No fixes needed')

print('\nDone!')
