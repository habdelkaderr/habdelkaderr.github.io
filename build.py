"""Builds the portfolio's static pages.

    python build.py            writes index.html and about/ work/ experience/ skills/ contact/
    python -m http.server      then open http://localhost:8000

Sources live in src/: page bodies in src/pages, shared fragments in src/parts,
and the signature (traced outline + one centre line per stroke) in src/sig_*.
Generated pages are committed, because GitHub Pages serves the repo as-is.
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
FILL = (SRC / "sig_fill.txt").read_text().strip()
LINES = json.loads((SRC / "sig_lines.json").read_text())

# Pen order, which is also the reading and tab order of the site.
SECTIONS = [
    # stroke,   slug,         label,        why that stroke
    ("stem",     "about",      "About"),       # the "I" of the signature
    ("loop",     "work",       "Work"),        # the loop holds the projects
    ("leg",      "experience", "Experience"),  # the long line down through time
    ("accent",   "skills",     "Skills"),      # small, sharp, precise
    ("flourish", "contact",    "Contact"),     # the stroke that reaches out to you
]
DRAW_ORDER = ["stem", "loop", "leg", "a", "accent", "flourish"]
# start and duration (seconds) of each stroke when the signature writes itself
TIMING = {"stem": (0.15, 0.32), "loop": (0.42, 0.62), "leg": (1.0, 0.3),
          "a": (1.24, 0.3), "accent": (1.48, 0.2), "flourish": (1.62, 0.42)}
# where each label sits around the signature, as % of its box
LABEL_POS = {"stem": (50.5, 1.5), "loop": (1.5, 49), "leg": (41.5, 92),
             "accent": (72.5, 10), "flourish": (97.5, 68)}

VIEWBOX = "0 20 1440 830"
PEN = 46  # width of the centre line that reveals each stroke


def signature(mode, active=None):
    """mode: 'index' (home: animated, clickable), 'mini' (header mark),
    'flourish' (contact underline: only the last stroke)."""
    p = {"index": "i", "mini": "m", "flourish": "f"}[mode]
    keys = ["flourish"] if mode == "flourish" else DRAW_ORDER
    vb = "1000 462 420 40" if mode == "flourish" else VIEWBOX
    defs = [
        f'<linearGradient id="{p}g" x1="0" y1="0" x2="1440" y2="840" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#ffffff"/><stop offset=".42" stop-color="#b4b4bc"/>'
        '<stop offset=".68" stop-color="#f4f4f6"/><stop offset="1" stop-color="#8a8a93"/></linearGradient>',
        f'<path id="{p}f" d="{FILL}"/>',
    ]
    groups = []
    for k in keys:
        start, dur = TIMING[k]
        defs.append(
            f'<mask id="{p}m-{k}" maskUnits="userSpaceOnUse" x="0" y="0" width="1440" height="860">'
            f'<path class="ink" d="{LINES[k]}" pathLength="1" style="--d:{start}s;--t:{dur}s"/></mask>')
        cls = "sk" + (" on" if k == active else "")
        groups.append(f'<g class="{cls}" data-k="{k}" mask="url(#{p}m-{k})"><use href="#{p}f" fill="url(#{p}g)"/></g>')
    if mode == "index":
        # wide invisible copies of each centre line, so a stroke is easy to hit
        for k, slug, label in SECTIONS:
            groups.append(f'<a class="hit" data-k="{k}" href="/{slug}/" tabindex="-1">'
                          f'<path d="{LINES[k]}"/></a>')
    return (f'<svg class="sig sig-{mode}" viewBox="{vb}" aria-hidden="true" focusable="false">'
            f'<defs>{"".join(defs)}</defs>{"".join(groups)}</svg>')


def index_labels():
    out = []
    for i, (k, slug, label) in enumerate(SECTIONS, 1):
        x, y = LABEL_POS[k]
        side = "right" if x > 90 else "left"
        out.append(f'<a class="lbl lbl-{side}" data-k="{k}" href="/{slug}/" style="--x:{x}%;--y:{y}%">'
                   f'<span class="n">0{i}</span>{label}</a>')
    return "\n      ".join(out)


def head(title, desc):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="https://habdelkaderr.github.io/assets/og.png?v=3">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Hatem Abdelkader's HA signature, with the line: I build websites people enjoy using, and hackers don't.">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#0b0b0d">
  <meta name="color-scheme" content="dark">
  <link rel="icon" href="/assets/favicon.ico" sizes="any">
  <link rel="icon" href="/assets/favicon-64.png" type="image/png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/site.css">
  <script>try{{if(sessionStorage.getItem('signed'))document.documentElement.classList.add('signed')}}catch(e){{}}</script>
  <script type="module" src="/assets/site.js"></script>
</head>"""


