#!/usr/bin/env python3
"""Generate 54 daily pages from study_library databases.
Each day: Math + English + rotating subject.
All content from enriched knowledge databases with questions+answers."""
import json, os, random, html
from datetime import date, timedelta

LIB = 'C:/Users/Tebon/BangMaker/Claw/study_library'
OUT = f'{LIB}/../days'

# ── Load all databases ──
def load_json(path):
    with open(path,'r',encoding='utf-8') as f:
        return json.load(f)

SVGS = load_json(f'{LIB}/svg/diagrams.json')
VOCAB = load_json(f'{LIB}/english/vocab_complete.json')
PHRASES = load_json(f'{LIB}/english/phrases.json')
POEMS = load_json(f'{LIB}/chinese/poems_61.json')
CHARS = load_json(f'{LIB}/chinese/chars.json')
IDIOMS = load_json(f'{LIB}/chinese/idioms.json')
XINGSHENG = load_json(f'{LIB}/chinese/xingsheng.json')
YICUOXIE = load_json(f'{LIB}/chinese/yicuoxie.json')
SHICI = load_json(f'{LIB}/chinese/shici.json')
XUCI = load_json(f'{LIB}/chinese/xuci.json')

# ── Load wenyanwen database ──
WENYANWEN = load_json(f'{LIB}/chinese/wenyanwen.json') if os.path.exists(f'{LIB}/chinese/wenyanwen.json') else []

KNOWLEDGE = {}
for subj in ['math','chinese','english','physics','chemistry','politics','history']:
    KNOWLEDGE[subj] = load_json(f'{LIB}/{subj}/knowledge.json')

print(f'Loaded: {len(SVGS)} SVGs, {len(VOCAB)} words, {len(PHRASES)} phrases, {len(POEMS)} poems, {len(CHARS)} chars, {len(IDIOMS)} idioms, {len(XINGSHENG)} xingsheng, {len(YICUOXIE)} yicuoxie, {len(XUCI)} xuci')

# ── Shuffle vocab for distribution ──
random.seed(42)
random.shuffle(VOCAB)
WORDS_PER_DAY = len(VOCAB) // 54 + 1  # ~31 words/day, covers all

# ── Shuffle phrases for distribution ──
random.seed(42)
random.shuffle(PHRASES)
random.shuffle(PHRASES)

