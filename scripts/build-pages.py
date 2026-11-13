"""Builds FlashView's pages: every .html file at the repo root and in legal/, from the content below plus one
shared <head> (favicons, Open Graph, the Discord link preview), header and footer. The .html files are
committed, so the site needs no build step; edit the content here and rerun this, rather than editing a page.

  python -I scripts/build-pages.py           rewrite the pages
  python -I scripts/build-pages.py --check   exit 1, naming them, if any page differs from what this builds (CI runs it)
"""
import json, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CHECK = "--check" in sys.argv[1:]
STALE = []
SITE = "https://flashview.stuxapis.net"
ACCENT = 0xC8102E


def esc_md(s):
    import re
    return re.sub(r"([\*_~`|\[\]])", r"\\\1", s)


def embed(title, url, bold, desc, small, buttons):
    content = f"-# [StuxAPIs](https://stuxapis.net)\n# [{esc_md(title)}]({url})\n**{esc_md(bold)}**\n{esc_md(desc)}\n-# {esc_md(small)}"
    comp = {"component": {"type": 17, "accent_color": ACCENT, "components": [
        {"type": 9, "components": [{"type": 10, "content": content}],
         "accessory": {"type": 11, "media": {"url": SITE + "/assets/icon.png"}}},
        {"type": 14},
        {"type": 1, "components": [{"type": 2, "style": 5, "label": l, "url": u} for l, u in buttons]}]}}
    return json.dumps(comp, ensure_ascii=False, separators=(",", ":"))


BUTTONS = [("Open the player", SITE + "/"), ("Embed it", SITE + "/embed"), ("StuxAPIs", "https://services.stuxapis.net")]


def head(title, desc, path, emb=True):
    full = f"{title} \u2014 FlashView" if title != "FlashView" else "FlashView \u2014 Play SWF files in your browser"
    url = SITE + path
    e = ""
    if emb:
        e = '    <script id="discord:component-embed" type="application/json">' + embed(
            "FlashView" if title == "FlashView" else f"FlashView \u00b7 {title}", url,
            "Play SWF files in your browser.", desc, "Powered by Ruffle \u00b7 nothing uploaded \u00b7 a StuxAPIs service", BUTTONS) + "</script>\n"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/favicon.ico" sizes="48x48">
    <link rel="icon" type="image/svg+xml" href="/assets/icon.svg">
    <link rel="icon" type="image/png" sizes="512x512" href="/assets/icon.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="manifest" href="/site.webmanifest">
    <meta name="theme-color" content="#121214">
{e}    <link rel="stylesheet" href="/assets/fonts/fonts.css">
    <link rel="stylesheet" href="/assets/css/style.css">
    <title>{full}</title>
    <meta name="description" content="{desc}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="FlashView by StuxAPIs">
    <meta property="og:title" content="{full}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{SITE}/assets/icon.png">
    <meta property="og:image:width" content="512">
    <meta property="og:image:height" content="512">
    <meta property="og:image:alt" content="FlashView icon">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{full}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{SITE}/assets/icon.png">
</head>
<body>
"""


def header(current):
    def nav(href, label):
        cur = ' aria-current="page"' if href == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""
<header class="site-header">
    <a class="brand" href="/" aria-label="FlashView home"><img class="brand-logo brand-logo--dark" src="/assets/logo-dark.svg" alt="FlashView" width="156" height="30"><img class="brand-logo brand-logo--light" src="/assets/logo.svg" alt="FlashView" width="156" height="30"><img class="brand-icon" src="/assets/icon.svg" alt="FlashView" width="32" height="32"></a>
    <div class="header-right">
        <nav class="site-nav" aria-label="Main">{nav('/', 'Player')}{nav('/embed', 'Embed')}{nav('/about', 'About')}</nav>
        <button type="button" id="theme-toggle" title="Toggle light/dark mode" aria-label="Toggle light/dark mode">&#9788;</button>
    </div>
</header>
"""


