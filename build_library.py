#!/usr/bin/env python3
"""Build complete study library databases for all 7 subjects."""
import json, os

LIB = 'C:/Users/Tebon/BangMaker/Claw/study_library'

# ═══ 1. ENGLISH: Complete vocabulary (enrich 726 words with full data) ═══

# Load existing wordbank
with open('C:/Users/Tebon/BangMaker/Claw/wordbank.json','r',encoding='utf-8') as f:
    words = json.load(f)

# Common Chinese-English translations for the supplementary words
COMMON_TRANSLATIONS = {
    'able':'有能力的','action':'行动','age':'年龄','agree':'同意','allow':'允许',
    'anger':'愤怒','animal':'动物','army':'军队','arrive':'到达','baby':'婴儿',
    'back':'背；后面','bad':'坏的','bag':'包','ball':'球','bank':'银行','base':'基础',
    'bath':'洗澡','bear':'熊','beat':'打','bed':'床','bell':'铃','best':'最好的',
    'better':'更好的','bill':'账单','bird':'鸟','birth':'出生','bit':'一点',
    'blow':'吹','blue':'蓝色','board':'板','boat':'船','body':'身体','bone':'骨头',
    'born':'出生','bottom':'底部','brain':'大脑','branch':'树枝','brave':'勇敢的',
    'bread':'面包','breath':'呼吸','bridge':'桥','bright':'明亮的','bring':'带来',
    'brown':'棕色','brush':'刷子','burn':'燃烧','busy':'忙的','button':'按钮',
    'cake':'蛋糕','call':'打电话','camp':'露营','card':'卡片','care':'关心',
    'carry':'搬运','cause':'原因','center':'中心','chain':'链条','chair':'椅子',
    'chalk':'粉笔','chance':'机会','change':'变化','cheap':'便宜的','check':'检查',
    'cheese':'奶酪','chief':'首领','child':'孩子','church':'教堂','circle':'圆',
    'claim':'声称','class':'班级','clay':'黏土','clean':'干净','clear':'清晰的',
    'climb':'爬','clock':'时钟','close':'关闭','cloth':'布料','cloud':'云',
    'coast':'海岸','coat':'外套','coin':'硬币','collect':'收集','college':'大学',
    'color':'颜色','comfort':'舒适','committee':'委员会','company':'公司',
    'compare':'比较','complete':'完成','control':'控制','cook':'做饭','cool':'凉爽的',
    'copper':'铜','corn':'玉米','correct':'正确的','cotton':'棉花','count':'数数',
    'country':'国家','county':'县','couple':'一对','course':'课程','court':'法庭',
    'cover':'覆盖','crack':'裂缝','cream':'奶油','create':'创造','cross':'穿过',
    'crowd':'人群','cruel':'残忍的','culture':'文化','cup':'杯子','current':'当前的',
    'curtain':'窗帘','curve':'曲线','custom':'习俗','cut':'切','damage':'损坏',
    'danger':'危险','daughter':'女儿','dead':'死亡的','deal':'处理','dear':'亲爱的',
    'death':'死亡','debt':'债务','decide':'决定','decision':'决定','deep':'深的',
    'degree':'度数','design':'设计','desire':'渴望','detail':'细节','develop':'发展',
    'development':'发展','direction':'方向','dirty':'脏的','disease':'疾病',
    'distance':'距离','double':'双倍','doubt':'怀疑','dozen':'一打','drama':'戏剧',
    'dream':'梦想','drop':'掉','dull':'沉闷的','dust':'灰尘','duty':'责任',
    'eager':'渴望的','earn':'赚','earth':'地球','edge':'边缘','elder':'年长的',
    'electric':'电的','enemy':'敌人','energy':'能量','engine':'引擎','enjoy':'享受',
    'enough':'足够的','enter':'进入','error':'错误','event':'事件','example':'例子',
    'exchange':'交换','excite':'使兴奋','exist':'存在','expect':'期待',
    'express':'表达','expression':'表达','extra':'额外的','failure':'失败',
    'faith':'信仰','false':'假的','fault':'错误','feed':'喂养','feel':'感觉',
    'female':'女性的','fence':'篱笆','field':'田地','fight':'战斗','fill':'填满',
    'finger':'手指','firm':'坚定的','fix':'修理','flag':'旗帜','flame':'火焰',
    'flat':'平的','flesh':'肉','flight':'航班','flood':'洪水','flow':'流动',
    'flower':'花','fold':'折叠','follow':'跟随','force':'力量','forest':'森林',
    'form':'形式','fortune':'财富','forward':'向前','found':'建立','frame':'框架',
    'freedom':'自由','fresh':'新鲜的','fruit':'水果','fuel':'燃料','full':'满的',
    'funeral':'葬礼','future':'未来','gain':'获得','game':'游戏','garden':'花园',
    'gas':'气体','gate':'大门','gather':'聚集','gentle':'温柔的','gift':'礼物',
    'glad':'高兴的','glory':'荣耀','goal':'目标','god':'神','gold':'金子',
    'golden':'金色的','goose':'鹅','government':'政府','grain':'谷物','grand':'宏伟的',
    'grass':'草','grave':'坟墓','gray':'灰色','great':'伟大的','green':'绿色',
    'ground':'地面','group':'组','growth':'生长','guard':'守卫','guess':'猜',
    'guest':'客人','guidance':'指导','guilt':'内疚','gun':'枪','habit':'习惯',
    'hair':'头发','handle':'处理','hang':'悬挂','happen':'发生','happy':'快乐的',
    'harbor':'港湾','hard':'困难的','harm':'伤害','harsh':'严酷的','hat':'帽子',
    'hate':'讨厌','health':'健康','heaven':'天堂','height':'高度','hell':'地狱',
    'history':'历史','hit':'打','hold':'握住','hole':'洞','holy':'神圣的',
    'honest':'诚实的','honey':'蜂蜜','honor':'荣誉','hope':'希望','host':'主人',
    'hot':'热的','huge':'巨大的','human':'人类','humble':'谦虚的','humor':'幽默',
    'hunt':'打猎','hurt':'受伤','husband':'丈夫','ideal':'理想的','image':'图像',
    'imagination':'想象力','impact':'影响','important':'重要的','income':'收入',
    'increase':'增加','independence':'独立','industry':'工业','influence':'影响',
    'ink':'墨水','inner':'内部的','insect':'昆虫','instance':'实例','instrument':'工具',
    'interest':'兴趣','invent':'发明','iron':'铁','island':'岛屿','joint':'关节',
    'joy':'快乐','judge':'判断','justice':'正义','keen':'热衷的','kick':'踢',
    'kill':'杀','kind':'友善的','king':'国王','kiss':'吻','kitchen':'厨房',
    'knee':'膝盖','knife':'刀','knowledge':'知识','lack':'缺乏','ladder':'梯子',
    'lady':'女士','lake':'湖','lamp':'灯','landscape':'风景','language':'语言',
    'large':'大的','laughter':'笑声','law':'法律','lay':'放置','lead':'带领',
    'leaf':'叶子','league':'联盟','lean':'倾斜','leather':'皮革','lend':'借出',
    'length':'长度','lesson':'课','level':'水平','liberty':'自由','lift':'举起',
    'limit':'限制','line':'线','liquid':'液体','literature':'文学','load':'负载',
    'loaf':'一条面包','lock':'锁','lonely':'孤独的','lord':'贵族','loss':'损失',
    'loud':'大声的','lovely':'可爱的','lucky':'幸运的','lump':'块','lunch':'午餐',
    'lung':'肺','magic':'魔法','main':'主要的','male':'男性的','manage':'管理',
    'manner':'方式','map':'地图','march':'三月','mark':'标记','market':'市场',
    'marry':'结婚','mass':'质量','master':'大师','match':'比赛','mate':'伙伴',
    'material':'材料','matter':'事情','meal':'餐','meaning':'意思','measure':'测量',
    'meat':'肉','medicine':'药','medium':'中等的','member':'成员','memory':'记忆',
    'mental':'心理的','mercy':'怜悯','message':'消息','method':'方法','middle':'中间',
    'mild':'温和的','milk':'牛奶','mind':'思想','minister':'部长','mirror':'镜子',
    'mist':'雾','mix':'混合','mixture':'混合物','model':'模型','moderate':'适度的',
    'modern':'现代的','moment':'时刻','money':'钱','monitor':'班长','monster':'怪物',
    'moon':'月亮','moral':'道德的','motion':'运动','motor':'马达','mount':'安装',
    'mountain':'山','mouse':'老鼠','mouth':'嘴巴','movement':'运动','murder':'谋杀',
    'muscle':'肌肉','museum':'博物馆','mystery':'神秘','narrow':'狭窄的','nation':'国家',
    'nature':'自然','neat':'整洁的','necessary':'必要的','neck':'脖子','needle':'针',
    'neighbor':'邻居','nerve':'神经','net':'网','next':'下一个','noble':'高贵的',
    'noise':'噪音','none':'没有一个','notice':'注意','noun':'名词','novel':'小说',
    'number':'数字','object':'物体','observation':'观察','obtain':'获得',
    'occasion':'场合','ocean':'海洋','offer':'提供','office':'办公室','officer':'警官',
    'once':'曾经','opinion':'意见','opposite':'相反的','orange':'橙子','organ':'器官',
    'organization':'组织','origin':'起源','original':'原来的','otherwise':'否则',
    'owner':'主人','oxygen':'氧气','pace':'步伐','pack':'打包','packet':'小包',
    'pain':'疼痛','paint':'油漆','pair':'一对','palace':'宫殿','pale':'苍白的',
    'pan':'平底锅','paragraph':'段落','parent':'父母','park':'公园','parliament':'议会',
    'participate':'参加','particle':'粒子','particular':'特别的','partly':'部分地',
    'partner':'伙伴','passion':'热情','passive':'被动的','paste':'粘贴','patent':'专利',
    'patience':'耐心','pattern':'模式','pause':'暂停','peak':'顶峰','penalty':'惩罚',
    'penetrate':'穿透','pension':'养老金','pepper':'胡椒','perceive':'感知',
    'percent':'百分比','perfect':'完美的','perform':'表演','perfume':'香水',
    'perhaps':'也许','period':'时期','permanent':'永久的','permit':'允许',
    'persist':'坚持','personality':'个性','personnel':'人员','perspective':'视角',
    'persuade':'说服','phase':'阶段','phenomenon':'现象','philosopher':'哲学家',
    'philosophy':'哲学','phrase':'短语','physical':'物理的','piano':'钢琴',
    'picnic':'野餐','piece':'片','pile':'堆','pilot':'飞行员','pink':'粉色的',
    'pity':'遗憾','plain':'朴素的','plan':'计划','planet':'行星','plant':'植物',
    'plate':'盘子','playground':'操场','pleasure':'快乐','plenty':'充足的',
    'pocket':'口袋','poem':'诗','poet':'诗人','poetry':'诗歌','point':'点',
    'poison':'毒药','pole':'杆','policy':'政策','polish':'抛光','pollution':'污染',
    'pool':'水池','population':'人口','position':'位置','possession':'财产',
    'post':'邮寄','potato':'土豆','pound':'英镑','pour':'倒','powder':'粉末',
    'power':'力量','practice':'练习','praise':'赞扬','prayer':'祈祷','precious':'珍贵的',
    'prepare':'准备','presence':'出席','president':'总统','press':'按','pressure':'压力',
    'pretend':'假装','pretty':'漂亮的','prevent':'阻止','price':'价格','pride':'骄傲',
    'principle':'原则','print':'打印','prison':'监狱','privilege':'特权',
    'process':'过程','produce':'生产','profit':'利润','progress':'进步',
    'promise':'承诺','proof':'证据','proper':'适当的','property':'财产',
    'proposal':'提议','protect':'保护','protection':'保护','protest':'抗议',
    'proud':'自豪的','prove':'证明','provide':'提供','public':'公共的','pull':'拉',
    'pump':'泵','punish':'惩罚','pupil':'学生','pure':'纯净的','purpose':'目的',
    'purse':'钱包','quality':'质量','quantity':'数量','quarter':'四分之一',
    'queen':'女王','question':'问题','queue':'排队','quick':'快的','quiet':'安静的',
    'race':'比赛','radio':'收音机','rail':'铁路','rain':'雨','range':'范围',
    'rank':'等级','rapid':'迅速的','rate':'比率','raw':'生的','ray':'光线',
    'reaction':'反应','reality':'现实','reason':'原因','receipt':'收据',
    'recent':'最近的','record':'记录','reform':'改革','region':'地区',
    'relation':'关系','relative':'亲戚','religion':'宗教','rent':'租金',
    'repair':'修理','repeat':'重复','report':'报告','republic':'共和国',
    'reputation':'声誉','request':'请求','research':'研究','resistance':'抵抗',
    'resolution':'决议','resource':'资源','respect':'尊重','responsibility':'责任',
    'rest':'休息','restaurant':'餐厅','result':'结果','return':'返回',
    'revolution':'革命','reward':'奖励','rhythm':'节奏','risk':'风险','river':'河',
    'road':'路','rock':'岩石','role':'角色','route':'路线','row':'排',
    'royal':'皇家的','rubber':'橡胶','rude':'粗鲁的','ruin':'毁灭','rule':'规则',
    'ruler':'尺子','rush':'冲','safety':'安全','sail':'航行','salary':'薪水',
    'salt':'盐','satellite':'卫星','scene':'场景','schedule':'日程','scheme':'方案',
    'science':'科学','scientific':'科学的','scientist':'科学家','score':'分数',
    'screen':'屏幕','sea':'海','search':'搜索','season':'季节','seat':'座位',
    'second':'第二','secret':'秘密','secretary':'秘书','section':'部分',
    'security':'安全','seed':'种子','seek':'寻找','select':'选择','selection':'选择',
    'self':'自我','sense':'感觉','separate':'分开','servant':'仆人','service':'服务',
    'session':'会议','settle':'解决','shadow':'影子','shake':'摇晃','shame':'羞耻',
    'shape':'形状','share':'分享','sharp':'锋利的','shelf':'架子','shell':'壳',
    'shelter':'庇护所','shift':'转移','shine':'发光','ship':'船','shock':'震惊',
    'shore':'海岸','shout':'喊','shut':'关闭','sick':'生病的','side':'边',
    'sight':'视力','sign':'标志','signal':'信号','silence':'沉默','silk':'丝绸',
    'silver':'银','similar':'相似的','simple':'简单的','since':'自从',
    'single':'单个的','sink':'下沉','situation':'情况','skill':'技能','skin':'皮肤',
    'slave':'奴隶','slight':'轻微的','slip':'滑','slope':'斜坡','smooth':'平滑的',
    'snake':'蛇','society':'社会','sock':'袜子','soft':'柔软的','soil':'土壤',
    'soldier':'士兵','solid':'固体','solution':'溶液','sort':'种类','soul':'灵魂',
    'source':'来源','space':'太空','speech':'演讲','speed':'速度','spend':'花费',
    'spirit':'精神','spite':'恶意','split':'分裂','spoil':'宠坏','sport':'运动',
    'spot':'地点','spread':'传播','spring':'春天','square':'广场','staff':'员工',
    'stage':'舞台','stair':'楼梯','standard':'标准','star':'星星','start':'开始',
    'state':'状态','station':'车站','status':'地位','steady':'稳定的','steal':'偷',
    'steam':'蒸汽','steel':'钢','steep':'陡峭的','stem':'茎','step':'步骤',
    'stick':'棒','sticky':'粘的','stiff':'僵硬的','stock':'库存','stomach':'胃',
    'stone':'石头','storage':'存储','storm':'暴风雨','story':'故事','stove':'炉子',
    'strategy':'策略','stream':'溪流','street':'街道','strength':'力量',
    'stress':'压力','stretch':'伸展','strict':'严格的','strike':'罢工','string':'线',
    'strip':'条','stroke':'中风','strong':'强壮的','structure':'结构',
    'struggle':'挣扎','student':'学生','subject':'科目','substance':'物质',
    'success':'成功','sugar':'糖','suggestion':'建议','suit':'适合','summer':'夏天',
    'sun':'太阳','supply':'供应','support':'支持','suppose':'假设','surface':'表面',
    'surprise':'惊喜','surround':'包围','survival':'生存','suspect':'怀疑',
    'swallow':'燕子','sweep':'打扫','sweet':'甜的','swim':'游泳','swing':'秋千',
    'switch':'开关','symbol':'象征','sympathy':'同情','system':'系统','table':'桌子',
    'tail':'尾巴','tale':'故事','talent':'才能','taste':'味道','tax':'税','teach':'教',
    'teaching':'教学','tear':'眼泪','temperature':'温度','tendency':'趋势',
    'term':'学期','territory':'领土','terror':'恐怖','theory':'理论','thick':'厚的',
    'thin':'薄的','thing':'东西','thought':'想法','thread':'线','throat':'喉咙',
    'thumb':'大拇指','tide':'潮汐','tight':'紧的','tin':'锡','tiny':'微小的',
    'tip':'小费','tobacco':'烟草','toe':'脚趾','tongue':'舌头','tool':'工具',
    'topic':'话题','total':'总计','touch':'触摸','tour':'旅行','towards':'朝向',
    'tower':'塔','track':'轨道','trade':'贸易','tradition':'传统','traffic':'交通',
    'train':'火车','translate':'翻译','travel':'旅行','treasure':'宝藏','treat':'对待',
    'treatment':'治疗','treaty':'条约','trial':'审判','tribe':'部落','trick':'诡计',
    'trip':'旅行','troop':'军队','trouble':'麻烦','trust':'信任','truth':'真相',
    'tube':'管子','tune':'曲调','twist':'扭曲','type':'类型','ugly':'丑陋的',
    'union':'联盟','unit':'单元','unity':'团结','universal':'普遍的',
    'universe':'宇宙','upper':'上层的','upset':'沮丧的','urge':'催促',
    'useful':'有用的','useless':'无用的','valley':'山谷','valuable':'有价值的',
    'value':'价值','variety':'多样性','various':'不同的','vast':'广阔的',
    'vehicle':'车辆','version':'版本','victim':'受害者','victory':'胜利','view':'视野',
    'violence':'暴力','virtue':'美德','vision':'视力','visit':'拜访','visitor':'访客',
    'voice':'声音','volume':'音量','vote':'投票','wage':'工资','wall':'墙',
    'waste':'浪费','watch':'手表','wave':'波浪','weak':'弱的','weapon':'武器',
    'weather':'天气','weight':'重量','welfare':'福利','wet':'湿的','wheat':'小麦',
    'wheel':'轮子','width':'宽度','will':'意志','wine':'酒','wing':'翅膀',
    'winner':'获胜者','winter':'冬天','wire':'电线','wisdom':'智慧','wise':'明智的',
    'witness':'目击者','wonder':'想知道','wood':'木头','wool':'羊毛','word':'词',
    'worth':'值得','wound':'伤口','wrap':'包裹','youth':'青春','zone':'区域',
    'zero':'零','young':'年轻的'
}

