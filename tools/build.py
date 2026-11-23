#!/usr/bin/env python3
"""Build a lesson page from the template.

Usage:  python3 tools/build.py lessons/01-weather.json
Reads   template/practice-template.html, the lesson JSON and its mp3 (lesson["audio"], relative to the repo root).
Writes  lessons/<id>.html (one self-contained page with the audio inside) and rebuilds index.html (lesson list).
"""
import base64, glob, html, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build(lesson_path):
    lesson = json.load(open(lesson_path, encoding='utf-8'))
    tpl = open(os.path.join(ROOT, 'template', 'practice-template.html'), encoding='utf-8').read()
    audio = open(os.path.join(ROOT, lesson['audio']), 'rb').read()
    data = json.dumps(lesson, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    out = (tpl.replace('/*__TITLE__*/', html.escape(lesson['num']['ko'] + ' · ' + lesson['title']['ko']))
              .replace('/*__LESSON__*/{}', data)
              .replace('/*__AUDIO__*/', 'data:audio/mpeg;base64,' + base64.b64encode(audio).decode())
              .replace('/*__LAME__*/', '../vendor/lame.min.js')
              .replace('/*__INDEX__*/', '../index.html'))
    for ph in ('/*__TITLE__*/', '/*__LESSON__*/', '/*__AUDIO__*/', '/*__LAME__*/', '/*__INDEX__*/'):
        assert ph not in out, ph
    dest = os.path.join(ROOT, 'lessons', lesson['id'] + '.html')
    open(dest, 'w', encoding='utf-8').write(out)
    print('wrote', os.path.relpath(dest, ROOT), len(out) // 1024, 'KB')


def build_index():
    lessons = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(ROOT, 'lessons', '*.json')))]
    # subtitle in the lesson's explanation language (lesson["xl"], default English)
    xl = lambda l, k: l[k].get(l.get('xl', 'en')) or l[k].get('en', '')
    cards = '\n'.join(
        f'<a class="card" href="lessons/{html.escape(l["id"])}.html"><span class="num">{html.escape(l["num"]["ko"])}</span>'
        f'<span class="body"><span class="ko">{html.escape(l["title"]["ko"])}</span>'
        f'<span class="en">{html.escape(xl(l, "num"))} · {html.escape(xl(l, "title"))} · {html.escape(l["level"])}</span></span>'
        f'<span class="go" aria-hidden="true">›</span></a>' for l in lessons)
    page = INDEX.replace('<!--CARDS-->', cards)
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(page)
    print('wrote index.html with', len(lessons), 'lesson(s)')


INDEX = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Korean with Taejeong · 태정쌤 한국어</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;700&family=Noto+Sans+KR:wght@500;700&display=swap" rel="stylesheet">
<style>
:root{color-scheme:light;--bg:#FAF7F2;--card:#fff;--line:#E6DCCF;--ink:#2B2420;--mut:#6B5F56;--at:#B4560F;--bg2:#F2ECE3}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.55 "Atkinson Hyperlegible Next","Noto Sans KR",-apple-system,"Apple SD Gothic Neo",sans-serif}
main{max-width:640px;margin:0 auto;padding:calc(36px + env(safe-area-inset-top)) 20px calc(48px + env(safe-area-inset-bottom))}
.ov{font-size:13px;font-weight:700;color:var(--at)}
h1{font-family:"Noto Sans KR",sans-serif;font-size:clamp(30px,7vw,40px);line-height:1.15;margin:4px 0 8px}
p{color:var(--mut);margin:0 0 26px}
.card{display:flex;align-items:center;gap:16px;padding:16px 18px;background:var(--card);border:1.5px solid var(--line);border-radius:22px;margin-bottom:12px;color:inherit;text-decoration:none}
.num{flex:none;min-width:52px;height:52px;padding:0 8px;border-radius:14px;background:var(--bg2);display:grid;place-items:center;font-family:"Noto Sans KR",sans-serif;font-weight:700;color:var(--at)}
.body{flex:1;min-width:0}
.ko{display:block;font-family:"Noto Sans KR",sans-serif;font-weight:700;font-size:19px}
.en{display:block;font-size:14px;color:var(--mut)}
.go{font-size:28px;color:var(--mut)}
footer{font-size:13px;color:var(--mut);margin-top:26px}
</style>
</head>
<body>
<main>
<div class="ov">Korean with Taejeong · 태정쌤 한국어</div>
<h1>수업 목록<br><span style="font-size:.55em;color:var(--mut);font-weight:500">All lessons</span></h1>
<p>Bookmark this page. Every new lesson appears here.<br>Speichere diese Seite als Lesezeichen. Jede neue Lektion erscheint hier.<br>이 페이지를 즐겨찾기해 두세요. 새 수업이 여기에 추가돼요.</p>
<!--CARDS-->
<footer>Recordings stay on your device. Aufnahmen bleiben auf deinem Gerät. 녹음은 여러분 기기에만 저장돼요.</footer>
</main>
</body>
</html>
'''

if __name__ == '__main__':
    for p in sys.argv[1:]:
        build(p)
    build_index()
