// add_phase3.js - 补齐政治、历史及缺失天数
const fs = require('fs');

// ===== 新Day页面模板 =====

function makeDay(dayNum, date, dayOfWeek, subjects, goal, sections) {
  const dtop = `<div class="day-page">
<div class="dtop"><div class="dnum">Day ${dayNum}</div><div class="dinfo"><div>${date} ${dayOfWeek}</div><div style="font-size:12px">${subjects}</div></div></div>
<div class="dbody">
<div class="goal"><b>🎯 今日目标</b>：${goal}</div>`;
  
  const dclose = `</div></div>`;
  return dtop + '\n' + sections + '\n' + dclose;
}

// ===== 政治内容库 =====
const POLITICS = {
  day31: {
    title: '🏛️ 政治 · 公民权利与义务（1h）',
    content: `<div class="step full"><h4><span class="dot" style="background:#e91e63"></span>讲练（1h）</h4>
<p><b>公民基本权利（宪法第二章）</b>：</p>
<p>①<b>平等权</b>：法律面前人人平等（宪法第33条）</p>
<p>②<b>政治权利</b>：选举权和被选举权（年满18周岁）、言论/出版/集会/结社/游行/示威自由</p>
<p>③<b>人身自由</b>：人身自由不受侵犯、人格尊严不受侵犯、住宅不受侵犯、通信自由和通信秘密受法律保护</p>
<p>④<b>社会经济权利</b>：劳动权、休息权、获得物质帮助权</p>
<p>⑤<b>文化教育权利</b>：受教育权（既是权利也是义务！）</p>
<p><b>公民基本义务</b>：遵守宪法和法律、维护国家统一和民族团结、维护国家安全荣誉和利益、依法服兵役、依法纳税</p>
<div class="q-block"><span class="q-num">1.</span> 受教育为什么既是权利又是义务？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">权利：公民有权获得教育机会，国家提供义务教育保障。义务：适龄儿童和少年必须接受义务教育，这是对国家和社会应尽的责任。</div></div>
<div class="q-block"><span class="q-num">2.</span> 下列哪种行为侵犯了公民的人身自由？A.超市怀疑顾客偷东西强行搜身 B.疫情期间要求居家隔离<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">A。未经法定程序，任何人不得被非法拘禁、搜查。超市无权搜身——侵犯了人格尊严和人身自由。</div></div>
<div class="q-block"><span class="q-num">3.</span> 公民的通信自由和通信秘密受法律保护。什么情况下可以例外？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">因国家安全或追查刑事犯罪的需要，由公安机关或检察机关依法定程序对通信进行检查。除此之外任何组织和个人不得侵犯。</div></div>
</div>`
  },
  day39: {
    title: '🏛️ 政治 · 国家机构与法治（1h）',
    content: `<div class="step full"><h4><span class="dot" style="background:#e91e63"></span>讲练（1h）</h4>
<p><b>国家机构体系</b>：</p>
<p>①<b>全国人民代表大会</b>——最高国家权力机关，行使立法权、决定权、任免权、监督权</p>
<p>②<b>国务院</b>——最高国家行政机关（中央人民政府）</p>
<p>③<b>人民法院</b>——审判机关，独立行使审判权</p>
<p>④<b>人民检察院</b>——法律监督机关</p>
<p><b>法治vs人治</b>：法治——法律面前人人平等，任何人没有超越法律的特权。人治——权力在个人手中，以个人意志代替法律。</p>
<p><b>依法行政</b>：行政机关必须依法行使职权，法无授权不可为，法定职责必须为。</p>
<div class="q-block"><span class="q-num">1.</span> 我国的根本政治制度是什么？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">人民代表大会制度。人民通过选举代表组成全国人大和地方各级人大，行使国家权力。</div></div>
<div class="q-block"><span class="q-num">2.</span> "把权力关进制度的笼子里"体现了什么道理？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">体现了依法治国、权力需要受到制约和监督的道理。任何人都没有超越宪法和法律的特权，必须依法行政、依法用权。</div></div>
<div class="q-block"><span class="q-num">3.</span> 人民法院独立行使审判权意味着什么？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">人民法院在审判案件时不受行政机关、社会团体和个人的干涉，只服从法律。但仍需接受人大监督和人民监督。</div></div>
</div>`
  },
  day52: {
    title: '🏛️ 政治 · 社会主义核心价值观（1h）',
    content: `<div class="step full"><h4><span class="dot" style="background:#e91e63"></span>讲练（1h）</h4>
<p><b>社会主义核心价值观24字（必背！）</b></p>
<p><b>国家层面</b>：<b>富强、民主、文明、和谐</b></p>
<p><b>社会层面</b>：<b>自由、平等、公正、法治</b></p>
<p><b>个人层面</b>：<b>爱国、敬业、诚信、友善</b></p>
<p>记忆技巧：国家→社会→个人，每个层面4个词，共12个词24个字。</p>
<p><b>如何践行</b>：从日常小事做起——①遵守交通规则（法治）②认真学习（敬业）③不说谎骗人（诚信）④帮助同学（友善）⑤升国旗时敬礼（爱国）</p>
<div class="q-block"><span class="q-num">1.</span> 社会主义核心价值观个人层面的内容是什么？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">爱国、敬业、诚信、友善。这是每个人可以直接践行的价值准则。</div></div>
<div class="q-block"><span class="q-num">2.</span> 同学考试作弊，从核心价值观角度怎么分析？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">违背了"诚信"。诚信是个人层面的核心价值，考试作弊是不诚实行为，既欺骗自己也欺骗他人，破坏公平竞争环境。</div></div>
<div class="q-block"><span class="q-num">3.</span> 为什么说"法治"是社会主义核心价值观的重要内容？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">法治是社会层面的价值取向，意味着通过法律治理国家和社会，保障公平正义。没有法治，自由、平等、公正就无从谈起。</div></div>
</div>`
  }
};

