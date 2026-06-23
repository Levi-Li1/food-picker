// add_supplements_v2.js - 全面补充语文、英语、政治、历史教学和练习内容
const fs = require('fs');
const path = require('path');

// ===== CONTENT LIBRARY =====

// 语文内容库：按周分配
const CHINESE = {
  // W1: 古诗文默写 + 文学常识
  w1_D3: {
    title: '📖 语文 · 古诗文默写+文言文入门（1h）',
    content: `<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（20min）</h4>
<p><b>古诗默写技巧</b>：先理解诗意再背诵。圈出易错字（如"澹澹"不要写成"淡淡"，"竦峙"不要写成"耸峙"）。默写后逐字对照原文，错一字整首重默。</p>
<p><b>文言文基础</b>——中考必考4大句式：</p>
<p>①<b>判断句</b>："……者，……也" / "乃" / "为" → 是<br>
②<b>省略句</b>：补充省略的主语或宾语<br>
③<b>倒装句</b>：宾语前置/状语后置，翻译时调整语序<br>
④<b>被动句</b>："为……所……" / "见……于……"</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>默写训练（20min）</h4>
<div class="q-block"><b>默写1</b>：《天净沙·秋思》马致远<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">枯藤老树昏鸦，小桥流水人家，古道西风瘦马。夕阳西下，断肠人在天涯。</div></div>
<div class="q-block"><b>翻译</b>："学而时习之，不亦说乎"是什么意思？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">学习了然后按时温习，不也是很愉快的吗？——"说"通"悦"，高兴。注意"时"是"按时"不是"时常"！</div></div>
<div class="q-block"><b>判断句式</b>："陈胜者，阳城人也"是什么句式？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">判断句。"……者，……也"是典型的判断句式。翻译：陈胜是阳城人。</div></div>
</div>
<div class="step"><h4><span class="dot" style="background:var(--green)"></span>固（10min）</h4>
<div class="err-box"><b>❗ 默写常见扣分点</b><br>1. 同音错字：如"生"写成"升"、"涯"写成"崖" → 只要错别字就扣分<br>2. 漏字添字：每句必须和原文一字不差<br>3. 字迹潦草：阅卷老师看不清就算错！</div></div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（10min）</h4><p>📔 抄写三道默写题中易错的字各5遍 📔 默写《天净沙·秋思》</p></div>`
  },
  // W3: 文言文阅读
  w3_D15: {
    title: '📖 语文 · 文言文阅读——《论语》十二章（1h）',
    content: `<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（20min）</h4>
<p><b>中考文言文三步翻译法</b>：</p>
<p>①<b>通读全文</b>，圈出不认识的字（结合注释推测）</p>
<p>②<b>逐句翻译</b>：留（人名地名不译）、换（古语换今语）、补（补省略成分）、删（删无义虚词）、调（调整倒装语序）</p>
<p>③<b>查漏补缺</b>：关键实词必须准确，虚词（之/其/而/以/于）的用法要清楚</p>
<p><b>《论语》十二章重点句</b>（中考高频）：</p>
<p>"学而不思则罔，思而不学则殆"——学习与思考的关系</p>
<p>"温故而知新，可以为师矣"——复习的重要性</p>
<p>"三人行，必有我师焉"——虚心学习的态度</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>练（30min）</h4>
<div class="q-block"><b>翻译</b>："知之者不如好之者，好之者不如乐之者"<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">懂得它的人不如喜爱它的人，喜爱它的人不如以它为乐的人。——阐述了学习的三种境界：知道→爱好→乐在其中。</div></div>
<div class="q-block"><b>虚词</b>："之"在"学而时习之"中是什么用法？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">代词，指代"学过的知识"。"之"作代词时一般指代前面说过的内容。</div></div>
<div class="q-block"><b>理解</b>："吾日三省吾身"是什么意思？"三"是三次吗？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">我每天多次反省自己。"三"不是确数"三次"，而是虚指"多次"。文言文中"三""九"常表虚数。</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--green)"></span>固+结（10min）</h4>
<div class="err-box"><b>❗ 翻译三大忌</b><br>1. 照抄原文不给翻译→0分<br>2. 漏译关键字词→扣一半<br>3. 语序完全按古文→不通顺扣分<br>🔑 秘诀：先把每个字的意思写出来，再连成通顺的现代汉语句子。</div></div>`
  },
  // W3: 现代文阅读
  w3_D17: {
    title: '📖 语文 · 现代文阅读——散文阅读（1h）',
    content: `<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（15min）</h4>
<p><b>散文阅读核心——抓"形散神不散"</b></p>
<p>散文的特点是"形散神聚"：看似零散的材料都围绕一个中心思想展开。</p>
<p><b>中考散文阅读4大题型</b>：</p>
<p>①<b>概括题</b>：谁+在什么情况下+做了什么+结果 → 每条不超过30字</p>
<p>②<b>赏析题</b>：用了什么修辞/描写+写出了什么+表达了什么情感。公式：修辞手法+描写内容+表达效果+作者情感</p>
<p>③<b>含义题</b>：先解释字面意思→再联系上下文→最后答出深层含义/作者意图</p>
<p>④<b>作用题</b>：内容上(写了什么/表现了什么)+结构上(引出下文/承上启下/总结全文)</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>练（35min）</h4>
<div class="q-block"><b>赏析题</b>：分析"春风又绿江南岸"中"绿"字的妙处。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">"绿"字是形容词活用为动词，意为"使……变绿"。化静态为动态，生动形象地写出了春风吹过江南岸后万物复苏、一片生机勃勃的景象，表达了诗人对春天的喜爱之情。</div></div>
<div class="q-block"><b>概括题</b>：阅读《背影》选段——"我看见他戴着黑布小帽……"请概括这段的主要内容。<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">父亲在车站艰难地穿过铁道为"我"买橘子。表现了父亲对儿子深沉的爱以及"我"的感动。</div></div>
<div class="q-block"><b>作用题</b>：文章开头描写环境有什么作用？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">内容上：渲染了……的气氛，暗示了人物……的心情；结构上：为下文……做铺垫，引出……</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（10min）</h4><p>📔 把赏析题的标准答题公式抄在笔记本上 📔 记住：中考阅读=套路+理解，缺一不可</p></div>`
  },
  // W6 Day 36 补充：作文基础
  w6_D36_extra: {
    title: '📖 语文 · 作文——记叙文写作（1h）',
    content: `<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（25min）</h4>
<p><b>中考记叙文高分结构——"凤头+猪肚+豹尾"</b></p>
<p><b>开头（凤头，100字）</b>：3种万能开头法：</p>
<p>①<b>悬念式</b>："那天推开教室门的那一刻，我愣住了……"</p>
<p>②<b>名言式</b>："'宝剑锋从磨砺出，梅花香自苦寒来。'这句话伴我走过了最艰难的时光。"</p>
<p>③<b>场景式</b>：用环境描写暗示心情（阴天→难过，阳光→快乐）</p>
<p><b>正文（猪肚，500字）</b>：</p>
<p>选一件具体的事来写（不要写多件事！中考800字只能写好一件事）。要有细节描写：外貌、动作、语言、心理、环境——五觉描写法（视听嗅味触）。</p>
<p><b>结尾（豹尾，100字）</b>：</p>
<p>①<b>点题升华</b>：回到题目，写出感悟 ②<b>首尾呼应</b>：呼应开头的话 ③<b>留白</b>：给人想象空间</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>练（25min）</h4>
<div class="q-block"><b>写开头</b>：以"温暖"为话题，写一个悬念式开头（50-100字）<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">示例：那个冬天格外冷。放学路上我缩着脖子快步走着，突然，一双布满老茧的手递来一个热乎乎的红薯。我抬起头，愣住了——是小区门口那个从来不说话的清洁工爷爷。</div></div>
<div class="q-block"><b>细节描写</b>：描写"妈妈生气时的样子"（50字以上，至少用3种描写）<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">示例：妈妈双眼瞪得溜圆(外貌)，双手叉腰(动作)，声音提高了八度(语言)："你怎么又没写作业！"我低下头不敢看她，心里像打翻了五味瓶(心理)。</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（10min）</h4><p>📔 记住：好作文不是写出来的，是改出来的。写完初稿→放一天→自己大声读一遍→改不通顺的地方→再抄正。</p></div>`
  },
  // W4 Day 23 补充：文言文翻译
  w4_D23_extra: {
    title: '📖 语文 · 古诗文默写+文言翻译技巧（1h）',
    content: `<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（20min）</h4>
<p><b>文言文翻译"五字诀"</b>：<b>留、换、补、删、调</b></p>
<p><b>留</b>：人名、地名、官名、朝代名、度量衡单位不译（如"太守""岳阳楼"直接保留）</p>
<p><b>换</b>：古汉语词汇换成现代汉语（如"吾"→"我"、"汝"→"你"、"尝"→"曾经"）</p>
<p><b>补</b>：补出省略的成分（文言文常省略主语/宾语，翻译时必须补上，用括号标注）</p>
<p><b>删</b>：删除无意虚词（发语词"夫""盖"、句中助词"之"等不译）</p>
<p><b>调</b>：调整倒装语序（宾语前置→改为正常语序；状语后置→提到动词前）</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>练（30min）</h4>
<div class="q-block"><b>翻译</b>："予独爱莲之出淤泥而不染，濯清涟而不妖"<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">我只喜爱莲花从淤泥中长出却不被污染，经过清水洗涤却不显得妖艳。——注意"之"在这里是取消句子独立性，不译。</div></div>
<div class="q-block"><b>翻译</b>："何陋之有？"<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">有什么简陋的呢？——这是宾语前置句，"何陋"是宾语提到动词"有"前面。正常语序是"有何陋"。</div></div>
<div class="q-block"><b>翻译</b>："人不知而不愠，不亦君子乎？"<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">别人不了解我但我不生气，不也是君子吗？——"而"表转折，"愠"是"生气恼怒"。</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（10min）</h4><p>📔 把"留换补删调"五字诀写在笔记本首页 📔 每篇文言文练习都要在译文旁标注用了哪几个字诀</p></div>`
  },
  // W7 Day 44 补充
  w7_D44_extra: {
    title: '📖 语文 · 议论文阅读+文言文综合（1h）',
    content: `<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（20min）</h4>
<p><b>议论文三要素</b>：论点（作者的观点/主张）→论据（证明论点的事实/道理）→论证（用论据证明论点的过程）</p>
<p><b>找中心论点的方法</b>：①看标题（很多标题就是论点）②找开头或结尾的判断句 ③自己概括（没有明确论点时）</p>
<p><b>四大论证方法</b>：</p>
<p>①<b>举例论证</b>：举……的例子，具体有力地论证了……<br>
②<b>道理论证</b>：引用……名言，有力论证了……<br>
③<b>对比论证</b>：将……与……对比，突出强调了……<br>
④<b>比喻论证</b>：把……比作……，生动形象地论证了……</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>练（30min）</h4>
<div class="q-block"><b>找论点</b>：《谈读书》的中心论点是什么？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">读书足以怡情，足以博彩，足以长才。——开篇第一句直接亮明观点。</div></div>
<div class="q-block"><b>论证方法</b>："读书如采金，要沙里淘金"用了什么论证方法？<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">比喻论证。把读书比作采金，把书中精华比作金子，生动形象地论证了读书要善于筛选、提取精华。</div></div>
<div class="q-block"><b>文言文翻译</b>："先天下之忧而忧，后天下之乐而乐"<button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">在天下人忧愁之前先忧愁，在天下人快乐之后才快乐。——范仲淹的忧乐观，表达了以天下为己任的抱负。</div></div>
</div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（10min）</h4><p>📔 默写四大论证方法及各自的答题模板 📔 找出范文中的论点和论据</p></div>`
  }
};

