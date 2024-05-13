import base64

from .common import InfoExtractor


class CloudflareStreamIE(InfoExtractor):
    _SUBDOMAIN_RE = r'(?:(?:watch|iframe|customer-\w+)\.)?'
    _DOMAIN_RE = r'(?:cloudflarestream\.com|(?:videodelivery|bytehighway)\.net)'
    _EMBED_RE = rf'embed\.{_DOMAIN_RE}/embed/[^/]+\.js\?.*?\bvideo='
    _ID_RE = r'[\da-f]{32}|[\w-]+\.[\w-]+\.[\w-]+'
    _VALID_URL = rf'https?://(?:{_SUBDOMAIN_RE}{_DOMAIN_RE}/|{_EMBED_RE})(?P<id>{_ID_RE})'
    _EMBED_REGEX = [
        rf'<script[^>]+\bsrc=(["\'])(?P<url>(?:https?:)?//{_EMBED_RE}(?:{_ID_RE}).*?)\1',
        rf'<iframe[^>]+\bsrc=["\'](?P<url>https?://{_SUBDOMAIN_RE}{_DOMAIN_RE}/[\da-f]{{32}})',
    ]
    _TESTS = [{
        'url': 'https://embed.cloudflarestream.com/embed/we4g.fla9.latest.js?video=31c9291ab41fac05471db4e73aa11717',
        'info_dict': {
            'id': '31c9291ab41fac05471db4e73aa11717',
            'ext': 'mp4',
            'title': '31c9291ab41fac05471db4e73aa11717',
            'thumbnail': 'https://videodelivery.net/31c9291ab41fac05471db4e73aa11717/thumbnails/thumbnail.jpg',
        },
        'params': {
            'skip_download': 'm3u8',
        },
    }, {
        'url': 'https://watch.cloudflarestream.com/9df17203414fd1db3e3ed74abbe936c1',
        'only_matching': True,
    }, {
        'url': 'https://cloudflarestream.com/31c9291ab41fac05471db4e73aa11717/manifest/video.mpd',
        'only_matching': True,
    }, {
        'url': 'https://embed.videodelivery.net/embed/r4xu.fla9.latest.js?video=81d80727f3022488598f68d323c1ad5e',
        'only_matching': True,
    }, {
        'url': 'https://customer-aw5py76sw8wyqzmh.cloudflarestream.com/2463f6d3e06fa29710a337f5f5389fd8/iframe',
        'only_matching': True,
    }]
    _WEBPAGE_TESTS = [{
        'url': 'https://upride.cc/incident/shoulder-pass-at-light/',
        'info_dict': {
            'id': 'eaef9dea5159cf968be84241b5cedfe7',
            'ext': 'mp4',
            'title': 'eaef9dea5159cf968be84241b5cedfe7',
            'thumbnail': 'https://videodelivery.net/eaef9dea5159cf968be84241b5cedfe7/thumbnails/thumbnail.jpg',
        },
        'params': {
            'skip_download': 'm3u8',
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        domain = 'bytehighway.net' if 'bytehighway.net/' in url else 'videodelivery.net'
        base_url = 'https://%s/%s/' % (domain, video_id)
        if '.' in video_id:
            video_id = self._parse_json(base64.urlsafe_b64decode(
                video_id.split('.')[1] + '==='), video_id)['sub']
        manifest_base_url = base_url + 'manifest/video.'

        formats, subtitles = self._extract_m3u8_formats_and_subtitles(
            manifest_base_url + 'm3u8', video_id, 'mp4',
            'm3u8_native', m3u8_id='hls', fatal=False)
        fmts, subs = self._extract_mpd_formats_and_subtitles(
            manifest_base_url + 'mpd', video_id, mpd_id='dash', fatal=False)
        formats.extend(fmts)
        self._merge_subtitles(subs, target=subtitles)

        return {
            'id': video_id,
            'title': video_id,
            'thumbnail': base_url + 'thumbnails/thumbnail.jpg',
            'formats': formats,
            'subtitles': subtitles,
        }