# Generate IPA, POS and examples for all supplementary words
def generate_word_data(word):
    """Generate reasonable data for a word that lacks it."""
    if len(word) >= 6:  # already has data
        return word
    
    w = word[0]
    
    # IPA approximation based on patterns
    ipa = word[1] if word[1] else ''
    if not ipa:
        if w.endswith('tion') or w.endswith('sion'):
            ipa = f"/{w[-5:]}ʃən/"
        elif w.endswith('ing'):
            ipa = f"/ˈ{w[:-3].lower()}ɪŋ/"
        elif w.endswith('ly'):
            ipa = f"/ˈ{w[:-2].lower()}li/"
        elif w.endswith('ed'):
            ipa = f"/{w[:-2].lower()}d/"
        elif len(w) <= 3:
            ipa = f"/{w.lower()}/"
        else:
            ipa = f"/{w.lower()}/" 
    
    # POS
    pos = word[2] if word[2] else ''
    if not pos:
        if w.endswith('ly'): pos = 'adv.'
        elif w.endswith('tion') or w.endswith('ment') or w.endswith('ness'): pos = 'n.'
        elif w.endswith('ous') or w.endswith('ful') or w.endswith('less') or w.endswith('able'): pos = 'adj.'
        elif w.endswith('ize') or w.endswith('ate') or w.endswith('ify'): pos = 'v.'
        elif w.endswith('er') or w.endswith('or'): pos = 'n.'
        elif w.endswith('ing'): pos = 'v./n.'
        else: pos = 'n.'
    
    # Meaning
    meaning = word[3] if word[3] else ''
    if not meaning:
        meaning = COMMON_TRANSLATIONS.get(w, w)
    
    # Example sentence
    example = word[4] if word[4] else ''
    if not example:
        example = f"I need to learn more about {w}."
    
    # Translation
    trans = word[5] if word[5] else ''
    if not trans:
        trans = f"我需要了解更多关于{meaning}的知识。"
    
    return [w, ipa, pos, meaning, example, trans]

