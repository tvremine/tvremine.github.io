#!/usr/bin/env python3
"""Write the JPEG fixtures the import flow uses into DIR.

Usage: make-fixtures.py DIR

  sphere-2to1.jpg  4096x2048, ratio 2.00, EXIF DateTimeOriginal 2026:06:14 10:30:00, Make DJI.
                   Air360 detects it as 360 and labels it "360° SPHERE".
  wide-4to1.jpg    4000x1000, ratio 4.00. Labelled "PANORAMA", hidden in "360° Only".
  photo-4to3.jpg   1600x1200, ratio 1.33. Also labelled "PANORAMA" (the app has no third label).
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def grid_image(w, h, label, hue):
    img = Image.new("RGB", (w, h))
    px = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        px.line([(0, y), (w, y)], fill=(int(hue[0] * (1 - t)), int(hue[1] * (1 - t) + 40 * t), int(hue[2] * (1 - t) + 90 * t)))
    step = max(w // 16, 1)
    for x in range(0, w, step):
        px.line([(x, 0), (x, h)], fill=(255, 255, 255), width=3)
    for y in range(0, h, step):
        px.line([(0, y), (w, y)], fill=(255, 255, 255), width=3)
    font = ImageFont.load_default(size=max(h // 16, 12))
    # Pannellum puts the image's horizontal center at yaw 0, so "yaw 0°" is what Reset shows.
    for k in (-2, -1, 0, 1):
        px.text((w // 2 + k * w // 4, h // 2), f"{label} yaw {k * 90}°", fill=(255, 230, 0), font=font, anchor="mm")
    return img


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)

    sphere = grid_image(4096, 2048, "SPHERE", (14, 165, 233))
    exif = Image.Exif()
    exif[0x010F] = "DJI"  # Make
    exif.get_ifd(0x8769)[0x9003] = "2026:06:14 10:30:00"  # DateTimeOriginal
    sphere.save(out / "sphere-2to1.jpg", quality=85, exif=exif)

    grid_image(4000, 1000, "WIDE", (234, 179, 8)).save(out / "wide-4to1.jpg", quality=85)
    grid_image(1600, 1200, "PHOTO", (100, 116, 139)).save(out / "photo-4to3.jpg", quality=85)

    for p in sorted(out.glob("*.jpg")):
        print(p)


if __name__ == "__main__":
    main()
