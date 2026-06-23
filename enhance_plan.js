// enhance_plan.js — Post-process week files with extra content, SVGs, politics, history
// Rule: NEVER inject inside style attributes. Always inject BEFORE <div style="background:#f0f0f5
const fs = require('fs');

// SVG diagrams
const SVGS = {
  numLine: '<div class="svg-diagram" style="text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px"><svg viewBox="0 0 600 80"><line x1="40" y1="40" x2="560" y2="40" stroke="#333" stroke-width="2"/><polygon points="560,36 570,40 560,44" fill="#333"/><text x="20" y="44" font-size="12">←负</text><text x="570" y="44" font-size="12">正→</text><text x="295" y="35" font-size="14" fill="var(--red)" font-weight="bold">0</text><circle cx="300" cy="40" r="4" fill="var(--red)"/><circle cx="200" cy="40" r="4" fill="var(--blue)"/><text x="195" y="25" font-size="11" fill="var(--blue)">-a</text><text x="195" y="65" font-size="10" fill="#888">|a|</text><circle cx="400" cy="40" r="4" fill="var(--blue)"/><text x="395" y="25" font-size="11" fill="var(--blue)">+a</text><text x="395" y="65" font-size="10" fill="#888">|a|</text></svg><p style="font-size:11px;color:var(--sub)">|a| = a(a≥0), |a| = -a(a<0) → 绝对值是到原点的距离</p></div>',
  reflection: '<div class="svg-diagram" style="text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px"><svg viewBox="0 0 500 200"><line x1="250" y1="10" x2="250" y2="190" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/><text x="255" y="15" font-size="10" fill="#999">法线</text><line x1="60" y1="120" x2="250" y2="90" stroke="var(--orange)" stroke-width="2"/><polygon points="250,90 240,85 240,95" fill="var(--orange)"/><text x="100" y="100" font-size="11" fill="var(--orange)">入射光线</text><line x1="250" y1="90" x2="440" y2="120" stroke="var(--green)" stroke-width="2"/><polygon points="440,120 430,115 430,125" fill="var(--green)"/><text x="350" y="108" font-size="11" fill="var(--green)">反射光线</text><path d="M 230 70 A 50 50 0 0 1 270 70" fill="none" stroke="var(--red)" stroke-width="1.5"/><text x="255" y="65" font-size="10" fill="var(--red)">θ</text><path d="M 270 70 A 50 50 0 0 1 230 70" fill="none" stroke="var(--red)" stroke-width="1.5"/><text x="235" y="110" font-size="10" fill="var(--red)">θ</text><text x="260" y="170" font-size="11">反射角 = 入射角（三线共面，两线分居）</text></svg></div>',
};

// Method tips
const TIPS = {
  math_num: '<div class="tip"><b>💡 有理数运算方法总结</b><br>①定符号(同号得正异号得负)→②算数值→③"先乘方再乘除后加减有括号先括号"<br>④去绝对值:|a|=a(a≥0),|a|=-a(a<0)→绝对值=距离，距离不能为负！<br>⑤遇括号能用分配律的先用分配律</div>',
  math_alg: '<div class="tip"><b>💡 整式乘除方法总结</b><br>同底数幂：乘加除减 aᵐ×aⁿ=aᵐ⁺ⁿ, aᵐ÷aⁿ=aᵐ⁻ⁿ | 幂的乘方：(aᵐ)ⁿ=aᵐⁿ<br>平方差：(a+b)(a-b)=a²-b² | 完全平方：(a±b)²=a²±2ab+b² "首平方尾平方2倍首尾放中央"<br>⚠️ (-2)⁴=16≠-2⁴=-16！完全平方中间项2ab最易漏！</div>',
  math_tri: '<div class="tip"><b>💡 全等证明万能模板</b><br>五判定：SSS|SAS|ASA|AAS|HL ⚠️SSA不能判定！中考第一陷阱！<br>步骤：圈条件→找隐含(公共边/公共角/对顶角/中点/平行)→选定理→写证明<br>"在△..和△..中→列条件→∴△..≌△..(判定法)"</div>',
  phys_lgt: '<div class="tip"><b>💡 光的反射与成像</b><br>反射定律:三线共面|两线分居|反射角=入射角(先画法线！)<br>平面镜成像四特点:等大/等距/垂直/虚像<br>镜面vs漫反射:都遵循反射定律！区别在反射面是否光滑</div>',
  phys_snd: '<div class="tip"><b>💡 声现象三特性辨析</b><br>音调↔频率(高尖低粗)|响度↔振幅(越大越响)|音色↔材料<br>"震耳欲聋"→响度；"曲高和寡"→音调；"闻声知人"→音色<br>回声计算:s=vt/2(v=340m/s) 噪声控制:声源/传播/人耳三途径</div>',
};

