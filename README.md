<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo.svg" height="100" alt="FlashView">
  </picture>
</p>

# FlashView

**Play SWF files in your browser.** FlashView opens an old Flash game or animation from your device, or
from a link, and plays it with a self-hosted copy of [Ruffle](https://ruffle.rs), the open-source Flash
Player emulator. Nothing is uploaded. It also hosts Ruffle for other sites: one script tag brings their
Flash embeds back.

**Live:** [flashview.stuxapis.net](https://flashview.stuxapis.net) · **Embed docs:** [flashview.stuxapis.net/embed](https://flashview.stuxapis.net/embed)

FlashView isn't affiliated with or endorsed by Adobe. Flash is a trademark of Adobe.

## Features

- Open a `.swf` with the file picker or by dropping it on the player; it's read in the browser, never uploaded
- Play an `.swf` from a link, with a shareable `?url=` link (the hosting site has to allow CORS)
- An old-DVD-player idle screen: the FlashView mark and "Please insert an SWF" bounce around the player
  and change colour at every wall, until something is loaded
- Fullscreen for the player (a corner button on the idle screen, a bar button, or F11 on the idle screen)
- Ruffle served from `flashview.stuxapis.net/ruffle/`, for any site to use:
  `<script src="https://flashview.stuxapis.net/ruffle/ruffle.js"></script>`
- Ruffle pinned to a stable release with its SHA-256 (`ruffle.json`), checked for updates every week

## Tech stack

Static HTML, CSS and JavaScript on GitHub Pages: no framework, no build step of our own. The Pages deploy
downloads the Ruffle release pinned in `ruffle.json`, checks its SHA-256 and serves it at `/ruffle/`.

## Directory structure

```
index.html, embed.html, about.html, changelog.html, legal.html, 404.html   the pages
legal/                  the six legal pages (Boring Legal Stuff)
assets/css/style.css    every page's styles, the player and its bouncing idle logo
assets/js/site.js       theme toggle, footer version and years
assets/js/player.js     the player: file picker, drag and drop, links, Ruffle setup
assets/                 logos, icons, bounce-mark.svg (the idle logo's mask), self-hosted Fredoka
ruffle.json             the pinned Ruffle release (version, asset, SHA-256)
ruffle/                 the unpacked Ruffle, fetched by scripts/fetch-ruffle.sh (gitignored)
scripts/                fetch-ruffle.sh, dev-server.py, build-icons.py
tests/                  pages.js, version.sh
.github/workflows/      ci.yml, pages.yml, update-ruffle.yml
```

## Local development

Run `./dev-server.sh [port]` (or `dev-server.bat [port]` on Windows), then open `http://127.0.0.1:8000`.
It fetches the pinned Ruffle into `ruffle/` the first time, and serves the site the way GitHub Pages does
(clean URLs, the 404 page, `application/wasm`). Dev mode is on by default and shows a "LOCAL DEV" banner;
pass `--no-dev-mode` to see the site exactly as production serves it. Needs Python 3, `curl` and `unzip`.

## Updating Ruffle

Every Monday `update-ruffle.yml` compares `ruffle.json` with Ruffle's latest stable release. If there's a
newer one, it pins it on a `ruffle-<version>` branch and opens a pull request into `test`. Try it locally,
add a changelog entry and release it as usual. To pin by hand, edit `ruffle.json` (version, tag, asset and
the zip's SHA-256) and run `bash scripts/fetch-ruffle.sh --force`.

## Testing

```
node tests/pages.js     # every page's embed, favicons and shared assets, the idle logo's timing, the Ruffle pin
bash tests/version.sh   # VERSION.md and the changelog
```

CI also checks that the pinned Ruffle downloads with the right SHA-256, and runs shellcheck.

## Versioning

FlashView is in its **pre-stable stage**, on [Semantic Versioning](https://semver.org) `0.x.y`. Its first
stable release will be its first [Date Version](https://datevers.ing) (`YY.MM.DD`, the UTC release date)
instead of `1.0.0`, and every release after that uses Date Versioning too. See [CHANGELOG.md](CHANGELOG.md).

Releases are committed and tagged on the `test` branch and reach `main` through a pull request from `test`,
which needs CI to pass and is reviewed and merged by Leo; see [Branches](CONTRIBUTING.md#branches).

## Contact

General: [hello@stuxapis.net](mailto:hello@stuxapis.net) · Legal: [legal@stuxapis.net](mailto:legal@stuxapis.net)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Closed source: see [LICENSE](LICENSE). Ruffle, which the site downloads and serves, is by the Ruffle
contributors under the MIT or Apache 2.0 licence; its licence files are served with it at `/ruffle/`.

## Copyright

(C) 2026 Stux.Group. All rights reserved.

---

*Built & Maintained by <picture><source media="(prefers-color-scheme: dark)" srcset="https://global.media.stuxapis.net/icon-light.png"><source media="(prefers-color-scheme: light)" srcset="https://global.media.stuxapis.net/icon-dark.png"><img src="https://global.media.stuxapis.net/icon-dark.png" height="14" alt="StuxAPIs" valign="middle"></picture> [StuxAPIs](https://github.com/StuxAPIs), Hosted by <img src="https://github.com/Stuxedo.png" height="14" alt="Stuxedo" valign="middle"> [Stuxedo](https://stuxedo.com).
StuxAPIs is a part of the <picture><source media="(prefers-color-scheme: dark)" srcset="https://global.media.stux.group/icon-light.png"><source media="(prefers-color-scheme: light)" srcset="https://global.media.stux.group/icon-dark.png"><img src="https://global.media.stux.group/icon-dark.png" height="14" alt="Stux.Group" valign="middle"></picture> Stux.Group brand of businesses.*
