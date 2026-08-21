#!/usr/bin/env python3
"""Generate the six static pages.

Run once (or after editing content); it writes plain .html files you
own and can hand-edit afterwards. There is no runtime build step —
this exists only so 33 near-identical video cards and a 90-entry
bibliography aren't transcribed by hand.

    python3 tools/build.py
"""
import os, re, sys, html

sys.path.insert(0, os.path.dirname(__file__))
from content import SESSIONS, PRESENTATIONS, GROUP_VIDEO, slug

# This script lives in archive/tools/ and writes into site/.
# Nothing it produces refers back to the archive.
ARCHIVE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(os.path.dirname(ARCHIVE), "site")
EXTRACT = os.path.join(ARCHIVE, "extract")

PDFS = {
    "ConferenceOverview": ("Conference Overview", "PDF · 2 pp"),
    "conferenceDescription": ("Conference Proposal", "PDF · 8 pp"),
    "ConferenceParticipants": ("Conference Participants", "PDF · 5 pp"),
    "creativeCommonsInfo": ("License Information", "PDF · 1 p"),
    "videoTranscript": ("Transcript of the classroom video", "PDF · 2 pp"),
    "groupSessionCommentary": ("Commentary on the group session", "PDF · 3 pp"),
}

PLAY_SVG = (
    '<span class="facade__play" aria-hidden="true">'
    '<svg viewBox="0 0 68 48" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M66.5 7.7a8.6 8.6 0 0 0-6-6C55.2 0 34 0 34 0S12.8 0 7.5 1.6a8.6 8.6 0 0 0-6 6'
    'A89.6 89.6 0 0 0 0 24a89.6 89.6 0 0 0 1.5 16.3 8.6 8.6 0 0 0 6 6C12.8 48 34 48 34 48'
    's21.2 0 26.5-1.7a8.6 8.6 0 0 0 6-6A89.6 89.6 0 0 0 68 24a89.6 89.6 0 0 0-1.5-16.3z" '
    'fill="#14181c" fill-opacity=".78"/>'
    '<path d="M27 34V14l18 10z" fill="#fff"/></svg></span>'
)


def e(s):
    return html.escape(s, quote=True)


def jpeg_size(path):
    """Read width/height from a baseline JPEG's SOF marker."""
    with open(path, "rb") as f:
        if f.read(2) != b"\xff\xd8":
            return None
        while True:
            b = f.read(1)
            if not b:
                return None
            if b != b"\xff":
                continue
            marker = f.read(1)
            while marker == b"\xff":
                marker = f.read(1)
            if marker in (b"\xc0", b"\xc1", b"\xc2", b"\xc3"):
                f.read(3)
                h = int.from_bytes(f.read(2), "big")
                w = int.from_bytes(f.read(2), "big")
                return w, h
            seg = int.from_bytes(f.read(2), "big")
            if seg < 2:
                return None
            f.seek(seg - 2, 1)


def dims(img):
    size = jpeg_size(os.path.join(ROOT, "assets", "img", img + ".jpg"))
    return size or (700, 394)


CARD_SIZES = "(min-width: 1240px) 390px, (min-width: 700px) 33vw, 100vw"
FEATURE_SIZES = "(min-width: 1100px) 990px, 100vw"
HERO_SIZES = "(min-width: 1240px) 1144px, 100vw"


def srcset(img):
    """Emit a srcset only when a real 2x file exists — several source
    thumbnails are 480px originals with nothing larger to offer."""
    base = dims(img)[0]
    retina = os.path.join(ROOT, "assets", "img", img + "@2x.jpg")
    if not os.path.exists(retina):
        return ""
    rw = jpeg_size(retina)[0]
    return (f' srcset="assets/img/{img}.jpg {base}w, '
            f'assets/img/{img}@2x.jpg {rw}w"')


def facade(vid, img, title, extra_class="", loading="lazy", sizes=CARD_SIZES):
    w, h = dims(img)
    return (
        f'<button class="facade{extra_class}" type="button" data-video="{e(vid)}" '
        f'data-title="{e(title)}" aria-label="Play video: {e(title)}">'
        f'<img src="assets/img/{img}.jpg"{srcset(img)} sizes="{sizes}" alt="" '
        f'width="{w}" height="{h}" loading="{loading}" decoding="async">'
        f'{PLAY_SVG}</button>'
    )


