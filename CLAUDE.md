# ncklln.com — Nick Allen's portfolio

Static site. Plain HTML + one CSS file. No build step, no dependencies, nothing to install.
Rebuilt from the original Wix site (Sept 2026) so it can be edited directly with Claude Code.

## Layout of the repo

| Path | What it is |
|---|---|
| `index.html` | Home. Dark page with a stack of full-width "cards" (Snapchat, Quibi, Route, HeyGen, Design Advising, outro). |
| `snap.html` | Snapchat case study — alternating image / copy rows. |
| `snap-stories.html` | Long-form article on designing Stories v1. Linked from `snap.html`. |
| `quibi-projects.html` | Quibi case study — same row pattern as `snap.html`. |
| `heygen-projects.html` | HeyGen case study — same row pattern, linked from "new products" on the home HeyGen card. |
| `heygen-home-v4.html`, `heygen-avatar-creation.html` | HeyGen case studies, linked from each row's "Read the case study" on `heygen-projects.html`. Sections: problem, iterations, (motion & polish), results, final prototype. |
| `bio.html` | About page: photo, intro, timeline, selected patents. |
| `styles.css` | All styling. Design tokens live in `:root` at the top. |
| `pyramid.css` | Generated. The live Prism Pyramid strip on the Home V4 case study; loaded only by that page. |
| `heygen-pyramid-playground.html` | The interactive pyramid sandbox, linked from the Home V4 case study. **The only page with JavaScript** — the mark is rebuilt and moved by script so every value is live. Self-contained: its own `<style>` and `<script>`, classes prefixed `pg-`. |
| `images/` | Every image the site uses, committed to git. Opaque photos were re-encoded as JPEG and a few oversized files downsized; The Wix GIFs are kept here untouched as source, but the pages show H.264 `.mp4` versions of them (about a third of the size, no visible difference). |
| `images-original/` | Full-size originals of everything re-encoded, straight from Wix. Git-ignored, local only — back it up somewhere; it's the only full-resolution copy once Wix is gone. |
| `scripts/assets.txt` | Maps each original Wix media id → local filename (provenance only; safe to leave alone). |
| `scripts/fetch-assets.sh` | One-time download of the originals from Wix's CDN. Idempotent. |
| `scripts/pyramid.py` | Generates `pyramid.css` and fills `<figure data-fig="evolution">` in `heygen-home-v4.html`: seven small live stages from the logo PNG to the glass pyramid (4 faces × up to 7 SVG sheets each). Copy stays hand-written in the HTML. Rerun after changing geometry, colours or motion. |
| `scripts/transcode.swift`, `scripts/poster.swift` | Video tools using macOS's built-in encoder (no ffmpeg needed). See **Video** below. |

## Conventions

- **Content lives in the HTML.** There is no templating; edit the words where they appear.
- **Shared header/footer** (inner pages only) is duplicated across `snap.html`, `snap-stories.html`, `quibi-projects.html`, `heygen-projects.html`, `heygen-home-v4.html`, `heygen-avatar-creation.html`, `heygen-pyramid-playground.html`, `bio.html`. When changing it, change all eight. The home page has no header/footer by design.
- **Home button** (`.home-btn`) stacks three images — `icon-home.png` (resting), `icon-home-hover.png`, `icon-home-pressed.png` — and swaps them with `:hover` / `:active`, like the Wix image button did.
- **Home cards** are `<section class="card">` blocks. Each sets its own colours via inline CSS custom properties:
  `--panel-bg` (left panel colour), `--panel-img` (optional image behind the copy), `--panel-ink` (text colour), `--media-bg` (right side background). Copy the Snapchat block to add a new one, and add a matching `<div class="gap">` chevron above it pointing at its `id`.