# ── CSS ──
CSS = '''
:root{--blue:#007aff;--blue-light:#e8f2ff;--blue-015:rgba(0,122,255,0.15);--blue-012:rgba(0,122,255,0.12);--blue-010:rgba(0,122,255,0.10);--blue-008:rgba(0,122,255,0.08);--blue-004:rgba(0,122,255,0.04);--blue-020:rgba(0,122,255,0.20);--green:#34c759;--green-light:#e8f8ed;--green-008:rgba(52,199,89,0.08);--green-004:rgba(52,199,89,0.04);--green-012:rgba(52,199,89,0.12);--orange:#ff9500;--orange-light:#fff3e0;--orange-015:rgba(255,149,0,0.15);--orange-012:rgba(255,149,0,0.12);--red:#ff3b30;--red-light:#ffe8e6;--red-015:rgba(255,59,48,0.15);--red-030:rgba(255,59,48,0.30);--red-020:rgba(255,59,48,0.20);--red-010:rgba(255,59,48,0.10);--red-008:rgba(255,59,48,0.08);--purple:#af52de;--purple-light:#f3e8ff;--purple-012:rgba(175,82,222,0.12);--bg:#f5f5f7;--card:#fff;--text:#1d1d1f;--text2:#636366;--text3:#8e8e93;--sep:#e5e5ea;--shadow:0 1px 3px rgba(0,0,0,0.06);--radius:14px;--radius-sm:10px;--r:0.3s ease;}
[data-theme="dark"]{--bg:#1c1c1e;--card:#2c2c2e;--text:#f5f5f7;--text2:#98989d;--text3:#636366;--sep:#38383a;--blue-light:#1a2744;--green-light:#1a2e20;--orange-light:#2a2410;--red-light:#2e1a18;--purple-light:#221a30;--shadow:0 1px 3px rgba(0,0,0,0.3);}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased;transition:background var(--r),color var(--r);}
.c,.container{max-width:720px;margin:0 auto;padding:0 12px}
.topbar{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.88);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid var(--sep);padding:10px 14px;display:flex;justify-content:space-between;align-items:center;gap:8px;}
[data-theme="dark"] .topbar{background:rgba(28,28,30,0.88);}
.topbar .title{font-size:15px;font-weight:600;white-space:nowrap}
.topbar .quote{font-size:12px;color:var(--text3);flex:1;text-align:center;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding:0 8px}
.topbar a{font-size:12px;color:var(--blue);text-decoration:none;white-space:nowrap;display:flex;align-items:center;gap:4px}
.topbar .right{display:flex;align-items:center;gap:4px}
.topbar .tbtn{display:flex;align-items:center;gap:5px;border:1px solid var(--sep);background:var(--bg);color:var(--text2);cursor:pointer;padding:5px 12px;border-radius:14px;font-size:12px;font-weight:500;transition:all var(--r);white-space:nowrap;}
.topbar .tbtn:hover{background:var(--card);border-color:var(--blue);color:var(--blue);box-shadow:0 1px 4px rgba(0,122,255,0.15)}
.day-card,.dcard{background:var(--card);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);border:1px solid var(--sep);margin-bottom:20px;transition:all var(--r);}
.dhead{background:var(--card);border-bottom:1px solid var(--sep);padding:16px 20px;display:flex;justify-content:space-between;align-items:center;}
.dhead .dnum{font-size:24px;font-weight:700;color:var(--text);letter-spacing:-0.5px}
.dhead .dinfo{text-align:right;font-size:12px;color:var(--text3);line-height:1.5}
.dbody{padding:20px}
.goal{background:var(--orange-light);border:1px solid rgba(255,149,0,0.25);border-radius:var(--radius-sm);padding:14px 18px;margin-bottom:18px;font-size:14px;line-height:1.6;}
.goal b{color:var(--orange)}
.steps{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px}
.step{background:var(--bg);border-radius:var(--radius-sm);padding:14px 16px;transition:all var(--r);border:1px solid transparent;}
.step:hover{border-color:var(--sep)}.step.full{grid-column:1/-1}
.step h4{font-size:13px;font-weight:600;margin-bottom:8px;display:flex;align-items:center;gap:6px}
.dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;display:inline-block}
p,li{font-size:13px;color:var(--text2);margin:4px 0;line-height:1.7}
.q-block{background:var(--card);border:1px solid var(--sep);border-radius:8px;padding:12px 16px;margin:8px 0;transition:all var(--r);}
.q-block:hover{border-color:var(--blue)}.q-num{font-weight:700;color:var(--blue);margin-right:4px;font-size:13px}
.question{font-size:13px;margin:4px 0;line-height:1.6}
.ans-btn{display:inline-block;margin-top:6px;padding:5px 14px;border-radius:14px;border:1.5px solid var(--blue);color:var(--blue);background:transparent;font-size:11px;font-weight:600;cursor:pointer;transition:all var(--r);float:right}
.ans-btn:hover{background:var(--blue);color:#fff;transform:translateY(-1px);box-shadow:0 2px 8px rgba(0,122,255,0.25)}
.answer{display:none;background:var(--blue-light);padding:10px 14px;border-radius:8px;margin-top:8px;font-size:12px;border-left:3px solid var(--blue);line-height:1.7;animation:sd 0.2s ease;clear:both}
.answer.show{display:block}
@keyframes sd{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}
.tip{background:var(--blue-light);border-left:3px solid var(--blue);padding:10px 14px;margin:8px 0;font-size:12px;border-radius:0 8px 8px 0;line-height:1.7;}
.tip b{color:var(--blue)}
.check{background:var(--green-light);border:1px solid rgba(52,199,89,0.25);border-radius:var(--radius-sm);padding:14px 18px;margin:12px 0;font-size:13px;line-height:2.2;}
.check b{color:var(--green)}
.summ-table{width:100%;border-collapse:collapse;font-size:12px;margin:8px 0;}
.summ-table th,.summ-table td{padding:5px 10px;border:1px solid var(--sep);text-align:left}
.summ-table th{background:var(--bg);font-weight:600;color:var(--text2)}
h3{font-size:17px;font-weight:600;display:flex;align-items:center;gap:8px;margin:20px 0 14px;color:var(--text);}
.vocab-box{background:var(--bg);border:1px solid var(--sep);border-radius:var(--radius-sm);padding:14px 16px;margin:10px 0;transition:all var(--r);}
.vocab-box:hover{border-color:var(--text3)}.vocab-box p{margin:0 0 8px 0;font-size:13px;font-weight:600}
.phrases-box{background:var(--purple-light);border:1px solid rgba(175,82,222,0.2);border-radius:var(--radius-sm);padding:14px 16px;margin:10px 0}
.ph-item{padding:5px 0;border-bottom:1px solid rgba(175,82,222,0.15);font-size:12px;line-height:1.6}
.ph-item:last-child{border-bottom:none}
.ph-play{border:none;background:var(--blue);color:#fff;border-radius:50%;width:20px;height:20px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;transition:all 0.2s;vertical-align:middle;margin:0 4px}
.ph-play:hover{background:#005bbf;transform:scale(1.1)}
.ph-ipa{color:var(--text3);font-size:11px;margin-right:4px}
.ph-mean{color:var(--purple);font-size:11px}
.ph-ex{color:var(--text2);font-size:11px}
.complete-bar,.cbar{display:flex;justify-content:center;padding:16px;border-top:1px solid var(--sep);gap:10px}
.complete-btn,.cbtn{padding:12px 36px;border-radius:22px;border:none;font-size:15px;font-weight:600;cursor:pointer;transition:all var(--r);letter-spacing:0.3px;}
.complete-btn.todo,.cbtn.todo{background:var(--blue);color:#fff;box-shadow:0 2px 10px rgba(0,122,255,0.2);}
.complete-btn.todo:hover,.cbtn.todo:hover{background:#005bbf;transform:translateY(-1px);box-shadow:0 4px 14px rgba(0,122,255,0.3);}
.complete-btn.done,.cbtn.done{background:var(--green-light);color:var(--green);border:2px solid var(--green)}
/* Nav — iOS 设置风格 */
.nav-links,.nav{display:flex;justify-content:space-between;align-items:center;padding:16px 0;border-top:1px solid var(--sep)}
.nav-links a,.nav a{text-decoration:none;font-size:13px;font-weight:500;transition:all var(--r);display:flex;align-items:center;gap:4px}
.nav-links .prev,.nav .prv{padding:6px 16px;border-radius:18px;background:var(--blue);color:#fff}
.nav-links .prev:hover,.nav .prv:hover{background:#005bbf}
.nav-links .home,.nav .hm{color:var(--blue);font-weight:500;justify-content:center}
.nav-links .home:hover,.nav .hm:hover{opacity:.7}
.nav-links .next,.nav .nxt{padding:6px 16px;border-radius:18px;background:var(--bg);color:var(--text2);border:1px solid var(--sep)}
.nav-links .next:hover,.nav .nxt:hover{border-color:var(--blue);color:var(--blue)}
.svg-wrap{text-align:center;margin:10px 0;background:var(--bg);border-radius:8px;padding:8px}
.svg-wrap svg{max-width:100%;height:auto}
.watermark{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%) rotate(-25deg);font-size:60px;font-weight:800;color:rgba(0,0,0,0.03);pointer-events:none;z-index:9999;white-space:nowrap;user-select:none;letter-spacing:8px;}
[data-theme="dark"] .watermark{color:rgba(255,255,255,0.03)}
.sdots{display:flex;gap:3px;justify-content:flex-end;margin-top:2px}
.sdots .sd{width:6px;height:6px;border-radius:50%;display:inline-block}
/* 词汇卡片 — 突出单词 + 轻量玻璃 */
.vocab-section{margin:12px 0;padding:12px;border-radius:12px;background:linear-gradient(135deg,#f0f5ff 0%,#f5f0ff 100%);position:relative}
[data-theme="dark"] .vocab-section{background:linear-gradient(135deg,rgba(0,122,255,0.08),rgba(175,82,222,0.06))}
.vocab-title{font-size:14px;font-weight:600;margin-bottom:8px;color:var(--text)}
.v-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.v-card{background:rgba(255,255,255,0.75);border:1px solid rgba(255,255,255,0.6);border-radius:10px;padding:8px 10px;transition:all 0.25s;cursor:pointer;position:relative;overflow:hidden;box-shadow:0 1px 2px rgba(0,0,0,0.03),inset 0 1px 0 rgba(255,255,255,0.9)}
.v-card::before{content:'';position:absolute;inset:0;background:linear-gradient(145deg,rgba(255,255,255,0.5) 0%,rgba(255,255,255,0.08) 40%,transparent 65%);pointer-events:none;border-radius:10px}
.v-card:hover{box-shadow:0 3px 12px rgba(0,0,0,0.05);border-color:rgba(0,122,255,0.2)}
[data-theme="dark"] .v-card{background:rgba(44,44,46,0.55);border-color:rgba(255,255,255,0.08)}
[data-theme="dark"] .v-card::before{background:linear-gradient(145deg,rgba(255,255,255,0.06),transparent)}
[data-theme="dark"] .v-card:hover{border-color:rgba(0,122,255,0.25)}
.v-card.done{background:rgba(52,199,89,0.12);border-color:var(--green)}
[data-theme="dark"] .v-card.done{background:rgba(52,199,89,0.18);border-color:var(--green)}
/* 单词突出 */
.v-top{display:flex;align-items:center;gap:4px;margin-bottom:1px}
.v-word{font-size:17px;font-weight:700;color:var(--text);letter-spacing:-0.2px;line-height:1.3}
.v-play{border:none;background:var(--blue);color:#fff;border-radius:50%;width:20px;height:20px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;transition:all 0.2s;margin-left:auto}
.v-play:hover{background:#005bbf;transform:scale(1.1)}
.v-mid{display:flex;align-items:center;gap:4px;margin-bottom:3px;flex-wrap:wrap}
.v-ipa{font-size:10px;color:var(--text3);font-family:'SF Mono',monospace}
.v-pos{font-size:10px;font-weight:600}
.v-mean{font-size:12px;color:var(--text);font-weight:500}
.v-ex{font-size:10px;color:var(--text2);line-height:1.4}
.v-trans{color:var(--text3);font-size:9px;display:flex;align-items:center;justify-content:space-between;width:100%}
.v-tag{display:inline-block;width:13px;height:13px;border-radius:50%;border:2px solid var(--text3);text-align:center;line-height:13px;font-size:7px;color:transparent;vertical-align:middle;margin-left:2px;transition:all 0.3s;flex-shrink:0}
.v-tag:hover{border-color:var(--blue);transform:scale(1.15)}
.v-card.done .v-tag{border-color:var(--green);background:var(--green);box-shadow:0 0 4px rgba(52,199,89,0.35)}
@media(max-width:500px){.v-grid{grid-template-columns:1fr}}
/* 艾宾浩斯复习 — 两列 */
.review-section{background:var(--purple-light);border:1px solid rgba(175,82,222,0.2);border-radius:var(--radius-sm);padding:14px 16px;margin:14px 0}
.review-title{font-size:14px;font-weight:600;color:var(--purple);margin-bottom:2px}
.review-sub{font-size:11px;color:var(--text3);margin-bottom:8px}
.review-day-label{font-size:11px;font-weight:600;color:var(--text2);margin:8px 0 4px;padding:2px 0 2px 6px;border-left:3px solid var(--purple)}
.rv-grid{display:grid;grid-template-columns:1fr 1fr;gap:4px}
.rv-card{display:flex;align-items:center;gap:4px;padding:4px 8px;background:var(--card);border-radius:6px;border:1px solid var(--sep);font-size:11px;flex-wrap:wrap;min-height:28px}
.rv-word{font-weight:700;color:var(--text)}
.rv-ipa{font-size:9px;color:var(--text3);font-family:'SF Mono',monospace}
.rv-pos{font-size:9px}
.rv-mean{color:var(--text2);font-size:10px}
.rv-play{border:none;background:var(--blue);color:#fff;border-radius:50%;width:18px;height:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all 0.2s;margin-left:auto}
.rv-play:hover{background:#005bbf;transform:scale(1.1)}
@media(max-width:500px){.rv-grid{grid-template-columns:1fr}}
/* Chinese base block */
.vb-chinese{background:var(--orange-light);border:1px solid rgba(255,149,0,0.2);border-radius:var(--radius-sm);padding:14px 16px;margin:10px 0}
.vb-chinese-title{font-weight:700;font-size:14px;color:var(--orange);margin-bottom:6px}
.vb-idioms-title{font-weight:600;font-size:12px;color:var(--orange);margin-top:10px;margin-bottom:4px}
.vb-idiom-item{padding:3px 0;font-size:11px;border-bottom:1px dotted var(--sep)}
/* Dark mode override for inline-hardcoded colors */
[data-theme="dark"] .vocab-box[style*="background:#fef9f0"],
[data-theme="dark"] .vocab-box[style*="background:#f0f4ff"],
[data-theme="dark"] [style*="background:#fffbf0"],
[data-theme="dark"] [style*="background:#fff8f0"],
[data-theme="dark"] [style*="background:#faf0ff"],
[data-theme="dark"] [style*="background:#fef0f7"] {
  background: var(--card) !important;
  border-color: var(--sep) !important;
}
[data-theme="dark"] [style*="color:#4a3728"],
[data-theme="dark"] [style*="color:#795548"],
[data-theme="dark"] [style*="color:#6b4c8a"],
[data-theme="dark"] [style*="color:#6b1e3a"] {
  color: var(--text2) !important;
}
[data-theme="dark"] .summ-table td{color:var(--text2)}
[data-theme="dark"] [style*="color:#b45309"]{color:var(--orange)!important}
[data-theme="dark"] [style*="color:#3b5998"]{color:var(--blue)!important}
@media(max-width:500px){.dbody{padding:14px}.dhead{padding:12px 14px}.steps{grid-template-columns:1fr}.topbar .quote{display:none}.goal{padding:10px 14px}}
/* iPad optimization */
@media(min-width:768px){.c,.container{max-width:800px}.dbody{padding:24px}.dhead{padding:18px 24px}.dhead .dnum{font-size:28px}.step{padding:16px 18px}.q-block{padding:14px 18px}}
@media print{body{font-size:11px;background:#fff}.topbar{position:static;background:#fff}.answer{display:block!important}.ans-btn{display:none}}
'''

