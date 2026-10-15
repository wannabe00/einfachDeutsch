"""Build every logo file from one definition of the symbol.

    cd frontend && python3 scripts/make_brand.py

Writes the SVGs, then renders the PNGs with macOS's `qlmanage` (no other
tools needed). Re-run it after changing the shapes below; the header mark in
src/components/layout/BrandMark.tsx is printed at the end to paste in.

The symbol: a blue square, a pink triangle centred on top, a yellow circle on
the right, softly rounded, with a thin gap in the background colour where the
shapes overlap.
"""

import math
import pathlib
import shutil
import subprocess
import tempfile

BLUE, PINK, YELLOW = "#0A6CDB", "#E2407E", "#FBBF24"
INK, RED, BG_DARK = "#111114", "#D6001C", "#0B0B0F"
ROUND = 5.0
OG_PAD = (1200 - 630) // 2  # see og_svg
PUBLIC = pathlib.Path(__file__).resolve().parent.parent / "public"


def rotate(pts, deg, cx, cy):
    a = math.radians(deg)
    return [
        (cx + (x - cx) * math.cos(a) - (y - cy) * math.sin(a),
         cy + (x - cx) * math.sin(a) + (y - cy) * math.cos(a))
        for x, y in pts
    ]


def rounded(pts, r):
    """Closed path through `pts` with every corner rounded."""
    corners = []
    for i in range(len(pts)):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % len(pts)]
        v1 = (p0[0] - p1[0], p0[1] - p1[1])
        v2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1, l2 = math.hypot(*v1), math.hypot(*v2)
        ang = math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (l1 * l2))
        d = min(r / math.tan(ang / 2), l1 / 2, l2 / 2)
        a = (p1[0] + v1[0] / l1 * d, p1[1] + v1[1] / l1 * d)
        b = (p1[0] + v2[0] / l2 * d, p1[1] + v2[1] / l2 * d)
        corners.append((a, p1, b))
    d = f"M{corners[0][2][0]:.2f} {corners[0][2][1]:.2f}"
    for a, c, b in corners[1:] + corners[:1]:
        d += f"L{a[0]:.2f} {a[1]:.2f}Q{c[0]:.2f} {c[1]:.2f} {b[0]:.2f} {b[1]:.2f}"
    return d + "Z"


def shapes():
    """(square path, triangle path, circle (cx, cy, r)) in symbol units."""
    square = rotate([(18, 47), (56, 47), (56, 85), (18, 85)], -6, 37, 66)
    side, cx, base = 47, 53, 55
    h = side * math.sqrt(3) / 2
    triangle = rotate(
        [(cx - side / 2, base), (cx + side / 2, base), (cx, base - h)], 1, cx, base - h / 3
    )
    return rounded(square, ROUND), rounded(triangle, ROUND * 0.8), (71, 65, 20.5)


def _bounds():
    """A square viewBox centred exactly on the shapes (gap outline included),
    so the symbol looks centred wherever it's placed."""
    square = rotate([(18, 47), (56, 47), (56, 85), (18, 85)], -6, 37, 66)
    side, cx, base = 47, 53, 55
    h = side * math.sqrt(3) / 2
    tri = [(cx - side / 2, base), (cx + side / 2, base), (cx, base - h)]
    tri = rotate(tri, 1, cx, base - h / 3)
    ccx, ccy, r = 71, 65, 20.5
    xs = [p[0] for p in square + tri] + [ccx - r, ccx + r]
    ys = [p[1] for p in square + tri] + [ccy - r, ccy + r]
    pad = 1.7 + 1.0  # half the gap stroke, plus a hair of air
    x0, x1, y0, y1 = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad
    side_len = max(x1 - x0, y1 - y0)
    # Optical lift: the triangle's point is light and the bottom is heavy, so
    # the exactly centred symbol reads low. Shift the frame down a little.
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + side_len * 0.025
    return (round(mx - side_len / 2, 2), round(my - side_len / 2, 2), round(side_len, 2), round(side_len, 2))


VIEWBOX = _bounds()


