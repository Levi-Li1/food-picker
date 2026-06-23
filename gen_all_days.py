"""Generate all 28 missing day templates for w4-w8 and insert into guct.html."""
import re

WORD30 = '<p style="margin:10px 0"><b>今日30词</b>（点击 ▶ 按钮听发音）</p>\n'

H3_M = 'style="color:var(--blue);border-bottom:2px solid var(--blue);padding-bottom:6px;margin:16px 0 12px"'
H3_P = 'style="color:var(--orange);border-bottom:2px solid var(--orange);padding-bottom:6px;margin:20px 0 12px"'
H3_E = 'style="color:var(--green);border-bottom:2px solid var(--green);padding-bottom:6px;margin:20px 0 12px"'
H3_C = 'style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:20px 0 12px"'
H3_CH = 'style="color:#9c27b0;border-bottom:2px solid #9c27b0;padding-bottom:6px;margin:20px 0 12px"'
H3_POL = 'style="color:var(--teal);border-bottom:2px solid var(--teal);padding-bottom:6px;margin:20px 0 12px"'
H3_HIS = 'style="color:#e91e63;border-bottom:2px solid #e91e63;padding-bottom:6px;margin:20px 0 12px"'

B='background:var(--blue)'; O='background:var(--orange)'; G='background:var(--green)'
P='background:var(--purple)'; R='background:var(--red)'

def step(title, dot, content, full=False):
    c = 'step full' if full else 'step'
    return f'<div class="{c}"><h4><span class="dot" style="{dot}"></span>{title}</h4>{content}</div>'

def qn(n,t,a): return f'<div class="q-block"><span class="q-num">{n}.</span><span class="question">{t}</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">{a}</div></div>'

def formula(eq,m=''): return f'<div class="formula"><div class="eq">{eq}</div>'+ (f'<div class="meaning">{m}</div>' if m else '')+'</div>'

def errbox(t): return f'<div class="err-box"><b>❗ 注意</b>：{t}</div>'

def h3(clr,ico,txt): return f'<h3 {clr}>{ico} {txt}</h3>'

def make_day(num, date, subs, goal, sections, check):
    parts = [f'<div class="day-page">',
             f'<div class="dtop"><div class="dnum">Day {num}</div><div class="dinfo"><div>{date}</div><div style="font-size:12px">{subs}</div></div></div>',
             f'<div class="dbody">',
             f'<div class="goal"><b>🎯 今日目标</b>：{goal}</div>']
    parts.extend(sections)
    parts.append(f'<div class="check"><b>✔ 今日达标检查</b>（睡前逐条确认）：<br>{check}</div>')
    parts.append('</div></div>')
    return '\n'.join(parts)

all_days = []

# ═══════════ WEEK 4: Days 23-28 ═══════════

