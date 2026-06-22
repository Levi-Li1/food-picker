// add_supplements.js v3 — Clean targeted approach
const fs = require('fs');

const swb = [['effort','ˈefərt','n.','努力','I will put more effort into my studies.','我会在学习上更加努力。'],['education','ˌedʒuˈkeɪʃn','n.','教育','Education is very important.','教育非常重要。'],['effect','ɪˈfekt','n.','影响;效果','The medicine had a good effect.','药效果很好。'],['enemy','ˈenəmi','n.','敌人','He is not your enemy.','他不是你的敌人。'],['energy','ˈenərdʒi','n.','能量;精力','I have no energy today.','我今天没有精力。'],['engineer','ˌendʒɪˈnɪr','n.','工程师','My father is an engineer.','我爸爸是工程师。'],['enjoy','ɪnˈdʒɔɪ','v.','享受;喜欢','I enjoy reading books.','我喜欢读书。'],['environment','ɪnˈvaɪrənmənt','n.','环境','Protect the environment.','保护环境。'],['especially','ɪˈspeʃəli','adv.','特别;尤其','I like fruit, especially apples.','我喜欢水果，尤其是苹果。'],['event','ɪˈvent','n.','事件;活动','It was a big event.','那是一个大事件。'],['exam','ɪɡˈzæm','n.','考试','The exam is next week.','考试在下周。'],['example','ɪɡˈzæmpl','n.','例子','Give me an example.','给我一个例子。'],['excellent','ˈeksələnt','adj.','优秀的','Your work is excellent.','你的工作很优秀。'],['exercise','ˈeksərsaɪz','n./v.','锻炼;练习','Take more exercise every day.','每天多锻炼。'],['expect','ɪkˈspekt','v.','期待;预料','I expect to pass the exam.','我期待通过考试。'],['experience','ɪkˈspɪriəns','n.','经验;经历','Do you have any work experience?','你有工作经验吗？'],['experiment','ɪkˈsperɪmənt','n.','实验','We did a science experiment.','我们做了一个科学实验。'],['explain','ɪkˈspleɪn','v.','解释','Can you explain this to me?','你能解释这个给我吗？'],['fact','fækt','n.','事实','This is a scientific fact.','这是一个科学事实。'],['family','ˈfæməli','n.','家庭','Family is very important.','家庭非常重要。'],['famous','ˈfeɪməs','adj.','著名的','He is a famous singer.','他是一位著名歌手。'],['fan','fæn','n.','风扇;粉丝','I am a big fan of football.','我是个足球迷。'],['fashion','ˈfæʃn','n.','时尚','She likes fashion design.','她喜欢时尚设计。'],['fast','fæst','adj./adv.','快的','He runs very fast.','他跑得很快。'],['father','ˈfɑːðər','n.','父亲','My father is a teacher.','我父亲是老师。'],['favorite','ˈfeɪvərɪt','adj./n.','最喜欢的','This is my favorite book.','这是我最喜欢的书。'],['fear','fɪr','n./v.','害怕','Do not fear failure.','不要害怕失败。'],['feed','fiːd','v.','喂养','Please feed the dog.','请喂狗。'],['feel','fiːl','v.','感觉','I feel very happy today.','我今天感觉很开心。'],['field','fiːld','n.','领域;田野','The children play in the field.','孩子们在田野里玩耍。']];
let si=0; function snext(){const w=swb[si%swb.length];si++;return w;}
function swc(n,w){return `<div style="display:flex;align-items:baseline;gap:8px;padding:6px 0;border-bottom:1px solid #eee;font-size:13px"><span style="color:#999;min-width:24px;font-size:11px">${n}.</span><b style="color:#1d1d1f;min-width:80px">${w[0]}</b> <span style="color:var(--sub);font-size:12px;min-width:100px">${w[1]}</span> <span style="color:var(--green);min-width:30px"><i>${w[2]}</i></span> ${w[3]} <button onclick="speak('${w[0]}')" style="border:none;background:#8e8e93;color:#fff;border-radius:50%;width:22px;height:22px;cursor:pointer;font-size:10px;flex-shrink:0" title="播放发音">▶</button></div>`;}
function sg30(){let s='';for(let i=1;i<=30;i++){const w=snext();s+=swc(i,w)+`<div style="font-size:11px;color:#888;margin-left:122px;margin-bottom:2px">${w[4]} <span style="color:#999">${w[5]}</span></div>\n`;}return `<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea">\n<p style="margin:0 0 8px 0"><b>今日30词</b>（点击 ▶ 按钮听发音）</p>\n${s}</div>`;}