def viewing(vid, img, name, meta, kind="", feature=False, loading="lazy"):
    classes = " viewing"
    if kind == "source":
        classes += " viewing--source"
    if feature:
        classes += " viewing--feature"
    return (
        f'<li class="{classes.strip()}">'
        f'{facade(vid, img, name, "", loading, FEATURE_SIZES if feature else CARD_SIZES)}'
        f'<h3 class="viewing__name">{e(name)}</h3>'
        f'<p class="viewing__meta">{meta}</p></li>'
    )


def doc_link(key):
    label, meta = PDFS[key]
    return (f'<li><a href="assets/pdf/{key}.pdf">'
            f'<span class="doc__name">{e(label)}</span>'
            f'<span class="doc__meta">{meta}</span></a></li>')


SITE = "https://www.learninghowtolookandlisten.com"
OG_IMAGE = f"{SITE}/assets/img/cover-scholars-viewing@2x.jpg"


def shell(title, desc, body, page_class="", slug="/"):
    cls = f' class="{page_class}"' if page_class else ""
    url = SITE + slug
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Learning How to Look &amp; Listen">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="2400">
<meta property="og:image:height" content="1444">
<meta property="og:image:alt" content="Scholars seated around a table viewing classroom video together.">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="css/site.css">
<script src="js/site.js" defer></script>
</head>
<body{cls}>
<a class="skip" href="#main">Skip to content</a>
<site-nav></site-nav>
<main id="main">
{body}
</main>
<site-footer></site-footer>
</body>
</html>
"""


# ---------------------------------------------------------------- pages

def page_index():
    cw, ch = dims("cover-scholars-viewing")
    cover = ('<figure class="hero__figure">'
             f'<img src="assets/img/cover-scholars-viewing.jpg"'
             f'{srcset("cover-scholars-viewing")} sizes="{HERO_SIZES}" '
             f'width="{cw}" height="{ch}" '
             'alt="Conference participants seated at laptops, each conducting an individual '
             'analysis of the same two-minute classroom video." fetchpriority="high" '
             'decoding="async">'
             '<figcaption>Participants conducting individual analysis of the same '
             'two-minute video of classroom interaction.</figcaption></figure>')

    tally = """<ul class="tally">
<li><b>19</b><span>Individual viewings</span></li>
<li><b>14</b><span>Presentations</span></li>
<li><b>1</b><span>Group session</span></li>
<li><b>2:00</b><span>The shared clip</span></li>
</ul>"""

    sections = """<div class="index">
<a class="index__item" href="individualsessions.html">
  <span class="index__count">19 recordings</span>
  <h3>Individual Viewing Sessions</h3>
  <p>Each participant thinks out loud while watching the same two-minute clip, showing their own approach to video analysis.</p>
</a>
<a class="index__item" href="groupsession.html">
  <span class="index__count">1 recording</span>
  <h3>Group Viewing Session</h3>
  <p>All participants view and discuss the same clip together, in a collaborative interaction analysis.</p>
</a>
<a class="index__item" href="presentations.html">
  <span class="index__count">14 recordings</span>
  <h3>Presentations</h3>
  <p>Scholars describe how video-based analysis has shaped their past and current research.</p>
</a>
<a class="index__item" href="futuredirections.html">
  <span class="index__count">3 themes</span>
  <h3>Future Directions</h3>
  <p>Key issues, needs and next steps for video analysis in education and the social sciences.</p>
</a>
</div>"""

    body = f"""<section class="wrap hero">
  <p class="label">Spencer Foundation &middot; Arizona State University</p>
  <h1 class="hero__title">Learning How to Look &amp; Listen</h1>
  <p class="hero__sub">Building capacity for video-based social &amp; educational research</p>
  {cover}
  {tally}
</section>

<section class="wrap section">
  <div class="prose">
    <p class="lede">Nineteen scholars watched the same two minutes of classroom
    video. This archive collects what each of them saw and heard.</p>
    <p>This website brings together resources from a conference supported by the
    Spencer Foundation at Arizona State University, where an interdisciplinary
    group of older and younger scholars gathered to document and illustrate the
    basic patterns of visual and auditory attention employed by researchers who
    use video to study social interaction.</p>
    <p>The shared clip shows the teaching of a key idea in the physics of
    matter&mdash;that matter occupies space&mdash;in a bilingual
    kindergarten&ndash;first grade classroom.</p>
  </div>
</section>