# Day 23
all_days.append(make_day(23,'7月23日 周三','数学+物理+化学',
    '四边形综合证明完全掌握；理解空气组成与氧气性质；掌握分子原子概念',
    [h3(H3_M,'📖','数学 · 四边形综合证明（2h）')+
     step('讲（40min）',B,'<p><b>矩形判定</b>：①有三个角是直角 ②对角线相等的平行四边形 ③有一个角是直角的平行四边形</p><p><b>菱形判定</b>：①四边相等 ②对角线互相垂直的平行四边形 ③有一组邻边相等的平行四边形</p><p><b>正方形判定</b>：既是矩形又是菱形</p><p><b>梯形中位线</b>：MN=(上底+下底)/2</p>'+errbox('四边形证明题的万能思路：先证平行四边形，再加条件证特殊四边形'),False)+
        qn('1','矩形ABCD中AB=6,BC=8,对角线AC=?','AC=10（勾股定理）')+qn('2','梯形中AD∥BC,AD=5,BC=13,中位线=?','(5+13)/2=9')+qn('3','菱形对角线8和6,求边长','√(4²+3²)=5')+qn('4','证明：对角线相等的平行四边形是矩形','对角线相等→四个三角形全等→四个角相等→各90°→矩形'),False)+     ]]),False)+
     step('固（20min）',G,'<p>四边形家族树：四边形→平行四边形（两组对边平行）→矩形/菱形/正方形</p>',True)+
     step('结（10min）',P,'<p>📔 默写四边形所有判定方法 📔 画四边形家族树</p>',True),

     h3(H3_P,'⚡','物理 · 透镜成像规律复习（1h）')+
     step('讲（25min）',O,'<p><b>凸透镜成像规律口诀</b>：一倍焦距分虚实，二倍焦距分大小。物近像远像变大。</p><p>u>2f：倒立缩小实像（照相机）| f<u<2f：倒立放大实像（投影仪）| u<f：正立放大虚像（放大镜）</p><p><b>近视眼与远视眼</b>：近视用凹透镜（先发散），远视用凸透镜（先会聚）</p>',False)+
        qn('1','物体在2f处，像的性质？','倒立等大实像，像距=2f')+qn('2','放大镜是利用什么原理？','u<f时成正立放大虚像')+qn('3','近视眼镜是什么透镜？为什么？','凹透镜。近视眼晶状体太凸→像在视网膜前→用凹透镜先发散。'),False)+     ]]),False)+
     step('结（5min）',P,'<p>📔 默写凸透镜成像规律表格</p>',True),

     h3(H3_CH,'🧪','化学 · 空气组成+氧气（1h）')+
     step('讲（25min）',P,'<p><b>空气组成</b>：N₂78%, O₂21%, 稀有气体0.94%, CO₂0.03%</p><p><b>氧气的化学性质</b>：①C+O₂→CO₂（白光）②S+O₂→SO₂（蓝紫火焰）③3Fe+2O₂→Fe₃O₄（火星四射）</p><p><b>化合反应</b>：多种→一种（多变一）</p>',False)+
        qn('1','空气中含量最多的气体？','N₂(78%)')+qn('2','铁丝在氧气中燃烧的现象？','火星四射，生成黑色固体Fe₃O₄')+qn('3','木炭在氧气中燃烧生成什么？','CO₂（使石灰水变浑浊）'),False)+     ]]),False)+
     step('结（5min）',P,'<p>📔 默写3个燃烧反应方程式</p>',True),
    ],
    '□ 四边形判定全默写？ □ 凸透镜成像表画出？ □ 3个燃烧方程式写对？'
))

# Day 24
all_days.append(make_day(24,'7月24日 周四','数学+化学+英语',
    '梯形中位线应用熟练；掌握氧气制取实验；背30词；定语从句',
    [h3(H3_M,'📖','数学 · 梯形中位线+几何综合（2h）')+
     step('讲（40min）',B,'<p><b>梯形中位线</b>=(上底+下底)/2，平行于两底。</p><p><b>等腰梯形</b>：两腰相等，同底角相等，对角线相等。</p><p><b>几何辅助线技巧</b>：①作高线（化梯形为矩形+RT△）②平移腰（化梯形为平行四边形）③延长两腰交于一点</p>',False)+
        qn('1','梯形AD∥BC,AD=4,BC=10,中位线=?','7')+qn('2','等腰梯形∠B=60°,高3√3,AB=?','AB=3√3/sin60°=6')+qn('3','梯形中位线长8,下底12,上底=?','(x+12)/2=8→x=4'),False)+     ]]),False)+
     step('固（20min）',G,'<p>辅助线四法：作高、平移腰、平移对角线、延长两腰</p>',True)+
     step('结（10min）',P,'<p>📔 画四种辅助线方法图</p>',True),

     h3(H3_CH,'🧪','化学 · 氧气的制取（1h）')+
     step('讲（25min）',P,'<p><b>实验室制O₂三种方法</b>：①2KMnO₄→△→K₂MnO₄+MnO₂+O₂↑ ②2KClO₃→MnO₂△→2KCl+3O₂↑ ③2H₂O₂→MnO₂→2H₂O+O₂↑</p><p><b>收集方法</b>：排水法（O₂不易溶于水）/向上排空气法</p><p><b>催化剂</b>：一变（改变化学反应速率）二不变（质量和化学性质）</p>',False)+
        qn('1','KMnO₄制O₂试管口为何塞棉花？','防止粉末进入导管')+qn('2','催化剂的特点？','一变二不变')+qn('3','如何检验O₂已收集满？','带火星木条放在瓶口，复燃则满'),False)+     ]]),False)+
     step('结（5min）',P,'<p>📔 默写三种制O₂方程式</p>',True),

     h3(H3_E,'🔤','英语 · 定语从句+词汇91-120（1h）')+
     step('讲（15min）',G,'<p><b>定语从句</b>：修饰名词/代词的从句。who(人/主语) whom(人/宾语) which(物) that(人或物)</p><p><b>只用that</b>：①最高级 ②序数词 ③不定代词 ④人+物</p>',False)+
     step('练（25min）',O,
         qn('1','The girl ___ is singing is my sister.(who/which)','who')+
         qn('2','This is the best book ___ I have read.(that/which)','that(最高级)')+
         qn('3','I like books ___ are interesting.(that/who)','that/which')+
         qn('4','He is the only person ___ can help.(that/who)','that(only修饰)'),False)+
     step('固（5min）',G,'<p>关系词口诀：人who物which,模糊就用that</p>',True)+
     step('结（5min）',P,'<p>📔 用who/which/that各造一句</p>',True)+WORD30,
    ],
    '□ 梯形辅助线四种都会？ □ 制O₂三法默写全？ □ 定语从句关系词选对？'
))