# ── Color / Emoji maps ──
CM = {'b':'var(--blue)','o':'var(--orange)','g':'var(--green)','p':'var(--purple)','r':'var(--red)','k':'#795548','e':'#e91e63'}
C  = {'math':'b','english':'g','chinese':'r','physics':'o','chemistry':'p','politics':'e','history':'k'}
EMOJI = {'math':'📖','english':'🔤','chinese':'📖','physics':'⚡','chemistry':'🧪','politics':'🏛️','history':'📜'}
SUBJ_CN = {'math':'数学','english':'英语','chinese':'语文','physics':'物理','chemistry':'化学','politics':'政治','history':'历史'}

# ── 9th grade topics for (初三预习) tag ──
GRADE9_TOPICS = {
    'chemistry': {'物理变化与化学变化', '元素与原子', '化合价与化学式', '质量守恒定律', '化学方程式', '化学反应类型', '根据方程式计算', '空气与氧气', '水', '碳与碳的氧化物', '金属与溶液', '酸碱盐', '科学探究与实验', '化学与生活综合'},
    'physics': {'电学', '磁现象与电磁', '热学', '电磁波与通信'},
    'politics': {'改革开放与法治', '创新驱动与文明建设', '中国担当与梦想'},
    'history': {'古代与中世纪文明', '近代欧洲与世界格局'},
    'math': {'二次函数', '圆', '反比例函数', '统计量与概率'},
    'chinese': {'议论文阅读', '应用文写作'},
}
# 九年级古诗标题（部编版九上/九下）
G9_POEMS = {'行路难（其一）', '酬乐天扬州初逢席上见赠', '水调歌头（明月几时有）', '月夜忆舍弟', '左迁至蓝关示侄孙湘', '咸阳城东楼', '无题', '白雪歌送武判官归京', '过零丁洋', '山坡羊·潼关怀古', '南乡子·登京口北固亭有怀'}
# 九年级文言文标题（部编版九上/九下）
G9_WENYAN = {'岳阳楼记', '醉翁亭记', '出师表', '鱼我所欲也', '送东阳马生序', '曹刿论战', '湖心亭看雪', '邹忌讽齐王纳谏', '唐雎不辱使命'}

# ── Daily encouraging quotes ──
QUOTES = [
    "所有的逆袭，都是有备而来。",
    "今天不走，明天要跑。",
    "乾坤未定，你我皆是黑马。",
    "自律是最高级的自由。",
    "熬过无人问津的日子，才能拥抱诗和远方。",
    "努力是会上瘾的，尤其是在尝到甜头之后。",
    "你有多努力，就有多特殊。",
    "不拼一把，怎么知道自己是人是神？",
    "将来的你，会感谢现在拼命的自己。",
    "每天进步一点点，坚持带来大改变。",
    "世界上最大的谎言就是你不行。",
    "半山腰太挤了，我想去山顶看看。",
    "星光不问赶路人，时光不负有心人。",
    "你的潜力远比你想象的大。",
    "不要假装很努力，因为结果不会陪你演戏。",
    "既然选择了远方，便只顾风雨兼程。",
    "你必须要非常努力，才能看起来毫不费力。",
    "读书是为了遇见更好的自己。",
    "每一个优秀的人，都有一段沉默的时光。",
    "没有什么天生如此，只是我们天天坚持。",
    "奇迹是努力的另一个名字。",
    "今天不吃学习的苦，明天就吃生活的苦。",
    "所有的不甘，都是因为还在心怀梦想。",
    "努力到无能为力，拼搏到感动自己。",
    "你背单词时，阿拉斯加的鳕鱼正跃出水面。",
    "别让未来的你，讨厌现在的自己。",
    "怕什么真理无穷，进一寸有进一寸的欢喜。",
    "想要人前显贵，必先人后受罪。",
    "你只管努力，剩下的交给时间。",
    "最怕你一生碌碌无为，还安慰自己平凡可贵。",
    "只要路是对的，就不怕路远。",
    "坚持是世界上最简单也最困难的事。",
    "不要让你的梦想，只是想想而已。",
    "哪有什么一夜成名，其实都是百炼成钢。",
    "天赋决定起点，努力决定终点。",
    "你流过的每一滴汗，都在浇灌未来的花。",
    "今天少刷一题，明天多流一滴泪。",
    "优秀是一种习惯，放弃是一种习惯。",
    "乾坤未定，你我皆是黑马；乾坤已定，那就扭转乾坤。",
    "没有什么能够阻挡，你对自由的向往。",
    "成功的路上并不拥挤，因为坚持的人不多。",
    "你现在的努力，是为了以后有更多选择的权利。",
    "梦想还是要有的，万一实现了呢？",
    "每一个不曾起舞的日子，都是对生命的辜负。",
    "既然选择了远方，便只顾风雨兼程。",
    "你生而有翼，为何愿一生匍匐前行？",
    "种一棵树最好的时间是十年前，其次是现在。",
    "不要在最该奋斗的年纪选择安逸。",
    "你必须去努力，因为身后空无一人。",
    "努力的意义就是：当好运降临在自己身上时，你会觉得'我配'。",
    "你所浪费的今天，是昨天死去的人奢望的明天。",
    "没有伞的孩子，必须努力奔跑。",
    "所有的光芒，都需要时间才能被看到。",
    "最后一公里最难走，但也是最接近成功的地方。",
]

# ── Helper functions ──
def h3(subj, text):
    c = C.get(subj,'b'); e = EMOJI.get(subj,'')
    return f'<h3 style="color:{CM[c]};border-bottom:2px solid {CM[c]};padding-bottom:6px;margin:16px 0 12px">{e} {text}</h3>'

def sh(title, color, body, full=True):
    return f'<div class="step{" full" if full else ""}"><h4><span class="dot" style="background:{CM[color]}"></span>{title}</h4>{body}</div>'

def sts(*a): return f'<div class="steps">{"".join(a)}</div>'

def qb(n, q, a):
    """Question block: number + question + button + hidden answer."""
    q = html.escape(str(q))
    a = html.escape(str(a))
    return f'<div class="q-block"><span class="q-num">{n}.</span><span class="question">{q}</span><button class="ans-btn" onclick="showAns(this)">展开答案</button><div class="answer">{a}</div></div>'

def qbs(items):
    """items = list of (n, q, a) tuples."""
    return ''.join(qb(n, str(q), str(a)) for n,q,a in items)

def tip(t): return f'<div class="tip"><b>方法</b>：{t}</div>'

def svg_block(name):
    if name in SVGS:
        return f'<div class="svg-wrap">{SVGS[name]["svg"]}</div>'
    return ''

# ── Word-to-emoji visual mnemonic ──
WORD_EMOJI_CACHE = {}
def word_emoji(word, meaning):
    """Return a visual emoji for a word based on its meaning for memory association."""
    if word in WORD_EMOJI_CACHE:
        return WORD_EMOJI_CACHE[word]
    m = meaning.lower()
    # Category-based emoji mapping
    if any(k in m for k in ['吃','喝','食物','水果','蔬菜','餐','饭','菜','食','饮','酒','茶','面包','牛奶','鸡蛋','肉','鱼','米','汤']):
        e = '🍽️'
    elif any(k in m for k in ['动物','狗','猫','鸟','鱼','马','牛','羊','猪','鸡','鸭','熊','虎','狮','象','猴','兔','龙','蛇','鼠']):
        e = '🐾'
    elif any(k in m for k in ['学习','书','读','写','课','学','教','师','生','考','试','文','字','词','句','篇','章']):
        e = '📖'
    elif any(k in m for k in ['爱','喜','欢','乐','快','幸','福','感','情','心','想','念','思']):
        e = '❤️'
    elif any(k in m for k in ['大','小','高','低','长','短','远','近','快','慢','好','坏','美','丑','新','旧']):
        e = '📏'
    elif any(k in m for k in ['工','作','业','职','位','公','司','办','商','务','经济','钱','买','卖','价','值']):
        e = '💼'
    elif any(k in m for k in ['运动','跑','跳','走','游','泳','球','赛','体','健身','锻炼']):
        e = '⚽'
    elif any(k in m for k in ['音','乐','歌','唱','舞','琴','声']):
        e = '🎵'
    elif any(k in m for k in ['颜','色','光','彩','画','图','美','艺']):
        e = '🎨'
    elif any(k in m for k in ['旅行','旅','游','行','走','去','来','到','达','离','开']):
        e = '✈️'
    elif any(k in m for k in ['医','药','病','痛','健','康','身','体']):
        e = '🏥'
    elif any(k in m for k in ['科','学','技','术','数','理','化','实','验','发','现']):
        e = '🔬'
    elif any(k in m for k in ['时','间','日','月','年','星','期','钟','点','分','秒']):
        e = '⏰'
    elif any(k in m for k in ['天','气','风','云','雨','雪','雷','电','晴','阴','温']):
        e = '🌤️'
    elif any(k in m for k in ['家','庭','父','母','子','女','兄','弟','姐','妹','亲']):
        e = '👨‍👩‍👧‍👦'
    elif any(k in m for k in ['国','家','城','市','地','方','区','域','世','界']):
        e = '🌍'
    elif any(k in m for k in ['电','脑','网','信','机','器','智','能','数字']):
        e = '💻'
    else:
        # Fallback: pick a random emoji based on word hash (consistent per word)
        h = sum(ord(c) for c in word) % 20
        fallbacks = ['📚','🎯','💡','⭐','🔥','💪','🏆','🚀','💎','🌈','🍀','🎪','🌺','🎭','🎨','🎵','⚡','🌟','💫','🎈']
        e = fallbacks[h]
    WORD_EMOJI_CACHE[word] = e
    return e

