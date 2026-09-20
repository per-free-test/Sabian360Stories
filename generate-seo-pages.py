import json
import re
import urllib.request
from html import escape
from pathlib import Path

# ============================================================
# Sabian 360 Stories - SEO page generator
# ============================================================

API_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbx4Ws1e1JVicBQR7Lfr8v7G0o7yvRBiX1uPZZdXHFr7BhEDcHmXCFYBNt2kkgX62lrVUA/exec"
)

BASE_URL = "https://per-free-test.github.io/Sabian360Stories"

ROOT = Path(__file__).resolve().parent

ZODIAC = {
    "aries":       {"ja": "牡羊座", "en": "Aries"},
    "taurus":      {"ja": "牡牛座", "en": "Taurus"},
    "gemini":      {"ja": "双子座", "en": "Gemini"},
    "cancer":      {"ja": "蟹座",   "en": "Cancer"},
    "leo":         {"ja": "獅子座", "en": "Leo"},
    "virgo":       {"ja": "乙女座", "en": "Virgo"},
    "libra":       {"ja": "天秤座", "en": "Libra"},
    "scorpio":     {"ja": "蠍座",   "en": "Scorpio"},
    "sagittarius": {"ja": "射手座", "en": "Sagittarius"},
    "capricorn":   {"ja": "山羊座", "en": "Capricorn"},
    "aquarius":    {"ja": "水瓶座", "en": "Aquarius"},
    "pisces":      {"ja": "魚座",   "en": "Pisces"},
}


def fetch_stories():
    print("SOAのデータを取得しています...")

    request = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "Sabian360Stories-SEO-Generator/1.0"},
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    if not isinstance(data, list):
        raise ValueError("Apps Scriptから取得したデータが配列ではありません。")

    return data


def story_info(story):
    story_id = str(story.get("id", "")).strip().lower()

    match = re.match(r"([a-z]+)-(\d{1,2})", story_id)

    if not match:
        return None

    sign = match.group(1)
    degree = int(match.group(2))

    if sign not in ZODIAC or not 1 <= degree <= 30:
        return None

    return sign, degree


def paragraphs(text):
    text = str(text or "").replace("\r\n", "\n").replace("\r", "\n")

    blocks = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]

    if not blocks and text.strip():
        blocks = [text.strip()]

    result = []

    for block in blocks:
        result.append(
            "<p>" + escape(block).replace("\n", "<br>") + "</p>"
        )

    return "\n".join(result)


