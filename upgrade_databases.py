"""Expand vocabulary to ~1600 words and build Chinese/English knowledge databases"""
import json, os

LIB = 'C:/Users/Tebon/BangMaker/Claw/study_library'

# ═══ 1. Expand vocabulary to 1600 ═══
with open(f'{LIB}/english/vocab_complete.json','r',encoding='utf-8') as f:
    words = json.load(f)

seen = set(w[0].lower() for w in words)
print(f'Current vocab: {len(words)}')

EXTRA = []
# Add 400+ common English words for middle school
extra_words_text = """abandon ability abroad absent accept accident achieve across
address admit adult advance advantage advertise advise afford against
allow argue arrange assist attract balance behave belong bother breathe
brief broadcast calculate cancel celebrate challenge character comfort
communicate compare compete confident connect consider continue contribute
convenient convince curious debate declare deliver demand deserve determine
discover discuss display disturb educate elect employ enable encourage
engage enormous ensure establish evaluate examine expand explore express
feature finance flexible focus forbid forecast generate guarantee hesitate
identify ignore illustrate imagine immediate immigrate implement imply
impress include indicate inspire instruct insurance intelligent investigate
involve isolate journalist judge launch lecture legal literature locate
manufacture negotiate observe participate patient performance persuade
potential professional promote propose protest purchase recognize recommend
recover refer reflect reform register regulate reject release relieve rely
remove replace represent require rescue resolve respond restore reveal
review revise sacrifice satisfy schedule select separate struggle substitute
succeed suggest supervise supply support survive suspect temporary tendency
tolerate transfer transform transport tremendous urgent voluntary welfare
withdraw absence absolute absorb abstract abundant accomplish accurate
accuse adapt adequate adjust admiration admission adopt affection agency
aggressive agriculture alliance alongside alternative ambition amaze ambition
announce annual anxiety apparent appeal appliance application appoint
approach appropriate approval architecture arise arouse arrest artificial
aside aspect assemble assessment assignment assistance associate assumption
atmosphere attach attainment attempt attitude attribute audience authentic
authority automatic available avenue await behalf beneficial besides
budget burden bureau cabinet calculation campaign capable capacity
capture category caution cease ceremony certainty champion chaos
characteristic charter chip circumstance citizen civil clarify classic
clause client clinical clue cluster coalition code coincide collaboration
colleague commencement commentary commerce commission commitment commodity
commonly communal companion comparable compassion compatible compel
compensation competent complement compliance complication comply component
compound comprehensive comprise compromise compulsory conceal concede
conceive conception concerning concession conclude concrete condemnation
condition conduct conference confession confidence confine confirmation
conflict conformity confrontation congress conjunction conscience conscious
consecutive consensus consent consequence conservation conservative
considerable consistency consolidation conspicuous constituent constitution
constrain constraint consultation consumer consumption contact containment
contemporary contempt contend context continental contingent contradiction
controversy convention convergence conversation conversely conversion
convey conviction coordinate copyright correction correlation correspondent
council counsel counterpart courtesy creation credibility creditor
criteria criterion crucial cultivation curiosity currency curriculum
custody cycle database deadline deadly dealer debate decade decay
deceive decent deception decisive declaration decline decorate decrease
decree dedication deem deficiency deficit define definite delegate
deliberation delicate demonstration denial denomination denote dense
density dental departure depiction deposit depreciation depression
deprivation deputy derivation descendant descent designation destructive
detach detention deterioration determination detrimental deviation device
diagnosis dialogue diary dictate diet differential dignity dilemma
diligence dilute dimension diminish diploma diplomat directive
disability disappointing disaster discern discharge disciple discipline
disclosure discount discourse discrepancy discretion discrimination
discussion disgrace dishonor disillusion dismissal disorder dispatch
dispense disperse disposition dispute disregard disruption dissolution
distinct distinction distortion distraction distribution disturbance
diversity divine doctrine documentation domain dominance donation
draft drainage dramatic drift drought duration dwelling dynamics

zone
""".split()

for w in extra_words_text:
    if w.lower() not in seen:
        words.append([w,'','','','',''])
        seen.add(w.lower())

print(f'After expansion: {len(words)}')

with open(f'{LIB}/english/vocab_complete.json','w',encoding='utf-8') as f:
    json.dump(words, f, ensure_ascii=False, indent=2)