- **Case-study rows** are `<section class="row">` with `.media` (left, 667px; images are cropped to 667×402 like on Wix) and `.copy` (right, 251px). Add a row by copying one. For a screenshot that isn't 667×402 (a phone screen, a full app window), use `.media framed`: the image is shown whole, centred on the HeyGen gradient (`--heygen-bg`); add `class="phone"` to a phone screenshot or recording for rounded corners and a square frame on phones. Recordings are `<video autoplay muted loop playsinline>` with the first frame as `poster` (see **Video**).
- **Sizes mirror the Wix site measured at 1440px**: home cards are 667px tall with a 619px (43%) panel; inner pages sit on Wix's 980px canvas.
- **Fonts**: Inter (400, 500, 600, 400 italic) from Google Fonts, regular weight for body text. Brandon Grotesque (the Wix font) isn't licensed here, and the closer-matching light geometrics (League Spartan, Josefin Sans) read too thin. Inter sets ~20% wider than Brandon, so lines wrap differently than on Wix; that's accepted. The serif is Times New Roman, the system font Wix used. To change site-wide, swap `--font-sans` / `--font-serif` in `styles.css` **and** the Google Fonts `<link>` in every page's `<head>` (they're identical; sed them together).
- **HeyGen fonts** (`fonts/`): ABC Solar Display for headings and TT Norms Pro for UI text, used only where the site renders HeyGen UI (the playground's stand-in cards). Nick has rights to use them for HeyGen work; the committed files are **subsets** containing only the glyphs the mock UI needs, so they aren't usable fonts to anyone who downloads them from the public repo. Regenerate with `scripts/subset-fonts.sh` if the mock text changes.
- **Source exports** (e.g. from Figma) get saved into the repo root. Image files there are git-ignored; make a right-sized copy in `images/` and reference that.
- **Images**: reference as `images/<name>`. Prefer descriptive kebab-case names. Large screenshots should be ≤ 2800px wide; compress PNGs before committing when convenient (`pngquant`, ImageOptim, etc.).
- **Case studies** (`<article class="article case">` on a `.page.wide`): `.crumbs`, a display-size `h1`, a two-column `.intro` (The problem / The goal + a `.facts` row), a full-width hero `figure.framed`, then `<section>`s with large `h2`s — paragraphs wrapped in `.text` (760px), figures full page width, captions as `p.cap` after the figure. Results is a `.stats` row of big numbers (`.stat.placeholder` until real ones exist); the prototype is a full-width figure. Product UI is shown with real screenshots and recordings, not CSS re-creations (fonts and sizing never match). Captions are a `<p class="cap">` *after* the figure, not a `<figcaption>`, so the generator can refill a figure without losing them. `figure.framed` puts media on the HeyGen gradient; `figure.todo` is a dashed stand-in for media not supplied yet, and `.placeholder` marks unwritten copy. Search for both before publishing.
- **Wide case studies** (`<main class="page wide">`): copy keeps its 650px column, every `figure` breaks out to the page edge — 48px from the viewport, 1440px max — and hero media is capped at ~80% of the viewport height so a whole screenshot fits on a laptop while presenting.
- **Password gate** on `heygen-projects.html` is CSS only: the `<input pattern="HeyGen123!">` in `.gate` must be valid before `.page` displays. The same block sits on the two HeyGen case studies and the playground, so each page asks once per load. The password is readable in the source; it's a courtesy curtain, not security.
- **Video**: every moving image is an H.264 MP4 (`<video autoplay muted loop playsinline poster=…>`), never a GIF or HEVC (HEVC screen recordings don't play in Firefox). Encode with `swift scripts/transcode.swift <src> images/<name>.mp4 <width> <bitrate>` — no audio, web-optimised. 1.6 Mbps at 540px wide was visually lossless for a phone recording. Make the poster with `swift scripts/poster.swift images/<name>.mp4 /tmp/p.png`, then save it as `images/<name>-poster.webp`.
- Keep the pages working with **no JavaScript**. The one exception is `heygen-pyramid-playground.html`, whose whole point is live controls; nothing else may depend on script.
- Test at phone width (≈400px). Cards stack to one column under 900px.

## Preview locally

Open `index.html` in a browser. Or, for correct relative paths and live reload:

```
python3 -m http.server 8000     # then http://localhost:8000
```

## Deploy

Hosted on **GitHub Pages** from the public repo `nrallen20/ncklln.com` (personal account), branch `main`, root folder. Every push to `main` goes live in about a minute. There's no build step: `.nojekyll` makes Pages serve the files as-is, and `CNAME` holds the custom domain, `www.ncklln.com`. The bare `ncklln.com` redirects to it, as it did on Wix.

- **Why the repo is public:** GitHub Pages on a free account only publishes public repos. Everything here is either on the live site already or harmless notes; `images-original/` is git-ignored.
- **Why not Cloudflare Pages:** a custom apex domain there needs Cloudflare nameservers, and Wix doesn't allow nameserver changes on domains bought through Wix.
- **Git auth:** this laptop's `gh` is signed in to two accounts and the work one (`nickallen-heygen`) stays active. This repo's `.git/config` has a credential helper that always uses `nrallen20`'s token (`gh auth token --user nrallen20`), so pushes work whichever account is active. On a new machine, `gh auth login` as `nrallen20` and re-add that helper.
- **DNS** lives in Wix → Settings → Domains → ncklln.com → **Manage DNS records**:
  - four `A` records, host `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (they replace Wix's A records)
  - `CNAME` record, host `www` → `nrallen20.github.io` (replaces Wix's `www` CNAME)

  GitHub issues the HTTPS certificate once those resolve; then turn on **Enforce HTTPS** in the repo's Settings → Pages (it can take up to 24 hours to become available).
- The domain registration stays with Wix (paid through 2029) and renews separately from the site plan. Once the site answers at ncklln.com, the Wix Premium plan can be cancelled.

## Things left over from the migration

- Bio timeline was "2020 – Present: Route" on Wix; updated to Route 2020–2024, HeyGen 2024–Present. Check dates.
- Patent links on Wix were broken (three pointed at one PDF). Now each links to `patents.google.com/patent/<id>`. `US18095473` is an application number and isn't linked.
- "shoot me an email" on the home page now links to `mailto:nrallen2013@gmail.com` (Wix version had no link).
- Wix served the home-page background as a 1919px-wide tile of greyscale logos (`images/bg-logos.png`), fixed behind the page at 9% opacity over black. `body.home::before` does the same.
- Wix's mobile site hid the Snapchat, Quibi and Route images; here every card stacks its panel above its image instead.
