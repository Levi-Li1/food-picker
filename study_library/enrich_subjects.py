"""Enrich physics/chemistry/politics/history with 3-layer teaching structure"""
import json

LIB = 'C:/Users/Tebon/BangMaker/Claw/study_library'

# ═══ PHYSICS (most complete) ═══
with open(f'{LIB}/physics/knowledge.json','r',encoding='utf-8') as f:
    phy = json.load(f)

lectures = {
    '声音的产生与传播':'声音由物体振动产生。振动停止，发声停止。声音需要介质传播(气体/液体/固体)，真空不能传声。声速：固体>液体>气体，15°C空气中340m/s。回声：声音遇到障碍物反射回来，回声测距s=vt/2。',
    '声音的特性':'音调：声音的高低，由振动频率决定。频率越高音调越高(女声>男声)。响度：声音的大小，由振幅决定。振幅越大响度越大。音色：声音的品质，由材料结构决定(不同乐器音色不同)。超声波>20000Hz，次声波<20Hz。',
    '噪声的控制':'噪声从三个方面控制：①声源处(禁止鸣笛/安装消声器)②传播过程中(隔音墙/关门窗)③人耳处(戴耳塞/捂住耳朵)。',
    '光的直线传播':'光在同种均匀介质中沿直线传播。光速c=3×10⁸m/s(真空中最快)。现象：小孔成像(倒立实像)、影子的形成、日食月食。激光准直利用光的直线传播。',
    '光的反射定律':'反射光线、入射光线、法线在同一平面内(三线共面)；反射光线和入射光线分居法线两侧(两线分居)；反射角等于入射角(两角相等)。光路可逆。镜面反射(光滑表面)→平行光反射后仍平行；漫反射(粗糙表面)→平行光反射向各个方向。两者都遵守反射定律。',
    '凸透镜成像规律':'凸透镜：中间厚边缘薄，对光有会聚作用。成像5种情况：①u>2f→倒立缩小实像(照相机)②u=2f→倒立等大实像(测焦距)③f<u<2f→倒立放大实像(投影仪)④u=f→不成像(平行光)⑤u<f→正立放大虚像(放大镜)。记忆口诀：一倍焦距分虚实，二倍焦距分大小。',
    '二力平衡':'平衡状态：静止或匀速直线运动。二力平衡条件：同体(同一物体)+等大(大小相等)+反向(方向相反)+共线(作用在同一直线上)。与相互作用力的区别：二力平衡作用在同一物体上，相互作用力作用在两个不同物体上。',
    '压强':'固体压强P=F/S(单位Pa)。增大压强：增大压力或减小受力面积(刀刃/针尖)。减小压强：减小压力或增大受力面积(坦克履带/书包宽背带)。液体压强P=ρgh(与深度/密度有关，与容器形状无关)。大气压强：1标准大气压=1.013×10⁵Pa=760mmHg。',
    '浮力':'浮力方向竖直向上。阿基米德原理：F浮=G排=ρ液gV排。沉浮条件：F浮>G(上浮→最终漂浮F浮=G)；F浮=G(悬浮/漂浮)；F浮<G(下沉)。轮船从江到海：ρ液增大→V排减小→船浮起一些。潜水艇：改变自身重力实现浮沉。',
    '欧姆定律':'I=U/R(电流=电压/电阻)。串联电路：I=I₁=I₂，U=U₁+U₂，R=R₁+R₂。并联电路：I=I₁+I₂，U=U₁=U₂，1/R=1/R₁+1/R₂。伏安法测电阻原理：R=U/I。',
    '电功率':'P=UI(功率=电压×电流)，单位瓦特W。额定功率：用电器正常工作时消耗的功率。实际功率：实际电压下消耗的功率。P=I²R=U²/R(纯电阻电路)。焦耳定律：Q=I²Rt(电流通过导体产生的热量)。'
}

for chapter in phy['chapters']:
    for topic in chapter['topics']:
        if topic['name'] in lectures:
            topic['lecture'] = lectures[topic['name']]
            topic['practice'] = [f'{topic["name"]}基础练习题：判断对错×5', f'{topic["name"]}计算题×3']
            topic['exam_practice'] = [f'【泰州中考真题】{topic["name"]}相关题目']
            topic['method'] = f'{topic["name"]}解题方法和记忆口诀'

with open(f'{LIB}/physics/knowledge.json','w',encoding='utf-8') as f:
    json.dump(phy, f, ensure_ascii=False, indent=2)
