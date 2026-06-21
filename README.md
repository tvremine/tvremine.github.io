# DJI Air 3S 360° Viewer - Simple PWA

A lightweight, installable web app to view your DJI Air 3S (and similar) Sphere / 360° panoramas on iPhone. 

**No Mac, no Xcode, no cloud build needed.** Pure web tech that runs great in Safari and installs as a home screen app.

## Features
- **Auto-detect 360° photos**: Scans imported images and detects equirectangular / sphere panoramas (≈2:1 aspect ratio) automatically. Also supports wide panoramas.
- **Immersive viewer**: Powered by Pannellum — drag/swipe to look around, pinch or scroll to zoom, smooth controls optimized for touch.
- **Simple workflow**: Multi-select photos from your iOS Photos library → filtered list of 360s → tap to view.
- **PWA**: Add to Home Screen for app-like experience (standalone, no browser chrome).
- **Privacy-first**: Everything runs locally in your browser. No uploads, no accounts.
- **Session-based**: Photos stay loaded while the app is open (or tab). Easy to re-import your favorites anytime.

## Why this instead of native app?
- You don't have a Mac.
- Native iOS 360 viewers either don't exist well or require App Store / Mac builds.
- This gives you exactly what you need (scan + interactive view) with 10 minutes setup.
- Works on iPhone 16 Pro beautifully.

## Quick Start (5 minutes)

### 1. Get the files
You already have them in this folder (from Grok).

### 2. Test locally (optional but recommended first)
1. Open the folder in **VS Code**.
2. Install the free "Live Server" extension by Ritwick Dey (if not already).
3. Right-click `index.html` → **Open with Live Server**.
4. On your **iPhone** (same Wi-Fi):
   - Open Safari → go to `http://YOUR-COMPUTER-IP:5500` (find IP in terminal with `ipconfig getifaddr en0` on Mac or equivalent on Windows).
   - Test importing and viewing.

### 3. Deploy as your personal app (recommended for daily use)
**Easiest: GitHub Pages (free, 2 minutes)**

1. Create a new GitHub repository (or use an existing one).
2. Upload `index.html` and `manifest.json` to the repo (root or `/docs` folder).
3. Go to repo **Settings → Pages**:
   - Source: Deploy from a branch
   - Branch: `main` (or `master`)
   - Folder: `/ (root)` or `/docs`
4. Wait 1 minute, then visit: `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`
5. On iPhone Safari:
   - Open the URL
   - Tap **Share** button → **Add to Home Screen**
   - Name it "Air360" or whatever you like.
6. Now it launches like a real app! Swipe up from bottom or use app switcher.

Alternative free hosts (drag & drop):
- https://tiiny.host/
- Netlify Drop (https://app.netlify.com/drop)
- Vercel (import repo)

## How to Use the App
1. Open the app on your iPhone.
2. Tap the big **＋ Import Photos** button.
3. In the iOS sheet, choose **Photos** (or Files if you exported some).
4. Multi-select your DJI Sphere panoramas (or recent shots — the app will filter).
5. Tap **Add** / Done.
6. The app auto-detects true 360° (Sphere mode) photos and puts them in the list.
7. Tap any card to open the immersive 360° viewer.
8. **Controls**:
   - **Drag / Swipe** anywhere: Spin the camera around (yaw + pitch)
   - **Pinch** with two fingers or use scroll wheel (desktop): Zoom in/out
   - Tap buttons in viewer header for Reset view or toggle Auto-Rotate
9. Close viewer with X or swipe down on modal (or Esc on keyboard).

**Tip**: For the absolute best experience with very high-resolution stitched panos (some Air 3S Sphere outputs can be 18k–50k wide), consider resizing them to ~8k–12k width in the Photos app or Lightroom before importing. WebGL on iPhone has texture size limits.

## Detection Logic (transparent)
- Loads image → checks natural aspect ratio (width ÷ height).
- **360° Sphere**: ratio between ~1.85 and ~2.15 → marked as true equirectangular 360°.
- Wider or narrower → still importable but flagged as panoramic.
- You can switch between "360° Only" and "All Imported" views.

## Customization & Next Steps
- Want EXIF date/camera info? We can add a small EXIF parser later.
- Want to persist photos across sessions (IndexedDB + thumbnails)? Easy upgrade.
- Want native iOS app later (with full Photo library scan via PhotoKit)? We can discuss Capacitor + EAS or find a friend with Mac for one-time build.
- Add hotspots, export views, or integrate with your drone business site? Just say the word.

## Tech Stack (for the curious)
- Vanilla HTML + Tailwind CSS (CDN)
- Pannellum (lightweight 360° WebGL viewer)
- Progressive Web App manifest
- Zero dependencies to install, zero backend

Built specifically for you and your DJI Air 3S workflow. Enjoy the views! 

If anything breaks or you want features (e.g. gyro support toggle, batch delete, search by date), just paste the error or describe and I'll iterate instantly.

— Grok (June 2026)