// ===== 历史内容库 =====
const HISTORY = {
  day25: {
    title: '📜 历史 · 隋唐时期（1h）',
    content: `<div class="step full"><h4><span class="dot" style="background:#795548"></span>讲练（1h）</h4>
<p><b>隋朝（581-618年）</b>：杨坚建立→统一全国（589年灭陈）→开凿大运河（贯通南北，洛阳为中心）→创立科举制（打破门阀，选拔人才）→因暴政短命而亡</p>
<p><b>唐朝（618-907年）</b>：</p>
<p><b>贞观之治</b>（唐太宗）：虚心纳谏（魏征）、完善科举、轻徭薄赋</p>
<p><b>开元盛世</b>（唐玄宗前期）：唐朝鼎盛期——政治清明、经济繁荣、文化昌盛、万国来朝</p>
<p><b>安史之乱</b>（755年）：唐朝由盛转衰的转折点</p>
<p><b>唐朝文化</b>：①唐诗（李白浪漫主义、杜甫现实主义、白居易通俗易懂）②书法（颜真卿、柳公权）③绘画（吴道子"画圣"）</p>
<div class="q-block"><span class="q-num">1.</span> 科举制是什么时候创立的？有什么意义？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">隋朝创立。意义：打破世家大族对官场的垄断，让平民通过考试进入仕途，促进社会阶层流动，推动教育文化发展。科举制持续了约1300年。</div></div>
<div class="q-block"><span class="q-num">2.</span> 大运河的中心城市是哪里？连接了哪几条水系？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">以洛阳为中心，北达涿郡(今北京)，南至余杭(今杭州)。连接了海河、黄河、淮河、长江、钱塘江五大水系。全长约2700公里。</div></div>
<div class="q-block"><span class="q-num">3.</span> 唐太宗说"以铜为镜，可以正衣冠；以史为镜，可以知兴替"。这句话体现了什么？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">体现了唐太宗以史为鉴、虚心纳谏的治国思想。他善于吸取隋朝灭亡的教训，任用贤臣(如魏征)，开创了贞观之治。</div></div>
</div>`
  },
  day32: {
    title: '📜 历史 · 宋元时期（1h）',
    content: `<div class="step full"><h4><span class="dot" style="background:#795548"></span>讲练（1h）</h4>
<p><b>宋朝（960-1279年）</b>：</p>
<p><b>北宋</b>：赵匡胤陈桥兵变→杯酒释兵权（重文轻武政策）→经济繁荣（交子=世界最早纸币）→王安石变法→靖康之变</p>
<p><b>南宋</b>：偏安江南→岳飞抗金（精忠报国）→经济重心南移完成（"苏湖熟，天下足"）</p>
<p><b>元朝（1271-1368年）</b>：</p>
<p>忽必烈建立→统一中国（第一个由少数民族建立的全国性统一王朝）→行省制度（影响至今）→设立宣政院管理西藏→马可·波罗来华→民族融合</p>
<div class="q-block"><span class="q-num">1.</span> "苏湖熟，天下足"反映了什么经济现象？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">反映南宋时期经济重心南移完成。苏州、湖州一带的粮食产量足以供应全国，南方成为全国的经济中心。原因：北方战乱人口南迁+南方自然条件优越。</div></div>
<div class="q-block"><span class="q-num">2.</span> 交子是什么？为什么出现在北宋？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">交子是世界上最早的纸币，出现于北宋四川地区。原因：北宋商业繁荣，金属货币太重不便携带→商人发明交子→政府正式发行。</div></div>
<div class="q-block"><span class="q-num">3.</span> 元朝的行省制度有什么历史意义？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">行省制度是元朝创立的地方行政管理制度，将全国分为若干个行省进行管理。意义：加强了中央对地方的控制，是中国省制的开端，影响至今。</div></div>
</div>`
  },
  day38: {
    title: '📜 历史 · 明清时期（1h）',
    content: `<div class="step full"><h4><span class="dot" style="background:#795548"></span>讲练（1h）</h4>
<p><b>明朝（1368-1644年）</b>：</p>
<p>朱元璋建立→废除丞相(强化皇权)→设立锦衣卫/东厂(特务统治)→郑和七下西洋(1405-1433年)→实行海禁→戚继光抗倭→李自成起义→灭亡</p>
<p><b>清朝前期（1644-1840年）</b>：</p>
<p>满族入关→康乾盛世(康熙/雍正/乾隆)→设军机处(君主专制达到顶峰)→闭关锁国(仅留广州一口通商)→文字狱(思想控制)→鸦片战争前国力衰退</p>
<div class="q-block"><span class="q-num">1.</span> 郑和下西洋比哥伦布发现美洲早了多少年？有什么意义？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">早了约90年（郑和1405-1433，哥伦布1492）。意义：①世界航海史上的壮举②促进了中国与亚非各国的友好往来③展示了明朝的国力和航海技术。但目的主要是宣扬国威而非经济贸易。</div></div>
<div class="q-block"><span class="q-num">2.</span> 清朝"闭关锁国"政策的主要内容是什么？有何影响？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">内容：严格限制对外贸易，仅留广州一处通商口岸（"一口通商"），由官方特许的"十三行"统一管理。影响：短期维护了统治稳定，长期导致中国与世界隔绝、落后于世界发展潮流，为近代屈辱史埋下伏笔。</div></div>
<div class="q-block"><span class="q-num">3.</span> 明朝废除丞相、清朝设立军机处反映了什么趋势？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">反映了君主专制不断强化的趋势。明朝废除丞相后皇帝直接管理六部，清朝军机处成为皇帝传达命令的工具。皇权达到中国历史的顶峰。</div></div>
</div>`
  },
  day46: {
    title: '📜 历史 · 中国近代史——鸦片战争与列强侵略（1h）',
    content: `<div class="step full"><h4><span class="dot" style="background:#795548"></span>讲练（1h）</h4>
<p><b>第一次鸦片战争（1840-1842年）</b>：</p>
<p>原因：英国向中国倾销鸦片→林则徐虎门销烟→英国以此为借口发动战争</p>
<p>结果：中国战败→签订《南京条约》（割让香港岛、开放五口通商、赔款2100万银元）→中国开始沦为半殖民地半封建社会</p>
<p><b>第二次鸦片战争（1856-1860年）</b>：英法联军火烧圆明园→《北京条约》</p>
<p><b>甲午中日战争（1894-1895年）</b>：北洋水师全军覆没→《马关条约》（割台湾、赔款2亿两白银）→大大加深半殖民地化</p>
<p><b>八国联军侵华（1900年）</b>：《辛丑条约》→赔款4.5亿两白银→中国完全沦为半殖民地半封建社会</p>
<div class="q-block"><span class="q-num">1.</span> 《南京条约》的主要内容是什么？为什么说它是中国近代史上第一个不平等条约？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">内容：割香港岛给英国、赔款2100万银元、开放广州/厦门/福州/宁波/上海五口通商、关税须与英国协商。它是中国近代第一个不平等条约，标志着中国开始沦为半殖民地半封建社会。</div></div>
<div class="q-block"><span class="q-num">2.</span> 林则徐虎门销烟体现了什么精神？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">体现了中华民族反抗外来侵略的坚强意志和爱国主义精神。林则徐是"开眼看世界的第一人"，主张学习西方先进技术。</div></div>
<div class="q-block"><span class="q-num">3.</span> 《马关条约》与《南京条约》相比，对中国危害更大的地方在哪里？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">①割让台湾及附属岛屿，破坏了领土完整②赔款2亿两白银（远超南京条约），加重人民负担③允许日本在中国开设工厂——列强开始对华资本输出，严重阻碍中国民族工业发展。</div></div>
</div>`
  },
  day52_hist: {
    title: '📜 历史 · 世界史——第二次世界大战（1h）',
    content: `<div class="step full"><h4><span class="dot" style="background:#795548"></span>讲练（1h）</h4>
<p><b>二战时间线</b>：1939年德国突袭波兰→1941年日本偷袭珍珠港→1942年《联合国家宣言》（反法西斯同盟形成）→1945年德国投降→日本投降（二战结束）</p>
<p><b>重要会议</b>：</p>
<p>①<b>开罗会议</b>（1943）：中美英→要求日本归还侵占的中国领土（台湾等）</p>
<p>②<b>雅尔塔会议</b>（1945）：美英苏→战后成立联合国、苏联对日作战</p>
<p><b>中国战场</b>：中国人民抗日战争是世界反法西斯战争的重要组成部分，中国是亚洲主战场，为世界反法西斯战争做出了巨大牺牲和贡献。</p>
<div class="q-block"><span class="q-num">1.</span> 第二次世界大战全面爆发的标志是什么？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">1939年9月1日德国突袭波兰，英法对德宣战——二战全面爆发。</div></div>
<div class="q-block"><span class="q-num">2.</span> 反法西斯同盟形成的标志是什么？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">1942年1月，26个国家签署《联合国家宣言》，标志着世界反法西斯同盟正式形成。各国保证全力对轴心国作战，不单独与敌媾和。</div></div>
<div class="q-block"><span class="q-num">3.</span> 为什么说中国的抗日战争是世界反法西斯战争的重要组成部分？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">①中国战场牵制了日本陆军主力，使其无力北攻苏联 ②中国战场是世界反法西斯战争中开始最早、持续时间最长的战场(1931-1945共14年) ③中国人民付出了巨大牺牲(伤亡3500万+) ④中国参加了战后国际秩序的建立(联合国创始国)。</div></div>
</div>`
  }
};