# Day 25
all_days.append(make_day(25,'7月25日 周五','数学+物理+化学',
    '几何证明综合训练>80%；光的色散+不可见光；分子与原子',
    [h3(H3_M,'📖','数学 · 几何证明综合（2h）')+
     step('讲（40min）',B,'<p><b>几何证明通用步骤</b>：①读题圈条件 ②找隐藏条件(公共边/对顶角/中点→等边) ③选判定定理 ④按格式书写</p><p><b>常见隐藏条件</b>：公共边/公共角/对顶角/中点/角平分线/垂直→90°</p>'+errbox('SSA不能判定全等！证明时必须写出判定依据'),False)+
     step('练（60min）',O,
         qn('1','△ABC中AB=AC,BD⊥AC,CE⊥AB。证BD=CE','△ABD≌△ACE(AAS)→BD=CE')+
         qn('2','平行四边形ABCD,AC=BD。证矩形','对角线相等→矩形')+
         qn('3','梯形ABCD中AD∥BC,∠B=∠C。证等腰梯形','作高证全等→AB=DC'),False)+
     step('固（20min）',G,'<p>证明书写规范：在△...和△...中→列三个条件→∴△≌△(判定法)</p>',True)+
     step('结（10min）',P,'<p>📔 整理本周几何错题 📔 写出最易犯的3个错误</p>',True),

     h3(H3_P,'⚡','物理 · 光现象综合复习（1h）')+
     step('讲（25min）',O,'<p><b>光现象五部分</b>：①直线传播(影子/日食/小孔成像) ②反射(三线共面/两线分居/两角相等) ③平面镜(正立等大虚像/像距=物距) ④折射(空气→水:靠近法线) ⑤色散(白光→七色光/RGB三原色)</p>',False)+
        qn('1','为什么看水中鱼比实际位置浅？','水→空气折射，虚像偏上')+qn('2','红外线和紫外线各有什么应用？','红外:遥控器/夜视 紫外:验钞/杀菌'),False)+     ]),False)+
     step('结（5min）',P,'<p>📔 画光现象全章思维导图</p>',True),

     h3(H3_CH,'🧪','化学 · 分子与原子（1h）')+
     step('讲（25min）',P,'<p><b>分子</b>：保持化学性质的最小粒子。<b>原子</b>：化学变化中的最小粒子。</p><p>化学变化实质：分子分解→原子重新组合→新分子</p>'+errbox('分子可分、原子不可分——仅限化学变化中！'),False)+
        qn('1','闻到花香说明什么？','分子在不断运动')+qn('2','水蒸发和水电解的本质区别？','蒸发:物理变化,分子不变;电解:化学变化,分子分解')+qn('3','化学变化中分子和原子谁可分？','分子可分,原子不可分'),False)+     ]),False)+
     step('结（5min）',P,'<p>📔 画水电解微观示意图</p>',True),
    ],
    '□ 几何证明格式规范？ □ 光现象五点归纳完？ □ 分子原子区别说清？'
))

