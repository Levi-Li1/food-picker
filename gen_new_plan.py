#!/usr/bin/env python3
"""Generate sample Week 1 for review. Outputs to w1-new.html"""
import os

# Helpers
CH = {'b':'var(--blue)','o':'var(--orange)','g':'var(--green)','p':'var(--purple)','r':'var(--red)','l':'#9c27b0','k':'#795548','e':'#e91e63'}
RNAME = {'b':'数学','o':'物理','g':'英语','p':'化学','r':'语文','l':'政治','k':'历史'}

def h3(c,e,t): return f'<h3 style="color:{CH[c]};border-bottom:2px solid {CH[c]};padding-bottom:6px;margin:16px 0 12px">{e} {t}</h3>'
def sh(t,c,b,f=False): return f'<div class="step{" full" if f else ""}"><h4><span class="dot" style="background:{CH[c]}"></span>{t}</h4>{b}</div>'
def sts(*a): return f'<div class="steps">{"".join(a)}</div>'
def qb(n,q,a): return f'<div class="q-block"><span class="q-num">{n}.</span><span class="question">{q}</span><button class="ans-btn" onclick="showAns(this)">点击查看答案</button><div class="answer">{a}</div></div>'
def qbs(its): return ''.join(qb(n,q,a) for n,q,a in its)
def tip(t): return f'<div class="tip"><b>方法</b>：{t}</div>'
def trap(t): return f'<div class="err-box"><b>易错</b>：{t}</div>'

def recite_table(items):
    rows = ''.join(f'<tr><td>{r}</td><td>□ □</td></tr>' for r in items)
    return f'<table class="summ-table"><tr><th>默写内容</th><th>已背/已默</th></tr>{rows}</table>'

def vocab_block(items):
    h = '<div style="background:#f0f0f5;border-radius:10px;padding:12px 16px;margin:10px 0;border:1px solid #e5e5ea"><p style="margin:0 0 8px 0"><b>今日单词</b></p>'
    for i,(w,p,m) in enumerate(items):
        h += f'<div style="display:flex;align-items:baseline;gap:8px;padding:4px 0;border-bottom:1px solid #eee;font-size:13px"><span style="color:#999;min-width:24px;font-size:11px">{i+1}.</span><b style="color:#1d1d1f;min-width:80px">{w}</b><span style="color:var(--sub);font-size:12px;min-width:60px">{p}</span><span style="color:var(--green);min-width:30px">{m}</span></div>'
    return h+'</div>'

def day(num,date,wd,subj,goal,body,check):
    return f'''
<div class="day-page" id="d{num}"><div class="dtop"><div class="dnum">Day {num}</div><div class="dinfo"><div>{date} {wd}</div><div style="font-size:12px">{subj}</div></div></div>
<div class="dbody">
<div class="goal"><b>今日目标</b>：{goal}</div>
{body}
<div class="check"><b>今日达标检查</b>（睡前逐条确认）：<br>{check}</div>
</div></div>'''

def rest_day(date):
    return f'<div class="day-page" style="border:2px dashed #ddd;background:#f9f9fb"><div class="dbody" style="text-align:center;padding:30px"><p style="font-size:18px;color:#999">{date} 周日休息日</p><p style="font-size:13px;color:#bbb">复习本周错题 - 整理笔记 - 户外活动 - 阅读课外书 - 预习下周内容</p></div></div>'

# ═══════ WEEK 1: 数学有理数+英语字母/问候+语文古诗 ═══════
out = '''<div class="week-marker" id="w1">第一周（7月6日-11日）<div class="wnote">主题：数学有理数入门 - 英语字母与问候 - 古诗文基础 - 每天学习4h(数学1.5h+英语1.5h+语文1h)</div></div>
'''

# DAY 1 ── 负数/数轴 + 字母表 + 观沧海
d1_body = ''

