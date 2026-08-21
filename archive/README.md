# Archive — version controlled, never deployed

Source material from the Squarespace version of learninghowtolookandlisten.com.
This folder is committed to GitHub so it is backed up, but it is excluded from
the deploy: Vercel's Root Directory is set to `site/`, so nothing here is ever
served. Nothing in `site/` depends on it at runtime.

```
originals/    full-resolution images pulled from the Squarespace CDN (34 files)
raw-html/     the six scraped Squarespace pages, exactly as served
extract/      text pulled out of the scrape; build.py reads two of these
tools/        the generators
```

## Why keep it

`originals/` is the only copy of the full-resolution images. `raw-html/` is the
only record of the pre-migration site. If you ever need a larger image or want
to check wording against the original, it is here.

It is roughly 9 MB, almost all of it `originals/`. That is small enough to live
in git comfortably, and it means the only copy of the full-resolution images is
backed up rather than sitting on one laptop.

## Tools

Both write into `../site/` and never modify anything in this folder.

```bash
python3 tools/prep_images.py   # originals/ -> site/assets/img/
python3 tools/build.py         # regenerates the six .html files in site/
```

`tools/content.py` holds the mapping of each YouTube video ID to its analyst and
thumbnail, verified against document order in the original HTML. That mapping is
the one thing here that would be tedious to reconstruct.

`build.py` would overwrite the six `.html` files in `site/`, so it now refuses
to run when those files already exist and prints what it would have clobbered.
`--force` overrides that; back up `site/` first if you use it.

Its content has drifted from the live pages, which is exactly why the guard is
there: `site/` has since been hand-edited (the index lede was rewritten, the
group session still was swapped, and every page gained canonical/Open Graph
tags), and the generator does not know about any of it. Treat `site/` as the
source of truth and this script as provenance. The generator exists because 34
near-identical video cards and an 89-entry bibliography were not worth typing by
hand, not because the site needs a build step.

The drift has since widened, and the markup it emits is now simply wrong for
the current site. `build.py` still writes an inline play-button SVG into every
card (drawn in CSS now), `<site-nav>`/`<site-footer>` custom elements (plain
HTML now), and a Google Fonts `<link>` (self-hosted now). Do not run it with
`--force` expecting a usable site; read it for the content mapping only.
