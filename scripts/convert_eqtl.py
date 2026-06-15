#!/usr/bin/env python3
"""Convert web_eqtl.tsv to pre-sorted web_eqtl.json for faster page load."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, 'data', 'web_eqtl.tsv')
JSON = os.path.join(ROOT, 'data', 'web_eqtl.json')


def main():
    rows = []
    with open(TSV, encoding='utf-8') as f:
        f.readline()  # skip header
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) == 11:
                rows.append(parts)

    rows.sort(key=lambda r: float(r[5]))  # P-value ascending

    with open(JSON, 'w', encoding='utf-8') as f:
        json.dump(rows, f, separators=(',', ':'))

    print('Wrote %d rows to %s (%.1f MB)' % (
        len(rows), JSON, os.path.getsize(JSON) / 1024 / 1024))


if __name__ == '__main__':
    main()