d1_body += h3('b','\U0001f4d6','数学 - 认识负数与数轴（1.5h）')
d1_body += sts(
sh('讲（25min）','b','''<p><b>什么是负数？</b>比0小的数就是负数！</p><p>生活中常见的负数：温度零下3度记作-3度、欠别人5元记作-5元、海拔低于海平面记作负数。</p><p><b>数轴三要素</b>：原点(0) + 正方向(箭头) + 单位长度(等距离)</p><p>数轴上，右边的数 > 左边的数。负数在0的左边，正数在0的右边。</p>''',True),

sh('A组基础（10min）','g',qbs([(1,"下列哪个是负数? A.5 B.0 C.-3 D.1/2","C.-3"),
(2,"零下5度怎么表示?","-5度"),
(3,"收入20元记作+20,支出15元记作?","-15元"),
(4,"-2,3,0从小到大排列","-2<0<3"),
(5,"在数轴上1在-3的哪边?","右边"),
(6,"海拔-100米比0米高还是低?","低"),
(7,"-1和-3哪个更大?","-1更大(离0更近)"),
(8,"数轴三要素是什么?","原点,正方向,单位长度")])),

sh('B组进阶（10min）','o',qbs([(9,"画数轴标出-3,-1,0,2,4","略(从左到右依次排列)"),
(10,"-5到3之间有几个整数?","9个:-5,-4,-3,-2,-1,0,1,2,3")])),

sh('C组真题（10min）','r',qbs([(11,"【2023泰州】-2的相反数是 A.2 B.-2 C.+-2","A.2")])),

sh('方法总结（5min）','p',tip("负数<0<正数。数轴上右边大于左边。相反数就是符号相反的两个数(和为零)。")+trap("不要把负号和减号混淆!-3读作负三不是减三"),True)
)

d1_body += h3('g','\U0001f527','英语 - 26个字母和基本发音（1.5h）')
d1_body += sts(
sh('讲（20min）','g','''<p><b>26个字母</b></p><p>元音字母(5个): Aa Ee Ii Oo Uu</p><p>辅音字母(21个): Bb Cc Dd Ff Gg Hh Jj Kk Ll Mm Nn Pp Qq Rr Ss Tt Vv Ww Xx Yy Zz</p><p>字母发音口诀:A/ei/ B/bi/ C/si/ D/di/ E/i/ F/ef/ G/dʒi/ H/eitʃ/ I/ai/ J/dʒei/ K/kei/ L/el/ M/em/ N/en/ O/əu/ P/pi/ Q/kju/ R/ɑ/ S/es/ T/ti/ U/ju/ V/vi/ W/dʌblju/ X/eks/ Y/wai/ Z/zed/</p>''',True),

sh('练（15min）','o',qbs([(1,"默写字母表前10个","A B C D E F G H I J"),
(2,"5个元音字母是?","A E I O U"),(3,"字母b的发音?","bi:"),
(4,"cat由哪三个字母组成?","C-A-T"),(5,"字母表共多少个字母?","26个"),
(6,"按顺序填空:K_L_N","K L M N")])),

sh('总结（5min）','p',tip("元音字母是英语的灵魂。每天背诵字母表5遍,一周内达到脱口而出。"),True)
)

d1_body += vocab_block([('apple','苹果',''),('book','书',''),('cat','猫',''),('dog','狗',''),('egg','鸡蛋','')])

d1_body += h3('r','\U0001f4d6','语文 - 古诗文入门:观沧海（1h）')
d1_body += sts(
sh('讲（20min）','r','''<p><b>观沧海</b> - 曹操(汉末)</p><p>东临碣石,以观沧海。水何澹澹,山岛竦峙。树木丛生,百草丰茂。秋风萧瑟,洪波涌起。日月之行,若出其中。星汉灿烂,若出其里。幸甚至哉,歌以咏志。</p><p><b>逐句翻译</b>:</p><p>东行登上碣石山来观赏大海。海水多么宽阔浩荡,山岛高高耸立。树木百草十分茂盛。秋风吹动,海中涌起巨浪。太阳和月亮的运行好像从大海中升起。银河星光灿烂好像从大海中产生。太值得庆幸了,用诗歌来表达心志。</p>''',True),

sh('练（15min）','o',qbs([(1,"水何澹澹中澹澹的意思?","水波荡漾"),
(2,"描写草木茂盛的句子?","树木丛生,百草丰茂"),
(3,"星汉指的是什么?","银河"),
(4,"曹操表达什么情感?","博大的胸襟和远大的抱负")])),

sh('总结（5min）','p',tip("古诗背诵三遍法:看译文理解-逐句背诵-闭眼默背。默写时注意字不能写错!"),True),

sh('背诵默写（15min）','r',recite_table(["观沧海全诗背诵","重点字:澹澹/竦峙/星汉/志","曹操背景常识"]),True)
)