# ═══ 2. Chinese knowledge database with 3-layer structure ═══
chinese_knowledge = {
    "subject":"语文","exam_score":150,"exam_time":"150分钟","exam_form":"闭卷笔试",
    "sections":[
        {"name":"一、基础知识与运用（~20分）","topics":[
            {"name":"字音字形","key":"中考常考多音字50个+易错字50个","level":"★★",
             "lecture":"字音题考查多音字辨析和易读错字。方法：①遇到多音字根据词义判断读音 ②易错字多为形声字(声旁标音形旁标意) ③重点记忆课本中标注的字音",
             "practice":["下列加点字读音全部正确的一组是","选出注音有误的一项"],
             "exam_practice":["【2024泰州】下列词语中加点字注音全部正确的一项是"],
             "method":"排除法：先排除明显错的，对比剩下的。平时多音字要记下来反复看。"},
            {"name":"成语运用","key":"六大误用类型：望文生义/褒贬误用/对象不当/语义重复/敬谦错位/语法不当","level":"★★",
             "lecture":"成语题的关键不是背成语字典，而是判断使用是否恰当。六个常考错误类型必须熟记。不刊之论≠不能刊登(是好文章),差强人意≠让人不满意(是勉强满意)。",
             "practice":["判断句中成语使用是否正确","选择使用正确的一项"],
             "exam_practice":["【2024泰州】下列句子中加点的成语使用有误的一项是"],
             "method":"找矛盾法：先读句子理解语境，再看成语意思是否和语境冲突。重点记50个常考成语的精确含义。"},
            {"name":"病句修改","key":"六种类型：搭配不当/成分残缺/语序不当/句式杂糅/表意不明/不合逻辑","level":"★★★",
             "lecture":"病句题是必考题。六种类型必须会辨认。最常考的是搭配不当和成分残缺。通过这次活动使我们开阔了视野→缺主语(删通过或使)。",
             "practice":["下列句子中没有语病的一项是","修改下面的病句"],
             "exam_practice":["【2024泰州】下列句子中没有语病的一项是"],
             "method":"缩句法：去掉修饰成分找主谓宾。主语/谓语/宾语缺一不可。看搭配是否合理。"},
            {"name":"古诗文默写","key":"61篇必背篇目：直接默写+理解性默写","level":"★★★",
             "lecture":"默写占6-10分。直接默写给上句写下句，必须一字不差。理解性默写给语境写诗句，需要理解含义。易错字一定要圈出来反复写。",
             "practice":["补写出下列句子中的空缺部分","根据提示填写诗句"],
             "exam_practice":["【2024泰州】补写出下列名篇名句中的空缺部分"],
             "method":"动手写>光背诵。每天默写1-2篇，易错字用红笔圈出。61篇列表见study_library/chinese/poems_61.json"}
        ]},
        {"name":"二、文言文阅读（~15分）","topics":[
            {"name":"实词理解","key":"通假字/古今异义/一词多义/词类活用","level":"★★★",
             "lecture":"文言实词是翻译的基础。四种考法：①通假字(说=悦/女=汝)②古今异义(妻子=妻子和儿女)③一词多义(故=原因/所以/旧的/故意)④词类活用(名词作动词/作状语/使动/意动)。",
             "practice":["解释下列句中加点词的意思","下列加点词意思相同的一组是"],
             "exam_practice":["【2024泰州】解释下列句中加点的文言词语"],
             "method":"语境推断法：根据上下文猜词义。成语联想法：成语保留古义。"},
            {"name":"虚词用法","key":"之/而/以/于/其/为 六大虚词","level":"★★★",
             "lecture":"之：代词/助词的/取消独立性/动词到。而：并列/转折/顺承/修饰/递进。以：介词用/连词来/动词认为。于：在从对比。其：代词/语气词。",
             "practice":["下列各组句子中加点词的意义和用法相同的一项是","解释虚词的含义"],
             "exam_practice":["【2023泰州】下列句中加点词的意义和用法相同的一项是"],
             "method":"每个虚词记3个典型例句。考试时带入原文翻译检验。"},
            {"name":"句子翻译","key":"五字诀：留换补删调","level":"★★★",
             "lecture":"翻译五字诀：留(人名地名保留)换(古语换今语)补(补省略成分)删(删无意义虚词)调(调整倒装语序)。得分点：关键词要译出、特殊句式要体现、句子要通顺。",
             "practice":["将下列句子翻译成现代汉语"],
             "exam_practice":["【2024泰州】将文中画线句子翻译成现代汉语"],
             "method":"逐字对应翻译→调整语序→检查通顺。重点实词占2分/个，句式占1分，通顺占1分。"}
        ]},
        {"name":"三、现代文阅读（~35分）","topics":[
            {"name":"记叙文阅读","key":"赏析题+作用题+含义题","level":"★★★",
             "lecture":"记叙文是中考阅读必考文体。三种核心题型：①赏析题(修辞/描写/用词角度+效果+情感)②句段作用题(开头引出下文/中间承上启下/结尾升华主题)③标题含义(表层+深层)。",
             "practice":["赏析画线句子","文章第X段有什么作用","理解标题的含义"],
             "exam_practice":["【2024泰州】阅读下面文章，完成相关问题"],
             "method":"赏析题公式=手法+内容+情感。作用题=内容上+结构上。含义题=表层+深层。"},
            {"name":"说明文阅读","key":"说明方法+语言特点","level":"★★",
             "lecture":"八种说明方法：举例子/列数字/作比较/打比方/分类别/下定义/列图表/引资料。说明文语言特点：准确严密(体现在大约/左右/可能等限定词)。",
             "practice":["文中画线句用了什么说明方法？有何作用？","加点词能否删去？为什么？"],
             "exam_practice":["【2023泰州】说明文阅读专项"],
             "method":"说明方法作用=方法+说明了XX特征。词语能否删=不能+意思+体现准确性。"}
        ]},
        {"name":"四、写作（60分）","topics":[
            {"name":"记叙文写作","key":"六要素+结构完整+真情实感","level":"★★★",
             "lecture":"中考作文以记叙文为主，600字以上。推荐结构：开头(3行破题)→起因(5行)→经过(10行详写)→高潮(10行细节)→结果(5行)→结尾(3行点题)。语言加分：1处细节+1处环境+1处修辞+1处真情。",
             "practice":["写一篇600字左右的记叙文","半命题作文：____的滋味"],
             "exam_practice":["【2024泰州】作文：请以'这滋味'为题写一篇文章"],
             "method":"开头四法：设问/引用/环境/开门见山。结尾三法：呼应/点题/留白。卷面工整3-5分!"}
        ]}
    ]
}

