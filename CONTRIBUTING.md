<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo.svg" height="80" alt="FlashView">
  </picture>
</p>

# Contributing to FlashView

FlashView is a StuxAPIs project, part of the Stux.Group brand of businesses. The repository isn't open to
public pull requests, and per the [License](README.md#license) it isn't licensed for reuse. This document is
for anyone with write access.

Questions: [hello@stuxapis.net](mailto:hello@stuxapis.net).

## Local setup

```
git clone https://github.com/StuxAPIs/FlashView.git
cd FlashView
./dev-server.sh
```

No install step. The dev server fetches the pinned Ruffle into `ruffle/` (gitignored) the first time.
Pass `--no-dev-mode` to hide the "LOCAL DEV" banner and see the site as production serves it.

## Project conventions

- **Plain HTML/CSS/JS, no framework, no build step.** Every page is a real `.html` file at the repo root
  (or in `legal/`), with absolute asset paths (`/assets/...`), because GitHub Pages serves `404.html` at
  any URL.
- **Shared code:** styles in `assets/css/style.css`, theme and footer in `assets/js/site.js`, the player
  in `assets/js/player.js`.
- **Pages are built by `scripts/build-pages.py`.** It holds every page's content and writes all the `.html`
  files with one shared `<head>` (favicons, Open Graph, the Discord embed), header and footer. Edit the
  content there and run `python -I scripts/build-pages.py`; don't hand-edit a page, or the next build undoes
  it. CI runs it with `--check` and fails if a committed page differs. To add a page, add a `page(...)` call
  there, add it to the list in `tests/pages.js` and the copy step in `.github/workflows/pages.yml` (the 404
  page has no Discord embed).
- **Colours:** FlashView red, `#c8102e` (light) and `#ff6b70` (dark), from the logo's `#ff5a5f` to
  `#b3122a` gradient. The icon PNGs and `favicon.ico` are drawn by `python -I scripts/build-icons.py`
  from the same shapes as `assets/icon.svg`; run it after changing the icon.
- **Ruffle is never committed.** `ruffle.json` pins the release and its SHA-256, and
  `scripts/fetch-ruffle.sh` fetches it for the dev server, CI and the Pages deploy. Don't hotlink
  Ruffle's own CDN: the point is that FlashView serves it.
- **Nothing loads from elsewhere,** and files people open are never uploaded. If that ever changes,
  update the Privacy Policy and Cookies Policy first.
- **Never call the product "Flash"** on its own or use Adobe's logos: it's FlashView, and the pages say
  it isn't affiliated with Adobe.
- General contact uses `hello@stuxapis.net`; legal-page contact uses `legal@stuxapis.net`.

## The idle screen's bouncing logo

Until a movie is loaded, the player shows the FlashView mark and "Please insert an SWF", bouncing around
like an old DVD player's logo (`.bounce` in `style.css`):

- It moves with two linear, alternating animations: 13 s across and 9 s down, sized with container units
  (`cqw`, `cqh`) so it bounces off the player's edges at any size.
- It lands in a corner whenever both are at an end at once: every 117 s. The -4 s and -2 s delays start it
  part-way across, so the first corner is 61 s after the page loads.
- Its colour changes at every wall hit: the 21 hits in a 117 s cycle (multiples of 13 and of 9) are the
  stops of `bounce-colour`, `step-end`, with a 7-colour palette, delayed -56 s so 0% is a corner. A small
  pop (`bounce-pop`) runs on the same cycle. `tests/pages.js` checks the stops and timings.
- The mark is `assets/bounce-mark.svg` as a CSS mask, coloured by `currentColor`.
- With `prefers-reduced-motion`, or a player narrower than 420px, it sits still in the middle.
- Fullscreen (the corner button, the bar button, or F11 while nothing is loaded) puts the stage itself into
  fullscreen, so the logo bounces across the whole screen. F11 is only taken over on the idle screen; with a
  movie loaded it is left to the browser. Headless browsers refuse fullscreen, so test it in a real window.

If you change a duration or delay, recompute the hit percentages, the colour delay and the comment above
the keyframes, and update the test.

## Legal pages

All six live in `legal/` (`privacy`, `terms`, `cookies`, `imprint`, `disclaimer`, `opt-out`), linked from
the **Boring Legal Stuff** hub at `legal.html` (`/legal`). Keep them in step with what the site does.

## Branches

- Work on `test`, or on a branch off it. Never push to `main`
- Changes reach `main` only through a pull request from `test` into `main`, which needs CI to pass and is reviewed and merged by Leo
- Release commits and tags are made on `test` (`git push origin test v0.x.y`) and take effect when the pull request is merged. Merging deploys the site to GitHub Pages.
- The weekly Ruffle check opens its pull requests into `test`

## Versioning

FlashView is pre-stable, on Semantic Versioning `0.x.y`. To release:

1. Add a `## v0.x.y` entry at the top of `CHANGELOG.md`, with its sections in this order: Added, Changed, Fixed, Removed, Security, Deprecated.
2. Set `VERSION.md` to the same bare version (no `v`). Raise the middle number for a release that adds a
   feature or changes what visitors see (0.3.1 → 0.4.0), and the last number for fixes and small changes
   only (0.4.0 → 0.4.1). `./commit.sh --next` suggests the next fix version.
3. Run `bash tests/version.sh` and `node tests/pages.js`.
4. Run `./commit.sh` (or `commit.bat` on Windows). It checks the version, commits and tags `v0.x.y`, and never pushes.

Declaring FlashView stable is Leo's call. The stable release is its first Date Version (today's UTC date
as `YY.MM.DD`), not `1.0.0`, and the scripts refuse to go back to `0.x.y` after it.

## Before committing

- Open the changed pages with `./dev-server.sh` and click through, in light and dark mode
- After touching the player, play an SWF from a file, by dropping it, and from a link, and eject it
- Check the console for errors, and the page at phone width
