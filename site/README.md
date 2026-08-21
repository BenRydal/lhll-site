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
js/site.js        <site-nav> / <site-footer> + click-to-load video
assets/img/       images the site serves (1x and @2x)
assets/pdf/       the six conference documents
favicon.svg       lens mark; .ico and apple-touch-icon.png are the same artwork
```

That is the whole site. Everything it needs is in this folder.

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

## Shared header and footer

`<site-nav>` and `<site-footer>` are custom elements defined in `js/site.js`,
rendering into light DOM so `site.css` styles them normally. The chrome lives in
one place without a build step or a library.

Tradeoff: the nav is rendered by JavaScript, so it isn't in the raw HTML source.
`sitemap.xml` lists all six URLs so crawlers find every page regardless.

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