FOOTER = """
<footer>
    <p>&copy; <span data-copyright-years data-start="2026">2026</span> Stux.Group &mdash; <a href="/changelog" id="version-link">Changelog</a> &middot; <a href="/legal">Boring Legal Stuff</a> &middot; <a href="/about">About</a> &middot; <a href="https://services.stuxapis.net">A StuxAPIs Service</a></p>
    <p>Plays SWF files with <a href="https://ruffle.rs">Ruffle</a>. FlashView isn't affiliated with or endorsed by Adobe.</p>
</footer>
"""


def page(path_file, title, desc, url_path, current, body, scripts=("/assets/js/site.js",), emb=True):
    s = "".join(f'<script src="{x}"></script>\n' for x in scripts)
    html = head(title, desc, url_path, emb) + header(current) + body + FOOTER + s + "</body>\n</html>\n"
    full = os.path.join(ROOT, path_file)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


INDEX = """
<main>
    <div class="hero">
        <p class="service-eyebrow"><img src="/assets/stuxapis-icon.png" alt=""><a href="https://services.stuxapis.net">A StuxAPIs Service</a></p>
        <h1>Play <em>SWF</em> files in your browser</h1>
        <p class="lede">Open an old Flash game or animation from your computer, or from a link, and play it right here. No plugin, no download, and your file never leaves your device.</p>
    </div>

    <div class="player-shell">
        <div class="stage" id="stage">
            <button type="button" class="idle" id="idle" aria-label="Open an SWF file to play">
                <span class="bounce" aria-hidden="true"><span class="bounce-inner"><span class="bounce-mark"></span><span class="bounce-text">Please insert an SWF</span></span></span>
                <span class="idle-hint">Click, or drop a .swf file here <span class="hint-enter">&middot; F11 for fullscreen</span><span class="hint-exit">&middot; Esc to exit fullscreen</span></span>
            </button>
            <button type="button" class="fs-corner" id="fs-corner" aria-label="Fullscreen" title="Fullscreen (F11)"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path class="fs-enter" d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5"/><path class="fs-exit" d="M9 4v5H4M20 9h-5V4M15 20v-5h5M4 15h5v5"/></svg></button>
        </div>
        <div class="player-bar">
            <button type="button" class="btn btn-solid" id="open-btn">Open SWF file</button>
            <form class="url-form" id="url-form">
                <label class="visually-hidden" for="swf-url">SWF link</label>
                <input type="url" id="swf-url" name="url" placeholder="https://example.com/movie.swf" inputmode="url" autocomplete="off" spellcheck="false">
                <button type="submit" class="btn">Play link</button>
            </form>
            <button type="button" class="btn" id="fs-btn" title="Fullscreen (F11 before a movie is loaded)">Fullscreen</button>
            <button type="button" class="btn" id="eject-btn" disabled>Eject</button>
            <input type="file" id="swf-file" accept=".swf,.spl,application/x-shockwave-flash" hidden>
        </div>
        <p class="now-playing" id="now-playing" role="status" aria-live="polite"></p>
    </div>

    <section id="how">
        <h2>How it works</h2>
        <div class="cards">
            <div class="card"><h3>Stays on your device</h3><p>A file you open is read by your own browser and played there. It isn't uploaded anywhere.</p></div>
            <div class="card"><h3>Links work too</h3><p>Paste a link to an <code>.swf</code> and it plays from there. The site hosting it has to allow it (CORS). Share <code>?url=</code> links to send someone straight to a movie.</p></div>
            <div class="card"><h3>Powered by Ruffle</h3><p>FlashView runs <a href="https://ruffle.rs">Ruffle</a>, an open-source Flash Player emulator, served from this site. Older ActionScript 1 and 2 content works best; ActionScript 3 support is still growing.</p></div>
            <div class="card"><h3>Use it on your site</h3><p>Add one script tag and Ruffle plays the Flash embeds already on your pages. See <a href="/embed">Embed</a>.</p></div>
        </div>
    </section>
</main>
"""