// ===== 新Day内容库 =====
const NEW_DAYS = {
  // W4 Day 24: 化学+物理
  w4_day24: makeDay(24, '7月24日', '周四', '数学+物理+化学',
    '掌握二次函数y=ax²的图像和性质；会用阿基米德原理解决复杂浮力问题；背下前20号元素周期表',
    `<h3 style="color:var(--blue);border-bottom:2px solid var(--blue);padding-bottom:6px;margin:16px 0 12px">📖 数学 · 二次函数y=ax²（1.5h）</h3><div class="step"><h4><span class="dot" style="background:var(--blue)"></span>讲（30min）</h4>
<p><b>⭐ 二次函数定义</b>——形如y=ax²+bx+c（a≠0）的函数。</p>
<p><b>y=ax²的图像特征</b>：①图像是抛物线 ②对称轴是y轴(x=0) ③顶点在原点(0,0) ④a>0开口向上有最低点，a<0开口向下有最高点 ⑤|a|越大开口越窄</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（60min）</h4>
<div class="q-block"><span class="q-num">1.</span> y=2x²的开口方向是？顶点坐标是？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">开口向上(a=2>0)，顶点坐标(0,0)。当x=0时y最小=0。</div></div>
<div class="q-block"><span class="q-num">2.</span> y=-3x²与y=-x²哪个开口更窄？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">y=-3x²更窄。|a|越大开口越窄，|-3|=3>|-1|=1。</div></div>
<div class="q-block"><span class="q-num">3.</span> 当x=2时y=x²=？x=-2时呢？说明了什么？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">都是4。因为(-x)²=x²，所以y轴左右两侧对称点的y值相同→y轴是对称轴。</div></div>
</div>

<h3 style="color:var(--orange);border-bottom:2px solid var(--orange);padding-bottom:6px;margin:16px 0 12px">⚡ 物理 · 浮力综合应用（1h）</h3><div class="step full"><h4><span class="dot" style="background:var(--orange)"></span>讲练（1h）</h4>
<p><b>浮力解题三步法</b>：①确定研究对象（浸在液体中的物体）②判断物体状态（漂浮/悬浮/下沉）③根据状态列方程（漂浮/悬浮：F浮=G物；下沉：F浮=ρ液gV排）</p>
<div class="q-block"><span class="q-num">1.</span> 一木块漂浮在水面上，有2/5的体积露出水面，求木块的密度。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">漂浮→F浮=G→ρ水gV排=ρ木gV木。V排=3V木/5→ρ水×3/5=ρ木→ρ木=0.6g/cm³</div></div>
<div class="q-block"><span class="q-num">2.</span> 一个铁球重10N，浸没在水中时弹簧测力计示数为7N。求铁球受到的浮力和铁球的体积。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">F浮=10-7=3N。F浮=ρ水gV排→3=1000×10×V→V=3×10⁻⁴m³=300cm³</div></div>
</div>

<h3 style="color:#9c27b0;border-bottom:2px solid #9c27b0;padding-bottom:6px;margin:16px 0 12px">🧪 化学 · 元素周期表前20号（1h）</h3><div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>讲练（1h）</h4>
<p><b>背诵口诀</b>：氢氦锂铍硼，碳氮氧氟氖。钠镁铝硅磷，硫氯氩钾钙。</p>
<p>H He Li Be B / C N O F Ne / Na Mg Al Si P / S Cl Ar K Ca</p>
<p><b>记忆技巧</b>：按原子序数1-20逐个背，结合元素名称的偏旁：气态(气字头)→H He N O F Ne Cl Ar；金属(金字旁)→Li Be Na Mg Al K Ca；非金属固态(石字旁)→B C Si P S</p>
<div class="q-block"><span class="q-num">默写</span>：前20号元素符号+名称<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">1H氢 2He氦 3Li锂 4Be铍 5B硼 6C碳 7N氮 8O氧 9F氟 10Ne氖 11Na钠 12Mg镁 13Al铝 14Si硅 15P磷 16S硫 17Cl氯 18Ar氩 19K钾 20Ca钙</div></div>
</div>`),

  // W4 Day 25: 隋唐历史
  w4_day25: makeDay(25, '7月25日', '周五', '数学+历史+化学',
    '掌握二次函数图像的平移规律；了解隋唐时期的关键事件和影响；学会书写简单化学式',
    `<h3 style="color:var(--blue);border-bottom:2px solid var(--blue);padding-bottom:6px;margin:16px 0 12px">📖 数学 · 二次函数图像的平移（1.5h）</h3><div class="step"><h4><span class="dot" style="background:var(--blue)"></span>讲（30min）</h4>
<p><b>平移口诀</b>：<b>左加右减，上加下减</b>（对x操作是反的！）</p>
<p>y=a(x-h)²+k：顶点(h,k)，对称轴x=h。y=ax²向右移h得到y=a(x-h)²。</p>
<p>y=x²+2x+3=(x+1)²+2→顶点(-1,2)。配方法是关键技能！</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（60min）</h4>
<div class="q-block"><span class="q-num">1.</span> y=(x-3)²+2的顶点坐标是？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">顶点(3, 2)，对称轴x=3。开口向上(a=1>0)。</div></div>
<div class="q-block"><span class="q-num">2.</span> 将y=x²向左平移2个单位，再向上平移3个单位，解析式变为？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">y=(x+2)²+3。左移→x变x+2（左加），上移→结尾+3。</div></div>
</div>

<h3 style="color:#795548;border-bottom:2px solid #795548;padding-bottom:6px;margin:16px 0 12px">${HISTORY.day25.title}</h3>${HISTORY.day25.content}

<h3 style="color:#9c27b0;border-bottom:2px solid #9c27b0;padding-bottom:6px;margin:16px 0 12px">🧪 化学 · 化学式书写（0.5h）</h3><div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>讲练（0.5h）</h4>
<p>水H₂O | 二氧化碳CO₂ | 氧气O₂ | 氮气N₂ | 氢气H₂ | 一氧化碳CO | 甲烷CH₄ | 氨气NH₃</p>
<div class="q-block"><span class="q-num">1.</span> 写出下列物质的化学式：水、二氧化碳、氧气<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">水H₂O、二氧化碳CO₂、氧气O₂</div></div>
</div>`),

  // W5 Day 31: 圆+杠杆+政治
  w5_day31: makeDay(31, '7月31日', '周四', '数学+物理+政治',
    '掌握圆的切线性质与判定；理解杠杆平衡条件并能解决实际问题；了解公民基本权利与义务',
    `<h3 style="color:var(--blue);border-bottom:2px solid var(--blue);padding-bottom:6px;margin:16px 0 12px">📖 数学 · 圆——切线（1.5h）</h3><div class="step"><h4><span class="dot" style="background:var(--blue)"></span>讲（30min）</h4>
<p><b>切线判定定理</b>：经过半径的外端点且垂直于这条半径的直线是圆的切线。</p>
<p><b>切线性质</b>：圆的切线垂直于经过切点的半径。</p>
<p><b>切线长定理</b>：从圆外一点引圆的两条切线，它们的切线长相等，且该点与圆心的连线平分两切线的夹角。</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（60min）</h4>
<div class="q-block"><span class="q-num">1.</span> AB是圆O的切线，B是切点，∠AOB=40°，求∠ABO。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">切线⊥半径→∠OBA=90°。△ABO中：∠A=180°-90°-40°=50°</div></div>
<div class="q-block"><span class="q-num">2.</span> 从圆外一点P引两条切线PA、PB，PA=8cm，∠APB=60°，求PB长和OP长。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">PA=PB=8cm(切线长定理)。OP平分∠APB→∠OPA=30°。Rt△OAP中，OA=PA×tan30°=8√3/3≈4.6cm(半径)，OP=PA/cos30°=16/√3≈9.2cm</div></div>
</div>

<h3 style="color:var(--orange);border-bottom:2px solid var(--orange);padding-bottom:6px;margin:16px 0 12px">⚡ 物理 · 杠杆（1h）</h3><div class="step full"><h4><span class="dot" style="background:var(--orange)"></span>讲练（1h）</h4>
<p><b>⭐ 杠杆平衡条件</b>：F₁L₁ = F₂L₂（动力×动力臂 = 阻力×阻力臂）</p>
<p><b>三种杠杆</b>：①省力杠杆：L₁>L₂，费距离(撬棍) ②费力杠杆：L₁<L₂，省距离(镊子) ③等臂杠杆：L₁=L₂，不省力不省距离(天平)</p>
<div class="q-block"><span class="q-num">1.</span> 用一根长1m的撬棍撬石头，支点离石头一端0.2m。在另一端施加100N的力，能撬起多重？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">L₁=1-0.2=0.8m(动力臂)，L₂=0.2m(阻力臂)。F₁L₁=F₂L₂→100×0.8=G×0.2→G=400N≈40kg</div></div>
<div class="q-block"><span class="q-num">2.</span> 筷子是哪种杠杆？为什么？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">费力杠杆。支点在手指处，阻力点在筷子末端(夹食物处)，动力点在中间。动力臂<阻力臂，费力但省距离(手指移动小距离就能让筷子末端移动大距离)。</div></div>
</div>

<h3 style="color:#e91e63;border-bottom:2px solid #e91e63;padding-bottom:6px;margin:16px 0 12px">${POLITICS.day31.title}</h3>${POLITICS.day31.content}`),

  // W5 Day 32: 统计+宋元历史+化学方程式
  w5_day32: makeDay(32, '8月1日', '周五', '数学+历史+化学',
    '会用树状图和列表法求简单事件的概率；了解宋元时期的历史脉络；学会书写和配平化学方程式',
    `<h3 style="color:var(--blue);border-bottom:2px solid var(--blue);padding-bottom:6px;margin:16px 0 12px">📖 数学 · 概率初步（1.5h）</h3><div class="step"><h4><span class="dot" style="background:var(--blue)"></span>讲（30min）</h4>
<p><b>概率定义</b>：P(A) = 事件A可能出现的结果数 / 所有等可能结果的总数</p>
<p><b>求概率两法</b>：①<b>列表法</b>（两步试验，如掷两个骰子）②<b>树状图法</b>（三步及以上试验）</p>
<p>范围：0 ≤ P(A) ≤ 1。P=0不可能事件，P=1必然事件。</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（60min）</h4>
<div class="q-block"><span class="q-num">1.</span> 掷一枚均匀的骰子，求掷出偶数的概率。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">偶数有2、4、6→3个。P=3/6=1/2=0.5</div></div>
<div class="q-block"><span class="q-num">2.</span> 同时掷两枚硬币，求一正一反的概率。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">总结果：正正、正反、反正、反反(4种)。一正一反有2种(正反、反正)→P=2/4=1/2</div></div>
</div>

<h3 style="color:#795548;border-bottom:2px solid #795548;padding-bottom:6px;margin:16px 0 12px">${HISTORY.day32.title}</h3>${HISTORY.day32.content}

<h3 style="color:#9c27b0;border-bottom:2px solid #9c27b0;padding-bottom:6px;margin:16px 0 12px">🧪 化学 · 化学方程式书写（0.5h）</h3><div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>讲练（0.5h）</h4>
<p><b>书写规则</b>：①以客观事实为基础 ②遵循质量守恒定律(配平) ③注明反应条件</p>
<div class="q-block"><span class="q-num">1.</span> 写出氢气燃烧的化学方程式<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">2H₂ + O₂ →(点燃) 2H₂O</div></div>
<div class="q-block"><span class="q-num">2.</span> 写出碳完全燃烧的方程式<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">C + O₂ →(点燃) CO₂</div></div>
</div>`),

  // W6 Day 37: 二次函数与方程+机械能+化学配平
  w6_day37: makeDay(37, '8月6日', '周三', '数学+物理+化学',
    '掌握二次函数与一元二次方程的关系(Δ判别)；理解机械能守恒定律；学会化学方程式配平',
    `<h3 style="color:var(--blue);border-bottom:2px solid var(--blue);padding-bottom:6px;margin:16px 0 12px">📖 数学 · 二次函数与方程（2h）</h3><div class="step"><h4><span class="dot" style="background:var(--blue)"></span>讲（30min）</h4>
<p><b>⭐ Δ判别式</b>——y=ax²+bx+c与x轴交点个数：Δ=b²-4ac</p>
<p>Δ>0→2个交点(两个不等实根)；Δ=0→1个交点(两个相等实根)；Δ<0→无交点(无实根)</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（60min）</h4>
<div class="q-block"><span class="q-num">1.</span> y=x²-4x+3与x轴有几个交点？并求交点坐标。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">Δ=16-12=4>0→2个交点。x²-4x+3=0→(x-1)(x-3)=0→x=1或3。交点(1,0)和(3,0)。</div></div>
<div class="q-block"><span class="q-num">2.</span> y=x²+2x+3与x轴有交点吗？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">Δ=4-12=-8<0→无交点。抛物线全部在x轴上方(a>0且Δ<0)。</div></div>
</div>

<h3 style="color:var(--orange);border-bottom:2px solid var(--orange);padding-bottom:6px;margin:16px 0 12px">⚡ 物理 · 机械能守恒（1h）</h3><div class="step full"><h4><span class="dot" style="background:var(--orange)"></span>讲练（1h）</h4>
<p><b>动能</b>：Ek=½mv²（由质量和速度决定）。<b>重力势能</b>：Ep=mgh（由质量和高度的决定）。<b>机械能</b>=动能+势能。</p>
<p><b>⭐ 机械能守恒</b>：在只有重力（或弹力）做功的情况下，机械能总量保持不变。Ek₁+Ep₁ = Ek₂+Ep₂</p>
<div class="q-block"><span class="q-num">1.</span> 一个质量为2kg的球从10m高处自由下落。求落地瞬间的速度(g=10m/s²)。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">机械能守恒：mgh=½mv²→2×10×10=½×2×v²→v²=200→v≈14.1m/s</div></div>
<div class="q-block"><span class="q-num">2.</span> 为什么人造卫星在近地点速度最大？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">近地点高度最低→重力势能最小→根据机械能守恒→动能最大→速度最大。远地点则相反，势能最大速度最小。</div></div>
</div>

<h3 style="color:#9c27b0;border-bottom:2px solid #9c27b0;padding-bottom:6px;margin:16px 0 12px">🧪 化学 · 化学方程式配平（0.5h）</h3><div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>讲练（0.5h）</h4>
<p><b>配平方法</b>：最小公倍数法→观察法→待定系数法</p>
<div class="q-block"><span class="q-num">1.</span> 配平：P + O₂ → P₂O₅<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">4P + 5O₂ →(点燃) 2P₂O₅（观察法：右边2个P→左边4个P，右边5个O→左边需要5个O₂=10个O→匹配！）</div></div>
<div class="q-block"><span class="q-num">2.</span> 配平：Fe + O₂ → Fe₃O₄<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">3Fe + 2O₂ →(点燃) Fe₃O₄</div></div>
</div>`),

  // W6 Day 38: 英语阅读+明清历史
  w6_day38: makeDay(38, '8月7日', '周四', '英语+历史',
    '掌握英语阅读理解5大题型；了解明清时期的关键史实',
    `<h3 style="color:var(--green);border-bottom:2px solid var(--green);padding-bottom:6px;margin:16px 0 12px">🔤 英语 · 阅读理解题型突破（1.5h）</h3><div class="step"><h4><span class="dot" style="background:var(--green)"></span>讲（30min）</h4>
<p><b>阅读5大题型及技巧</b>：</p>
<p>①<b>事实细节题</b>：在原文中找原句→对比选项，选最接近的</p>
<p>②<b>推理判断题</b>：根据原文信息推断→不能凭空想象→答案一定能在原文找到依据</p>
<p>③<b>词义猜测题</b>：利用上下文+构词法(前缀/后缀/词根)猜词义</p>
<p>④<b>主旨大意题</b>：重点读首段和末段+每段第一句→串起来概括</p>
<p>⑤<b>作者态度题</b>：看形容词和副词的情感色彩(positive/negative/neutral)</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（60min）</h4>
<p>完成2025年泰州中考真题阅读理解C、D两篇。限时：每篇8分钟。做完对答案，统计正确率。</p>
</div>

<h3 style="color:#795548;border-bottom:2px solid #795548;padding-bottom:6px;margin:16px 0 12px">${HISTORY.day38.title}</h3>${HISTORY.day38.content}`),

  // W6 Day 39: 二次函数综合+滑轮+政治
  w6_day39: makeDay(39, '8月8日', '周五', '数学+物理+政治',
    '二次函数综合应用(最值问题)；理解定滑轮和动滑轮的区别；了解国家机构与法治',
    `<h3 style="color:var(--blue);border-bottom:2px solid var(--blue);padding-bottom:6px;margin:16px 0 12px">📖 数学 · 二次函数最值应用题（1.5h）</h3><div class="step"><h4><span class="dot" style="background:var(--blue)"></span>讲（30min）</h4>
<p><b>最值公式</b>：y=ax²+bx+c的顶点x=-b/(2a)，y最大值/最小值=f(-b/(2a))。a>0有最小值，a<0有最大值。</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（60min）</h4>
<div class="q-block"><span class="q-num">1.</span> 某商品售价为x元/件时，利润y=-x²+80x-1200。求利润最大时的售价x。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">x=-b/(2a)=-80/(-2)=40元。最大利润=-40²+80×40-1200=-1600+3200-1200=400元</div></div>
<div class="q-block"><span class="q-num">2.</span> 用40m长的篱笆靠墙围一个矩形菜园（一边靠墙不围），求最大面积。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">设宽为x→长40-2x。面积S=x(40-2x)=-2x²+40x。顶点x=40/4=10→Smax=-200+400=200m²</div></div>
</div>

<h3 style="color:var(--orange);border-bottom:2px solid var(--orange);padding-bottom:6px;margin:16px 0 12px">⚡ 物理 · 滑轮（1h）</h3><div class="step full"><h4><span class="dot" style="background:var(--orange)"></span>讲练（1h）</h4>
<p><b>定滑轮</b>：改变力的方向，不省力（F=G），实质是等臂杠杆。</p>
<p><b>动滑轮</b>：省一半力（F=G/2），但不能改变力的方向，实质是省力杠杆（动力臂是阻力臂的2倍）。</p>
<p><b>滑轮组</b>：既省力又能改变方向。绳子段数n→F=G/n（不计滑轮重和摩擦）</p>
<div class="q-block"><span class="q-num">1.</span> 用动滑轮将200N的重物匀速提升，不计滑轮重和摩擦，拉力多大？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">F=G/2=200/2=100N。若考虑滑轮重20N，则F=(G+G轮)/2=220/2=110N。</div></div>
<div class="q-block"><span class="q-num">2.</span> 滑轮组中绳子承担物重的段数为3，物重600N。不计摩擦和滑轮重，拉力多大？绳子自由端移动3m时，物体升高多少？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">F=G/3=600/3=200N。s=nh→3=3h→h=1m（绳子自由端移动距离是物体升高距离的n倍）。</div></div>
</div>

<h3 style="color:#e91e63;border-bottom:2px solid #e91e63;padding-bottom:6px;margin:16px 0 12px">${POLITICS.day39.title}</h3>${POLITICS.day39.content}`),

  // W7 Day 46: 物理电学+历史近代史
  w7_day46: makeDay(46, '8月15日', '周五', '物理+历史',
    '理解电路基本概念(电流/电压/电阻)；掌握中国近代史·鸦片战争至辛丑条约',
    `<h3 style="color:var(--orange);border-bottom:2px solid var(--orange);padding-bottom:6px;margin:16px 0 12px">⚡ 物理 · 电路基础（1.5h）</h3><div class="step"><h4><span class="dot" style="background:var(--orange)"></span>讲（40min）</h4>
<p><b>电流(I)</b>：电荷的定向移动形成电流。方向：正电荷定向移动的方向(与电子移动方向相反)。单位：安培(A)。</p>
<p><b>电压(U)</b>：使电荷定向移动形成电流的原因。类比：电压=水压，电流=水流。单位：伏特(V)。</p>
<p><b>电阻(R)</b>：导体对电流的阻碍作用。决定因素：材料、长度(越长电阻越大)、横截面积(越粗电阻越小)、温度。单位：欧姆(Ω)。</p>
<p><b>串联电路</b>：电流处处相等(I=I₁=I₂)，总电压=各用电器电压之和(U=U₁+U₂)，总电阻=各电阻之和(R=R₁+R₂)。</p>
<p><b>并联电路</b>：总电流=各支路电流之和(I=I₁+I₂)，各支路电压相等(U=U₁=U₂)，总电阻小于任一支路电阻。</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（50min）</h4>
<div class="q-block"><span class="q-num">1.</span> 两电阻R₁=3Ω和R₂=6Ω串联，总电阻是多少？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">R总=R₁+R₂=3+6=9Ω</div></div>
<div class="q-block"><span class="q-num">2.</span> 上题中两电阻并联，总电阻是多少？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">1/R总=1/3+1/6=3/6=1/2→R总=2Ω（并联总电阻小于任一支路电阻，验证：2<3<6）</div></div>
<div class="q-block"><span class="q-num">3.</span> 家庭电路中各用电器是串联还是并联？为什么？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">并联。原因：①各用电器互不影响(一个关了其他还能用)②各用电器电压相等(都是220V)③如果串联，一个坏了全部断电。</div></div>
</div>

<h3 style="color:#795548;border-bottom:2px solid #795548;padding-bottom:6px;margin:16px 0 12px">${HISTORY.day46.title}</h3>${HISTORY.day46.content}`),

  // W8 Day 51: 一元二次+欧姆定律+化学计算
  w8_day51: makeDay(51, '8月20日', '周三', '数学+物理+化学',
    '掌握因式分解法解一元二次方程；理解欧姆定律I=U/R；学会用化学方程式进行计算',
    `<h3 style="color:var(--blue);border-bottom:2px solid var(--blue);padding-bottom:6px;margin:16px 0 12px">📖 数学 · 一元二次方程——因式分解法（1.5h）</h3><div class="step"><h4><span class="dot" style="background:var(--blue)"></span>讲（30min）</h4>
<p><b>⭐ 因式分解法</b>——把方程化为(x-a)(x-b)=0的形式，则x=a或x=b。</p>
<p><b>十字相乘法</b>：x²+(a+b)x+ab=(x+a)(x+b)。关键：找到两个数，和为一次项系数，积为常数项。</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（60min）</h4>
<div class="q-block"><span class="q-num">1.</span> 解方程：x²+5x+6=0<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">(x+2)(x+3)=0→x=-2或x=-3</div></div>
<div class="q-block"><span class="q-num">2.</span> 解方程：x²-3x-10=0<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">(x-5)(x+2)=0→x=5或x=-2</div></div>
<div class="q-block"><span class="q-num">3.</span> 一个数的平方减去这个数等于6，求这个数。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">x²-x=6→x²-x-6=0→(x-3)(x+2)=0→x=3或x=-2</div></div>
</div>

<h3 style="color:var(--orange);border-bottom:2px solid var(--orange);padding-bottom:6px;margin:16px 0 12px">⚡ 物理 · 欧姆定律（1h）</h3><div class="step full"><h4><span class="dot" style="background:var(--orange)"></span>讲练（1h）</h4>
<p><b>⭐ 欧姆定律</b>：I = U / R（电流=电压/电阻）。三个变形：U=IR、R=U/I。</p>
<p><b>电阻是导体本身的性质</b>——与电压和电流无关！不能说"电阻与电压成正比"。</p>
<div class="q-block"><span class="q-num">1.</span> 一个电阻两端电压为6V时，通过电流为0.5A。电阻多大？电压改为12V时电流多大？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">R=U/I=6/0.5=12Ω（电阻不变）。I=U/R=12/12=1A</div></div>
<div class="q-block"><span class="q-num">2.</span> 两个电阻R₁=6Ω和R₂=3Ω串联接在9V电源上。求总电流和每个电阻两端的电压。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">R总=9Ω，I=U/R总=9/9=1A。U₁=IR₁=1×6=6V，U₂=IR₂=1×3=3V（串联分压，电阻越大分到的电压越多）。</div></div>
</div>

<h3 style="color:#9c27b0;border-bottom:2px solid #9c27b0;padding-bottom:6px;margin:16px 0 12px">🧪 化学 · 化学方程式计算（0.5h）</h3><div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>讲练（0.5h）</h4>
<div class="q-block"><span class="q-num">1.</span> 电解18g水可以得到多少克氢气？(2H₂O→2H₂+O₂)<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">2H₂O→2H₂+O₂。36g水→4g氢气。比例：18/36=x/4→x=2g氢气。</div></div>
</div>`),

  // W8 Day 52: 二次函数复习+世界史+核心价值观
  w8_day52: makeDay(52, '8月21日', '周四', '数学+历史+政治',
    '二次函数全章复习；了解二战重要事件；背诵核心价值观24字',
    `<h3 style="color:var(--blue);border-bottom:2px solid var(--blue);padding-bottom:6px;margin:16px 0 12px">📖 数学 · 二次函数全章复习（2h）</h3><div class="step full"><h4><span class="dot" style="background:var(--blue)"></span>复习（2h）</h4>
<p>1. 默写y=ax²+bx+c的顶点公式和对称轴公式</p>
<p>2. 默写Δ=b²-4ac的判别规则(>0/=0/<0)</p>
<p>3. 做综合练习：求y=x²-4x+3的开口方向、顶点、对称轴、与x轴交点、最小值</p>
<div class="q-block"><span class="q-num">综合</span>：y=x²-4x+3的全部信息<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">开口向上(a=1>0)；顶点(2,-1)(配方→(x-2)²-1)；对称轴x=2；与x轴交点(1,0)和(3,0)[Δ=16-12=4>0]；最小值y=-1(当x=2时)。</div></div>
</div>

<h3 style="color:#795548;border-bottom:2px solid #795548;padding-bottom:6px;margin:16px 0 12px">${HISTORY.day52_hist.title}</h3>${HISTORY.day52_hist.content}

<h3 style="color:#e91e63;border-bottom:2px solid #e91e63;padding-bottom:6px;margin:16px 0 12px">${POLITICS.day52.title}</h3>${POLITICS.day52.content}`)
};