// Politics/History supplementary day content
function politicsBlock(title, content, questions, checkItems) {
  return '<div class="step full"><h4><span class="dot" style="background:#e91e63"></span>🏛️ 政治 · '+title+'</h4>\n'+content+'\n'+questions+'</div>';
}
function historyBlock(title, content, questions, checkItems) {
  return '<div class="step full"><h4><span class="dot" style="background:#795548"></span>📜 历史 · '+title+'</h4>\n'+content+'\n'+questions+'</div>';
}
function Q(n,q,a){return '<div class="q-block"><span class="q-num">'+n+'.</span><span class="question">'+q+'</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">'+a+'</div></div>';}

// Supplementary days for sparse weeks
const W4_EXTRA = `
<div class="day-page">
<div class="dtop"><div class="dnum">Day 23</div><div class="dinfo"><div>7月23日 周三</div><div style="font-size:12px">数学+政治+化学</div></div></div>
<div class="dbody">
<div class="goal"><b>🎯 今日目标</b>：相似三角形面积比+政治宪法专题+化学原子结构</div>
<div class="steps">
<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>📖 数学 · 相似三角形（2h）</h4>
<p><b>三判定</b>：AA(两角等)|SAS(两边成比例+夹角等)|SSS(三边成比例)</p>
<p><b>性质</b>：面积比=相似比²！周长比=相似比 <span style="color:var(--red)">★★★</span></p>
`+Q('1','相似比2:3，面积比=？','面积比=相似比²=(2/3)²=4:9')+
Q('2','△ABC中DE∥BC,AD=3,DB=6,AE=4，求EC','AD/DB=AE/EC→3/6=4/EC→EC=8')+
Q('3','同一时刻1.6m人影长2m，8m旗杆影长？','1.6/2=8/x→x=10m')+
`</div>
`+politicsBlock('宪法是根本法','<p><b>宪法地位</b>：①宪法是国家的根本法 ②宪法具有最高的法律效力 ③宪法的制定和修改程序比其他法律更严格</p><p><b>公民基本权利</b>：平等权/政治权利和自由/人身自由/社会经济权利/文化教育权利</p><p><b>公民基本义务</b>：遵守宪法法律/维护国家统一/依法纳税/服兵役</p>',
Q('1','为什么说宪法是根本法？','宪法规定国家生活中最根本最重要的问题；具有最高法律效力；制定修改程序更严格')+
Q('2','公民最基本、最重要的权利是什么？','人身自由权'),
'')+`
<div class="step full"><h4><span class="dot" style="background:var(--red)"></span>📖 语文 · 古诗文默写（0.5h）</h4>
<p>默写《望岳》杜甫 + 《春望》杜甫</p>
`+Q('默写1','《望岳》杜甫','岱宗夫如何？齐鲁青未了。造化钟神秀，阴阳割昏晓。荡胸生曾云，决眦入归鸟。会当凌绝顶，一览众山小。')+
Q('默写2','《春望》杜甫','国破山河在，城春草木深。感时花溅泪，恨别鸟惊心。烽火连三月，家书抵万金。白头搔更短，浑欲不胜簪。')+
`</div>
</div>
<div class="check"><b>✔ 达标检查</b> □ 面积比=相似比²？ □ 宪法三点理由能背？ □ 古诗默写全对？</div>
</div>
</div>`;

