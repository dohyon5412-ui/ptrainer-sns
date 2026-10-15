#!/usr/bin/env python3
"""P trainer 인스타 카드 렌더러.

사용법:  python3 tools/render_cards.py specs/<날짜>-<종류>.json cards/<날짜>/
사양 JSON 형식은 tools/README.md 참고. 1080x1350 PNG를 1.png ... N.png 로 저장합니다.
"""
import json,re,sys,os
from playwright.sync_api import sync_playwright
CSS=r'''
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;font-family:"Noto Sans CJK KR",sans-serif;word-break:keep-all;-webkit-font-smoothing:antialiased}
.c{width:1080px;height:1350px;position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:250px 88px 170px}
.navy{background:linear-gradient(170deg,#2b3a5c,#1c273d);color:#fff}
.paper{background:#f6f7fa;color:#1c2333}
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
def top(tag,sub,red=False):
    return f'<div class="top"><span class="pill{" red" if red else ""}">{tag}</span>'+(f'<span class="sub2">{sub}</span>' if sub else '')+'</div>'
def brk(h):
    # 마침표/물음표/느낌표 뒤에서 줄바꿈 (설명 상자 안 <p>, <li>만)
    return re.sub(r'(?<=[.?!])\s+(?=[^\s<])','<br>',h)
def page(c,i,n):
    body=re.sub(r'(<(p|li)( [^>]*)?>)(.*?)(</\2>)',lambda m:m.group(1)+brk(m.group(4))+m.group(5),c['body'])
    inner=top(c['tag'],c.get('sub',''),c.get('red',False))+body
    return f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="c {c["theme"]}">{inner}<div class="pg">{i} / {n}</div><div class="logo"><b>P</b>trainer</div></div></body></html>'
def main(spec,out):
    s=json.load(open(spec,encoding='utf8'));os.makedirs(out,exist_ok=True)
    name=s.get('name','card');files=[]
    with sync_playwright() as p:
        b=p.chromium.launch();pg=b.new_page(viewport={'width':1080,'height':1350})
        for i,c in enumerate(s['cards'],1):
            pg.set_content(page(c,i,len(s['cards'])));pg.wait_for_timeout(150)
            f=os.path.join(out,f'{name}-{i}.png');pg.screenshot(path=f);files.append(f)
        b.close()
    print('\n'.join(files))
if __name__=='__main__':main(sys.argv[1],sys.argv[2])