// Method summary cards
const methods = {
  math_num: `<div class="tip"><b>💡 有理数运算解题方法总结</b><br>①定符号：先判定最终结果符号（同号得正，异号得负）<br>②算数值：忽略符号只算数字<br>③混合运算口诀："先乘方、再乘除、后加减、有括号先括号"<br>④去绝对值：|a|=a(a≥0), |a|=-a(a<0)<br>⑤遇括号能用分配律的先用分配律</div>`,
  math_algebra: `<div class="tip"><b>💡 整式乘除与乘法公式解题总结</b><br>同底数幂：乘加除减（aᵐ×aⁿ=aᵐ⁺ⁿ, aᵐ÷aⁿ=aᵐ⁻ⁿ）<br>幂的乘方：(aᵐ)ⁿ=aᵐⁿ → 指数相乘<br>平方差：(a+b)(a-b)=a²-b² → 正反向都要练<br>完全平方：(a±b)²=a²±2ab+b² → 口诀"首平方，尾平方，2倍首尾放中央"<br>⚠️ (-2)⁴≠-2⁴！负号在括号内外结果不同！中间项2ab最易漏！</div>`,
  math_eq: `<div class="tip"><b>💡 一元一次方程解题五步法</b><br>①去分母（每项都乘最小公倍数）→ ②去括号（括号前"-"各项变号）→ ③移项（过等号必变号！）→ ④合并同类项 → ⑤系数化1<br>代入vs加减选择：系数差1倍→加减法；某变量系数为1→代入法<br>应用题：设未知数→找等量关系→列方程→解→检验</div>`,
  math_ineq: `<div class="tip"><b>💡 不等式解题方法总结</b><br>核心：①加减不变号 ②乘除正数不变号 ③乘除负数必须变号！>变<！<br>不等式组：分别求解→数轴画解集→找公共部分<br>口诀："同大取大，同小取小，大小小大取中间，大大小小无解"</div>`,
  math_congruent: `<div class="tip"><b>💡 全等三角形证明万能模板</b><br>五判定：SSS|SAS|ASA|AAS|HL（仅Rt△）⚠️ SSA不能判定！<br>证明步骤：①圈条件 ②找隐含（公共边/公共角/对顶角/中点→等边/平行→等角）③选定理 ④写"在△..和△..中→列条件→∴△..≌△..（判定法）"<br>隐含条件清单：公共边、公共角、对顶角、中点→等边、平行→等角、等腰→等边等角</div>`,
  math_func: `<div class="tip"><b>💡 一次函数解题方法总结</b><br>y=kx+b，k→斜率(k>0上升,k<0下降)，b→y轴截距<br>待定系数法：①设y=kx+b ②代入两点 ③解方程组 ④代回<br>象限判断：k>0,b>0→一二三；k>0,b<0→一三四；k<0,b>0→一二四；k<0,b<0→二三四<br>交点：联立两解析式解方程组</div>`,
  math_pythag: `<div class="tip"><b>💡 勾股定理解题方法总结</b><br>Rt△中 a²+b²=c²（c斜边）<br>三种用法：①知两直角边求斜边 c=√(a²+b²) ②知斜边和一直角边求另 a=√(c²-b²) ③逆定理判直角<br>常用勾股数：(3,4,5)(6,8,10)(5,12,13)(7,24,25)(8,15,17)→考试秒杀！<br>辅助线：等腰三角形画底边高→得两个全等Rt△→用勾股求高</div>`,
  math_geom: `<div class="tip"><b>💡 几何证明通用方法总结</b><br>综合法：已知→可知→更多→结论<br>分析法：要证什么←需要什么←已知<br>两路夹击：同时前后推，找中间桥梁（最常用！）<br>辅助线口诀：遇中点→中线/中位线；遇角分线→对称；遇平行→同位角/内错角；遇等腰→三线合一<br>书写格式：∵条件 ∴结论（每步有依据）</div>`,
  math_similar: `<div class="tip"><b>💡 相似三角形解题方法总结</b><br>三判定：AA（两角等）、SAS（两边成比例+夹角等）、SSS（三边成比例）<br>性质：对应边成比例 | 周长比=相似比 | 面积比=相似比²<br>⚠️ 相似vs全等：全等是相似的特例（相似比=1），全等用"等"，相似用"成比例"<br>应用：测高→物高/影长=人高/人影长</div>`,
  math_circle: `<div class="tip"><b>💡 圆的定理解题方法总结</b><br>垂径定理：垂直于弦的直径平分弦及所对弧<br>圆周角定理：圆周角=圆心角/2；直径所对圆周角=90°<br>切线判定：经过半径外端且垂直于半径的直线是切线<br>切线长定理：从圆外一点引两条切线，切线长相等<br>弧长L=nπr/180 | 扇形面积S=nπr²/360=Lr/2</div>`,
  math_stats: `<div class="tip"><b>💡 统计与概率解题方法总结</b><br>平均数=总和÷个数 | 中位数=排序后中间的数 | 众数=出现最多的数<br>方差：各数据与平均数差的平方和的平均数（越大越不稳定）<br>概率P(A)=m/n（m→事件出现次数，n→总可能）<br>列举法：树状图确保不重不漏！</div>`,
  phys_sound: `<div class="tip"><b>💡 声现象三特性辨析</b><br>音调↔频率（高尖低粗）| 响度↔振幅（越大越响）| 音色↔材质<br>考题对应："震耳欲聋"→响度；"曲高和寡"→音调；"闻其声知其人"→音色<br>计算：s=vt, v=340m/s → 回声测距s=vt/2<br>噪声控制三途径：声源处、传播中、人耳处</div>`,
  phys_light: `<div class="tip"><b>💡 光的反射与平面镜成像</b><br>反射定律：三线共面、两线分居、反射角=入射角（画图先画法线！）<br>镜面反射vs漫反射：都遵循反射定律！<br>平面镜成像四特点：等大、等距、垂直、虚像<br>画图步骤：①作对称点 ②虚线连像 ③实线连人眼</div>`,
  phys_pressure: `<div class="tip"><b>💡 压强解题方法总结</b><br>固体：P=F/S → 先算F(通常F=G)再算S(注意m²!)<br>液体：P=ρgh → 只与ρ和h有关，与容器形状无关！<br>增大压强：增大F/减小S（刀刃、针尖）<br>减小压强：减小F/增大S（坦克履带、书包宽带）</div>`,
  phys_buoyancy: `<div class="tip"><b>💡 浮力四种计算方法总结</b><br>①压力差法：F浮=F下-F上 ②称重法：F浮=G物-F示 ③阿基米德：F浮=G排=ρ液gV排（核心！）④平衡法：漂浮/悬浮F浮=G物<br>沉浮判断：ρ物<ρ液→上浮；ρ物=ρ液→悬浮；ρ物>ρ液→下沉<br>解题策略：先判断状态→选公式→代入计算</div>`,
  phys_work: `<div class="tip"><b>💡 功和机械能解题方法总结</b><br>做功两条件：①有力 ②在力的方向有距离（缺一不可）<br>不做功三情况：有力无距/有距无力/力距垂直<br>W=Fs（F和s必须在同一方向！）<br>P=W/t=匀速时P=Fv<br>机械能=动能+势能（动能看m,v；势能看m,h）<br>机械能守恒条件：只有重力/弹力做功</div>`,
  phys_lever: `<div class="tip"><b>💡 简单机械解题方法总结</b><br>杠杆平衡：F₁L₁=F₂L₂<br>三种杠杆：省力(L₁>L₂，撬棍)、费力(L₁<L₂，镊子)、等臂(L₁=L₂，天平)<br>定滑轮：F=G，只改变方向（等臂杠杆）<br>动滑轮：F=G/2，省力不改方向（L₁=2L₂）<br>滑轮组：F=G/n（n=承重绳子段数），s=nh</div>`,
  eng_future: `<div class="tip"><b>💡 一般将来时解题总结</b><br>结构①：will+do（客观将来/临时决定）②am/is/are going to+do（计划/迹象）<br>标志词：tomorrow, next week, in the future, soon<br>否定：won't+do / am not going to+do<br>⚠️ if/unless/as soon as引导从句用一般现在时表将来（主将从现）</div>`,
  eng_past: `<div class="tip"><b>💡 一般过去时解题总结</b><br>结构：主语+动词过去式(did)<br>标志词：yesterday, last week, ...ago, in 2020<br>否定：didn't+动词原形 疑问：Did+主语+动词原形？<br>必背不规则动词：go→went, come→came, see→saw, eat→ate, take→took, get→got, have→had, do→did, make→made</div>`,
  eng_perfect: `<div class="tip"><b>💡 现在完成时解题总结</b><br>结构：have/has+过去分词(done)<br>三用法：①已完成(already/just/yet) ②经历(ever/never) ③持续(for+时段/since+时间点)<br>⚠️ have gone to(去了没回) vs have been to(去过已回)<br>与一般过去时区别：完成时强调对现在的影响/持续到现在</div>`,
  eng_obj: `<div class="tip"><b>💡 宾语从句三步法</b><br>①选引导词（陈述→that；一般疑问→if/whether；特殊疑问→wh-词）<br>②变语序（必须陈述语序！主+谓！最大易错点！）<br>③调时态（主现从任意，主过从过，客观真理不变）<br>⚠️ "Do you know what is his name?" ❌ → "...what his name is?" ✅</div>`,
  eng_passive: `<div class="tip"><b>💡 被动语态解题总结</b><br>结构：be+过去分词(done)<br>一般现在被动：am/is/are+done；一般过去被动：was/were+done<br>情态动词被动：can/must/should+be+done<br>主动变被动口诀：宾变主、谓变be+done、主变by+宾<br>不用被动：不及物动词(happen/die)、系动词(sound/feel)</div>`,
  eng_rel: `<div class="tip"><b>💡 定语从句解题总结</b><br>关系代词：who(人)、whom(人/宾)、which(物)、that(通用)、whose(…的)<br>只用that：①最高级/序数词修饰先行词 ②先行词是all/anything/nothing等 ③先行词既有人又有物<br>关系代词作宾语时可省略 → The book (that) I read is good.</div>`,
  eng_compare: `<div class="tip"><b>💡 比较级/最高级解题总结</b><br>规则：单音节+er/est；多音节+more/most<br>不规则：good→better→best; bad→worse→worst; many→more→most; little→less→least<br>句型：比较级+than | the+最高级+范围 | as+原级+as | not as/so+原级+as</div>`,
  chem_change: `<div class="tip"><b>💡 物理变化vs化学变化辨析</b><br>唯一标准：是否有新物质生成<br>物理变化：状态/形状改变（水结冰、铁制铁钉、玻璃碎）<br>化学变化：新物质生成（燃烧、生锈、食物腐败、酿酒）<br>⚠️ 发光发热≠化学变化！（电灯发光=物理变化）<br>化学变化伴随现象（不是判断依据！）：发光/放热/变色/气体/沉淀</div>`,
  chem_elem: `<div class="tip"><b>💡 元素与化合价记忆方法</b><br>前20号：氢氦锂铍硼 碳氮氧氟氖 钠镁铝硅磷 硫氯氩钾钙<br>地壳含量：O>Si>Al>Fe>Ca>Na>K>Mg<br>化合价口诀：一价钾钠氯氢银，二价氧钙钡镁锌，三铝四硅五价磷<br>写化学式：正左负右→标化合价→找最小公倍数→定原子个数</div>`,
  chem_eq: `<div class="tip"><b>💡 化学方程式配平方法总结</b><br>步骤：写(化学式)→配(计量数)→注(条件+↑↓)<br>配平法1：最小公倍数法（适合大多数）<br>配平法2：奇数偶配法（有奇数的先用2调整）<br>质量守恒：反应前后原子种类/数目/质量不变<br>四反应类型：化合(A+B→AB)、分解(AB→A+B)、置换(A+BC→AC+B)、复分解(AB+CD→AD+CB)</div>`,
};

