#!/usr/bin/env python3
"""Asset prep: rename scraped CDN images to semantic slugs and emit two
web sizes each, using macOS `sips`.

Rules:
  * Never upscale. An original narrower than the target is emitted at its
    own width — upscaling only adds bytes and blur.
  * Quality 88, high enough that these read as source stills rather than
    compressed thumbnails.
  * Two widths per image (1x / 2x) so retina displays get real detail
    without forcing that weight on everyone.

Originals stay untouched in assets/images/.

    python3 tools/prep_images.py
"""
import os, subprocess, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
from content import SESSIONS, PRESENTATIONS, COVER, slug

# Reads the untouched originals in archive/originals/, writes web images
# into site/assets/img/. The originals are never modified.
ARCHIVE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ARCHIVE, "originals")
OUT = os.path.join(os.path.dirname(ARCHIVE), "site", "assets", "img")
QUALITY = "88"

# (base width, retina width) per role
CARD = (800, 1600)
HERO = (1600, 2400)

os.makedirs(OUT, exist_ok=True)


def real_ext(path):
    with open(path, "rb") as f:
        head = f.read(16)
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    if head[:3] == b"\xff\xd8\xff":
        return "jpg"
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    return "bin"


def width_of(path):
    out = subprocess.run(["sips", "-g", "pixelWidth", path],
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        if "pixelWidth" in line:
            return int(line.split(":")[1])
    return 0


def convert(src, dest, width):
    subprocess.run(
        ["sips", "-s", "format", "jpeg", "-s", "formatOptions", QUALITY,
         "-Z", str(width), src, "--out", dest],
        check=True, capture_output=True)


def main():
    jobs = [(COVER, "cover-scholars-viewing", HERO)]
    for _vid, img, cap, _kind in SESSIONS:
        jobs.append((img, "session-" + slug(cap), CARD))
    for _vid, img, cap, _kind in PRESENTATIONS:
        jobs.append((img, "talk-" + slug(cap), CARD))

    seen, total = set(), 0
    for fname, name, (w1, w2) in jobs:
        src = os.path.join(SRC, fname)
        if not os.path.exists(src):
            print("MISSING", src); continue
        if name in seen:
            print("DUPLICATE SLUG", name); continue
        seen.add(name)

        tmp = src
        if real_ext(src) == "webp":
            tmp = os.path.join(OUT, "_tmp.webp")
            shutil.copy(src, tmp)

        try:
            ow = width_of(tmp)
            # never upscale
            base = min(w1, ow) if ow else w1
            retina = min(w2, ow) if ow else w2

            convert(tmp, os.path.join(OUT, name + ".jpg"), base)
            note = f"{ow}px -> {base}px"

            if retina > base:
                convert(tmp, os.path.join(OUT, name + "@2x.jpg"), retina)
                note += f" + {retina}px @2x"
            else:
                # original too small to justify a 2x file; drop a stale one
                stale = os.path.join(OUT, name + "@2x.jpg")
                if os.path.exists(stale):
                    os.remove(stale)
                note += "  (no 2x — original too small)"

            total += 1
            print(f"{name:<44} {note}")
        except subprocess.CalledProcessError as e:
            print("FAIL", fname, e.stderr.decode()[:200])
        finally:
            if tmp != src and os.path.exists(tmp):
                os.remove(tmp)

    print(f"\n{total} images prepared at quality {QUALITY}")


if __name__ == "__main__":
    main()
