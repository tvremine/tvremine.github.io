# Filter and search

Above the photo grid, the "360° Only" and "All" buttons choose whether non-360 photos show, and a search box narrows the grid to filenames containing the typed text. When nothing matches, the empty state appears.

## Sub-features

- `filter-360` shows only `360° SPHERE` photos. This is the default view.
- `filter-all` shows every imported photo.
- `search-name` keeps cards whose filename contains the query, case-insensitive.
- `search-empty` shows the empty state when nothing matches.
- `search-clear` restores the full list for the current view when the query is emptied.
- `search-date` is meant to match capture dates but never matches at commit 6b75762 (see Gotchas).

## How to get to it (user POV)

- Choose "360° Only" or "All" in the toggle to the right of the search box.
- Type in the box labelled "Search filenames or dates...". Results update on every keystroke.

## Driving it with drive.sh

Preconditions:

- The baseline preconditions in `README.md` hold.
- Each call imports all three fixtures first.

- **Default view.** Run `$S/drive.sh --name filter-and-search "goto /" "import sphere-2to1.jpg wide-4to1.jpg photo-4to3.jpg" "expect-text 'Added 3 photos'" "expect-count-text .jpg 1" "expect-no-text wide-4to1.jpg" ...` with the steps below appended. Only `sphere-2to1.jpg` shows.
- **All.** Steps `"click button All"`, `"expect-count-text .jpg 3"`. All three cards show.
- **Name match.** Steps `"fill textbox 'Search filenames or dates...' WIDE"`, `"expect-text wide-4to1.jpg"`, `"expect-no-text sphere-2to1.jpg"`. Matching ignores case.
- **No match.** Steps `"fill textbox 'Search filenames or dates...' volcano"`, `"expect-text 'No 360° photos yet'"`, `"expect-count-text .jpg 0"`.
- **Clear.** Steps `"fill textbox 'Search filenames or dates...' ''"`, `"expect-count-text .jpg 3"`.
- **Back to 360° Only.** Steps `"click button '360° Only'"`, `"expect-count-text .jpg 1"`.
- **Proof.** Steps `"fill textbox 'Search filenames or dates...' sphere"`, `"aria search-sphere"`, `"screenshot search-sphere"`. The artifacts show the query and the single sphere card.

## Gotchas

- The empty state always says "No 360° photos yet", even in the All view with a search that matches nothing.
- Date search compares the query with `captureDate`, which is always null because the EXIF date parser fails (see `import-photos.md`). `6/14/2026` matches nothing, and the dates shown on cards (file modified dates) are not searchable either.
- The toggle's selected state is only a background color, with no `aria-pressed`. Assert the visible cards, not the button.
- `expect-count-text .jpg N` counts visible elements whose text contains `.jpg`. Keep fixture names ending in `.jpg`.
