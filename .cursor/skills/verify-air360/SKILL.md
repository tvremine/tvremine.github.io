---
name: verify-air360
description: Drive the Air360 360° photo viewer (tvremine.github.io/360/, a static PWA in 360/index.html) in headless Chromium and capture proof. Use when you change 360/index.html or 360/manifest.json, or need to show that importing, 360° detection, the Pannellum viewer, filtering, search, or IndexedDB persistence work the way a user sees them.
---

# Verify Air360

Air360 is one static page, `360/index.html`, plus `360/manifest.json`. The site root is the Waypoint Aerial homepage. GitHub Pages serves the files with no build step. The viewer pulls Tailwind from `cdn.tailwindcss.com` and Pannellum 2.5.7 from `cdn.jsdelivr.net`, so the box needs internet access. Users pick photos with the "Import Photos" button. The app stores each photo in IndexedDB (`air360-db-v3`, store `photos`) and opens any photo card in a Pannellum viewer. `archive_version1.html` and `archive_version2.html` are older copies, reachable only by URL.

There is no backend, no account, and no test suite. The only surface is the browser page, and this skill drives it with Playwright.

All commands below run from the repo root:

```bash
S=.cursor/skills/verify-air360/scripts
```

## Launch

One-time setup creates a venv at `~/.cache/verify-air360/venv` with Playwright and Pillow, then downloads Playwright's Chromium. Set `VERIFY_AIR360_VENV` to put the venv elsewhere.

```bash
$S/setup.sh
```

Start a server for this run:

```bash
eval "$($S/start.sh)"          # or: $S/start.sh my-run-id
export VERIFY_AIR360_RUN=$RUN_ID
echo "$URL"                     # e.g. http://127.0.0.1:4360
```

`start.sh` runs `python3 -m http.server <port> --bind 127.0.0.1 --directory <repo root>` on the first free port from 4360 up. Set `VERIFY_AIR360_PORT` to force a port. It writes the PID, port, and URL to `/tmp/verify-air360/<run-id>/` and generates fixture photos in `/tmp/verify-air360/<run-id>/fixtures/`. It exits 0 and prints `RUN_ID`, `URL`, `STATE`, and `EVIDENCE` once `GET /360/` returns the `<title>Air360 • DJI 360 Viewer</title>` page. If the server exits or the title never appears within 10 seconds, it prints the server log and exits 1.

Why a plain static server: the repo has no `_config.yml`, `Gemfile`, or `package.json`, and no file has Jekyll front matter, so GitHub Pages copies every file unchanged. On 2026-10-05 the live `https://tvremine.github.io/` returned bytes identical to `index.html` at commit 6b75762, and both servers send `manifest.json` as `application/json`. What this server does not reproduce: HTTPS, GitHub's 404 page, and Safari on iOS. The README's own local recipe is VS Code Live Server on port 5500, which needs a GUI editor, so this skill does not use it.

Teardown is `$S/stop.sh` (see Cleanup).

Isolation: every run gets its own port, and IndexedDB is scoped to the origin, so two runs never share saved photos. Each `drive.sh` call starts a fresh browser context with empty storage unless you pass `--profile`. Never drive a server you did not start in this run. The user's own browser and the live site are separate origins and stay untouched.

## Doctor

Run this first, and again whenever a step fails in a way you do not understand. It is read-only.

```bash
$S/doctor.sh                    # uses $VERIFY_AIR360_RUN, or: $S/doctor.sh <run-id>
```

It checks that the PID is alive and is our `http.server` for this port and directory, that `ss` shows that PID owning the port, that `GET /` shows the Waypoint Aerial homepage, that `GET /360/` shows the Air360 title, that the served `360/index.html` matches the checkout byte for byte (and prints the commit), that `360/manifest.json` parses with `short_name` "Air360", that the three fixtures exist, that both CDNs answer, and that Playwright can launch Chromium. It ends with `doctor: healthy (...)` and exit 0, or `doctor: NOT healthy` and exit 1. Do not drive an unhealthy instance.

## Drive

`drive.sh` opens headless Chromium (SwiftShader WebGL, locale en-US, time zone America/New_York), runs the steps in order, and stops at the first failure. Each step is one quoted argument.

