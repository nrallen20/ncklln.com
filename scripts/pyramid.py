#!/usr/bin/env python3
"""Generates the Prism Pyramid evolution strip in heygen-home-v4.html.

    python3 scripts/pyramid.py

Writes pyramid.css and fills the <figure data-fig="evolution"> in the page. The
copy around it is hand-written in the HTML and left alone; rerun this after
changing geometry, colours or motion. Everything it emits is plain CSS + inline
SVG, matching the shipped component. The interactive version lives in
heygen-pyramid-playground.html, which builds the same mark in JavaScript.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'heygen-home-v4.html'
CSS = ROOT / 'pyramid.css'

# id, gradient from, gradient to, rotation of the wing
FACES = [('s', '#FDA1FF', '#97C5FF', 0), ('w', '#4FDB5E', '#00CDC2', 90),
         ('n', '#B78EFA', '#97C5FF', 180), ('e', '#3CE6AC', '#00E3FF', 270)]
# Face box is 200x100, the bottom half of the base square. Base corners sit at 42/158 —
# further in than "parallel to the diagonal" — so the gap still reads even after the fold
# and camera tilt foreshorten it near the rim.
PETAL = 'M42 84 L158 84 L109 30 Q100 21 91 30 Z'
RIM_STOPS = [(0, .7), (.22, .12), (.48, .45), (.75, .06), (1, .3)]


def lighten(hex_, amount):
    return '#' + ''.join(
        format(round(v + (255 - v) * amount), '02x')
        for v in (int(hex_[i:i + 2], 16) for i in (1, 3, 5)))


def defs():
    grads = []
    for fid, a, b, _ in FACES:
        grads.append(f'<linearGradient id="pg-{fid}" x1="0" y1="1" x2="1" y2="0">'
                     f'<stop stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')
        # the terminal lightened stop IS the sheen; a translucent overlay would compound at its own edge
        grads.append(f'<linearGradient id="pg-{fid}-sheen" x1="0" y1="1" x2="1" y2="0">'
                     f'<stop stop-color="{a}"/><stop offset=".6" stop-color="{b}"/>'
                     f'<stop offset="1" stop-color="{lighten(b, .4)}"/></linearGradient>')
    rim = ''.join(f'<stop offset="{o}" stop-color="#fff" stop-opacity="{op}"/>' for o, op in RIM_STOPS)
    grads.append(f'<linearGradient id="pg-rim" x1="0" y1="0" x2="1" y2="1">{rim}</linearGradient>')
    return ('<svg class="pyr-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>'
            f'<path id="petal" d="{PETAL}"/>' + ''.join(grads) + '</defs></svg>')


def use(fill, stroke, width=18, extra=''):
    return (f'<use href="#petal" fill="{fill}" stroke="{stroke}" stroke-width="{width}" '
            f'stroke-linejoin="round"{extra}/>')


def face(fid, sheets=7, front='glass', depth=7):
    """One petal as a stack of SVG sheets, back to front.
    front: 'glass' = rim sliver under an opaque sheen surface (shipped), 'plain' = the first flat gradient."""
    n = max(1, sheets)
    layers = []
    for i in range(n - 1, -1, -1):
        z = 0 if n == 1 else -depth * i / (n - 1)
        style = f' style="transform:translateZ({z:.2f}px)"' if z else ''
        g = f'url(#pg-{fid})'
        if i > 0:
            body = use(g, g) + use('#000', '#000', extra=f' opacity="{.3 * i / (n - 1):.2f}"')
        elif front == 'glass':
            s = f'url(#pg-{fid}-sheen)'
            body = use(s, 'url(#pg-rim)') + use(s, s, 15)
        else:
            body = use(g, g)
        layers.append(f'<svg viewBox="0 0 200 100"{style}>{body}</svg>')
    return ''.join(layers)


def mark(path='still', size='72%', fold=32, tilt=42, sway=4, sway_t=18, spin_t=50,
         rx=50, ry=38, lap=48, sheets=7, front='glass', depth=7, spin=True):
    style = (f'--size:{size};--fold:{fold}deg;--tilt:{tilt}deg;--tilt-lo:{tilt - sway}deg;'
             f'--tilt-hi:{tilt + sway}deg;--sway-t:{sway_t}s;--spin-t:{spin_t}s;--rx:{rx}%;--ry:{ry}%;--lap:{lap}s')
    wings = ''.join(
        f'<div class="wing wing-{fid}"><div class="face">{face(fid, sheets, front, depth)}</div></div>'
        for fid, _, _, _ in FACES)
    tilt_cls = 'pyr-tilt sway' if sway else 'pyr-tilt'
    spin_style = '' if spin else ' style="animation:none;transform:rotateZ(45deg)"'
    return (f'<div class="pyr {path}" style="{style}"><div class="pyr-y"><div class="pyr-scene">'
            f'<div class="{tilt_cls}"><div class="pyr-spin"{spin_style}>{wings}</div></div></div></div></div>')


LOGO = '<img class="flat" src="images/heygen-prism.png" alt="" width="600" height="600">'


def logo(path='still', size='100%', spin_t=60, rocking=False):
    """The logo PNG itself: still, drifting flat, or rocking as a rigid card in perspective."""
    style = f'--size:{size};--spin-t:{spin_t}s;--rx:50%;--ry:38%;--lap:48s;--tilt-lo:38deg;--tilt-hi:46deg;--sway-t:18s'
    if rocking:
        inner = f'<div class="pyr-scene"><div class="pyr-tilt sway"><div class="pyr-spin">{LOGO}</div></div></div>'
    elif path == 'still':
        inner = LOGO
    else:
        inner = f'<div class="pyr-spin">{LOGO}</div>'
    return f'<div class="pyr {path}" style="{style}"><div class="pyr-y">{inner}</div></div>'


def step(cell, name, note, cls=''):
    return f'<div class="step{cls}"><div class="cell">{cell}</div><b>{name}</b><span>{note}</span></div>'


STRIP = '<div class="strip">' + ''.join([
    step(logo(size='64%'), 'The logo', 'The HeyGen mark: a PNG, drawn at one forced perspective.'),
    step(mark(fold=0, tilt=0, sway=0, sheets=1, front='plain', spin=False), 'Even petals',
         'Redrawn flat as one petal, four times. No baked-in angle.'),
    step(mark(fold=0, tilt=32, sway=14, sway_t=5, sheets=1, front='plain', spin=False), 'Into 3D + motion',
         'The flat mark placed in perspective space and set rocking. Still a single layer.'),
    step(mark(fold=32, tilt=42, spin_t=40, sheets=1, front='plain'), 'Folded',
         'Each petal tilts up on its base edge until it reads as a pyramid.'),
    step(mark(fold=32, tilt=50, sway=0, spin_t=40, sheets=7, front='plain', depth=26), 'Depth',
         'Seven stacked sheets stand in for a solid slab. Fanned apart here so you can count them.'),
    step(mark(spin_t=40), 'Light &amp; glass', 'A baked-in sheen and a patchy rim of light, so the edge catches as it turns.'),
    step(mark('ellipse', size='60%', rx=22, ry=14, lap=16, spin_t=40), 'Motion path',
         'Orbit, spin and tilt sway on three clocks that never line up. Hover to freeze and frost.', ' frost'),
]) + '</div>'

CSS_TEXT = '''/* Generated by scripts/pyramid.py — the live Prism Pyramid strip on heygen-home-v4.html.
   Edit the script, not this file. */

.pyr-defs { position: absolute; width: 0; height: 0; overflow: hidden; }

/* ---- the strip: seven small stages in a row (scrolls sideways on phones) ---- */
.framed.live { content-visibility: auto; contain-intrinsic-size: auto 480px; padding: 40px 32px; }
.strip { display: flex; gap: 28px; width: 100%; overflow-x: auto; scroll-snap-type: x proximity; padding-bottom: 6px; color: #fff; }
.step { position: relative; flex: 1 0 150px; scroll-snap-align: center; display: grid; grid-template-rows: auto auto 1fr; gap: 6px; font-size: 13px; line-height: 1.4; }
.step + .step::before { content: "\\2192"; position: absolute; left: -22px; top: calc(50% - 60px); color: rgb(255 255 255 / .35); font-size: 16px; }
.step b { font-weight: 600; font-size: 15px; margin-top: 10px; }
.step span { color: rgb(255 255 255 / .65); }
.cell { position: relative; width: 100%; aspect-ratio: 1; border-radius: 18px; overflow: hidden; background: rgb(255 255 255 / .05); }
.step.frost .cell { cursor: crosshair; }
.step.frost .cell:hover :is(.pyr, .pyr-tilt, .pyr-spin) { animation-play-state: paused; }
.step.frost .cell:hover .pyr { filter: blur(18px); }

/* ---- the mark: orbit wrappers → perspective scene → tilt → spin → 4 wings → folded faces → sheets ---- */
.pyr { position: absolute; width: var(--size); height: var(--size); left: calc(50% - var(--size) / 2); top: calc(50% - var(--size) / 2);
  pointer-events: none; user-select: none; will-change: transform; transition: filter .3s ease; }
.pyr-y { width: 100%; height: 100%; will-change: transform; }
.pyr-scene { width: 100%; height: 100%; perspective: 1100px; }
/* preserve-3d must run unbroken from .pyr-tilt to the sheets: no overflow, filter or opacity on any of these */
.pyr-tilt { width: 100%; height: 100%; transform-style: preserve-3d; transform: rotateX(var(--tilt)); }
.pyr-tilt.sway { animation: pyr-sway var(--sway-t) ease-in-out infinite alternate; }
.pyr-spin { position: relative; width: 100%; height: 100%; transform-style: preserve-3d; will-change: transform; animation: pyr-turn var(--spin-t) linear infinite; }
.wing { position: absolute; inset: 0; transform-style: preserve-3d; }
.wing-w { transform: rotateZ(90deg); } .wing-n { transform: rotateZ(180deg); } .wing-e { transform: rotateZ(270deg); }
.face { position: absolute; top: 50%; left: 0; width: 100%; height: 50%; transform-origin: 50% 100%; transform: rotateX(calc(-1 * var(--fold))); transform-style: preserve-3d; }
.face svg { position: absolute; inset: 0; width: 100%; height: 100%; display: block; overflow: visible; }
.flat { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; }

/* the tile ellipse: two nested alternate tracks, Y a quarter period behind, so x ≈ cos and y ≈ sin */
.pyr.ellipse { animation: orb-x var(--lap) ease-in-out infinite alternate; }
.pyr.ellipse > .pyr-y { animation: orb-y var(--lap) ease-in-out infinite alternate; animation-delay: calc(var(--lap) / -2); }
@keyframes pyr-turn { to { transform: rotateZ(360deg); } }
@keyframes pyr-sway { from { transform: rotateX(var(--tilt-lo)); } to { transform: rotateX(var(--tilt-hi)); } }
@keyframes orb-x { from { transform: translateX(calc(-1 * var(--rx))); } to { transform: translateX(var(--rx)); } }
@keyframes orb-y { from { transform: translateY(calc(-1 * var(--ry))); } to { transform: translateY(var(--ry)); } }

@media (max-width: 900px) {
  .framed.live { padding: 24px 16px; }
  .step { flex-basis: min(240px, 68vw); }
}

@media (prefers-reduced-motion: reduce) {
  .pyr, .pyr-y, .pyr-tilt, .pyr-spin { animation: none; }
  .pyr-spin { transform: rotateZ(45deg); }
}
'''


def main():
    CSS.write_text(CSS_TEXT)
    html = PAGE.read_text()
    html = re.sub(r'<svg class="pyr-defs".*?</svg>\n?', '', html, flags=re.S)
    html = re.sub(r'(<body[^>]*>\n)', lambda m: m.group(1) + defs() + '\n', html, count=1)
    pattern = re.compile(r'(<figure[^>]*data-fig="evolution"[^>]*>).*?(</figure>)', re.S)
    html, n = pattern.subn(lambda m: m.group(1) + STRIP + m.group(2), html)
    PAGE.write_text(html)
    print(f'wrote {CSS.name} and filled {n} figure(s) in {PAGE.name}')


if __name__ == '__main__':
    main()
