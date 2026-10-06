# Saved library

Air360 keeps imported photos in the browser's IndexedDB, so they come back on the next visit. The header shows a storage pill with the photo count, and the stats line under the controls counts photos and 360° photos. Both refresh on every change. A user can delete one photo, clear the on-screen list for this visit with "Clear Session", or erase every saved photo with "Clear Data".

## Sub-features

- `library-restore` brings saved photos back after a reload or a new browser session.
- `library-pill` shows `N photos • ~K KB thumbnails` in the header at 768 px or wider, and just `N photos` on one line below that.
- `library-stats` shows `N photos • M 360°` under the controls and hides it when the list is empty.
- `library-delete` removes one photo from the grid and from storage after a confirm prompt.
- `library-clear-session` empties the grid after a confirm prompt but keeps storage, so a reload brings the photos back.
- `library-clear-data` erases storage after a confirm prompt and shows `All persisted data cleared`.

## How to get to it (user POV)

- Reload the page or reopen the app later.
- Read the pill in the header, left of "Clear Data", and the stats line above the grid.
- Choose the × at the top left of a card's thumbnail. With a mouse it appears when you hover the card. On a touch screen it is always shown.
- Choose "Clear Session" at the end of the controls row.
- Choose "Clear Data" in the header. Below 640 px it is a trash icon, still named "Clear Data".

## Driving it with drive.sh

Preconditions:

- The baseline preconditions in `README.md` hold.
- The viewport is the default 1280x800, so the pill shows the thumbnail size.

- **Restore on reload.** Run `$S/drive.sh --name saved-library "goto /360/" "import sphere-2to1.jpg wide-4to1.jpg" "expect-text 'Added 2 photos'" "idb-count 2" "reload" "expect-text sphere-2to1.jpg" "expect-text '2 photos • ~'" "expect-text '2 photos • 1 360°'" ...` with the steps below appended. The sphere card, the pill, and the stats line return after reload.
- **Clear Session.** Steps `"dialogs accept"`, `"click button 'Clear Session'"`, `"expect-text 'No 360° photos yet'"`, `"idb-count 2"`, `"reload"`, `"expect-text sphere-2to1.jpg"`. The grid empties, storage keeps both records, and reload restores them.
- **Delete one.** Steps `"click button All"`, `"hover '.photo-card:has-text(\"wide-4to1.jpg\")'"`, `"expect-style '.photo-card:has-text(\"wide-4to1.jpg\") button' opacity 1"`, `"card wide-4to1.jpg button ×"`, `"expect-no-text wide-4to1.jpg"`, `"idb-count 1"`, `"expect-text '1 photo • 1 360°'"`. The × shows on hover, the stats line drops to one photo without a reload, and `steps.log` records the confirm prompt `Remove this photo from the list?`.
- **Clear Data.** Steps `"click button 'Clear Data'"`, `"expect-text 'All persisted data cleared'"`, `"idb-count 0"`, `"expect-text 'No photos yet'"`, `"expect-no-text '1 360°'"`, `"reload"`, `"expect-text 'No 360° photos yet'"`. The All view's empty title shows and the stats line hides.
- **Phone width.** Run `$S/drive.sh --name library-phone --viewport 402x874 "goto /360/" "import sphere-2to1.jpg wide-4to1.jpg photo-4to3.jpg" "expect-text 'Added 3 photos'" "expect-text '3 photos • 1 360°'" "dialogs accept" "click button 'Clear Data'" "expect-text 'All persisted data cleared'" "idb-count 0"`. Screenshot the grid after the toast has gone (`"sleep 3500"`): the pill reads `3 photos` on one line next to the trash icon.
- **New browser session.** Two calls sharing a profile. Run `$S/drive.sh --name library-session-1 --profile lib "goto /360/" "import sphere-2to1.jpg" "expect-text 'Added 1 photo'" "idb-count 1"`, then `$S/drive.sh --name library-session-2 --profile lib "goto /360/" "expect-text sphere-2to1.jpg" "idb-count 1" "screenshot restored"`. The second browser launch shows the photo with no import.
- **Cancel keeps data.** Run `$S/drive.sh --name library-cancel "goto /360/" "import sphere-2to1.jpg" "expect-text 'Added 1 photo'" "click button 'Clear Data'" "idb-count 1" "expect-text sphere-2to1.jpg"`. Without `dialogs accept` the prompt is cancelled and nothing changes.
- **Proof.** `steps.log` lists each confirm prompt and answer, and `idb-*.json` shows the record count after each change.

## Gotchas

- The card's × is transparent until the card is hovered, but Playwright's `card ... button ×` clicks it either way. To prove it is visible, `hover` the card and `expect-style ... opacity 1` as above. The headless browser has a mouse, so the always-on touch style is not exercised.
- The toasts also have `button "×"`. Always scope deletes with `card FILENAME button ×`.
- With zero photos, the header pill still shows `0 photos` at 640 px or wider, because `sm:flex` overrides the `hidden` class. Below 640 px it is hidden until there is a photo.
- The stats line keeps its last text while hidden. Assert it with `expect-no-text`, which only counts visible elements.
- Without `dialogs accept`, every Clear and delete is cancelled silently. Check `steps.log` for the dialog lines.
