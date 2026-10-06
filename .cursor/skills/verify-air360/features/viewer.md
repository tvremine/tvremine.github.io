# 360° viewer

Choosing a photo card opens a full-screen dialog with the photo name, its size, ratio, date, and camera make, and a Pannellum view of the panorama. The user can drag to look around, reset the view, toggle auto-rotation, and close the dialog.

## Sub-features

- `viewer-open` opens the dialog from a photo card and renders the panorama.
- `viewer-drag` turns the view when the user drags across it.
- `viewer-reset` animates back to yaw 0, pitch 0.
- `viewer-autorotate` starts and stops continuous rotation.
- `viewer-close` closes from the close button, the Escape key, and a click on the dark backdrop.

## How to get to it (user POV)

- Import a photo, then choose its card.
- Inside the dialog, use the Reset and Auto Rotate buttons in the header, or drag across the panorama.
- Close with the arrow button at the top right, the Escape key, or a click outside the dialog.

## Driving it with drive.sh

Preconditions:

- The baseline preconditions in `README.md` hold.
- Every call passes `--viewport 402x874`. At 640 px wide or more the panorama area has zero height (see Gotchas).

- **Open.** Import the sphere and choose its card. Run `$S/drive.sh --name viewer --viewport 402x874 "goto /" "import sphere-2to1.jpg" "click-text sphere-2to1.jpg" "expect-css '#viewer canvas'" "expect-text 'Powered by Pannellum'" "sleep 1000" "screenshot open" "aria open" ...` with the steps below appended. The canvas has a non-zero size and the screenshot shows `SPHERE yaw 0°` near the middle.
- **Drag.** Drag left across the panorama. Steps `"drag '#viewer' -250 0"`, `"sleep 800"`, `"screenshot dragged"`. `SPHERE yaw 0°` has moved off center.
- **Reset.** Choose Reset. Steps `"click button 'Reset view'"`, `"sleep 900"`, `"screenshot reset"`. `SPHERE yaw 0°` is back near the middle.
- **Auto Rotate.** Choose the Auto Rotate button, then choose it again to stop. Steps `"click-css '#autoRotateBtn'"`, `"expect-redraw '#viewer' 1500"`, `"click-css '#autoRotateBtn'"`. The panorama moves between the two captures.
- **Close with Escape.** Steps `"press Escape"` and `"expect-no-text 'Powered by Pannellum'"`. The dialog is gone and the card grid shows.
- **Close with the button.** Steps `"click-text sphere-2to1.jpg"`, `"click-css '#viewerModal button[onclick=\"closeViewer()\"]'"`, `"expect-no-text 'Powered by Pannellum'"`.
- **Close with the backdrop.** Steps `"click-text sphere-2to1.jpg"`, `"expect-css '#viewer canvas'"`, `"click-at 4 4"`, `"expect-no-text 'Powered by Pannellum'"`. The point (4, 4) is on the dark backdrop above the dialog at 402x874.
- **Proof.** Keep `open.png`, `dragged.png`, and `reset.png` together. The yaw labels show the view moved and came back.

## Gotchas

- At 640 px wide or more, including an iPhone in landscape (844x390), `#viewer` collapses to zero height and the dialog shows only a black strip. `expect-css '#viewer canvas'` fails there. That is a real app bug at commit 6b75762, not a harness problem.
- Below 640 px the Auto Rotate and Reset labels are hidden. Reset keeps the name "Reset view" from its `title`, while Auto Rotate has no name, hence `#autoRotateBtn`.
- The Auto Rotate label changes to "Stop" only at 640 px or wider, where the panorama does not render. At phone width, prove rotation with `expect-redraw`.
- The close button draws an arrow, not an X, and has no accessible name at any width.
- Pannellum loads the image after the dialog opens. Wait for `#viewer canvas` before taking screenshots.
