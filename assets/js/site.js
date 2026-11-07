// FlashView: shared behaviour for every page (theme toggle, footer version and copyright years).
(function () {
    var root = document.documentElement;

    var btn = document.getElementById('theme-toggle');
    if (btn) {
        var stored = null;
        try { stored = localStorage.getItem('stuxapis-theme'); } catch (e) { /* storage blocked */ }
        var isDark = stored ? stored === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches;
        var apply = function (dark) {
            root.classList.toggle('theme-dark', dark);
            root.classList.toggle('theme-light', !dark);
            btn.textContent = dark ? '☀' : '☾';
            btn.title = dark ? 'Switch to light mode' : 'Switch to dark mode';
        };
        apply(isDark);
        btn.addEventListener('click', function () {
            isDark = !isDark;
            try { localStorage.setItem('stuxapis-theme', isDark ? 'dark' : 'light'); } catch (e) { /* storage blocked */ }
            apply(isDark);
        });
    }

    var versionLink = document.getElementById('version-link');
    if (versionLink) {
        fetch(versionLink.getAttribute('data-version-src') || '/VERSION.md')
            .then(function (r) { return r.ok ? r.text() : Promise.reject(); })
            .then(function (v) { versionLink.textContent = 'v' + v.trim(); })
            .catch(function () {});
    }

    var y = new Date().getFullYear();
    document.querySelectorAll('[data-copyright-years]').forEach(function (e) {
        var s = parseInt(e.getAttribute('data-start'), 10);
        e.textContent = s >= y ? String(y) : s + '–' + y;
    });
})();
