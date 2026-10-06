# Air360 verification map

This directory is the maintained source for verifying what an Air360 user can do. Read this index before driving the app, then use the matching feature file as the recipe. All commands assume the repo root as the working directory and `S=.cursor/skills/verify-air360/scripts`.

## Baseline preconditions

- `eval "$($S/start.sh)"` and `export VERIFY_AIR360_RUN=$RUN_ID` have run in this shell.
- `$S/doctor.sh` ends with `doctor: healthy`.
- The fixtures `sphere-2to1.jpg`, `wide-4to1.jpg`, and `photo-4to3.jpg` exist in the run's fixtures directory. `start.sh` creates them.
- Never drive an instance that this run did not start.

## Driving conventions

- Every `drive.sh` call starts with empty IndexedDB unless it passes `--profile`. Import what a recipe needs inside the same call.
- The default viewport is 1280x800. The 360° viewer only renders below 640 px wide, so viewer recipes pass `--viewport 402x874` (iPhone 16 Pro, the device the README targets).
- Prefer ARIA roles and names (`click button "All"`), then visible text (`click-text sphere-2to1.jpg`). Use `click-css` only for the controls `SKILL.md` lists as nameless.
- After `import`, wait for the `Added N photo` toast before any `idb` step. The app saves to IndexedDB after the file chooser closes.
- Every Clear and delete asks `confirm()`. Put `dialogs accept` before the click, or the click is cancelled.

## Proof and skip reporting

- Capture the user action and the resulting state: a snapshot before and after, plus `steps.log`.
- UI proof is an ARIA snapshot and a screenshot that shows the Air360 header or the viewer title.
- Changes to stored photos need an `idb-count` or `idb` read next to the visible result.
- Record the run id, feature ID, and entry point with every artifact.
- If a path cannot be reached, report the attempted step and the unmet precondition. Do not report a skipped entry point as verified through a different one.

## Feature entry contract

Each feature file starts with an H1 title and one paragraph describing the user-visible behavior. It then uses exactly four H2 sections in this order.

1. `Sub-features` lists short IDs with one line for each behavior.
2. `How to get to it (user POV)` lists every user entry point.
3. `Driving it with drive.sh` starts with `Preconditions:` and uses labeled bullets that pair each user action with an exact command and observable result.
4. `Gotchas` lists traps that can waste or invalidate a verification run.

## Features

- [Import photos](./import-photos.md) covers the file chooser, 360° detection, card labels, and the saved records.
- [360° viewer](./viewer.md) covers opening a photo, dragging, Reset view, Auto Rotate, and the three ways to close.
- [Filter and search](./filter-and-search.md) covers the 360° Only and All toggle and the filename search.
- [Saved library](./saved-library.md) covers reload persistence, the storage pill, deleting one photo, Clear Session, and Clear Data.
- [Pages and links](./pages-and-links.md) covers the Waypoint Aerial link, the PWA manifest, and the two archived versions.