# Day 26
all_days.append(make_day(26,'7月26日 周六','数学+化学+英语',
    '一次函数与几何结合；元素符号全默写；完形填空专项',
    [h3(H3_M,'📖','数学 · 一次函数与几何（2h）')+
     step('讲（40min）',B,'<p><b>一次函数y=kx+b</b>：k>0增,k<0减。b是y轴截距。</p><p><b>与坐标轴围成面积</b>：与x轴交(-b/k,0),与y轴交(0,b)→S=|b²/(2k)|</p><p><b>两直线关系</b>：平行→k₁=k₂;垂直→k₁·k₂=-1</p>',False)+
        qn('1','y=2x+1与x轴交点?','(-1/2,0)')+qn('2','y=2x+1与两轴围成面积?','S=|1/(2×2)|=1/4')+qn('3','y=-x+3与y=2x-3交点?','(2,1)'),False)+     ]),False)+
     step('固（20min）',G,'<p>函数解题核心：画草图分析</p>',True)+
     step('结（10min）',P,'<p>📔 总结一次函数所有公式</p>',True),

     h3(H3_CH,'🧪','化学 · 元素与元素符号（1h）')+
     step('讲（25min）',P,'<p><b>元素</b>：具有相同质子数的一类原子。<b>地壳含量前五</b>:O>Si>Al>Fe>Ca</p><p><b>前20号元素</b>:H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca</p><p><b>元素符号意义</b>:①表示一种元素 ②表示该元素的一个原子</p>',False)+
        qn('1','地壳中最多的金属元素?','Al(铝)')+qn('2','Fe表示什么?','铁元素;一个铁原子;铁单质')+qn('3','默写前10号元素符号','H He Li Be B C N O F Ne'),False)+     ]),False)+
     step('结（5min）',P,'<p>📔 默写前20号元素名称和符号</p>',True),

     h3(H3_E,'🔤','英语 · 完形填空+词汇121-150（1h）')+
     step('讲（15min）',G,'<p><b>完形填空三步</b>:①通读全文(不选)②结合上下文选 ③复读检查</p><p><b>高频考点</b>:时态/介词搭配(in on at with)/连词(but and because)/词义辨析(say tell speak talk)</p>',False)+
        qn('1','She is good ___ math.(at/in/on)','at(be good at固定搭配)')+qn('2','He studied hard,___ he passed.(but/so/because)','so(因果关系)')+qn('3','I ___ (go) to park yesterday.(go/went/gone)','went(yesterday→过去时)'),False)+     ]),False)+
     step('固（5min）',G,'<p>高频搭配:be interested in/look forward to/be proud of</p>',True)+
     step('结（5min）',P,'<p>📔 整理10个高频搭配</p>',True)+WORD30,
    ],
    '□ 一次函数面积会算？ □ 前20号元素全默写？ □ 完形三步法掌握？'
))

# Day 27  
all_days.append(make_day(27,'7月27日 周日','数学+物理+英语',
    '第四周数学复习>85%；光现象全章回顾；阅读理解专项',
    [h3(H3_M,'📖','数学 · 错题回炉+周测（2h）')+
     step('讲+练（2h）',B,'<p><b>第四周数学重点</b>:①全等判定(SSS/SAS/ASA/AAS/HL)②勾股定理(a²+b²=c²)③平行四边形→矩形→菱形→正方形 ④梯形中位线 ⑤一次函数与几何</p><p><b>方法</b>:翻出本周所有错题,遮答案重做。两遍以上错的做标记。</p>',True)+
     step('结',P,'<p>📔 记录错题重做正确率 📔 列出3个薄弱点</p>',True),

     h3(H3_P,'⚡','物理 · 光现象全章复习（1h）')+
     step('讲+练（1h）',O,'<p>1.默写光的反射定律 2.默写凸透镜成像规律表 3.区分光的直线传播/反射/折射应用场景 4.解释近视眼和远视眼的矫正原理</p><p>错一处→回头看对应章节</p>',True),

     h3(H3_E,'🔤','英语 · 阅读理解+词汇151-180（1h）')+
     step('讲（15min）',G,'<p><b>阅读四步法</b>:①先读题 ②扫读找关键词 ③精读对比 ④排除干扰</p><p><b>题型</b>:细节题(找原话)/推断题(看逻辑)/主旨题(首尾段)/猜词题(看上下文)</p>',False)+
        qn('1','阅读理解第一步?','先读题目,带问题找答案')+qn('2','主旨题看哪里?','首段和末段')+qn('3','遇到生词怎么办?','根据上下文猜,不停下来查'),False)+     ]),False)+
     step('结（5min）',P,'<p>📔 用四步法做一篇完整阅读</p>',True)+WORD30,
    ],
    '□ 本周错题全部重做？ □ 光现象知识导图画完？ □ 阅读四步法会用？'
))

