"""Generate SVG diagram database for all subjects"""
import json

SVGS = {}

# ═══ MATH: Number Line ═══
SVGS['math_number_line'] = {
    'subject':'math','name':'数轴','desc':'数轴三要素：原点/正方向/单位长度',
    'svg':'''
<svg viewBox="0 0 400 80"><defs><marker id="arrow" markerWidth="6" markerHeight="4" refX="6" refY="2" orient="auto"><path d="M0,0 L6,2 L0,4" fill="#666"/></marker></defs>
<line x1="20" y1="45" x2="380" y2="45" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
<line x1="140" y1="50" x2="140" y2="40" stroke="#007aff" stroke-width="2.5"/>
<text x="135" y="35" fill="#007aff" font-size="13" font-weight="bold">-3</text>
<line x1="200" y1="50" x2="200" y2="40" stroke="#e65100" stroke-width="2.5"/>
<text x="196" y="35" fill="#e65100" font-size="13" font-weight="bold">0</text>
<line x1="260" y1="50" x2="260" y2="40" stroke="#007aff" stroke-width="2.5"/>
<text x="256" y="35" fill="#007aff" font-size="13" font-weight="bold">3</text>
<line x1="80" y1="50" x2="80" y2="40" stroke="#888" stroke-width="1.5"/>
<line x1="260" y1="55" x2="200" y2="55" stroke="#34c759" stroke-width="1.5" stroke-dasharray="4,2"/>
<text x="215" y="70" fill="#34c759" font-size="11">|3|=3</text>
<line x1="140" y1="55" x2="200" y2="55" stroke="#ff3b30" stroke-width="1.5" stroke-dasharray="4,2"/>
<text x="140" y="70" fill="#ff3b30" font-size="11">|-3|=3</text>
<text x="365" y="65" fill="#888" font-size="10">→ 正方向</text>
</svg>'''
}

# ═══ MATH: Coordinate System ═══
SVGS['math_coordinate'] = {
    'subject':'math','name':'平面直角坐标系','desc':'四个象限+点的坐标',
    'svg':'''
<svg viewBox="0 0 400 280"><defs><marker id="arr" markerWidth="6" markerHeight="4" refX="6" refY="2" orient="auto"><path d="M0,0 L6,2 L0,4" fill="#666"/></marker></defs>
<line x1="30" y1="240" x2="370" y2="240" stroke="#666" stroke-width="1.5" marker-end="url(#arr)"/>
<line x1="200" y1="260" x2="200" y2="20" stroke="#666" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="375" y="238" fill="#666" font-size="13">x</text><text x="204" y="18" fill="#666" font-size="13">y</text>
<circle cx="200" cy="240" r="3" fill="#e65100"/><text x="204" y="258" fill="#e65100" font-size="12" font-weight="bold">O(0,0)</text>
<!-- Quadrant labels -->
<text x="290" y="50" fill="#ccc" font-size="13">第一象限 (+,+)</text>
<text x="30" y="50" fill="#ccc" font-size="13">第二象限 (-,+)</text>
<text x="30" y="210" fill="#ccc" font-size="13">第三象限 (-,-)</text>
<text x="290" y="210" fill="#ccc" font-size="13">第四象限 (+,-)</text>
<!-- Point A (3,2) -->
<circle cx="290" cy="180" r="4" fill="#007aff"/>
<line x1="290" y1="240" x2="290" y2="180" stroke="#007aff" stroke-width="1" stroke-dasharray="3,2"/>
<line x1="200" y1="180" x2="290" y2="180" stroke="#007aff" stroke-width="1" stroke-dasharray="3,2"/>
<text x="295" y="172" fill="#007aff" font-size="12">A(3,2)</text>
</svg>'''
}

# ═══ MATH: Pythagorean Theorem ═══
SVGS['math_pythagorean'] = {
    'subject':'math','name':'勾股定理','desc':'a²+b²=c²',
    'svg':'''
<svg viewBox="0 0 300 200"><rect x="1" y="1" width="298" height="198" rx="8" fill="#fafafa" stroke="#ddd" stroke-width="1"/>
<polygon points="40,170 280,170 120,30" fill="none" stroke="#007aff" stroke-width="2.5"/>
<text x="145" y="165" fill="#007aff" font-size="13" font-weight="bold">a</text>
<text x="190" y="105" fill="#ff3b30" font-size="13" font-weight="bold">b</text>
<text x="65" y="105" fill="#34c759" font-size="13" font-weight="bold">c</text>
<!-- Right angle marker -->
<polyline points="120,150 140,150 140,170" fill="none" stroke="#999" stroke-width="1.5"/>
<text x="50" y="30" fill="#e65100" font-size="14" font-weight="bold">a² + b² = c²</text>
<!-- Squares on each side -->
<rect x="40" y="120" width="50" height="50" fill="rgba(0,122,255,0.1)" stroke="#007aff" stroke-width="1" stroke-dasharray="3,2"/>
<rect x="120" y="30" width="140" height="140" fill="rgba(52,199,89,0.08)" stroke="#34c759" stroke-width="1" stroke-dasharray="3,2" transform="rotate(45,190,100)"/>
</svg>'''
}

