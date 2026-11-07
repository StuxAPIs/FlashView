// FlashView: the player page. Opens a .swf from the visitor's own device (picker, drag and drop) or from a URL,
// and plays it with the self-hosted Ruffle in /ruffle/. A local file is read in the browser and never uploaded.
(function () {
    var stage = document.getElementById('stage');
    var idle = document.getElementById('idle');
    var fileInput = document.getElementById('swf-file');
    var openBtn = document.getElementById('open-btn');
    var ejectBtn = document.getElementById('eject-btn');
    var urlForm = document.getElementById('url-form');
    var urlInput = document.getElementById('swf-url');
    var status = document.getElementById('now-playing');
    var fsCorner = document.getElementById('fs-corner');
    var fsBtn = document.getElementById('fs-btn');
    var player = null;

    window.RufflePlayer = window.RufflePlayer || {};
    window.RufflePlayer.config = {
        publicPath: '/ruffle/',
        polyfills: false,
        autoplay: 'auto',
        unmuteOverlay: 'visible',
        letterbox: 'on',
        backgroundColor: '#050506',
        splashScreen: true,
        showSwfDownload: false,
        openUrlMode: 'confirm',
        allowScriptAccess: false,
        warnOnUnsupportedContent: true,
        logLevel: 'error'
    };

    function say(text, isError) {
        status.textContent = text;
        status.classList.toggle('error', !!isError);
    }

    function eject() {
        if (player) { player.remove(); player = null; }
        stage.classList.remove('has-movie');
        ejectBtn.disabled = true;
        say('');
    }

    function load(options, label) {
        if (!window.RufflePlayer.newest) {
            say('The player could not start. Reload the page and try again.', true);
            return;
        }
        eject();
        player = window.RufflePlayer.newest().createPlayer();
        stage.appendChild(player);
        stage.classList.add('has-movie');
        ejectBtn.disabled = false;
        var api = typeof player.ruffle === 'function' ? player.ruffle() : player;
        Promise.resolve(api.load(options))
            .then(function () { say('Now playing: ' + label); })
            .catch(function (e) { say('Could not play ' + label + ': ' + (e && e.message ? e.message : e), true); });
    }

    function isSwf(file) {
        return /\.(swf|spl)$/i.test(file.name) || file.type === 'application/x-shockwave-flash';
    }

    function loadFile(file) {
        if (!file) return;
        if (!isSwf(file)) { say(file.name + " doesn't look like an SWF file.", true); return; }
        file.arrayBuffer().then(function (data) {
            load({ data: data, swfFileName: file.name }, file.name);
        });
    }

    function loadUrl(raw) {
        var url;
        try { url = new URL(raw, location.href); } catch (e) { say("That isn't a valid URL.", true); return; }
        if (url.protocol !== 'https:' && url.protocol !== 'http:') { say('Only http and https links can be played.', true); return; }
        load({ url: url.href }, url.href);
        var params = new URLSearchParams(location.search);
        params.set('url', url.href);
        history.replaceState(null, '', location.pathname + '?' + params.toString());
    }

    openBtn.addEventListener('click', function () { fileInput.click(); });
    idle.addEventListener('click', function () { fileInput.click(); });
    fileInput.addEventListener('change', function () { loadFile(fileInput.files[0]); fileInput.value = ''; });
    ejectBtn.addEventListener('click', function () {
        eject();
        history.replaceState(null, '', location.pathname);
        idle.focus();
    });
    urlForm.addEventListener('submit', function (e) {
        e.preventDefault();
        if (urlInput.value.trim()) loadUrl(urlInput.value.trim());
    });

    // Fullscreen puts the player itself (the stage) into fullscreen, idle screen or movie alike.
    var fsElement = function () { return document.fullscreenElement || document.webkitFullscreenElement || null; };
    var canFullscreen = !!(stage.requestFullscreen || stage.webkitRequestFullscreen);
    function toggleFullscreen() {
        if (fsElement()) {
            (document.exitFullscreen || document.webkitExitFullscreen).call(document);
        } else {
            var req = stage.requestFullscreen || stage.webkitRequestFullscreen;
            Promise.resolve(req.call(stage)).catch(function () { say("Fullscreen isn't available here.", true); });
        }
    }
    function syncFullscreen() {
        var on = fsElement() === stage;
        stage.classList.toggle('is-fullscreen', on);
        fsBtn.textContent = on ? 'Exit fullscreen' : 'Fullscreen';
        fsCorner.setAttribute('aria-label', on ? 'Exit fullscreen' : 'Fullscreen');
        fsCorner.title = on ? 'Exit fullscreen (Esc)' : 'Fullscreen (F11)';
    }
    if (canFullscreen) {
        fsBtn.addEventListener('click', toggleFullscreen);
        fsCorner.addEventListener('click', toggleFullscreen);
        document.addEventListener('fullscreenchange', syncFullscreen);
        document.addEventListener('webkitfullscreenchange', syncFullscreen);
        // On the "Please insert an SWF" screen, F11 fullscreens the player rather than the browser window.
        // Once a movie is loaded, F11 is left alone (the movie or the browser may want it).
        document.addEventListener('keydown', function (e) {
            if (e.key !== 'F11' || e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
            if (stage.classList.contains('has-movie') && !fsElement()) return;
            e.preventDefault();
            toggleFullscreen();
        });
    } else {
        fsBtn.hidden = true;
        fsCorner.hidden = true;
    }

    ['dragenter', 'dragover'].forEach(function (type) {
        stage.addEventListener(type, function (e) { e.preventDefault(); stage.classList.add('dragging'); });
    });
    ['dragleave', 'drop'].forEach(function (type) {
        stage.addEventListener(type, function () { stage.classList.remove('dragging'); });
    });
    stage.addEventListener('drop', function (e) {
        e.preventDefault();
        var files = e.dataTransfer && e.dataTransfer.files;
        if (files && files.length) loadFile(files[0]);
    });

    // ?url=https://example.com/movie.swf plays that link straight away (it's a share link for the same thing).
    var shared = new URLSearchParams(location.search).get('url');
    if (shared) {
        urlInput.value = shared;
        window.addEventListener('load', function () { loadUrl(shared); });
    }
})();
