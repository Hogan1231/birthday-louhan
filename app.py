"""
🎂 生日快乐网站 · 最终版
架构：整个网站是一个单页 HTML，用 st.components.v1.html() 渲染
      完全脱离 Streamlit 重跑机制，不再卡顿
      图片和音频全部 base64 内嵌，自包含，无需网络

交互：上下滑动（或鼠标滚轮）切换页面，流畅无刷新

文件结构（同一文件夹）：
    birthday_app.py
    envelope.png / cake.png / cat.png / isabell.png / bgm.mp3

运行：streamlit run birthday_app.py
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

st.set_page_config(
    page_title="Joyeux anniversaire 🎂",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 隐藏 Streamlit 所有默认 UI，让页面干净
st.markdown("""
<style>
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }

/* 让 Streamlit 外层容器铺满全屏，消除手机端白边/方块 */
.stApp,
.stAppViewContainer,
.appview-container,
.stMain,
.stMainBlockContainer,
.block-container,
.stVerticalBlock,
.stElementContainer {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 100vw !important;
    margin: 0 !important;
    padding: 0 !important;
}
.stApp,
.stAppViewContainer,
.appview-container {
    min-height: 100vh !important;
    height: 100vh !important;
    height: 100dvh !important;
}
.stMain {
    align-items: stretch !important;
    justify-content: flex-start !important;
}
.stElementContainer {
    height: auto !important;
}
.stIFrame {
    width: 100% !important;
    min-height: 100vh !important;
    height: 100vh !important;
    height: 100dvh !important;
}

.stApp { background: #fdf4ea; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 读取所有资源文件，转为 base64
# @st.cache_data 缓存：只在服务器首次启动时读一次，之后直接用缓存
# ─────────────────────────────────────────────
@st.cache_data
def load_all_assets():
    assets = {}
    files = {
        "envelope": "envelope.png",
        "cake":     "cake.png",
        "cat":      "cat.png",
        "isabell":  "isabell.png",
        "bgm":      "bgm.mp3",
    }
    base = Path(__file__).parent
    for key, fname in files.items():
        p = base / fname
        if p.exists():
            b64 = base64.b64encode(p.read_bytes()).decode()
            if fname.endswith(".png"):
                assets[key] = f"data:image/png;base64,{b64}"
            else:
                assets[key] = f"data:audio/mpeg;base64,{b64}"
        else:
            assets[key] = ""
    return assets

assets = load_all_assets()

# ─────────────────────────────────────────────
# 构建完整的单页 HTML
# 所有页面是垂直排列的 section，CSS scroll-snap 实现整屏吸附滑动
# ─────────────────────────────────────────────

# 图片标签生成（有图用图，没图用 emoji）
def img(key, emoji_fallback, style=""):
    src = assets.get(key, "")
    if src:
        return f'<img src="{src}" style="mix-blend-mode:multiply;{style}">'
    return f'<span style="font-size:72px;">{emoji_fallback}</span>'

envelope_tag = img("envelope", "✉️", "width:55vw;max-width:220px;display:block;margin:0 auto;animation:floatY 3s ease-in-out infinite;filter:drop-shadow(0 8px 20px rgba(196,149,106,0.2));")
cake_tag     = img("cake",     "🎂", "width:50vw;max-width:200px;display:block;margin:0 auto;animation:pulse 2.5s ease-in-out infinite;filter:drop-shadow(0 8px 24px rgba(253,168,180,0.25));")
isabell_tag  = img("isabell",  "🐶", "width:62vw;max-width:240px;display:block;margin:0 auto;filter:drop-shadow(0 6px 16px rgba(196,149,106,0.18));")
cat_tag      = img("cat",      "🐱", "width:100%;height:auto;mix-blend-mode:multiply;display:block;margin-top:4px;")

bgm_src = assets.get("bgm", "")

html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;1,400&family=Lora:ital,wght@0,400;0,500;1,400&family=Dancing+Script:wght@500;600&display=swap');

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body {{
    width: 100%; height: 100%;
    overflow: hidden;         /* 禁止 body 滚动，由容器控制 */
    background: #fdf4ea;
}}

/* ── 主容器：垂直全屏滚动 + scroll-snap ── */
#app {{
    width: 100vw;
    height: 100vh;
    overflow-y: scroll;
    overflow-x: hidden;
    scroll-snap-type: y mandatory;   /* 竖向整页吸附 */
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;           /* 隐藏滚动条 */
}}
#app::-webkit-scrollbar {{ display: none; }}