# ═══ MATH: Functions graph ═══
SVGS['math_functions'] = {
    'subject':'math','name':'一次函数与二次函数','desc':'y=kx+b和y=ax²+bx+c的图像对比',
    'svg':'''
<svg viewBox="0 0 400 200">
<line x1="20" y1="100" x2="380" y2="100" stroke="#ccc" stroke-width="1"/>
<line x1="200" y1="180" x2="200" y2="20" stroke="#ccc" stroke-width="1"/>
<text x="382" y="98" fill="#999" font-size="11">x</text><text x="204" y="18" fill="#999" font-size="11">y</text>
<!-- Linear function: y=2x-1 -->
<line x1="80" y1="140" x2="320" y2="40" stroke="#007aff" stroke-width="2.5"/>
<text x="280" y="40" fill="#007aff" font-size="11" font-weight="bold">y=2x+1</text>
<!-- Quadratic function: y=-x²+4x -->
<path d="M60,30 Q130,10 200,60 Q270,110 340,30" fill="none" stroke="#ff3b30" stroke-width="2.5"/>
<text x="300" y="160" fill="#ff3b30" font-size="11" font-weight="bold">y=-x²+4x</text>
<circle cx="200" cy="60" r="3" fill="#ff3b30"/><text x="180" y="55" fill="#ff3b30" font-size="10">顶点(2,4)</text>
</svg>'''
}

# ═══ MATH: Geometry - Triangle ═══
SVGS['math_triangle'] = {
    'subject':'math','name':'全等三角形','desc':'SSS/SAS/ASA/AAS/HL判定',
    'svg':'''
<svg viewBox="0 0 400 160">
<rect x="1" y="1" width="398" height="158" rx="8" fill="#fafafa" stroke="#ddd" stroke-width="1"/>
<!-- Triangle ABC -->
<polygon points="30,130 180,130 100,20" fill="rgba(0,122,255,0.08)" stroke="#007aff" stroke-width="2"/>
<text x="20" y="148" fill="#007aff" font-size="13" font-weight="bold">A</text>
<text x="180" y="148" fill="#007aff" font-size="13" font-weight="bold">B</text>
<text x="95" y="15" fill="#007aff" font-size="13" font-weight="bold">C</text>
<text x="90" y="120" fill="#007aff" font-size="12">AB=DE</text>
<!-- Triangle DEF -->
<polygon points="220,130 370,130 290,20" fill="rgba(255,59,48,0.08)" stroke="#ff3b30" stroke-width="2"/>
<text x="210" y="148" fill="#ff3b30" font-size="13" font-weight="bold">D</text>
<text x="370" y="148" fill="#ff3b30" font-size="13" font-weight="bold">E</text>
<text x="285" y="15" fill="#ff3b30" font-size="13" font-weight="bold">F</text>
<!-- Congruence marks -->
<line x1="80" y1="130" x2="100" y2="110" stroke="#34c759" stroke-width="2"/>
<line x1="270" y1="130" x2="290" y2="110" stroke="#34c759" stroke-width="2"/>
<text x="30" y="190" fill="#666" font-size="11">三边对应相等(SSS) / 两边夹角(SAS) / 两角夹边(ASA) / 两角对边(AAS) / 直角斜边(HL)</text>
</svg>'''
}