out += day(1,"7月6日","周一","数学+英语+语文","负数概念+数轴+字母表+观沧海",d1_body,
          "负数定义背出来 - 字母表会背会写 - 观沧海能默写")

# DAY 2 ── 相反数/绝对值 + 日常问候 + 论语
d2_body = ''
d2_body += h3('b','\U0001f4d6','数学 - 相反数与绝对值（1.5h）')
d2_body += sts(
sh('讲（25min）','b','''<p><b>相反数</b>：符号相反的两个数。3和-3是相反数,它们的和=0。0的相反数是0。</p><p><b>绝对值</b>：数轴上一个数到原点的"距离",用|a|表示。距离一定是正数或0。</p><p>|3|=3,|-3|=3,|0|=0。</p><p>绝对值的重要性质：|a| >= 0 (绝对值不可能是负数!)</p>''',True),

sh('A组基础（10min）','g',qbs([(1,"5的相反数是?","-5"),(2,"-8的相反数是?","8"),
(3,"|7|=?","7"),(4,"|-7|=?","7"),(5,"|0|=?","0"),
(6,"相反数等于本身的数是?","0"),(7,"|-5|和|3|比较","5>3"),
(8,"若|x|=5,x=?","x=5或x=-5")])),

sh('B组进阶（10min）','o',qbs([(9,"比较:-5__-3(填>或<)","-5<-3"),
(10,"若|a|=|b|,a和b什么关系?","a=b或a=-b")])),

sh('C组真题（10min）','r',qbs([(11,"【2024泰州】-2的绝对值 A.-2 B.2 C.+-2","B.2"),
(12,"【2023泰州】-(-3)结果 A.-3 B.3 C.+-3","B.3")])),

sh('总结（5min）','p',tip("相反数:和为0。绝对值:距离>=0。|x|=a -> x=+-a(两个解!)")+trap("|x|=5的解有5和-5两个,不要只写一个!"),True)
)

d2_body += h3('g','\U0001f527','英语 - 日常问候语（1.5h）')
d2_body += sts(
sh('讲（20min）','g','''<p><b>打招呼</b>: Hello! Hi! Good morning!(中午前) Good afternoon!(下午) Good evening!(晚上)</p><p><b>告别</b>: Goodbye! See you! See you tomorrow!</p><p><b>礼貌用语</b>: Thank you!/Thanks! Sorry!/Im sorry. Please. Youre welcome. Excuse me.</p>''',True),

sh('练（20min）','o',qbs([(1,"早上见老师说什么?","Good morning!"),
(2,"别人说Thank you回答?","You are welcome."),
(3,"不小心碰到别人说?","Sorry!"),(4,"放学道别说?","Goodbye!"),
(5,"问路前先说?","Excuse me."),
(6,"用英语自我介绍:我叫Lucy,13岁","My name is Lucy. I am 13.")])),

sh('总结（5min）','p',tip("英语礼貌用语要养成习惯。见到人说Hi,谢谢说Thank you,对不起说Sorry。"),True)
)

d2_body += vocab_block([('hello','你好',''),('goodbye','再见',''),('thank','谢谢',''),('sorry','对不起',''),('please','请','')])