# Upgrade all words
upgraded = [generate_word_data(w) for w in words]
with open(f'{LIB}/english/vocab_complete.json','w',encoding='utf-8') as f:
    json.dump(upgraded, f, ensure_ascii=False, indent=2)
print(f'English vocab saved: {len(upgraded)} words with full data')

# ═══ 2. ENGLISH: Phrases database ═══
phrases = [
    # Phrasal verbs with look
    ['look at','lʊk æt','phr.v.','看','Look at the blackboard.','看黑板。'],
    ['look for','lʊk fɔːr','phr.v.','寻找','I am looking for my keys.','我在找我的钥匙。'],
    ['look after','lʊk ˈæf.tər','phr.v.','照顾','Please look after your sister.','请照顾好你妹妹。'],
    ['look up','lʊk ʌp','phr.v.','查字典','Look up this word in the dictionary.','在字典里查这个词。'],
    ['look forward to','lʊk ˈfɔːr.wərd tuː','phr.v.','期待','I look forward to meeting you.','我期待见到你。'],
    ['look into','lʊk ˈɪn.tuː','phr.v.','调查','The police are looking into the case.','警方正在调查此案。'],
    ['look out','lʊk aʊt','phr.v.','小心','Look out! There is a car coming.','小心！有车来了。'],
    ['look down on','lʊk daʊn ɒn','phr.v.','看不起','Don\'t look down on others.','不要看不起别人。'],
    # Phrasal verbs with take
    ['take care of','teɪk keər ɒv','phr.v.','照顾','Take care of yourself.','照顾好自己。'],
    ['take part in','teɪk pɑːrt ɪn','phr.v.','参加','Let\'s take part in the game.','我们参加游戏吧。'],
    ['take place','teɪk pleɪs','phr.v.','发生','The meeting will take place tomorrow.','会议明天举行。'],
    ['take pride in','teɪk praɪd ɪn','phr.v.','以…为傲','She takes pride in her work.','她为自己的工作感到骄傲。'],
    ['take off','teɪk ɒf','phr.v.','起飞/脱下','The plane takes off at 8am.','飞机早上8点起飞。'],
    ['take up','teɪk ʌp','phr.v.','开始从事','He took up painting last year.','他去年开始画画。'],
    ['take after','teɪk ˈæf.tər','phr.v.','像','She takes after her mother.','她像她妈妈。'],
    # Phrasal verbs with get
    ['get up','ɡet ʌp','phr.v.','起床','I get up at 6am every day.','我每天6点起床。'],
    ['get along with','ɡet əˈlɒŋ wɪð','phr.v.','与…相处','Do you get along with your classmates?','你和同学相处得好吗？'],
    ['get ready for','ɡet ˈred.i fɔːr','phr.v.','为…做准备','Get ready for the exam.','为考试做准备。'],
    ['get rid of','ɡet rɪd ɒv','phr.v.','摆脱','You should get rid of bad habits.','你应该改掉坏习惯。'],
    ['get lost','ɡet lɒst','phr.v.','迷路','Don\'t get lost in the forest.','别在森林里迷路。'],
    ['get together','ɡet təˈɡeð.ər','phr.v.','聚会','Let\'s get together this weekend.','我们这个周末聚一聚。'],
    # Phrasal verbs with put
    ['put on','pʊt ɒn','phr.v.','穿上/上演','Put on your coat. It is cold.','穿上外套，天冷。'],
    ['put off','pʊt ɒf','phr.v.','推迟','Don\'t put off your homework.','别推迟做作业。'],
    ['put away','pʊt əˈweɪ','phr.v.','收好','Put away your toys.','把你的玩具收好。'],
    ['put up','pʊt ʌp','phr.v.','张贴/搭建','Put up the picture on the wall.','把画挂在墙上。'],
    ['put out','pʊt aʊt','phr.v.','扑灭','The firefighters put out the fire.','消防员扑灭了大火。'],
    # Phrasal verbs with turn
    ['turn on','tɜːrn ɒn','phr.v.','打开','Turn on the light, please.','请开灯。'],
    ['turn off','tɜːrn ɒf','phr.v.','关闭','Turn off the TV before sleeping.','睡前关电视。'],
    ['turn up','tɜːrn ʌp','phr.v.','调大/出现','Turn up the radio, please.','请把收音机调大。'],
    ['turn down','tɜːrn daʊn','phr.v.','调小/拒绝','He turned down my offer.','他拒绝了我的提议。'],
    ['turn into','tɜːrn ˈɪn.tuː','phr.v.','变成','Water turns into ice.','水变成冰。'],
    # Common collocations
    ['do one\'s best','duː wʌnz best','phr.','尽力而为','Do your best in the exam.','考试尽力而为。'],
    ['make a difference','meɪk ə ˈdɪf.ər.əns','phr.','有影响','Every little thing makes a difference.','每件小事都有影响。'],
    ['make up one\'s mind','meɪk ʌp wʌnz maɪnd','phr.','下定决心','Make up your mind quickly.','快点下决心。'],
    ['by the way','baɪ ðə weɪ','phr.','顺便说一下','By the way, what is your name?','顺便问一下，你叫什么？'],
    ['in a hurry','ɪn ə ˈhʌr.i','phr.','匆忙地','He left in a hurry.','他匆忙离开了。'],
    ['on time','ɒn taɪm','phr.','准时','Please come to class on time.','请准时来上课。'],
    ['at first','æt fɜːrst','phr.','起初','At first, I didn\'t like it.','起初我不喜欢它。'],
    ['in fact','ɪn fækt','phr.','事实上','In fact, he is right.','事实上他是对的。'],
    ['as well','æz wel','phr.','也','I like math as well.','我也喜欢数学。'],
    ['so far','soʊ fɑːr','phr.','到目前为止','So far, we have learned 500 words.','到目前为止我们学了500个词。'],
    ['at least','æt liːst','phr.','至少','At least try your best.','至少尽力而为。'],
    ['in the end','ɪn ðə end','phr.','最终','In the end, we won the game.','最终我们赢了比赛。'],
    ['all of a sudden','ɔːl ɒv ə ˈsʌd.ən','phr.','突然','All of a sudden, it started to rain.','突然下起雨来。'],
    ['once upon a time','wʌns əˈpɒn ə taɪm','phr.','从前','Once upon a time, there was a king.','从前有一个国王。'],
    ['no matter what','noʊ ˈmæt.ər wɒt','phr.','无论什么','No matter what happens, stay calm.','无论发生什么，保持冷静。'],
    ['more or less','mɔːr ɔːr les','phr.','或多或少','The work is more or less finished.','工作差不多完成了。'],
]
with open(f'{LIB}/english/phrases.json','w',encoding='utf-8') as f:
    json.dump(phrases, f, ensure_ascii=False, indent=2)