# ═══ PHYSICS: Light Reflection ═══
SVGS['physics_reflection'] = {
    'subject':'physics','name':'光的反射定律','desc':'反射角=入射角,三线共面',
    'svg':'''
<svg viewBox="0 0 360 200">
<!-- Mirror -->
<line x1="50" y1="20" x2="310" y2="180" stroke="#333" stroke-width="4"/>
<line x1="60" y1="22" x2="70" y2="32" stroke="#333" stroke-width="1.5"/>
<line x1="75" y1="40" x2="85" y2="50" stroke="#333" stroke-width="1.5"/>
<line x1="220" y1="68" x2="260" y2="50" stroke="#ff3b30" stroke-width="2.5"/>
<text x="250" y="45" fill="#ff3b30" font-size="12">入射光线</text>
<line x1="170" y1="95" x2="130" y2="113" stroke="#007aff" stroke-width="2.5"/>
<text x="85" y="115" fill="#007aff" font-size="12">反射光线</text>
<!-- Normal -->
<line x1="180" y1="100" x2="180" y2="160" stroke="#999" stroke-width="1.5" stroke-dasharray="5,3"/>
<text x="182" y="170" fill="#999" font-size="10">法线</text>
<!-- Angles -->
<path d="M200,90 A30,30 0 0,0 190,80" fill="none" stroke="#e65100" stroke-width="1.5"/>
<text x="205" y="80" fill="#e65100" font-size="11">∠i</text>
<path d="M160,100 A30,30 0 0,1 150,110" fill="none" stroke="#34c759" stroke-width="1.5"/>
<text x="140" y="118" fill="#34c759" font-size="11">∠r</text>
<text x="25" y="45" fill="#e65100" font-size="11">反射定律:</text>
<text x="25" y="62" fill="#333" font-size="11">反射角∠r=入射角∠i</text>
</svg>'''
}

# ═══ PHYSICS: Lens Imaging ═══
SVGS['physics_lens'] = {
    'subject':'physics','name':'凸透镜成像','desc':'5种成像情况',
    'svg':'''
<svg viewBox="0 0 500 200">
<!-- Lens -->
<ellipse cx="250" cy="100" rx="8" ry="70" fill="rgba(0,122,255,0.15)" stroke="#007aff" stroke-width="2"/>
<text x="255" y="15" fill="#007aff" font-size="11">凸透镜</text>
<text x="348" y="103" fill="#999" font-size="10">F</text><text x="148" y="103" fill="#999" font-size="10">F</text>
<line x1="160" y1="100" x2="250" y2="100" stroke="#ccc" stroke-width="1"/><line x1="250" y1="100" x2="340" y2="100" stroke="#ccc" stroke-width="1"/>
<line x1="340" y1="105" x2="340" y2="95" stroke="#ccc" stroke-width="1"/><line x1="160" y1="105" x2="160" y2="95" stroke="#ccc" stroke-width="1"/>
<!-- Arrow object at u>2f -->
<line x1="50" y1="100" x2="50" y2="50" stroke="#ff3b30" stroke-width="3"/><text x="25" y="45" fill="#ff3b30" font-size="11">物体</text>
<!-- Rays from object through lens -->
<line x1="50" y1="50" x2="250" y2="50" stroke="#e65100" stroke-width="1.5" stroke-dasharray="4,2"/>
<line x1="250" y1="50" x2="420" y2="50" stroke="#e65100" stroke-width="1.5"/>
<line x1="50" y1="50" x2="340" y2="50" stroke="#34c759" stroke-width="1" stroke-dasharray="3,2"/>
<line x1="340" y1="50" x2="250" y2="100" stroke="#34c759" stroke-width="1"/>
<!-- Image at f<v<2f -->
<line x1="390" y1="100" x2="390" y2="70" stroke="#007aff" stroke-width="2.5"/>
<text x="370" y="65" fill="#007aff" font-size="11">倒立缩小实像</text>
<text x="25" y="185" fill="#999" font-size="11">u>2f → 倒立缩小实像(照相机)</text>
</svg>'''
}

# ═══ PHYSICS: Force diagram ═══
SVGS['physics_forces'] = {
    'subject':'physics','name':'受力分析','desc':'重力/支持力/摩擦力示意图',
    'svg':'''
<svg viewBox="0 0 360 200">
<defs><marker id="arr2" markerWidth="6" markerHeight="4" refX="6" refY="2" orient="auto"><path d="M0,0 L6,2 L0,4" fill="#666"/></marker></defs>
<!-- Ground -->
<rect x="20" y="160" width="320" height="30" fill="#ddd" stroke="#999" stroke-width="1"/>
<!-- Block -->
<rect x="140" y="100" width="80" height="60" fill="rgba(0,122,255,0.15)" stroke="#007aff" stroke-width="2" rx="3"/>
<text x="170" y="135" fill="#007aff" font-size="12" font-weight="bold">物块</text>
<!-- Gravity (down) -->
<line x1="180" y1="160" x2="180" y2="195" stroke="#ff3b30" stroke-width="2.5" marker-end="url(#arr2)"/>
<text x="148" y="192" fill="#ff3b30" font-size="12" font-weight="bold">G=mg</text>
<!-- Support (up) -->
<line x1="180" y1="100" x2="180" y2="65" stroke="#34c759" stroke-width="2.5" marker-end="url(#arr2)"/>
<text x="148" y="60" fill="#34c759" font-size="12" font-weight="bold">F支持</text>
<!-- Friction (left) -->
<line x1="140" y1="130" x2="100" y2="130" stroke="#e65100" stroke-width="2.5" marker-end="url(#arr2)"/>
<text x="60" y="125" fill="#e65100" font-size="12" font-weight="bold">F摩擦</text>
<!-- Pull (right) -->
<line x1="220" y1="130" x2="260" y2="130" stroke="#9c27b0" stroke-width="2.5" marker-end="url(#arr2)"/>
<text x="260" y="125" fill="#9c27b0" font-size="12" font-weight="bold">F拉</text>
</svg>'''
}

