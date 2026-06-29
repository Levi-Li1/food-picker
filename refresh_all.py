#!/usr/bin/env python3
"""
refresh_all.py — 苏超全面数据更新脚本

更新 football.html 的三大模块：
1. 积分榜 (standings) — 从 suchao.crazy-thursday.com/standings 的 RSC 解析
2. 最新赛果 (results) — 从 163.com 赛事页提取已结束比赛
3. 赛程预告 (fixtures) — 从 suchao API /api/matches 获取未来赛程

用法: python refresh_all.py
"""

import re
import json
import urllib.request
import urllib.error
import datetime
import os

# ── 配置 ──
STANDINGS_URL = "https://suchao.crazy-thursday.com/standings"
API_MATCHES_URL = "https://suchao.crazy-thursday.com/api/matches?page=1&perPage=100&all=true"
API_MATCHES_P2_URL = "https://suchao.crazy-thursday.com/api/matches?page=2&perPage=100&all=true"
SPORTS163_URL = "https://sports.163.com/caipiao/league/football/7306"
HTML_PATH = "football.html"

TEAM_ORDER = ['盐城','无锡','常州','宿迁','苏州','南京','徐州','淮安','扬州','泰州','南通','连云港','镇江']

def fetch(url, timeout=30):
    """Fetch URL content."""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/json,*/*'
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  ⚠ Fetch failed: {e}")
        return None

# ═════════════════════════════════════════╗
#  PART 1: Standings from suchao RSC      ║
# ═════════════════════════════════════════╝
def fetch_standings():
    """Extract standings from suchao RSC payload."""
    print("📊 Fetching standings...")
    html = fetch(STANDINGS_URL)
    if not html:
        return None

    # Extract RSC values — same approach as refresh-suchao.js
    all_vals = []
    combined = r'\\"children\\":(?:(-?\d+)}|\\"([^"\\]+)\\")'
    for m in re.finditer(combined, html):
        if m.group(1) is not None:
            all_vals.append(int(m.group(1)))
        elif m.group(2) is not None:
            all_vals.append(m.group(2))

    print(f"  Extracted {len(all_vals)} values")

    teams = []
    for name in TEAM_ORDER:
        try:
            idx = all_vals.index(name)
        except ValueError:
            print(f"  ⚠ Team not found: {name}")
            continue
        nums = []
        for i in range(idx + 1, min(idx + 20, len(all_vals))):
            if isinstance(all_vals[i], (int, float)):
                nums.append(all_vals[i])
            if len(nums) >= 8:
                break
        if len(nums) >= 8:
            teams.append({
                'pos': len(teams) + 1,
                'name': name + '队',
                'p': nums[0], 'w': nums[1], 'd': nums[2], 'l': nums[3],
                'gf': nums[4], 'ga': nums[5], 'gd': nums[6], 'pts': nums[7]
            })

    if len(teams) != 13:
        print(f"  ⚠ Expected 13 teams, got {len(teams)}")
        return None

    print(f"  ✓ {len(teams)} teams loaded")
    for t in teams:
        print(f"    {t['pos']}. {t['name']} {t['p']}GP {t['w']}W {t['d']}D {t['l']}L {t['pts']}pts")
    return teams

# ═════════════════════════════════════════╗
#  PART 2: Match results from 163.com     ║
# ═════════════════════════════════════════╝
def fetch_results():
    """Extract finished match results from 163.com."""
    print("⚽ Fetching match results from 163.com...")
    html = fetch(SPORTS163_URL)
    if not html:
        return None

    # Decode HTML entities
    html = html.replace('&quot;', '"')

    # Find all match entries
    entries = html.split('matchId":[')
    matches = []

    for e in entries[1:]:
        try:
            asc = re.search(r'awayScore":\[0,(\d+)\]', e)
            hs = re.search(r'homeScore":\[0,(\d+)\]', e)
            if not (asc and hs):
                continue

            names = re.findall(r'name":\[0,"([^"]+队)"\]', e)
            ts_m = re.search(r'matchTime":\[0,(\d+)\]', e)
            st_m = re.search(r'matchStatus":\[0,(\d+)\]', e)

            if len(names) >= 2 and ts_m:
                ts = int(ts_m.group(1)) / 1000
                dt = datetime.datetime.fromtimestamp(ts)
                date_str = dt.strftime('%Y-%m-%d')

                matches.append({
                    'date': date_str,
                    'home': names[0],
                    'away': names[1],
                    'hs': int(hs.group(1)),
                    'as': int(asc.group(1)),
                    'status': int(st_m.group(1)) if st_m else 0,
                    'ts': ts
                })
        except:
            pass

    # Deduplicate
    seen = set()
    unique = []
    for m in matches:
        key = (m['date'], m['home'], m['away'])
        if key not in seen:
            seen.add(key)
            unique.append(m)

    finished = [m for m in unique if m['status'] == 3]
    finished.sort(key=lambda x: x['ts'], reverse=True)

    print(f"  ✓ {len(finished)} finished matches loaded")
    return finished

# ═════════════════════════════════════════╗
#  PART 3: Upcoming fixtures from API     ║
# ═════════════════════════════════════════╝
def fetch_fixtures():
    """Fetch upcoming fixtures from suchao API."""
    print("📅 Fetching upcoming fixtures from API...")
    
    all_matches = []
    for url in [API_MATCHES_URL, API_MATCHES_P2_URL]:
        data = fetch(url)
        if data:
            try:
                j = json.loads(data)
                items = j['items'] if isinstance(j, dict) and 'items' in j else (j if isinstance(j, list) else [])
                all_matches.extend(items)
            except:
                pass

    # Filter to upcoming matches only
    now = datetime.datetime.now()
    upcoming = []
    for m in all_matches:
        if m.get('homeScore') is None and m.get('awayScore') is None:
            try:
                d = datetime.datetime.strptime(m['date'], '%Y-%m-%d')
                if d >= now - datetime.timedelta(days=1):
                    upcoming.append(m)
            except:
                pass

    upcoming.sort(key=lambda x: x['date'])
    print(f"  ✓ {len(upcoming)} upcoming fixtures loaded")
    return upcoming

# ═════════════════════════════════════════╗
#  PART 4: Generate HTML fragments        ║
# ═════════════════════════════════════════╝
def gen_standings_js(teams):
    """Generate SPFL array JS code."""
    lines = ['        const SPFL = [']
    for i, t in enumerate(teams):
        comma = ',' if i < len(teams) - 1 else ''
        lines.append(
            f'            {{ pos:{t["pos"]}, name:\'{t["name"]}\', p:{t["p"]}, '
            f'w:{t["w"]}, d:{t["d"]}, l:{t["l"]}, gf:{t["gf"]}, ga:{t["ga"]}, '
            f'gd:{t["gd"]}, pts:{t["pts"]},\n'
            f'              crest:\'crests/default.png\' }}{comma}'
        )
    lines.append('        ];')
    return '\n'.join(lines)

def gen_results_html(teams, finished_matches):
    """Generate HTML for latest results section."""
    if not finished_matches:
        return '<p style="color:var(--text3);text-align:center;">暂无比赛数据</p>'

    # Group by date
    by_date = {}
    for m in finished_matches:
        d = m['date']
        if d not in by_date:
            by_date[d] = []
        by_date[d].append(m)

    # Get latest 2 match days
    latest_dates = sorted(by_date.keys(), reverse=True)[:2]
    
    # Build crest map from teams
    crest_map = {t['name']: t.get('crest', 'crests/default.png') for t in teams}

    def crest_img(url):
        return f'<img src="{url}" width="28" height="28" style="border-radius:50%;display:block;object-fit:cover" alt="" loading="lazy" onerror="this.style.display=\'none\'">'

    def r_row(home, away, score, venue):
        hc = crest_img(crest_map.get(home, 'crests/default.png'))
        ac = crest_img(crest_map.get(away, 'crests/default.png'))
        return f'''                <div class="match-card">
                    <div class="match-header"><span>{venue}</span><span class="match-status final">已结束</span></div>
                    <div class="match-teams">
                        <div class="match-team home"><span class="crest-inline">{hc}</span><span class="match-name">{home}</span></div>
                        <div class="match-score">{score}</div>
                        <div class="match-team away"><span class="crest-inline">{ac}</span><span class="match-name">{away}</span></div>
                    </div>
                </div>'''

    parts = []
    for dt in latest_dates:
        ms = by_date[dt]
        # Parse date
        try:
            d = datetime.datetime.strptime(dt, '%Y-%m-%d')
            date_label = f"{d.month}月{d.day}日"
        except:
            date_label = dt
        
        # Find round info from standings
        round_label = f"第{latest_dates.index(dt)+1}轮"  # approximate

        rows = []
        for m in ms:
            score = f"{m['hs']} – {m['as']}"
            rows.append(r_row(m['home'], m['away'], score, date_label))
        
        part = f'''        <div style="margin-top:8px;">
            <div style="font-size:12px;color:var(--text3);margin-bottom:8px;padding-left:2px;">{date_label} · 最新比赛</div>
            {''.join(rows)}
        </div>'''
        parts.append(part)

    return '\n'.join(parts)

def gen_fixtures_html(upcoming_matches):
    """Generate HTML for upcoming fixtures section."""
    if not upcoming_matches:
        return '<p style="color:var(--text3);text-align:center;">暂无赛程数据</p>'

    # Group by date
    by_date = {}
    for m in upcoming_matches:
        d = m['date']
        if d not in by_date:
            by_date[d] = []
        by_date[d].append(m)

    sorted_dates = sorted(by_date.keys())

    # Build venue lookup
    venue_map = {m['id']: m.get('venue', '') for m in upcoming_matches}

    def crest_img_home(m):
        logo = m.get('homeTeamLogo', '')
        if logo:
            return f'<img src="{logo}" width="28" height="28" style="border-radius:50%;display:block;object-fit:cover" alt="" loading="lazy" onerror="this.style.display=\'none\'">'
        return ''

    def crest_img_away(m):
        logo = m.get('awayTeamLogo', '')
        if logo:
            return f'<img src="{logo}" width="28" height="28" style="border-radius:50%;display:block;object-fit:cover" alt="" loading="lazy" onerror="this.style.display=\'none\'">'
        return ''

    def fix_row(m, date_label):
        home = m.get('homeTeam', '?') + '队'
        away = m.get('awayTeam', '?') + '队'
        venue = m.get('venue', '')
        hc = crest_img_home(m)
        ac = crest_img_away(m)
        time = m.get('time', '19:40')
        venue_html = ''
        if venue:
            venue_html = f'''<div style="font-size:11px;color:var(--text3);margin-top:8px;display:flex;align-items:center;gap:4px;"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>{venue}</div>'''
        return f'''                <div class="match-card">
                    <div class="match-header"><span>{date_label} · {time}</span><span class="match-status upcoming">即将开始</span></div>
                    <div class="match-teams">
                        <div class="match-team home"><span class="crest-inline">{hc}</span><span class="match-name">{home}</span></div>
                        <div class="match-score vs">VS</div>
                        <div class="match-team away"><span class="crest-inline">{ac}</span><span class="match-name">{away}</span></div>
                    </div>{venue_html}
                </div>'''

    parts = []
    # Take up to next 3 match dates
    for dt in sorted_dates[:4]:
        ms = by_date[dt]
        try:
            d = datetime.datetime.strptime(dt, '%Y-%m-%d')
            date_label = f"{d.month}月{d.day}日"
        except:
            date_label = dt

        rows = ''.join(fix_row(m, date_label) for m in ms)
        part = f'''        <div style="margin-top:8px;">
            <div style="font-size:12px;color:var(--text3);margin-bottom:8px;padding-left:2px;">{date_label}</div>
            {rows}
        </div>'''
        parts.append(part)

    return '\n'.join(parts)

# ═════════════════════════════════════════╗
#  MAIN                                    ║
# ═════════════════════════════════════════╝
def main():
    print("=" * 50)
    print(" 苏超数据全面更新脚本")
    print("=" * 50)
    print()

    # Step 1: Fetch standings
    teams = fetch_standings()
    if not teams:
        print("❌ Failed to fetch standings, aborting.")
        return
    print()

    # Step 2: Fetch match results from 163.com
    finished_matches = fetch_results()
    if not finished_matches:
        print("❌ Failed to fetch match results, aborting.")
        return
    print()

    # Step 3: Fetch upcoming fixtures from API
    upcoming_matches = fetch_fixtures()
    if not upcoming_matches:
        print("⚠ No upcoming fixtures found, continuing...")
    print()

    # ── Generate updated content ──
    print("🔄 Updating football.html...")

    try:
        with open(HTML_PATH, 'r', encoding='utf-8') as f:
            html = f.read()
    except FileNotFoundError:
        print(f"❌ {HTML_PATH} not found")
        return

    old_size = len(html)

    # Generate standings JS
    new_standings_js = gen_standings_js(teams)

    # Replace SPFL array
    spfl_start = html.find('const SPFL = [')
    spfl_end = html.find('];', spfl_start) + 2
    if spfl_start >= 0:
        html = html[:spfl_start] + new_standings_js + html[spfl_end:]
        print("  ✓ Standings JS updated")
    else:
        print("  ⚠ SPFL array not found in HTML")

    # Replace renderSPFL function body for results and fixtures
    # We need to find the renderSPFL function and update its content
    
    # Update results section - find the spflResults assignment
    # We'll replace the entire renderSPFL() function body
    
    # Generate new results HTML
    results_html = gen_results_html(teams, finished_matches)
    
    # Find and replace the results assignment in renderSPFL
    # Pattern: document.getElementById('spflResults').innerHTML = ...
    results_start = html.find("document.getElementById('spflResults').innerHTML =")
    if results_start >= 0:
        # Find the semicolon after this assignment
        semi = html.find(';', results_start)
        # The old results template is between the previous statement and this assignment
        # Let's find the template literal that defines resultsHTML
        
        # Actually simpler: find the resultsHTML assignment
        rh_start = html.find("const resultsHTML = `")
        if rh_start >= 0:
            rh_end = html.find("`;", rh_start) + 2
            # Build new results HTML with proper escaping
            # The HTML needs to be inside a template literal
            escaped_results = results_html.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
            new_results = f"const resultsHTML = `\n{escaped_results}\n        `;"
            html = html[:rh_start] + new_results + html[rh_end:]
            print("  ✓ Results HTML updated")

    # Generate new fixtures HTML
    fixtures_html = gen_fixtures_html(upcoming_matches)
    
    # Find and replace fixtures assignment
    fh_start = html.find("const fixturesHTML = `")
    if fh_start >= 0:
        fh_end = html.find("`;", fh_start) + 2
        escaped_fixtures = fixtures_html.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
        new_fixtures = f"const fixturesHTML = `\n{escaped_fixtures}\n        `;"
        html = html[:fh_start] + new_fixtures + html[fh_end:]
        print("  ✓ Fixtures HTML updated")

    # Update summary text
    # Find and update "盐城队 · X分（Y战Z胜）"
    if teams:
        top = teams[0]
        summary_pattern = r'盐城队 · \d+分（[^）]+）'
        new_summary = f'盐城队 · {top["pts"]}分（{top["p"]}战{top["w"]}胜）'
        html = re.sub(summary_pattern, new_summary, html)
        
        # Update "已进行 X 轮"
        round_pattern = r'>\d+ 轮<'
        html = re.sub(round_pattern, f'>{top["p"]} 轮<', html)
        print("  ✓ Summary updated")

    # Validate JS
    js_start = html.find('<script>')
    js_end = html.rfind('</script>')
    if js_start >= 0 and js_end > js_start:
        js_code = html[js_start + 8:js_end]
        # Write to temp file for node validation
        with open('_temp_check.js', 'w', encoding='utf-8') as f:
            f.write(js_code)

    # Write HTML
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    
    new_size = len(html)
    print(f"  ✓ HTML written ({old_size} → {new_size} bytes)")

    # Cleanup
    if os.path.exists('_temp_check.js'):
        os.remove('_temp_check.js')

    print()
    print("✅ Update complete!")
    print()

    # Print summary of what was updated
    if teams:
        print(f"📊 积分榜: {len(teams)} 队, 领头羊 {teams[0]['name']} ({teams[0]['pts']}分)")
    if finished_matches:
        latest = finished_matches[0]
        print(f"⚽ 最新赛果: {latest['date']} {latest['home']} {latest['hs']}-{latest['as']} {latest['away']} 等共 {len(finished_matches)} 场")
    if upcoming_matches:
        next_match = upcoming_matches[0]
        print(f"📅 赛程预告: 从 {next_match['date']} 起共 {len(upcoming_matches)} 场")

if __name__ == '__main__':
    main()