EMBED = """
<main>
    <div class="hero">
        <p class="service-eyebrow"><img src="/assets/stuxapis-icon.png" alt=""><a href="https://services.stuxapis.net">A StuxAPIs Service</a></p>
        <h1>Embed <em>Ruffle</em> on your site</h1>
        <p class="lede">FlashView hosts a copy of Ruffle you can load from your own pages. Add one script tag and your old Flash embeds play again.</p>
    </div>

    <section id="quick-start">
        <h2>Quick start</h2>
        <p class="section-sub">Put this anywhere on a page with Flash content. Ruffle finds every <code>&lt;object&gt;</code> and <code>&lt;embed&gt;</code> that loads an SWF and replaces it with a player.</p>
<pre><code>&lt;script src="https://flashview.stuxapis.net/ruffle/ruffle.js"&gt;&lt;/script&gt;</code></pre>
        <p class="section-sub">Ruffle loads its WebAssembly from FlashView too, so there's nothing else to host. Your SWF files stay on your own site.</p>
    </section>

    <section id="javascript">
        <h2>Add a player from JavaScript</h2>
        <p class="section-sub">For a page without existing embeds, create a player yourself:</p>
<pre><code>&lt;div id="game" style="width:800px;height:600px"&gt;&lt;/div&gt;
&lt;script src="https://flashview.stuxapis.net/ruffle/ruffle.js"&gt;&lt;/script&gt;
&lt;script&gt;
  const player = window.RufflePlayer.newest().createPlayer();
  player.style.width = '100%';
  player.style.height = '100%';
  document.getElementById('game').appendChild(player);
  player.ruffle().load('/games/my-game.swf');
&lt;/script&gt;</code></pre>
    </section>

    <section id="config">
        <h2>Options</h2>
        <p class="section-sub">Set <code>window.RufflePlayer.config</code> before the script tag to change how every player behaves. A few useful ones:</p>
<pre><code>&lt;script&gt;
  window.RufflePlayer = window.RufflePlayer || {};
  window.RufflePlayer.config = {
    autoplay: 'on',            // 'auto', 'on' or 'off'
    unmuteOverlay: 'hidden',   // or 'visible'
    letterbox: 'on',           // 'fullscreen', 'off' or 'on'
    backgroundColor: '#000000',
    splashScreen: false
  };
&lt;/script&gt;
&lt;script src="https://flashview.stuxapis.net/ruffle/ruffle.js"&gt;&lt;/script&gt;</code></pre>
        <table>
            <tr><th>Option</th><th>What it does</th></tr>
            <tr><td>autoplay</td><td><code>auto</code> plays when the browser allows it; <code>on</code> always tries; <code>off</code> waits for a click.</td></tr>
            <tr><td>unmuteOverlay</td><td>Whether to show the &ldquo;click to unmute&rdquo; overlay when sound is blocked.</td></tr>
            <tr><td>letterbox</td><td>Black bars to keep the movie's shape: <code>on</code>, <code>off</code> or <code>fullscreen</code> only.</td></tr>
            <tr><td>backgroundColor</td><td>Overrides the movie's own background colour.</td></tr>
            <tr><td>splashScreen</td><td>Whether to show Ruffle's loading screen.</td></tr>
            <tr><td>polyfills</td><td><code>false</code> stops Ruffle replacing existing embeds, if you only want players you create.</td></tr>
        </table>
        <p class="section-sub">The full list is in <a href="https://github.com/ruffle-rs/ruffle/wiki/Using-Ruffle#javascript-api">Ruffle's documentation</a>.</p>
    </section>

    <section id="version">
        <h2>Which version</h2>
        <p class="section-sub">FlashView serves Ruffle <strong id="ruffle-version">(loading&hellip;)</strong>, a stable release. We check for new releases every week and update after testing. If you need a fixed version, or a lot of traffic, host Ruffle yourself: download the <a href="https://ruffle.rs/downloads">self-hosted build</a> and upload its files next to your pages.</p>
        <p class="section-sub">Ruffle is made by the <a href="https://github.com/ruffle-rs/ruffle">Ruffle contributors</a> and is licensed MIT or Apache 2.0 (<a href="/ruffle/LICENSE_MIT">MIT</a>, <a href="/ruffle/LICENSE_APACHE">Apache</a>).</p>
    </section>
</main>
"""

EMBED_SCRIPT = """<script>
    fetch('/ruffle.json').then(function (r) { return r.json(); }).then(function (j) {
        document.getElementById('ruffle-version').textContent = j.version;
    }).catch(function () { document.getElementById('ruffle-version').textContent = 'a pinned release'; });
</script>
"""

