# Learning How to Look & Listen

Static site: plain HTML, one stylesheet, one small script. No framework, no
build step, no dependencies.

## Deploying

The git repo is the **parent** folder, so `archive/` is backed up too. Only this
folder is deployed.

```bash
cd ..                       # repo root, the folder containing site/ and archive/
git init && git add -A && git commit -m "Initial commit"
git remote add origin git@github.com:<you>/<repo>.git
git push -u origin main
```

Then import the repo on Vercel and set **Root Directory → `site`**. Framework
preset "Other", no build command, no output directory — Vercel serves it as-is.
That Root Directory setting is what keeps `archive/` out of the deploy; without
it Vercel would serve the repo root and the site would 404.

`vercel.json` sets `cleanUrls: true`, so `individualsessions.html` is served at
`/individualsessions`. That keeps the original URLs working, which matters
because this site is cited in the literature.

To preview locally:

```bash
python3 -m http.server 8788
```

## Layout

```
*.html            the six pages
css/site.css      every design decision
js/site.js        click-to-load video, and nothing else
assets/img/       images the site serves (1x and @2x)
assets/pdf/       the six conference documents
assets/fonts/     the three typefaces, self-hosted, plus their licenses
favicon.svg       lens mark; .ico and apple-touch-icon.png are the same artwork
```

That is the whole site. Everything it needs is in this folder — it makes no
third-party request at all, and nothing outside this folder is fetched at
runtime until a reader chooses to play a video.

## Editing

The pages are ordinary HTML — open one and edit it. Nothing is compiled and
nothing regenerates behind your back.

Each `<head>` carries a `<link rel="canonical">` and a block of Open Graph tags
whose URLs are absolute, pointing at `www.learninghowtolookandlisten.com`. If the
production domain ever changes, those are the strings to update — they are the
only place the domain is hardcoded in the HTML (it also appears in `robots.txt`
and `sitemap.xml`).

`archive/tools/build.py` originally generated these pages. It has since drifted
from them and now refuses to overwrite `site/` unless forced. Edit the HTML here;
don't regenerate.

## Header and footer

Both are plain HTML, repeated in all six pages. They were custom elements
rendered by `js/site.js` until it became clear what that cost: if the script
failed to load, a reader got a page with no navigation and no license notice —
no way out of the page they landed on. The chrome is the one part a reader
cannot do without, so it does not depend on JavaScript.

The duplication is real: editing the nav means editing six files. Two things
keep that honest — the nav has been stable for the life of the site, and the
current page is marked with `aria-current="page"` on its own link, so each
page's copy differs by exactly one attribute. If you add or rename a page,
grep for `class="nav"` and update all six.

## Fonts

Newsreader, IBM Plex Sans and IBM Plex Mono are served from `assets/fonts/`.
They are the same woff2 files Google was serving — pulled from its API and
committed — so the rendering did not change, but no request now leaves the
site. The old shared-CDN-cache argument for using Google's copy has not
applied since 2020, when browsers partitioned the HTTP cache by site.

Each family ships `latin` and `latin-ext` faces with `unicode-range`
descriptors, so `latin-ext` is fetched only if a character in that range
appears. Nothing on the site uses one today; the files are there so a
bibliography entry with an unusual name renders correctly rather than
silently dropping to Georgia.

Two faces are preloaded in each `<head>` — the body sans and the display
roman, the ones needed for first paint. `crossorigin` on those `<link>`s is
required even though the files are same-origin: fonts are always fetched in
CORS mode, and without it the browser downloads them twice.

Both families are SIL OFL 1.1, which permits this but requires the license
travel with the files: `assets/fonts/OFL-Newsreader.txt` and `OFL-IBMPlex.txt`.

`/assets/fonts/` is cached for a year as `immutable`. If you ever replace a
font file, **rename it** and update `css/site.css` — a same-named replacement
would never reach anyone who has already visited.

## Video

The 34 talks stay on YouTube. Each card is a local still with a play button; the
player iframe is only created on click, from `youtube-nocookie.com`. A page with
19 videos loads its own weight instead of 19 embedded players, and no YouTube
cookie is set unless someone chooses to watch.

## Images

Served at quality 88 in two widths (`name.jpg`, `name@2x.jpg`) so retina
displays get real detail. Nothing is upscaled.

The 19 individual-session stills come from ~1083px sources and serve at full
detail. The 14 presentation thumbnails come from 480px sources — YouTube's
default thumbnail size — which is their ceiling. Replacing them means capturing
new stills from the source videos.

## Known content gap

The Future Directions page on the original site had a fourth heading,
"Looking & Listening", with no text under it. It is omitted here rather than
rendered as an empty section.

## License

Content is published under
[CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/).
