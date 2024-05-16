import re
from dataclasses import dataclass, field, InitVar, asdict

import lxml.html
import lxml.etree

from .api.base import create_key
from .band import BandLink
from .album import AlbumLink
from .genre import Subgenres


@dataclass
class LabelRosterMember:
    metallum_id: int
    band: BandLink
    subgenres: Subgenres
    country_of_origin: str


@dataclass
class LabelRoster:
    current: list[LabelRosterMember]
    past: list[LabelRosterMember]


@dataclass
class LabelLink:
    name: str = field(init=False)
    link: str = field(init=False)

    def __init__(self, html: str):
        html_anchor = lxml.html.fragment_fromstring(html)
        self.name = html_anchor.text
        self.link = html_anchor.attrib['href']


@dataclass
class LabelRelease:
    band: BandLink
    album: AlbumLink
    release_type: str
    year_str: InitVar[str]
    catalog: str
    media_format: str
    description: str

    year: int = field(init=False)

    def __post_init__(self, year: str):
        self.year = int(year)



@dataclass
class LabelExternalLink:
    """ An HTML anchor tag pointing to a label's profile outside of metal-archives.com """

    name: str
    url: str




@dataclass
class LabelExternalLinks:
    """ A collection of profiles pertaining to a single band, defined by metallum_id """

    metallum_id: int
    html: InitVar[bytes]
    links: list = field(init=False)

    def __post_init__(self, links_html: bytes):
        links_document = lxml.html.document_fromstring(links_html)
        anchors: list = links_document.xpath('//table[@id = "linksTablemain"]//td/a')
        
        links = list()
        for link in anchors:
            try:
                links.append(LabelExternalLink(link.text.strip(), link.attrib['href']))
            except AttributeError:
                alt_name = link.attrib['title'].replace('Go to:', '').strip()
                links.append(LabelExternalLink(alt_name, link.attrib['href']))
        
        self.links = links


@dataclass
class Label:
    label: LabelLink
    status: str
    has_shop: bool

    specialisation: str | None
    country: str | None
    website: str | None


@dataclass(frozen=True)
class LabelDescription:
    """ Additional information pertaining to a unique label """
    address: str = field(kw_only=True)
    country: str = field(kw_only=True)
    phone_number: str = field(kw_only=True)
    status: str = field(kw_only=True)
    styles_and_specialties: str = field(kw_only=True)
    founding_date: str = field(kw_only=True)
    online_shopping: str = field(kw_only=True)


@dataclass
class LabelProfile:
    url: str
    html: InitVar[bytes]

    name: str = field(init=False)
    metallum_id: int = field(init=False)
    label_key: str = field(init=False)
    description: LabelDescription = field(init=False)

    def __post_init__(self, profile_html: bytes):
        profile_document = lxml.html.fromstring(profile_html)

        if isinstance(profile_document, lxml.etree.ElementBase):
            self.name = name = profile_document.xpath('//h1[@class="label_name"]/text()[1]').pop()
            self.metallum_id = metallum_id = int(self.url.split('/')[-1])
            self.label_key = create_key(metallum_id, name)

            description_titles = self._parse_description_titles(profile_document)
            description_details = self._parse_description_details(profile_document)
            self.description = self._parse_description(description_titles, description_details)

    @staticmethod
    def _parse_description_titles(profile_document: lxml.etree.ElementBase) -> list[str]:
        desc_titles_xpath = '//div[@id="label_info"]/dl/dt//text()'
        desc_titles = profile_document.xpath(desc_titles_xpath)
        desc_titles = [re.sub(r'\/', ' and ', title) for title in desc_titles]
        desc_titles = [re.sub(r'[^\w\s]+', '', title) for title in desc_titles]
        desc_titles = [re.sub(r'\s+', '_', title.strip()).lower() for title in desc_titles]
        return desc_titles

    @staticmethod
    def _parse_description_details(profile_document: lxml.etree.ElementBase) -> list[str]:
        desc_detail_xpath = '//div[@id="label_info"]/dl/dt/following-sibling::dd'
        desc_detail = profile_document.xpath(desc_detail_xpath)
        desc_detail = [node.xpath('./text()|./a/text()|./span/text()') for node in desc_detail]
        desc_detail = [', '.join(filter(lambda n: n != '', map(str.strip, text))) for text in desc_detail]
        desc_detail = ['Unknown' if detail == 'N/A' else detail for detail in desc_detail]

        return desc_detail

    @staticmethod
    def _parse_description(description_titles, description_details) -> LabelDescription:
        description = {dt: dd for dt, dd in zip(description_titles, description_details)}
        return LabelDescription(**description)

    def to_dict(self):
        return asdict(self)


@dataclass
class LabelContainer:
    profile: LabelProfile

    roster_current: InitVar[list[LabelRosterMember]]
    roster_past: InitVar[list[LabelRosterMember]]

    releases: list[LabelRelease]
    links: LabelExternalLinks

    roster: LabelRoster = field(init=False)

    def __post_init__(self, roster_current: list[LabelRosterMember], 
                      roster_past: list[LabelRosterMember]):
        
        self.roster = LabelRoster(roster_current, roster_past)