d2_body += h3('r','\U0001f4d6','语文 - 论语十二章选讲（1h）')
d2_body += sts(
sh('讲（20min）','r','''<p><b>论语</b>：记录孔子言行的书。</p><p><b>第一则</b>：学而时习之,不亦说乎?有朋自远方来,不亦乐乎?人不知而不愠,不亦君子乎?</p><p>翻译:学习了按时复习,不是很愉快吗?有朋友从远方来,不是很快乐吗?别人不了解我但我也不生气,不是君子吗?</p><p><b>第二则</b>：温故而知新,可以为师矣。翻译:温习旧知识得到新理解,可以当老师了。</p><p>重点字:说=悦(通假)、时=按时、愠=生气</p>''',True),

sh('练（15min）','o',qbs([(1,"不亦说乎中说通哪个字?","通悦,愉快"),
(2,"学而时习之中时怎么解释?","按时"),
(3,"温故而知新的道理?","复习旧知识获得新理解"),
(4,"人不知而不愠的愠的意思?","生气")])),

sh('总结（5min）','p',tip("通假字:读音和现在不一样-可能通假。常见:说通悦,女通汝。"),True),

sh('背诵默写（15min）','r',recite_table(["论语第一则背诵","论语第二则背诵","通假字:说=悦"]),True)
)  # close sts

out += day(2,"7月7日","周二","数学+英语+语文","相反数绝对值+英语问候+论语",d2_body,
          "相反数绝对值概念 - 5句英语问候 - 论语前两则口译")

# DAY 3 ── 有理数加减 + be动词 + 天净沙
d3_body = ''
d3_body += h3('b','\U0001f4d6','数学 - 有理数加减法（1.5h）')
d3_body += sts(
sh('讲（25min）','b','''<p><b>同号相加</b>:绝对值相加,符号不变。(-3)+(-5)=-(3+5)=-8</p><p><b>异号相加</b>:绝对值大的减小的,符号跟大的走。(-7)+3=-(7-3)=-4</p><p><b>减法变加法</b>:a-b=a+(-b)。5-(-3)=5+3=8; -4-2=-4+(-2)=-6</p>''',True),

sh('A组（10min）','g',qbs([(1,"(-15)+(-3)=?","-18"),(2,"8+(-3)=?","5"),
(3,"(-7)+12=?","5"),(4,"(-5)-3=?","-8"),
(5,"0-(-6)=?","6(0减负6等于加6)"),
(6,"(-8)-(-3)=?","-5"),(7,"(-2)+(-4)-(-1)=?","-5")])),

sh('B组（10min）','o',qbs([(8,"(-8)-(-3)+(-2)=?","(-8)+3+(-2)=-7"),
(9,"温度从-5度升到3度上升多少?","3-(-5)=8度")])),

sh('C组（10min）','r',qbs([(10,"【2024泰州】(-2)+3-(-4)=?","(-2)+3+4=5")])),

sh('总结（5min）','p',tip("减法变加法:a-b=a+(-b)。同号相加符号不变,异号相加符号跟大走。")+trap("(-5)-3=-8不是-2!减法不能直接减绝对值"),True)
)

d3_body += h3('g','\U0001f527','英语 - be动词:am/is/are（1.5h）')
d3_body += sts(
sh('讲（20min）','g','''<p><b>be动词三兄弟</b>:</p><p>I am (我是) - I am a student.</p><p>He/She/It is (他/她/它是) - He is a boy. She is a girl. It is a cat.</p><p>You/We/They are (你/我们/他们是) - You are a teacher. We are friends. They are students.</p><p><b>否定句</b>：在be动词后加not。I am not a teacher.</p>''',True),

sh('练（20min）','o',qbs([(1,"I ___ a boy.","am"),(2,"She ___ a girl.","is"),
(3,"They ___ students.","are"),(4,"I am a student变否定","I am not a student."),
(5,"He is a teacher.变否定","He is not a teacher."),
(6,"用be动词填空:We ___ happy.","are"),(7,"翻译:她是一个好学生。","She is a good student.")])),

sh('总结（5min）','p',tip("I用am,he/she/it用is,you/we/they用are。否定加not。"),True)
)

d3_body += vocab_block([('student','学生',''),('teacher','老师',''),('friend','朋友',''),('happy','快乐的',''),('good','好的','')])