# ═══ PHYSICS: Circuit ═══
SVGS['physics_circuit'] = {
    'subject':'physics','name':'串联与并联电路','desc':'两种基本电路连接方式',
    'svg':'''
<svg viewBox="0 0 450 180">
<!-- Series circuit -->
<rect x="10" y="5" width="200" height="170" rx="8" fill="rgba(0,122,255,0.04)" stroke="#ddd" stroke-width="1"/>
<text x="55" y="25" fill="#007aff" font-size="12" font-weight="bold">串联电路</text>
<line x1="40" y1="50" x2="40" y2="90" stroke="#e65100" stroke-width="2"/>
<line x1="40" y1="90" x2="80" y2="90" stroke="#e65100" stroke-width="2"/>
<circle cx="80" cy="90" r="12" fill="none" stroke="#999" stroke-width="1.5"/><text x="73" y="95" fill="#666" font-size="9">L₁</text>
<line x1="92" y1="90" x2="130" y2="90" stroke="#e65100" stroke-width="2"/>
<circle cx="130" cy="90" r="12" fill="none" stroke="#999" stroke-width="1.5"/><text x="123" y="95" fill="#666" font-size="9">L₂</text>
<line x1="142" y1="90" x2="170" y2="90" stroke="#e65100" stroke-width="2"/>
<line x1="170" y1="90" x2="170" y2="50" stroke="#e65100" stroke-width="2"/>
<circle cx="170" cy="50" r="10" fill="rgba(255,59,48,0.3)" stroke="#ff3b30" stroke-width="2"/><text x="166" y="54" fill="#fff" font-size="8">+</text>
<line x1="170" y1="40" x2="40" y2="40" stroke="#e65100" stroke-width="2"/>
<text x="65" y="130" fill="#666" font-size="10">I=I₁=I₂, U=U₁+U₂</text>
<!-- Parallel circuit -->
<rect x="230" y="5" width="210" height="170" rx="8" fill="rgba(52,199,89,0.04)" stroke="#ddd" stroke-width="1"/>
<text x="285" y="25" fill="#34c759" font-size="12" font-weight="bold">并联电路</text>
<line x1="260" y1="50" x2="260" y2="95" stroke="#34c759" stroke-width="2"/>
<line x1="260" y1="95" x2="290" y2="95" stroke="#34c759" stroke-width="2"/>
<circle cx="290" cy="95" r="12" fill="none" stroke="#999" stroke-width="1.5"/><text x="283" y="100" fill="#666" font-size="9">L₁</text>
<line x1="302" y1="95" x2="380" y2="95" stroke="#34c759" stroke-width="2"/>
<line x1="260" y1="95" x2="260" y2="130" stroke="#34c759" stroke-width="2"/>
<circle cx="260" cy="130" r="12" fill="none" stroke="#999" stroke-width="1.5"/><text x="253" y="135" fill="#666" font-size="9">L₂</text>
<line x1="260" y1="142" x2="380" y2="142" stroke="#34c759" stroke-width="2"/>
<rect x="370" y="90" width="10" height="55" fill="none" stroke="#34c759" stroke-width="2"/>
<circle cx="380" cy="50" r="10" fill="rgba(255,59,48,0.3)" stroke="#ff3b30" stroke-width="2"/><text x="376" y="54" fill="#fff" font-size="8">+</text>
<line x1="380" y1="40" x2="260" y2="40" stroke="#34c759" stroke-width="2"/>
<text x="265" y="160" fill="#666" font-size="10">I=I₁+I₂, U=U₁=U₂</text>
</svg>'''
}

