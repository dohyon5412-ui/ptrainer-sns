"""카드(1080x1350)를 릴스·스토리 크기(1080x1920)로 바꾸고, 원하면 슬라이드 영상(mp4)도 만든다.
사용법: python3 tools/make_reel.py cards/<날짜>/<접두어> [초=3]
예:     python3 tools/make_reel.py cards/2026-10-16/excerpt-t01 3
        python3 tools/make_reel.py 'cards/2026-10-16/news-*-v4' 3   (다시 만든 판)
결과:   cards/<날짜>/reel/<접두어>-1.png ... 와 <접두어>.mp4
카드 위아래를 카드 맨 윗줄·아랫줄 색으로 이어 붙여서 양옆이 잘리지 않고 이음새도 보이지 않는다."""
import sys, os, glob, subprocess, re
from PIL import Image
prefix = sys.argv[1]; sec = float(sys.argv[2]) if len(sys.argv) > 2 else 3
if '*' in prefix:  # 예: cards/2026-10-16/news-*-v4  (같은 날 다시 만든 -v2 같은 파일)
    files = sorted(glob.glob(prefix + '.png'), key=lambda p: int(re.search(r'-(\d+)(?:-v\d+)?\.png$', p).group(1)))
else:
    files = sorted(glob.glob(prefix + '-[0-9].png') + glob.glob(prefix + '-[0-9][0-9].png'),
                   key=lambda p: int(re.search(r'-(\d+)\.png$', p).group(1)))
if not files: sys.exit('카드를 찾지 못했어요: ' + prefix)
outdir = os.path.join(os.path.dirname(prefix), 'reel'); os.makedirs(outdir, exist_ok=True)
W, H = 1080, 1920
outs = []
for f in files:
    c = Image.open(f).convert('RGB')
    if c.size != (1080, 1350): c = c.resize((1080, 1350))
    pad = (H - 1350) // 2
    top = c.crop((0, 0, W, 1)).resize((W, pad))
    bot = c.crop((0, 1349, W, 1350)).resize((W, H - 1350 - pad))
    bg = Image.new('RGB', (W, H)); bg.paste(top, (0, 0)); bg.paste(c, (0, pad)); bg.paste(bot, (0, pad + 1350))
    o = os.path.join(outdir, os.path.basename(f)); bg.save(o); outs.append(o); print(o)
lst = os.path.join(outdir, '_list.txt')
with open(lst, 'w') as fh:
    for o in outs: fh.write(f"file '{os.path.abspath(o)}'\nduration {sec}\n")
    fh.write(f"file '{os.path.abspath(outs[-1])}'\n")
mp4 = os.path.join(outdir, os.path.basename(prefix).replace('-*', '') + '.mp4')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
                '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-movflags', '+faststart', mp4], check=True)
os.remove(lst); print(mp4)
