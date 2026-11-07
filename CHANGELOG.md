# Changelog

All notable changes to FlashView are documented here.

FlashView is in its pre-stable stage, on [Semantic Versioning](https://semver.org) (`0.x.y`). Its first stable release will be its first [Date Version](https://datevers.ing) (`YY.MM.DD`, the UTC release date), not `1.0.0`.

## v0.1.1

### Changed

- FlashView's address is flashview.stuxapis.net, not flash.stuxapis.net: the custom domain (`CNAME`), every page's links, Discord preview and Open Graph tags, the Embed page's script tag, and the README

## v0.1.0

### Added

- FlashView, at flash.stuxapis.net: plays SWF files in the browser with a self-hosted copy of Ruffle. Open a file with the picker or by dropping it on the player (it's read in the browser, never uploaded), or play one from a link, with a shareable `?url=` link
- An idle screen like an old DVD player's: the FlashView mark and "Please insert an SWF" bounce around the player, change colour at every wall, and land in a corner every 117 seconds (first at 61 seconds). It holds still with reduced motion or on narrow players
- The Embed page: how to load FlashView's Ruffle on another site with one script tag, or create a player from JavaScript, and its main options
- Ruffle 0.7.1, pinned in `ruffle.json` with its SHA-256 and fetched by `scripts/fetch-ruffle.sh` for the dev server, CI and the Pages deploy
- A weekly workflow that pins a newer stable Ruffle release on a branch and opens a pull request into `test`
- FlashView's own logo and icons (a screen with a lightning bolt, in red), a red theme with light and dark modes, About and Changelog pages, and the Boring Legal Stuff hub with its six pages
- A custom Discord link preview on every page except the 404 page, and a full favicon set
- `dev-server.sh`/`.bat` (dev mode on by default, `--no-dev-mode`), `commit.sh`/`.bat` for both versioning stages, `tests/pages.js`, `tests/version.sh`, and CI