# ═══ PHYSICS: Lever ═══
SVGS['physics_lever'] = {
    'subject':'physics','name':'杠杆原理','desc':'F₁L₁=F₂L₂',
    'svg':'''
<svg viewBox="0 0 400 180">
<!-- Fulcrum -->
<polygon points="200,150 185,180 215,180" fill="#666"/>
<line x1="200" y1="150" x2="200" y2="180" stroke="#666" stroke-width="2"/>
<text x="204" y="175" fill="#999" font-size="10">支点O</text>
<!-- Lever bar -->
<line x1="50" y1="130" x2="350" y2="130" stroke="#333" stroke-width="6" stroke-linecap="round"/>
<!-- Left force (down) -->
<line x1="100" y1="130" x2="100" y2="180" stroke="#ff3b30" stroke-width="3"/>
<text x="75" y="175" fill="#ff3b30" font-size="12" font-weight="bold">F₂</text>
<!-- Right force (down) -->
<line x1="300" y1="130" x2="300" y2="50" stroke="#007aff" stroke-width="3"/>
<text x="280" y="45" fill="#007aff" font-size="12" font-weight="bold">F₁</text>
<!-- Distance markers -->
<line x1="200" y1="155" x2="100" y2="155" stroke="#999" stroke-width="1" stroke-dasharray="3,2"/>
<text x="130" y="167" fill="#999" font-size="11">L₂</text>
<line x1="200" y1="155" x2="300" y2="155" stroke="#999" stroke-width="1" stroke-dasharray="3,2"/>
<text x="240" y="167" fill="#999" font-size="11">L₁</text>
<text x="100" y="20" fill="#e65100" font-size="14" font-weight="bold">F₁×L₁ = F₂×L₂</text>
</svg>'''
}

# ═══ CHEMISTRY: Atomic Structure ═══
SVGS['chem_atom'] = {
    'subject':'chemistry','name':'原子结构','desc':'原子核(质子+中子)+核外电子',
    'svg':'''
<svg viewBox="0 0 360 200">
<rect x="1" y="1" width="358" height="198" rx="8" fill="#fafafa" stroke="#ddd" stroke-width="1"/>
<!-- Nucleus -->
<circle cx="180" cy="100" r="15" fill="#ff3b30"/>
<text x="172" y="105" fill="#fff" font-size="11" font-weight="bold">+</text>
<!-- Electron orbits -->
<ellipse cx="180" cy="100" rx="50" ry="30" fill="none" stroke="#007aff" stroke-width="1" stroke-dasharray="4,2"/>
<ellipse cx="180" cy="100" rx="80" ry="45" fill="none" stroke="#34c759" stroke-width="1" stroke-dasharray="4,2"/>
<!-- Electrons -->
<circle cx="140" cy="82" r="4" fill="#007aff"/><text x="125" y="78" fill="#007aff" font-size="10">e⁻</text>
<circle cx="220" cy="82" r="4" fill="#007aff"/>
<circle cx="180" cy="118" r="4" fill="#007aff"/>
<circle cx="115" cy="125" r="4" fill="#34c759"/>
<circle cx="245" cy="125" r="4" fill="#34c759"/>
<!-- Labels -->
<text x="35" y="20" fill="#ff3b30" font-size="11" font-weight="bold">原子核(质子+中子)</text>
<text x="35" y="38" fill="#007aff" font-size="11">• 核外电子(带负电)</text>
<text x="35" y="56" fill="#666" font-size="11">• 质子数=核外电子数(原子不显电性)</text>
<text x="35" y="74" fill="#999" font-size="11">• 第一层≤2,第二层≤8,最外层≤8</text>
</svg>'''
}

