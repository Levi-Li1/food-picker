"""Post-process w2-w9: add steps wrappers, fix English word list nesting, inline step split."""
import re

def find_all_needles(text, needle):
    """Find all positions of needle in text."""
    positions = []
    pos = 0
    while True:
        pos = text.find(needle, pos)
        if pos == -1:
            break
        positions.append(pos)
        pos += len(needle)
    return positions

for wnum in range(2, 10):
    fname = f'C:/Users/Tebon/BangMaker/Claw/w{wnum}.html'
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            h = f.read()
    except FileNotFoundError:
        continue
    
    # --- Step 1: Split inline steps ---
    h = h.replace('</div><div class="step"', '</div>\n<div class="step"')
    h = h.replace('</div><div class="step full"', '</div>\n<div class="step full"')
    
    # --- Step 2: Split dbody+h3 ---
    h = h.replace('<div class="dbody"><h3', '<div class="dbody">\n<h3')
    
    # --- Step 3: Add steps wrappers and fix English word lists ---
    # Find all day-pages
    day_starts = [m.start() for m in re.finditer(r'<div class="day-page">', h)]
    
    new_parts = []
    prev_end = 0
    
    for ds in day_starts:
        # Find end of this day-page (next day-page or end of container)
        next_ds = h.find('<div class="day-page">', ds + 20)
        if next_ds == -1:
            # Find end of container
            container_end = h.find('</div>\n\n</div>', ds)
            if container_end == -1:
                day_end = len(h)
            else:
                day_end = container_end
        else:
            day_end = next_ds
        
        # Everything before this day-page
        new_parts.append(h[prev_end:ds])
        
        day_content = h[ds:day_end]
        
        # Find h3 sections within this day
        h3_positions = [(m.start(), m.end(), m.group(1)) 
                       for m in re.finditer(r'<h3[^>]*>([^<]*)</h3>', day_content)]
        
        if not h3_positions:
            new_parts.append(day_content)
            prev_end = day_end
            continue
        
        # Find dbody position
        dbody_start = day_content.find('<div class="dbody">')
        if dbody_start == -1:
            new_parts.append(day_content)
            prev_end = day_end
            continue
        
        # Content before first h3 (dtop + goal)
        before_first_h3 = day_content[:h3_positions[0][0]]
        
        # Process each h3 section
        sections = []
        for i, (h3_start, h3_end, h3_text) in enumerate(h3_positions):
            # Determine content of this section: from h3_end to next h3 or end of day
            if i + 1 < len(h3_positions):
                section_end = h3_positions[i + 1][0]
            else:
                # Last section: go until check div or end of day
                check_pos = day_content.find('<div class="check">', h3_end)
                if check_pos != -1:
                    section_end = check_pos
                else:
                    # Go until the closing divs of dbody/day-page
                    section_end = len(day_content)
            
            section_body = day_content[h3_end:section_end]
            h3_tag = day_content[h3_start:h3_end]
            
            is_english = '英语' in h3_text
            
            # Step cards: find all <div class="step" and <div class="step full" 
            # that appear before any non-step div
            # Strategy: wrap consecutive step cards in <div class="steps">
            
            # Find all step opens
            step_pattern = re.compile(r'<div class="step[\s">]')
            step_matches = list(step_pattern.finditer(section_body))
            
            if step_matches:
                # Find the first non-step, non-h3 opening div
                # We'll wrap all step cards into a steps container
                first_step = step_matches[0].start()
                last_step_end = -1
                
                # Track from first step to find where the consecutive steps end
                pos = first_step
                depth = 0
                in_steps = False
                step_count = 0
                steps_close_needed = 0
                
                # Simpler approach: find the first step, find its closing div,
                # then find the next step, etc. Collect all step boundaries.
                step_ranges = []
                for sm in step_matches:
                    step_open = sm.start()
                    # Find matching close for this step
                    d = 0
                    j = sm.end()
                    # Find the > that closes the opening tag
                    gt = section_body.find('>', step_open)
                    if gt == -1:
                        continue
                    d = 1
                    j = gt + 1
                    while j < len(section_body):
                        if section_body[j:j+4] == '<div':
                            d += 1
                            j += 4
                        elif section_body[j:j+6] == '</div>':
                            d -= 1
                            if d == 0:
                                step_ranges.append((step_open, j + 6))
                                break
                            j += 6
                        else:
                            j += 1
                
                if step_ranges:
                    # Check if there's content between step cards that isn't a step
                    # (like word list div)
                    between_content = []
                    for si in range(len(step_ranges)):
                        if si > 0:
                            between = section_body[step_ranges[si-1][1]:step_ranges[si][0]]
                            between_content.append(between.strip())
                    
                    # If all between-content is empty (just whitespace/newlines), wrap in steps
                    all_empty_between = all(not b or b.isspace() for b in between_content)
                    
                    if all_empty_between:
                        # Wrap consecutive steps
                        steps_start_pos = step_ranges[0][0]
                        steps_end_pos = step_ranges[-1][1]
                        
                        before_steps = section_body[:steps_start_pos]
                        steps_content = section_body[steps_start_pos:steps_end_pos]
                        after_steps = section_body[steps_end_pos:]
                        
                        # Add steps wrapper
                        section_body = before_steps + '<div class="steps">\n' + steps_content + '\n</div>' + after_steps
                    
                    # Now handle English word list
                    if is_english:
                        # Find word list div
                        wl_start = section_body.find('<div style="background:#f0f0f5')
                        if wl_start != -1:
                            # Find word list close
                            d = 1
                            j = section_body.find('>', wl_start) + 1
                            while j < len(section_body):
                                if section_body[j:j+4] == '<div':
                                    d += 1
                                    j += 4
                                elif section_body[j:j+6] == '</div>':
                                    d -= 1
                                    if d == 0:
                                        wl_end = j + 6
                                        break
                                    j += 6
                                else:
                                    j += 1
                            else:
                                wl_end = -1
                            
                            if wl_end != -1:
                                wl_content = section_body[wl_start:wl_end]
                                # Remove word list from its position
                                section_body = section_body[:wl_start] + section_body[wl_end:]
                                
                                # Find the 讲 step (first step) and its closing div
                                steps_div = section_body.find('<div class="steps">')
                                if steps_div != -1:
                                    # Find first step inside steps
                                    first_step_open = section_body.find('<div class="step', steps_div)
                                    if first_step_open != -1:
                                        # Find first step close
                                        d = 0
                                        gt = section_body.find('>', first_step_open)
                                        if gt != -1:
                                            d = 1
                                            j = gt + 1
                                            while j < len(section_body):
                                                if section_body[j:j+4] == '<div':
                                                    d += 1
                                                    j += 4
                                                elif section_body[j:j+6] == '</div>':
                                                    d -= 1
                                                    if d == 0:
                                                        step_close = j
                                                        # Insert word list before step close
                                                        section_body = (section_body[:step_close] + 
                                                                      wl_content + 
                                                                      section_body[step_close:])
                                                        # Change class="step" to class="step full"
                                                        section_body = section_body.replace(
                                                            '<div class="step">',
                                                            '<div class="step full">',
                                                            1  # only first occurrence in this body
                                                        )
                                                        break
                                                    j += 6
                                                else:
                                                    j += 1
            
            sections.append(h3_tag + section_body)
        
        # Reassemble day
        fixed_day = before_first_h3 + ''.join(sections)
        new_parts.append(fixed_day)
        prev_end = day_end
    
    new_parts.append(h[prev_end:])
    h = ''.join(new_parts)
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(h)
    
    # Verify
    steps_count = h.count('<div class="steps">')
    step_full_count = h.count('class="step full"')
    print(f'w{wnum}: steps={steps_count}, step_full={step_full_count}')

print('Done!')