// Map each day to a method card
const dayMethod = {
  'Day 1': methods.math_num, 'Day 2': methods.math_algebra, 'Day 3': methods.math_eq,
  'Day 4': methods.math_ineq, 'Day 8': methods.math_congruent, 'Day 9': methods.math_congruent,
  'Day 10': methods.phys_light, 'Day 11': methods.math_pythag, 'Day 12': methods.math_pythag,
  'Day 15': methods.math_func, 'Day 16': methods.math_func, 'Day 17': methods.math_func,
  'Day 18': methods.phys_pressure, 'Day 19': methods.math_eq,
  'Day 22': methods.math_geom, 'Day 23': methods.math_similar, 'Day 24': methods.eng_past,
  'Day 29': methods.math_geom, 'Day 30': methods.math_circle, 'Day 31': methods.phys_lever,
  'Day 32': methods.math_stats, 'Day 36': methods.eng_obj, 'Day 37': methods.phys_work,
  'Day 43': methods.math_geom, 'Day 44': methods.chem_eq, 'Day 45': methods.math_congruent,
  'Day 50': methods.math_congruent, 'Day 51': methods.math_circle,
  'Day 57': methods.math_geom, 'Day 58': methods.chem_eq, 'Day 59': methods.math_geom,
  'Day 60': methods.math_eq,
};

