# Waypoint Aerial

Homepage for **Waypoint Aerial, LLC**, the Part 107 drone studio of Tom ReMine in Indianapolis, with the Air360 viewer for DJI equirectangular panoramas.

Live root: [tvremine.github.io](https://tvremine.github.io/)

## Pages

- `/` — Waypoint Aerial landing page
- `/work/` — filterable gallery
- `/services/` — events, property, inspection, mapping, cinematic
- `/about/` — the studio
- `/about-me/` — Thomas ReMine, for hiring managers
- `/contact/` — quote request, stored in the browser
- `/360/` — Air360, the local DJI 360° panorama viewer

The header has a **360° Viewer** button. **About Me** is in the menu and as a small link in the footer.

## 360 viewer

Open `/360/`, import DJI sphere panoramas, and look around with drag, pinch, and scroll. Photos stay in this browser (IndexedDB). Nothing is uploaded.

Older copies of the viewer remain at `archive_version1.html` and `archive_version2.html`.

## Local

Any static server works. From this folder:

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080/`.
