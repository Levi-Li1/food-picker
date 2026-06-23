#!/usr/bin/env python3
"""Comprehensive Chinese (语文) content supplement for guct.html.
Adds missing 讲/练/结 to existing sections and new sections for W5."""

import re

# ─── Chinese content templates ───

# W5: Day 29-35 Chinese sections (30min each)
W5_CHINESE = {
    'd29': '''\n<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:16px 0 12px">📚 语文 · 古诗文实词积累（30min）</h3>
<div class="steps">
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（15min）</h4><p><b>中考必考12实词</b>：①安——怎么/安定 ②被——通"披"穿/覆盖 ③本——本来/根本 ④鄙——目光短浅 ⑤毕——完成/都 ⑥薄——迫近/轻视 ⑦策——马鞭/鞭打 ⑧长——与"短"相对/长久 ⑨朝——早晨/朝廷 ⑩诚——确实/如果 ⑪出——出去/产生 ⑫辞——告辞/语言</p><p><b>记忆方法</b>：语境推断法（根据上下文猜义）、成语联想法（成语保留古义如"走马观花"中"走=跑"）</p></div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（10min）</h4><p>1."肉食者鄙"中"鄙"意为? <b>答</b>：目光短浅。 2."薄暮冥冥"中"薄"意为? <b>答</b>：迫近。</p><p>3."策之不以其道"中"策"意为? <b>答</b>：鞭打（名词作动词）。</p></div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（5min）</h4><p>📔 制12个实词卡片：正面写词，背面写义项+例句</p></div>
</div>''',

    'd30': '''\n<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:16px 0 12px">📚 语文 · 文言文虚词——之乎者也（30min）</h3>
<div class="steps">
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（15min）</h4><p><b>中考四大核心虚词</b>：</p><p><b>之</b>：①代词(代人/事/物) "学而时习之" ②结构助词"的" "醉翁之意不在酒" ③主谓间取消独立性 ④动词"到/往"</p><p><b>而</b>：①并列 "黑质而白章" ②转折 "可远观而不可亵玩" ③顺承 "温故而知新" ④修饰 "面山而居"</p><p><b>以</b>：①介词"用/拿/凭" ②连词"来/因为" ③动词"认为"</p><p><b>其</b>：①代词"他/它/那" ②语气词"大概/难道"</p></div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（10min）</h4><p>1."予独爱莲之出淤泥而不染"中"之"作用? <b>答</b>：主谓间取消独立性，不译。</p><p>2."人不知而不愠"中"而"表? <b>答</b>：转折。 3."以其境过清"中"以"意为? <b>答</b>：因为。</p></div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（5min）</h4><p>📔 之而以其→默写每个虚词的所有用法</p></div>
</div>''',

    'd31': '''\n<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:16px 0 12px">📚 语文 · 现代文阅读——含义题（30min）</h3>
<div class="steps">
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（15min）</h4><p><b>词语含义题答题公式</b>：本义（字典意思）+语境义（在文中的特殊含义/修辞/情感）</p><p><b>句子含义题公式</b>：表层意思（字面）+深层意思（主旨/情感/哲理）</p><p><b>常考点</b>：<b>词语</b>——找它在文中的指代内容、找它的修辞含义。<b>句子</b>——关注位置(开头/结尾/过渡)+修辞手法+作者情感。</p></div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（10min）</h4><p>1."父亲的背影"中"背影"除了指背影还象征什么? <b>答</b>：父亲的衰老、父爱的深沉。</p><p>2.赏析句"春天像刚落地的娃娃"的手法? <b>答</b>：比喻，生动形象写出春天充满生机和希望。</p></div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（5min）</h4><p>📔 含义题公式：本义+语境义+情感 → 背下来</p></div>
</div>''',

    'd32': '''\n<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:16px 0 12px">📚 语文 · 作文——记叙文开头技法（30min）</h3>
<div class="steps">
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（15min）</h4><p><b>四大精彩开头法</b>：</p><p>①<b>设问式</b>——"你见过凌晨四点的校园吗？"开头设问吸引读者好奇心。</p><p>②<b>引用式</b>——"生活不止眼前的苟且，还有诗和远方。"引用名言增加文采。</p><p>③<b>场景式</b>——"窗外的雨淅淅沥沥地下着，教室里只剩我一个人……"画面感强。</p><p>④<b>对比式</b>——"别人暑假在打游戏，我的暑假在图书馆泡了60天。"对比突出主题。</p><p><b>开头三忌</b>：忌啰嗦/忌跑题/忌抄袭。</p></div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（10min）</h4><p>分别用四种开头法，为"我的暑假"各写一个开头（每种50字以内）。</p><p><b>例</b>——设问式："60天能改变什么？我的回答是：一切。"</p></div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（5min）</h4><p>📔 把四个开头写在作文本上，选最好的发展成一篇600字作文</p></div>
</div>''',

    'd33': '''\n<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:16px 0 12px">📚 语文 · 古诗鉴赏——意象与意境（30min）</h3>
<div class="steps">
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（15min）</h4><p><b>常见意象及其含义</b>：月→思乡(举头望明月)；柳→送别(柳谐"留")；落花→时光流逝/伤感；流水→愁绪(问君能有几多愁？恰似一江春水向东流)；孤雁→孤独/思亲；梅兰竹菊→君子品格</p><p><b>意境</b>：诗歌通过意象营造的整体氛围。常见意境：雄浑壮阔/凄凉悲苦/恬淡闲适/孤寂冷清/清新明丽。</p><p><b>答题思路</b>：找出意象→分析特点→概括意境→联系情感。</p></div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（10min）</h4><p>1."枯藤老树昏鸦"营造了怎样的意境? <b>答</b>：萧瑟凄凉的秋日黄昏意境，表达游子思乡的悲苦。</p><p>2."明月"在古诗中通常表达? <b>答</b>：思乡怀人。</p></div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（5min）</h4><p>📔 整理10个常见意象及其含义</p></div>
</div>''',

    'd34': '''\n<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:16px 0 12px">📚 语文 · 文言文翻译五字诀（30min）</h3>
<div class="steps">
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（15min）</h4><p><b>文言翻译五字诀</b>：</p><p><b>留</b>——人名/地名/官名/朝代/度量衡保留不译。如"庆历四年春"→"庆历四年的春天"。</p><p><b>换</b>——古语换今语。如"吾"换"我"，"汝"换"你"，"尝"换"曾经"。</p><p><b>补</b>——补出省略成分。如"一鼓作气，再(鼓)而衰，三(鼓)而竭"。</p><p><b>删</b>——删去无实义的虚词。如"夫战，勇气也"中"夫"删去。</p><p><b>调</b>——调整倒装语序。如"何陋之有"→"有何陋"→"有什么简陋呢？"</p></div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（10min）</h4><p>用五字诀翻译：1."马之千里者"（定语后置→"千里马"） 2."甚矣，汝之不惠"（主谓倒装→"你不聪明太严重了"→"你也太不聪明了"）</p></div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（5min）</h4><p>📔 五字诀口诀：留换补删调→背熟+各写一例</p></div>
</div>''',

    'd35': '''\n<h3 style="color:var(--red);border-bottom:2px solid var(--red);padding-bottom:6px;margin:16px 0 12px">📚 语文 · 名著《骆驼祥子》阅读（30min）</h3>
<div class="steps">
<div class="step"><h4><span class="dot" style="background:var(--red)"></span>讲（15min）</h4><p><b>《骆驼祥子》老舍</b>——现代文学经典。主人公祥子是旧北京的人力车夫。</p><p><b>三起三落</b>：①攒三年买新车→被兵抢走 ②卖骆驼攒钱→被孙侦探敲诈 ③用虎妞钱买车→虎妞死后卖车葬妻</p><p><b>人物形象</b>：祥子——从勤劳善良的青年变成自私堕落的行尸走肉(旧社会把人变成鬼)。虎妞——泼辣有心机。小福子——善良悲苦。</p><p><b>主题</b>：揭露旧社会的黑暗，表达对底层劳动人民的同情。</p></div>
<div class="step"><h4><span class="dot" style="background:var(--orange)"></span>练（10min）</h4><p>1.祥子为什么被称为"骆驼祥子"? <b>答</b>：车被抢后牵回三匹骆驼卖掉，得了这个外号。</p><p>2.祥子"三起三落"对你有什么启示? <b>答</b>：个人奋斗在黑暗社会中难以成功，但祥子的堕落也有自身局限——他没有找到正确的出路。</p></div>
<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（5min）</h4><p>📔 画出祥子"三起三落"的命运曲线图</p></div>
</div>''',
}