ABOUT = """
<main class="narrow">
    <h1>About</h1>
    <p class="subtitle">Play SWF files in your browser, from a StuxAPIs service.</p>
    <p><a href="/">FlashView</a> plays Flash content (SWF files) in any modern browser, with no plugin. Open a file from your device or a link, and it plays on the page. It's built on <a href="https://ruffle.rs">Ruffle</a>, an open-source Flash Player emulator written in Rust, which FlashView hosts itself.</p>
    <h2>What it does</h2>
    <ul>
        <li>Plays an SWF from your computer (pick it, or drop it on the player). The file is read by your browser and never uploaded.</li>
        <li>Plays an SWF from a link, and gives you a <code>?url=</code> link to share it.</li>
        <li>Hosts Ruffle for other sites: one script tag brings their old Flash embeds back. See <a href="/embed">Embed</a>.</li>
    </ul>
    <h2>What plays</h2>
    <p>Ruffle supports most ActionScript 1 and 2 content (most Flash games and animations from before 2010), and a growing share of ActionScript 3. If something doesn't play, it's usually a Ruffle limitation; their <a href="https://ruffle.rs/compatibility">compatibility page</a> says what works.</p>
    <h2>The name</h2>
    <p>Flash and Flash Player are trademarks of Adobe. FlashView isn't affiliated with or endorsed by Adobe, and neither is Ruffle.</p>
    <h2>Who's behind this</h2>
    <p>Built &amp; Maintained by <a href="https://stuxapis.net">StuxAPIs</a>, Hosted by <a href="https://stuxedo.com">Stuxedo</a>. StuxAPIs is a part of the Stux.Group brand of businesses.</p>
</main>
"""

CHANGELOG = """
<main class="narrow">
    <h1>Changelog</h1>
    <p class="subtitle">What changed in each FlashView release. FlashView is in its pre-stable stage, on Semantic Versioning (<code>0.x.y</code>).</p>
    <div id="changelog-body"><p class="changelog-p">Loading&hellip;</p></div>
</main>
"""

CHANGELOG_SCRIPT = """<script>
    (function () {
        var target = document.getElementById('changelog-body');
        // Fixed display order: sections are sorted into this order at render time rather than trusting the
        // markdown's order; unknown types go last.
        var CATEGORIES = ['Added', 'Changed', 'Fixed', 'Removed', 'Security', 'Deprecated'];
        function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
        function inline(s) {
            return esc(s).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\\*\\*([^*]+)\\*\\*/g, '<strong>$1</strong>')
                .replace(/\\[([^\\]]+)\\]\\((https?:[^)\\s]+)\\)/g, '<a href="$2">$1</a>');
        }
        function render(md) {
            var releases = md.replace(/\\r\\n/g, '\\n').split(/^(?=## )/m).filter(function (r) { return /^## /.test(r); });
            target.innerHTML = releases.map(function (rel) {
                var chunks = rel.split(/^(?=### )/m);
                var version = chunks.shift().match(/^##\\s+(.+)/)[1].trim();
                var sections = chunks.map(function (c, i) {
                    var name = (c.match(/^###\\s+(.+)/) || [, ''])[1].trim();
                    var rank = CATEGORIES.indexOf(name);
                    var items = [];
                    c.split('\\n').slice(1).forEach(function (line) {
                        var m = line.match(/^-\\s+(.*)$/);
                        if (m) items.push(m[1]); else if (line.trim() && items.length) items[items.length - 1] += ' ' + line.trim();
                    });
                    return { name: name, rank: rank === -1 ? CATEGORIES.length : rank, i: i, items: items };
                }).sort(function (a, b) { return a.rank - b.rank || a.i - b.i; });
                return '<div class="changelog-entry"><h3 class="changelog-version">' + esc(version) + '</h3>' +
                    sections.map(function (s) {
                        var label = CATEGORIES.indexOf(s.name) !== -1
                            ? '<span class="changelog-label changelog-label-' + s.name.toLowerCase() + '">' + s.name + '</span>'
                            : '<strong>' + esc(s.name) + '</strong>';
                        return '<div class="changelog-label-row">' + label + '</div><ul class="changelog-list">' +
                            s.items.map(function (it) { return '<li>' + inline(it) + '</li>'; }).join('') + '</ul>';
                    }).join('') + '</div>';
            }).join('') || '<p class="changelog-p">No changelog entries yet.</p>';
        }
        fetch('/CHANGELOG.md').then(function (r) { if (!r.ok) throw new Error(); return r.text(); }).then(render)
            .catch(function () { target.innerHTML = '<p class="changelog-p">The changelog couldn\\'t be loaded. It\\'s also on <a href="https://github.com/StuxAPIs/FlashView/blob/main/CHANGELOG.md">GitHub</a>.</p>'; });
    })();
</script>
"""