// Supplementary day pages for weeks with gaps
const suppDays = {
w4: `
<div class="day-page">
<div class="dtop"><div class="dnum">Day 23</div><div class="dinfo"><div>7月23日 周三</div><div style="font-size:12px">数学+物理+英语</div></div></div>
<div class="dbody">
<div class="goal"><b>🎯 今日目标</b>：相似三角形判定与应用；液体压强深化；形容词副词比较级最高级</div>
<div class="steps">
<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>📖 数学 · 相似三角形（2h）</h4>
<p><b>⭐ 相似三角形定义</b>——三角对应相等、三边对应成比例。符号：△ABC∽△DEF</p>
<p><b>三判定法</b>：①AA（两角对应相等）②SAS（两边成比例且夹角等）③SSS（三边成比例）</p>
<p><b>核心性质</b>：面积比=相似比²！周长比=相似比 <span class="star" style="color:var(--red)">★★★</span></p>
<p><b>应用·测高</b>：同一时刻物高与影长成正比</p>
<div class="q-block"><span class="q-num">1.</span>△ABC中DE∥BC,AD=3,DB=6,AE=4，求EC。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">AD/DB=AE/EC→3/6=4/EC→EC=8</div></div>
<div class="q-block"><span class="q-num">2.</span>相似比2:3，面积比？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">面积比=相似比²=4:9</div></div>
<div class="q-block"><span class="q-num">3.</span>同一时刻1.6m人影长2m，8m旗杆影长？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">1.6/2=8/x→x=10m</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--orange)"></span>⚡ 物理 · 液体压强（1h）</h4>
<p>P=ρgh（只与密度和深度有关）| 连通器原理</p>
<div class="q-block"><span class="q-num">1.</span>水深5m处压强？(ρ水=1.0×10³, g=10)<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">P=1.0×10³×10×5=5×10⁴Pa</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--green)"></span>🔤 英语 · 比较级最高级（1h）</h4>
<p>规则：单音节+er/est；多音节+more/most</p>
<p>不规则：good→better→best|bad→worse→worst|many→more→most</p>
<p>句型：比较级+than|the+最高级+范围|as+原级+as|not as/so+原级+as</p>
<div class="q-block"><span class="q-num">1.</span>Tom is ___(tall) than Jack.<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">taller（比较级+than）</div></div>
</div>
</div>
<div class="check"><b>✔ 达标检查</b> □ 相似面积比=相似比²？ □ P=ρgh公式记住？ □ 比较级不规则变化记住？</div>
${sg30()}
</div></div>
<div class="day-page">
<div class="dtop"><div class="dnum">Day 24</div><div class="dinfo"><div>7月24日 周四</div><div style="font-size:12px">数学+化学+英语</div></div></div>
<div class="dbody">
<div class="goal"><b>🎯 今日目标</b>：圆的基础（垂径定理+圆周角定理）；化学原子结构+离子；英语一般过去时</div>
<div class="steps">
<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>📖 数学 · 圆——垂径定理+圆周角定理（2h）</h4>
<p><b>⭐ 垂径定理</b>：垂直于弦的直径平分弦及所对弧</p>
<p><b>⭐ 圆周角定理</b>：圆周角=圆心角/2；直径所对圆周角=90° <span class="star" style="color:var(--red)">★★★</span></p>
<div class="formula"><div class="eq">弧长L=nπr/180 | 扇形面积S=nπr²/360=Lr/2</div></div>
<div class="q-block"><span class="q-num">1.</span>半径5，弦AB=8，求弦心距。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">弦一半=4，弦心距=√(5²-4²)=3（垂径定理+勾股）</div></div>
<div class="q-block"><span class="q-num">2.</span>AB是直径，C在圆周上，∠ACB=？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">90°（直径所对圆周角是直角）</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>🧪 化学 · 原子结构+离子（1h）</h4>
<p>原子=原子核(质子+中子)+核外电子 | 原子序数=质子数=电子数</p>
<p>核外电子排布：第1层≤2,第2层≤8,最外层≤8</p>
<p>阳离子（失电子带正电，Na⁺）| 阴离子（得电子带负电，Cl⁻）</p>
<div class="q-block"><span class="q-num">1.</span>钠原子11个质子，电子数？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">11（原子中质子数=电子数）</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--green)"></span>🔤 英语 · 一般过去时（1h）</h4>
<p>结构：主语+动词过去式(did) | 标志词：yesterday, last week, ...ago</p>
<p>规则变化：+ed, 以e+d, 辅y→ied, 重读闭音节双写+ed</p>
<p>必背：go→went, come→came, see→saw, eat→ate, get→got, have→had, do→did</p>
<p>否定：didn't+动原 | 疑问：Did+主+动原？<span class="star" style="color:var(--red)">★★★</span></p>
<div class="q-block"><span class="q-num">1.</span>She ___(go) to Beijing last week.<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">went（last week→一般过去时）</div></div>
</div>
</div>
<div class="check"><b>✔ 达标检查</b> □ 垂径定理+圆周角定理能默写？ □ 原子结构三个等式？ □ 不规则动词10个背熟？</div>
${sg30()}
</div></div>`,

w5: `
<div class="day-page">
<div class="dtop"><div class="dnum">Day 30</div><div class="dinfo"><div>7月30日 周三</div><div style="font-size:12px">数学+物理+化学</div></div></div>
<div class="dbody">
<div class="goal"><b>🎯 今日目标</b>：圆的切线与综合；物理简单机械（杠杆）；化学化合价</div>
<div class="steps">
<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>📖 数学 · 圆的切线+综合（2h）</h4>
<p><b>切线判定</b>：经过半径外端且垂直于半径 | <b>切线性质</b>：圆的切线⊥过切点的半径</p>
<p><b>切线长定理</b>：从圆外一点引两条切线，切线长相等</p>
<div class="q-block"><span class="q-num">1.</span>半径6，圆心到直线距离6？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">d=r→相切（切线）</div></div>
<div class="q-block"><span class="q-num">2.</span>半径10cm，圆心角72°，扇形面积？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">S=72×π×100/360=20π cm²</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--orange)"></span>⚡ 物理 · 杠杆（1h）</h4>
<p><b>杠杆平衡</b>：F₁L₁=F₂L₂ <span class="star" style="color:var(--red)">★★★</span></p>
<p>省力杠杆(L₁>L₂，撬棍) | 费力杠杆(L₁<L₂，镊子) | 等臂杠杆(L₁=L₂，天平)</p>
<div class="q-block"><span class="q-num">1.</span>200N物体距支点0.5m，另一端距支点2m，需多少力？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">F₁×2=200×0.5→F₁=50N（省力杠杆）</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>🧪 化学 · 化合价+化学式（1h）</h4>
<p>口诀：一价钾钠氯氢银，二价氧钙钡镁锌，三铝四硅五价磷</p>
<p>化合物中正负化合价代数和=0 | 写化学式：正左负右→标化合价→找最小公倍数</p>
<div class="q-block"><span class="q-num">1.</span>写出氧化铝化学式（Al+3, O-2）<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">Al₂O₃（最小公倍数法：Al×2=+6, O×3=-6）</div></div>
</div>
</div>
<div class="check"><b>✔ 达标检查</b> □ 切线性质与判定能区分？ □ F₁L₁=F₂L₂记住了？ □ 化合价口诀背熟？</div>
${sg30()}
</div></div>
<div class="day-page">
<div class="dtop"><div class="dnum">Day 31</div><div class="dinfo"><div>7月31日 周四</div><div style="font-size:12px">数学+英语+语文</div></div></div>
<div class="dbody">
<div class="goal"><b>🎯 今日目标</b>：统计与概率；英语定语从句；语文成语误用+病句修改</div>
<div class="steps">
<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>📖 数学 · 统计与概率（2h）</h4>
<p>平均数=总和÷个数 | 中位数=排序后中间的数 | 众数=出现最多的数</p>
<p>方差=各数据与平均数差的平方和的平均数（越大越不稳定）</p>
<p><b>概率</b>P(A)=m/n | 列举法：树状图确保不重不漏！</p>
<div class="q-block"><span class="q-num">1.</span>数据2,3,3,4,5,5,5的平均数、中位数、众数？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">平均数≈3.86，中位数=4，众数=5</div></div>
<div class="q-block"><span class="q-num">2.</span>掷两枚硬币都正面的概率？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">P=1/4（正正/正反/反正/反反共4种可能）</div></div>
<div class="q-block"><span class="q-num">3.</span>袋中3红2白，取1球，取到红球概率？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">P=3/5</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--green)"></span>🔤 英语 · 定语从句（1h）</h4>
<p>关系代词：who(人)、which(物)、that(通用)、whose(…的)</p>
<p>只用that：①最高级/序数词修饰 ②先行词all/anything等 ③先行词既有人又有物</p>
<div class="q-block"><span class="q-num">1.</span>The girl ___ is singing is my sister.<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">who/that（指人作主语）</div></div>
<div class="q-block"><span class="q-num">2.</span>This is the best movie ___ I have seen.<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">that（最高级best修饰→只用that）</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--red)"></span>📖 语文 · 成语误用+病句修改（0.5h）</h4>
<p><b>六种病句类型</b>：①搭配不当 ②成分残缺（"通过…使…"→删"使"或"通过"）③语序不当 ④句式杂糅 ⑤表意不明 ⑥不合逻辑（"避免不再"→双重否定）</p>
<div class="q-block"><span class="q-num">1.</span>改：秋天的北京是美丽的季节。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">北京的秋天是美丽的季节（搭配不当）</div></div>
<div class="q-block"><span class="q-num">2.</span>改：为了防止不再发生事故。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">删"不"：为了防止再发生事故</div></div>
</div>
</div>
<div class="check"><b>✔ 达标检查</b> □ 平均数/中位数/众数区别？ □ who/which/that区别？ □ 六种病句类型能判断？</div>
${sg30()}
</div></div>`,

w6: `
<div class="day-page">
<div class="dtop"><div class="dnum">Day 37</div><div class="dinfo"><div>8月6日 周三</div><div style="font-size:12px">数学+物理+英语</div></div></div>
<div class="dbody">
<div class="goal"><b>🎯 今日目标</b>：二次函数基础；物理滑轮；英语过去进行时</div>
<div class="steps">
<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>📖 数学 · 二次函数（2h）</h4>
<p><b>y=ax²+bx+c(a≠0)</b>→图像是抛物线</p>
<p>开口：a>0向上∪，a<0向下∩ | 对称轴：x=-b/(2a) | 顶点：(-b/(2a), (4ac-b²)/(4a))</p>
<p><b>三种形式</b>：一般式|顶点式y=a(x-h)²+k|交点式y=a(x-x₁)(x-x₂)</p>
<p>a,b,c符号：a看开口、b看对称轴（左同右异）、c看y轴交点 <span class="star" style="color:var(--red)">★★★</span></p>
<div class="q-block"><span class="q-num">1.</span>y=x²-4x+3的顶点坐标。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">配方y=(x-2)²-1，顶点(2,-1)；或公式x=2,y=-1</div></div>
<div class="q-block"><span class="q-num">2.</span>y=-2x²的开口方向？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">a=-2<0开口向下</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--orange)"></span>⚡ 物理 · 滑轮（1h）</h4>
<p><b>定滑轮</b>：F=G，只改变方向。实质→等臂杠杆</p>
<p><b>动滑轮</b>：F=G/2，省一半力。实质→L₁=2L₂的杠杆</p>
<p><b>滑轮组</b>：F=G/n (n=承重绳子段数)，s=nh</p>
<div class="q-block"><span class="q-num">1.</span>300N物体用2段绳子动滑轮，需多少力？（不计摩擦）<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">F=G/2=150N</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--green)"></span>🔤 英语 · 过去进行时（1h）</h4>
<p>was/were+doing | 标志：at this time yesterday, at 8 last night, while</p>
<p>⚠️ when+短暂动(一般过去), while+持续动(过去进行)</p>
<div class="q-block"><span class="q-num">1.</span>I ___(read) when he came in.<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">was reading（when+短暂过去→主句过去进行）</div></div>
</div>
</div>
<div class="check"><b>✔ 达标检查</b> □ 二次函数顶点公式？ □ 定滑轮/动滑轮/滑轮组区别？ □ was/were+doing结构？</div>
${sg30()}
</div></div>`,

w8: `
<div class="day-page">
<div class="dtop"><div class="dnum">Day 51</div><div class="dinfo"><div>8月20日 周三</div><div style="font-size:12px">数学+物理+英语</div></div></div>
<div class="dbody">
<div class="goal"><b>🎯 今日目标</b>：圆综合复习；物理电学入门（串联并联）；英语阅读理解技巧</div>
<div class="steps">
<div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>📖 数学 · 圆综合复习（2h）</h4>
<p>核心定理汇总：垂径定理|圆周角定理|切线性质与判定|切线长定理</p>
<p>弧长L=nπr/180 | 扇形面积S=nπr²/360=Lr/2</p>
<div class="q-block"><span class="q-num">1.</span>半径10，圆心角72°，扇形面积？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">S=72π·100/360=20π cm²</div></div>
<div class="q-block"><span class="q-num">2.</span>弦AB=8，半径=5，弦心距？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">√(5²-4²)=3</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--orange)"></span>⚡ 物理 · 电学入门（1h）</h4>
<p>电路组成：电源、用电器、导线、开关</p>
<p><b>串联</b>：电流一条路径（互影响）| <b>并联</b>：多条分支（互不影响）</p>
<p><b>短路</b>：电流不经过用电器直接回电源（危险！）</p>
<p>电流表串联 | 电压表并联</p>
<div class="q-block"><span class="q-num">1.</span>家庭电路用电器是串联还是并联？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">并联（各用电器互不影响，一个坏其他还能用）</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--green)"></span>🔤 英语 · 阅读理解四大题型（1h）</h4>
<p>①细节题→定位原文比对 ②推断题→不选原文直接出现的 ③主旨题→看首尾段 ④词义猜测→看上下文</p>
</div>
</div>
<div class="check"><b>✔ 达标检查</b> □ 串并联电路区别？ □ 阅读四题型技巧记住？</div>
${sg30()}
</div></div>`
};

