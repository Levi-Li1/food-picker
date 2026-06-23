"""One-shot post-process for w2-w9. Handles all English section variants."""
import re

def find_matching_close(text, start_pos):
    depth = 1
    i = text.find('>', start_pos) + 1
    while i < len(text):
        if text[i:i+4] == '<div': depth += 1; i += 4
        elif text[i:i+6] == '</div>':
            depth -= 1
            if depth == 0: return i
            i += 6
        else: i += 1
    return -1

def find_step_cards(text):
    results = []
    for sm in re.finditer(r'<div class="step[\s">]', text):
        so = sm.start()
        sc = find_matching_close(text, so)
        if sc != -1:
            results.append((so, sc + 6, sm.group()))
    return results

def extract_word_list(text):
    """Find and extract the 今日30词 word list from text.
    Handles both new format (background:#f0f0f5 wrapper) and old format (raw <p>今日30词).
    Returns (word_list_html, remaining_text) or (None, text)."""
    # Try new format first
    wl_start = text.find('<div style="background:#f0f0f5')
    if wl_start != -1:
        wl_end = find_matching_close(text, wl_start)
        if wl_end != -1:
            wl_html = text[wl_start:wl_end + 6]
            remaining = text[:wl_start] + text[wl_end + 6:]
            return wl_html, remaining
    
    # Try old format: <p>今日30词</p> followed by 30 word-entry div pairs
    old_hdr = text.find('<p style="margin:10px 0"><b>今日30词</b>')
    if old_hdr == -1:
        return None, text
    
    # Find the word entries that follow. Old format:
    # <p>今日30词</p>
    # <div style="display:flex...">word</div><div style="font-size:11px...">ex</div>
    # ... (30 pairs)
    # After the 30th pair, there's usually </div></div> (structural closes) or end of section
    
    # Find position after the header <p> tag
    p_end = text.find('</p>', old_hdr)
    if p_end == -1: return None, text
    p_end += 4
    
    # Count word entry pairs. Each pair = <div display:flex>...</div> + <div font-size:11px>...</div>
    # Count them by finding all <div style="font-size:11px" and their matching closes
    pos = p_end
    entries = []
    while True:
        entry_start = text.find('<div style="display:flex', pos)
        if entry_start == -1: break
        
        # Find this entry's close
        entry_close = find_matching_close(text, entry_start)
        if entry_close == -1: break
        
        # Find the example div
        example_start = text.find('<div style="font-size:11px', entry_close)
        if example_start == -1: break
        
        example_close = find_matching_close(text, example_start)
        if example_close == -1: break
        
        entries.append((entry_start, example_close + 6))
        pos = example_close + 6
        
        if len(entries) >= 30:
            break
    
    if not entries:
        return None, text
    
    # The word list spans from old_hdr to entries[-1][1]
    wl_end = entries[-1][1]
    
    # Extract and wrap in background container
    wl_content = text[old_hdr:wl_end]
    wl_html = '<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">\n' + wl_content + '\n</div>'
    remaining = text[:old_hdr] + text[wl_end:]
    return wl_html, remaining

def process_normal_section(body):
    """Non-English: wrap all step cards in one steps container."""
    steps = find_step_cards(body)
    if not steps: return body
    fs, fe = steps[0][0], steps[-1][1]
    # Check if already wrapped (new days from gen_missing_days.py)
    prefix = body[:fs]
    if '<div class="steps"' in prefix:
        return body
    return body[:fs] + '<div class="steps">\n' + body[fs:fe] + '\n</div>' + body[fe:]