<section class="wrap section--tight">
{sections}
</section>

<section class="wrap section">
  <div class="section__head">
    <p class="label">Start here</p>
    <h2>Conference documents</h2>
    <div class="prose"><p>In the group viewing session, conference organizer
    Frederick Erickson introduces the purposes and goals of this work.</p></div>
  </div>
  <ul class="docs">
    {doc_link("ConferenceOverview")}
    {doc_link("conferenceDescription")}
    {doc_link("ConferenceParticipants")}
    {doc_link("creativeCommonsInfo")}
  </ul>
</section>

<section class="wrap section">
  <div class="prose">
    <p>With thanks to the Spencer Foundation for their generous support of this
    work, and to Arizona State University for hosting the conference.</p>
    <p class="label signoff">Frederick Erickson, Sherman Dorn &amp; Alfredo Artiles</p>
  </div>
</section>"""
    return shell(
        "Learning How to Look & Listen",
        "An archive of video-based interaction analysis: 19 scholars analysing the "
        "same two-minute classroom clip, from a Spencer Foundation conference at "
        "Arizona State University.",
        body, slug="/")


def page_sessions():
    source = SESSIONS[0]
    rest = SESSIONS[1:]
    cards = [viewing(source[0], "session-" + slug(source[2]),
                     "The “matter occupies space” video",
                     "The clip every session refers to &middot; 2:00",
                     kind="source", feature=True, loading="eager")]
    for i, (vid, _img, cap, kind) in enumerate(rest):
        cards.append(viewing(vid, "session-" + slug(cap), cap,
                             "Individual viewing",
                             loading="eager" if i < 3 else "lazy"))

    body = f"""<section class="wrap section">
  <div class="section__head">
    <p class="label">19 recordings</p>
    <h1>Individual Viewing Sessions</h1>
    <div class="prose">
      <p class="lede">Each participant was invited to analyse the same
      two-minute clip by &ldquo;thinking out loud&rdquo; while watching it.</p>
      <p>In each half-hour recording below, a participant illustrates their own
      personal and diverse approach to video analysis of the &ldquo;matter
      occupies space&rdquo; clip, which is included separately as the first
      video. A transcript of the sequence, created by Sarah Diaz and used by
      participants during analysis, is available below.</p>
    </div>
  </div>
  <ul class="docs docs--after">
    {doc_link("videoTranscript")}
  </ul>
  <ul class="sheet">
    {"".join(cards)}
  </ul>
</section>"""
    return shell(
        "Individual Viewing Sessions — Learning How to Look & Listen",
        "Nineteen recordings of scholars thinking out loud while analysing the same "
        "two-minute video of classroom interaction.",
        body, slug="/individualsessions")


def page_group():
    card = viewing(GROUP_VIDEO, "cover-scholars-viewing",
                   "Group interaction analysis session",
                   "Group discussion &middot; analysis begins at 15:03",
                   feature=True, loading="eager")
    body = f"""<section class="wrap section">
  <div class="section__head">
    <p class="label">1 recording</p>
    <h1>Group Viewing Session</h1>
    <div class="prose">
      <p class="lede">The same clip, watched and discussed together.</p>
      <p>Following a brief introduction by Frederick Erickson that includes a
      moment of silence for the late Brigitte &ldquo;Gitti&rdquo; Jordan, the
      recording below shows researchers conducting group interaction analysis of
      the two-minute classroom video. The analysis begins at 15:03. This is the
      same clip participants used in their individual sessions.</p>
    </div>
  </div>
  <ul class="sheet">{card}</ul>
  <ul class="docs docs--after">
    {doc_link("groupSessionCommentary")}
  </ul>
</section>"""
    return shell(
        "Group Viewing Session — Learning How to Look & Listen",
        "Researchers conduct a collaborative interaction analysis of the same "
        "two-minute classroom video.",
        body, slug="/groupsession")


def page_presentations():
    cards = [viewing(vid, "talk-" + slug(cap), cap, "Presentation",
                     loading="eager" if i < 4 else "lazy")
             for i, (vid, _img, cap, _k) in enumerate(PRESENTATIONS)]
    body = f"""<section class="wrap section">
  <div class="section__head">
    <p class="label">14 recordings</p>
    <h1>Presentations</h1>
    <div class="prose">
      <p class="lede">How each scholar has used video analysis in their own
      research.</p>
      <p>Together these talks illustrate a diverse set of historical,
      contemporary and interdisciplinary approaches to video-based analysis,
      supporting an equally diverse set of research questions from different
      philosophical orientations.</p>
    </div>
  </div>
  <ul class="sheet">
    {"".join(cards)}
  </ul>
