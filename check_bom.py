import sys

files = ['src/platforms/netease/crawler.py', 'scripts/run_netease.py']
for f in files:
    with open(f, 'rb') as fp:
        bom = fp.read(3)
        has_bom = bom == b'\xef\xbb\xbf'
        print(f'{f}:', 'ERROR: BOM detected' if has_bom else 'OK: No BOM')