import cgi
import lxml.html
import re
import requests

_link_re = re.compile(r"^https?:\/\/www\.anilibria\.tv\/release\/[\w-]+\.html?$")


def match_link(link):
    return _link_re.match(link) is not None


def _get_hevc_torrents(content):
    tree = lxml.html.fromstring(content)
    nodes = tree.xpath('//div[@class="download-torrent"]/table/tr')
    links = []
    for n in nodes:
        is_hevc = False
        tpath = ""
        for ch in n:
            cl = ch.get('class')
            if cl == 'torrentcol1' and 'HEVC' in ch.text:
                is_hevc = True
            if cl == 'torrentcol4':
                tpath = ch.xpath('a')[0].get('href')
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


def _get_torrent_file_name(headers):
    _, params = cgi.parse_header(headers['Content-Disposition'])
    return params['filename'].encode('latin1').decode('utf-8')


def _download_torrent_file(link, session):
    r = session.get(link)
    filename = _get_torrent_file_name(r.headers)
    return (filename, r.content)


def download_torrents(link, session=None, prefer_hevc=False):
    if not session:
        session = requests.Session()
    r = session.get(link)
    if r.status_code != 200:
        return []
    torrent_links = _get_torrent_links(r.content, prefer_hevc)
    return [_download_torrent_file(t, session) for t in torrent_links]