# ── Ebbinghaus review system ──
EBBINGHAUS_INTERVALS = [1]  # 间隔1天复习
def get_review_words(day_num):
    """Return words from previous days that need review today per Ebbinghaus curve."""
    review_items = []  # list of (source_day, word_tuple)
    for interval in EBBINGHAUS_INTERVALS:
        src_day = day_num - interval
        if 1 <= src_day <= 54:
            vi = (src_day - 1) * WORDS_PER_DAY
            words = VOCAB[vi : vi + WORDS_PER_DAY]
            for w in words:
                review_items.append((src_day, w))
    return review_items

def review_block(day_num):
    """Generate Ebbinghaus review section HTML."""
    items = get_review_words(day_num)
    if not items:
        return ''
    from collections import OrderedDict
    by_day = OrderedDict()
    for src_day, w in items:
        if src_day not in by_day:
            by_day[src_day] = []
        by_day[src_day].append(w)
    
    h = '<div class="review-section"><p class="review-title">🧠 艾宾浩斯复习 · 今日需复习</p>'
    h += '<p class="review-sub">根据遗忘曲线，以下单词需要今日复习巩固</p>'
    
    for src_day, words in by_day.items():
        h += f'<div class="review-day-label">📅 Day {src_day}</div><div class="rv-grid">'
        for w in words:
            wi, ipa, pos, meaning, ex, trans = w if len(w) >= 6 else (w[0],'','','','','')
            safe_wi = wi.replace("'", "\\'")
            svg_play = '<svg width="9" height="9"><use href="#i-play"/></svg>'
            btn = f'<button onclick="speak(\'{safe_wi}\',this)" class="rv-play" title="点击发音">{svg_play}</button>'
            h += f'<div class="rv-card"><b class="rv-word">{wi}</b><span class="rv-ipa">/ {ipa} /</span><span class="rv-pos" style="color:var(--purple)">{pos}</span><span class="rv-mean">{meaning}</span>{btn}</div>'
        h += '</div>'
    h += '</div>'
    return h

def vocab_block(words, day_num=1):
    """词汇卡片：单词突出 + 音标+释义 + 标记已记住"""
    h = '<div class="vocab-section"><p class="vocab-title">📖 今日新词</p><div class="v-grid">'
    for i, w in enumerate(words):
        wi, ipa, pos, meaning, ex, trans = w if len(w) >= 6 else (w[0],'','','','','')
        safe_wi = wi.replace("'", "\\'")
        wk = f'wd_{day_num}_{i}'
        svg_play = '<svg width="11" height="11"><use href="#i-play"/></svg>'
        btn = f'<button onclick="speak(\'{safe_wi}\',this)" class="v-play" title="点击发音">{svg_play}</button>'
        pos_color = {'n.':'var(--blue)','v.':'var(--green)','adj.':'var(--orange)','adv.':'var(--purple)','prep.':'var(--red)','conj.':'#e91e63','pron.':'#795548'}
        pc = pos_color.get(pos, 'var(--purple)')
        h += f'''<div class="v-card" id="{wk}" onclick="tR(\'{wk}\')">
  <div class="v-top"><span class="v-word">{wi}</span>{btn}</div>
  <div class="v-mid"><span class="v-ipa">/ {ipa} /</span><span class="v-pos" style="color:{pc}">{pos}</span><span class="v-mean">{meaning}</span></div>
  <div class="v-ex">{ex}<br><span class="v-trans">({trans}) <span class="v-tag" id="{wk}_tag">○</span></span></div>
</div>'''
    return h + '</div></div>'

def phrases_block(phrases):
    if not phrases:
        return ''
    h = '<div class="phrases-box"><p style="font-weight:600;margin-bottom:6px">🔗 今日短语搭配（' + str(len(phrases)) + '条）</p>'
    for i, p in enumerate(phrases):
        safe_p = p[0].replace("'", "\\'")
        svg_play = '<svg width="9" height="9"><use href="#i-play"/></svg>'
        btn = f'<button onclick="speak(\'{safe_p}\',this)" class="ph-play" title="点击发音">{svg_play}</button>'
        h += f'<div class="ph-item"><b>{p[0]}</b>{btn}<span class="ph-ipa">/ {p[1]} /</span><span class="ph-mean">{p[3]}</span><br><span class="ph-ex">{p[4]}（{p[5]}）</span></div>'
    return h + '</div>'

def chinese_base_block(chars_list, idioms_list, xingsheng_item, yicuoxie_item, shici_item, xuci_item):
    """Daily Chinese fundamental block: 5 词语 + 5 成语"""
    # Extract SHICI data based on type rotation
    shici_type = shici_item['type']  # 通假字/古今异义/一词多义/词类活用
    shici_entries = shici_item['entries']  # list of entries
    
    h = '<div class="vb-chinese">'
    h += '<p class="vb-chinese-title">📝 今日语文基础积累（7词语 + 5成语）</p>'
    
    # ── 5 词语 ──
    h += '<table class="summ-table" style="margin-top:6px"><tr><th style="width:12%">类型</th><th style="width:18%">内容</th><th style="width:70%">详解</th></tr>'
    
    # 1. 多音字 (3个，全量覆盖)
    if chars_list:
        for ch in chars_list[:3]:
            h += f'<tr><td style="font-size:11px;color:var(--orange)">多音字</td><td style="font-weight:700;font-size:13px;color:var(--text)">{ch[0]}</td>'
            h += f'<td style="font-size:11px;color:var(--text2)">音: <span style="color:var(--red)">{ch[1]}</span> · 义: {ch[3]} · 例: {ch[4]}</td></tr>'
    
    # 2. 形声字 (1个)
    if xingsheng_item:
        xs = xingsheng_item
        h += f'<tr><td style="font-size:11px;color:var(--orange)">形声字</td><td style="font-weight:700;font-size:13px;color:var(--text)">{xs[0]}</td>'
        h += f'<td style="font-size:11px;color:var(--text2)">音: {xs[1]} · 形旁(义): {xs[2]} · 声旁(音): {xs[3]} · {xs[4]}</td></tr>'
    
    # 3. 易错字 (1个)
    if yicuoxie_item:
        yc = yicuoxie_item
        h += f'<tr><td style="font-size:11px;color:var(--orange)">易错字</td><td style="font-weight:700;font-size:13px;color:var(--text)">{yc[0]}</td>'
        h += f'<td style="font-size:11px;color:var(--text2)">音: {yc[1]} · 义: {yc[2]} · <span style="color:var(--red)">区别: {yc[3]}</span></td></tr>'
    
    # 4. 实词 (1个, 轮转类型)
    for se in shici_entries:
        h += f'<tr><td style="font-size:11px;color:var(--orange)">{shici_type}</td><td style="font-weight:700;font-size:13px;color:var(--text)">{se[0]}</td>'
        h += f'<td style="font-size:11px;color:var(--text2)">{"音: "+se[1]+" · " if len(se)>1 and se[1] else ""}{se[2]} · 例: {se[3] if len(se)>3 else ""}</td></tr>'
    
    # 5. 虚词 (1个)
    if xuci_item:
        xu = xuci_item
        h += f'<tr><td style="font-size:11px;color:var(--orange)">虚词</td><td style="font-weight:700;font-size:13px;color:var(--text)">{xu[0]}</td>'
        h += f'<td style="font-size:11px;color:var(--text2)">{xu[1]} — {xu[2]} · 例: {xu[3]} · <span style="color:var(--blue)">{xu[4]}</span></td></tr>'
    
    h += '</table>'
    
    # ── 5 成语 ──
    h += '<div class="vb-idioms-title">📖 成语（5个）</div>'
    for i, idm in enumerate(idioms_list):
        if len(idm) >= 5:
            h += f'<div class="vb-idiom-item">'
            h += f'<b style="color:var(--text);font-size:12px">{i+1}.{idm[0]}</b> '
            h += f'<span style="color:var(--text3)">{idm[1]}</span> — {idm[2]}'
            if idm[4]:
                h += f' · <span style="color:var(--red);font-size:10px">⚠{idm[4]}</span>'
            h += '</div>'
    
    return h + '</div>'

def recite_block(items):
    rows = ''.join(f'<tr><td style="font-size:12px">{r}</td><td>□ □</td></tr>' for r in items)
    return f'<table class="summ-table"><tr><th>背诵内容</th><th>已背/已默</th></tr>{rows}</table>'