def process_english_section(body):
    """English: restructure to 讲(50%)+练(50%) in one steps, word list as step full(100%) in another."""
    # Step 1: Extract word list from wherever it is
    wl_html, body = extract_word_list(body)
    
    # Step 2: Extract all step cards as independent HTML blocks
    step_cards = []
    for sm in re.finditer(r'<div class="step[\s">]', body):
        so = sm.start()
        sc = find_matching_close(body, so)
        if sc != -1:
            full_html = body[so:sc + 6]
            # Keep step full as-is (固/结 should be 100% width)
            step_cards.append(full_html)
    
    # Step 3: Find what's before the first step and after the last step
    steps = find_step_cards(body)
    if steps:
        before = body[:steps[0][0]]
        after = body[steps[-1][1]:]
    else:
        before = body
        after = ''
    
    # Step 4: Build result
    # Check if body already has steps wrapper (from gen_missing_days.py)
    already_wrapped = '<div class="steps"' in before
    
    result = before
    if step_cards:
        if already_wrapped:
            result += '\n'.join(step_cards)
        else:
            result += '<div class="steps">\n' + '\n'.join(step_cards) + '\n</div>'
    result += after
    
    # Step 5: Add word list as separate step full (if present)
    if wl_html:
        result += '\n<div class="steps">\n<div class="step full">\n' + wl_html + '\n</div>\n</div>'
    else:
        # Fallback: if wl_html was not extracted but result still contains f0f0f5 word list,
        # extract it forcibly from the result
        wl2_start = result.find('<div style=\"background:#f0f0f5')
        if wl2_start != -1:
            # Find matching close
            depth = 0; wl2_i = wl2_start
            while wl2_i < len(result):
                if result[wl2_i:wl2_i+4] == '<div': depth += 1; wl2_i += 4
                elif result[wl2_i:wl2_i+6] == '</div>':
                    depth -= 1
                    if depth == 0: wl2_end = wl2_i + 6; break
                    wl2_i += 6
                else: wl2_i += 1
            else:
                wl2_end = len(result)
            wl2_html = result[wl2_start:wl2_end]
            result = result[:wl2_start] + result[wl2_end:]
            result += '\n<div class="steps">\n<div class="step full">\n' + wl2_html + '\n</div>\n</div>'
    
    # Clean up: remove extra </div> that might close dbody prematurely before word list
    result = result.replace('</div>\n</div>\n\n\n<div class="steps">\n<div class="step full">', 
                            '</div>\n\n<div class="steps">\n<div class="step full">')
    
    return result

def process_day(day):
    dbody_pos = day.find('<div class="dbody">')
    if dbody_pos == -1: return day
    
    prefix = day[:dbody_pos]
    dbody = day[dbody_pos:]
    
    h3s = list(re.finditer(r'<h3[^>]*>([^<]*)</h3>', dbody))
    if not h3s: return day
    
    new_dbody = dbody[:h3s[0].start()]
    
    for i, hm in enumerate(h3s):
        h3_tag = hm.group(0)
        h3_text = hm.group(1)
        h3_end = hm.end()
        
        if i + 1 < len(h3s):
            sec_end = h3s[i + 1].start()
        else:
            check = dbody.find('<div class="check">', h3_end)
            sec_end = check if check != -1 else len(dbody)
        
        body = dbody[h3_end:sec_end]
        
        if '英语' in h3_text:
            body = process_english_section(body)
        else:
            body = process_normal_section(body)
        
        new_dbody += h3_tag + body
    
    if h3s:
        last = h3s[-1].end()
        check = dbody.find('<div class="check">', last)
        if check != -1:
            new_dbody += dbody[check:]
    
    return prefix + new_dbody

# ── Main ──
for wnum in range(2, 10):
    fname = f'C:/Users/Tebon/BangMaker/Claw/w{wnum}.html'
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            h = f.read()
    except FileNotFoundError:
        continue

    h = h.replace('</div><div class="step"', '</div>\n<div class="step"')
    h = h.replace('</div><div class="step full"', '</div>\n<div class="step full"')
    h = h.replace('<div class="dbody"><h3', '<div class="dbody">\n<h3')

    day_starts = [m.start() for m in re.finditer(r'<div class="day-page"', h)]
    parts = []; le = 0
    for i, ds in enumerate(day_starts):
        de = day_starts[i+1] if i+1 < len(day_starts) else len(h)
        parts.append(h[le:ds])
        parts.append(process_day(h[ds:de]))
        le = de
    parts.append(h[le:])
    h = ''.join(parts)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(h)
    
    sc = h.count('<div class="steps">')
    print(f'w{wnum}: steps={sc}')

print('Done!')