```bash
$S/drive.sh --name import-photos \
  "goto /360/" \
  "import sphere-2to1.jpg wide-4to1.jpg photo-4to3.jpg" \
  "expect-text 'Added 3 photos • 1 detected as 360°'" \
  "aria after-import" "screenshot after-import"
```

Options: `--run ID` (defaults to `$VERIFY_AIR360_RUN`), `--name NAME` (the evidence subdirectory, required), `--viewport WxH` (default `1280x800`), and `--profile NAME`, which keeps IndexedDB across `drive.sh` calls in this run. `$S/drive.sh --help` lists every step. The ones you will use most:

| Step | What it does |
| --- | --- |
| `goto /360/` | Open the viewer. `goto /` opens the Waypoint Aerial homepage. Use `/archive_version1.html` or `/archive_version2.html` for the archives. |
| `import FILE...` | Click "Import Photos" and pick the files in the real file chooser. Bare names resolve to the run's fixtures. |
| `click ROLE NAME`, `fill ROLE NAME VALUE` | Act on a control by ARIA role and exact accessible name. |
| `click-text TEXT` | Click the first visible element containing TEXT. Photo cards have no role, so open one by its filename. |
| `card FILENAME ROLE NAME` | Click a control inside one photo card, e.g. `card wide-4to1.jpg button ×`. |
| `click-css SELECTOR` | Last resort for a control with no accessible name. Every control listed below has one. |
| `drag SELECTOR DX DY`, `click-at X Y`, `press KEY` | Mouse drag from the element's center, mouse click at viewport coordinates, keyboard press. |
| `hover SELECTOR` | Move the mouse over an element, e.g. `hover '.photo-card:has-text("sphere-2to1.jpg")'` to reveal its ×. |
| `dialogs accept` | Answer later `confirm()` prompts with OK. The default is Cancel. |
| `expect ROLE NAME`, `expect-text`, `expect-no-text`, `expect-count-text TEXT N`, `expect-css`, `expect-url` | Assertions against what is visible. `expect-css` also fails on a zero-size element. |
| `expect-style SELECTOR PROP VALUE` | The first match's computed CSS property equals VALUE exactly, retried until transitions finish. Use it for what only shows as colour or opacity. |
| `expect-redraw SELECTOR MS` | The element's pixels change within MS, e.g. the panorama moving. |
| `idb`, `idb-count N` | Read the `photos` store and save it to `idb-<n>.json`. Never creates the database. |
| `screenshot NAME`, `aria NAME` | Save `NAME.png` and an ARIA snapshot `NAME.aria.yml`. |

