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
| `bio.html` | About page: photo, intro, timeline, selected patents. |
| `styles.css` | All styling. Design tokens live in `:root` at the top. |
| `images/` | Every image the site uses, committed to git. Opaque photos were re-encoded as JPEG and a few oversized files downsized; GIFs are the untouched Wix originals. |
| `images-original/` | Full-size originals of everything re-encoded, straight from Wix. Git-ignored, local only — back it up somewhere; it's the only full-resolution copy once Wix is gone. |
| `scripts/assets.txt` | Maps each original Wix media id → local filename (provenance only; safe to leave alone). |
| `scripts/fetch-assets.sh` | One-time download of the originals from Wix's CDN. Idempotent. |

## Conventions

- **Content lives in the HTML.** There is no templating; edit the words where they appear.
- **Shared header/footer** (inner pages only) is duplicated across `snap.html`, `snap-stories.html`, `quibi-projects.html`, `bio.html`. When changing it, change all four. The home page has no header/footer by design.
- **Home button** (`.home-btn`) stacks three images — `icon-home.png` (resting), `icon-home-hover.png`, `icon-home-pressed.png` — and swaps them with `:hover` / `:active`, like the Wix image button did.
- **Home cards** are `<section class="card">` blocks. Each sets its own colours via inline CSS custom properties:
  `--panel-bg` (left panel colour), `--panel-img` (optional image behind the copy), `--panel-ink` (text colour), `--media-bg` (right side background). Copy the Snapchat block to add a new one, and add a matching `<div class="gap">` chevron above it pointing at its `id`.
- **Case-study rows** are `<section class="row">` with `.media` (left, 667px; images are cropped to 667×402 like on Wix) and `.copy` (right, 251px). Add a row by copying one.
- **Sizes mirror the Wix site measured at 1440px**: home cards are 667px tall with a 619px (43%) panel; inner pages sit on Wix's 980px canvas.
- **Fonts**: Josefin Sans (300, 300 italic, 600) from Google Fonts stands in for Brandon Grotesque, which Wix licensed and we can't ship — it has the same low x-height but sets ~10% wider, so a few paragraphs wrap one line longer than on Wix. The serif is Times New Roman, the system font Wix used. Swap `--font-sans` / `--font-serif` in `styles.css` to change site-wide.
- **Images**: reference as `images/<name>`. Prefer descriptive kebab-case names. Large screenshots should be ≤ 2800px wide; compress PNGs before committing when convenient (`pngquant`, ImageOptim, etc.).
- Keep the page working with **no JavaScript** — there currently is none, and nothing needs it.
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