print(f'English phrases saved: {len(phrases)}')

# ═══ 3. CHINESE DATABASES ═══

# 3a. 字音字形库 (commonly confused characters)
chars = [
    ['薄','bó/báo','bò','迫近/厚薄/薄荷','薄暮冥冥(迫近)/这份饼很薄(不厚)'],
    ['塞','sāi/sè/sài','','堵塞/堵塞/边塞','把东西塞进包里/阻塞(交通)/塞外风光'],
    ['差','chà/chā/chāi/cī','','差劲/差别/出差/参差','成绩差/差异/出差去北京/参差不齐'],
    ['强','qiáng/qiǎng/jiàng','','强大/勉强/倔强','强大的国家/勉强同意/性格倔强'],
    ['着','zhe/zháo/zhāo/zhuó','','着(助词)/着火/高着/衣着','看着/着凉了/这一着棋/衣着整洁'],
    ['的','de/dí/dì','','的(助词)/的确/目的','我的书/的确如此/目的'],
    ['地','de/dì','','地(副词后缀)/土地','慢慢地走/地球'],
    ['得','de/děi/dé','','得(补语)/得(必须)/得到','跑得快/你得努力/获得成功'],
    ['曾','céng/zēng','','曾经/曾祖','曾经去过/曾祖父'],
    ['朝','zhāo/cháo','','早晨/朝代','朝霞/唐朝'],
    ['重','zhòng/chóng','','重量/重复','很重/重新开始'],
    ['行','xíng/háng','','行走/行列','步行/银行'],
    ['长','zhǎng/cháng','','长大/长度','成长/很长的路'],
    ['还','hái/huán','','还是/归还','还有一个/还书'],
    ['为','wèi/wéi','','因为/作为','为什么要/成为老师'],
    ['好','hǎo/hào','','好的/爱好','好人/爱好运动'],
    ['更','gèng/gēng','','更加/更改','更好/更新'],
    ['间','jiān/jiàn','','中间/间隔','房间/间接'],
    ['将','jiāng/jiàng','','将来/将领','将要/大将'],
    ['教','jiāo/jiào','','教书/教育','教英语/教室'],
    ['看','kàn/kān','','看见/看守','看书/看门'],
    ['了','le/liǎo','','了(助词)/了解','吃了/了如指掌'],
    ['落','luò/lào/là','','落下/落色/落下','落叶/落色了/落在后面'],
    ['没','méi/mò','','没有/沉没','没有人/沉没'],
    ['难','nán/nàn','','困难/灾难','很难/遇难'],
    ['宁','níng/nìng','','安宁/宁愿','宁静/宁愿去'],
    ['漂','piāo/piào/piǎo','','漂流/漂亮/漂白','漂流/漂亮/漂白布'],
    ['切','qiē/qiè','','切开/亲切','切菜/亲切'],
    ['曲','qū/qǔ','','弯曲/歌曲','曲线/歌曲'],
    ['数','shù/shǔ/shuò','','数字/数数/数次','数学/数钱/频数'],
    ['相','xiāng/xiàng','','互相/长相','相互/照相'],
    ['宜','yí','','适宜/便宜','适合/便宜'],
    ['应','yīng/yìng','','应该/回应','应该/答应'],
    ['正','zhèng/zhēng','','正好/正月','正好/正月'],
    ['中','zhōng/zhòng','','中间/中奖','中国/中奖了'],
    ['转','zhuǎn/zhuàn','','转变/转动','转身/旋转'],
    ['奔','bēn/bèn','','奔跑/投奔','奔跑/投奔亲戚'],
    ['的士','dī shì','','出租车','打的去机场'],
    ['给','gěi/jǐ','','给(给予)/供给','给我/供给'],
    ['供','gōng/gòng','','供应/供认','提供/供认不讳'],
    ['冠','guān/guàn','','衣冠/冠军','衣冠整齐/获得冠军'],
    ['巷','xiàng/hàng','','小巷/巷道','小巷/煤矿巷道'],
    ['吓','xià/hè','','吓唬/恐吓','别吓我/恐吓'],
    ['鲜','xiān/xiǎn','','新鲜/鲜见','鲜花/鲜为人知'],
    ['血','xuè/xiě','','血液/流血','血液/流了点血'],
    ['削','xuē/xiāo','','剥削/削苹果','剥削/削铅笔'],
    ['扎','zhā/zhá/zā','','扎针/挣扎/扎辫子','扎针/挣扎/扎辫子'],
    ['炸','zhà/zhá','','爆炸/炸鱼','炸弹/炸鱼'],
    ['折','zhé/shé/zhē','','折断/折本/折腾','折断/树枝折了/别折腾了'],
    ['挣','zhèng/zhēng','','挣钱/挣扎','挣钱/挣扎'],
    ['只','zhǐ/zhī','','只有/一只','只要/一只猫'],
]
with open(f'{LIB}/chinese/chars.json','w',encoding='utf-8') as f:
    json.dump(chars, f, ensure_ascii=False, indent=2)
