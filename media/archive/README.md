# Archived photos

Replaced images live here so a page can be put back. Each file is dated (`name-YYYY-MM-DD`). Nothing in this folder is linked from the site.

## hero-2026-11-18.jpg

Homepage hero (`index.html`, shown at `/media/hero.jpg`) and the Work gallery frame that used the same file. Blue-hour skyline over a river. Replaced on 2026-11-19 with a night aerial of downtown Indianapolis.

## How to revert

Move the dated file back to the path the page used, then restore the alt text and any caption from that change. For this hero:

```bash
git mv media/archive/hero-2026-11-18.jpg media/hero.jpg
```

Set the homepage image alt back to “Downtown skyline at blue hour over a river.”

## work-river-2026-11-18.jpg

Work page tile “Park bend / White River” (`work/index.html`, `data-item="river"`, shown at `/media/work-river.jpg`). Sunrise aerial of a river curving through a park. Replaced on 2026-11-19 with a fall aerial of the Coffer Dam causeway on Eagle Creek Reservoir, now at `/media/work-eagle-creek.jpg`.

To put that tile back:

```bash
git mv media/archive/work-river-2026-11-18.jpg media/work-river.jpg
```

Point the tile at `/media/work-river.jpg` again. Restore the title “Park bend”, the location “White River”, and the alt text “Sunrise aerial of a river curving through a park.”

## work-neighborhood-2026-11-18.jpg

Work page tile “Tree streets / Perry Township” (`work/index.html`, `data-item="neighborhood"`, shown at `/media/work-neighborhood.jpg`). Golden-hour aerial of a tree-lined neighborhood. Replaced on 2026-11-19 with a golden-hour aerial of a Perry Township subdivision, now at `/media/work-perry-township.jpg`. No other page used this file.

To put that tile back:

```bash
git mv media/archive/work-neighborhood-2026-11-18.jpg media/work-neighborhood.jpg
```

Point the tile at `/media/work-neighborhood.jpg` again. Keep the title “Tree streets” and the location “Perry Township”. Restore the alt text “Golden-hour aerial of a tree-lined neighborhood.”

## Lawn reception tile

The Work page tile “Lawn reception / Central Indiana” (`work/index.html`, `data-item="reception"`) used `/media/events.jpg`. That tile was retired on 2026-11-19 and now shows a ballroom general session at `/media/work-corporate-event.jpg`, titled “Corporate event / JW Marriott.”

`/media/events.jpg` was not removed. It is still the live photo for:

- Homepage service card “Events & production” (`index.html`)
- Homepage selected-work card “Lawn reception / Central Indiana” (`index.html`)
- Services page “Events & production” row (`services/index.html`, `#events`)

To put the Work tile back, point it at `/media/events.jpg` again. Restore the title “Lawn reception”, the location “Central Indiana”, and the alt text “Overhead of an evening outdoor reception.”

Do not add an image or link that points at `media/archive/`.
