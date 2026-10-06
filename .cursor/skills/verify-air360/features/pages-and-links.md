# Pages and links

The 360° viewer lives at `/360/`. Its header link returns to the Waypoint Aerial homepage at `/`. The viewer has its own web app manifest so iPhone users can add Air360 to the home screen. Two archived copies of earlier app versions are reachable only by URL. The homepage header and mobile menu include a 360° Viewer button, and About Me is in the menu and the footer.

## Sub-features

- `link-home` opens `/` from the viewer header. The homepage title is `Waypoint Aerial — Precision from above.`
- `open-viewer` opens `/360/` from the homepage button named `360° Viewer`.
- `about-me` opens `/about-me/` from the homepage menu. The page heading is `Thomas ReMine`.
- `pwa-manifest` serves `/360/manifest.json` with name "Air360 Viewer - DJI 360 Panoramas", short name "Air360", and `display: standalone`.
- `archive-v1` loads `/archive_version1.html`, the first version, which keeps photos only for the visit.
- `archive-v2` loads `/archive_version2.html`, which saves thumbnails only.

## How to get to it (user POV)

- On the viewer, choose "Waypoint Aerial" in the header (hidden below 640 px wide).
- On the homepage, choose "360° Viewer" in the header, or the same control in the mobile menu.
- On the homepage, choose "About Me" in the menu, or the small "About Me" link in the footer.
- In Safari on iPhone, open `/360/`, Share, then Add to Home Screen. The browser reads `/360/manifest.json`.
- Type `/archive_version1.html` or `/archive_version2.html` after the site URL. No page links to them.

## Driving it with drive.sh

Preconditions:

- The baseline preconditions in `README.md` hold.

- **Home link.** Run `$S/drive.sh --name pages-and-links "goto /360/" "expect link 'Waypoint Aerial'" "click link 'Waypoint Aerial'" "expect-text 'Precision from above.'" "screenshot home"`. The browser stays on this server and lands on the homepage.
- **Link hidden on phones.** Run `$S/drive.sh --name pages-and-links-phone --viewport 402x874 "goto /360/" "expect-no-text 'Waypoint Aerial'"`.
- **Open the viewer from the homepage.** Run `$S/drive.sh --name open-viewer "goto /" "click link '360° Viewer'" "expect-text 'Your 360° moments'" "expect button 'Import Photos'" "screenshot viewer"`.
- **About Me.** Run `$S/drive.sh --name about-me "goto /" "click-text 'About Me'" "expect-text 'Thomas ReMine'" "expect-text 'Project Manager, Production & Digital Execution'" "screenshot about-me"`. The first visible "About Me" is the menu link. The footer repeats it.
- **Manifest.** Run `curl -fsS "$URL/360/manifest.json" | python3 -c 'import json,sys; m=json.load(sys.stdin); print(m["short_name"], m["display"], m["start_url"])'`. Output is `Air360 standalone ./index.html`.
- **Archive v1.** Run `$S/drive.sh --name archive-v1 "goto /archive_version1.html" "expect-text 'Ready for iPhone 16 Pro'" "expect textbox 'Search filenames...'" "aria v1" "screenshot v1"`.
- **Archive v2.** Run `$S/drive.sh --name archive-v2 "goto /archive_version2.html" "expect-text 'Persisted with thumbnails only'" "expect button 'Clear Data'" "aria v2" "screenshot v2"`.
- **Proof.** The screenshots and ARIA snapshots per page, and the manifest command's output saved next to them.

## Gotchas

- The homepage link stays on the local server. It does not load `tvremine.github.io/waypoint-aerial/`.
- "About Me" appears twice on the homepage (menu and footer). `click link 'About Me'` uses the first match, which is the menu.
- Add to Home Screen needs iOS Safari. Headless Chromium cannot prove it. Verify the manifest contents and report the install step as unverified.
- The archives share the page title `Air360 • DJI 360 Viewer` with the current app. Assert their own text, not the title.
- `archive_version2.html` uses the database `air360-db-v2`, so the `idb` steps (which read `air360-db-v3`) report nothing there.
