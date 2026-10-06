# Filter and search

Above the photo grid, the "360° Only" and "All" buttons choose whether non-360 photos show. A search box narrows the grid to photos whose filename or EXIF capture date contains the typed text. When nothing matches, the empty state appears, with a title that fits the active view and search.

## Sub-features

- `filter-360` shows only `360° SPHERE` photos. This is the default view.
- `filter-all` shows every imported photo.
- `search-name` keeps cards whose filename contains the query, case-insensitive.
- `search-empty` shows the empty state when nothing matches, titled `No photos match "QUERY"` in All or `No 360° photos match "QUERY"` in 360° Only.
- `search-clear` restores the full list for the current view when the query is emptied.
- `search-date` matches the capture date in the browser's short date format, e.g. `6/14/2026` in en-US.
- `empty-title` says `No photos yet` in All and `No 360° photos yet` in 360° Only when there is nothing to show without a search.

## How to get to it (user POV)

- Choose "360° Only" or "All" in the toggle to the right of the search box.
- Type in the box labelled "Search filenames or dates...". Results update on every keystroke.

## Driving it with drive.sh

Preconditions:

- The baseline preconditions in `README.md` hold.
- Each call imports all three fixtures first.

- **Default view.** Run `$S/drive.sh --name filter-and-search "goto /360/" "import sphere-2to1.jpg wide-4to1.jpg photo-4to3.jpg" "expect-text 'Added 3 photos'" "expect-count-text .jpg 1" "expect-no-text wide-4to1.jpg" ...` with the steps below appended. Only `sphere-2to1.jpg` shows.
- **All.** Steps `"click button All"`, `"expect-count-text .jpg 3"`. All three cards show.
- **Name match.** Steps `"fill textbox 'Search filenames or dates...' WIDE"`, `"expect-text wide-4to1.jpg"`, `"expect-no-text sphere-2to1.jpg"`. Matching ignores case.
- **No match.** Steps `"fill textbox 'Search filenames or dates...' volcano"`, `"expect-text 'No photos match \"volcano\"'"`, `"expect-count-text .jpg 0"`.
- **Clear.** Steps `"fill textbox 'Search filenames or dates...' ''"`, `"expect-count-text .jpg 3"`.
- **Date match.** Steps `"fill textbox 'Search filenames or dates...' 6/14/2026"`, `"expect-count-text .jpg 1"`, `"expect-text sphere-2to1.jpg"`, then `"fill textbox 'Search filenames or dates...' ''"`. Only the sphere has an EXIF date.
- **Back to 360° Only.** Steps `"click button '360° Only'"`, `"expect-count-text .jpg 1"`.
- **Empty titles.** In a separate call, steps `"goto /360/"`, `"click button All"`, `"expect-text 'No photos yet'"`, `"click button '360° Only'"`, `"expect-text 'No 360° photos yet'"`.
- **Proof.** Steps `"fill textbox 'Search filenames or dates...' sphere"`, `"aria search-sphere"`, `"screenshot search-sphere"`. The artifacts show the query and the single sphere card.

## Gotchas

- Date search matches the browser's short date format (`6/14/2026` in en-US), not the `Jun 14` shown on cards. File modified dates are not searchable, so photos without EXIF never match a date.
- The empty state's second line always says to import DJI Sphere panoramas, even after a search that matches nothing. Assert the title.
- The toggle's selected state is only a background color, with no `aria-pressed`. Assert the visible cards, not the button.
- `expect-count-text .jpg N` counts visible elements whose text contains `.jpg`. Keep fixture names ending in `.jpg`.
