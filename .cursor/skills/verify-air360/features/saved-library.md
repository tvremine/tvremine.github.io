# Saved library

Air360 keeps imported photos in the browser's IndexedDB, so they come back on the next visit. The header shows a storage pill with the photo count. A user can delete one photo, clear the on-screen list for this visit with "Clear Session", or erase every saved photo with "Clear Data".

## Sub-features

- `library-restore` brings saved photos back after a reload or a new browser session.
- `library-pill` shows `N photos • ~K KB thumbnails` in the header.
- `library-delete` removes one photo from the grid and from storage after a confirm prompt.
- `library-clear-session` empties the grid after a confirm prompt but keeps storage, so a reload brings the photos back.
- `library-clear-data` erases storage after a confirm prompt and shows `All persisted data cleared`.

## How to get to it (user POV)

- Reload the page or reopen the app later.
- Read the pill in the header, left of "Clear Data" (only at 640 px wide or more).
- Choose the × at the top left of a card's thumbnail.
- Choose "Clear Session" at the end of the controls row.
- Choose "Clear Data" in the header (its label shows only at 640 px wide or more).

## Driving it with drive.sh

Preconditions:

- The baseline preconditions in `README.md` hold.
- The viewport is the default 1280x800 so the pill and the "Clear Data" name exist.

- **Restore on reload.** Run `$S/drive.sh --name saved-library "goto /" "import sphere-2to1.jpg wide-4to1.jpg" "expect-text 'Added 2 photos'" "idb-count 2" "reload" "expect-text sphere-2to1.jpg" "expect-text '2 photos • ~'" ...` with the steps below appended. The sphere card and the pill return after reload.
- **Clear Session.** Steps `"dialogs accept"`, `"click button 'Clear Session'"`, `"expect-text 'No 360° photos yet'"`, `"idb-count 2"`, `"reload"`, `"expect-text sphere-2to1.jpg"`. The grid empties, storage keeps both records, and reload restores them.
- **Delete one.** Steps `"click button All"`, `"card wide-4to1.jpg button ×"`, `"expect-no-text wide-4to1.jpg"`, `"idb-count 1"`. The confirm prompt reads `Remove this photo from the list?` in `steps.log`.
- **Clear Data.** Steps `"click button 'Clear Data'"`, `"expect-text 'All persisted data cleared'"`, `"idb-count 0"`, `"reload"`, `"expect-text 'No 360° photos yet'"`.
- **New browser session.** Two calls sharing a profile. Run `$S/drive.sh --name library-session-1 --profile lib "goto /" "import sphere-2to1.jpg" "expect-text 'Added 1 photo'" "idb-count 1"`, then `$S/drive.sh --name library-session-2 --profile lib "goto /" "expect-text sphere-2to1.jpg" "idb-count 1" "screenshot restored"`. The second browser launch shows the photo with no import.
- **Cancel keeps data.** Run `$S/drive.sh --name library-cancel "goto /" "import sphere-2to1.jpg" "expect-text 'Added 1 photo'" "click button 'Clear Data'" "idb-count 1" "expect-text sphere-2to1.jpg"`. Without `dialogs accept` the prompt is cancelled and nothing changes.
- **Proof.** `steps.log` lists each confirm prompt and answer, and `idb-*.json` shows the record count after each change.

## Gotchas

- The card's × is always transparent (`opacity-0` with no `group` parent), so a sighted user cannot see it. Playwright still clicks it. Report that the control works but is invisible.
- The toasts also have `button "×"`. Always scope deletes with `card FILENAME button ×`.
- With zero photos, the header pill still shows `0 photos • 0 KB` at 640 px or wider, because `sm:flex` overrides the `hidden` class.
- Below 640 px, "Clear Data" has no accessible name. Drive it at the default viewport.
- Without `dialogs accept`, every Clear and delete is cancelled silently. Check `steps.log` for the dialog lines.
