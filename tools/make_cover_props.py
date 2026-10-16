# 말이 늦은 아이(t01) 표지: 교구 그림 + 상단 PLUG & Ptrainer 로고. 실행하면 cover-brand-1350/1920.png 생성
from playwright.sync_api import sync_playwright
NAVY='#1c273d'
# 빨대 꽂힌 컵
cup=f'''<svg width="240" height="330" viewBox="0 0 240 330">
<g transform="rotate(8 150 40)"><rect x="130" y="0" width="22" height="190" rx="11" fill="#fff" stroke="{NAVY}" stroke-width="6"/>
<g fill="#ff5a3c"><rect x="133" y="22" width="16" height="16"/><rect x="133" y="60" width="16" height="16"/><rect x="133" y="98" width="16" height="16"/><rect x="133" y="136" width="16" height="16"/></g></g>
<path d="M30 130 L210 130 L190 320 L50 320 Z" fill="#8fd3ff" stroke="{NAVY}" stroke-width="7" stroke-linejoin="round"/>
<path d="M40 175 L200 175" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".7"/>
<rect x="22" y="118" width="196" height="22" rx="11" fill="#fff" stroke="{NAVY}" stroke-width="7"/></svg>'''
# 비눗방울 막대 + 방울
bub=f'''<svg width="300" height="360" viewBox="0 0 300 360">
<circle cx="200" cy="70" r="58" fill="#e9f6ff" fill-opacity=".85" stroke="#5b8def" stroke-width="6"/><path d="M170 45 q15 -18 35 -14" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round"/>
<circle cx="255" cy="170" r="32" fill="#e9f6ff" fill-opacity=".85" stroke="#5b8def" stroke-width="5"/>
<circle cx="120" cy="25" r="20" fill="#e9f6ff" stroke="#5b8def" stroke-width="5"/>
<g transform="translate(40 0) rotate(-20 90 230)"><circle cx="90" cy="150" r="44" fill="#d9f0ff" fill-opacity=".9" stroke="{NAVY}" stroke-width="12"/><circle cx="90" cy="150" r="44" fill="none" stroke="#ff9b3c" stroke-width="6"/>
<rect x="82" y="194" width="16" height="120" rx="8" fill="#ff9b3c" stroke="{NAVY}" stroke-width="6"/></g></svg>'''
# 그림책
book=f'''<svg width="320" height="250" viewBox="0 0 320 250">
<path d="M160 40 Q100 10 20 30 L20 220 Q100 200 160 230 Z" fill="#fff" stroke="{NAVY}" stroke-width="7" stroke-linejoin="round"/>
<path d="M160 40 Q220 10 300 30 L300 220 Q220 200 160 230 Z" fill="#fff" stroke="{NAVY}" stroke-width="7" stroke-linejoin="round"/>
<circle cx="90" cy="100" r="32" fill="#ffd84d" stroke="{NAVY}" stroke-width="5"/>
<path d="M50 175 Q90 140 130 175" fill="#7bd389" stroke="{NAVY}" stroke-width="5"/>
<g stroke="{NAVY}" stroke-width="7" stroke-linecap="round"><line x1="195" y1="80" x2="270" y2="75"/><line x1="195" y1="115" x2="270" y2="110"/><line x1="195" y1="150" x2="250" y2="146"/></g></svg>'''
# 손거울
mirror=f'''<svg width="200" height="300" viewBox="0 0 200 300">
<g transform="rotate(-12 100 150)"><rect x="86" y="170" width="28" height="120" rx="14" fill="#c792ea" stroke="{NAVY}" stroke-width="7"/>
<circle cx="100" cy="95" r="82" fill="#c792ea" stroke="{NAVY}" stroke-width="7"/><circle cx="100" cy="95" r="62" fill="#eaf6ff" stroke="{NAVY}" stroke-width="5"/>
<circle cx="80" cy="85" r="7" fill="{NAVY}"/><circle cx="120" cy="85" r="7" fill="{NAVY}"/><path d="M76 112 Q100 135 124 112" stroke="{NAVY}" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M60 60 L78 44" stroke="#fff" stroke-width="9" stroke-linecap="round"/></g></svg>'''
# 장난감 전화기
phone=f'''<svg width="290" height="230" viewBox="0 0 290 230">
<path d="M40 130 Q40 95 75 92 L215 92 Q250 95 250 130 L265 215 L25 215 Z" fill="#ff5a3c" stroke="{NAVY}" stroke-width="7" stroke-linejoin="round"/>
<circle cx="145" cy="160" r="34" fill="#fff" stroke="{NAVY}" stroke-width="6"/><circle cx="145" cy="160" r="10" fill="{NAVY}"/>
<path d="M30 70 Q30 25 75 25 L215 25 Q260 25 260 70 L230 80 Q220 55 200 58 L90 58 Q70 55 60 80 Z" fill="#ffd84d" stroke="{NAVY}" stroke-width="7" stroke-linejoin="round"/></svg>'''
import sys;sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)));import render_cards as RC
def mk(H):
  return f'''<html><head><meta charset=utf8><style>*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:{H}px;font-family:"Noto Sans CJK KR";word-break:keep-all;overflow:hidden}}
.a{{position:absolute}}</style></head><body>
<div style="position:relative;width:1080px;height:{H}px;background:#fff6dc;overflow:hidden"><div style="position:absolute;left:-170px;bottom:-170px;width:520px;height:520px;border-radius:50%;background:#ffe27a"></div><div style="position:absolute;left:0;top:{(H-1350)//2}px;width:1080px;height:1350px;color:{NAVY}">
<div class="a" style="right:-160px;bottom:260px;width:460px;height:460px;border-radius:50%;background:#ffd0c4"></div>
<div class="a" style="left:0;right:0;top:200px;text-align:center"><span style="background:#e03131;color:#fff;font-size:34px;font-weight:800;padding:10px 28px;border-radius:999px">요즘 이슈 · 말과 소통</span></div>
<div class="a" style="left:0;right:0;top:290px;text-align:center;font-size:96px;font-weight:900;line-height:1.2;letter-spacing:-2px">말이 늦은<br>우리 아이</div>
<div class="a" style="left:0;right:0;top:548px;text-align:center"><span style="display:inline-block;background:{NAVY};color:#ffd84d;font-size:76px;font-weight:900;padding:12px 40px;border-radius:24px">언제까지 기다려요?</span></div>
<div class="a" style="left:0;right:0;top:708px;text-align:center;font-size:38px;font-weight:700;color:#5b6478">18개월·두 돌·세 돌, 나이별로 정리했어요</div>
<div class="a" style="left:60px;top:790px">{bub}</div>
<div class="a" style="left:330px;top:1000px">{book}</div>
<div class="a" style="left:610px;top:800px">{cup}</div>
<div class="a" style="left:820px;top:860px">{mirror}</div>
<div class="a" style="left:88px;bottom:56px;font-size:30px;font-weight:600;color:#7a8296">1 / 5</div>
'''+RC.brand('cream').replace('class="top" style="top:84px"','class="a" style="left:0;right:0;top:70px;display:flex;justify-content:center"')+f'''
</div></div></body></html>'''
import sys
for H in (1350,1920):
  html=mk(H)
  with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':H})
    pg.set_content(html); pg.wait_for_timeout(300); pg.screenshot(path=f'cover-brand-{H}.png'); b.close()
