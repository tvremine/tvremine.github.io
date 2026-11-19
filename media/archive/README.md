# Archived photos

Replaced images live here so a page can be put back. Each file is dated (`name-YYYY-MM-DD`). Nothing in this folder is linked from the site.

## hero-2026-11-18.jpg

Homepage hero (`index.html`, shown at `/media/hero.jpg`) and the Work gallery frame that used the same file. Blue-hour skyline over a river. Replaced on 2026-11-19 with a night aerial of downtown Indianapolis.

## How to revert

Move the dated file back to the path the page used, then restore the alt text and any caption from that change. For this hero:

```bash
git mv media/archive/hero-2026-11-18.jpg media/hero.jpg
```

Set the homepage image alt back to “Downtown skyline at blue hour over a river.” Do not add an image or link that points at `media/archive/`.