# Missing 练/结 for existing Chinese sections
# Format: day_id -> (section_h3_match_text, content_to_insert_before_section_end)
EXISTING_FIXES = {
    # W3 Day 15: 陋室铭 - needs 结
    'd15': {
        'h3_match': '文言文《陋室铭》',
        'insert_before': '</div></div>',  # before day close
        'content': '''\n<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（10min）</h4><p><b>陋室铭核心考点</b>：①主旨——安贫乐道、高洁傲岸 ②名句——"斯是陋室，惟吾德馨"（主旨句）、"谈笑有鸿儒，往来无白丁"（交往之人高雅）、"无丝竹之乱耳，无案牍之劳形"（反面衬托） ③类比——"南阳诸葛庐，西蜀子云亭"——以自己的陋室比诸葛亮的草庐和扬雄的亭子 ④背诵全文+默写</p></div>\n'''
    },
    # W3 Day 17: 爱莲说 - needs 结
    'd17': {
        'h3_match': '文言文《爱莲说》',
        'insert_before': '</div></div>',
        'content': '''\n<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（10min）</h4><p><b>爱莲说核心考点</b>：①托物言志——以莲花比喻君子品格 ②三种花象征——菊(隐士·陶渊明)、牡丹(富贵者·世人)、莲(君子·作者) ③名句——"出淤泥而不染，濯清涟而不妖"(不与世俗同流合污) ④背诵全文+默写重点句</p></div>\n'''
    },
    # W4 Day 27: 议论文阅读 - needs 结
    'd27': {
        'h3_match': '议论文阅读',
        'insert_before': '</div></div>',
        'content': '''\n<div class="step full"><h4><span class="dot" style="background:var(--purple)"></span>结（10min）</h4><p><b>议论文答题速记</b>：①论点=作者观点主张(常在开头/结尾) ②论据=事实论据/道理论据 ③论证方法六种→背口诀：引道对比举例证 ④议论文语言特点：严密/准确/有说服力</p></div>\n'''
    },
}

