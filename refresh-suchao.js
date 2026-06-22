const { execSync } = require('child_process');
const fs = require('fs');

console.log('[', new Date().toISOString(), '] Fetching Su Chao data...');

let html;
try {
  html = execSync('curl -sL --connect-timeout 15 --max-time 30 https://suchao.crazy-thursday.com/standings', {
    maxBuffer: 2 * 1024 * 1024, encoding: 'utf8'
  });
} catch (e) {
  console.error('Standings FAIL:', e.message);
  process.exit(0);
}

// The RSC payload uses escaped JSON: \"children\":\"value\"
// In regex, we need \\\" to match the literal \"
function extractVal(v) {
  // v could be a number like "12" or a string like "盐城"
  const num = parseInt(v, 10);
  return isNaN(num) ? v.replace(/^"|"$/g, '').replace(/\\"/g, '"') : num;
}

// Extract all "children" values
const vals = [];
const pat = /\\"children\\":\\"([^"\\]+)\\"/g;
let m;
while ((m = pat.exec(html)) !== null) {
  vals.push(extractVal(m[1]));
}
// Also match numeric children: \"children\":12}
const patNum = /\\"children\\":(-?\d+)}/g;
const allVals = [];
let lastMatch = 0;
// Combine both patterns by scanning position
const html2 = html;
// Simpler: use a single regex for both
const combined = /\\"children\\":(?:(-?\d+)}|\\"([^"\\]+)\\")/g;
while ((m = combined.exec(html2)) !== null) {
  if (m[1] !== undefined) allVals.push(+m[1]);
  else if (m[2] !== undefined) allVals.push(m[2]);
}

console.log('Extracted', allVals.length, 'values');
if (allVals.length < 50) {
  console.error('Not enough values extracted');
  process.exit(0);
}

// Find team names and their stats
const teamOrder = ['盐城','无锡','常州','宿迁','苏州','南京','徐州','淮安','扬州','泰州','南通','连云港','镇江'];
const teams = [];
for (const name of teamOrder) {
  const idx = allVals.indexOf(name);
  if (idx < 0) { console.error('Team not found:', name); continue; }
  // Collect next 8 numbers after team name
  const nums = [];
  for (let i = idx + 1; i < allVals.length && nums.length < 8; i++) {
    if (typeof allVals[i] === 'number') nums.push(allVals[i]);
  }
  if (nums.length >= 8) {
    teams.push({
      pos: teams.length + 1,
      name: name + '队',
      p: nums[0], w: nums[1], d: nums[2], l: nums[3],
      gf: nums[4], ga: nums[5], gd: nums[6], pts: nums[7]
    });
  }
}

if (teams.length !== 13) {
  console.error('Expected 13 teams, got', teams.length);
  process.exit(0);
}
console.log('Standings: OK');
teams.forEach(t => console.log(' ', t.pos, t.name, t.p + 'GP', t.w + 'W', t.d + 'D', t.l + 'L', t.gf + '-' + t.ga, t.pts + 'pts'));

// Update football.html
let fb = fs.readFileSync('football.html', 'utf8');

const spflStart = fb.indexOf('const SPFL = [');
const spflEnd = fb.indexOf('];', spflStart) + 2;
if (spflStart < 0) { console.error('SPFL not found'); process.exit(0); }

const oldSpfl = fb.substring(spflStart, spflEnd);
const crestPat = /name:'(\S+?)'[\s\S]*?crest:'([^']+)'/g;
const crestMap = {};
while ((m = crestPat.exec(oldSpfl)) !== null) {
  crestMap[m[1]] = m[2];
}

const newSpfl = 'const SPFL = [\n' +
  teams.map(t => {
    const c = crestMap[t.name] || 'crests/default.png';
    return `            { pos:${t.pos}, name:'${t.name}', p:${t.p}, w:${t.w}, d:${t.d}, l:${t.l}, gf:${t.gf}, ga:${t.ga}, gd:${t.gd}, pts:${t.pts},\n              crest:'${c}' }`;
  }).join(',\n') + '\n        ];';

fb = fb.slice(0, spflStart) + newSpfl + fb.slice(spflEnd);

// Update summary
fb = fb.replace(/盐城队 · \d+分（[^）]+）/, `盐城队 · ${teams[0].pts}分（${teams[0].p}战${teams[0].w}胜）`);
fb = fb.replace(/>\d+ 轮</, `>${teams[0].p} 轮<`);

// Validate JS
const js = fb.substring(fb.indexOf('<script>') + 8, fb.lastIndexOf('</script>'));
try {
  execSync('node --check -', { input: js, stdio: 'pipe' });
} catch (e) {
  console.error('JS validation FAILED, not saving.');
  process.exit(0);
}

fs.writeFileSync('football.html', fb);
console.log('Su Chao data updated and validated.');