def group(gap, gap_attr=None):
    """The three shapes as SVG elements. `gap` is the colour of the separating
    outline (or `gap_attr` for a CSS class)."""
    sq, tri, (cx, cy, r) = shapes()
    stroke = f'stroke="{gap}"' if gap else ""
    common = f'{gap_attr or stroke} stroke-width="3.4" stroke-linejoin="round" paint-order="stroke"'
    return (
        f'<path d="{sq}" fill="{BLUE}" {common}/>'
        f'<path d="{tri}" fill="{PINK}" {common}/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{YELLOW}" {common}/>'
    )


def vb():
    return " ".join(map(str, VIEWBOX))


def symbol_svg(gap):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb()}">{group(gap)}</svg>\n'


def favicon_svg():
    # Gap follows the browser's light / dark tab.
    gap_class = 'class="g"'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb()}">'
        "<style>.g{stroke:#fff}@media (prefers-color-scheme:dark){.g{stroke:#202124}}</style>"
        f"{group(None, gap_attr=gap_class)}</svg>\n"
    )


def placed(size, scale):
    """The symbol centred in a `size` square, its box `scale` of the side."""
    x, y, w, h = VIEWBOX
    s = size * scale / w
    tx = (size - w * s) / 2 - x * s
    ty = (size - h * s) / 2 - y * s
    return f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">{group("#FFFFFF")}</g>'


def app_icon_svg(size=1024):
    # Opaque white square (iOS needs no transparency); the phone rounds it.
    # The symbol fits the central 60%, inside Android's maskable safe zone.
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 {size} {size}"><rect width="{size}" height="{size}" fill="#FFFFFF"/>'
        f"{placed(size, 0.6)}</svg>\n"
    )


def og_svg():
    """1200x630 link preview (symbol left, name and tagline right), drawn in the
    middle band of a 1200x1200 canvas: Quick Look renders square, so the band
    is cropped out afterwards."""
    x, y, w, h = VIEWBOX
    s = 360 / w
    tx, ty = 110 - x * s, (630 - h * s) / 2 - y * s + OG_PAD
    font = "font-family=\"-apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif\""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200" viewBox="0 0 1200 1200">'
        '<rect width="1200" height="1200" fill="#FFFFFF"/>'
        f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">{group("#FFFFFF")}</g>'
        f'<text x="540" y="{318 + OG_PAD}" {font} font-size="88" font-weight="800" letter-spacing="-3" '
        f'fill="{INK}">einfach<tspan fill="{RED}">Deutsch</tspan></text>'
        f'<text x="544" y="{390 + OG_PAD}" {font} font-size="34" font-weight="500" fill="#6E6E73">'
        "Learn German, one short lesson a day.</text></svg>\n"
    )


def render_png(svg_text, size, out):
    """Render with macOS Quick Look; the result is `size` px on its long side."""
    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(tmp) / "in.svg"
        src.write_text(svg_text)
        subprocess.run(["qlmanage", "-t", "-s", str(size), "-o", tmp, str(src)],
                       check=True, capture_output=True)
        shutil.move(pathlib.Path(tmp) / "in.svg.png", out)


def main():
    brand = PUBLIC / "brand"
    brand.mkdir(exist_ok=True)
    (brand / "symbol.svg").write_text(symbol_svg("#FFFFFF"))
    (brand / "symbol-dark.svg").write_text(symbol_svg(BG_DARK))
    (PUBLIC / "favicon.svg").write_text(favicon_svg())
    icon = app_icon_svg()
    (brand / "app-icon.svg").write_text(icon)
    for size, name in ((180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")):
        render_png(icon, size, PUBLIC / name)
    og = og_svg()
    (brand / "og.svg").write_text(og)
    render_png(og, 1200, brand / "og.png")
    subprocess.run(["sips", "-c", "630", "1200", str(brand / "og.png")], check=True, capture_output=True)

    sq, tri, (cx, cy, r) = shapes()
    print("viewBox:", vb())
    print("square:", sq)
    print("triangle:", tri)
    print("circle:", cx, cy, r)


if __name__ == "__main__":
    main()