def inject_chinese(html):
    """Inject Chinese content into guct.html."""
    modified = False
    
    # ── Part 1: W5 Day 29-35 ──
    for day_id, content in W5_CHINESE.items():
        # Find the day's check div
        day_start = html.find(f'id="{day_id}"')
        if day_start == -1: continue
        
        # Find closing of the last section before check div
        check_pos = html.find('<div class="check">', day_start)
        if check_pos == -1: continue
        
        # Insert Chinese section before check div
        insert_pos = check_pos
        html = html[:insert_pos] + content + '\n' + html[insert_pos:]
        print(f'  W5 {day_id}: added Chinese section')
        modified = True
    
    # ── Part 2: Fix existing incomplete sections ──
    for day_id, fix in EXISTING_FIXES.items():
        day_start = html.find(f'id="{day_id}"')
        if day_start == -1: continue
        
        # Find next day's start
        next_day = html.find('<div class="day-page"', day_start + 10)
        if next_day == -1: next_day = len(html)
        
        # Find the specific Chinese section
        h3_pos = html.find(fix['h3_match'], day_start, next_day)
        if h3_pos == -1: continue
        
        # Find the insertion point (before section end, before next h3 or check)
        # Search for the closing </div></div> pattern after the h3
        search_start = h3_pos
        # Find the NEXT h3 after this one, or check div
        next_h3 = html.find('<h3', search_start + 50, next_day)
        check_pos = html.find('<div class="check">', search_start, next_day)
        
        sec_end = min(next_h3 if next_h3 > 0 else 999999, check_pos if check_pos > 0 else 999999)
        if sec_end == 999999:
            sec_end = next_day
        
        # Find the last </div> before sec_end
        insert_point = html.rfind('</div>', h3_pos, sec_end)
        if insert_point == -1: continue
        
        html = html[:insert_point] + fix['content'] + html[insert_point:]
        print(f'  {day_id}: added 结 to {fix["h3_match"][:30]}...')
        modified = True
    
    return html, modified


def main():
    fname = 'C:/Users/Tebon/BangMaker/Claw/guct.html'
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    
    print("=== 语文内容补充 ===")
    html, mod = inject_chinese(html)
    
    if mod:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'\nDone! guct.html updated.')
    else:
        print('No changes needed.')

if __name__ == '__main__':
    main()