d3_body += h3('r','\U0001f4d6','语文 - 天净沙秋思（1h）')
d3_body += sts(
sh('讲（20min）','r','''<p><b>天净沙秋思</b> - 马致远(元代)</p><p>枯藤老树昏鸦,小桥流水人家,古道西风瘦马。夕阳西下,断肠人在天涯。</p><p><b>赏析</b>:前三句全用名词堆叠,画面感极强。小桥流水人家(温馨)反衬断肠人在天涯(孤独)。</p>''',True),

sh('练（10min）','o',qbs([(1,"全曲表达什么情感?","游子思乡的悲苦"),
(2,"小桥流水人家和断肠人在天涯的关系?","反衬,别人家温馨自己却漂泊"),
(3,"前三句写作特点?","名词意象组合,不用动词连接")])),

sh('总结（5min）','p',tip("意象分析三步:找出意象-分析特点-联系情感。枯藤老树昏鸦=凄凉。"),True),

sh('背诵（15min）','r',recite_table(["天净沙秋思全诗背诵","名词意象组合手法","马致远背景常识"]),True)
)

out += day(3,"7月8日","周三","数学+英语+语文","加减法+be动词+天净沙",d3_body,
          "加减法5题计算正确 - am/is/are用法 - 天净沙能默写")

# DAY 4 ── 乘除 + 一般现在时 + 闻王昌龄
d4_body = ''
d4_body += h3('b','\U0001f4d6','数学 - 有理数乘除法（1.5h）')
d4_body += sts(
sh('讲（25min）','b','''<p><b>乘法符号规则</b>：同号得正,异号得负!</p><p>(+3)x(+4)=12 (-3)x(-4)=12 (-3)x(+4)=-12 (+3)x(-4)=-12</p><p><b>多个数相乘</b>：数负号个数。奇数个-结果为负,偶数个-结果为正。</p><p><b>除法</b>：除以一个数等于乘以这个数的倒数。(-8)/4=(-8)x1/4=-2</p>''',True),

sh('A组（10min）','g',qbs([(1,"(-3)x5=?","-15"),(2,"(-4)x(-2)=?","8"),
(3,"(-12)/3=?","-4"),(4,"0x(-5)=?","0"),
(5,"(-1)x(-2)x(-3)=?","-6(三个负号=负)"),
(6,"(-6)/(-2)=?","3(负/负=正)")])),

sh('B组（10min）','o',qbs([(7,"(-2)x3x(-1)x(-4)=?","-24(三个负号=负)"),
(8,"(-20)/(-5)x(-2)=?","4x(-2)=-8")])),

sh('C组（10min）','r',qbs([(9,"【2023泰州】(-2)x(-3)x(-1)=?","-6(三负=负)")])),

sh('总结（5min）','p',tip("乘法符号:奇负偶正!除法=乘倒数。0乘任何数=0,0不能做除数。"),True)
)

d4_body += h3('g','\U0001f527','英语 - 一般现在时(1.5h)')
d4_body += sts(
sh('讲（20min）','g','''<p><b>一般现在时</b>：表示经常发生的动作或事实真理。</p><p>主语是I/You/复数 -> 动词原形: I eat breakfast at 7am. They play football.</p><p>主语是He/She/It -> 动词加s/es: He eats breakfast. She plays tennis.</p><p>动词+s规则:一般加s(likes),s/sh/ch/x+es(teaches),辅音+y变ies(studies)</p>''',True),

sh('练（20min）','o',qbs([(1,"I ___ (get) up at 6am.","get"),
(2,"She ___ (get) up at 6am.","gets"),
(3,"They ___ (play) basketball.","play"),
(4,"He ___ (study) English.","studies"),
(5,"My mother ___ (cook) dinner.","cooks")])),

sh('总结（5min）','p',tip("三单现:he/she/it做主语时动词加s/es。一般现在时表习惯和真理。"),True)
)

d4_body += vocab_block([('eat','吃',''),('drink','喝',''),('play','玩/打',''),('study','学习',''),('cook','做饭','')])