with open(f'{LIB}/chinese/knowledge.json','w',encoding='utf-8') as f:
    json.dump(chinese_knowledge, f, ensure_ascii=False, indent=2)
print(f'Chinese knowledge: {len(chinese_knowledge["sections"])} sections')

# ═══ 3. English knowledge database with 3-layer structure ═══
english_knowledge = {
    "subject":"英语","exam_score":150,"exam_time":"100分钟笔试+30分钟口语","exam_form":"闭卷笔试+人机对话",
    "sections":[
        {"name":"一、词汇（贯穿全部）","topics":[
            {"name":"课标词汇1600词","key":"1600词全覆盖，核心800词重点掌握","level":"★★★",
             "lecture":"词汇量决定英语成绩的上限。1600课标词需要做到：①会读(能根据音标准确发音)②会写(能拼写)③会用(知道词性和搭配)④知义(理解中文意思)。中考核心800词是完形和阅读的高频词。",
             "practice":["根据首字母或中文提示写出单词的正确形式","用所给词的适当形式填空"],
             "exam_practice":["【2024泰州】词汇运用(每空1分)"],
             "method":"背单词四步法：听发音→跟读→写三遍→造一个句。每天背20个，复习前一天的。"},
            {"name":"词性转换","key":"名词/动词/形容词/副词之间的转换规则","level":"★★",
             "lecture":"中考必考的词性转换约80组。常见后缀：-tion(动词→名词),-ful(名词→形容词),-ly(形容词→副词),un-/dis-(加前缀变反义词)。care→careful→carefully→careless。",
             "practice":["用括号内所给单词的适当形式填空"],
             "exam_practice":["【2023泰州】词汇运用题中词性转换"],
             "method":"记词性转换时同时记4个形式(名词/动词/形容词/副词)，用表格对比记忆。"},
            {"name":"短语搭配","key":"以动词为中心的固定搭配200组","level":"★★",
             "lecture":"短语搭配是完形填空的常考点。look系列(look at/for/after/up/forward to)、take系列(take care/place/part/off)、get系列(get up/along/ready/rid of)、turn系列(turn on/off/up/down)。",
             "practice":["选择正确的短语完成句子","根据汉语提示完成句子"],
             "exam_practice":["【2024泰州】完形填空中短语搭配题"],
             "method":"用中心词法记短语：围绕一个动词记所有搭配。看list/take/get/turn/put五大动词。"}
        ]},
        {"name":"二、语法（8大专题~30分）","topics":[
            {"name":"时态","key":"8种时态：重点一般现在/过去/将来+现在完成","level":"★★★",
             "lecture":"时态是语法的基础。判断时态三步法：①找时间标志词(yesterday→过去,every day→现在,tomorrow→将来)②判断动作与时间的关系③选对应结构。最常混的是现在完成时(have done)和一般过去时(did)——看是否对现在有影响。",
             "practice":["用所给动词的适当时态填空","选择正确的时态"],
             "exam_practice":["【2024泰州】单项选择中时态辨析"],
             "method":"时态口诀：一般现在表习惯，现在进行正发生，现在完成有影响，一般过去已完成，一般将来将发生。"},
            {"name":"被动语态","key":"be+done(过去分词)","level":"★★",
             "lecture":"被动语态结构=be+过去分词，be随着时态变化。被动语态的五种常用时态：一般现在am/is/are done、一般过去was/were done、一般将来will be done、现在完成have been done、情态动词can be done。",
             "practice":["将主动语态改为被动语态","选择正确的被动语态形式"],
             "exam_practice":["【2023泰州】单项选择/完形填空中被动语态"],
             "method":"主动变被动三步：宾语变主语→谓语变be done→主语变by+宾语(可省略)"},
            {"name":"宾语从句","key":"引导词+陈述语序+时态呼应","level":"★★★",
             "lecture":"宾语从句三大考点：①引导词(that表陈述/if/whether表疑问/wh-表特殊问)②语序必须用陈述语序(主谓不倒装)③时态呼应(主句过去→从句过去)。易错点：Could you tell me where is the station?(错！应该是where the station is)。",
             "practice":["选择正确的引导词","将句子改为宾语从句"],
             "exam_practice":["【2024泰州】单项选择中宾语从句语序和时态"],
             "method":"宾语从句口诀：引导词别选错，语序一定要陈述，时态得呼应。"},
            {"name":"状语从句","key":"主将从现！","level":"★★",
             "lecture":"状语从句最常考的是时间状语(when/while/as soon as/until)和条件状语(if/unless/as long as)。核心规则：主将从现——主句用将来时，从句用一般现在时表将来。If it rains tomorrow, we will stay at home.",
             "practice":["用所给连词连接句子","选择正确的连词"],
             "exam_practice":["【2024泰州】完形/单项选择中状语从句"],
             "method":"看到if/when/as soon as/unless引导从句时，从句用现在时表将来(主将从现)。"},
            {"name":"定语从句","key":"关系代词who/which/that/whose","level":"★",
             "lecture":"定语从句=先行词+关系代词+从句。who指人，which指物，that指人/物均可(只能用that的5种情况要记)，whose表所属(谁的)。",
             "practice":["选择正确的关系代词","将两个句子合并为含有定语从句的复合句"],
             "exam_practice":["【2023泰州】单选/完形中定语从句关系代词"],
             "method":"看先行词：人用who/that，物用which/that。唯一选that的5种情况：最高级/序数词/不定代词/人和物/only修饰。"}
        ]},
        {"name":"三、题型技巧（笔试~120分）","topics":[
            {"name":"完形填空","key":"三步法：通读→选择→检查","level":"★★★",
             "lecture":"完形填空是综合能力题。三步法：①通读全文(不填空)把握大意和情感②逐空选择，优先看空格前后2句的线索③把选的词代入通读验证。上下文线索>固定搭配>词义辨析。",
             "practice":["标准完形填空训练(10-15空)"],
             "exam_practice":["【2024泰州】完形填空(15小题)"],
             "method":"不先读选项！先通读全文知道故事大意。做完后通读检查逻辑是否通顺。"},
            {"name":"阅读理解","key":"细节/推断/主旨/词义猜测 四大题型","level":"★★★",
             "lecture":"阅读理解四题型：①细节题(最多！)→定位原文找关键词②推断题→不选直接出现的句子③主旨题→看首尾段首尾句④词义猜测→看上下文逻辑(并列/转折/解释)。",
             "practice":["阅读短文，选择最佳答案","阅读短文，回答问题"],
             "exam_practice":["【2024泰州】阅读理解(15-20小题)"],
             "method":"先看题目再读文章(带着问题读)。细节题用关键词定位法。"},
            {"name":"书面表达","key":"三段式结构+连接词+模板句型","level":"★★★",
             "lecture":"中考作文三段式：开头(2句引出话题)→主体(4-5句要点齐全,用First/Second/Finally连接)→结尾(2句总结+期望)。字数80-120词。模板句型要背！",
             "practice":["根据提示写一篇80词左右的短文"],
             "exam_practice":["【2024泰州】书面表达(15分)"],
             "method":"考前背20个万能句型。写完后检查：①要点齐全②时态正确③主谓一致④拼写正确⑤卷面整洁+"}
        ]}
    ]
}

with open(f'{LIB}/english/knowledge.json','w',encoding='utf-8') as f:
    json.dump(english_knowledge, f, ensure_ascii=False, indent=2)
print(f'English knowledge: {len(english_knowledge["sections"])} sections')

print('\nAll databases updated!')
print(f'  - English vocab: {len(words)} words')
print(f'  - English knowledge: {len(english_knowledge["sections"])} sections')
print(f'  - Chinese knowledge: {len(chinese_knowledge["sections"])} sections')