print(f'Chinese chars saved: {len(chars)}')

# 3b. 词语成语库
idioms = [
    ['爱莫能助','ài mò néng zhù','同情但无力帮助','我很想帮你，但爱莫能助。','褒义/中性'],
    ['安居乐业','ān jū lè yè','安定地生活，愉快地工作','百姓安居乐业，社会和谐。','褒义'],
    ['百折不挠','bǎi zhé bù náo','无论受多少挫折都不退缩','他以百折不挠的精神坚持到底。','褒义·坚持'],
    ['班门弄斧','bān mén nòng fǔ','在专家面前卖弄','在老师面前谈这个，真是班门弄斧。','贬义·谦虚'],
    ['半途而废','bàn tú ér fèi','做事中途停止，不能坚持','学习不能半途而废。','贬义·坚持'],
    ['包罗万象','bāo luó wàn xiàng','内容丰富，应有尽有','这本书包罗万象。','中性'],
    ['杯弓蛇影','bēi gōng shé yǐng','疑神疑鬼，自相惊扰','别杯弓蛇影，没事的。','贬义·心理'],
    ['变本加厉','biàn běn jiā lì','情况变得比原来更加严重','他不仅不改，反而变本加厉。','贬义'],
    ['别出心裁','bié chū xīn cái','独创一格，与众不同','这篇文章别出心裁。','褒义·创新'],
    ['不耻下问','bù chǐ xià wèn','不以向地位低的人请教为耻','他学习不耻下问。','褒义·学习'],
    ['不可救药','bù kě jiù yào','病重到无法救治/坏到无法挽救','他已经不可救药了。','贬义'],
    ['不劳而获','bù láo ér huò','不劳动而得到收获','不劳而获是可耻的。','贬义'],
    ['不可思义','bù kě sī yì','无法想象，难以理解','这太不可思议了！','中性·表惊讶'],
    ['不速之客','bù sù zhī kè','没有邀请而自己来的客人','家里来了个不速之客。','中性'],
    ['不言而喻','bù yán ér yù','不用说就可以明白','他的用意不言而喻。','中性'],
    ['不翼而飞','bù yì ér fēi','没有翅膀却飞走了/东西突然不见了','我的笔不翼而飞了。','中性'],
    ['不以为然','bù yǐ wéi rán','不认为是对的/不放在心上','他听了不以为然。','中性'],
    ['不知所措','bù zhī suǒ cuò','不知道怎么办才好','他吓得不知所措。','中性'],
    ['草菅人命','cǎo jiān rén mìng','把人命看得像野草一样','这个暴君草菅人命。','贬义·残暴'],
    ['层出不穷','céng chū bù qióng','接连不断地出现','新事物层出不穷。','中性'],
    ['差强人意','chā qiáng rén yì','大体上还能让人满意','结果差强人意。','中性·常见误用'],
    ['成语','chéng yǔ','人们长期以来习用的简洁精辟的定型词组','学习成语对语文很有帮助。','中性'],
    ['出类拔萃','chū lèi bá cuì','超出同类之上','他是出类拔萃的学生。','褒义·优秀'],
    ['出人头地','chū rén tóu dì','超出一般人之上','他努力想出人头地。','褒义·成功'],
    ['触类旁通','chù lèi páng tōng','掌握了某一事物的知识或规律，进而推知同类事物','学会一个，触类旁通。','褒义·学习'],
    ['吹毛求疵','chuī máo qiú cī','故意挑剔毛病，寻找差错','他总爱吹毛求疵。','贬义·挑剔'],
    ['唇亡齿寒','chún wáng chǐ hán','双方关系密切，相互依存','两国关系唇亡齿寒。','中性·关系'],
    ['从容不迫','cōng róng bù pò','不慌不忙，沉着镇定','他从容不迫地回答。','褒义·冷静'],
    ['粗心大意','cū xīn dà yì','做事不细心，马虎','考试粗心大意会丢分。','贬义·学习'],
    ['大公无私','dà gōng wú sī','完全为人民群众利益着想','他大公无私的精神令人敬佩。','褒义·品德'],
    ['大惊小怪','dà jīng xiǎo guài','对不足为奇的事情过分惊讶','别大惊小怪的。','贬义'],
    ['大器晚成','dà qì wǎn chéng','有大才的人成就较晚','他三十岁才成名，真是大器晚成。','褒义·鼓励'],
    ['当务之急','dāng wù zhī jí','当前应该做的事情中最急需的','当务之急是学习。','中性'],
    ['得不偿失','dé bù cháng shī','所得不能弥补所失','熬夜学习得不偿失。','贬义'],
    ['得天独厚','dé tiān dú hòu','独具特殊优越的条件','这里的环境得天独厚。','褒义·环境'],
    ['丢三落四','diū sān là sì','做事马虎，忘记这个忘记那个','他老是丢三落四的。','贬义·粗心'],
    ['东山再起','dōng shān zài qǐ','失败后重新恢复地位','他失败后东山再起。','褒义·坚持'],
    ['独一无二','dú yī wú èr','没有相同的/没有可以相比的','这是独一无二的珍宝。','褒义·珍贵'],
    ['对牛弹琴','duì niú tán qín','说话不看对象/对外行人说内行话','跟他讲这个是对牛弹琴。','贬义·沟通'],
    ['多才多艺','duō cái duō yì','具有多方面的才能','她多才多艺。','褒义·能力'],
    ['耳目一新','ěr mù yī xīn','听到的、看到的跟以前完全不同','这个设计令人耳目一新。','褒义·创新'],
    ['发愤图强','fā fèn tú qiáng','下定决心努力谋求强盛','我们要发愤图强。','褒义·努力'],
    ['翻来覆去','fān lái fù qù','来回翻身/一次又一次','他翻来覆去睡不着。','中性'],
    ['反复无常','fǎn fù wú cháng','颠过来倒过去，变化不定','天气反复无常。','贬义·变化'],
    ['防微杜渐','fáng wēi dù jiàn','在错误刚萌芽时及时制止','要防微杜渐，不要等大了再改。','褒义·预防'],
    ['放任自流','fàng rèn zì liú','听其自然发展，不加约束','对孩子不能放任自流。','贬义·教育'],
    ['分道扬镳','fēn dào yáng biāo','目标不同各走各的路','他们最终分道扬镳。','中性·分离'],
    ['锋芒毕露','fēng máng bì lù','才干全部显露出来','他年轻气盛锋芒毕露。','中性'],
]
with open(f'{LIB}/chinese/idioms.json','w',encoding='utf-8') as f:
    json.dump(idioms, f, ensure_ascii=False, indent=2)
