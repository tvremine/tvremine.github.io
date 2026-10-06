# Import photos

A user picks photos from their device with the "Import Photos" button. Air360 measures each photo, labels 2:1 photos (ratio 1.82 to 2.22) as `360° SPHERE` and everything else as `PANORAMA`, shows a toast with the counts, and saves the full image to IndexedDB.

## Sub-features

- `import-pick` opens the file chooser from the "Import Photos" button and accepts several files at once.
- `import-detect` labels the 2:1 photo `360° SPHERE` and the others `PANORAMA`, with size and ratio on each card.
- `import-toast` shows `Added N photos • M detected as 360°`.
- `import-store` writes one IndexedDB record per photo, with the full image blob.

## How to get to it (user POV)

- Choose the blue "Import Photos" button under the heading. This is the only way in. The page has no drag and drop.

## Driving it with drive.sh

Preconditions:

- The baseline preconditions in `README.md` hold.
- The browser context is fresh (no `--profile`), so the library starts empty.

- **Empty start.** Open the app. Run `$S/drive.sh --name import-photos "goto /" "expect-text 'No 360° photos yet'" "idb-count 0" "aria before" "screenshot before" ...` with the steps below appended to the same call. The empty state shows and the store has no records.
- **Pick photos.** Choose "Import Photos" and select all three fixtures. Step `"import sphere-2to1.jpg wide-4to1.jpg photo-4to3.jpg"`. The toast `Added 3 photos • 1 detected as 360°` appears: step `"expect-text 'Added 3 photos • 1 detected as 360°'"`.
- **360° label.** The default "360° Only" view shows just the sphere. Steps `"expect-count-text '360° SPHERE' 1"`, `"expect-text 4096×2048"`, `"expect-text 2.00:1"`, `"expect-no-text wide-4to1.jpg"`.
- **Other labels.** Switch to All. Steps `"click button All"`, `"expect-count-text PANORAMA 2"`, `"expect-text 4000×1000"`, `"expect-text 1600×1200"`.
- **Stored records.** Steps `"idb-count 3"` and `"idb"`. `idb-*.json` lists three records, `is360` true only for `sphere-2to1.jpg`, each with `imageBlobBytes` equal to the fixture's file size.
- **Proof.** Steps `"aria after-import"` and `"screenshot after-import"`. The artifacts show all three cards with their labels and the Air360 header.

## Gotchas

- Run `idb` only after the toast appears. The records are written after the file chooser closes.
- The default view is "360° Only", so non-360 imports look missing until you choose All.
- There is no third label. A 4:3 photo is labelled `PANORAMA` too.
- The card date is the file's modified date, not the EXIF date. The app's EXIF date parser turns `10:30:00` into `10-30-00` and gets an invalid date, so `captureDate` is always null at commit 6b75762.
- The stats line under the controls (`#statsBar`) updates only on page load. It stays hidden after an import until you reload.
- The `360° SPHERE` badge has no green background. Its CSS class `.360-badge` starts with a digit, which is not a valid selector, so the rule never applies. Assert the text, not the color.
- The toasts `Processing N photos...` and `Added ...` disappear after 1.8 and 3.2 seconds. Assert them right after the import step.
