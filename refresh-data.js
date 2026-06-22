const { execSync } = require('child_process');
const fs = require('fs');

console.log('[', new Date().toISOString(), '] Fetching World Cup data...');

let games, groups;
try {
  games = JSON.parse(execSync('curl -sL --connect-timeout 10 --max-time 30 https://worldcup26.ir/get/games', {
    maxBuffer: 2 * 1024 * 1024
  }));
  console.log('Games API: OK,', (games.games || games).length, 'matches');
} catch (e) {
  console.error('Games API FAIL:', e.message);
  process.exit(0);
}

try {
  groups = JSON.parse(execSync('curl -sL --connect-timeout 10 --max-time 30 https://worldcup26.ir/get/groups', {
    maxBuffer: 1024 * 1024
  }));
  console.log('Groups API: OK,', (groups.groups || groups).length, 'groups');
} catch (e) {
  console.error('Groups API FAIL:', e.message);
  groups = null;
}

// Minimize to short field names
const gs = (games.games || games).map(m => ({
  i: m.id || m._id, g: m.group, h: m.home_team_id, a: m.away_team_id,
  hs: m.home_score, as: m.away_score, hs2: m.home_scorers, as2: m.away_scorers,
  ld: m.local_date, s: m.stadium_id, f: m.finished, te: m.time_elapsed
}));

const gr = groups
  ? (groups.groups || groups).map(g => ({
      n: g.name || g.group,
      t: (g.teams || g.standings || []).map(t => ({
        id: t.team_id || t.id, w: +t.wins || +t.won || +t.w || 0,
        d: +t.draws || +t.drawn || +t.d || 0, l: +t.losses || +t.lost || +t.l || 0,
        p: +t.played || +t.mp || +t.p || 0, gf: +t.gf || +t.goals_for || 0,
        ga: +t.ga || +t.goals_against || 0
      }))
    }))
  : null;

// Safe array boundary finder using depth tracking
function findArrayEnd(html, startMarker) {
  const start = html.indexOf(startMarker);
  if (start < 0) return null;
  // Skip the 'const XXX=[' prefix (marker length)
  let i = start + startMarker.length;
  let depth = 0, inStr = false, esc = false;
  while (i < html.length) {
    const c = html[i];
    if (esc) { esc = false; i++; continue; }
    if (c === '\\') { esc = true; i++; continue; }
    if (c === '"' && !esc) { inStr = !inStr; i++; continue; }
    if (inStr) { i++; continue; }
    if (c === '[' || c === '{') { depth++; }
    else if (c === ']' || c === '}') { depth--; if (depth === 0) { return i; } }
    i++;
  }
  return null;
}

let html = fs.readFileSync('football.html', 'utf8');
const oldSize = html.length;

// Replace E_G
const egEnd = findArrayEnd(html, 'const E_G=[');
if (egEnd) {
  html = html.slice(0, html.indexOf('const E_G=') + 10) + JSON.stringify(gs) + html.slice(egEnd + 1);
}

// Replace E_P
if (gr) {
  const epEnd = findArrayEnd(html, 'const E_P=[');
  if (epEnd) {
    html = html.slice(0, html.indexOf('const E_P=') + 10) + JSON.stringify(gr) + html.slice(epEnd + 1);
  }
}

// Update version timestamp
const ts = new Date().toISOString().replace(/[-:]/g, '').slice(0, 15).replace('T', '-');
html = html.replace(/>\d{8}-\d{4} \(git [a-f0-9]{7}\)</, `>${ts} (git auto)</`);

fs.writeFileSync('football.html', html);

if (html.length !== oldSize) {
  console.log('Data changed, will commit.');
} else {
  console.log('No changes.');
}
