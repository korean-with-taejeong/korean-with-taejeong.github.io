# Korean with Taejeong · 태정쌤 한국어

Pronunciation and expression practice apps for Korean learners.
Students open: https://korean-with-taejeong.github.io/

## Structure
- `index.html` — lesson list (generated)
- `lessons/<id>.json` — lesson content: words with timings, pronunciation [ ], tags, segments, parts, notes (explanation language / Korean). `"xl": "de"` = German explanations and German app text; without it, English.
- `lessons/<id>.html` — the app students open (generated, audio inside)
- `audio/<id>.mp3` — model audio from ElevenLabs (eleven_v4, with timestamps)
- `template/practice-template.html` — the app template
- `tools/build.py` — `python3 tools/build.py lessons/<id>.json` builds the lesson page and the index
- `vendor/lame.min.js` — MP3 encoder (LAME, LGPL, lame.sourceforge.net) for phones that can't record m4a
- `test/mic.html` — microphone test page

Recordings stay on the student's device; nothing is uploaded.