d4_body += h3('r','\U0001f4d6','语文 - 闻王昌龄左迁龙标遥有此寄（1h）')
d4_body += sts(
sh('讲（20min）','r','''<p><b>闻王昌龄左迁龙标遥有此寄</b> - 李白</p><p>杨花落尽子规啼,闻道龙标过五溪。我寄愁心与明月,随君直到夜郎西。</p><p><b>赏析</b>:杨花(飘零)+子规(哀鸣)渲染悲凉气氛。把我对朋友的思念寄托给明月,拟人手法。</p>''',True),

sh('总结（5min）','p',tip("送别诗常见意象:杨花=飘零,子规=哀伤,明月=思念。"),True),

sh('背诵（15min）','r',recite_table(["闻王昌龄全诗背诵","杨花+子规+明月三层意象"]),True)
)

out += day(4,"7月9日","周四","数学+英语+语文","乘除法+一般现在时+闻王昌龄",d4_body,
          "乘法符号判断正确 - 一般现在时+三单 - 闻王昌龄能背")

# DAY 5 ── 乘方 + 词汇积累 + 次北固山下  
d5_body = ''
d5_body += h3('b','\U0001f4d6','数学 - 乘方与科学记数法（1.5h）')
d5_body += sts(
sh('讲（25min）','b','''<p><b>乘方</b>:a的n次方(a^n)=n个a相乘。2^3=2x2x2=8</p><p>注意:(-2)^2=4,但-2^2=-4(括号很重要!)</p><p><b>科学记数法</b>:把一个数写成a x 10^n(1<=|a|<10)。3000000=3x10^6</p>''',True),

sh('A组（10min）','g',qbs([(1,"3^2=?","9"),(2,"(-2)^3=?","-8"),
(3,"2^4=?","16"),(4,"-2^2=?","-4(不是4!)"),
(5,"540000用科学记数法?","5.4x10^5"),
(6,"0.0003用科学记数法?","3x10^-4")])),

sh('B组（10min）','o',qbs([(7,"2^3-(-3)^2=?","8-9=-1"),
(8,"(-1)^101=?","-1(奇数次方=负)")])),

sh('C组（10min）','r',qbs([(9,"【2024泰州】-2^2+(-3)^2=?","-4+9=5")])),

sh('总结（5min）','p',tip("(-a)^n和-(a^n)不同!括号在指数内时负号参与乘方。")+trap("-2^2=-4不是4!指数只对紧邻的数起作用"),True)
)

d5_body += h3('g','\U0001f527','英语 - 词汇积累与短文阅读（1.5h）')
d5_body += sts(
sh('讲（20min）','g','''<p>本周学了5个日常用语+5个be动词结构+5个一般现在时动词。</p><p>词汇是英语的砖瓦!今天学10个高频词,用"看-读-写-造句"四步法记忆。</p>''',True),

sh('练（20min）','o',qbs([(1,"翻译:我每天6点起床。","I get up at 6 every day."),
(2,"is的否定形式?","is not"),
(3,"他们不是学生翻译","They are not students."),
(4,"she的否定形式?","She does not get up..." if False else "she用does not+动词原形")])),

sh('总结（5min）','p',tip("背单词四步法:看读音-读出来-写三遍-造一个句"),True)
)

d5_body += vocab_block([('morning','早上',''),('night','晚上',''),('today','今天',''),('everyday','每天',''),('always','总是','')])

d5_body += h3('r','\U0001f4d6','语文 - 次北固山下（1h）')
d5_body += sts(
sh('讲（20min）','r','''<p><b>次北固山下</b> - 王湾</p><p>客路青山外,行舟绿水前。潮平两岸阔,风正一帆悬。海日生残夜,江春入旧年。乡书何处达?归雁洛阳边。</p><p><b>名句</b>:海日生残夜,江春入旧年。蕴含新旧交替的哲理。</p>''',True),

sh('总结（5min）','p',tip("意境分析:写什么景-抒什么情-含什么理。名句要会赏析!"),True),

sh('背诵（15min）','r',recite_table(["次北固山下全诗背诵","海日生残夜哲理分析","王湾背景"]),True)
)

out += day(5,"7月10日","周五","数学+英语+语文","乘方+词汇+次北固山下",d5_body,
          "乘方计算正确 - 本周英语单词15个 - 次北固山下能默写")