const W5_EXTRA = `
<div class="day-page">
<div class="dtop"><div class="dnum">Day 30</div><div class="dinfo"><div>7月30日 周三</div><div style="font-size:12px">数学+历史+化学</div></div></div>
<div class="dbody">
<div class="goal"><b>🎯 今日目标</b>：圆的切线与弧长+历史秦汉专题+化学化合价</div>
<div class="steps">
<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>📖 数学 · 圆（垂径定理+圆周角）（2h）</h4>
<p><b>⭐ 垂径定理</b>：垂直于弦的直径平分弦及所对弧。推论：平分弦(非直径)的直径⊥弦</p>
<p><b>⭐ 圆周角定理</b>：圆周角=圆心角/2；直径所对圆周角=90° <span style="color:var(--red)">★★★</span></p>
<div class="formula"><div class="eq">弧长 L=nπr/180 | 扇形面积 S=nπr²/360=Lr/2</div></div>
`+Q('1','半径5，弦AB=8，求弦心距','弦一半=4，弦心距=√(5²-4²)=3（垂径定理+勾股）')+
Q('2','AB是直径，C在圆周上，∠ACB=？','90°（直径所对圆周角是直角）')+
Q('3','半径为10cm，圆心角72°，扇形面积？','S=72×π×100/360=20π cm²')+
`</div>
`+historyBlock('秦汉时期','<p><b>秦朝</b>(前221年)：统一六国→中央集权制(皇帝制/三公九卿/郡县制)→统一文字/货币/度量衡→焚书坑儒→陈胜吴广起义</p><p><b>汉朝</b>：文景之治→汉武帝大一统(推恩令/独尊儒术/盐铁官营)→张骞出使西域→丝绸之路</p><p><b>对比秦皇汉武</b>：秦皇重法家统一/汉武尊儒术大一统</p>',
Q('1','秦朝统一全国是在哪一年？','公元前221年')+
Q('2','汉武帝"大一统"的核心措施是什么？','推恩令(削弱诸侯)+独尊儒术(思想统一)'),
'')+`
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>🧪 化学 · 化合价+化学式（1h）</h4>
<p><b>化合价口诀</b>：一价钾钠氯氢银 二价氧钙钡镁锌 三铝四硅五价磷 二三铁二四碳 一二铜二四六硫</p>
<p><b>规则</b>：单质化合价=0 | 化合物正负化合价代数和=0</p>
<p><b>写化学式</b>：正左负右→标化合价→找最小公倍数→定各原子个数</p>
`+Q('1','写出氧化铝的化学式(Al+3,O-2)','Al₂O₃(最小公倍数法:Al×2=+6,O×3=-6)')+
Q('2','CO₂中C的化合价是多少？','+4(O为-2,CO₂: x+2×(-2)=0→x=+4)')+
`</div>
</div>
<div class="check"><b>✔ 达标检查</b> □ 垂径定理+圆周角定理？ □ 秦汉时间线能画？ □ 化合价口诀背熟？</div>
</div>
</div>`;

// Inject content into each week
function injectBeforeGray(html, dayLabel, content) {
  // Find the day section, then find the first gray box in that section, inject before it
  const dayIdx = html.indexOf('<div class="dnum">'+dayLabel+'</div>');
  if (dayIdx === -1) return html;
  const after = html.slice(dayIdx);
  const nextDay = after.indexOf('<div class="dnum">Day ', 50);
  const section = nextDay > 0 ? after.slice(0, nextDay) : after.slice(0, after.indexOf('</body>'));
  const grayPos = section.indexOf('<div style="background:#f0f0f5');
  if (grayPos === -1) return html;
  // Check if already injected
  const beforeGray = section.slice(0, grayPos);
  if (beforeGray.includes(content.substring(0, 50))) return html;
  return html.slice(0, dayIdx + grayPos) + content + '\n' + html.slice(dayIdx + grayPos);
}

// Process all weeks
for (const wid of ['w1','w2','w3','w4','w5','w6','w7','w8','w9']) {
  let html = fs.readFileSync(wid+'.html', 'utf8');
  let adds = 0;

  // Add SVG diagrams
  if (wid === 'w1') {
    html = injectBeforeGray(html, 'Day 1', SVGS.numLine);
    html = injectBeforeGray(html, 'Day 4', SVGS.reflection);
  }
  if (wid === 'w2') {
    html = injectBeforeGray(html, 'Day 8', TIPS.math_tri);
    html = injectBeforeGray(html, 'Day 9', TIPS.phys_snd);
    html = injectBeforeGray(html, 'Day 10', TIPS.math_tri);
  }
  if (wid === 'w3') {
    html = injectBeforeGray(html, 'Day 15', TIPS.math_alg);
    html = injectBeforeGray(html, 'Day 16', TIPS.phys_lgt);
  }
  
  // Add supplementary content for sparse weeks
  if (wid === 'w4' && !html.includes('Day 23')) {
    html = html.replace('</div>\n<script>', '</div>\n\n'+W4_EXTRA+'\n<script>');
    adds += 1;
  }
  if (wid === 'w5' && !html.includes('Day 30')) {
    html = html.replace('</div>\n<script>', '</div>\n\n'+W5_EXTRA+'\n<script>');
    adds += 1;
  }

  // Add SVG class to CSS if not present
  if (!html.includes('.svg-diagram')) {
    html = html.replace('</style>', '.svg-diagram{text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px}\n.svg-diagram svg{max-width:100%;height:auto}\n</style>');
  }

  fs.writeFileSync(wid+'.html', html, 'utf8');
  const svgs = (html.match(/svg-diagram/g)||[]).length;
  const tips = (html.match(/class="tip"/g)||[]).length;
  console.log(wid+'.html: '+html.length+'B, svg='+svgs+', tips='+tips+', added='+adds+' blocks');
}
console.log('\nDone!');