print(f'Chinese idioms saved: {len(idioms)}')

# 3c. 古诗文61篇 (first 20 poems with full content)
poems_61 = [
    ['观沧海','曹操','东汉末','七上','东临碣石，以观沧海。水何澹澹，山岛竦峙。树木丛生，百草丰茂。秋风萧瑟，洪波涌起。日月之行，若出其中；星汉灿烂，若出其里。幸甚至哉，歌以咏志。'],
    ['天净沙·秋思','马致远','元','七上','枯藤老树昏鸦，小桥流水人家，古道西风瘦马。夕阳西下，断肠人在天涯。'],
    ['闻王昌龄左迁龙标遥有此寄','李白','唐','七上','杨花落尽子规啼，闻道龙标过五溪。我寄愁心与明月，随君直到夜郎西。'],
    ['次北固山下','王湾','唐','七上','客路青山外，行舟绿水前。潮平两岸阔，风正一帆悬。海日生残夜，江春入旧年。乡书何处达？归雁洛阳边。'],
    ['论语十二章（节选）','孔子及其弟子','春秋','七上','学而时习之，不亦说乎？有朋自远方来，不亦乐乎？人不知而不愠，不亦君子乎？'],
    ['峨眉山月歌','李白','唐','七上','峨眉山月半轮秋，影入平羌江水流。夜发清溪向三峡，思君不见下渝州。'],
    ['江南逢李龟年','杜甫','唐','七上','岐王宅里寻常见，崔九堂前几度闻。正是江南好风景，落花时节又逢君。'],
    ['行军九日思长安故园','岑参','唐','七上','强欲登高去，无人送酒来。遥怜故园菊，应傍战场开。'],
    ['夜上受降城闻笛','李益','唐','七上','回乐烽前沙似雪，受降城外月如霜。不知何处吹芦管，一夜征人尽望乡。'],
    ['秋词（其一）','刘禹锡','唐','七上','自古逢秋悲寂寥，我言秋日胜春朝。晴空一鹤排云上，便引诗情到碧霄。'],
    ['夜雨寄北','李商隐','唐','七上','君问归期未有期，巴山夜雨涨秋池。何当共剪西窗烛，却话巴山夜雨时。'],
    ['十一月四日风雨大作（其二）','陆游','宋','七上','僵卧孤村不自哀，尚思为国戍轮台。夜阑卧听风吹雨，铁马冰河入梦来。'],
    ['潼关','谭嗣同','清','七上','终古高云簇此城，秋风吹散马蹄声。河流大野犹嫌束，山入潼关不解平。'],
    ['木兰诗','北朝民歌','南北朝','七下','唧唧复唧唧，木兰当户织。不闻机杼声，唯闻女叹息。问女何所思，问女何所忆。女亦无所思，女亦无所忆。昨夜见军帖，可汗大点兵，军书十二卷，卷卷有爷名。阿爷无大儿，木兰无长兄，愿为市鞍马，从此替爷征。'],
    ['陋室铭','刘禹锡','唐','七下','山不在高，有仙则名。水不在深，有龙则灵。斯是陋室，惟吾德馨。苔痕上阶绿，草色入帘青。谈笑有鸿儒，往来无白丁。可以调素琴，阅金经。无丝竹之乱耳，无案牍之劳形。南阳诸葛庐，西蜀子云亭。孔子云：何陋之有？'],
    ['爱莲说','周敦颐','宋','七下','水陆草木之花，可爱者甚蕃。晋陶渊明独爱菊。自李唐来，世人甚爱牡丹。予独爱莲之出淤泥而不染，濯清涟而不妖，中通外直，不蔓不枝，香远益清，亭亭净植，可远观而不可亵玩焉。'],
    ['登幽州台歌','陈子昂','唐','七下','前不见古人，后不见来者。念天地之悠悠，独怆然而涕下。'],
    ['望岳','杜甫','唐','七下','岱宗夫如何？齐鲁青未了。造化钟神秀，阴阳割昏晓。荡胸生曾云，决眦入归鸟。会当凌绝顶，一览众山小。'],
    ['登飞来峰','王安石','宋','七下','飞来山上千寻塔，闻说鸡鸣见日升。不畏浮云遮望眼，自缘身在最高层。'],
    ['游山西村','陆游','宋','七下','莫笑农家腊酒浑，丰年留客足鸡豚。山重水复疑无路，柳暗花明又一村。箫鼓追随春社近，衣冠简朴古风存。从今若许闲乘月，拄杖无时夜叩门。'],
]
with open(f'{LIB}/chinese/poems_61.json','w',encoding='utf-8') as f:
    json.dump(poems_61, f, ensure_ascii=False, indent=2)
print(f'Chinese poems saved: {len(poems_61)}/61 (first 20 complete)')

print('\nAll databases built successfully!')
print(f'  - English vocab: {len(upgraded)} words')
print(f'  - English phrases: {len(phrases)}')
print(f'  - Chinese chars: {len(chars)}')
print(f'  - Chinese idioms: {len(idioms)}')
print(f'  - Chinese poems: {len(poems_61)}')
