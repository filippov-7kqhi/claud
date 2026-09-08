"""Shared SVG primitives for BranchForge / HaulCrest product imagery.

Every illustration is authored here from scratch, so the only branding that
appears on a machine is the one passed in via `brand`.
"""

W, H = 1200, 760
GROUND = 622


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------- document ---
def doc(body, defs="", bg="dark", vw=W, vh=H):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw} {vh}" '
        f'width="{vw}" height="{vh}" role="img">\n<defs>\n{base_defs()}{defs}\n</defs>\n'
        f'{backdrop(bg, vw, vh)}\n{body}\n</svg>\n'
    )


def base_defs():
    return """
<linearGradient id="steel" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#6b7280"/><stop offset=".45" stop-color="#4b5563"/>
  <stop offset="1" stop-color="#2a2f38"/></linearGradient>
<linearGradient id="steelLite" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#aeb6c2"/><stop offset="1" stop-color="#6b7280"/></linearGradient>
<linearGradient id="dark" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#31363f"/><stop offset="1" stop-color="#15181d"/></linearGradient>
<linearGradient id="rubber" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#3a3f47"/><stop offset=".5" stop-color="#23272d"/>
  <stop offset="1" stop-color="#131519"/></linearGradient>
<radialGradient id="studioD" cx=".5" cy=".42" r=".78">
  <stop offset="0" stop-color="#232a33"/><stop offset=".6" stop-color="#141920"/>
  <stop offset="1" stop-color="#0b0e13"/></radialGradient>
<radialGradient id="studioL" cx=".5" cy=".4" r=".8">
  <stop offset="0" stop-color="#ffffff"/><stop offset=".65" stop-color="#eef1f5"/>
  <stop offset="1" stop-color="#d7dce4"/></radialGradient>
<linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#9fc0d8"/><stop offset=".55" stop-color="#cfe0ea"/>
  <stop offset="1" stop-color="#e8eef2"/></linearGradient>
<radialGradient id="shadow" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="#000" stop-opacity=".55"/>
  <stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<linearGradient id="glassG" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#dfeaf2" stop-opacity=".9"/>
  <stop offset="1" stop-color="#8fa6b8" stop-opacity=".75"/></linearGradient>
"""


def paint_defs(name, light, mid, deep):
    """Body-colour ramp for a machine."""
    return (
        f'<linearGradient id="{name}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{light}"/><stop offset=".5" stop-color="{mid}"/>'
        f'<stop offset="1" stop-color="{deep}"/></linearGradient>'
        f'<linearGradient id="{name}Top" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{light}"/><stop offset="1" stop-color="{mid}"/></linearGradient>'
    )


def backdrop(kind, vw=W, vh=H):
    if kind == "dark":
        return (f'<rect width="{vw}" height="{vh}" fill="url(#studioD)"/>'
                f'<ellipse cx="{vw/2}" cy="{GROUND+18}" rx="{vw*0.42}" ry="34" fill="url(#shadow)"/>')
    if kind == "light":
        return (f'<rect width="{vw}" height="{vh}" fill="url(#studioL)"/>'
                f'<ellipse cx="{vw/2}" cy="{GROUND+18}" rx="{vw*0.40}" ry="30" fill="url(#shadow)" opacity=".5"/>')
    if kind == "blueprint":
        return (f'<rect width="{vw}" height="{vh}" fill="#0d1420"/>'
                f'<g stroke="#1e3350" stroke-width="1">'
                + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{vh}"/>' for x in range(0, vw, 40))
                + "".join(f'<line x1="0" y1="{y}" x2="{vw}" y2="{y}"/>' for y in range(0, vh, 40))
                + '</g>')
    if kind == "flat":
        return f'<rect width="{vw}" height="{vh}" fill="#f4f6f9"/>'
    return f'<rect width="{vw}" height="{vh}" fill="#111"/>'


# ------------------------------------------------------------------ pieces ---
def shadow(cx, rx, cy=None, ry=26, op=".5"):
    cy = GROUND + 14 if cy is None else cy
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#shadow)" opacity="{op}"/>'