def footer():
    return f"""<footer class="foot wrap">
  <span>© {date.today().year} Hatem Abdelkader</span>
  <span><a href="mailto:habdelkader676@gmail.com">habdelkader676@gmail.com</a> · <a href="https://www.linkedin.com/in/hatem-abdelkader" target="_blank" rel="noopener">LinkedIn</a> · <a href="https://github.com/habdelkaderr" target="_blank" rel="noopener">GitHub</a></span>
</footer>"""


def read_page(name):
    """A page source starts with <!--key: value--> lines, then its body."""
    text = (SRC / "pages" / f"{name}.html").read_text(encoding="utf-8")
    meta = dict(re.findall(r"<!--(\w+):\s*(.*?)-->", text.split("\n\n", 1)[0]))
    body = text.split("\n\n", 1)[1]
    body = re.sub(r"\{\{part:(\w+)\}\}",
                  lambda m: (SRC / "parts" / f"{m.group(1)}.html").read_text(encoding="utf-8"), body)
    body = body.replace("{{sig:flourish}}", signature("flourish"))
    body = body.replace('src="assets/', 'src="/assets/')
    return meta, body


def build_home():
    meta, body = read_page("home")
    body = body.replace("{{sig:index}}", signature("index")).replace("{{labels}}", index_labels())
    return f"""{head(meta['title'], meta['desc'])}
<body class="home">
<a class="skip" href="#main">Skip to content</a>
{body}
{footer()}
</body>
</html>
"""


def build_inner(n, key, slug, label):
    meta, body = read_page(slug)
    links = "".join(
        f'<a href="/{s}/"{" aria-current=page" if s == slug else ""}>{l}</a>' for _, s, l in SECTIONS)
    nxt = SECTIONS[n % len(SECTIONS)]
    next_link = (f'<a href="/{nxt[1]}/">{nxt[2]} <span aria-hidden="true">→</span></a>'
                 if n < len(SECTIONS) else '<a href="/">Back to the signature <span aria-hidden="true">↺</span></a>')
    return f"""{head(meta['title'], meta['desc'])}
<body class="inner" data-page="{key}">
<a class="skip" href="#main">Skip to content</a>
<header class="topbar wrap">
  <a class="mini" href="/" aria-label="Hatem Abdelkader: back to the signature index">{signature('mini', key)}</a>
  <nav class="toplinks" aria-label="Main">{links}</nav>
  <a class="btn btn-sm bar-cta" href="/contact/">Contact</a>
</header>
<main id="main" class="wrap page">
  <p class="kicker"><span class="n">0{n}</span>{label}</p>
  <h1>{meta['h1']}</h1>
  <div class="rule" aria-hidden="true"></div>
{body}
  <nav class="next" aria-label="Next section">Up next: {next_link}</nav>
</main>
{footer()}
</body>
</html>
"""


def main():
    css = "".join((SRC / f).read_text(encoding="utf-8") for f in ("site-head.css", "site-cases.css"))
    (ROOT / "assets" / "site.css").write_text(css, encoding="utf-8")
    (ROOT / "index.html").write_text(build_home(), encoding="utf-8")
    for n, (key, slug, label) in enumerate(SECTIONS, 1):
        out = ROOT / slug / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(build_inner(n, key, slug, label), encoding="utf-8")
    print("built: / " + " ".join(f"/{s}/" for _, s, _ in SECTIONS))


if __name__ == "__main__":
    main()
