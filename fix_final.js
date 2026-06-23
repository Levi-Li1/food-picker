// fix_final.js — Dead simple: add showAns + insert tips/SVGs BEFORE gray box (safest position)
const fs = require('fs');

// Method tips and SVGs mapped to day+subject
const CONTENT = {
  w1_D1: '<div class="svg-diagram" style="text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px"><svg viewBox="0 0 600 80"><line x1="40" y1="40" x2="560" y2="40" stroke="#333" stroke-width="2"/><polygon points="560,36 570,40 560,44" fill="#333"/><text x="20" y="44" font-size="12">←负</text><text x="570" y="44" font-size="12">正→</text><text x="295" y="35" font-size="14" fill="var(--red)" font-weight="bold">0</text><circle cx="300" cy="40" r="4" fill="var(--red)"/><circle cx="200" cy="40" r="4" fill="var(--blue)"/><text x="195" y="25" font-size="11" fill="var(--blue)">-a</text><text x="195" y="65" font-size="10" fill="#888">|a|</text><circle cx="400" cy="40" r="4" fill="var(--blue)"/><text x="395" y="25" font-size="11" fill="var(--blue)">+a</text><text x="395" y="65" font-size="10" fill="#888">|a|</text></svg><p style="font-size:11px;color:var(--sub)">|a| = a(a≥0), |a| = -a(a<0) → 绝对值是到原点的距离</p></div>\n<div class="tip"><b>💡 有理数运算方法总结</b><br>定符号→算数值→"先乘方再乘除后加减有括号先括号"<br>去绝对值:|a|=a(a≥0),|a|=-a(a<0)<br>遇括号能用分配律的先用分配律</div>',
  w1_D2: '<div class="tip"><b>💡 整式乘除方法总结</b><br>同底数幂:乘加除减 aᵐ×aⁿ=aᵐ⁺ⁿ,aᵐ÷aⁿ=aᵐ⁻ⁿ|幂的乘方:(aᵐ)ⁿ=aᵐⁿ<br>平方差:(a+b)(a-b)=a²-b²|完全平方:(a±b)²=a²±2ab+b²"首平方尾平方2倍首尾放中央"<br>⚠️(-2)⁴=16≠-2⁴=-16！完全平方中间项2ab最易漏！</div>',
  w1_D3: '<div class="tip"><b>💡 方程不等式方法总结</b><br>五步法:去分母→去括号→移项变号→合并→系数化1<br>代入vs加减:系数差1倍→加减法;系数为1→代入法<br>不等式:乘除负数必须变号!>变<!口诀"同大取大同小取小"</div>',
  w1_D4: '<div class="svg-diagram" style="text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px"><svg viewBox="0 0 500 200"><line x1="250" y1="10" x2="250" y2="190" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/><text x="255" y="15" font-size="10" fill="#999">法线</text><line x1="60" y1="120" x2="250" y2="90" stroke="var(--orange)" stroke-width="2"/><polygon points="250,90 240,85 240,95" fill="var(--orange)"/><text x="100" y="100" font-size="11" fill="var(--orange)">入射光线</text><line x1="250" y1="90" x2="440" y2="120" stroke="var(--green)" stroke-width="2"/><polygon points="440,120 430,115 430,125" fill="var(--green)"/><text x="350" y="108" font-size="11" fill="var(--green)">反射光线</text><path d="M 230 70 A 50 50 0 0 1 270 70" fill="none" stroke="var(--red)" stroke-width="1.5"/><text x="255" y="65" font-size="10" fill="var(--red)">θ</text><path d="M 270 70 A 50 50 0 0 1 230 70" fill="none" stroke="var(--red)" stroke-width="1.5"/><text x="235" y="110" font-size="10" fill="var(--red)">θ</text><text x="260" y="170" font-size="11">反射角=入射角（三线共面两线分居）</text></svg></div>\n<div class="tip"><b>💡 光的反射与成像</b><br>反射定律:三线共面|两线分居|反射角=入射角(先画法线!)<br>平面镜成像四特点:等大/等距/垂直/虚像<br>镜面vs漫反射:都遵循反射定律!</div>',
};

// Supplementary days
const W4_EXTRA = `
<div class="day-page">
<div class="dtop"><div class="dnum">Day 23</div><div class="dinfo"><div>7月23日 周三</div><div style="font-size:12px">数学+政治+语文</div></div></div>
<div class="dbody">
<div class="goal"><b>🎯 今日目标</b>：相似三角形+政治宪法专题+古诗文默写</div>
<div class="steps">
<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>📖 数学 · 相似三角形（2h）</h4>
<p><b>三判定</b>：AA(两角等)|SAS(两边成比例+夹角等)|SSS(三边成比例)</p>
<p><b>性质</b>：面积比=相似比²！周长比=相似比</p>
<div class="q-block"><span class="q-num">1.</span>相似比2:3，面积比=？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">面积比=相似比²=(2/3)²=4:9</div></div>
<div class="q-block"><span class="q-num">2.</span>同一时刻1.6m人影长2m，8m旗杆影长？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">1.6/2=8/x→x=10m</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:#e91e63"></span>🏛️ 政治 · 宪法是根本法（1h）</h4>
<p><b>宪法地位</b>：①根本法 ②最高法律效力 ③制定修改程序更严格</p>
<p><b>公民基本权利</b>：平等权/政治权利/人身自由/社会经济/文化教育</p>
<p><b>公民基本义务</b>：遵守宪法/维护国家统一/依法纳税/服兵役</p>
<div class="q-block"><span class="q-num">1.</span>为什么说宪法是根本法？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">规定国家最根本问题；最高法律效力；制定修改程序更严格</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--red)"></span>📖 语文 · 古诗文默写（0.5h）</h4>
<p>默写《望岳》《春望》杜甫</p>
<div class="q-block"><span class="q-num">默写1</span>《望岳》<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">岱宗夫如何？齐鲁青未了。造化钟神秀，阴阳割昏晓。荡胸生曾云，决眦入归鸟。会当凌绝顶，一览众山小。</div></div>
</div></div>
<div class="check"><b>✔ 达标检查</b> □ 面积比=相似比²？ □ 宪法三点理由能背？ □ 古诗默写全对？</div>
</div></div>`;

