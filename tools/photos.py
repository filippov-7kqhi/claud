# -*- coding: utf-8 -*-
"""Fit supplied product photographs to the gallery's 1200x760 frame.

A studio shot on a plain ground is trimmed to the machine and then padded back
out in that same ground colour, so it fills the frame without a visible seam.
A photograph with no uniform border -- anything shot on site -- is centre
cropped instead, because padding one would band it with a colour that is not
in the picture.
"""
import os, sys
from PIL import Image, ImageChops

W, H = 1200, 760


def border_colour(im, n=6):
    """The median colour of the outer n pixels, or None if they are not uniform."""
    px = []
    w, h = im.size
    for x in range(0, w, 7):
        px += [im.getpixel((x, y)) for y in (0, n, h - 1 - n, h - 1)]
    for y in range(0, h, 7):
        px += [im.getpixel((x, y)) for x in (0, n, w - 1 - n, w - 1)]
    med = tuple(sorted(c[i] for c in px)[len(px) // 2] for i in range(3))
    spread = max(max(abs(c[i] - med[i]) for i in range(3)) for c in px)
    return med if spread <= 26 else None


def fit(path, out, quality=88, anchor=0.5):
    im = Image.open(path).convert("RGB")
    bg = border_colour(im)

    if bg:
        # trim the plain margin back to the machine, keeping a little air
        diff = ImageChops.difference(im, Image.new("RGB", im.size, bg)).convert("L")
        box = diff.point(lambda v: 255 if v > 22 else 0).getbbox()
        if box:
            pad = int(min(im.size) * 0.035)
            im = im.crop((max(0, box[0] - pad), max(0, box[1] - pad),
                          min(im.size[0], box[2] + pad), min(im.size[1], box[3] + pad)))
        k = min(W / im.size[0], H / im.size[1])
        im = im.resize((max(1, int(im.size[0] * k)), max(1, int(im.size[1] * k))), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), bg)
        canvas.paste(im, ((W - im.size[0]) // 2, (H - im.size[1]) // 2))
    else:
        k = max(W / im.size[0], H / im.size[1])
        im = im.resize((int(im.size[0] * k), int(im.size[1] * k)), Image.LANCZOS)
        x = (im.size[0] - W) // 2
        y = int((im.size[1] - H) * anchor)
        canvas = im.crop((x, y, x + W, y + H))

    os.makedirs(os.path.dirname(out), exist_ok=True)
    canvas.save(out, "JPEG", quality=quality, optimize=True, progressive=True)
    return "padded" if bg else "cropped"


# Shots whose subject sits at the very bottom of the frame -- a dimension arrow
# drawn on the ground -- and would be cropped away by a centred crop.
ANCHOR_BOTTOM = ("rear-view-width", "narrow-access-width", "width")


def run(src, dst):
    for f in sorted(os.listdir(src)):
        if not f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            continue
        a = 1.0 if any(k in f for k in ANCHOR_BOTTOM) else 0.5
        how = fit(f"{src}/{f}", f"{dst}/{os.path.splitext(f)[0]}.jpg", anchor=a)
        print(f"  {f:38} {how}{'  (bottom)' if a == 1.0 else ''}")


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