def create_page(story, sign, degree):
    ja_degree = story.get("degreeJa") or f"{ZODIAC[sign]['ja']}{degree:02d}度"
    en_degree = story.get("degreeEn") or f"{ZODIAC[sign]['en']} {degree:02d}°"

    original_ja = str(story.get("originalJa") or "")
    original_en = str(story.get("originalEn") or "")
    story_ja = str(story.get("storyJa") or "")
    story_en = str(story.get("storyEn") or "")
    story_zh = str(story.get("storyZhTw") or "")

    page_url = f"{BASE_URL}/{sign}/{degree:02d}/"
    main_url = f"{BASE_URL}/#{story.get('id', '')}"

    title = f"{ja_degree}｜{original_ja}｜Sabian 360 Stories"

    description_source = re.sub(r"\s+", " ", story_ja).strip()

    if description_source:
        description = description_source[:120]
    else:
        description = f"{ja_degree}のサビアンシンボルを物語として解読します。"

    image_url = f"{BASE_URL}/images/{sign}-{degree:02d}.webp"

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>{escape(title)}</title>

  <meta name="description" content="{escape(description, quote=True)}">
  <link rel="canonical" href="{escape(page_url, quote=True)}">

  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(title, quote=True)}">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:url" content="{escape(page_url, quote=True)}">
  <meta property="og:image" content="{escape(image_url, quote=True)}">

  <style>
    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      color: #302c25;
      background: #f8f3e8;
      font-family:
        "Yu Mincho",
        "Hiragino Mincho ProN",
        "Noto Serif JP",
        "Times New Roman",
        serif;
      line-height: 2;
    }}

    main {{
      width: min(720px, calc(100% - 32px));
      margin: 0 auto;
      padding: 48px 0 80px;
    }}

    .site-name {{
      text-align: center;
      color: #7b6338;
      font-size: 0.9rem;
      letter-spacing: 0.08em;
    }}

    h1 {{
      margin: 24px 0 8px;
      text-align: center;
      color: #7b6338;
      font-size: clamp(1.8rem, 5vw, 2.7rem);
      font-weight: 500;
    }}

    .english-degree {{
      margin: 0 0 32px;
      text-align: center;
      color: #766c5d;
      font-family: Arial, sans-serif;
    }}

    .card-image {{
      display: block;
      width: min(360px, 100%);
      height: auto;
      margin: 0 auto 42px;
      border-radius: 12px;
      box-shadow: 0 14px 32px rgba(40, 32, 20, 0.18);
    }}

    article {{
      padding: clamp(22px, 5vw, 48px);
      border: 1px solid rgba(177, 145, 85, 0.6);
      border-radius: 14px;
      background: #fffdf7;
    }}

    h2 {{
      margin-top: 36px;
      color: #7b6338;
      font-size: 1rem;
      letter-spacing: 0.08em;
    }}

    h2:first-child {{
      margin-top: 0;
    }}

    .original {{
      padding: 16px 20px;
      border-left: 3px solid #b19155;
      background: #f8f3e8;
    }}

    .language-section {{
      margin-top: 48px;
      padding-top: 24px;
      border-top: 1px solid rgba(177, 145, 85, 0.35);
    }}

    .back-link {{
      display: block;
      width: fit-content;
      margin: 40px auto 0;
      padding: 10px 22px;
      border: 1px solid #b19155;
      border-radius: 999px;
      color: #7b6338;
      text-decoration: none;
      background: #fffdf7;
    }}

    footer {{
      margin-top: 48px;
      text-align: center;
      color: #837868;
      font-family: Arial, sans-serif;
      font-size: 0.78rem;
    }}
  </style>
</head>

<body>
  <main>
    <div class="site-name">Sabian 360 Stories</div>

    <h1>{escape(ja_degree)}</h1>
    <p class="english-degree">{escape(en_degree)}</p>

    <img
      class="card-image"
      src="../../images/{sign}-{degree:02d}.webp"
      alt="{escape(ja_degree, quote=True)}"
    >

    <article>
      <h2>原文</h2>
      <div class="original">{paragraphs(original_ja)}</div>

      <h2>解読</h2>
      <div>{paragraphs(story_ja)}</div>

      <section class="language-section" lang="en">
        <h2>Original Text</h2>
        <div class="original">{paragraphs(original_en)}</div>

        <h2>Deciphering</h2>
        <div>{paragraphs(story_en)}</div>
      </section>

      <section class="language-section" lang="zh-Hant">
        <h2>解讀</h2>
        <div>{paragraphs(story_zh)}</div>
      </section>
    </article>

    <a class="back-link" href="{escape(main_url, quote=True)}">
      カードで見る
    </a>

    <footer>
      © Sabian 360 Stories
    </footer>
  </main>
</body>
</html>
"""


def write_sitemap(urls):
    items = "\n".join(
        f"  <url><loc>{escape(url)}</loc></url>"
        for url in urls
    )

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{BASE_URL}/</loc></url>
{items}
</urlset>
"""

    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def main():
    stories = fetch_stories()

    generated = 0
    urls = []

    for story in stories:
        info = story_info(story)

        if not info:
            continue

        sign, degree = info

        # 日本語の解読がまだない度数は検索ページを作らない
        if not str(story.get("storyJa") or "").strip():
            continue

        folder = ROOT / sign / f"{degree:02d}"
        folder.mkdir(parents=True, exist_ok=True)

        html = create_page(story, sign, degree)

        (folder / "index.html").write_text(
            html,
            encoding="utf-8"
        )

        urls.append(f"{BASE_URL}/{sign}/{degree:02d}/")
        generated += 1

    write_sitemap(urls)

    print()
    print(f"完了：{generated}ページを生成しました。")
    print("sitemap.xml も生成しました。")


if __name__ == "__main__":
    main()