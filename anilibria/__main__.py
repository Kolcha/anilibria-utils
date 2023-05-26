"""
Simple tool to download torrents from www.anilibria.tv
"""

import argparse
import pathlib

from . import match_link, download_torrents

parser = argparse.ArgumentParser(prog='anilibria', description=__doc__)
parser.add_argument('urls', metavar='url', type=str, nargs='+',
                    help='page URL to download torrents from')
parser.add_argument('-d', '--dst', type=str,
                    help='torrents destination path', default='')
parser.add_argument('--hevc', action='store_true',
                    help='prefer HEVC torrents if available')

args = parser.parse_args()

dst_dir = pathlib.Path(args.dst)
dst_dir.mkdir(parents=True, exist_ok=True)

for url in args.urls:
    if not match_link(url):
        print(f'unsupported link, ignoring: {url}')
        continue
    for filename, data in download_torrents(url, prefer_hevc=args.hevc):
        print(f'downloaded torrent: {filename}')
        (dst_dir / filename).write_bytes(data)