# DAY 6 ── 周复习
d6_body = ''
d6_body += h3('b','\U0001f4d6','数学 - 第一周复习(1.5h)')
d6_body += sts(
sh('讲（20min）','b','''<p><b>本周学的知识点</b>:</p><p>1.正负数:>0是正数,<0是负数,0不是正也不是负</p><p>2.数轴:原点+正方向+单位长度,右边>左边</p><p>3.相反数:符号不同的两个数,和为0</p><p>4.绝对值:到原点的距离,>=0</p><p>5.加减法:同号相加,异号相减;减法变加法</p><p>6.乘除法:同号得正异号得负</p><p>7.乘方:a的n次方=n个a相乘</p>''',True),

sh('综合练（25min）','o',qbs([(1,"|-8|-|3|=?","5"),
(2,"(-2)+(-5)-(-3)=?","-4"),
(3,"(-3)x4/(-2)=?","6"),
(4,"(-1)^10=?","1(偶数次方=正)"),
(5,"(-2)^2-3x(-2)+4=?","4+6+4=14"),
(6,"科学记数法:56000=?","5.6x10^4")])),

sh('易错专练（15min）','r',qbs([(7,"-2^2=?(-2)^2=?","-4和4(两者不同!)"),
(8,"若|x|=3,x=?","x=3或x=-3"),
(9,"-5和-8谁大?","-5更大(绝对值大的负数反而小)")])),

sh('总结（10min）','p',tip("复习比学新知识更重要!:用数轴想大小,用口诀记符号,动手算避免错。"),True)
)

d6_body += h3('g','\U0001f527','英语 - 第一周复习（1.5h）')
d6_body += sts(
sh('讲（20min）','g','''<p><b>本周学过的内容</b>:</p><p>1.26个字母会背诵会默写</p><p>2.5个元音字母:A E I O U</p><p>3.基本问候:Hello/Good morning/Thank you/Sorry</p><p>4.be动词:I am/He is/She is/You are/They are</p><p>5.一般现在时:三单加s/es</p><p>6.本周词汇:15个</p>''',True),

sh('综合练（20min）','o',qbs([(1,"I ___ a student. She ___ a teacher.","am / is"),
(2,"早上好+下午好+晚上好英文","Good morning/afternoon/evening"),
(3,"she get up 改为正确形式","She gets up(加s)"),
(4,"我每天都吃苹果翻译","I eat apples every day."),
(5,"他们不是学生翻译","They are not students.")])),

sh('总结（5min）','p',tip("第一周目标达成!下周开始学动词时态和更多词汇。每天坚持背10分钟单词。"),True)
)

d6_body += h3('r','\U0001f4d6','语文 - 第一周四首古诗复习（1h）')
d6_body += sts(
sh('默写测验（30min）','r','''<p><b>四首古诗默写检测</b></p><p>1.观沧海(曹操)-重点句:日月之行,若出其中</p><p>2.天净沙秋思(马致远)-重点句:枯藤老树昏鸦</p><p>3.闻王昌龄左迁龙标遥有此寄(李白)-重点句:我寄愁心与明月</p><p>4.次北固山下(王湾)-重点句:海日生残夜,江春入旧年</p><p>每首盖住答案默写一遍,错字圈出来重写3遍!</p>''',True),

sh('总结（10min）','p',tip("这4首都是中考必背篇目!要求一字不差地默写出来。"),True),

sh('背诵检查（15min）','r',recite_table(["观沧海默写过关","天净沙秋思默写过关","闻王昌龄默写过关","次北固山下默写过关"]),True)
)

out += day(6,"7月11日","周六","数学+英语+语文","第一周全科复习",d6_body,
          "有理数计算8题全对 - 英语本周内容掌握 - 4首古诗全部能默写")

# Rest Day
out += rest_day("7月12日")

# Write output to a review file
with open('w1-new.html','w',encoding='utf-8') as f:
    # Simple wrapper with minimal CSS
    c = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>新计划 - 第一周预览</title>
