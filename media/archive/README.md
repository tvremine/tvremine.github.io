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

Do not add an image or link that points at `media/archive/`.