# Day 28
all_days.append(make_day(28,'7月28日 周一','本周总复习+周测',
    '第四周全科自测；找出薄弱点',
    [h3(H3_M,'📖','数学 · 自测（2h）')+
     step('自测',B,'<p>1.默写五种全等判定 2.画四边形家族树 3.默写勾股定理+常用勾股数 4.默写梯形中位线公式 5.做3道几何证明(计时40min)</p><p>评分:每项20分,<16分重做该章</p>',True),
     h3(H3_P,'⚡','物理 · 自测（0.5h）')+
     step('自测',B,'<p>1.默写凸透镜成像规律表 2.默写光的反射定律 3.解释近视/远视矫正原理</p>',True),
     h3(H3_CH,'🧪','化学 · 自测（0.5h）')+
     step('自测',B,'<p>1.默写空气组成 2.默写三种制O₂方程式 3.默写前20号元素符号 4.区分分子与原子</p>',True),
     h3(H3_E,'🔤','英语 · 自测（1h）')+
     step('自测',B,'<p>1.自测词汇91-180 2.翻译5个定语从句 3.完形填空1篇(15min)</p><p>错词>6个→明天早起过一遍</p>',True),
    ],
    '□ 全科自测完成？ □ 薄弱点已列出？'
))

# ═══════════ WEEK 5: Days 30-35 ═══════════

all_days.append(make_day(30,'7月30日 周三','数学+物理+化学',
    '相似三角形判定掌握；质量密度概念和计算；原子结构与离子',
    [h3(H3_M,'📖','数学 · 相似三角形（2h）')+
     step('讲（40min）',B,'<p><b>相似三角形</b>:三角相等,三边成比例。△ABC∽△DEF</p><p><b>判定(3种)</b>:①两角(AA)②两边夹角(SAS)③三边(SSS)</p><p><b>性质</b>:对应角等/对应边成比例/周长比=相似比/面积比=相似比²</p>'+errbox('SSA不能判定相似！'),False)+
        qn('1','∠A=50°∠B=60°;∠D=50°∠E=60°。相似?','相似(AA)')+qn('2','相似比2的两个三角形面积比?','4(面积比=k²)')+qn('3','AB/DE=BC/EF=2,∠B=∠E。相似?','相似(SAS)'),False)+     ]),False)+
     step('固（20min）',G,'<p>相似判定口诀:两角AA/两边夹角SAS/三边SSS</p>',True)+
     step('结（10min）',P,'<p>📔 默写3种判定+性质</p>',True),

     h3(H3_P,'⚡','物理 · 质量与密度（1h）')+
     step('讲（25min）',O,f'<p><b>质量(m)</b>:物体所含物质的量。单位kg。<b>密度(ρ)</b>:单位体积的质量。{formula("ρ=m/V")}<p>ρ水=1.0×10³kg/m³。密度是物质的特性。</p>',False)+
        qn('1','铁块158g,体积20cm³,密度?','7.9g/cm³')+qn('2','500mL水质量?','500g')+qn('3','质量相同,铁块和棉花谁体积大?','棉花(密度小)'),False)+     ]),False)+
     step('结（5min）',P,'<p>📔 默写密度公式及两种变形</p>',True),

     h3(H3_CH,'🧪','化学 · 原子结构与离子（1h）')+
     step('讲（25min）',P,'<p><b>原子构成</b>:原子核(质子+中子)+电子。<b>核外电子排布</b>:第一层≤2,第二层≤8,最外层≤8</p><p><b>离子</b>:阳离子(失电子,+)如Na⁺;阴离子(得电子,-)如Cl⁻</p>'+errbox('原子不带电(质子数=电子数),离子带电'),False)+
        qn('1','Na⁺有几个电子?(Na原子11个电子)','10个')+qn('2','Cl原子最外层7个电子,容易?','得1个电子→Cl⁻')+qn('3','最外层8电子结构叫什么?','相对稳定结构'),False)+     ]),False)+
     step('结（5min）',P,'<p>📔 画出Na和Cl原子结构图</p>',True),
    ],
    '□ 相似3种判定默全？ □ 密度公式变形都会？ □ Na/Cl原子结构图画对？'
))

