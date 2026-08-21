# Learning How to Look & Listen

The website for a Spencer Foundation conference at Arizona State University,
where nineteen scholars each analysed the same two-minute video of classroom
interaction. Migrated off Squarespace to plain static HTML.

Live at <https://www.learninghowtolookandlisten.com>.

```
site/      the deployed website — plain HTML, one stylesheet, one script
archive/   source material from the Squarespace original; never deployed
```

## Deploying

Vercel is configured with **Root Directory → `site`**. Only that folder is
served; `archive/` rides along in git purely as a backup. There is no build
step, no framework, and no dependencies — Vercel serves `site/` as-is.

Push to `main` and Vercel redeploys.

## Why archive/ is in the repo

`archive/originals/` holds the only copies of the full-resolution images pulled
from the Squarespace CDN, and `archive/raw-html/` is the only record of the
pre-migration site. About 9 MB total. Keeping it in git means it is backed up
instead of living on one laptop, and the Root Directory setting keeps it from
ever being served.

## Working on the site

```bash
cd site
python3 -m http.server 8788    # then open http://localhost:8788
```

The pages are hand-maintained HTML. See `site/README.md` for how the site is put
together, and `archive/README.md` for what the archive contains.

## License

Content is published under
[CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/).