const W5_EXTRA = `
<div class="day-page">
<div class="dtop"><div class="dnum">Day 30</div><div class="dinfo"><div>7月30日 周三</div><div style="font-size:12px">数学+历史+化学</div></div></div>
<div class="dbody">
<div class="goal"><b>🎯 今日目标</b>：圆(垂径+圆周角)+历史秦汉专题+化学化合价</div>
<div class="steps">
<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>📖 数学 · 圆（2h）</h4>
<p><b>垂径定理</b>：垂直于弦的直径平分弦及所对弧</p>
<p><b>圆周角定理</b>：圆周角=圆心角/2；直径所对圆周角=90°</p>
<div class="formula"><div class="eq">弧长 L=nπr/180 | 扇形 S=nπr²/360=Lr/2</div></div>
<div class="q-block"><span class="q-num">1.</span>半径5，弦AB=8，求弦心距<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">弦一半=4，弦心距=√(5²-4²)=3（垂径定理+勾股）</div></div>
<div class="q-block"><span class="q-num">2.</span>AB是直径，C在圆周上，∠ACB=？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">90°（直径所对圆周角是直角）</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:#795548"></span>📜 历史 · 秦汉时期（1h）</h4>
<p><b>秦朝</b>(前221年)：统一六国→中央集权→统一文字/货币/度量衡</p>
<p><b>汉朝</b>：文景之治→汉武帝大一统(推恩令/独尊儒术)→丝绸之路</p>
<div class="q-block"><span class="q-num">1.</span>秦朝统一全国在哪一年？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">公元前221年</div></div>
<div class="q-block"><span class="q-num">2.</span>汉武帝大一统的核心措施？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">推恩令(削弱诸侯)+独尊儒术(思想统一)</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>🧪 化学 · 化合价+化学式（1h）</h4>
<p><b>化合价口诀</b>：一价钾钠氯氢银 二价氧钙钡镁锌 三铝四硅五价磷</p>
<p>化合物中正负化合价代数和=0</p>
<div class="q-block"><span class="q-num">1.</span>写出氧化铝化学式(Al+3,O-2)<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">Al₂O₃(最小公倍数法:Al×2=+6,O×3=-6)</div></div>
</div></div>
<div class="check"><b>✔ 达标检查</b> □ 垂径定理+圆周角定理？ □ 秦汉时间线？ □ 化合价口诀背熟？</div>
</div></div>`;

// Process each week
for (const wid of ['w1','w2','w3','w4','w5','w6','w7','w8','w9']) {
  let html = fs.readFileSync(wid+'.html', 'utf8');

  // 1. Add showAns function
  if (!html.includes('function showAns')) {
    html = html.replace('function speak(text)',
      'function showAns(btn){var a=btn.nextElementSibling;a.classList.toggle("show");btn.textContent=a.classList.contains("show")?"隐藏答案":"点击查看答案";}\nfunction speak(text)');
  }

  // 2. Add SVG CSS class
  if (!html.includes('.svg-diagram{')) {
    html = html.replace('</style>','.svg-diagram{text-align:center;margin:10px 0;background:#fafafa;border-radius:10px;padding:8px}\n.svg-diagram svg{max-width:100%;height:auto}\n</style>');
  }

  // 3. Add tips/SVGs BEFORE gray box (search for COMPLETE gray box opening tag)
  if (wid === 'w1') {
    // Day 1: find its gray box, inject before it
    html = html.replace(
      /(<div class="dnum">Day 1<\/div>[\s\S]*?)<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">/,
      '$1' + CONTENT.w1_D1 + '\n<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">'
    );
    // Day 2
    html = html.replace(
      /(<div class="dnum">Day 2<\/div>[\s\S]*?)<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">/,
      '$1' + CONTENT.w1_D2 + '\n<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">'
    );
    // Day 3
    html = html.replace(
      /(<div class="dnum">Day 3<\/div>[\s\S]*?)<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">/,
      '$1' + CONTENT.w1_D3 + '\n<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">'
    );
    // Day 4
    html = html.replace(
      /(<div class="dnum">Day 4<\/div>[\s\S]*?)<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">/,
      '$1' + CONTENT.w1_D4 + '\n<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">'
    );
  }

  // 4. Add supplementary days
  if (wid === 'w4' && !html.includes('Day 23')) {
    html = html.replace('</div>\n<script>', '</div>\n\n'+W4_EXTRA+'\n<script>');
  }
  if (wid === 'w5' && !html.includes('Day 30')) {
    html = html.replace('</div>\n<script>', '</div>\n\n'+W5_EXTRA+'\n<script>');
  }

  fs.writeFileSync(wid+'.html', html, 'utf8');
  const hasShowAns = html.includes('function showAns');
  const tips = (html.match(/class="tip"/g)||[]).length;
  const svgs = (html.match(/svg-diagram/g)||[]).length - 1; // subtract CSS class
  console.log(wid+'.html: showAns='+hasShowAns+' tips='+tips+' svgs='+svgs+' size='+html.length+'B');
}
console.log('\nDone!');