# Day 31
all_days.append(make_day(31,'7月31日 周四','数学+化学+政治',
    '相似证明专题；化合价与化学式；公民基本权利',
    [h3(H3_M,'📖','数学 · 相似证明专题（2h）')+
     step('讲（40min）',B,'<p><b>相似模型</b>:①A字型(DE∥BC→△ADE∽△ABC)②X字型(AB∥CD→△AOB∽△COD)③母子型(Rt△斜边上的高)</p><p><b>解题步骤</b>:找相等角→选判定→列比例→求解</p>',False)+
        qn('1','DE∥BC,AD=3,DB=6,AE=4,EC=?','△ADE∽△ABC→3/9=4/(4+EC)→EC=8')+qn('2','AB∥CD,AB=4,CD=6,OA=3,OC=?','4.5')+qn('3','Rt△中CD⊥AB,AC=6,BC=8,CD=?','4.8'),False)+     ]),False)+
     step('固（20min）',G,'<p>三大模型:A字/X字/母子型</p>',True)+
     step('结（10min）',P,'<p>📔 画三种模型图</p>',True),

     h3(H3_CH,'🧪','化学 · 化合价与化学式（1h）')+
     step('讲（25min）',P,'<p><b>化合价口诀</b>:一价钾钠氯氢银,二价氧钙钡镁锌,三铝四硅五价磷</p><p><b>写化学式</b>:正价前负价后,交叉化简。化合物中正负化合价代数和为零</p>',False)+
        qn('1','Al³⁺和O²⁻组成?','Al₂O₃')+qn('2','Fe₂O₃中Fe化合价?','+3(2x+3×(-2)=0)')+qn('3','H₂SO₄中S化合价?','+6'),False)+     ]),False)+
     step('结（5min）',P,'<p>📔 默写化合价口诀</p>',True),

     h3(H3_POL,'🏛️','政治 · 公民基本权利（0.5h）')+
     step('讲（20min）',R,'<p><b>公民基本权利(宪法规定)</b>:①平等权 ②政治权利(选举权/被选举权,18周岁) ③人身自由 ④社会经济权利(劳动/休息/物质帮助) ⑤文化教育权(受教育既是权利也是义务!)</p>'+errbox('权利和义务是统一的'),True)+
     step('固（10min）',G,'<p>宪法是公民权利的保障书</p>',True),
    ],
    '□ 相似三大模型记住？ □ 化合价口诀默全？ □ 五大基本权利说全？'
))

# Day 32
all_days.append(make_day(32,'8月1日 周五','数学+物理+化学',
    '相似应用题；密度测量实验；化学式计算',
    [h3(H3_M,'📖','数学 · 相似应用（2h）')+
     step('讲（40min）',B,'<p><b>实际应用</b>:①测高(影子相似)②测距(河宽)③位似图形(对应点连线交于一点)</p><p><b>位似</b>:两相似图形,对应点连线过同一点且对应边平行</p>',False)+
        qn('1','1.5m人影2m,楼影24m,楼高?','18m')+qn('2','位似比k=2,面积变几倍?','4倍')+qn('3','△ABC∽△DEF,相似比2:3,△ABC周长16,△DEF周长?','24'),False)+     ]),False)+
     step('固（20min）',G,'<p>相似应用:建模型→列比例→解方程</p>',True)+
     step('结（10min）',P,'<p>📔 整理相似应用解题模板</p>',True),

     h3(H3_P,'⚡','物理 · 密度测量实验（1h）')+
     step('讲（25min）',O,'<p><b>测固体密度</b>:①天平测m②量筒加水V₁③放固体后V₂④ρ=m/(V₂-V₁)</p><p><b>测液体密度</b>:①杯+液总m₁②倒入量筒V③剩余杯+液m₂④ρ=(m₁-m₂)/V</p>',False)+
        qn('1','石块54g,水面50→70mL,密度?','2.7g/cm³')+qn('2','先测体积后测质量会?','质量偏大→密度偏大'),False)+     ]),False)+
     step('结（5min）',P,'<p>📔 画测密度实验步骤图</p>',True),

     h3(H3_CH,'🧪','化学 · 有关化学式的计算（1h）')+
     step('讲（25min）',P,'<p><b>相对分子质量</b>:各原子相对原子质量之和。<b>元素质量比</b>:原子个数×原子量之比。<b>质量分数</b>:该元素质量/总质量×100%</p>',False)+
        qn('1','CO₂相对分子质量?','44')+qn('2','CO₂中C:O质量比?','12:32=3:8')+qn('3','NH₄NO₃中N%?','28/80=35%'),False)+     ]),False)+
     step('结（5min）',P,'<p>📔 计算CaCO₃的相对分子质量和各元素质量比</p>',True),
    ],
    '□ 相似应用模板掌握？ □ 密度测量步骤默全？ □ 化式计算三种都会？'
))