// 英语语法内容库
const ENGLISH = {
  // W1 Day 1: 一般现在时 (already present in some form)
  w1_D1_extra: {
    title: '🔤 英语 · 一般现在时（1h）',
    content: `<div class="step"><h4><span class="dot" style="background:var(--green)"></span>讲（15min）</h4>
<p><b>一般现在时</b>——表示经常性、习惯性的动作或客观真理。</p>
<p>结构：<b>主语 + 动词原形/动词+s(es)</b>（第三人称单数加s/es）</p>
<p>标志词：always, usually, often, sometimes, every day/week/month, never</p>
<p><b>三单变化规则</b>：①一般+s：work→works ②以s/x/sh/ch/o结尾+es：watch→watches, go→goes ③辅音+y结尾变y为i+es：study→studies</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（30min）</h4>
<div class="q-block"><span class="q-num">1.</span><span class="question">She ___ (go) to school by bus every day.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">goes（第三人称单数，go→goes）</div></div>
<div class="q-block"><span class="q-num">2.</span><span class="question">They ___ (not like) math. Math ___ (be) difficult.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">don't like; is（they是复数用don't，math是不可数名词用is）</div></div>
<div class="q-block"><span class="q-num">3.</span><span class="question">___ your father ___ (work) in a hospital?</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">Does; work（三单疑问句用Does，动词恢复原形）</div></div>
<div class="q-block"><span class="q-num">4.</span><span class="question">The sun ___ (rise) in the east.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">rises（客观真理用一般现在时，不加任何时间限制）</div></div>
</div></div>`
  },
  // W1 Day 3: 一般过去时
  w1_D3_eng: {
    title: '🔤 英语 · 一般过去时（1h）',
    content: `<div class="step"><h4><span class="dot" style="background:var(--green)"></span>讲（15min）</h4>
<p><b>一般过去时</b>——表示过去某个时间发生的动作或状态。</p>
<p>结构：<b>主语 + 动词过去式</b></p>
<p>标志词：yesterday, last week/month/year, ...ago, in 2020, just now</p>
<p><b>动词过去式变化</b>：①规则动词+ed（play→played, study→studied, stop→stopped）②不规则动词必须逐个背！</p>
<p><b>常见不规则动词</b>（中考必考15个）：go→went, do→did, have→had, see→saw, eat→ate, come→came, get→got, make→made, take→took, give→gave, buy→bought, think→thought, write→wrote, read→read(读音变), fly→flew</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（30min）</h4>
<div class="q-block"><span class="q-num">1.</span><span class="question">I ___ (go) to Beijing last summer.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">went（一般过去时，go→went）</div></div>
<div class="q-block"><span class="q-num">2.</span><span class="question">He ___ (not see) the movie yesterday.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">didn't see（过去时否定：didn't + 动词原形！易错：很多人写成didn't saw）</div></div>
<div class="q-block"><span class="q-num">3.</span><span class="question">Where ___ you ___ (go) last night?</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">did; go（疑问句：Did + 主语 + 动词原形）</div></div>
<div class="q-block"><span class="q-num">4.</span><span class="question">She ___ (read) three books last month.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">read /red/（read的过去式写法不变但读音变，read/riːd/→read/red/）</div></div>
</div></div>`
  },
  // W3 Day 15 英语: 现在完成时
  w3_D15_eng: {
    title: '🔤 英语 · 现在完成时（1h）',
    content: `<div class="step"><h4><span class="dot" style="background:var(--green)"></span>讲（20min）</h4>
<p><b>⭐ 现在完成时</b>——连接过去和现在的时态，中考必考！</p>
<p>结构：<b>主语 + have/has + 过去分词</b></p>
<p>标志词：already(已经), yet(还/已经), ever(曾经), never(从未), just(刚刚), since+时间点, for+时间段, so far(到目前为止)</p>
<p><b>两种核心用法</b>：</p>
<p>①<b>过去的动作对现在有影响</b>：I have lost my key. (钥匙丢了→现在进不去门)</p>
<p>②<b>从过去持续到现在</b>：I have lived here for 10 years. (现在仍住在这里)</p>
<p><b>have been to vs have gone to</b>：been to去过(已回来)，gone to去了(还没回来)</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（25min）</h4>
<div class="q-block"><span class="q-num">1.</span><span class="question">I ___ (finish) my homework already.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">have finished（already用于现在完成时）</div></div>
<div class="q-block"><span class="q-num">2.</span><span class="question">She ___ (live) in Taizhou since 2015.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">has lived（since+时间点，用现在完成时）</div></div>
<div class="q-block"><span class="q-num">3.</span><span class="question">He ___ (be) to Beijing twice. He ___ (go) to Nanjing and will be back next week.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">has been; has gone（has been to去过已回；has gone to去了未回）</div></div>
<div class="q-block"><span class="q-num">4.</span><span class="question">I ___ (not see) him since last Monday.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">haven't seen（since+过去时间点，主句用现在完成时）</div></div>
</div></div>`
  },
  // W3 Day 17 英语: 宾语从句
  w3_D17_eng: {
    title: '🔤 英语 · 宾语从句（1h）',
    content: `<div class="step"><h4><span class="dot" style="background:var(--green)"></span>讲（20min）</h4>
<p><b>宾语从句三要素</b>：连接词 + 语序 + 时态</p>
<p><b>1. 连接词</b>：</p>
<p>①that（陈述句作从句，无意义可省略）：I think (that) he is right.</p>
<p>②if/whether（一般疑问句作从句）：I don't know if he will come.</p>
<p>③wh-词（特殊疑问句作从句）：Can you tell me where he lives?</p>
<p><b>2. 语序</b>：从句永远用<b>陈述语序（主语+谓语）</b>！</p>
<p>❌ Can you tell me where does he live? → ✅ Can you tell me where he lives?</p>
<p><b>3. 时态呼应</b>：主句现在时→从句任意时态；主句过去时→从句用相应的过去时态；客观真理永远用一般现在时</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（25min）</h4>
<div class="q-block"><span class="q-num">1.</span><span class="question">I don't know ___. A. where he lives B. where does he live</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">A。宾语从句用陈述语序（where he lives），B是疑问语序错误。</div></div>
<div class="q-block"><span class="q-num">2.</span><span class="question">She said that the earth ___ (go) around the sun.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">goes（主句said是过去时，但"地球绕太阳转"是客观真理，不受时态呼应规则限制，永远用一般现在时）</div></div>
<div class="q-block"><span class="q-num">3.</span><span class="question">Could you tell me ___? A. what time is it B. what time it is</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">B。宾语从句语序：连接词+主语+谓语，即what time it is。</div></div>
</div></div>`
  },
  // W6 Day 36 英语: 被动语态
  w6_D36_eng: {
    title: '🔤 英语 · 被动语态（1h）',
    content: `<div class="step"><h4><span class="dot" style="background:var(--green)"></span>讲（20min）</h4>
<p><b>被动语态</b>——强调动作的承受者而非执行者。</p>
<p>结构：<b>主语 + be + 过去分词 (+ by + 动作执行者)</b></p>
<p><b>各种时态的被动</b>：</p>
<p>一般现在：am/is/are + done → The classroom is cleaned every day.</p>
<p>一般过去：was/were + done → The window was broken yesterday.</p>
<p>一般将来：will be + done → The work will be finished soon.</p>
<p>现在完成：have/has been + done → The letter has been sent.</p>
<p>含情态动词：can/must/should + be + done → Homework must be handed in on time.</p>
<p><b>不能变被动的情况</b>：不及物动词（happen, arrive, die）、系动词（be, feel, look）</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（25min）</h4>
<div class="q-block"><span class="q-num">1.</span><span class="question">English ___ (speak) all over the world.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">is spoken（一般现在时被动：is + spoken）</div></div>
<div class="q-block"><span class="q-num">2.</span><span class="question">The bridge ___ (build) in 2010.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">was built（过去时间in 2010→一般过去时被动：was + built）</div></div>
<div class="q-block"><span class="q-num">3.</span><span class="question">The meeting ___ (hold) next Monday.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">will be held（将来时间→一般将来时被动：will be + held）</div></div>
<div class="q-block"><span class="q-num">4.</span><span class="question">The classroom must ___ (clean) every day.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">be cleaned（情态动词被动：must + be + 过去分词）</div></div>
</div></div>`
  },
  // W7 Day 44 英语: 定语从句
  w7_D44_eng: {
    title: '🔤 英语 · 定语从句（1h）',
    content: `<div class="step"><h4><span class="dot" style="background:var(--green)"></span>讲（20min）</h4>
<p><b>定语从句</b>——修饰名词或代词的从句，被修饰的词叫"先行词"。</p>
<p><b>关系代词</b>：</p>
<p>who（指人，作主语/宾语）：The girl who is singing is my sister.</p>
<p>whom（指人，作宾语，正式）：The man whom you met is my teacher.</p>
<p>which（指物，作主语/宾语）：The book which is on the desk is mine.</p>
<p>that（指人或物，作主语/宾语，最通用）：I like the movie that you recommended.</p>
<p>whose（指人或物，表所属）：The boy whose father is a doctor is my classmate.</p>
<p><b>只用that不用which的情况</b>（中考常考！）：先行词有最高级/序数词/all/anything/nothing/the only/the very等修饰时 → 只用that！</p>
</div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（25min）</h4>
<div class="q-block"><span class="q-num">1.</span><span class="question">This is the best movie ___ I have ever seen. A. which B. that</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">B。先行词有最高级best修饰，只用that不用which。</div></div>
<div class="q-block"><span class="q-num">2.</span><span class="question">The girl ___ is wearing a red dress is my cousin. A. who B. which</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">A。先行词the girl指人，用who。</div></div>
<div class="q-block"><span class="q-num">3.</span><span class="question">I still remember the day ___ we first met.</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">when（先行词the day表时间，关系副词when引导定语从句）</div></div>
</div></div>`
  }
};