// ===== 注入逻辑 =====
function injectBeforeScript(filePath, content) {
  let html = fs.readFileSync(filePath, 'utf8');
  const scriptPos = html.indexOf('<script>');
  if (scriptPos === -1) {
    console.log(`  ❌ 找不到script标签 in ${filePath}`);
    return;
  }
  // Find the last </div> before script
  const before = html.substring(0, scriptPos);
  const lastCloseDiv = before.lastIndexOf('</div>');
  if (lastCloseDiv === -1) {
    console.log(`  ❌ 找不到注入点 in ${filePath}`);
    return;
  }
  html = html.substring(0, lastCloseDiv) + '\n' + content + '\n' + html.substring(lastCloseDiv);
  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`  ✅ 已注入内容到 ${filePath}`);
}

// ===== 主流程 =====
console.log('Phase 3: 补齐政治、历史及缺失天数\n');

// W4: Day 24, 25
console.log('处理 W4...');
injectBeforeScript('w4.html', NEW_DAYS.w4_day24);
injectBeforeScript('w4.html', NEW_DAYS.w4_day25);

// W5: Day 31, 32
console.log('处理 W5...');
injectBeforeScript('w5.html', NEW_DAYS.w5_day31);
injectBeforeScript('w5.html', NEW_DAYS.w5_day32);

// W6: Day 37, 38, 39
console.log('处理 W6...');
injectBeforeScript('w6.html', NEW_DAYS.w6_day37);
injectBeforeScript('w6.html', NEW_DAYS.w6_day38);
injectBeforeScript('w6.html', NEW_DAYS.w6_day39);

// W7: Day 46
console.log('处理 W7...');
injectBeforeScript('w7.html', NEW_DAYS.w7_day46);

// W8: Day 51, 52
console.log('处理 W8...');
injectBeforeScript('w8.html', NEW_DAYS.w8_day51);
injectBeforeScript('w8.html', NEW_DAYS.w8_day52);

console.log('\n✅ Phase 3 完成！');