LEGAL = """
<main class="narrow">
    <h1>Boring Legal Stuff</h1>
    <p class="subtitle">The stuff nobody reads but everybody needs. All of it, in one place, in plain English.</p>
    <div class="legal-grid">
        <a href="/legal/privacy" class="legal-card"><h3>Privacy Policy</h3><p>What's collected (almost nothing) and why.</p></a>
        <a href="/legal/terms" class="legal-card"><h3>Terms and Ethics</h3><p>The simple rules for using FlashView.</p></a>
        <a href="/legal/cookies" class="legal-card"><h3>Cookies Policy</h3><p>No cookies. Just your theme, and the movies' own saves.</p></a>
        <a href="/legal/imprint" class="legal-card"><h3>Imprint</h3><p>Who runs FlashView, and how to reach them.</p></a>
        <a href="/legal/disclaimer" class="legal-card"><h3>Disclaimer</h3><p>Trademarks, the content you play, and links.</p></a>
        <a href="/legal/opt-out" class="legal-card"><h3>Opt-Out Preferences</h3><p>There's nothing sold, so nothing to opt out of.</p></a>
    </div>
    <p class="section-sub">Questions about any of this? Contact <a href="mailto:legal@stuxapis.net">legal@stuxapis.net</a>.</p>
</main>
"""

def legal_page(title, meta, body):
    return f"""
<main class="narrow">
    <a class="back-link" href="/legal">&larr; Boring Legal Stuff</a>
    <h1>{title}</h1>
    <p class="meta">{meta}</p>
{body}
</main>
"""

EFF = "Effective: 7 November 2026"
PRIVACY = legal_page("Privacy Policy", EFF, """    <h2>The short version</h2>
    <p>FlashView is a static website with no server-side code, no database, no accounts and no analytics. We don't collect anything about you.</p>
    <h2>Files you open</h2>
    <p>When you open an SWF from your device, your browser reads it and plays it on the page. The file isn't uploaded to us or anyone else.</p>
    <h2>Links you play</h2>
    <p>When you play an SWF from a link, your browser downloads it straight from that link's site, which sees the request as it would any visit. The link also goes into the page's address (<code>?url=</code>) so you can share it; we don't receive or store it.</p>
    <h2>What the movies do</h2>
    <p>A Flash movie can save data (its &ldquo;local shared objects&rdquo;, such as game saves), which Ruffle keeps in your browser's local storage on this site. A movie can also try to open links or contact other sites; FlashView asks you before opening a link.</p>
    <h2>Hosting</h2>
    <p>The site is served by GitHub Pages, which may log technical request details (like IP addresses) for security and operations, under <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub's privacy statement</a>. Every file, the fonts and Ruffle included, comes from this same domain.</p>
    <h2>Sites that embed our Ruffle</h2>
    <p>If another site loads Ruffle from FlashView, your browser fetches the Ruffle files from us. We don't run anything else on those requests and don't see what you play there.</p>
    <h2>Changes</h2>
    <p>If FlashView ever collects data, this policy will be updated first to say exactly what and why. The date above marks the latest revision.</p>
    <h2>Contact</h2>
    <p>Questions? Contact <a href="mailto:legal@stuxapis.net">legal@stuxapis.net</a>.</p>""")

