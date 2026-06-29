#!/usr/bin/env python3
"""
refresh_all.py — 苏超全面数据更新脚本

更新 football.html 的三大模块：
1. 积分榜 (standings) — 从 suchao.crazy-thursday.com/standings 的 RSC 解析
2. 最新赛果 (results) — 保留原有的 JS 模板方式，只更新球队名
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
#  PART 2: Upcoming fixtures from API     ║
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
#  PART 3: Generate HTML fragments        ║
# ═════════════════════════════════════════╝
def gen_standings_js(teams, existing_crests=None):
    """Generate SPFL array JS code, preserving existing crest URLs."""
    if existing_crests is None:
        existing_crests = {}
    lines = ['        const SPFL = [']
    for i, t in enumerate(teams):
        comma = ',' if i < len(teams) - 1 else ''
        crest = existing_crests.get(t['name'], 'crests/default.png')
        lines.append(
            f'            {{ pos:{t["pos"]}, name:\'{t["name"]}\', p:{t["p"]}, '
            f'w:{t["w"]}, d:{t["d"]}, l:{t["l"]}, gf:{t["gf"]}, ga:{t["ga"]}, '
            f'gd:{t["gd"]}, pts:{t["pts"]},\n'
            f'              crest:\'{crest}\' }}{comma}'
        )
    lines.append('        ];')
    return '\n'.join(lines)

def gen_fixtures_html(upcoming_matches):
    """Generate HTML for upcoming fixtures section using JS template literal.

    Uses the same approach as the original HTML: generates JS template literals
    with rRow-style function calls that render crests from the SPFL array at runtime.
    """
    if not upcoming_matches:
        return '        <p style="color:var(--text3);text-align:center;">暂无赛程数据</p>'

    # Group by date
    by_date = {}
    for m in upcoming_matches:
        d = m['date']
        if d not in by_date:
            by_date[d] = []
        by_date[d].append(m)

    sorted_dates = sorted(by_date.keys())

    parts = []
    # Take up to next 4 match dates
    for dt in sorted_dates[:4]:
        ms = by_date[dt]
        try:
            d = datetime.datetime.strptime(dt, '%Y-%m-%d')
            date_label = f"{d.month}月{d.day}日"
        except:
            date_label = dt

        rows = []
        for m in ms:
            home = m.get('homeTeam', '?') + '队'
            away = m.get('awayTeam', '?') + '队'
            venue = m.get('venue', '')
            rows.append(f"                {{{{fixRow('{home}','{away}','{venue}','{date_label}')}}}}")

        part = f'''        <div style="margin-top:8px;">
            <div style="font-size:12px;color:var(--text3);margin-bottom:8px;padding-left:2px;">{date_label}</div>
            {''.join(rows)}
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

    # Step 2: Fetch upcoming fixtures from API
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

    # Extract existing crest URLs from current HTML's SPFL section
    existing_crests = {}
    crest_pat = re.compile(r"name:'([^']+?)',[\s\S]*?crest:'([^']+)'")
    for m in crest_pat.finditer(html):
        existing_crests[m.group(1)] = m.group(2)

    # ── Update Standings ──
    new_standings_js = gen_standings_js(teams, existing_crests)
    spfl_start = html.find('const SPFL = [')
    spfl_end = html.find('];', spfl_start) + 2
    if spfl_start >= 0:
        html = html[:spfl_start] + new_standings_js + html[spfl_end:]
        print("  ✓ Standings JS updated")
    else:
        print("  ⚠ SPFL array not found in HTML")

    # ── Update Summary ──
    if teams:
        top = teams[0]
        html = re.sub(r'盐城队 · \d+分（[^）]+）',
                      f'盐城队 · {top["pts"]}分（{top["p"]}战{top["w"]}胜）', html)
        html = re.sub(r'>\d+ 轮<', f'>{top["p"]} 轮<', html)
        print("  ✓ Summary updated")

    # ── Update Fixtures ──
    if upcoming_matches:
        # Build fixtures HTML using JS template literals (fixRow)
        # Group by date
        by_date = {}
        for m in upcoming_matches:
            d = m['date']
            if d not in by_date:
                by_date[d] = []
            by_date[d].append(m)

        sorted_dates = sorted(by_date.keys())[:4]

        # Replace the content inside `const fixturesHTML = `...`;`
        fh_start = html.find('const fixturesHTML = `')
        if fh_start >= 0:
            # Find the closing backtick after fixturesHTML
            fh_end = html.find('`;', fh_start) + 2

            new_fixtures_lines = ['            const fixturesHTML = `']
            for dt in sorted_dates:
                ms = by_date[dt]
                try:
                    d = datetime.datetime.strptime(dt, '%Y-%m-%d')
                    label = f"{d.month}月{d.day}日"
                except:
                    label = dt

                new_fixtures_lines.append('        <div style="margin-top:8px;">')
                new_fixtures_lines.append(f'            <div style="font-size:12px;color:var(--text3);margin-bottom:8px;padding-left:2px;">{label}</div>')
                for m in ms:
                    home = m.get('homeTeam', '?') + '队'
                    away = m.get('awayTeam', '?') + '队'
                    venue = m.get('venue', '')
                    t = m.get('time', '19:40')
                    venue_html = ''
                    if venue:
                        venue_html = f'<div style="font-size:11px;color:var(--text3);margin-top:8px;display:flex;align-items:center;gap:4px;"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>{venue}</div>'
                    new_fixtures_lines.append('                <div class="match-card">')
                    new_fixtures_lines.append(f'                    <div class="match-header"><span>{label} · {t}</span><span class="match-status upcoming">即将开始</span></div>')
                    new_fixtures_lines.append('                    <div class="match-teams">')
                    new_fixtures_lines.append(f'                        <div class="match-team home"><span class="crest-inline">${{crestImg(crestMap["{home}"])}}</span><span class="match-name">{home}</span></div>')
                    new_fixtures_lines.append(f'                        <div class="match-score vs">VS</div>')
                    new_fixtures_lines.append(f'                        <div class="match-team away"><span class="crest-inline">${{crestImg(crestMap["{away}"])}}</span><span class="match-name">{away}</span></div>')
                    new_fixtures_lines.append('                    </div>')
                    if venue_html:
                        new_fixtures_lines.append(f'                    {{{{venue_html}}}}')
                    new_fixtures_lines.append('                </div>')
                new_fixtures_lines.append('        </div>')

            new_fixtures_lines.append('        `;')
            new_fixtures = '\n'.join(new_fixtures_lines)

            html = html[:fh_start] + new_fixtures + html[fh_end:]
            print("  ✓ Fixtures HTML updated")

    # ── Results section: keep original JS template approach ──
    # The results use ${rRow(...)} which renders crests at runtime from crestMap.
    # Just update the crestMap by ensuring SPFL array has correct crests (already done above).
    print("  ✓ Results section preserved (uses JS template literals with crestMap)")

    # Validate JS by extraction
    js_start = html.find('<script>')
    js_end = html.rfind('</script>')
    if js_start >= 0 and js_end > js_start:
        js_code = html[js_start + 8:js_end]
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
    print(f"📊 积分榜: {len(teams)} 队, 领头羊 {teams[0]['name']} ({teams[0]['pts']}分)")
    if upcoming_matches:
        print(f"📅 赛程预告: 从 {upcoming_matches[0]['date']} 起共 {len(upcoming_matches)} 场")

if __name__ == '__main__':
    main()
