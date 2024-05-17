 
import re
from datetime import datetime
from dataclasses import dataclass, field, InitVar, asdict

import lxml.etree
import lxml.html

from .band import BandLink
from .genre import Subgenres


class ParseError(Exception):
    ...


def _parse_release_date(release_date) -> str:
    """ Normalizes textual release dates to a datetime object """

    def _try_parse_release_date(release_date: str, date_format: str):
        try:
            return datetime.strptime(release_date, date_format) \
                           .date().strftime('%Y-%m-%d')
        except ValueError:
            return None

    release_date = re.sub(r',', '', release_date)
    release_date = re.sub(r'(\d)st', r'\g<1>', release_date)
    release_date = re.sub(r'(\d)nd', r'\g<1>', release_date)
    release_date = re.sub(r'(\d)rd', r'\g<1>', release_date)
    release_date = re.sub(r'(\d)th', r'\g<1>', release_date)
    release_date = re.sub(r'\s(\d)\s', r' 0\g<1> ', release_date)

    release_date_parsed = _try_parse_release_date(release_date, '%B %d %Y')
    if not release_date_parsed:
        release_date_parsed = _try_parse_release_date(release_date, '%B %Y')
    if not release_date_parsed:
        release_date_parsed = _try_parse_release_date(release_date, '%Y-%m-%d %H:%M:%S')

    if release_date_parsed is None:
        raise ParseError('unable to parse release date')

    return release_date_parsed


@dataclass
class AlbumLink:
    """ The data within an HTML anchor tag pointing to an album page """
    name: str = field(init=False)
    link: str = field(init=False)

    def __init__(self, html: str):
        html_anchor = lxml.html.fragment_fromstring(html)
        self.name = html_anchor.text
        self.link = html_anchor.attrib['href']


@dataclass
class AlbumRelease:    
    band: BandLink
    album: AlbumLink

    release_type: str
    genres: Subgenres
    release_date_display: InitVar[str]
    added_date_display: InitVar[str | None] = field(default=None)

    release_date: str = field(init=False)
    added_date: str | None = field(init=False)

    def __post_init__(self, release_date_display, added_date_display):
        self.release_date = _parse_release_date(release_date_display)

        if added_date_display == 'N/A' or added_date_display is None:
            self.added_date = None
        else:
            added_date = re.sub(r'\/(\d)\/', '/0\1/', added_date_display)
            self.added_date = datetime.strptime(added_date, '%Y-%m-%d %H:%M:%S') \
                                      .strftime('%Y-%m-%dT%H:%M:%SZ')


@dataclass
class AlbumTrackLength:
    """ Numerically defines the length of an album track """
    length_text: InitVar[str]
    hours: int = field(init=False, default=0)
    minutes: int = field(init=False, default=0)
    seconds: int = field(init=False)

    def __post_init__(self, length_text: str):
        split_length_text = length_text.split(':')[::-1]

        self.seconds = int(split_length_text[0])

        try:
            self.minutes = int(split_length_text[1])
            self.hours = int(split_length_text[2])
        except IndexError:
            pass


@dataclass
class AlbumTrack:
    """ A unique track on an album """
    tablerow: InitVar[lxml.etree.ElementBase]

    metallum_id: int = field(init=False)
    number: str = field(init=False)
    title: str = field(init=False)
    length: AlbumTrackLength = field(init=False)
    lyrics: str = field(init=False)

    def __post_init__(self, tablerow: lxml.etree.ElementBase):
        number, title, length, lyrics = tablerow.xpath('./td')
        metallum_id = number.xpath('./a').pop().attrib['name']

        self.metallum_id = int(metallum_id)
        self.title = title.text
        self.number = number.text
        self.length = AlbumTrackLength(length.text)
        self.lyrics = lyrics.text


@dataclass
class AlbumDescription:
    """ Additional information concerning an album """
    release_type: str | None
    release_date: str | None
    catalog_id: str | None
    label: str | None
    media_format: str | None
    version_desc: str | None = field(default=None)
    limitation: str | None = field(default=None)
    reviews: str | None = field(default=None)


@dataclass
class AlbumProfile:
    """ An album profile page """
    url: str
    html: InitVar[bytes]

    name: str = field(init=False)
    metallum_id: int = field(init=False)
    
    band: BandLink = field(init=False)
    tracklist: list[AlbumTrack] = field(init=False)
    description: AlbumDescription = field(init=False)

    def __post_init__(self, profile_html):
        self.metallum_id = int(self.url.split('/')[-1])

        profile_document = lxml.html.document_fromstring(profile_html)

        self.name = profile_document.xpath('.//h1[@class="album_name"]/a/text()').pop()

        band_link = profile_document.xpath('.//h2[@class="band_name"]/a').pop()
        band_link_str = lxml.etree.tostring(band_link).decode('utf-8').split('\n')[0]
        self.band = BandLink(band_link_str)

        album_desc_titles_xpath = '//div[@id="album_info"]/dl/dt/text()'
        album_desc_titles = profile_document.xpath(album_desc_titles_xpath)

        album_desc_detail_xpath = '//div[@id="album_info"]/dl/dd/text()'
        album_desc_detail = profile_document.xpath(album_desc_detail_xpath)

        self.description = self._parse_description(album_desc_titles, album_desc_detail)
        
        album_tracklist_xpath = ('//div[@id="album_tabs_tracklist"]'
                                 '//tr[@class="even" or @class="odd"]')
        album_tracklist = profile_document.xpath(album_tracklist_xpath)
        self.tracklist = list(map(AlbumTrack, album_tracklist))

    @classmethod
    def _parse_description(cls, description_titles, description_details) -> AlbumDescription:
        description = {str(dt).lower(): str(dd).strip() 
                       for dt, dd in zip(description_titles, description_details)}
        
        # scrub non alpha and whitespace
        description = {re.sub(r'[^\w\s]+', '', dt): None if dd == 'N/A' else dd 
                       for dt, dd in description.items()}
        
        # underscores
        description = {re.sub(r'\s+', '_', dt): dd
                       for dt, dd in description.items()}
        
        # scrub invalid key names
        description = {cls._scrub_key_names(dt): dd
                       for dt, dd in description.items()}

        return AlbumDescription(**description)
    
    @staticmethod
    def _scrub_key_names(key: str) -> str:
        if key == 'type':
            return 'release_type'

        if key == 'format':
            return 'media_format'

        return key
    
    @property
    def release_date(self):
        return _parse_release_date(self.description.release_date)
    
    def to_dict(self):
        return asdict(self)