TERMS = legal_page("Terms and Ethics", EFF, """    <h2>Using FlashView</h2>
    <p>You're welcome to use FlashView to play SWF files, share <code>?url=</code> links, and load our hosted Ruffle on your own site. It's free, with nothing to sign up for.</p>
    <h2>Content you play</h2>
    <p>Only play content you have the right to. You're responsible for the files and links you open, and for the content on any site where you embed our Ruffle. Don't use FlashView to distribute or promote anything illegal or infringing.</p>
    <h2>Hotlinking Ruffle</h2>
    <p>Loading <code>flashview.stuxapis.net/ruffle/ruffle.js</code> from your site is fine. We may update Ruffle, change paths with notice where we can, or limit use that puts the service at risk. For a fixed version or heavy traffic, host Ruffle yourself.</p>
    <h2>No warranty</h2>
    <p>FlashView and the hosted Ruffle are provided &ldquo;as is&rdquo;, without warranty of any kind. Not every Flash movie will play correctly.</p>
    <h2>Intellectual property</h2>
    <p>The FlashView and StuxAPIs names, logos and branding belong to Stux Group Ltd and its brands. Ruffle is open source, by the Ruffle contributors, under the MIT or Apache 2.0 licence. Flash is a trademark of Adobe.</p>
    <h2>Acceptable use</h2>
    <p>Don't try to disrupt or attack FlashView or the infrastructure serving it.</p>
    <h2>Changes</h2>
    <p>These terms may change as FlashView develops. The date above marks the latest revision.</p>
    <h2>Contact</h2>
    <p>Questions? Contact <a href="mailto:legal@stuxapis.net">legal@stuxapis.net</a>.</p>""")

COOKIES = legal_page("Cookies Policy", EFF, """    <h2>Short version</h2>
    <p>FlashView sets no cookies: none for tracking, advertising or analytics.</p>
    <h2>What's stored in your browser</h2>
    <ul>
        <li><code>stuxapis-theme</code> in <code>localStorage</code>: whether you last chose light or dark mode.</li>
        <li>Saved data from the Flash movies you play (their &ldquo;local shared objects&rdquo;, such as game progress), which Ruffle keeps in <code>localStorage</code>.</li>
    </ul>
    <p><code>localStorage</code> isn't a cookie: it isn't sent to any server and never leaves your device.</p>
    <h2>Third parties</h2>
    <p>There are no third-party scripts, ads or trackers, so nothing else can set cookies here either.</p>
    <h2>Clearing it</h2>
    <p>Clear this site's data in your browser's settings at any time. This also deletes the movies' saves.</p>
    <h2>Contact</h2>
    <p>Questions? Contact <a href="mailto:legal@stuxapis.net">legal@stuxapis.net</a>.</p>""")

IMPRINT = legal_page("Imprint", EFF, """    <h2>Operator</h2>
    <p>FlashView is operated by <strong>StuxAPIs</strong>, which is operated by:</p>
    <p><strong>Stux Group Ltd</strong><br>
    Company number: 13160574<br>
    Registered in England and Wales<br>
    Registered office: 124 City Road, London, EC1V 2NX, England, United Kingdom</p>
    <h2>Contact</h2>
    <p>General enquiries: <a href="mailto:hello@stuxapis.net">hello@stuxapis.net</a><br>
    Legal enquiries: <a href="mailto:legal@stuxapis.net">legal@stuxapis.net</a></p>
    <h2>Responsibility for content</h2>
    <p>Stux Group Ltd is responsible for FlashView's own pages. It isn't responsible for the SWF files visitors open or link to, which aren't hosted here.</p>""")