print(f'Physics: enriched {len(lectures)} topics')

# ═══ CHEMISTRY ═══
with open(f'{LIB}/chemistry/knowledge.json','r',encoding='utf-8') as f:
    chem = json.load(f)

chem_lectures = {
    '物理变化与化学变化':'物理变化：没有新物质生成的变化(水结冰/铁制成钉/石蜡熔化)。化学变化：有新物质生成的变化(蜡烛燃烧/铁生锈/食物腐败)。判断依据：是否有新物质(不是看现象！)。化学变化常伴随发光放热变色产生气体沉淀，但有这些现象不一定都是化学变化(如灯泡发光是物理变化)。',
    '元素与原子':'元素：具有相同质子数的一类原子总称。地壳含量前四：O>Si>Al>Fe。前20号元素符号必须会背(H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca)。原子结构：原子核(质子+中子)+核外电子。原子序数=质子数=核外电子数。最外层电子数决定化学性质。',
    '化合价与化学式':'化合价口诀：一价钾钠银氢铵，二价氧钙钡镁锌，三价铝四硅五价磷，二三铁二四碳二四硫，铜汞正二最常见。化学式写法：正价前负价后，交换价数做角标，化简约分。化合物中各元素化合价代数和为0。',
    '质量守恒定律':'参加化学反应的各物质质量总和=反应后生成的各物质质量总和。实质：化学反应中原子种类不变、数目不变、质量不变(三不变)。解释：镁带燃烧变重(有O₂参与反应)，蜡烛燃烧变轻(生成CO₂/H₂O跑掉)。',
    '化学方程式':'书写步骤：写(写出反应物生成物化学式)→配(配平，最小公倍数法/奇数配偶法)→注(标注反应条件△/点燃/催化剂/MnO₂，标注↑气体↓沉淀)。等号两边各原子种类和数目相等。',
    '化学反应类型':'化合反应：A+B→AB(多变一)。分解反应：AB→A+B(一变多)。置换反应：A+BC→AC+B(单质+化合物→新单质+新化合物)。复分解反应：AB+CD→AD+CB(双交换，价不变)。复分解反应发生条件：有沉淀/气体/水生成。',
    '空气与氧气':'空气中N₂约占78%，O₂约占21%，稀有气体0.94%，CO₂0.03%。O₂化学性质：支持燃烧(助燃性)，供给呼吸。C+O₂→点燃→CO₂(白光)，S+O₂→点燃→SO₂(蓝紫色火焰)，3Fe+2O₂→点燃→Fe₃O₄(火星四射)。',
    '水':'电解水正极产生O₂，负极产生H₂(正氧负氢，体积比1:2)。水的净化：沉淀→过滤→吸附(活性炭)→蒸馏。硬水：含较多可溶性钙镁化合物(肥皂水泡沫少)，软水：不含或含较少(泡沫多)。'
}

for ch in chem['chapters']:
    for t in ch['topics']:
        if t['name'] in chem_lectures:
            t['lecture'] = chem_lectures[t['name']]
            t['practice'] = [f'{t["name"]}填空题×5', f'{t["name"]}选择题×3']
            t['exam_practice'] = [f'【泰州中考真题】{t["name"]}相关题目']
            t['method'] = f'{t["name"]}记忆方法和解题技巧'

with open(f'{LIB}/chemistry/knowledge.json','w',encoding='utf-8') as f:
    json.dump(chem, f, ensure_ascii=False, indent=2)
print(f'Chemistry: enriched {len(chem_lectures)} topics')

# ═══ POLITICS ═══
with open(f'{LIB}/politics/knowledge.json','r',encoding='utf-8') as f:
    pol = json.load(f)

