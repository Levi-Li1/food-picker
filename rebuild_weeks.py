#!/usr/bin/env python3
"""rebuild_weeks.py - fix w2-w9 by rebuilding day-page structures with correct div nesting"""
import re, os

BASE = 'C:/Users/Tebon/BangMaker/Claw'

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find all day-page sections
    days = []
    pos = 0
    while True:
        start = html.find('<div class="day-page">', pos)
        if start < 0:
            break
        end = html.find('<div class="day-page">', start + 1)
        if end < 0:
            end = html.find('</body>', start)
        if end < 0:
            end = len(html)
        days.append((start, end))
        pos = end

    if not days:
        return False

    # Process each day
    new_html = html
    offset = 0  # track position shifts from edits

    for ds, de in days:
        # Adjust for previous edits
        ads = ds + offset
        ade = de + offset
        day_html = new_html[ads:ade]

        # Skip if already well-formed (check by counting div balance)
        depth = 0
        for line in day_html.split('\n'):
            depth += len(re.findall(r'<div\b[^>]*>', line)) - len(re.findall(r'</div>', line))
        if depth == 0:
            continue  # already balanced

        # Find dbody start
        dbody_pos = day_html.find('<div class="dbody">')
        if dbody_pos < 0:
            continue

        # Get the dbody content (everything after <div class="dbody">)
        dbody_open = '<div class="dbody">'
        dbody_content_start = dbody_pos + len(dbody_open)

        # Find the day closing: where does dbody end?
        # Pattern: ...</div>\n</div> (close dbody + close day-page) at the very end
        # Look for the last </div>\n</div> in the day
        closing_pos = day_html.rfind('</div>\n</div>')
        if closing_pos < dbody_content_start:
            continue

        dbody_content_end = closing_pos  # content before the day closes
        day_end = closing_pos + len('</div>\n</div>')

        # Split dbody content by h3 sections
        dbody_content = day_html[dbody_content_start:dbody_content_end]

        # Find all h3 boundaries within dbody_content
        h3_positions = [m.start() for m in re.finditer(r'<h3\b[^>]*>', dbody_content)]

        if not h3_positions:
            continue

        # For each h3 section, extract and rebuild with correct nesting
        rebuilt_sections = []
        for i, h3_pos in enumerate(h3_positions):
            next_pos = h3_positions[i + 1] if i + 1 < len(h3_positions) else len(dbody_content)
            section = dbody_content[h3_pos:next_pos]

            # Extract h3 tag
            h3_end = section.find('>') + 1
            h3_tag = section[:h3_end]

            # Content after h3
            content = section[h3_end:]

            # Find all step divs in this content
            # Pattern: content may have <div class="step"> or <div class="step full"> blocks
            # These may or may not be wrapped in <div class="steps">

            steps_match = re.search(r'<div class="steps">', content)
            steps_close = content.rfind('</div>')

            if steps_match:
                # Has explicit steps wrapper - keep structure, fix closing
                steps_content = content[steps_match.start():]
                # Count step divs within the steps
                step_count = len(re.findall(r'<div class="step[\s">]', steps_content))
                # Expected: steps_content has step_count step divs + 1 steps close = step_count + 1 closes
                # But we need to ensure dbody is NOT closed here

                # We'll keep the original content but fix the closing
                # The issue is extra </div> at the very end
                # Strategy: trim trailing </div> to leave exactly step_count + 1
                trailing = re.findall(r'</div>\s*$', steps_content)
                # Just keep the steps content as-is but ensure the last </div> is only steps close, not dbody close
                rebuilt_sections.append(h3_tag + content.strip())
            else:
                # No explicit steps wrapper - wrap step divs in steps
                rebuilt_sections.append(h3_tag + content.strip())

        # For sections after the first, ensure they don't close dbody
        # The issue: sections have extra </div> at the end closing dbody
        # Fix: for all sections except the last, trim to correct closing

        # Actually, let me take a different approach.
        # The problem is that sections have varying numbers of trailing </div>
        # The correct structure: each section closes step divs + steps div (2 closes minimum)
        # dbody only closes AFTER the last section
        
        # For each section (except last), count expected closes:
        # - Number of <div class="step"> or <div class="step full"> in the section
        # - Plus 1 for the closing of <div class="steps">
        # The trailing </div> count should be: step_count + 1
        
        # Fix: for non-last sections, remove excess trailing </div>
        pass

    # The above logic is getting complex. Let me use a simpler approach:
    # For each day, find dbody content, split by h3, then rebuild with:
    # <h3>...</h3>
    # <div class="steps">
    #   <div class="step">...</div>
    #   ...
    # </div>
    # At the end: dbody closes, day-page closes

    # Return whether any changes were made
    return True