/* ── 每一页 ── */
.page {{
    width: 100vw;
    height: 100vh;
    scroll-snap-align: start;        /* 每页吸附到顶部 */
    scroll-snap-stop: always;        /* 一次只滑一页 */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 0 24px;
}}

/* ── 背景渐变（每页共用） ── */
.page {{
    background:
        radial-gradient(ellipse at 15% 40%, #fde3d0 0%, transparent 55%),
        radial-gradient(ellipse at 85% 15%, #fdd4e6 0%, transparent 45%),
        radial-gradient(ellipse at 55% 85%, #e4edfb 0%, transparent 45%),
        #fdf4ea;
}}

/* ── 文字排版 ── */
.t-script {{
    font-family: 'Dancing Script', cursive;
    color: #9b6b4a;
    text-align: center;
}}
.t-serif {{
    font-family: 'Playfair Display', serif;
    font-weight: 400;
    color: #7a4e2d;
    text-align: center;
    letter-spacing: 0.04em;
}}
.t-sub {{
    font-family: 'Lora', serif;
    color: #c4956a;
    text-align: center;
    letter-spacing: 0.14em;
    opacity: 0.82;
}}
.t-deco {{
    font-family: 'Dancing Script', cursive;
    color: #b08060;
    text-align: center;
    opacity: 0.82;
}}

/* ── 滑动提示箭头 ── */
.swipe-hint {{
    position: absolute;
    bottom: 22px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
    animation: breathe 2s ease-in-out infinite;
}}
.swipe-hint span {{
    font-family: 'Lora', serif;
    font-size: 10px;
    color: #c4956a;
    letter-spacing: 0.16em;
    opacity: 0.75;
}}
.swipe-arrow {{
    width: 16px;
    height: 16px;
    border-right: 1.5px solid #c4956a;
    border-bottom: 1.5px solid #c4956a;
    transform: rotate(45deg);
    opacity: 0.6;
    margin-top: 2px;
}}

/* ── 进度点 ── */
.dots {{
    display: flex;
    gap: 7px;
    justify-content: center;
    margin-top: 12px;
}}
.dot {{
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #c4956a;
    opacity: 0.22;
    transition: opacity 0.3s, transform 0.3s;
}}
.dot.on {{ opacity: 1; transform: scale(1.4); }}

/* ── 动画 ── */
@keyframes floatY {{
    0%,100% {{ transform: translateY(0); }}
    50%     {{ transform: translateY(-10px); }}
}}
@keyframes pulse {{
    0%,100% {{ transform: scale(1); }}
    50%     {{ transform: scale(1.05); }}
}}
@keyframes breathe {{
    0%,100% {{ opacity: 0.4; }}
    50%     {{ opacity: 1; }}
}}
@keyframes fadeInUp {{
    from {{ opacity:0; transform: translateY(18px); }}
    to   {{ opacity:1; transform: translateY(0); }}
}}
@keyframes shimmer {{
    0%   {{ background-position: -200% center; }}
    100% {{ background-position:  200% center; }}
}}

/* ── shimmer 彩虹文字 ── */
.shimmer {{
    background: linear-gradient(90deg, #f6a8b8, #f9d4a0, #a8d8ea, #f6a8b8);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
    font-size: 22px;
    letter-spacing: 10px;
}}

/* ── 彩带粒子 ── */
.confetti-wrap {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}}
.cp {{
    position: absolute;
    width: 8px; height: 14px;
    top: -20px;
    border-radius: 2px;
    opacity: 0;
    animation: cpFall linear infinite;
}}
@keyframes cpFall {{
    0%   {{ transform: translateY(0) rotate(0deg); opacity: 1; }}
    85%  {{ opacity: 1; }}
    100% {{ transform: translateY(105vh) rotate(600deg); opacity: 0; }}
}}

/* ── 信纸 ── */
.letter-card {{
    background: linear-gradient(135deg, #fffbef 0%, #fff8e1 50%, #fef3c7 100%);
    border: 1px solid rgba(196,149,106,0.22);
    border-radius: 3px;
    padding: 18px 14px 14px 22px;
    position: relative;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 2px 0 #f0dfc9, 0 4px 0 #e8d3b8, 0 12px 28px rgba(196,149,106,0.12);
}}
.letter-card::before {{
    content: '';
    display: block;
    width: 22px; height: 1.5px;
    background: #c4956a; opacity: 0.45;
    margin: 0 auto 14px;
}}
.letter-card::after {{
    content: '· · ·';
    display: block;
    text-align: center;
    color: #c4956a; opacity: 0.38;
    margin-top: 10px;
    font-size: 12px; letter-spacing: 5px;
}}
.letter-line {{
    position: absolute;
    left: 14px; top: 0; bottom: 0; width: 1px;
    background: linear-gradient(to bottom, transparent 5%, rgba(196,149,106,0.18) 20%, rgba(196,149,106,0.18) 80%, transparent 95%);
}}
.letter-inner {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
}}
.letter-text {{ flex: 1; min-width: 0; }}
.letter-img  {{ flex: 0 0 36%; max-width: 36%; }}
.letter-to {{
    font-family: 'Dancing Script', cursive;
    font-size: 16px; color: #9b6b4a;
    margin: 0 0 10px; opacity: 0.88;
}}
.letter-body {{
    font-family: 'Lora', serif;
    font-size: clamp(11px, 3vw, 13px);
    line-height: 1.9; color: #5c4033;
}}
.letter-body p {{ margin: 0 0 0.55em; }}
.letter-sign {{
    font-family: 'Dancing Script', cursive;
    font-size: 15px; color: #9b6b4a;
    text-align: right; margin-top: 8px;
}}
</style>
</head>
<body>

<!-- BGM：page 加载即播放，翻页不中断 -->
{'<audio id="bgm" autoplay loop><source src="' + bgm_src + '" type="audio/mpeg"></audio>' if bgm_src else ''}

<div id="app">

  <!-- ══ 页面 1：信封 ══ -->
  <section class="page" id="p1">
    <p class="t-script" style="font-size:clamp(20px,6vw,28px);margin-bottom:6px;">叮，你收到了一封信</p>
    <p class="t-sub"   style="font-size:clamp(11px,3vw,13px);margin-bottom:20px;">Une lettre t'attend</p>
    {envelope_tag}
    <p class="t-deco"  style="font-size:clamp(13px,3.5vw,16px);margin-top:16px;">just for you · 🌸</p>
    <div class="dots" id="dots1">
      <div class="dot on"></div><div class="dot"></div>
      <div class="dot"></div><div class="dot"></div>
    </div>
    <div class="swipe-hint"><span>向上滑动</span><div class="swipe-arrow"></div></div>
  </section>

  <!-- ══ 页面 2：蛋糕 ══ -->
  <section class="page" id="p2">
    <p class="t-serif" style="font-size:clamp(28px,7vw,38px);">生日快乐！！！</p>
    <p class="t-sub"   style="font-size:clamp(11px,3vw,13px);font-style:italic;margin-top:4px;margin-bottom:18px;">Happy Birthday Louhan!</p>
    {cake_tag}
    <p class="t-sub"   style="font-size:11px;margin-top:12px;animation:breathe 2s ease-in-out infinite;">✦ 闭上眼睛，许个愿吧 ✦</p>
    <p class="t-deco"  style="font-size:clamp(13px,3.5vw,16px);margin-top:10px;">✦ ✧ ✦ ✧ ✦</p>
    <div class="dots" id="dots2">
      <div class="dot"></div><div class="dot on"></div>
      <div class="dot"></div><div class="dot"></div>
    </div>
    <div class="swipe-hint"><span>向上滑动</span><div class="swipe-arrow"></div></div>
  </section>

  <!-- ══ 页面 3：彩带 + 伊莎贝尔 ══ -->
  <section class="page" id="p3">
    <!-- 彩带粒子层 -->
    <div class="confetti-wrap" id="confetti"></div>
    <div style="position:relative;z-index:1;width:100%;display:flex;flex-direction:column;align-items:center;">
      <span class="shimmer" style="display:block;text-align:center;margin-bottom:8px;">🎊 🎉 🎊</span>
      <p class="t-serif" style="font-size:clamp(24px,6vw,32px);font-style:italic;margin-bottom:4px;">准备蛋糕的小秘书西施惠</p>
      <p class="t-sub"   style="font-size:clamp(11px,3vw,13px);margin-bottom:14px;">听说しずえ是动森的吉祥物</p>
      {isabell_tag}
      <p class="t-deco"  style="font-size:clamp(13px,3.5vw,16px);margin-top:10px;">所以希望能给你带来好运</p>
      <div class="dots" id="dots3">
        <div class="dot"></div><div class="dot"></div>
        <div class="dot on"></div><div class="dot"></div>
      </div>
    </div>
  </section>

  <!-- ══ 页面 4：信纸 ══ -->
  <section class="page" id="p4">
    <p class="t-serif" style="font-size:clamp(20px,5vw,24px);font-style:italic;margin-bottom:14px;">给你的一封信</p>
    <div class="letter-card">
      <div class="letter-line"></div>
      <div class="letter-inner">
        <div class="letter-text">
          <p class="letter-to">致梁露菡，</p>
          <div class="letter-body">
            <p>Joyeux anniversaire！在多邻国刚好学到了这一部分，正好派上用场啦。</p>
            <p>不知道你的南法之旅如何，我希望这会是一段治愈的旅程，因为那儿有阳光、沙滩和海风。这些事情总能不断让人察觉到生命的美。</p>
            <p>如果静下来感受和思考，我总觉得这一切的美好，开始于降生后呼吸到的第一口空气，这或许就是为什么生日对我们来说总有特殊的意义。</p>
            <p>请好好享受这一天。希望你能永远保有感受美和幸福的力量。需要休息的时候，也可以随时找到你心中的老式家属院。</p>
            <p>祝你一切都好，我十分期待下一次与你见面。</p>
          </div>
          <p class="letter-sign">From 黄俊豪</p>
        </div>
        <div class="letter-img">{cat_tag}</div>
      </div>
    </div>
    <p style="text-align:center;font-size:15px;letter-spacing:7px;opacity:0.42;margin-top:10px;">🍎 🍊 🍑 🫐</p>
    <div class="dots" id="dots4">
      <div class="dot"></div><div class="dot"></div>
      <div class="dot"></div><div class="dot on"></div>
    </div>
  </section>

</div><!-- /#app -->

<script>
// ── BGM：降级处理（部分手机需要触摸后才能播放）──
var bgm = document.getElementById('bgm');
if (bgm) {{
    bgm.volume = 0.45;
    bgm.play().catch(function() {{
        document.addEventListener('touchstart', function() {{
            bgm.play();
        }}, {{ once: true }});
    }});
}}

// ── 彩带粒子生成 ──
(function() {{
    var colors = ["#f9a8d4","#fbbf24","#6ee7b7","#93c5fd","#c4b5fd","#f97316","#fb7185","#a3e635","#fdba74"];
    var wrap = document.getElementById('confetti');
    if (!wrap) return;
    for (var i = 0; i < 30; i++) {{
        var el = document.createElement('div');
        el.className = 'cp';
        var left  = Math.random() * 96 + 2;
        var delay = (Math.random() * 4).toFixed(2);
        var dur   = (Math.random() * 2.5 + 2.5).toFixed(2);
        var rot   = Math.floor(Math.random() * 60 - 30);
        var color = colors[Math.floor(Math.random() * colors.length)];
        el.style.cssText = 'left:' + left + '%;background:' + color +
            ';animation-duration:' + dur + 's;animation-delay:' + delay +
            's;transform:rotate(' + rot + 'deg);';
        wrap.appendChild(el);
    }}
}})();

// ── scroll-snap 已处理滑动，无需额外 JS ──
// 但需要同步更新进度点，监听 scroll 事件计算当前页
var app = document.getElementById('app');
var pages = document.querySelectorAll('.page');
var allDotGroups = [
    document.getElementById('dots1'),
    document.getElementById('dots2'),
    document.getElementById('dots3'),
    document.getElementById('dots4'),
];

function updateDots(idx) {{
    allDotGroups.forEach(function(g, gi) {{
        if (!g) return;
        var dots = g.querySelectorAll('.dot');
        dots.forEach(function(d, di) {{
            d.classList.toggle('on', di === idx);
        }});
    }});
}}

app.addEventListener('scroll', function() {{
    var idx = Math.round(app.scrollTop / window.innerHeight);
    updateDots(idx);
}}, {{ passive: true }});
</script>
</body>
</html>"""

# ─────────────────────────────────────────────
# 渲染：用 components.html 铺满整个视口
# height 设为 100vh（像素近似值 900，实际由 CSS 控制）
# ─────────────────────────────────────────────
components.html(html, height=900, scrolling=False)
