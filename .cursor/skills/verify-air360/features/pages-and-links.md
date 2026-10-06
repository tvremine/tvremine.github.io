# Pages and links

Besides the app itself, the site has a header link to the Waypoint Aerial site, a web app manifest that lets iPhone users add Air360 to the home screen, and two archived copies of earlier app versions that are reachable only by URL.

## Sub-features

- `link-waypoint` opens `https://tvremine.github.io/waypoint-aerial/` from the header.
- `pwa-manifest` serves `manifest.json` with name "Air360 Viewer - DJI 360 Panoramas", short name "Air360", and `display: standalone`.
- `archive-v1` loads `/archive_version1.html`, the first version, which keeps photos only for the visit.
- `archive-v2` loads `/archive_version2.html`, which saves thumbnails only.

## How to get to it (user POV)

- Choose "Waypoint Aerial" in the header (hidden below 640 px wide).
- In Safari on iPhone, Share, then Add to Home Screen. The browser reads `manifest.json`.
- Type `/archive_version1.html` or `/archive_version2.html` after the site URL. No page links to them.

## Driving it with drive.sh

Preconditions:

- The baseline preconditions in `README.md` hold.
- The box can reach `tvremine.github.io` for the Waypoint step.

- **Waypoint link.** Run `$S/drive.sh --name pages-and-links "goto /" "expect link 'Waypoint Aerial'" "click link 'Waypoint Aerial'" "expect-url tvremine.github.io/waypoint-aerial/" "screenshot waypoint"`. The browser leaves the app and lands on the live Waypoint Aerial page.
- **Link hidden on phones.** Run `$S/drive.sh --name pages-and-links-phone --viewport 402x874 "goto /" "expect-no-text 'Waypoint Aerial'"`.
- **Manifest.** Run `curl -fsS "$URL/manifest.json" | python3 -c 'import json,sys; m=json.load(sys.stdin); print(m["short_name"], m["display"], m["start_url"])'`. Output is `Air360 standalone ./index.html`.
- **Archive v1.** Run `$S/drive.sh --name archive-v1 "goto /archive_version1.html" "expect-text 'Ready for iPhone 16 Pro'" "expect textbox 'Search filenames...'" "aria v1" "screenshot v1"`.
- **Archive v2.** Run `$S/drive.sh --name archive-v2 "goto /archive_version2.html" "expect-text 'Persisted with thumbnails only'" "expect button 'Clear Data'" "aria v2" "screenshot v2"`.
- **Proof.** The screenshots and ARIA snapshots per page, and the manifest command's output saved next to them.

## Gotchas

- The Waypoint step leaves the local server and loads the live site, so it fails offline. That is a network precondition, not an app failure.
- Add to Home Screen needs iOS Safari. Headless Chromium cannot prove it. Verify the manifest contents and report the install step as unverified.
- The archives share the page title `Air360 • DJI 360 Viewer` with the current app. Assert their own text, not the title.
- `archive_version2.html` uses the database `air360-db-v2`, so the `idb` steps (which read `air360-db-v3`) report nothing there.