# Day 33
all_days.append(make_day(33,'8月2日 周六','数学+物理+英语',
    '位似+图形变换；力的基本概念；词汇+时态复习',
    [h3(H3_M,'📖','数学 · 位似+图形变换（2h）')+
     step('讲（40min）',B,'<p><b>四大变换</b>:①平移(全等/位置变)②旋转(全等/绕点转)③轴对称(全等/关于线对称)④位似(相似/大小可变)</p><p><b>坐标系中位似</b>:(x,y)→(kx,ky)或(-kx,-ky)</p>',False)+
        qn('1','平移/旋转/轴对称共同特点?','形状大小不变(全等变换)')+qn('2','位似比2,点A(1,3)→?','(2,6)或(-2,-6)'),False)+     ]),False)+
     step('固（20min）',G,'<p>平移/旋转/轴对称→全等;位似→相似</p>',True)+
     step('结（10min）',P,'<p>📔 画四种变换示意图</p>',True),

     h3(H3_P,'⚡','物理 · 力（1h）')+
     step('讲（25min）',O,'<p><b>力</b>:物体对物体的作用。三要素:大小/方向/作用点。作用效果:改变运动状态/形变。</p><p><b>重力G=mg</b>(g≈10N/kg)。方向竖直向下。</p>'+errbox('力的作用是相互的！'),False)+
        qn('1','50kg人重力?','500N')+qn('2','力的三要素?','大小/方向/作用点'),False)+     ]),False)+
     step('结（5min）',P,'<p>📔 默写G=mg</p>',True),

     h3(H3_E,'🔤','英语 · 词汇181-210+时态复习（1h）')+
     step('讲（15min）',G,'<p><b>时态公式</b>:一般现在do/does;一般过去did;一般将来will do;现在进行am/is/are doing;现在完成have/has done</p><p><b>时间标志词</b>:yesterday→过去;tomorrow→将来;already→完成;now→进行</p>',False)+
        qn('1','She ___(go) to Beijing last week.','went(过去时)')+qn('2','They ___(study) English for 3 years.','have studied(完成时)')+qn('3','Look!The bus ___(come).','is coming(进行时)'),False)+     ]),False)+
     step('固（5min）',G,'<p>五大时态公式必须烂熟于心</p>',True)+
     step('结（5min）',P,'<p>📔 默写五种时态公式+标志词</p>',True)+WORD30,
    ],
    '□ 四大变换分清？ □ 力的三要素记住？ □ 五种时态区分开？'
))

print(f'Generated {len(all_days)} days')
print('Saving to guct.html...')

# Insert into guct.html
with open('C:/Users/Tebon/BangMaker/Claw/guct.html','r',encoding='utf-8') as f:
    h = f.read()

# w4: after Day 22, before w5 marker
w5 = h.find('<div class="week-marker" id="w5">')
h = h[:w5] + '\n' + '\n'.join(all_days[:6]) + '\n\n' + h[w5:]

# w5: after Day 29, before w6  
w6 = h.find('<div class="week-marker" id="w6">')
h = h[:w6] + '\n' + '\n'.join(all_days[6:12]) + '\n\n' + h[w6:]

# w6: after Day 36, before w7
w7 = h.find('<div class="week-marker" id="w7">')
h = h[:w7] + '\n' + '\n'.join(all_days[12:]) + '\n\n' + h[w7:]

with open('C:/Users/Tebon/BangMaker/Claw/guct.html','w',encoding='utf-8') as f:
    f.write(h)

print(f'guct.html: {len(h)} bytes')
print('Done!')
