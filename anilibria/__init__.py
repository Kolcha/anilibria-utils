import re
import lxml.html
import requests

_link_re = re.compile(r"^https://www\.anilibria\.tv/release/[\w-]+\.html$")


def match_link(link: str) -> bool:
    return _link_re.match(link) is not None


def _get_hevc_torrents(content: bytes) -> list[str]:
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


def _get_torrent_links(content: bytes, prefer_hevc: bool = False) -> list[str]:
    if prefer_hevc:
        links = _get_hevc_torrents(content)
        if links:
            return links

    tree = lxml.html.fromstring(content)
    nodes = tree.xpath('//div[@class="download-torrent"]/table/tr/td/a')
    return ['https://www.anilibria.tv' + n.get('href') for n in nodes]


def _download_torrent_file(link: str, session: requests.Session) -> tuple[str, bytes]:
    resp = session.get(link)
    filename = resp.headers['Content-Disposition'].split('filename=')[1].strip('"')
    return filename, resp.content


def download_torrents(link: str, session: requests.Session = None, prefer_hevc: bool = False) -> list[tuple[str, bytes]]:
    if not session:
        session = requests.Session()
    resp = session.get(link)
    if resp.status_code != 200:
        return []
    torrent_links = _get_torrent_links(resp.content, prefer_hevc)
    return [_download_torrent_file(t, session) for t in torrent_links]