def recitation_block(title, author, full_text='', keywords='', author_bg='', famous_lines=''):
    """Enhanced poem recitation: full text + key words + author background + famous lines."""
    h = f'<div class="vocab-box" style="background:#fef9f0;border-color:#e8d5b7">'
    h += f'<p style="font-weight:700;color:#b45309;font-size:14px">📜 今日古诗背诵：{title} — {author}</p>'
    
    # Full poem text (collapsible)
    if full_text:
        safe_text = full_text.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_text\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开全文 ▶\':\'收起全文 ▲\';" class="coll-btn" style="background:var(--blue)">展开全文 ▶</button>'
        h += f'<div id="poem_text" style="display:none;padding:10px 14px;border-radius:8px;margin:8px 0;border:1px dashed var(--sep);font-size:14px;line-height:2;color:var(--text2);background:var(--card);white-space:pre-line">>{full_text}</div>'
    
    # Key word explanations (collapsible)
    if keywords:
        safe_kw = keywords.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_words\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开字词释义 📖\':\'收起字词释义 ▲\';" class="coll-btn" style="background:var(--orange)">展开字词释义 📖</button>'
        h += f'<div id="poem_words" style="display:none;padding:10px 14px;border-radius:8px;margin:8px 0;border:1px dashed var(--sep);font-size:12px;line-height:1.8;color:var(--text2);background:var(--card)">{keywords}</div>'
    
    # Author background (collapsible)
    if author_bg:
        safe_bg = author_bg.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_author\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开作者背景 📝\':\'收起作者背景 ▲\';" class="coll-btn" style="background:var(--purple)">展开作者背景 📝</button>'
        h += f'<div id="poem_author" style="display:none;padding:10px 14px;border-radius:8px;margin:8px 0;border:1px dashed var(--sep);font-size:12px;line-height:1.8;color:var(--text2);background:var(--card)">{author_bg}</div>'
    
    # Famous lines (collapsible)
    if famous_lines:
        safe_fl = famous_lines.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_famous\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开千古名句 🌟\':\'收起名句 ▲\';" style="background:#e91e63;color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px">展开千古名句 🌟</button>'
        h += f'<div id="poem_famous" style="display:none;background:#fef0f7;padding:8px 12px;border-radius:8px;margin:6px 0;border:1px dashed #e8b7c8;font-size:12px;line-height:1.8;color:#6b1e3a">{famous_lines}</div>'
    
    # Checkbox table
    items = [f'{author}: 《{title}》全诗背诵','重点字词释义掌握','作者背景常识了解','千古名句解析']
    rows = ''.join(f'<tr><td style="font-size:12px">{r}</td><td>□ □</td></tr>' for r in items)
    h += f'<table class="summ-table" style="margin-top:8px"><tr><th>背诵内容</th><th>已背/已默</th></tr>{rows}</table>'
    
    return h + '</div>'
    """Enhanced poem recitation: full text + key words + author background."""
    h = f'<div class="vocab-box" style="background:#fef9f0;border-color:#e8d5b7">'
    h += f'<p style="font-weight:700;color:#b45309;font-size:14px">📜 每日古诗背诵：{title} — {author}</p>'
    
    # Full poem text (collapsible)
    if full_text:
        safe_text = full_text.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_text\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开全文 ▶\':\'收起全文 ▲\';" style="background:var(--blue);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px 0">展开全文 ▶</button>'
        h += f'<div id="poem_text" style="display:none;padding:10px 14px;border-radius:8px;margin:8px 0;border:1px dashed var(--sep);font-size:14px;line-height:2;color:var(--text2);background:var(--card);white-space:pre-line">>{full_text}</div>'
    
    # Key word explanations (collapsible)
    if keywords:
        safe_kw = keywords.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_words\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开字词释义 📖\':\'收起字词释义 ▲\';" style="background:var(--orange);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px 4px">展开字词释义 📖</button>'
        h += f'<div id="poem_words" style="display:none;padding:10px 14px;border-radius:8px;margin:8px 0;border:1px dashed var(--sep);font-size:12px;line-height:1.8;color:var(--text2);background:var(--card)">{keywords}</div>'
    
    # Author background (collapsible)
    if author_bg:
        safe_bg = author_bg.replace("'", "\\'").replace('"', '&quot;')
        h += f'<button onclick="var t=document.getElementById(\'poem_author\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'展开作者背景 📝\':\'收起作者背景 ▲\';" style="background:var(--purple);color:#fff;border:none;padding:4px 12px;border-radius:12px;cursor:pointer;font-size:12px;margin:4px 4px">展开作者背景 📝</button>'
        h += f'<div id="poem_author" style="display:none;padding:10px 14px;border-radius:8px;margin:8px 0;border:1px dashed var(--sep);font-size:12px;line-height:1.8;color:var(--text2);background:var(--card)">{author_bg}</div>'
    
    # Checkbox table
    items = [f'{author}: 《{title}》全诗背诵','重点字词释义掌握','作者背景常识了解']
    rows = ''.join(f'<tr><td style="font-size:12px">{r}</td><td>□ □</td></tr>' for r in items)
    h += f'<table class="summ-table" style="margin-top:8px"><tr><th>背诵内容</th><th>已背/已默</th></tr>{rows}</table>'
    
    return h + '</div>'

# ── Extract question text from mixed formats ──
def get_q(item):
    """item is either dict {q:..., a:...} or plain string."""
    if isinstance(item, dict):
        return item.get('q', str(item))
    return str(item)

def get_a(item):
    if isinstance(item, dict):
        return item.get('a', '')
    return ''

# ── Find topic by name ──
def find_topic(subj, topic_name):
    k = KNOWLEDGE.get(subj, {})
    sections = k.get('sections', k.get('chapters', []))
    for s in sections:
        for t in s.get('topics', []):
            if topic_name in t['name']:
                return t
    return None

# ── Build subject section from database ──
def build_subject_section(subj, topic_name, extra_lecture='', extra_practice=None, svg_names=None):
    topic = find_topic(subj, topic_name)
    if not topic:
        return ''
    steps_list = []
    
        # Lecture
    lecture = topic.get('lecture', '')
    if lecture:
        body = f'<div class="lecture-expanded">{lecture}</div>'
        if extra_lecture:
            body += f'<p>{extra_lecture}</p>'
        if svg_names:
            for sn in svg_names:
                body += svg_block(sn)
        steps_list.append(sh('讲（20min）', C.get(subj,'b'), body, True))
    
    # Practice (handle both dict and string formats)
    practice = topic.get('practice', [])
    if practice:
        all_p = list(practice)
        if extra_practice:
            all_p.extend(extra_practice)
        
        # Group A (first 5)
        items_a = [(i+1, get_q(p), get_a(p)) for i,p in enumerate(all_p[:5])]
        steps_list.append(sh('A组·基础练', 'g', qbs(items_a), True))
        
        # Group B (next 5)
        if len(all_p) > 5:
            items_b = [(i+1, get_q(p), get_a(p)) for i,p in enumerate(all_p[5:10])]
            steps_list.append(sh('B组·进阶练', 'o', qbs(items_b), True))
    
    # Exam practice
    exam = topic.get('exam_practice', [])
    if exam:
        items_e = [(i+1, get_q(e), get_a(e)) for i,e in enumerate(exam[:3])]
        steps_list.append(sh('C组·中考真题', 'r', qbs(items_e), True))
    
    # Method
    method = topic.get('method', '')
    if method:
        steps_list.append(sh('方法总结', 'p', tip(method), True))
    
    return sts(*steps_list)

# ── SVG names per subject topic ──
SVG_MAP = {
    'math': {
        '有理数与实数': ['math_number_line'],
        '整式与因式分解': [],
        '分式与二次根式': [],
        '一元一次方程与方程组': ['math_quadratic_formula'],
        '不等式（组）': [],
        '一次函数': ['math_functions'],
        '二次函数': ['math_parabola'],
        '反比例函数': [],
        '三角形（全等+相似+勾股）': ['math_triangle','math_pythagorean'],
        '四边形': [],
        '圆': ['math_circle'],
        '统计量与概率': ['math_coordinate'],
    },
    'physics': {
        '磁现象与磁场': ['physics_magnet'],
        '电生磁（电磁铁）': ['physics_magnet'],
        '热机与效率': ['physics_engine'],
        '内能与热量': ['physics_engine'],
        '压强': ['physics_pressure_float'],
        '浮力': ['physics_pressure_float'],
        '光的反射定律': ['physics_reflection'],
        '凸透镜成像规律': ['physics_lens'],
        '受力分析': ['physics_forces'],
        '电路基础': ['physics_circuit'],
        '简单机械': ['physics_lever'],
    },
    'chemistry': {
        '金属': ['chem_metal_order'],
        '酸碱盐': ['chem_ph_scale'],
        '燃烧与灭火': ['chem_fire_triangle'],
        '空气与氧气': ['chem_fire_triangle'],
        '物理变化与化学变化': ['chem_molecule'],
        '元素与原子': ['chem_atom'],
        '溶液': ['chem_ph_scale'],
    },
    'history': {
        '列强侵略与民族危机': ['history_timeline'],
        '新民主主义革命': ['history_timeline'],
        '近代化的探索': ['history_timeline'],
        '世界史': ['history_world_timeline'],
    },
}

# ── Schedule (block-based: 2 consecutive days per topic) ──
# 语数英每天必有，每个知识点集中攻克2天，理化政史循环穿插
DAILY = ['math','english','chinese']
ROTATING = ['physics','chemistry','politics','history']