# ═══ CHEMISTRY: Molecule ═══
SVGS['chem_molecule'] = {
    'subject':'chemistry','name':'分子与原子','desc':'分子由原子构成,化学变化中分子可分原子不可分',
    'svg':'''
<svg viewBox="0 0 360 140">
<rect x="1" y="1" width="358" height="138" rx="8" fill="#fafafa" stroke="#ddd" stroke-width="1"/>
<!-- H₂O molecule -->
<circle cx="120" cy="70" r="22" fill="rgba(255,59,48,0.2)" stroke="#ff3b30" stroke-width="2.5"/>
<text x="112" y="75" fill="#ff3b30" font-size="13" font-weight="bold">O</text>
<circle cx="70" cy="100" r="14" fill="rgba(0,122,255,0.2)" stroke="#007aff" stroke-width="2"/>
<text x="64" y="105" fill="#007aff" font-size="11" font-weight="bold">H</text>
<circle cx="170" cy="100" r="14" fill="rgba(0,122,255,0.2)" stroke="#007aff" stroke-width="2"/>
<text x="164" y="105" fill="#007aff" font-size="11" font-weight="bold">H</text>
<!-- Bonds -->
<line x1="90" y1="90" x2="110" y2="82" stroke="#999" stroke-width="2"/>
<line x1="130" y1="82" x2="150" y2="90" stroke="#999" stroke-width="2"/>
<text x="115" y="130" fill="#666" font-size="11">水分子 H₂O</text>
<!-- Arrow -->
<text x="210" y="75" fill="#999" font-size="18">→</text>
<!-- Separate atoms -->
<circle cx="265" cy="70" r="18" fill="rgba(255,59,48,0.15)" stroke="#ff3b30" stroke-width="2"/>
<text x="259" y="75" fill="#ff3b30" font-size="11" font-weight="bold">O</text>
<circle cx="315" cy="95" r="12" fill="rgba(0,122,255,0.15)" stroke="#007aff" stroke-width="2"/>
<text x="310" y="100" fill="#007aff" font-size="9" font-weight="bold">H</text>
<circle cx="315" cy="50" r="12" fill="rgba(0,122,255,0.15)" stroke="#007aff" stroke-width="2"/>
<text x="310" y="55" fill="#007aff" font-size="9" font-weight="bold">H</text>
</svg>'''
}

# ═══ HISTORY: Timeline ═══
SVGS['history_timeline'] = {
    'subject':'history','name':'中国近代史时间轴','desc':'列强侵略与近代化探索',
    'svg':'''
<svg viewBox="0 0 600 160">
<defs><marker id="arr3" markerWidth="6" markerHeight="4" refX="6" refY="2" orient="auto"><path d="M0,0 L6,2 L0,4" fill="#999"/></marker></defs>
<line x1="20" y1="80" x2="580" y2="80" stroke="#999" stroke-width="3" marker-end="url(#arr3)"/>
<!-- Events -->
<circle cx="80" cy="80" r="8" fill="#ff3b30"/><line x1="80" y1="72" x2="80" y2="55" stroke="#ff3b30" stroke-width="1.5"/><text x="35" y="50" fill="#ff3b30" font-size="10" font-weight="bold">1840鸦片战争</text>
<circle cx="160" cy="80" r="6" fill="#e65100"/><line x1="160" y1="72" x2="160" y2="55" stroke="#e65100" stroke-width="1.5"/><text x="128" y="50" fill="#e65100" font-size="10">1860火烧圆明园</text>
<circle cx="240" cy="80" r="8" fill="#ff3b30"/><line x1="240" y1="72" x2="240" y2="55" stroke="#ff3b30" stroke-width="1.5"/><text x="208" y="50" fill="#ff3b30" font-size="10" font-weight="bold">1894甲午战争</text>
<circle cx="320" cy="80" r="8" fill="#9c27b0"/><line x1="320" y1="88" x2="320" y2="105" stroke="#9c27b0" stroke-width="1.5"/><text x="280" y="118" fill="#9c27b0" font-size="10" font-weight="bold">1911辛亥革命</text>
<circle cx="400" cy="80" r="6" fill="#007aff"/><line x1="400" y1="88" x2="400" y2="105" stroke="#007aff" stroke-width="1.5"/><text x="365" y="118" fill="#007aff" font-size="10">1919五四运动</text>
<circle cx="480" cy="80" r="8" fill="#34c759"/><line x1="480" y1="88" x2="480" y2="105" stroke="#34c759" stroke-width="1.5"/><text x="445" y="118" fill="#34c759" font-size="10" font-weight="bold">1921中共一大</text>
<circle cx="540" cy="80" r="7" fill="#e91e63"/><line x1="540" y1="72" x2="540" y2="55" stroke="#e91e63" stroke-width="1.5"/><text x="510" y="46" fill="#e91e63" font-size="10" font-weight="bold">1949建国</text>
</svg>'''
}

# Save as JSON
with open('C:/Users/Tebon/BangMaker/Claw/study_library/svg/diagrams.json','w',encoding='utf-8') as f:
    json.dump(SVGS, f, ensure_ascii=False, indent=2)
print(f'Saved {len(SVGS)} SVG diagrams')
for name, data in SVGS.items():
    print(f'  {name}: {data["name"]} ({len(data["svg"])} chars)')
