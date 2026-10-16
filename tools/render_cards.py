#!/usr/bin/env python3
"""P trainer 인스타 카드 렌더러.

사용법:  python3 tools/render_cards.py specs/<날짜>-<종류>.json cards/<날짜>/
사양 JSON 형식은 tools/README.md 참고. 1080x1350 PNG를 1.png ... N.png 로 저장합니다.
"""
import json,re,sys,os
from playwright.sync_api import sync_playwright
CSS=r'''
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:var(--H,1350px);font-family:"Noto Sans CJK KR",sans-serif;word-break:keep-all;-webkit-font-smoothing:antialiased}
.c{width:1080px;height:var(--H,1350px);overflow:hidden;position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:250px 88px 170px}
.navy{background:linear-gradient(170deg,#2b3a5c,#1c273d);color:#fff}
.paper{background:#f6f7fa;color:#1c2333}
.cream{background:#fff6dc;color:#1c273d}
.cream:before{content:"";position:absolute;left:-120px;top:-120px;width:520px;height:520px;border-radius:50%;background:#ffe27a;z-index:0}
.cream:after{content:"";position:absolute;right:-160px;bottom:22%;width:460px;height:460px;border-radius:50%;background:#ffd0c4;z-index:0}
.cream>*{position:relative;z-index:1}.cream>.top,.cream>.pg,.cream>.logo{position:absolute}
.cream h1 em{font-style:normal;color:#ff5a3c}
.cream .lead{color:#5b6478;opacity:1}
.cream .pg{color:#7a8296}
.cream.brandc:before{top:auto;bottom:-170px;left:-170px}
.cream .logo{color:#1c273d}.cream .logo b{color:#ff5a3c}
.top{position:absolute;top:90px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:14px}
.pill{background:#f3c64d;color:#2a1f00;border-radius:999px;padding:10px 28px;font-size:34px;font-weight:800}
.pill.red{background:#e03131;color:#fff}
.sub2{font-size:34px;font-weight:700;opacity:.85}
.paper .sub2{color:#33456d}
h1{text-wrap:balance;font-size:84px;line-height:1.28;font-weight:900;letter-spacing:-.02em}
h1 em,h2 em{font-style:normal}
.navy h1 em{color:#f3c64d}
.lead{font-size:38px;line-height:1.55;opacity:.85;margin-top:40px;font-weight:500}
h2{text-wrap:balance;font-size:62px;line-height:1.3;font-weight:900;letter-spacing:-.02em}
.paper h2 em{color:#ff6a00}
.box{width:100%;text-align:center;background:#fff;border-radius:32px;padding:44px 48px;margin-top:44px;box-shadow:8px 12px 34px -14px rgba(24,32,52,.28),0 0 0 2px #e2e6ee}
.box p,.box li{text-wrap:pretty;font-size:38px;line-height:1.6;color:#3f485c;font-weight:500}
.box p+p{margin-top:18px}
.box ul{list-style:none;display:grid;gap:20px}
.box li{position:relative}
.box li:before{content:"";display:inline-block;vertical-align:middle;margin:-6px 16px 0 0;width:14px;height:14px;border-radius:50%;background:#3a4d78}
.box.alert{background:#fbedf2;box-shadow:8px 12px 34px -14px rgba(24,32,52,.25)}
.box.alert li:before{background:#e03131}
.box.tip{background:#fcf4dd;box-shadow:8px 12px 34px -14px rgba(24,32,52,.25)}
.lab{display:block;font-size:30px;font-weight:800;color:#7d5c0e;margin-bottom:12px}
table{width:100%;border-collapse:collapse}
td,th{font-size:36px;line-height:1.5;padding:20px 0;border-top:2px solid #e2e6ee;text-align:center;vertical-align:top;color:#3f485c;font-weight:500}
tr:first-child td,tr:first-child th{border-top:0}
th{width:220px;color:#33456d;font-weight:800}
.src{font-size:26px;color:#7a8296;margin-top:24px;line-height:1.5}
.cta{margin-top:56px;background:#f3c64d;color:#1c273d;border-radius:28px;padding:34px 40px;font-size:38px;font-weight:800;line-height:1.45}
.note{font-size:27px;opacity:.7;margin-top:28px;line-height:1.5}
.pg{position:absolute;bottom:56px;left:0;right:0;text-align:center;font-size:36px;font-weight:800}
.navy .pg{color:#fff}.paper .pg{color:#26334f}
.logo{position:absolute;right:88px;bottom:54px;font-weight:900;font-size:40px;letter-spacing:-.01em}
.logo b{color:#f3c64d;font-size:46px}
.paper .logo{color:#26334f}
'''
LOGO=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','assets','plug-logo.png')
def brand(theme):
    # 상단 중앙: PLUG 로고 + Ptrainer 로고만 (바탕 칩 없음, 두 로고 글자 높이 맞춤)
    import base64
    f=LOGO.replace('plug-logo.png','plug-logo-white.png') if theme=='navy' else LOGO
    b64=base64.b64encode(open(f,'rb').read()).decode()
    ink={'navy':'#fff','paper':'#26334f','cream':'#1c273d'}.get(theme,'#1c273d')
    pc={'cream':'#ff5a3c'}.get(theme,'#f3c64d')
    return ('<div class="top" style="top:84px"><div style="display:flex;align-items:center;gap:34px">'
            f'<img src="data:image/png;base64,{b64}" style="height:84px;display:block">'
            f'<span style="font-size:66px;line-height:1;font-weight:900;color:{ink};letter-spacing:-.02em;transform:translateY(-7px)"><b style="color:{pc}">P</b>trainer</span></div></div>')
