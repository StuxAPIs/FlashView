@echo off
setlocal
REM FlashView - Git commit + tag script (Windows). The same checks as commit.sh: VERSION.md must be a
REM pre-stable 0.x.y version, or a real, non-future Date Version (YY.MM.DD or YY.MM.DD-N); there is no
REM 1.0.0, and once a Date Version tag exists there's no going back to 0.x.y. Never pushes.

set "DIR=%~dp0"
cd /d "%DIR%"
set /p VERSION=<"%DIR%VERSION.md"

powershell -NoProfile -Command "$v = '%VERSION%'.Trim(); $dv = @(git tag) -match '^v\d{2}\.\d{2}\.\d{2}(-[1-9]\d*)?$'; if ($v -match '^0\.(0|[1-9]\d*)\.(0|[1-9]\d*)$') { if ($dv.Count) { exit 4 }; exit 0 }; if ($v -notmatch '^\d{2}\.(0[1-9]|1[0-2])\.(0[1-9]|[12]\d|3[01])(-[1-9]\d*)?$') { exit 1 }; $d = $v.Split('-')[0]; $p = [DateTime]::MinValue; if (-not [DateTime]::TryParseExact($d, 'yy.MM.dd', [Globalization.CultureInfo]::InvariantCulture, 'None', [ref]$p)) { exit 1 }; $t = [DateTime]::UtcNow.ToString('yy.MM.dd'); if ($d -gt $t) { exit 2 }; if ($d -lt $t) { exit 3 }; exit 0"
if errorlevel 4 (
    echo VERSION.md holds %VERSION%, but the project has moved to Date Versioning and can't go back to 0.x.y.
    exit /b 1
) else if errorlevel 3 (
    echo Warning: VERSION.md is dated before today ^(UTC^). Releasing today? Use today's date.
) else if errorlevel 2 (
    echo VERSION.md holds %VERSION%, which is dated in the future ^(UTC^). Date Versions can't be.
    exit /b 1
) else if errorlevel 1 (
    echo VERSION.md holds %VERSION%, which isn't a 0.x.y version or a Date Version ^(YY.MM.DD or YY.MM.DD-N^). There is no 1.0.0.
    exit /b 1
)

git rev-parse -q --verify "refs/tags/v%VERSION%" >nul 2>&1
if not errorlevel 1 (
    echo Tag v%VERSION% already exists, and released versions can't change.
    exit /b 1
)

git add -A
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Release v%VERSION%" -m "See CHANGELOG.md for details."
) else (
    echo Nothing to commit - tagging the current HEAD as v%VERSION%.
)

git tag -a "v%VERSION%" -m "FlashView v%VERSION%"
echo Tagged v%VERSION%.
echo Push with: git push origin test v%VERSION%, then open a pull request from test into main.