def track(x, y, w, h, r=None):
    """Rubber crawler track, side view."""
    r = h / 2 if r is None else r
    cy = y + h / 2
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#rubber)" '
           f'stroke="#5c636d" stroke-width="2.5"/>',
           f'<rect x="{x+r*0.5}" y="{y+3}" width="{w-r}" height="7" rx="3.5" fill="#6e767f" opacity=".45"/>']
    # tread lugs
    n = int(w // 26)
    for i in range(n):
        lx = x + 10 + i * 26
        out.append(f'<rect x="{lx}" y="{y+h-11}" width="15" height="9" rx="3" fill="#0c0e11" opacity=".85"/>')
        out.append(f'<rect x="{lx}" y="{y+2}" width="15" height="8" rx="3" fill="#454b54" opacity=".5"/>')
    # sprockets / idlers
    out.append(f'<circle cx="{x+r}" cy="{cy}" r="{r*0.56}" fill="#20242a" stroke="#585f69" stroke-width="3"/>')
    out.append(f'<circle cx="{x+w-r}" cy="{cy}" r="{r*0.56}" fill="#20242a" stroke="#585f69" stroke-width="3"/>')
    out.append(f'<circle cx="{x+r}" cy="{cy}" r="{r*0.2}" fill="#6f7883"/>')
    out.append(f'<circle cx="{x+w-r}" cy="{cy}" r="{r*0.2}" fill="#6f7883"/>')
    for i in range(3):
        rx_ = x + w * 0.3 + i * (w * 0.2)
        out.append(f'<circle cx="{rx_}" cy="{cy+r*0.42}" r="{r*0.24}" fill="#31363d" stroke="#575e68" stroke-width="2"/>')
    return "".join(out)


def wheel(cx, cy, r, hub="#c9ced6"):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#rubber)"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r*0.97}" fill="none" stroke="#0b0d10" stroke-width="3" opacity=".7"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r*0.56}" fill="{hub}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r*0.56}" fill="none" stroke="#8c939d" stroke-width="3"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r*0.16}" fill="#6b7280"/>'
        + "".join(
            f'<circle cx="{cx + r*0.36*__import__("math").cos(a*3.14159/180)}" '
            f'cy="{cy + r*0.36*__import__("math").sin(a*3.14159/180)}" r="{r*0.06}" fill="#767d87"/>'
            for a in range(0, 360, 72))
        + "".join(
            f'<path d="M{cx} {cy} L{cx + r*0.95*__import__("math").cos(a*3.14159/180)} '
            f'{cy + r*0.95*__import__("math").sin(a*3.14159/180)}" stroke="#0e1114" '
            f'stroke-width="2" opacity=".35"/>' for a in range(0, 360, 30))
    )


def engine_block(x, y, w, h, fill="url(#steel)"):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="#1b1f25" stroke-width="2"/>'
        + "".join(f'<rect x="{x+12+i*(w-24)/6}" y="{y+8}" width="{(w-24)/9}" height="{h*0.42}" rx="3" '
                  f'fill="#2b3038" opacity=".8"/>' for i in range(6))
        + f'<rect x="{x+10}" y="{y+h*0.62}" width="{w-20}" height="{h*0.26}" rx="5" fill="#242931"/>'
    )


def louvres(x, y, w, h, n=6, col="#0f1216", op=".55"):
    step = h / n
    return "".join(
        f'<rect x="{x}" y="{y + i*step}" width="{w}" height="{step*0.5}" rx="2" fill="{col}" opacity="{op}"/>'
        for i in range(n))


def decal(cx, cy, brand, size=34, col="#fff", sub=None, subcol="#ffffff", anchor="middle", weight="800"):
    out = (f'<text x="{cx}" y="{cy}" text-anchor="{anchor}" font-family="Arial Black,Helvetica,sans-serif" '
           f'font-weight="{weight}" font-size="{size}" letter-spacing="{size*0.045:.1f}" fill="{col}">{esc(brand)}</text>')
    if sub:
        out += (f'<text x="{cx}" y="{cy + size*0.78}" text-anchor="{anchor}" font-family="Arial,Helvetica,sans-serif" '
                f'font-weight="700" font-size="{size*0.42}" letter-spacing="{size*0.13:.1f}" fill="{subcol}" '
                f'opacity=".92">{esc(sub)}</text>')
    return out


def hazard_stripes(x, y, w, h, a="#f5b400", b="#15181d"):
    """Diagonal warning tape."""
    cid = f"hz{abs(hash((x,y,w,h)))%99999}"
    return (
        f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/></clipPath>'
        f'<g clip-path="url(#{cid})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{a}"/>'
        + "".join(f'<path d="M{x-30+i*22} {y+h} l22 -{h} h11 l-22 {h} z" fill="{b}"/>'
                  for i in range(int(w / 22) + 3))
        + f'</g>')


def bolts(pts, r=3.5, col="#9aa2ad"):
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>' for x, y in pts)


def hose(x1, y1, x2, y2, sag=40, col="#14171c", w=7):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + sag
    return (f'<path d="M{x1} {y1} Q{mx} {my} {x2} {y2}" fill="none" stroke="{col}" '
            f'stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{x1} {y1} Q{mx} {my} {x2} {y2}" fill="none" stroke="#3d434b" '
            f'stroke-width="{w*0.3}" stroke-linecap="round" opacity=".7"/>')