</section>"""
    return shell(
        "Presentations — Learning How to Look & Listen",
        "Fourteen scholars describe how video-based analysis has shaped their past "
        "and current research.",
        body, slug="/presentations")


def page_future():
    """Themes are parsed from the scrape so the wording stays faithful."""
    src = open(os.path.join(EXTRACT, "futuredirections.txt"),
               encoding="utf-8").read()
    blocks = re.split(r"## H2: ", src)[1:]
    themes = []
    for b in blocks:
        lines = [l.strip() for l in b.strip().split("\n") if l.strip()]
        if not lines:
            continue
        heading = lines[0]
        paras = [l for l in lines[1:] if not l.startswith("Supported by")]
        if not paras:
            continue  # "Looking & Listening" is an empty heading on the live site
        ps = "".join(f"<p>{e(p)}</p>" for p in paras)
        themes.append(f'<section class="theme"><h2>{e(heading)}</h2>'
                      f'<div class="prose">{ps}</div></section>')

    body = f"""<section class="wrap section">
  <div class="section__head">
    <h1>Future Directions</h1>
    <div class="prose">
      <p class="lede">Where video analysis in education and the social sciences
      goes next.</p>
      <p>The themes below are drawn from a concluding discussion about central
      topics raised across the conference, and about potential next steps for
      video analysis in education and the social sciences.</p>
    </div>
  </div>
  {"".join(themes)}
</section>"""
    return shell(
        "Future Directions — Learning How to Look & Listen",
        "Themes and next steps for video analysis in education and the social "
        "sciences, drawn from the conference's concluding discussion.",
        body, slug="/futuredirections")


def page_publications():
    """Bibliography parsed from the scrape into a real chronology."""
    src = open(os.path.join(EXTRACT, "publications.txt"),
               encoding="utf-8").read()
    entries = []
    for line in src.split("\n"):
        line = line.strip()
        m = re.match(r"^(\d{4}):\s*(.+)$", line)
        if m:
            entries.append((m.group(1), m.group(2).strip()))

    rows = "".join(
        f'<div class="chron__entry"><div class="chron__year">{y}</div>'
        f'<div class="chron__cite">{e(c)}</div></div>'
        for y, c in entries)

    span = f"{entries[0][0]}&ndash;{max(y for y, _ in entries)}" if entries else ""
    body = f"""<section class="wrap section">
  <div class="section__head">
    <p class="label">{len(entries)} entries &middot; {span}</p>
    <h1>A History of Interaction Analysis</h1>
    <div class="prose">
      <p class="lede">A chronology of the work this field is built on, from the
      1955 Natural History of an Interview working group to the present.</p>
    </div>
  </div>
  <div class="chron">{rows}</div>
</section>"""
    return shell(
        "A History of Interaction Analysis — Learning How to Look & Listen",
        "A chronological bibliography of interaction analysis, from the 1955 "
        "Natural History of an Interview working group to the present.",
        body, slug="/publications")


def main():
    pages = {
        "index.html": page_index(),
        "individualsessions.html": page_sessions(),
        "groupsession.html": page_group(),
        "presentations.html": page_presentations(),
        "futuredirections.html": page_future(),
        "publications.html": page_publications(),
    }

    # site/ is the source of truth now, not this generator. Pages here have
    # been hand-edited since the last run (the index lede was rewritten, the
    # group session still was swapped), and this script does not know about
    # those edits — running it unguarded silently reverts them. Refuse to
    # overwrite anything that already exists unless asked explicitly.
    force = "--force" in sys.argv
    existing = [n for n in pages if os.path.exists(os.path.join(ROOT, n))]
    if existing and not force:
        print("Refusing to overwrite hand-edited pages in site/:")
        for n in existing:
            print(f"  {n}")
        print("\nsite/ is maintained by hand. This generator is kept for "
              "provenance and for regenerating the long, repetitive pages "
              "(individualsessions, presentations, publications) from scratch.")
        print("If you really mean to regenerate, back up site/ first, then:")
        print("  python3 tools/build.py --force")
        return 1

    for name, content in pages.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{name:28} {len(content):>7,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