Stable handles in `360/index.html`, as of the `fix-air360-bugs` changes (PR #2). The header link now goes to `/`, the Waypoint Aerial homepage:

- Buttons by name at every width: "Import Photos", "360° Only", "All", "Clear Session", and "Clear Data".
- Search: `textbox "Search filenames or dates..."` (the placeholder is its only name).
- Header link: `link "Waypoint Aerial"` (only at 640 px wide or more).
- Viewer: `button "Close viewer"`, and `button "Auto Rotate"`, whose name changes to "Stop" while rotating, at every width. The Reset button is named "Reset" at 640 px or wider and "Reset view" (its `title`) below that. `press Escape` and a click on the dark backdrop also close the viewer.
- Card controls: the delete button is `card FILENAME button ×`. It shows on hover with a mouse and always on touch screens.
- Card labels as text: `360° SPHERE` (CSS class `.sphere-badge`, green), `PANORAMA` (`.pano-badge`, amber), `WIDTH×HEIGHT`, and `N.NN:1`. The card date is the EXIF capture date when the photo has one (`Jun 14` for the sphere fixture), otherwise the file's modified date.
- Stats line under the controls: `N photos • M 360°`. It refreshes after every import, delete, and clear, and it is hidden when the list is empty.
- Header storage pill: `N photos • ~K KB thumbnails` at 768 px or wider, just `N photos` below that.
- Empty state title: `No 360° photos yet` or `No photos yet` for the active view, and `No 360° photos match "QUERY"` or `No photos match "QUERY"` after a search.
- Toasts as text: `Added N photo(s) • M detected as 360°` and `All persisted data cleared`.

Fixtures written by `start.sh` (source: `$S/make-fixtures.py`):

| File | Size | Expected label |
| --- | --- | --- |
| `sphere-2to1.jpg` | 4096×2048, ratio 2.00, EXIF Make `DJI`, DateTimeOriginal `2026:06:14 10:30:00` | `360° SPHERE`, dated `Jun 14`, found by searching `6/14/2026` |
| `wide-4to1.jpg` | 4000×1000, ratio 4.00 | `PANORAMA` |
| `photo-4to3.jpg` | 1600×1200, ratio 1.33 | `PANORAMA` |

The sphere has a grid and `SPHERE yaw N°` labels, so a screenshot shows which way the viewer faces. Opening the viewer and choosing Reset both put `SPHERE yaw 0°` near the middle.

The feature map in `features/README.md` lists the user-facing features and the exact steps for each. Read it before driving, and drive every entry point a feature file lists.

## Evidence

Everything a drive writes goes to `.verify-evidence/air360/<run-id>/<name>/` in the repo root. Git ignores that directory, and no helper deletes it.

| File | Contents |
| --- | --- |
| `steps.log` | Run header (URL, commit, viewport, profile), every step with ok or FAIL and its duration, every dialog answered, and the final PASS or FAIL. |
| `*.png`, `*.aria.yml` | The screenshots and ARIA snapshots you asked for. |
| `failure.png`, `failure.aria.yml` | The page at the failing step. |
| `idb-<n>.json` | The stored photo records: name, size, ratio, `is360`, and image blob bytes. |
| `console.log`, `network.log` | Browser console and page errors, failed requests, and HTTP 4xx and 5xx responses. |
| `../server.log` | The http.server access log, copied in by `stop.sh`. |

Proof standards:

- Exercise the real user path. Import through the "Import Photos" button and its file chooser, never by setting the hidden `#fileInput` or calling page functions. The `idb` steps only read.
- Capture the action and the resulting state, not just the final screen. Take a snapshot before and after the change, and keep `steps.log`.
- Verify side effects alongside what is visible. Imports, deletes, and clears change IndexedDB, so pair the visible result with `idb-count`. For persistence, reload and check the photo comes back.
- Use mocks only where a production boundary already isolates the external system. The fixtures are real JPEGs going through the real import code. Nothing in this app is mocked.
- No dry-run or test mode exists. Every Clear and delete you accept really empties the run's IndexedDB, which is disposable because of the per-run port.
- Check `console.log` for `[pageerror]` lines and `network.log` for failed CDN loads before calling a run green.
- Report the run id, the feature file, and the entry point with each artifact. Do not report an entry point as verified through a different one.

## Cleanup

```bash
$S/stop.sh                      # uses $VERIFY_AIR360_RUN, or: $S/stop.sh <run-id>
```

`stop.sh` reads the PID file and kills that PID only if `/proc/<pid>/cmdline` still shows `http.server <port>`. It never kills by name. It copies `server.log` into the evidence directory, then deletes `/tmp/verify-air360/<run-id>/`, which holds the PID file, fixtures, and any `--profile` browser data. Evidence under `.verify-evidence/air360/<run-id>/` stays. Run it after every attempt, including failed ones, then confirm nothing is left:

```bash
ss -ltn "sport = :${URL##*:}" | tail -n +2   # expect no output
ls .verify-evidence/air360/$RUN_ID/          # evidence still present
```

## Helpers

All helpers live in `.cursor/skills/verify-air360/scripts/` and are executable.

| Script | Invocation | Purpose |
| --- | --- | --- |
| `setup.sh` | `$S/setup.sh` | Create the venv and install Playwright, Pillow, and Chromium. Safe to re-run. |
| `start.sh` | `eval "$($S/start.sh [run-id])"` | Start the static server, generate fixtures, wait until ready. |
| `doctor.sh` | `$S/doctor.sh [run-id]` | Read-only health check. |
| `drive.sh` | `$S/drive.sh --name NAME [--viewport WxH] [--profile P] STEP...` | Drive the page and write evidence. Wraps `drive.py` with the venv's Python. |
| `make-fixtures.py` | `"$HOME/.cache/verify-air360/venv/bin/python" $S/make-fixtures.py DIR` | Write the three fixture JPEGs. `start.sh` already calls it. |
| `stop.sh` | `$S/stop.sh [run-id]` | Stop this run's server and remove its scratch state, keeping evidence. |

`lib.sh` holds the shared paths and is sourced by the shell scripts, not run directly.
