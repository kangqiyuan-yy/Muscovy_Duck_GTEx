#!/usr/bin/env python3
"""
Resize + recompress GWAS Manhattan plot JPEGs for web display.

The source images in gwas/jpg_output/ are rendered at ~7778x3334 px
(print resolution for the vector PDFs), which is far larger than the
on-page display width (~1300px on desktop, up to ~2600px accounting
for 2x retina). Serving the full-resolution JPEGs wastes bandwidth and
slows down trait switching.

This script produces a web-optimized copy in gwas/jpg_web/, resized to
a max width suitable for retina desktop display, re-encoded as a
progressive baseline JPEG at a quality that keeps Manhattan-plot detail
(dense scatter points, thin significance line) legible while cutting
file size dramatically. Source files are left untouched.
"""
import os
import sys
from PIL import Image

SRC_DIR = os.path.join(os.path.dirname(__file__), '..', 'gwas', 'jpg_output')
DST_DIR = os.path.join(os.path.dirname(__file__), '..', 'gwas', 'jpg_web')
MAX_WIDTH = 2400
QUALITY = 82


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    files = sorted(f for f in os.listdir(SRC_DIR) if f.lower().endswith('.jpg'))
    if not files:
        print('No JPG files found in', SRC_DIR)
        return 1

    total_src = 0
    total_dst = 0
    for fname in files:
        src_path = os.path.join(SRC_DIR, fname)
        dst_path = os.path.join(DST_DIR, fname)
        src_size = os.path.getsize(src_path)

        with Image.open(src_path) as im:
            im = im.convert('RGB')
            if im.width > MAX_WIDTH:
                new_h = round(im.height * (MAX_WIDTH / im.width))
                im = im.resize((MAX_WIDTH, new_h), Image.LANCZOS)
            im.save(
                dst_path,
                'JPEG',
                quality=QUALITY,
                optimize=True,
                progressive=True,
            )

        dst_size = os.path.getsize(dst_path)
        total_src += src_size
        total_dst += dst_size
        pct = 100 * (1 - dst_size / src_size)
        print(f'{fname}: {src_size/1024:.0f}KB -> {dst_size/1024:.0f}KB ({pct:.0f}% smaller)')

    print('---')
    print(f'Total: {total_src/1024/1024:.1f}MB -> {total_dst/1024/1024:.1f}MB '
          f'({100*(1-total_dst/total_src):.0f}% smaller)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
