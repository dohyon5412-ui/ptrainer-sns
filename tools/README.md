# 카드 사양(spec) 형식

`specs/<날짜>-news.json`, `specs/<날짜>-excerpt-<글id>.json`

```json
{
  "name": "news",                      // 파일 이름 앞부분 (news-1.png ...)
  "cards": [
    {
      "theme": "navy",                 // 표지·마지막 장 navy, 가운데 장 paper
      "tag": "오늘의 발달 뉴스",         // 맨 위 가운데 노란 태그
      "sub": "2026.10.16",             // 태그 아래 보조 문구 (날짜, 주제 등)
      "red": false,                    // true면 빨간 태그 (요즘 이슈, 꼭 확인)
      "body": "<h1>...</h1><p class=\"lead\">...</p>",
      "text": "카드에 들어간 글 (대체 텍스트·원고함용)"
    }
  ]
}
```

## body에 쓰는 요소
- 표지/마지막 장(navy): `<h1>제목<br><em>노란 강조</em></h1>`, `<p class="lead">`, `<div class="cta">`, `<p class="note">`
- 가운데 장(paper): `<h2>제목<br><em>주황 강조</em></h2>` 다음에
  - `<div class="box"><p>…</p></div>` 기본 설명
  - `<div class="box tip"><span class="lab">라벨</span><p>…</p></div>` 노란 팁
  - `<div class="box alert"><ul><li>…</li></ul></div>` 분홍 확인 신호
  - `<div class="box"><table><tr><th>18개월</th><td>…</td></tr></table></div>` 표
  - `<p class="src">출처: …</p>`

## 글 규칙 (꼭 지키기)
- 모든 글은 가운데 정렬로 렌더링됨. 문장 끝(. ? !) 뒤에서 자동 줄바꿈.
- 한 문장이 두 줄을 넘으면 의미 단위로 `<br>` 직접 넣기 (예: "~명이던 아이가<br>2025년에는 ~").
- 제목은 2~3줄, 말하듯 자연스럽게. 기호(■ ▶ ✔ 이모지) 쓰지 않기.
- 홑따옴표는 ‘ ’(곡선) 사용. 파이썬 문자열 깨짐 방지.

## 실행
```
python3 tools/render_cards.py specs/2026-10-16-news.json cards/2026-10-16/
```

## OX 퀴즈 1장 (specs/example-quiz.json)
- 문제 h1 아래에 파란 O, 빨간 X 원을 나란히 넣는다. example-quiz.json 1장 body의 `<div style="display:flex...">` 부분을 그대로 복사해서 쓴다.
- 1장에는 정답을 쓰지 않는다. 3장은 댓글 유도용: "궁금한 내용이 있으면 댓글로 알려 주세요" + "O, X 답도 함께 남겨 주세요" + note "정답과 설명은 아래 캡션에 있어요." 정답과 설명은 캡션(specs/example-quiz-caption.txt 형식).

## 브랜드 로고 (마무리 장)
- 카드에 `"brand": true`를 넣으면 맨 위 노란 태그 대신 상단 중앙에 "PLUG 로고  Ptrainer"가 바탕 칩 없이 글자 높이를 맞춰 들어가고, 우측 하단 Ptrainer 표시는 빠진다. 남색 카드에서는 흰 글자 PLUG(assets/plug-logo-white.png)를 쓴다.

## 크림 테마 (표지·마무리 장)
- `"theme": "cream"`: 크림 바탕 + 노랑·분홍 동그라미, 남색 글자, h1 강조는 주황. 첫 장과 마지막 장을 같은 미감으로 맞출 때 쓴다(예: specs/2026-10-16-excerpt-t01.json 5장).

## 릴스·스토리 크기(1080x1920)
- `CARD_H=1920 python3 tools/render_cards.py <spec> <폴더>` 로 같은 사양을 세로형으로 다시 렌더링한다. 위아래 인스타 버튼에 가리지 않게 안전 영역 안으로 배치된다.
- 영상: `ffmpeg -framerate 1/3 -i <이름>-reel-%d.png -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 -vf "fps=30,format=yuv420p" -c:v libx264 -preset slow -tune stillimage -crf 16 -c:a aac -b:a 128k -shortest -movflags +faststart <이름>-reel.mp4`

## 브랜드 로고 (PLUG & Ptrainer)
- 마지막 장: `"brand": true` → 상단 중앙에 `PLUG 로고 & Ptrainer` (칩 없음, 높이 맞춤, Ptrainer는 PLUG와 비슷한 Poppins Bold 둥근 획·P는 PLUG 파랑, &는 글자색(크림·흰 바탕은 검정, 남색 바탕은 흰색) 세리프 이탤릭).
- 표지(1장): `"brand": "cover"` → 같은 로고 아래에 tag 칩·sub를 그대로 둔다(본문은 자동으로 아래로 내려감).
- **첫 페이지(표지)와 마지막 페이지에만** 넣는다. 중간 장은 기존 tag 칩. 이때 우측 하단 Ptrainer 표시는 숨김.
- 크림 표지는 로고와 겹치지 않게 노란 원을 왼쪽 아래로 옮기고, 태그 칩·제목을 로고 아래로 내린다(예: tools/make_cover_props.py).

- 우측 하단 Ptrainer 표시는 모든 장에서 쓰지 않는다. 쪽번호는 모든 장 가운데 아래.
