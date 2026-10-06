# 360° viewer

Choosing a photo card opens a full-screen dialog with the photo name, its size, ratio, date, and camera make, and a Pannellum view of the panorama. The user can drag to look around, reset the view, toggle auto-rotation, and close the dialog. The panorama fills the dialog at every width, from a portrait phone to a desktop.

## Sub-features

- `viewer-open` opens the dialog from a photo card and renders the panorama.
- `viewer-meta` shows `WIDTH×HEIGHT • RATIO:1 • DATE • MAKE`, where DATE is the EXIF capture date when there is one.
- `viewer-drag` turns the view when the user drags across it.
- `viewer-reset` animates back to yaw 0, pitch 0.
- `viewer-autorotate` starts and stops continuous rotation. The button turns green and its label changes to "Stop" while rotating.
- `viewer-close` closes from the close button, the Escape key, and a click on the dark backdrop. Every close path also turns Auto Rotate off, so the next open starts with the button back to "Auto Rotate".

## How to get to it (user POV)

- Import a photo, then choose its card.
- Inside the dialog, use the Reset and Auto Rotate buttons in the header, or drag across the panorama.
- Close with the arrow button at the top right, the Escape key, or a click outside the dialog.

## Driving it with drive.sh

Preconditions:

- The baseline preconditions in `README.md` hold.
- Run the recipe at the default 1280x800, then again with `--viewport 402x874` (portrait phone) and `--viewport 844x390` (landscape phone). The steps are the same at every width except the Reset button's name: `Reset` at 640 px or wider, `'Reset view'` below that.

- **Open.** Import the sphere and choose its card. Run `$S/drive.sh --name viewer "goto /" "import sphere-2to1.jpg" "expect-text 'Added 1 photo'" "click-text sphere-2to1.jpg" "expect-css '#viewer canvas'" "expect-text 'Powered by Pannellum'" "expect-text '6/14/2026 • DJI'" "sleep 3500" "screenshot open" "aria open" ...` with the steps below appended. The canvas has a non-zero size, and the screenshot shows `SPHERE yaw 0°` near the middle of a panorama that fills the dialog. At 1280x800 `#viewer` is about 590 px tall, and at 844x390 about 215 px.
- **Drag.** Drag left across the panorama. Steps `"drag '#viewer' -250 0"`, `"sleep 800"`, `"screenshot dragged"`. `SPHERE yaw 0°` has moved off center.
- **Reset.** Choose Reset. Steps `"click button Reset"` (or `"click button 'Reset view'"` below 640 px), `"sleep 900"`, `"screenshot reset"`. `SPHERE yaw 0°` is back near the middle.
- **Auto Rotate.** Choose Auto Rotate, then Stop. Steps `"click button 'Auto Rotate'"`, `"expect button Stop"`, `"expect-redraw '#viewer' 1500"`, `"click button Stop"`, `"expect button 'Auto Rotate'"`. The panorama moves between the two captures.
- **Close with Escape.** Steps `"press Escape"` and `"expect-no-text 'Powered by Pannellum'"`. The dialog is gone and the card grid shows.
- **Close with the button.** Steps `"click-text sphere-2to1.jpg"`, `"expect-css '#viewer canvas'"`, `"click button 'Close viewer'"`, `"expect-no-text 'Powered by Pannellum'"`.
- **Close with the backdrop.** Steps `"click-text sphere-2to1.jpg"`, `"expect-css '#viewer canvas'"`, `"click-at 4 4"`, `"expect-no-text 'Powered by Pannellum'"`. The point (4, 4) is on the dark backdrop above the dialog at all three viewports.
- **Close while rotating.** Steps `"click-text sphere-2to1.jpg"`, `"expect-css '#viewer canvas'"`, `"click button 'Auto Rotate'"`, `"expect button Stop"`, `"press Escape"`, `"click-text sphere-2to1.jpg"`, `"expect-css '#viewer canvas'"`, `"expect button 'Auto Rotate'"`, `"press Escape"`. Repeat with `"click button 'Close viewer'"` and `"click-at 4 4"` in place of the first Escape to cover each close path.
- **Proof.** Keep `open.png`, `dragged.png`, and `reset.png` together. The yaw labels show the view moved and came back.

## Gotchas

- Pannellum loads the image after the dialog opens. Wait for `#viewer canvas` before taking screenshots.
- The `Added N photo` toast stays for 3.2 seconds and covers the dialog's footer. Sleep about 3500 ms after the import before a screenshot you want clean.
- The close button draws an arrow, not an X. Its accessible name is "Close viewer".
- Below 640 px the Reset and Auto Rotate labels are hidden. Reset takes its name "Reset view" from its `title`, and Auto Rotate keeps its name ("Auto Rotate" or "Stop") from screen-reader-only text.
- On a landscape phone the dialog is short (about 360 px at 844x390), so the panorama is a wide strip. That is the intended layout, not a collapse. A collapse shows as `expect-css '#viewer canvas'` failing on a zero-height element.
