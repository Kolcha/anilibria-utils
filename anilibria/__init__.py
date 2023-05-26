"""
Simple Python module to download torrents from www.anilibria.tv

This module is not a some API client, this is just a web page parser.
So, it can stop working on any website UI change or may be unreliable.
"""

import re
import lxml.html
import requests

_link_re = re.compile(r"^https://www\.anilibria\.tv/release/[\w-]+\.html$")


def match_link(link):
    """Checks if given link can be handled or not.

    :type link: str
    :rtype: bool

    It does only text-based matching, no network calls are made.
    So, any link following the pattern will be considered as supported.
    """
    return _link_re.match(link) is not None


def _get_hevc_torrents(content):
    tree = lxml.html.fromstring(content)
    nodes = tree.xpath('//div[@class="download-torrent"]/table/tr')
    links = []
    for node in nodes:
        is_hevc = False
        tpath = ""
        for child in node:
            class_name = child.get('class')
            if class_name == 'torrentcol1' and 'HEVC' in child.text:
                is_hevc = True
            if class_name == 'torrentcol4':
                tpath = child.xpath('a')[0].get('href')
        if is_hevc:
            links.append(f'https://www.anilibria.tv{tpath}')
    return links


def _get_torrent_links(content, prefer_hevc=False):
    if prefer_hevc:
        links = _get_hevc_torrents(content)
        if links:
            return links

    tree = lxml.html.fromstring(content)
    nodes = tree.xpath('//div[@class="download-torrent"]/table/tr/td/a')
    return ['https://www.anilibria.tv' + n.get('href') for n in nodes]


def _download_torrent_file(link, session):
    resp = session.get(link)
    filename = resp.headers['Content-Disposition'].split('filename=')[1].strip('"')
    return filename, resp.content


def download_torrents(link, prefer_hevc=False):
    """Downloads all .torrent files from the given page.

    This function doesn't write any files, it returns file data instead.

    Basic usage::

        >>> import anilibria
        >>> page_url = 'https://www.anilibria.tv/release/dr-stone.html'
        >>> for filename, data in anilibria.download_torrents(page_url):
        ...     with open(filename, "wb") as f:
        ...         f.write(data)

    :param link: supported page URL. No validation is made,
        in case of unsupported URL behavior is undefined.
    :type link: str
    :param prefer_hevc: (optional) download only HEVC-encoded torrents if any,
        everything otherwise. Set to False by default.
    :returns: an iterator which yields ``('filename', 'file data')`` pairs
    """
    session = requests.Session()
    resp = session.get(link)
    for torrent_link in _get_torrent_links(resp.content, prefer_hevc):
        yield _download_torrent_file(torrent_link, session)
