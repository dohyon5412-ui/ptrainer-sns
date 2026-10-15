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