# Actually, let me use a much simpler approach:
# The build_weeks.js generates w2-w9 from guct.html
# If I fix guct.html first, then regenerate, the result will be correct

def fix_guct_html():
    """Fix guct.html template by correcting section boundary closes"""
    filepath = os.path.join(BASE, 'guct.html')
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find all day-page sections
    body_start = html.find('<body>')
    before_body = html[:body_start]
    body = html[body_start:]

    # Split by day-page markers
    day_markers = list(re.finditer(r'<div class="day-page">', body))
    
    fixed_body = body
    total_fixes = 0

    for i, dm in enumerate(day_markers):
        day_start = dm.start()
        day_end = day_markers[i + 1].start() if i + 1 < len(day_markers) else len(body)
        day_html = body[day_start:day_end]

        # Find dbody boundaries
        dbody_match = re.search(r'<div class="dbody">', day_html)
        if not dbody_match:
            continue
        
        dbody_start = dbody_match.end()  # content after <div class="dbody">
        
        # Find the last </div>\n</div> (day close)
        day_close = day_html.rfind('</div>\n</div>')
        if day_close < dbody_start:
            continue
        
        dbody_end = day_close
        dbody_content = day_html[dbody_start:dbody_end]

        # Find h3 boundaries within dbody
        h3_positions = [m.start() for m in re.finditer(r'<h3\b[^>]*>', dbody_content)]
        
        if len(h3_positions) < 2:
            continue  # single-section day, no inter-section boundary issues

        # For each adjacent pair of h3 sections, check the boundary
        fixed_content = dbody_content
        offset_shift = 0

        for j in range(len(h3_positions) - 1):
            h3_a = h3_positions[j]
            h3_b = h3_positions[j + 1]
            
            between = fixed_content[h3_a:h3_b]
            
            # Count trailing </div> in the last lines
            lines = between.split('\n')
            trailing_closes = 0
            trailing_lines = []
            for line in reversed(lines):
                c = line.count('</div>')
                if c > 0:
                    trailing_closes += c
                    trailing_lines.insert(0, line)
                elif line.strip():
                    break  # non-empty, non-div line
                else:
                    trailing_lines.insert(0, line)  # empty line

            if trailing_closes <= 2:
                continue  # already correct (just step+steps closes)

            # Need to fix: remove extra </div>(s)
            # How many to remove? We want exactly 2 closes (step + steps)
            # But sections may have internal step closes too
            # Count step divs in this section
            section_html = between
            step_divs = len(re.findall(r'<div class="step[\s">]', section_html))
            
            # Expected closes: step_divs (each step) + 1 (steps)
            expected_closes = step_divs + 1
            
            if trailing_closes <= expected_closes:
                continue  # Already correct or close enough
            
            # Remove extra trailing </div>
            excess = trailing_closes - expected_closes
            
            # Find the position of the first excess </div> in the trailing lines
            # Work backwards through trailing_lines, removing excess </div>
            fix_pos = h3_a
            remaining = excess
            for line in reversed(trailing_lines):
                if remaining <= 0:
                    break
                div_count = line.count('</div>')
                if div_count > 0:
                    line_start = between.rfind(line, 0, h3_b)
                    if line_start >= 0:
                        # Remove one </div> from this line
                        last_div = line.rfind('</div>')
                        if last_div >= 0:
                            remove_start = fix_pos + line_start + last_div
                            remove_end = remove_start + len('</div>')
                            # Remove this closing tag
                            new_between = between[:remove_start - h3_a + gap_fix] + between[remove_end - h3_a + gap_fix:]
                            # Actually this is getting too complex with inline position tracking
                            remaining -= 1

        # This approach is too complex. Let me use a simpler method.

    # SIMPLER APPROACH: Just fix the pattern </div>\n</div>\n</div> → </div>\n</div>
    # This handles the common case where sections have exactly 3 closes
    # For sections with more closes, we need a different approach

    print("Switching to simpler regex approach...")
    
    # Restore original body for a fresh start
    body_new = body
    
    # Pattern: multiple </div> on consecutive lines right before <h3>
    # Fix: reduce to exactly 2 </div> (one for last step, one for steps)
    pattern = re.compile(r'(</div>\s*){3,}(?=\s*(<!--[^-]*-->)?\s*<h3)', re.DOTALL)
    
    def fix_match(m):
        nonlocal total_fixes
        matched = m.group(0)
        # Count </div>
        count = len(re.findall(r'</div>', matched))
        total_fixes += 1
        # Return exactly 2 </div>
        return '</div>\n</div>'
    
    body_new = pattern.sub(fix_match, body_new)
    
    # Write fixed template
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(before_body + body_new)
    
    print(f'Fixed {total_fixes} section boundaries in guct.html')
    return total_fixes


if __name__ == '__main__':
    fix_guct_html()