// Process each week (skip w1 - it has unique manual structure)
for (const wid of ['w2','w3','w4','w5','w6','w7','w8','w9']) {
  let html = fs.readFileSync(`${wid}.html`, 'utf8');
  let added = 0;

  // 1. Add method summaries before gray box word sections
  for (const [day, method] of Object.entries(dayMethod)) {
    const dayIdx = html.indexOf(`<div class="dnum">${day}</div>`);
    if (dayIdx === -1) continue;
    if (html.includes(method.substring(0, 30))) continue;
    
    // Find gray box within this day's section
    const after = html.slice(dayIdx);
    const nextDay = after.indexOf('<div class="dnum">Day ', 50);
    const section = nextDay > 0 ? after.slice(0, nextDay) : after.slice(0, after.indexOf('</body>'));
    const grayPos = section.indexOf('<div style="background:#f0f0f5');
    if (grayPos === -1) continue;
    
    html = html.slice(0, dayIdx + grayPos) + method + '\n' + html.slice(dayIdx + grayPos);
    added++;
  }

  // 2. Add supplementary days for weeks with gaps
  if (suppDays[wid] && !html.includes(suppDays[wid].substring(30, 80))) {
    html = html.replace('</div>\n<script>', `</div>\n\n${suppDays[wid]}\n<script>`);
    added += (suppDays[wid].match(/<div class="day-page">/g) || []).length;
  }

  fs.writeFileSync(`${wid}.html`, html, 'utf8');
  console.log(`${wid}.html: ${added} blocks added, ${html.length}B`);
}
console.log('\nDone!');