def top(tag,sub,red=False):
    return f'<div class="top"><span class="pill{" red" if red else ""}">{tag}</span>'+(f'<span class="sub2">{sub}</span>' if sub else '')+'</div>'
def brk(h):
    # 마침표/물음표/느낌표 뒤에서 줄바꿈 (설명 상자 안 <p>, <li>만)
    return re.sub(r'(?<=[.?!])\s+(?=[^\s<])','<br>',h)
def page(c,i,n):
    body=re.sub(r'(<(p|li)( [^>]*)?>)(.*?)(</\2>)',lambda m:m.group(1)+brk(m.group(4))+m.group(5),c['body'])
    inner=(brand(c['theme']) if c.get('brand') else top(c['tag'],c.get('sub',''),c.get('red',False)))+body
    mark='' if c.get('brand') else '<div class="logo"><b>P</b>trainer</div>'
    return f'<html><head><meta charset="utf-8"><style>{CSS}:root{{--H:{H}px}}{REEL if H>1350 else ''}</style></head><body><div class="c {c["theme"]}{' brandc' if c.get('brand') else ''}">{inner}<div class="pg">{i} / {n}</div>{mark}</div></body></html>'
# 릴스 화면 위아래는 인스타 버튼에 가리므로 안전 영역 안으로 당긴다
REEL='.top{top:250px!important}.pg{bottom:330px}.logo{bottom:326px}.c{padding:420px 88px 400px}'
H=int(os.environ.get('CARD_H','1350'))  # 릴스·스토리용은 CARD_H=1920
def main(spec,out):
    s=json.load(open(spec,encoding='utf8'));os.makedirs(out,exist_ok=True)
    name=s.get('name','card');files=[]
    with sync_playwright() as p:
        b=p.chromium.launch();pg=b.new_page(viewport={'width':1080,'height':H})
        for i,c in enumerate(s['cards'],1):
            pg.set_content(page(c,i,len(s['cards'])));pg.wait_for_timeout(150)
            f=os.path.join(out,f'{name}-{i}.png');pg.screenshot(path=f);files.append(f)
        b.close()
    print('\n'.join(files))
if __name__=='__main__':main(sys.argv[1],sys.argv[2])