# ------------------------------------------------------------------- chrome ---
def caption(text, sub=None, light=False, vw=W):
    col = "#0f172a" if light else "#ffffff"
    subc = "#475569" if light else "#93a3b8"
    out = (f'<text x="56" y="76" font-family="Arial,Helvetica,sans-serif" font-weight="800" '
           f'font-size="34" fill="{col}">{esc(text)}</text>')
    if sub:
        out += (f'<text x="56" y="110" font-family="Arial,Helvetica,sans-serif" font-weight="500" '
                f'font-size="19" fill="{subc}">{esc(sub)}</text>')
    return out


def badge(x, y, text, fill, textcol="#0b0e13", w=None, h=38, size=17):
    w = (len(text) * size * 0.66 + 34) if w is None else w
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="{fill}"/>'
            f'<text x="{x + w/2:.0f}" y="{y + h*0.66:.0f}" text-anchor="middle" '
            f'font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="{size}" '
            f'letter-spacing=".6" fill="{textcol}">{esc(text)}</text>')


def dim_h(x1, x2, y, label, col="#5ad1ff"):
    return (f'<g stroke="{col}" stroke-width="2" fill="none">'
            f'<path d="M{x1} {y-9} v18 M{x2} {y-9} v18 M{x1} {y} H{x2}"/>'
            f'<path d="M{x1} {y} l13 -6 v12 z" fill="{col}" stroke="none"/>'
            f'<path d="M{x2} {y} l-13 -6 v12 z" fill="{col}" stroke="none"/></g>'
            f'<rect x="{(x1+x2)/2-52}" y="{y-19}" width="104" height="30" rx="6" fill="#0d1420"/>'
            f'<text x="{(x1+x2)/2}" y="{y+2}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
            f'font-weight="700" font-size="17" fill="{col}">{esc(label)}</text>')


def dim_v(y1, y2, x, label, col="#5ad1ff"):
    return (f'<g stroke="{col}" stroke-width="2" fill="none">'
            f'<path d="M{x-9} {y1} h18 M{x-9} {y2} h18 M{x} {y1} V{y2}"/>'
            f'<path d="M{x} {y1} l-6 13 h12 z" fill="{col}" stroke="none"/>'
            f'<path d="M{x} {y2} l-6 -13 h12 z" fill="{col}" stroke="none"/></g>'
            f'<rect x="{x-52}" y="{(y1+y2)/2-15}" width="104" height="30" rx="6" fill="#0d1420"/>'
            f'<text x="{x}" y="{(y1+y2)/2+6}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" '
            f'font-weight="700" font-size="17" fill="{col}">{esc(label)}</text>')


def callout(x, y, tx, ty, text, col="#a3e635", dark=True):
    bw = len(text) * 9.4 + 30
    bg = "#0d1117" if dark else "#0f172a"
    return (f'<path d="M{x} {y} L{tx} {ty}" stroke="{col}" stroke-width="2" opacity=".85"/>'
            f'<circle cx="{x}" cy="{y}" r="6" fill="{col}"/>'
            f'<rect x="{tx - (bw if tx < 600 else 0)}" y="{ty-19}" width="{bw:.0f}" height="38" rx="8" '
            f'fill="{bg}" stroke="{col}" stroke-width="1.5" opacity=".96"/>'
            f'<text x="{tx - (bw/2 if tx < 600 else -bw/2):.0f}" y="{ty+6}" text-anchor="middle" '
            f'font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="16" fill="#fff">{esc(text)}</text>')


def scene_ground(vw=W, horizon=560):
    """Outdoor worksite ground plane."""
    return (f'<rect y="{horizon}" width="{vw}" height="{H-horizon}" fill="#6f7f5a"/>'
            f'<rect y="{horizon}" width="{vw}" height="26" fill="#8a9a70" opacity=".7"/>'
            f'<ellipse cx="{vw*0.5}" cy="{H-40}" rx="{vw*0.6}" ry="90" fill="#5d6b4b" opacity=".55"/>')


def tree(x, base, h, spread, trunk="#4a3a2a", leaf="#3f6b3a", op="1"):
    return (f'<g opacity="{op}"><rect x="{x-h*0.045}" y="{base-h*0.45}" width="{h*0.09}" height="{h*0.45}" fill="{trunk}"/>'
            f'<ellipse cx="{x}" cy="{base-h*0.62}" rx="{spread}" ry="{h*0.34}" fill="{leaf}"/>'
            f'<ellipse cx="{x-spread*0.4}" cy="{base-h*0.5}" rx="{spread*0.6}" ry="{h*0.24}" fill="{leaf}" opacity=".85"/>'
            f'<ellipse cx="{x+spread*0.45}" cy="{base-h*0.55}" rx="{spread*0.55}" ry="{h*0.22}" fill="{leaf}" opacity=".8"/></g>')