// ===== INJECTION LOGIC =====

function injectContent(html, searchPattern, newContent) {
  // Find the injection point and insert before it
  if (html.includes(searchPattern)) {
    return html.replace(searchPattern, newContent + '\n' + searchPattern);
  }
  return html;
}

// Find the correct injection point for a day section
// We inject additional subject sections BEFORE the English vocabulary box OR before the check div
function findInjectionPoint(dayContent) {
  // Try to find the English word box (gray box with 今日30词)
  let idx = dayContent.indexOf('今日30词');
  if (idx > 0) {
    // Find the opening <div style="background:#f0f0f5..."> before 今日30词
    let before = dayContent.substring(0, idx);
    let grayBoxStart = before.lastIndexOf('<div style="background:#f0f0f5');
    if (grayBoxStart > 0) {
      return grayBoxStart;
    }
  }
  // Fallback: inject before check div
  idx = dayContent.indexOf('<div class="check">');
  if (idx > 0) {
    return idx;
  }
  // Last resort: inject before closing </div></div> of day-page
  return dayContent.lastIndexOf('</div></div>');
}

function processFile(filePath) {
  let html = fs.readFileSync(filePath, 'utf8');
  let modified = false;
  
  // Process each day-page
  let dayPages = html.split('<!-- DAY ');
  if (dayPages.length < 2) {
    // Try alternative split
    let parts = html.split('<div class="day-page">');
    if (parts.length < 2) {
      console.log(`  No day pages found in ${filePath}`);
      return false;
    }
  }
  
  // Get the HTML content and find all day sections
  // For each day with specific subjects, inject missing content
  
  // Strategy: find each day-page div and process individually
  let result = html;
  
  // ===== Process specific days =====
  
  // W1 Day 3: 数学+英语+语文 - needs 语文 (古诗文+文言文) + 英语语法 (一般过去时)
  if (filePath.includes('w1.html')) {
    let day3Start = result.indexOf('<div class="dnum">Day 3</div>');
    if (day3Start > 0) {
      let day3Section = result.substring(day3Start);
      let nextDay = day3Section.indexOf('<div class="dnum">Day 4</div>');
      if (nextDay > 0) day3Section = day3Section.substring(0, nextDay);
      
      // Check if 语文 section already exists
      if (!day3Section.includes('📖 语文') && !day3Section.includes('📖.*语文')) {
        let injectIdx = findInjectionPoint(day3Section);
        if (injectIdx > 0) {
          let absInject = day3Start + injectIdx;
          // Add Chinese section before English word box
          let chiBlock = '<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:20px 0 12px">' + CHINESE.w1_D3.title + '</h3>' + CHINESE.w1_D3.content;
          result = result.substring(0, absInject) + '\n' + chiBlock + '\n' + result.substring(absInject);
          modified = true;
          console.log('  + Day 3: 添加语文(古诗文+文言文入门)');
          
          // Recalculate positions after insertion
          day3Start = result.indexOf('<div class="dnum">Day 3</div>');
          day3Section = result.substring(day3Start);
          nextDay = day3Section.indexOf('<div class="dnum">Day 4</div>');
          if (nextDay > 0) day3Section = day3Section.substring(0, nextDay);
        }
      }
      
      // Add English grammar (一般过去时) if only word box exists
      if (day3Section.includes('今日30词') && !day3Section.includes('一般过去时') && !day3Section.includes('过去时')) {
        let injectIdx = findInjectionPoint(day3Section);
        if (injectIdx > 0) {
          let absInject = day3Start + injectIdx;
          let engBlock = '<h3 style="color:var(--green);border-bottom:2px solid var(--green);padding-bottom:6px;margin:20px 0 12px">' + ENGLISH.w1_D3_eng.title + '</h3>' + ENGLISH.w1_D3_eng.content;
          result = result.substring(0, absInject) + '\n' + engBlock + '\n' + result.substring(absInject);
          modified = true;
          console.log('  + Day 3: 添加英语(一般过去时)');
        }
      }
    }
  }
  
  // W3 Day 15: 数学+物理+英语+语文 - needs 语文(文言文) + 英语(现在完成时)
  if (filePath.includes('w3.html')) {
    let day15Start = result.indexOf('<div class="dnum">Day 15</div>');
    if (day15Start > 0) {
      let day15Section = result.substring(day15Start);
      let nextDay = day15Section.indexOf('<div class="dnum">Day 16</div>');
      if (nextDay > 0) day15Section = day15Section.substring(0, nextDay);
      
      if (!day15Section.includes('文言文') && !day15Section.includes('《论语》')) {
        let injectIdx = findInjectionPoint(day15Section);
        if (injectIdx > 0) {
          let absInject = day15Start + injectIdx;
          let chiBlock = '<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:20px 0 12px">' + CHINESE.w3_D15.title + '</h3>' + CHINESE.w3_D15.content;
          result = result.substring(0, absInject) + '\n' + chiBlock + '\n' + result.substring(absInject);
          modified = true;
          console.log('  + Day 15: 添加语文(文言文阅读)');
        }
      }
      
      if (day15Section.includes('今日30词') && !day15Section.includes('现在完成时') && !day15Section.includes('have done')) {
        let injectIdx = findInjectionPoint(day15Section);
        if (injectIdx > 0) {
          let absInject = day15Start + injectIdx;
          let engBlock = '<h3 style="color:var(--green);border-bottom:2px solid var(--green);padding-bottom:6px;margin:20px 0 12px">' + ENGLISH.w3_D15_eng.title + '</h3>' + ENGLISH.w3_D15_eng.content;
          result = result.substring(0, absInject) + '\n' + engBlock + '\n' + result.substring(absInject);
          modified = true;
          console.log('  + Day 15: 添加英语(现在完成时)');
        }
      }
    }
    
    // W3 Day 17: 数学+物理+英语+语文 - needs 语文(现代文阅读) + 英语(宾语从句)
    let day17Start = result.indexOf('<div class="dnum">Day 17</div>');
    if (day17Start > 0) {
      let day17Section = result.substring(day17Start);
      let nextDay = day17Section.indexOf('<div class="dnum">Day 18</div>');
      if (nextDay > 0) day17Section = day17Section.substring(0, nextDay);
      
      if (day17Section.includes('今日30词') && !day17Section.includes('散文阅读') && !day17Section.includes('现代文')) {
        let injectIdx = findInjectionPoint(day17Section);
        if (injectIdx > 0) {
          let absInject = day17Start + injectIdx;
          let chiBlock = '<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:20px 0 12px">' + CHINESE.w3_D17.title + '</h3>' + CHINESE.w3_D17.content;
          result = result.substring(0, absInject) + '\n' + chiBlock + '\n' + result.substring(absInject);
          modified = true;
          console.log('  + Day 17: 添加语文(现代文阅读)');
          
          // Recalculate
          day17Start = result.indexOf('<div class="dnum">Day 17</div>');
          day17Section = result.substring(day17Start);
          nextDay = day17Section.indexOf('<div class="dnum">Day 18</div>');
          if (nextDay > 0) day17Section = day17Section.substring(0, nextDay);
        }
      }
      
      if (day17Section.includes('今日30词') && !day17Section.includes('宾语从句')) {
        let injectIdx = findInjectionPoint(day17Section);
        if (injectIdx > 0) {
          let absInject = day17Start + injectIdx;
          let engBlock = '<h3 style="color:var(--green);border-bottom:2px solid var(--green);padding-bottom:6px;margin:20px 0 12px">' + ENGLISH.w3_D17_eng.title + '</h3>' + ENGLISH.w3_D17_eng.content;
          result = result.substring(0, absInject) + '\n' + engBlock + '\n' + result.substring(absInject);
          modified = true;
          console.log('  + Day 17: 添加英语(宾语从句)');
        }
      }
    }
  }
  
  // W4 Day 23: 数学+政治+语文 - already has some 语文, add more
  if (filePath.includes('w4.html')) {
    let day23Start = result.indexOf('<div class="dnum">Day 23</div>');
    if (day23Start > 0) {
      let day23Section = result.substring(day23Start);
      let nextEnd = day23Section.indexOf('</div></div>');
      if (nextEnd > 0) day23Section = day23Section.substring(0, nextEnd + 12);
      
      if (!day23Section.includes('留换补删调') && !day23Section.includes('五字诀')) {
        let injectIdx = findInjectionPoint(day23Section);
        if (injectIdx > 0) {
          let absInject = day23Start + injectIdx;
          let chiBlock = '<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:20px 0 12px">' + CHINESE.w4_D23_extra.title + '</h3>' + CHINESE.w4_D23_extra.content;
          result = result.substring(0, absInject) + '\n' + chiBlock + '\n' + result.substring(absInject);
          modified = true;
          console.log('  + Day 23: 添加语文(文言文翻译技巧)');
        }
      }
    }
  }
  
  // W6 Day 36: 数学+物理+英语+语文 - add 作文 + 英语被动语态
  if (filePath.includes('w6.html')) {
    let day36Start = result.indexOf('<div class="dnum">Day 36</div>');
    if (day36Start > 0) {
      let day36Section = result.substring(day36Start);
      let nextEnd = day36Section.indexOf('</div></div>');
      if (nextEnd > 0) day36Section = day36Section.substring(0, nextEnd + 12);
      
      if (!day36Section.includes('记叙文') && !day36Section.includes('凤头')) {
        let injectIdx = findInjectionPoint(day36Section);
        if (injectIdx > 0) {
          let absInject = day36Start + injectIdx;
          let chiBlock = '<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:20px 0 12px">' + CHINESE.w6_D36_extra.title + '</h3>' + CHINESE.w6_D36_extra.content;
          result = result.substring(0, absInject) + '\n' + chiBlock + '\n' + result.substring(absInject);
          modified = true;
          console.log('  + Day 36: 添加语文(记叙文写作)');
          
          day36Start = result.indexOf('<div class="dnum">Day 36</div>');
          day36Section = result.substring(day36Start);
          nextEnd = day36Section.indexOf('</div></div>');
          if (nextEnd > 0) day36Section = day36Section.substring(0, nextEnd + 12);
        }
      }
      
      if (day36Section.includes('今日30词') && !day36Section.includes('被动语态') && !day36Section.includes('be done')) {
        let injectIdx = findInjectionPoint(day36Section);
        if (injectIdx > 0) {
          let absInject = day36Start + injectIdx;
          let engBlock = '<h3 style="color:var(--green);border-bottom:2px solid var(--green);padding-bottom:6px;margin:20px 0 12px">' + ENGLISH.w6_D36_eng.title + '</h3>' + ENGLISH.w6_D36_eng.content;
          result = result.substring(0, absInject) + '\n' + engBlock + '\n' + result.substring(absInject);
          modified = true;
          console.log('  + Day 36: 添加英语(被动语态)');
        }
      }
    }
  }
  
  // W7 Day 44: 英语+语文 - needs 语文(议论文) + 英语(定语从句)
  if (filePath.includes('w7.html')) {
    let day44Start = result.indexOf('<div class="dnum">Day 44</div>');
    if (day44Start > 0) {
      let day44Section = result.substring(day44Start);
      let nextEnd = day44Section.indexOf('</div></div>');
      if (nextEnd > 0) day44Section = day44Section.substring(0, nextEnd + 12);
      
      if (!day44Section.includes('议论文')) {
        let injectIdx = findInjectionPoint(day44Section);
        if (injectIdx > 0) {
          let absInject = day44Start + injectIdx;
          let chiBlock = '<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:20px 0 12px">' + CHINESE.w7_D44_extra.title + '</h3>' + CHINESE.w7_D44_extra.content;
          result = result.substring(0, absInject) + '\n' + chiBlock + '\n' + result.substring(absInject);
          modified = true;
          console.log('  + Day 44: 添加语文(议论文阅读)');
          
          day44Start = result.indexOf('<div class="dnum">Day 44</div>');
          day44Section = result.substring(day44Start);
          nextEnd = day44Section.indexOf('</div></div>');
          if (nextEnd > 0) day44Section = day44Section.substring(0, nextEnd + 12);
        }
      }
      
      if (day44Section.includes('今日30词') && !day44Section.includes('定语从句') && !day44Section.includes('先行词')) {
        let injectIdx = findInjectionPoint(day44Section);
        if (injectIdx > 0) {
          let absInject = day44Start + injectIdx;
          let engBlock = '<h3 style="color:var(--green);border-bottom:2px solid var(--green);padding-bottom:6px;margin:20px 0 12px">' + ENGLISH.w7_D44_eng.title + '</h3>' + ENGLISH.w7_D44_eng.content;
          result = result.substring(0, absInject) + '\n' + engBlock + '\n' + result.substring(absInject);
          modified = true;
          console.log('  + Day 44: 添加英语(定语从句)');
        }
      }
    }
  }
  
  if (modified) {
    fs.writeFileSync(filePath, result, 'utf8');
    return true;
  }
  return false;
}

// ===== MAIN =====
console.log('开始补充语文、英语等学科内容...\n');

const files = ['w1.html', 'w2.html', 'w3.html', 'w4.html', 'w5.html', 'w6.html', 'w7.html', 'w8.html', 'w9.html'];

let totalModified = 0;
for (const f of files) {
  console.log(`处理 ${f}...`);
  if (processFile(f)) {
    totalModified++;
    console.log(`  ✅ ${f} 已更新`);
  } else {
    console.log(`  - ${f} 无需修改`);
  }
}

console.log(`\n完成！共修改 ${totalModified} 个文件。`);
