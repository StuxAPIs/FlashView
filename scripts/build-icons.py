"""Draws FlashView's PNG icons from the same shapes as assets/icon.svg (a red gradient tile with a screen and a
lightning bolt), so they need no SVG renderer. Run after changing the icon: python -I scripts/build-icons.py
Writes assets/icon.png (512), assets/icon-192.png, assets/icon-maskable-512.png, apple-touch-icon.png (180) and
favicon.ico (16, 32, 48)."""
import os
from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TOP, BOTTOM = (255, 90, 95), (179, 18, 42)  # #ff5a5f -> #b3122a, top-left to bottom-right
BOLT = (216, 30, 52)                         # #d81e34
WHITE = (255, 255, 255, 255)
S = 8                                        # supersampling factor


def gradient(n):
    g = Image.new("RGBA", (n, n))
    px = g.load()
    for y in range(n):
        for x in range(n):
            t = (x + y) / (2 * (n - 1))
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(TOP, BOTTOM)) + (255,)
    return g


def draw_mark(d, scale, ox=0, oy=0):
    """The 64-unit artwork: screen, stand and bolt, scaled by `scale` and offset by (ox, oy) pixels."""
    p = lambda x, y: (ox + x * scale, oy + y * scale)
    d.rounded_rectangle([p(9, 12), p(55, 46)], radius=6 * scale, fill=WHITE)
    d.rounded_rectangle([p(26, 49), p(38, 53)], radius=2 * scale, fill=WHITE)
    d.polygon([p(35.5, 16), p(22.5, 32), p(30.5, 32), p(27.5, 44), p(40.5, 27.5), p(32.3, 27.5)], fill=BOLT + (255,))


def icon(size, maskable=False):
    n = size * S
    img = gradient(n)
    d = ImageDraw.Draw(img)
    if maskable:
        # full-bleed background; the mark kept inside the 80% safe zone
        inner = n * 0.62
        draw_mark(d, inner / 64, (n - inner) / 2, (n - inner) / 2)
    else:
        mask = Image.new("L", (n, n), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, n - 1, n - 1], radius=14 * n / 64, fill=255)
        img.putalpha(mask)
        draw_mark(d, n / 64)
    return img.resize((size, size), Image.LANCZOS)


icon(512).save(os.path.join(ROOT, "assets", "icon.png"))
icon(192).save(os.path.join(ROOT, "assets", "icon-192.png"))
icon(512, maskable=True).save(os.path.join(ROOT, "assets", "icon-maskable-512.png"))
icon(180, maskable=True).convert("RGB").save(os.path.join(ROOT, "apple-touch-icon.png"))
icon(48).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("icons written")
