# Session handoff — ncklln.com

Paste into a new Claude Code session: **"Read HANDOFF.md and CLAUDE.md, then continue."**
CLAUDE.md has the repo layout and conventions; this file has the context that isn't derivable from the code.
Last updated 2026-09-29, end of the second working day on the migration.

## Where things are

- **Repo:** `~/Desktop/Non-H/Nick's Portfolio Site` (this folder). Public GitHub repo `nrallen20/ncklln.com`, branch `main`.
- **Hosting:** GitHub Pages from `main`, root. Custom domain `www.ncklln.com` (CNAME file); `ncklln.com` redirects to it. HTTPS enforced. Every push is live in ~1 minute; check the build with `gh api repos/nrallen20/ncklln.com/pages/builds/latest`.
- **DNS** stays at Wix (domain registered there, paid through 2029; renews separately from the Premium plan). Records: four `A` for `@` → GitHub Pages IPs, `CNAME www` → `nrallen20.github.io`. Wix Premium can be cancelled now; Nick hadn't yet as of this writing.
- **Local preview:** `python3 scripts/serve.py` → http://localhost:8000. It sends `Cache-Control: no-store`; the stock `http.server` made Chrome keep stale CSS and caused three false bug reports.

## Accounts (this is Nick's personal site; keep HeyGen work separate)

- Git identity in this repo is `Nick Allen <nrallen2013@gmail.com>` (repo-local config). Global git identity is the HeyGen one — don't use it here.
- `gh` is logged into two accounts. The **active** one is the work account (`nickallen-heygen`) and must stay active. This repo's `.git/config` has a credential helper that always pushes as `nrallen20` via `gh auth token --user nrallen20`, so `git push` just works. For `gh api` calls against this repo, prefix with `GH_TOKEN="$(gh auth token --hostname github.com --user nrallen20)"`.
- Nick has one free GitHub account (work); `nrallen20` is the personal one created for this. Don't create more.

## How Nick works with the agent

- He reviews in **his own Chrome** at localhost:8000 and sends screenshots of what's wrong. Verify changes yourself before reporting; don't ask him to check.
- **Assets:** chat attachments do *not* reliably arrive as files. Ask him to save into the project folder (root or a subfolder). Everything he drops there is a source export and is git-ignored (`/*.png`, `/*.mp4`, `/homepage/`, `/mobile work/`…); make right-sized copies in `images/`.
- **Copy** is his. New copy should be in his voice: first person, short sentences, plain and a bit wry ("Right idea, wrong room."). He's given the facts for everything written so far; don't invent numbers, timelines or outcomes.
- He wants the site to feel modern and mockup-led. Product UI is shown with real screenshots/recordings, never CSS re-creations (fonts and sizing never match).
- Decisions already made: Inter (regular weight, not light); dark case-study pages; 24px corners on all media; no JavaScript except the playground page.

## Things that bit us (don't repeat)

- **Explicit height + max-width on media letterboxes** when the width caps: the box no longer matches the picture, so rounded corners "don't work" on wide screens. Size framed media with `width:auto; height:auto; max-width:100cqw; max-height:…` (see `.page.wide .article figure.framed > :is(img, video)`).
- **Chrome may not round a playing `<video>`** by `border-radius` alone. The video figure hugs the video (`width: fit-content; overflow: hidden; border-radius`) and the video also has `clip-path: inset(0 round 24px)`.
- **The pyramid generator inserts its SVG `<defs>` after `<body…>`**; when `<body>` got `class="dark"` the insertion silently failed and every pyramid rendered empty. Fixed with a regex, but if the strip is ever blank, check `class="pyr-defs"` exists in the page.
- **Screen recordings:** trim browser chrome at encode time (`scripts/transcode.swift … <crop-top-px>`), not with CSS. Measure quality at full resolution against the source; half-res PSNR hid softness. The current "Home loop" source is 1080p and soft on retina; Nick may re-record at native resolution.
- **Browser-pane quirks (agent side):** screenshots come back blank after a scripted `window.scrollTo`; use `find` + `scroll_to`, or a mouse-wheel `scroll`. `requestAnimationFrame` doesn't run while the pane is hidden, so fps can't be measured there. Videos don't paint into pane screenshots. Check pixels (a screenshot), not just DOM counts — the empty-pyramid bug passed every DOM check.

## State of the pages

- **Home / Snap / Quibi / Bio / Snap-stories:** parity with the old Wix site, Inter, GIFs replaced by looping MP4s. Untouched otherwise. Bio timeline and Route content are still the migration-era stubs and are on Nick's list for a later rebuild.
- **heygen-projects.html:** two rows (Avatar Creation, Home V4) with blurbs and "Read the case study →" links. Linked from "new products" on the home HeyGen card.
- **heygen-home-v4.html:** complete. Overview (Team 2 eng / 1 designer / 1 PM; Timeline V2→V4 in a couple of weeks; Scope), six-state crossfade hero, V1–V3 iterations, "States, motion, polish" (Figma canvas → preamble → seven-step live pyramid strip → playground CTA), Results (+45.7% avatars, +5.3% paid conversion, +19.5% downloads), "Shipped to production" recording.
- **heygen-avatar-creation.html:** complete except no Timeline fact. Overview (Team 2 eng / 1 designer; Platform mobile app), phone recording hero, three-up explainer, first-run flow strips, new-voice branch, Results (+4.6% 30-day retention, +15.9% mobile video creation).
- **heygen-pyramid-playground.html:** fullscreen dark control panel, JS-driven. Only page with JS.
- **Password protection:** none right now, by Nick's decision (nothing on these pages is private). The CSS-only gate still exists in `styles.css` for a quick curtain. A proper scheme is planned: encrypt the HeyGen pages and decrypt in-browser with a password (works on GitHub Pages; alternative is moving to a host with built-in protection).

## Open items

1. Proper password protection (above), when Nick asks.
2. Avatar Creation: Timeline fact if he wants one; a retina re-record of the Home V4 "shipped" loop for sharpness.
3. Bio page and Route section rebuilds (his stated plan; nothing started).
4. Cancel Wix Premium once he's happy; keep domain auto-renew on.
5. `images-original/` (full-size Wix originals) exists only on this Mac and is git-ignored — it should be backed up somewhere.

## Tools in `scripts/`

`serve.py` (preview), `pyramid.py` (regenerates the strip + `pyramid.css`), `transcode.swift` / `poster.swift` (video → H.264 + poster; crop-top and frame-rate-divisor args), `subset-fonts.sh` (HeyGen font glyph subsets from Nick's Downloads), `fetch-assets.sh` (one-time Wix download, historical).