def get_topic(subj, day_num, block_size=2):
    """Block-based topic distribution: each topic gets `block_size` consecutive days.
    For rotating subjects, uses occurrence count (rounds) so no topic is skipped."""
    k = KNOWLEDGE.get(subj, {})
    sections = k.get('sections', k.get('chapters', []))
    all_topics = []
    for sec in sections:
        for t in sec.get('topics', []):
            all_topics.append(t['name'])
    if not all_topics:
        return ''
    
    if subj in DAILY:
        # DAILY subjects: every block counts contiguously
        block_idx = ((day_num - 1) // block_size) % len(all_topics)
    else:
        # ROTATING subjects: only count the rounds (each subject appears once per len(ROTATING) blocks)
        # occurrence = which complete round of rotating subjects we've done
        # E.g. physics appears on block 0,4,8,... → occurrence = block//4
        occurrence = ((day_num - 1) // block_size) // len(ROTATING)
        block_idx = occurrence % len(all_topics)
    
    return all_topics[block_idx]

def get_poems(day_num, count=2):
    """Return `count` poems for a given day (ensures 100% coverage)."""
    if not POEMS:
        return []
    result = []
    for i in range(count):
        idx = ((day_num - 1) * 2 + i) % len(POEMS)
        p = POEMS[idx]
        if len(p) >= 2:
            result.append({
                'title': p[0] if len(p)>0 else '',
                'author': p[1] if len(p)>1 else '',
                'full_text': p[4] if len(p)>4 else '',
                'keywords': p[5] if len(p)>5 else '',
                'author_bg': p[6] if len(p)>6 else '',
                'famous_lines': p[7] if len(p)>7 else '',
            })
    return result

# ── Day template ──
def day_template(num, month, day, wd, subjects, goal, body, check, prev, next_):
    prev_h = f'<a href="day{prev:03d}.html" class="prv">← Day {prev}</a>' if prev else '<span></span>'
    next_h = f'<a href="day{next_:03d}.html" class="nxt">Day {next_} →</a>' if next_ else '<span></span>'
    qi = QUOTES[(num-1) % len(QUOTES)]
    js = f'''<script>
var sp='<svg style="display:none"><defs><svg id="i-play" viewBox="0 0 24 24"><polygon points="5,3 19,12 5,21" fill="currentColor"/></svg><svg id="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg id="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></defs></svg>';
document.body.insertAdjacentHTML("afterbegin",sp);
function speak(t,btn){{try{{if(!window.speechSynthesis){{alert("当前浏览器不支持语音播放");return;}}window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(t);u.lang="en-US";u.rate=0.8;u.onstart=function(){{if(btn){{btn.style.background="#34c759";btn.style.transform="scale(1.15)";}}}};u.onend=function(){{if(btn){{btn.style.background="var(--blue)";btn.style.transform="scale(1)";}}}};window.speechSynthesis.speak(u);}}catch(e){{alert("播放失败:"+e.message);}}}}
function showAns(b){{var a=b.nextElementSibling;a.classList.toggle("show");b.textContent=a.classList.contains("show")?"隐藏答案":"展开答案";}}
function toggleComplete(dn){{var btn=document.getElementById("cbtn");if(btn.classList.contains("todo")){{localStorage.setItem("day_"+dn+"_done","true");btn.className="cbtn done";btn.textContent="已完成 ✓";}}else{{localStorage.setItem("day_"+dn+"_done","false");btn.className="cbtn todo";btn.textContent="标记完成";}}}}
function tR(k){{var c=document.getElementById(k);var t=document.getElementById(k+"_tag");if(c.classList.contains("done")){{c.classList.remove("done");t.textContent="○";localStorage.setItem(k,"0");}}else{{c.classList.add("done");t.textContent="●";localStorage.setItem(k,"1");}}}}
function tTheme(){{var h=document.documentElement;var b=document.querySelector(".tbtn");if(h.getAttribute("data-theme")=="dark"){{h.setAttribute("data-theme","light");b.innerHTML='<svg width="14" height="14"><use href="#i-moon"/></svg><span>深色</span>';localStorage.setItem("theme","light");}}else{{h.setAttribute("data-theme","dark");b.innerHTML='<svg width="14" height="14"><use href="#i-sun"/></svg><span>亮色</span>';localStorage.setItem("theme","dark");}}}}
window.onload=function(){{if(localStorage.getItem("day_{num}_done")==="true"){{var btn=document.getElementById("cbtn");btn.className="cbtn done";btn.textContent="已完成 ✓";}}if(localStorage.getItem("theme")==="dark") tTheme();for(var i=0;i<60;i++){{var k="wd_{num}_"+i;if(localStorage.getItem(k)==="1"){{var c=document.getElementById(k);if(c){{c.classList.add("done");var t=document.getElementById(k+"_tag");if(t)t.textContent="●";}}}}}}}};
</script>'''
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>暑假逆袭 · Day {num}</title><style>{CSS}</style></head><body>
<div class="watermark">顾辰泰 加油</div>
<div class="topbar"><span class="title">Day {num} · {month}/{day}</span><span class="quote">{qi}</span><div class="right"><button class="tbtn" onclick="tTheme()"><svg width="14" height="14"><use href="#i-moon"/></svg><span>深色</span></button><a href="../index.html">📋 目录</a></div></div>
<div class="c">
<div class="dcard"><div class="dhead"><div class="dnum">Day {num}</div><div class="dinfo"><div>{month}月{day}日 {wd}</div><div>{subjects}</div></div></div>
<div class="dbody"><div class="goal"><b>今日目标</b>：{goal}</div>{body}<div class="check"><b>今日达标检查</b>：<br>{check}</div></div>
<div class="cbar"><button id="cbtn" class="cbtn todo" onclick="toggleComplete({num})">标记完成</button></div>
<div class="nav">{prev_h}<a href="../index.html" class="hm">📋 目录</a>{next_h}</div></div></div>{js}</body></html>'''

# ── Generate all 54 days ──
def generate_all():
    start_date = date(2026, 6, 29)
    WD_CN = ['周一','周二','周三','周四','周五','周六']
    os.makedirs(OUT, exist_ok=True)
    
    for day_num in range(1, 55):
        w = (day_num - 1) // 6      # week index 0-8
        d = (day_num - 1) % 6       # day in week 0-5
        dt = start_date + timedelta(weeks=w, days=d)
        month_num, day_num_dt, wd = dt.month, dt.day, WD_CN[d]
        prev_d = day_num - 1 if day_num > 1 else None
        next_d = day_num + 1 if day_num < 54 else None
        
        # Get topics for today (block-based: 2 days per topic)
        math_topic = get_topic('math', day_num)
        eng_topic  = get_topic('english', day_num)
        chi_topic  = get_topic('chinese', day_num)
        rot_subj   = ROTATING[(day_num - 1) % len(ROTATING)]  # rotate every day among 4 subjects
        rot_topic  = get_topic(rot_subj, day_num, block_size=1)
        
        # Get vocabulary for today
        vi = (day_num - 1) * WORDS_PER_DAY
        todays_vocab = VOCAB[vi : vi + WORDS_PER_DAY]
        
        # Get phrases: 4 per day for full coverage (213/54 ≈ 4)
        phrases_per_day = 4
        pi_start = (day_num - 1) * phrases_per_day % len(PHRASES)
        todays_phrase = [PHRASES[(pi_start + i) % len(PHRASES)] for i in range(phrases_per_day)] if PHRASES else []
        
        # Build subject sections
        body_parts = []
        check_items = []
        
        # 1. Math section
        svg_list = SVG_MAP.get('math', {}).get(math_topic, [])
        g9_mtag = '<span style="color:#e91e63;font-size:11px;font-weight:600">（初三预习）</span>' if math_topic in GRADE9_TOPICS.get('math', set()) else ''
        body_parts.append(h3('math', f'数学 · {math_topic} {g9_mtag}'))
        body_parts.append(build_subject_section('math', math_topic, svg_names=svg_list))
        check_items.append(f'{math_topic}理解 □')
        check_items.append(f'数学练习完成 □')
        
        # 2. English section
        body_parts.append(h3('english', f'英语 · {eng_topic}'))
        body_parts.append(build_subject_section('english', eng_topic))
        check_items.append(f'{eng_topic}练习 □')
        
        # Vocabulary block (EVERY day)
        body_parts.append(vocab_block(todays_vocab, day_num))
        check_items.append(f'今日词汇({len(todays_vocab)}词)背完 □')
        
        # Ebbinghaus review section (words from previous days due for review)
        review_html = review_block(day_num)
        if review_html:
            body_parts.append(review_html)
            check_items.append(f'艾宾浩斯复习完成 □')
        
        # Phrases block (spread across days)
        body_parts.append(phrases_block(todays_phrase))
        
        # 3. Chinese section (EVERY day)
        body_parts.append(h3('chinese', f'语文 · {chi_topic}'))
        body_parts.append(build_subject_section('chinese', chi_topic))
        check_items.append(f'{chi_topic}理解 □')
        
        # 4. Poem + Wenyanwen recitation
        poems_today = get_poems(day_num, 2)
        for pi, poem in enumerate(poems_today):
            title = poem['title']; author = poem['author']
            full_text = poem['full_text']; keywords = poem['keywords']
            author_bg = poem['author_bg']; famous_lines = poem['famous_lines']
            pid = f'poem_text_{day_num}_{pi}'
            g9_tag_p = '<span style="color:var(--red);font-size:10px;font-weight:600">（初三预习）</span>' if title in G9_POEMS else ''
            h = f'<div class="vocab-box" style="background:var(--orange-light);border-color:rgba(255,149,0,0.2)">'
            h += f'<p style="font-weight:700;color:var(--orange);font-size:14px;margin-bottom:6px">📜 古诗{pi+1}：{title} — {author} {g9_tag_p}</p>'
            if full_text:
                h += f'<button onclick="var t=document.getElementById(\'{pid}\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'▶ 展开原文\':\'▼ 收起原文\';" style="background:var(--blue);color:#fff;border:none;padding:2px 10px;border-radius:10px;cursor:pointer;font-size:11px;margin:4px 0">▶ 展开原文</button>'
                h += f'<div id="{pid}" style="display:none;padding:6px 0;font-size:14px;line-height:2;color:var(--text2);white-space:pre-line">{full_text}</div>'
            if keywords:
                h += f'<div style="padding:2px 0;font-size:12px;color:var(--text3);line-height:1.8"><b>📖 字词</b>：{keywords}</div>'
            if author_bg:
                h += f'<div style="padding:2px 0;font-size:12px;color:var(--text3);line-height:1.8"><b>📝 作者</b>：{author_bg}</div>'
            if famous_lines:
                h += f'<div style="padding:2px 0;font-size:12px;color:var(--red);line-height:1.8"><b>🌟 名句</b>：{famous_lines}</div>'
            h += '</div>'
            body_parts.append(h)
            check_items.append(f'《{title}》背诵 □')
        
        # Wenyanwen (full text hidden, words+author shown)
        if WENYANWEN:
            ww_idx = (day_num - 1) % len(WENYANWEN)
            ww = WENYANWEN[ww_idx]
            ww_title = ww[0] if len(ww)>0 else ''
            ww_author = f'{ww[1]} ({ww[2]})' if len(ww)>2 else ''
            ww_text = ww[3] if len(ww)>3 else ''
            ww_words = ww[4] if len(ww)>4 else ''
            ww_bg = ww[5] if len(ww)>5 else ''
            wid = f'ww_text_{day_num}'
            g9_tag_w = '<span style="color:var(--red);font-size:10px;font-weight:600">（初三预习）</span>' if ww_title in G9_WENYAN else ''
            body_parts.append(f'<div class="vocab-box" style="background:var(--blue-light);border-color:rgba(0,122,255,0.2)">'
                f'<p style="font-weight:700;color:var(--blue);font-size:14px;margin-bottom:6px">📜 今日文言文背诵：{ww_title} — {ww_author} {g9_tag_w}</p>'
                f'<button onclick="var t=document.getElementById(\'{wid}\');t.style.display=t.style.display==\'none\'?\'block\':\'none\';this.textContent=t.style.display==\'none\'?\'▶ 展开原文\':\'▼ 收起原文\';" style="background:var(--blue);color:#fff;border:none;padding:2px 10px;border-radius:10px;cursor:pointer;font-size:11px;margin:4px 0">▶ 展开原文</button>'
                f'<div id="{wid}" style="display:none;padding:6px 0;font-size:14px;line-height:2;color:var(--text2);white-space:pre-line">{ww_text}</div>'
                f'<div style="padding:2px 0;font-size:12px;color:var(--text3);line-height:1.8"><b>📖 字词</b>：{ww_words}</div>'
                f'<div style="padding:2px 0;font-size:12px;color:var(--text3);line-height:1.8"><b>📝 作者</b>：{ww_bg}</div></div>')
            check_items.append(f'《{ww_title}》文言背诵 □')
        
        # Chinese words accumulation (EVERY day: 5 词语 + 5 成语)
        ci = (day_num - 1) * 3 % len(CHARS)  # 3 chars per day to cover all 136
        ii = (day_num - 1) * 5 % len(IDIOMS)
        xi = (day_num - 1) % len(XINGSHENG)
        yi = (day_num - 1) * 2 % len(YICUOXIE)  # step 2 for better coverage
        
        # SHICI: rotate through 通假字/古今异义/一词多义/词类活用
        shici_types = list(SHICI.keys())
        si_type = shici_types[(day_num - 1) % len(shici_types)]
        si_list = SHICI[si_type]
        si_idx = (day_num - 1) * 2 % len(si_list)  # step 2 to cover more entries
        
        # XUCI: rotate through 虚词 keys (之/而/以/于/其/为/乃/则/焉/乎)
        xuci_keys = list(XUCI.keys())
        xu_key = xuci_keys[(day_num - 1) % len(xuci_keys)]
        xu_list = XUCI[xu_key]
        xu_idx = (day_num - 1) % len(xu_list)
        
        # Build items for today
        todays_chars = [CHARS[(ci + j) % len(CHARS)] for j in range(3)] if CHARS else []  # 3 chars/day for full coverage
        todays_xingsheng = XINGSHENG[xi] if XINGSHENG else None
        todays_yicuoxie = YICUOXIE[yi] if YICUOXIE else None
        todays_shici = {'type': si_type, 'entries': [si_list[(si_idx + j) % len(si_list)] for j in range(2)]}  # 2 entries per day
        todays_xuci = xu_list[xu_idx] if xu_list else None
        
        # 5 idioms
        todays_idioms = []
        for j in range(5):
            idx_val = (ii + j) % len(IDIOMS)
            if IDIOMS:
                todays_idioms.append(IDIOMS[idx_val])
        
        body_parts.append(chinese_base_block(todays_chars, todays_idioms, todays_xingsheng, todays_yicuoxie, todays_shici, todays_xuci))
        check_items.append(f'今日5词语+5成语掌握 □')
        
        # 5. Rotating subject section
        svg_list_rot = SVG_MAP.get(rot_subj, {}).get(rot_topic, [])
        g9_tag = '<span style="color:var(--red);font-size:11px;font-weight:600">（初三预习）</span>' if rot_subj=='chemistry' or (rot_subj in GRADE9_TOPICS and rot_topic in GRADE9_TOPICS.get(rot_subj, set())) else ''
        body_parts.append(h3(rot_subj, f'{SUBJ_CN.get(rot_subj, rot_subj)} · {rot_topic} {g9_tag}'))
        body_parts.append(build_subject_section(rot_subj, rot_topic, svg_names=svg_list_rot))
        check_items.append(f'{rot_topic}理解 □')
        
        body = '\n'.join(body_parts)
        
        # Goal
        goal = f'系统学习{math_topic} / {eng_topic} / {chi_topic} / {rot_topic}'
        
        # Check
        check = '\n'.join(c for c in check_items)
        
        # Subjects header — colored dots matching index style
        cdots = {'math':'var(--blue)','english':'var(--green)','chinese':'var(--red)','physics':'var(--orange)','chemistry':'var(--purple)','politics':'#e91e63','history':'#795548'}
        c_chinese = cdots.get('chinese','var(--red)')
        c_rot = cdots.get(rot_subj, 'var(--purple)')
        subjects_str = f'<span class="sdots"><span class="sd" style="background:var(--blue)"></span><span class="sd" style="background:var(--green)"></span><span class="sd" style="background:{c_chinese}"></span><span class="sd" style="background:{c_rot}"></span></span>'
        
        # Generate HTML
        html = day_template(day_num, month_num, day_num_dt, wd,
                           subjects_str, goal, body, check,
                           prev_d, next_d)
        
        # Write file
        fname = f'day{day_num:03d}.html'
        fpath = f'{OUT}/{fname}'
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f'  Day {day_num:2d}: {month_num}/{day_num_dt} {wd} | '
              f'📖 {math_topic} | 🔤 {eng_topic} | 📖 {chi_topic} | {EMOJI.get(rot_subj,rot_subj)} {rot_topic} | '
              f'词汇{len(todays_vocab)}词')
    
    print(f'\nGenerated {54} daily pages in {OUT}/')

# ── Generate index page ──
def gen_index():
    total = 54
    idx = '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>暑假54天逆袭计划</title><style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;background:#f5f5f7;font-size:14px;line-height:1.8}
.hero{background:linear-gradient(135deg,#007aff,#5856d6);color:#fff;padding:28px 20px;text-align:center}
.hero h1{font-size:24px}
.hero .stats{margin:10px 0;font-size:13px}
.progress-bar{height:5px;background:rgba(255,255,255,.3);border-radius:3px;margin:8px auto;max-width:400px;overflow:hidden}
.progress-fill{height:100%;background:#34c759;border-radius:3px;transition:width .5s}
.week-card{background:#fff;border-radius:14px;margin:12px;overflow:hidden}
.week-header{background:linear-gradient(135deg,#007aff,#5856d6);color:#fff;padding:8px 14px;font-weight:700;font-size:15px;display:flex;justify-content:space-between}
.week-header .sun{font-size:11px;font-weight:400;opacity:.7}
.day-grid{display:grid;grid-template-columns:repeat(6,1fr)}
.day-item{text-decoration:none;color:#1d1d1f;padding:8px 4px;text-align:center;border-right:1px solid #eee;border-bottom:1px solid #eee;position:relative}
.day-item:nth-child(6n){border-right:none}.day-item:hover{background:#f0f7ff}
.day-item .dnum{font-size:14px;font-weight:700;color:#007aff}
.day-item .dsub{font-size:10px;color:#888}.day-item .dwd{font-size:9px;color:#bbb}
.day-item .status{position:absolute;top:3px;right:4px;font-size:13px}
.day-item .done{color:#34c759}.day-item .todo{color:#ddd}
.footer{text-align:center;color:#86868b;font-size:11px;padding:20px}
@media(max-width:500px){.day-grid{grid-template-columns:repeat(3,1fr)}.day-item:nth-child(6n){border-right:1px solid #eee}.day-item:nth-child(3n){border-right:none}}
</style></head><body>
<div class="hero"><h1>暑假54天逆袭计划</h1><p>6月29日-8月29日 · 周一至周六学习 · 周日休息</p>
<div class="stats"><span id="completed-count">已完成 0/54</span></div>
<div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div></div>
<div class="container">'''
    base = date(2026, 6, 29)
    for w in range(9):
        sun = base + timedelta(weeks=w, days=6)
        idx += f'<div class="week-card"><div class="week-header"><span>第{"一二三四五六七八九"[w]}周</span><span class="sun">☀️ {sun.month}/{sun.day}休息</span></div><div class="day-grid">'
        for d in range(6):
            dn = w*6+d+1
            dt = base+timedelta(weeks=w, days=d)
            idx += f'<a href="days/day{dn:03d}.html" class="day-item"><div class="dnum">Day {dn}</div><div class="dsub">{dt.month}/{dt.day}</div><div class="status todo" id="s{dn}">○</div></a>'
        idx += '</div></div>'
    idx += '''</div>
<script>
function update(){for(var i=1,total=54,done=0;i<=total;i++){var e=document.getElementById("s"+i);if(localStorage.getItem("day_"+i+"_done")==="true"){e.className="status done";e.textContent="✓";done++;}else{e.className="status todo";e.textContent="○";}}
document.getElementById("completed-count").textContent="已完成 "+done+"/54";document.getElementById("progress-fill").style.width=Math.round(done/54*100)+"%";}
window.onload=update;window.addEventListener("storage",update);
</script></body></html>'''
    idx_path = f'{LIB}/../index.html'
    with open(idx_path,'w',encoding='utf-8') as f:
        f.write(idx)
    print(f'Index generated ({os.path.getsize(idx_path)} bytes)')

# ── Link Checker ──
def check_links():
    """Verify all navigation links are working."""
    print('\n🔗 Checking navigation links...')
    errors = []
    
    # Check index.html has all 54 day links
    idx_path = f'{LIB}/../index.html'
    if os.path.exists(idx_path):
        with open(idx_path,'r',encoding='utf-8') as f:
            idx_content = f.read()
        for d in range(1, 55):
            link = f'days/day{d:03d}.html'
            if link not in idx_content:
                errors.append(f'Index: missing link to {link}')
    else:
        errors.append('Index: index.html not found')
    
    # Check each day page
    for d in range(1, 55):
        dp = f'{OUT}/day{d:03d}.html'
        if not os.path.exists(dp):
            errors.append(f'Day {d}: file not found')
            continue
        
        with open(dp,'r',encoding='utf-8') as f:
            content = f.read()
        
        # Check home link
        if '../index.html' not in content:
            errors.append(f'Day {d}: missing ../index.html link')
        
        # Check prev/next links
        if d > 1:
            prev_link = f'day{d-1:03d}.html'
            if prev_link not in content:
                errors.append(f'Day {d}: missing prev link {prev_link}')
        if d < 54:
            next_link = f'day{d+1:03d}.html'
            if next_link not in content:
                errors.append(f'Day {d}: missing next link {next_link}')
    
    if errors:
        print(f'  ❌ Found {len(errors)} link errors:')
        for e in errors:
            print(f'    {e}')
    else:
        print(f'  ✅ All {54} days + index links verified OK')
    
    return errors

# ── Syllabus / 考纲映射页面 ──
def gen_syllabus():
    """Generate syllabus.html mapping every knowledge point to its Day(s)."""
    print('\n📋 Generating syllabus page...')
    
    # Build reverse mapping: topic -> list of day numbers
    mapping = {}
    for subj in KNOWLEDGE:
        mapping[subj] = {}
        k = KNOWLEDGE[subj]
        sections = k.get('sections', k.get('chapters', []))
        for s in sections:
            for t in s.get('topics', []):
                mapping[subj][t['name']] = []
    
    # Simulate the schedule exactly
    start_date = date(2026, 6, 29)
    WD_CN = ['周一','周二','周三','周四','周五','周六']
    
    for day_num in range(1, 55):
        w = (day_num - 1) // 6
        d = (day_num - 1) % 6
        dt = start_date + timedelta(weeks=w, days=d)
        
        math_topic = get_topic('math', day_num)
        eng_topic  = get_topic('english', day_num)
        chi_topic  = get_topic('chinese', day_num)
        rot_subj   = ROTATING[(day_num - 1) % len(ROTATING)]  # rotate every day
        rot_topic  = get_topic(rot_subj, day_num, block_size=1)
        
        # Record
        for subj, topic in [('math', math_topic), ('english', eng_topic), 
                             ('chinese', chi_topic), (rot_subj, rot_topic)]:
            if subj in mapping and topic in mapping[subj]:
                mapping[subj][topic].append(day_num)
    
    # Build HTML
    SUBJ_COLORS = {
        'math': '#007aff', 'chinese': '#ff3b30', 'english': '#34c759',
        'physics': '#ff9500', 'chemistry': '#af52de', 'politics': '#e91e63', 'history': '#795548'
    }
    
    body_rows = ''
    total_topics = 0
    for subj in ['math','chinese','english','physics','chemistry','politics','history']:
        subj_cn = SUBJ_CN.get(subj, subj)
        color = SUBJ_COLORS.get(subj, '#333')
        
        # Section header
        body_rows += f'<tr style="background:#f5f5f7"><td colspan="4" style="font-weight:700;font-size:15px;color:{color};padding:10px 14px">📚 {subj_cn}</td></tr>'
        
        topics = mapping.get(subj, {})
        for topic_name, days in topics.items():
            total_topics += 1
            # Format days as links
            if days:
                day_links = ', '.join(f'<a href="days/day{d:03d}.html" style="color:{color}">Day {d}</a>' for d in days)
            else:
                day_links = '<span style="color:#ccc">—</span>'
            
            # Mark 9th grade topics
            tag = '<span style="color:#e91e63;font-size:10px;font-weight:600">（初三预习）</span>' if subj in GRADE9_TOPICS and topic_name in GRADE9_TOPICS[subj] else ''
            body_rows += f'<tr><td style="padding:6px 14px;font-size:13px">{topic_name} {tag}</td>'
            body_rows += f'<td style="padding:6px;font-size:12px;color:#888">{len(days)}天</td>'
            body_rows += f'<td style="padding:6px;font-size:11px">{day_links}</td>'
            go_link = f'<a href="days/day{days[0]:03d}.html" class="go-btn">▶</a>' if days else '<span style="color:#ccc">—</span>'
            body_rows += f'<td style="padding:6px;text-align:center">{go_link}</td></tr>'
    
    html = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>考纲知识点索引 · 暑假逆袭计划</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;background:#f5f5f7;font-size:14px;line-height:1.8;color:#1d1d1f}}
.hero{{background:linear-gradient(135deg,#5856d6,#007aff);color:#fff;padding:20px;text-align:center}}
.hero h1{{font-size:20px;margin-bottom:4px}}
.container{{max-width:900px;margin:0 auto;padding:12px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05)}}
th{{background:#f0f0f5;padding:8px 14px;font-size:12px;color:#666;text-align:left}}
tr{{border-bottom:1px solid #eee}}
tr:hover{{background:#f8f8ff}}
a{{text-decoration:none;font-weight:600}}
a:hover{{text-decoration:underline}}
.go-btn{{display:inline-block;width:28px;height:24px;line-height:24px;text-align:center;border-radius:12px;background:#007aff;color:#fff!important;font-size:11px}}
.nav-bar{{background:#fff;padding:10px 14px;margin-bottom:12px;border-radius:8px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
.nav-bar a{{padding:6px 14px;border-radius:16px;margin:0 3px;font-size:12px;background:#f0f0f5;color:#666}}
.nav-bar a:hover{{background:#007aff;color:#fff}}
.footer{{text-align:center;color:#86868b;font-size:11px;padding:20px}}
</style></head><body>
<div class="hero"><h1>📋 考纲知识点索引</h1><p>共 {total_topics} 个知识点 · 暑假54天全覆盖</p></div>
<div class="container">
<div class="nav-bar">
<a href="index.html">🏠 首页</a>
<a href="#math">📖 数学</a><a href="#chinese">📖 语文</a><a href="#english">🔤 英语</a>
<a href="#physics">⚡ 物理</a><a href="#chemistry">🧪 化学</a><a href="#politics">🏛️ 政治</a><a href="#history">📜 历史</a>
</div>
<table>
<tr><th style="width:35%">知识点</th><th style="width:8%">天数</th><th style="width:50%">覆盖日期 (点击跳转)</th><th style="width:7%">去</th></tr>
{body_rows}
</table>
</div>
<div class="footer">暑假逆袭计划 · 考纲索引 · 共 {total_topics} 个知识点</div>
</body></html>'''
    
    syllabus_path = f'{LIB}/../syllabus.html'
    with open(syllabus_path,'w',encoding='utf-8') as f:
        f.write(html)
    print(f'  ✅ Syllabus page generated ({os.path.getsize(syllabus_path)} bytes): {syllabus_path}')

# ── Main ──
if __name__ == '__main__':
    generate_all()
    # gen_index() disabled — index.html maintained separately with Apple style
    # gen_index()
    errors = check_links()
    gen_syllabus()
    print(f'\n{"="*60}')
    print(f'  生成完成: 54天页面 + index + syllabus')
    print(f'  链接检查: {"✅ 全部正常" if not errors else f"❌ {len(errors)}个错误"}')
    print(f'{"="*60}')