<style>
:root{{--blue:#007aff;--red:#ff3b30;--green:#34c759;--orange:#ff9500;--purple:#af52de;--bg:#f5f5f7;--card:#fff;--text:#1d1d1f;--sub:#86868b}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,PingFang SC,Microsoft YaHei,sans-serif;background:var(--bg);color:var(--text);line-height:1.9;font-size:15px;padding:16px}}
.week-marker{{background:linear-gradient(135deg,var(--blue),var(--purple));color:#fff;text-align:center;padding:16px;border-radius:14px;font-size:20px;font-weight:700;margin:32px 0 20px}}
.week-marker .wnote{{font-size:13px;opacity:.85;margin-top:4px}}
.day-page{{border:2px solid #e5e5ea;background:var(--card);border-radius:16px;margin-bottom:20px;overflow:hidden}}
.dtop{{background:linear-gradient(135deg,var(--blue),#5856d6);color:#fff;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}}
.dnum{{font-size:28px;font-weight:800}}
.dbody{{padding:16px}}
.goal{{background:#fffbf0;border:1px solid #ffd54f;border-radius:10px;padding:10px 14px;margin-bottom:12px;font-size:14px}}
.steps{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}}
.step{{background:#f8f8fa;border-radius:12px;padding:12px 14px}}
.step.full{{grid-column:1/-1}}
.step h4{{font-size:14px;margin-bottom:6px;display:flex;align-items:center;gap:6px}}
.dot{{width:8px;height:8px;border-radius:50%;display:inline-block}}
p,li{{font-size:13px;color:#444;margin:4px 0}}
.q-block{{background:#fff;border:1px solid #e5e5ea;border-radius:8px;padding:10px 12px;margin:6px 0}}
.q-num{{font-weight:700;color:var(--blue);margin-right:4px}}
.question{{font-size:13px}}
.ans-btn{{display:inline-block;margin-top:4px;padding:3px 10px;border-radius:12px;border:1px solid var(--blue);color:var(--blue);background:transparent;font-size:11px;cursor:pointer}}
.answer{{display:none;background:#f0f7ff;padding:8px 12px;border-radius:6px;margin-top:6px;font-size:12px;border-left:3px solid var(--blue)}}
.answer.show{{display:block}}
.tip{{background:#f0f7ff;border-left:3px solid var(--blue);padding:8px 12px;margin:6px 0;font-size:12px;border-radius:0 6px 6px 0}}
.err-box{{background:#fff5f5;border-left:3px solid var(--red);padding:8px 12px;margin:6px 0;font-size:12px;border-radius:0 6px 6px 0}}
.check{{background:#e8f5e9;border:1px solid #a5d6a7;border-radius:10px;padding:10px 14px;margin:10px 0;font-size:13px}}
.summ-table{{width:100%;border-collapse:collapse;font-size:12px;margin:6px 0}}
.summ-table th,.summ-table td{{padding:4px 8px;border:1px solid #e5e5ea}}
.summ-table th{{background:#f0e6f6;color:var(--purple)}}
h3{{font-size:16px;display:flex;align-items:center;gap:8px}}
.footer{{text-align:center;color:var(--sub);font-size:12px;padding:20px}}
</style></head><body>
<div style="background:#007aff;color:#fff;padding:12px 16px;border-radius:14px;margin-bottom:16px;text-align:center">
<p style="color:#fff;font-size:18px;font-weight:700">新计划预览 - 第一周（共10周）</p>
<p style="color:rgba(255,255,255,.85);font-size:13px">周一至周六学习,周日休息 | 零基础起点 | 讲解+大量练习+背诵</p>
</div>
'''
    c += out
    c += '''<div class="footer">注:Day3-6内容已简化预览,完整版每科含A组8-10题+B组3-5题+C组2-3题+方法总结+背诵</div>
<script>
function showAns(btn){var a=btn.nextElementSibling;a.classList.toggle("show");btn.textContent=a.classList.contains("show")?"隐藏答案":"点击查看答案";}
</script>
</body></html>'''
    f.write(c)
print(f'Generated w1-new.html ({len(c)} bytes)')
print('Preview at: file:///C:/Users/Tebon/BangMaker/Claw/w1-new.html')