pol_lectures = {
    '法律基础':'法律是由国家制定或认可、靠国家强制力保证实施、对全体社会成员具有普遍约束力的行为规范。未成年人六道防线：家庭保护→学校保护→社会保护→网络保护→政府保护→司法保护(由近到远)。依法办事：守法/用法/维权。',
    '宪法与公民权利':'宪法是国家的根本法(最高法律效力)。公民基本权利：平等权/政治权利和自由/人身自由/社会经济权利/文化教育权利。公民基本义务：遵守宪法和法律/维护国家统一和民族团结/依法纳税/受教育。权利和义务的关系：没有无义务的权利，也没有无权利的义务。',
    '国家机构':'全国人民代表大会：最高国家权力机关。国务院：最高国家行政机关。监察委员会：国家监察机关。人民法院：国家审判机关。人民检察院：国家法律监督机关。它们都由人大产生，对人大负责，受人大监督。',
    '改革开放':'改革开放是强国之路。1978年十一届三中全会作出改革开放的决策。经济体制改革：农村→家庭联产承包责任制，城市→国有企业改革。对外开放格局：经济特区→沿海开放城市→沿海经济开放区→内地。共同富裕是社会主义的根本原则(不是同步富裕)。',
    '文化与精神':'中华文化的特点：源远流长、博大精深。文化自信：对自身文化生命力的坚定信念。民族精神的核心：爱国主义(团结统一/爱好和平/勤劳勇敢/自强不息)。社会主义核心价值观：国家层面(富强民主文明和谐)、社会层面(自由平等公正法治)、个人层面(爱国敬业诚信友善)。'
}

for ch in pol['chapters']:
    for t in ch['topics']:
        if t['name'] in pol_lectures:
            t['lecture'] = pol_lectures[t['name']]
            t['practice'] = [f'{t["name"]}简答题×3', f'{t["name"]}选择题×5']
            t['exam_practice'] = [f'【泰州中考】{t["name"]}材料分析题']
            t['method'] = f'{t["name"]}开卷答题核心考点'

with open(f'{LIB}/politics/knowledge.json','w',encoding='utf-8') as f:
    json.dump(pol, f, ensure_ascii=False, indent=2)
print(f'Politics: enriched {len(pol_lectures)} topics')

# ═══ HISTORY ═══
with open(f'{LIB}/history/knowledge.json','r',encoding='utf-8') as f:
    his = json.load(f)

his_lectures = {
    '秦汉时期':'公元前221年秦始皇统一六国，建立中国历史上第一个统一的中央集权国家。秦朝推行郡县制，统一文字(小篆)、货币(圆形方孔钱)、度量衡。汉武帝采纳董仲舒建议"罢黜百家，独尊儒术"。张骞出使西域开辟丝绸之路。东汉蔡伦改进造纸术。',
    '隋唐时期':'隋朝开创科举制，修建大运河(促进南北经济交流)。唐朝是中国古代最强盛的朝代之一。唐太宗李世民开创"贞观之治"，唐玄宗前期达到"开元盛世"。文成公主入藏促进汉藏友好。鉴真东渡日本传播佛教文化。',
    '列强侵略与民族危机':'1840年鸦片战争→中国战败签订《南京条约》(割香港岛/赔款2100万银元/开放五口通商)。1894年甲午中日战争→《马关条约》(割台湾/赔款2亿两/允许日本在通商口岸开设工厂)。1900年八国联军侵华→《辛丑条约》(赔款4.5亿两/划定东交民巷为使馆界)。中国逐步沦为半殖民地半封建社会。',
    '新民主主义革命':'1919五四运动是新民主主义革命的开端(彻底反帝反封建)。1921中共一大在上海召开，标志着中国共产党诞生。1927南昌起义打响了武装反抗国民党反动统治的第一枪。1934-1936红军长征，遵义会议确立毛泽东的领导地位，是党的历史上生死攸关的转折点。1949新中国成立。',
    '两次世界大战':'第一次世界大战(1914-1918)：同盟国vs协约国，战后建立凡尔赛-华盛顿体系。第二次世界大战(1939-1945)：法西斯轴心国vs反法西斯联盟。雅尔塔会议决定战后成立联合国。冷战(1947-1991)：杜鲁门主义/马歇尔计划/北约vs华约。1991年苏联解体，世界格局向多极化发展。'
}

for ch in his['chapters']:
    for t in ch['topics']:
        if t['name'] in his_lectures:
            t['lecture'] = his_lectures[t['name']]
            t['practice'] = [f'{t["name"]}填空题×5', f'{t["name"]}时间排序题×3']
            t['exam_practice'] = [f'【泰州中考】{t["name"]}材料解析题']
            t['method'] = f'{t["name"]}大事年表记忆法'

with open(f'{LIB}/history/knowledge.json','w',encoding='utf-8') as f:
    json.dump(his, f, ensure_ascii=False, indent=2)
print(f'History: enriched {len(his_lectures)} topics')

print('\nAll 4 subject databases enriched with lecture/practice/exam/method structure!')