DISCLAIMER = legal_page("Disclaimer", EFF, """    <h2>Trademarks</h2>
    <p>Adobe, Flash and Flash Player are trademarks of Adobe in the United States and other countries. FlashView isn't affiliated with, sponsored or endorsed by Adobe. Ruffle is an independent open-source project, also unaffiliated with Adobe and with FlashView.</p>
    <h2>Content you play</h2>
    <p>FlashView doesn't host, check or endorse the SWF files you open or link to. They're the responsibility of whoever made or published them.</p>
    <h2>Accuracy</h2>
    <p>FlashView and Ruffle emulate Flash Player, not perfectly. Some movies play differently from the original or not at all. Everything is provided &ldquo;as is&rdquo; and may change between releases.</p>
    <h2>Accessibility</h2>
    <p>We aim to keep FlashView usable with a keyboard and a screen reader, but the Flash content itself often isn't accessible. If you hit a barrier in FlashView's own pages, tell us at <a href="mailto:legal@stuxapis.net">legal@stuxapis.net</a>.</p>
    <h2>Security</h2>
    <p>Found a security issue? Please report it to <a href="mailto:legal@stuxapis.net">legal@stuxapis.net</a> before disclosing it publicly. Issues in Ruffle itself go to <a href="https://github.com/ruffle-rs/ruffle/security">the Ruffle project</a>.</p>
    <h2>Third-party links</h2>
    <p>We aren't responsible for the content or availability of sites we link to.</p>""")

OPTOUT = legal_page("Opt-Out Preferences", "The short version: there's nothing to opt out of.", """    <h2>No data sale or sharing</h2>
    <p>Laws like California's CCPA/CPRA give you the right to opt out of the sale or sharing of your personal data. FlashView collects no personal data for advertising or analytics, so there's none to sell or share.</p>
    <h2>What actually happens</h2>
    <p>Everything FlashView needs, Ruffle and the fonts included, comes from this same domain. Files you open stay on your device. Links you play are fetched by your browser straight from their own site.</p>
    <h2>Do Not Track</h2>
    <p>FlashView runs no tracking, so a Do Not Track signal changes nothing here.</p>
    <h2>Questions</h2>
    <p>Contact <a href="mailto:legal@stuxapis.net">legal@stuxapis.net</a>.</p>""")

NOTFOUND = """
<main>
    <div class="not-found">
        <div class="code">404</div>
        <h1>Page not found</h1>
        <p>Whatever you were looking for isn't here. The link might be old, or the page might have moved.</p>
        <a class="btn" href="/">&larr; Back to the player</a>
    </div>
</main>
"""

D = "Play Flash (SWF) games and animations in your browser with Ruffle. Open a file or a link; nothing is uploaded."
page("index.html", "FlashView", D, "/", "/", INDEX, ("/assets/js/site.js", "/ruffle/ruffle.js", "/assets/js/player.js"))
page("embed.html", "Embed", "Load FlashView's self-hosted Ruffle on your own site with one script tag, and your old Flash embeds play again.", "/embed", "/embed", EMBED + EMBED_SCRIPT)
page("about.html", "About", "What FlashView is: a StuxAPIs service that plays SWF files in the browser with Ruffle.", "/about", "/about", ABOUT)
page("changelog.html", "Changelog", "What changed in each FlashView release.", "/changelog", "", CHANGELOG + CHANGELOG_SCRIPT)
page("legal.html", "Boring Legal Stuff", "FlashView's privacy policy, terms, cookies policy, imprint, disclaimer and opt-out preferences.", "/legal", "", LEGAL)
page("legal/privacy.html", "Privacy Policy", "FlashView's privacy policy: no accounts, no analytics, and files you open never leave your device.", "/legal/privacy", "", PRIVACY)
page("legal/terms.html", "Terms and Ethics", "The simple rules for using FlashView and its hosted Ruffle.", "/legal/terms", "", TERMS)
page("legal/cookies.html", "Cookies Policy", "FlashView sets no cookies.", "/legal/cookies", "", COOKIES)
page("legal/imprint.html", "Imprint", "Who operates FlashView, and how to reach them.", "/legal/imprint", "", IMPRINT)
page("legal/disclaimer.html", "Disclaimer", "Trademarks, the content you play, and accuracy.", "/legal/disclaimer", "", DISCLAIMER)
page("legal/opt-out.html", "Opt-Out Preferences", "There's nothing sold or shared, so nothing to opt out of.", "/legal/opt-out", "", OPTOUT)
page("404.html", "Page not found", "That page isn't here.", "/404", "", NOTFOUND, emb=False)
if CHECK:
    if STALE:
        print("Out of date (run python -I scripts/build-pages.py): " + ", ".join(STALE))
        sys.exit(1)
    print("pages up to date")
else:
    print("pages written")
