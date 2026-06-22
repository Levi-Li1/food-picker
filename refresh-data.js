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

// Replace in HTML using unique marker approach
let html = fs.readFileSync('football.html', 'utf8');
const oldSize = html.length;

// Insert a marker before each embedded data block (one-time setup)
if (!html.includes('/*EMBED')) {
  html = html.replace('const E_G=[', '/*E_G*/const E_G=[');
  html = html.replace('const E_P=[', '/*E_P*/const E_P=[');
}

// Replace between markers and next variable declaration
function replaceBetween(html, startMarker, nextMarker, newData, varPrefix) {
  const start = html.indexOf(startMarker);
  if (start < 0) return html;
  const searchFrom = start + startMarker.length;
  const end = html.indexOf(nextMarker, searchFrom);
  if (end < 0) return html;
  return html.slice(0, start + startMarker.length)
    + varPrefix + JSON.stringify(newData) + ';'
    + html.slice(end);
}

html = replaceBetween(html, '/*E_G*/', 'const E_P=', gs, 'const E_G=');
if (gr) {
  html = replaceBetween(html, '/*E_P*/', 'const STADIUMS', gr, 'const E_P=');
}

// Update timestamp
const ts = new Date().toISOString().replace(/[-:]/g, '').slice(0, 15).replace('T', '-');
html = html.replace(/>\d{8}-\d{4} \(git [a-f0-9]{7}\)</, `>${ts} (git auto)</`);

// Validate JS
const js = html.substring(html.indexOf('<script>') + 8, html.lastIndexOf('</script>'));
require('child_process').execSync('node --check -', { input: js, stdio: 'pipe' });

fs.writeFileSync('football.html', html);
console.log('Data updated and validated.');
