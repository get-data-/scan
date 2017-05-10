'''PageParse is a class which extracts information from an html string
and returns structured responses
'''

__author__ = 'Kevin Tarvin'
from bs4 import BeautifulSoup
import json


class PageParse(object):
    '''
    Take a webpage's HTML and extract information from it
    '''

    def __init__(self, html, url):
        '''
        Pass the webpage's HTML as a string which is then turned into a
        BeautifulSoup object

        :param html: an HTML webpage as a string
        :param url: The URL string of the corresponding HTML page
        :param soup: Structuring the html string into a BeautifulSoup object
        :param empty: an Empty HTML string
        :return: None
        '''
        self.html = html
        self.url = url
        try:
            self.soup = BeautifulSoup(html, 'html5lib')
        except Exception as e:
            print(e, e.args, self.html, 'Html error with BeautifulSoup')
            empty = '<html><head></head><body></body></html>'
            self.soup = BeautifulSoup(empty, 'html5lib')

    def hrefs(self):
        '''
        :param linkData: a list anachor tags within a webpage
        :param hrefs: a list of hrefs from the anchor tags in linkData
        :return: list of hrefs from the webpage
        '''
        linkData = self.soup.find_all('a', href=True)
        hrefs = [a['href'] for a in linkData]
        return hrefs

    def title(self):
        '''
        Extract the Title text from a webpage

        :return: the text string extracted from HTML <title> tags
        '''
        try:
            return self.soup.title.text if self.soup.title else ''
        except Exception as e:
            print(e, e.args, 'title')

    def h1(self):
        '''
        Extract H1 text from a webpage and return a list

        :param h1s: A list of h1 tags
        :param h1: a list of text strings extracted from h1 tags
        :return: the text string extracted from HTML <h1> tags
        '''
        try:
            h1s = self.soup.find_all('h1')
            h1 = [x.text for x in h1s]
            return h1 if h1s else ''
        except Exception as e:
            print(e, e.args, 'h1')

    def metaDesc(self):
        '''
        Extract the meta description text from a webpage

        :param desc: a dictionary object of parsed meta description tags
        :return: Text string extracted from HTML <meta> tags or empty string
        '''
        try:
            desc = self.soup.find(attrs={'name': 'Description'})
            if desc is None:
                    desc = self.soup.find(attrs={'name': 'description'})
            return desc.get('content', '') if desc else ''
        except Exception as e:
            print(e, e.args, 'metaDesc')

    def ogDesc(self):
        '''
        Extract the meta og:description text from a webpage

        :param dbDesc: parsed meta og:description tags
        :return: the text string extracted from HTML <meta> tags
        '''
        try:
            fbDesc = self.soup.find('meta',  property='og:Description')
            if fbDesc is None:
                    fbDesc = self.soup.find('meta',  property='og:description')
            # return fbDesc['content'] if fbDesc else ''
            return fbDesc.get('content', '') if fbDesc else ''
        except Exception as e:
            print(e, e.args, 'ogDesc')

    def twitDesc(self):
        '''
        Extract the meta twitter:description text from a webpage

        :param tMeta: a parsed soup object of twitter meta description tags
        :return: Text string extracted from HTML <meta> tags or empty string
        '''
        try:
            tMeta = self.soup.find(attrs={'name': 'twitter:description'})
            if tMeta is None:
                tMeta = self.soup.find(attrs={'name': 'twitter:description'})
            # return tMeta['content'] if tMeta else ''
            return tMeta.get('content', '') if tMeta else ''
        except Exception as e:
            print(e, e.args, 'twitDesc')

    def twitName(self):
        '''
        Extract the Twitter ID associated with the webpage

        :param twittername: Parsed meta twitter name tags
        :return: Twitter username string extracted from HTML
        '''
        try:
            twittername = self.soup.find(attrs={'name': 'Twitter:site'})
            if twittername is None:
                twittername = self.soup.find(attrs={'name': 'twitter:site'})
            try:
                # return twittername['content'] if twittername else ''
                return twittername.get('content', '') if twittername else ''
            except Exception as e:
                return 'Attribute Syntax Error: %s' % (e, e.args, 'twitName')
        except Exception as e:
            print(e, e.args, 'twitName')

    def htmlLang(self):
        '''
        Identify the declared language of the page

        :param language: parsed tags that have lang attribute
        :param l: Extract the iso639-1 value of the declared html language
        :param xmllang: the language value declared in xml rather than html
        :return: string value of html language for a webpage
        '''
        try:
            language = self.soup.find('html', attrs={'lang': True})
            # return language['lang'] if language else ''
            l = language.get('lang', '') if language else ''
            if len(l) == 0:
                xmllang = self.soup.find('html', attrs={'xml:lang': True})
                return xmllang.get('xml:lang', '') if xmllang else ''
            else:
                return language.get('lang', '') if language else ''
        except Exception as e:
            print(e, e.args, 'htmlLang')

    def canoncial(self):
        '''
        Extract the canonical link for the webpage

        :param canon: Parsed list of tags with rel=canonical attribute
        :return: href extracted from the canonical link
        '''
        try:
            canon = self.soup.find('link', rel='canonical')
            # return canon['href'] if canon else ''
            return canon.get('href', '') if canon else ''
        except Exception as e:
            print(e, e.args, 'canoncial')

    def hreflangOnPage(self):
        '''
        Detect the number of hreflang instances on the page

        :param hreflang: List of html elements with an hreflang attribute
        :return: Integer representing the quantity of hreflang tags on page
        '''
        try:
            hreflang = self.soup.find_all('link', hreflang=True)
            return len(hreflang) if hreflang else 0
        except Exception as e:
            print(e, e.args, 'hreflangOnPage')

    def hreflangValues(self):
        '''
        Extract a dictionary of hreflang values and alternate site locs

        :param href: list of link elements with an hreflang attribute
        :param altSites: list of alternate language sites for a given webpage
        :param alt: a dictionary of the iso639-1 value and alternate URL
        :return: List of dictionaries containing alternate versions of webpage
        '''
        try:
            href = self.soup.find_all('link', hreflang=True)
            altSites = []
            for link in href:
                alt = {'hreflang': link['hreflang'], 'loc': link['href']}
                altSites.append(alt)
            return altSites if href else 'None'
        except Exception as e:
            print(e, e.args, 'hreflangValues')

    def missingImgAlt(self):
        '''
        Returns a float which is the percentage of img tags on page which
        have alt text with more than 4 characters

        :param img: list of img elements
        :param alts: list of img elements with alt attribute
        :param hasAlts: list of img tags using alt attributes with content
        :return: Float representing percentage of SEO img tags
        '''
        try:
            img = self.soup.find_all('img')
            alts = self.soup.find_all('img', alt=True)
            hasAlts = [x['alt'] for x in alts if len(x['alt']) > 4]
            return (1 - (len(hasAlts)/len(img))) if len(img) > 0 else 0
        except Exception as e:
            print(e, e.args, 'missingImgAlt')

    def preresolve(self):
        '''
        Returns a list of resources which use the dns-prefetch attribute

        :param preresolved: list of link elements with dns-prefetch attribute
        :param resources: list of hrefs that are preresolved resources
        :return: list of preresolved resources
        '''
        try:
            preresolved = self.soup.find_all('link', rel='dns-prefetch')
            resources = [x['href'] for x in preresolved]
            return resources if preresolved else ''
        except Exception as e:
            print(e, e.args, 'preresolve')

    def preconnect(self):
        '''
        Returns a list of resources using the preconnect attribute

        :param preconnected: list of link elements with preconnect attribute
        :param resources: list of hrefs that are preconnect resources
        :return: list of preconnected resources
        '''
        try:
            preconnected = self.soup.find_all('link', rel='preconnect')
            resources = [x['href'] for x in preconnected]
            return resources if preconnected else ''
        except Exception as e:
            print(e, e.args, 'preconnect')

    def prefetch(self):
        '''
        Returns a list of resources using the prefetch attribute

        :param prefetched: list of link elements with prefetch attribute
        :param resources: list of hrefs that are prefetch resources
        :return: list of prefetched resources
        '''
        try:
            prefetched = self.soup.find_all('link', rel='prefetch')
            resources = [x['href'] for x in prefetched]
            return resources if prefetched else ''
        except Exception as e:
            print(e, e.args, 'prefetch')

    def prerender(self):
        '''
        Returns a list of prerendered attributes

        :param prerendered: list of link elements with prerender attribute
        :param resources: list of hrefs that are prerender resources
        :return: list of prerendered resources
        '''
        try:
            prerendered = self.soup.find_all('link', rel='prerender')
            resources = [x['href'] for x in prerendered]
            return resources if prerendered else ''
        except Exception as e:
            print(e, e.args, 'prerender')

    def microdataAttrs(self):
        '''
        Extracts and returns a list of attributes used in microdata elements on
        page

        :param itemprop: list of elements with an itemprop attribute
        :return: list of microdata elements found on page
        '''
        try:
            itemprops = self.soup.find_all(itemprop=True)
            return [x['itemprop'] for x in itemprops]
        except Exception as e:
            print(e, e.args, 'microdataAttrs')

    def microdataType(self):
        '''
        Extracts and returns a list of the types of schema elements on page

        :param schema: list of elements with itemscope attribute
        :return: list of itemtype values within on page microdata
        '''
        try:
            schema = self.soup.find_all(itemscope=True)
            return [x['itemtype'] for x in schema]
        except Exception as e:
            print(e, e.args, 'microdataType')

    def schemaSyntax(self):
        '''
        This method identifies the syntax of structured data within webpage.
        Currently checks for microdata and JSON-LD

        :param microdata: list of elements with itemprop attribute
        :param isMicro: list of microdata schema elements
        :param jsonld: list elements with ld+json attribute
        :return: string description of implemented schema
        '''
        try:
            microdata = self.soup.find_all(itemprop=True)
            isMicro = [x['itemprop'] for x in microdata]
            jsonld = self.soup.find_all(attrs={'type': 'application/ld+json'})
            if len(isMicro) >= 1:
                return 'Microdata'
            elif len(jsonld) >= 1:
                return 'JSON-LD'
            else:
                return 'None Detected'
        except Exception as e:
            print(e, e.args, 'schemaSyntax')

    def jsonld(self):
        '''
        Identify jsonld element types on webpage

        :param data: a list of json schema found in webpage
        :param jsonld: list of elements with ls+json attribute
        :param jsonldelements: list of parsed json elements as strings
        :param schema: convert strings into JSON objects
        :return: list of json+ld schema found on page
        '''
        try:
            data = []
            jsonld = self.soup.find_all(attrs={'type': 'application/ld+json'})
            jsonldelements = [x.text for x in jsonld]
            # Enemeration for multiple scripts tags on page
            for element in jsonldelements:
                # Type validation to determine if multiple elements present
                schema = json.loads(element)
                if isinstance(schema, list):
                    for obj in schema:
                        data.append(obj.get('@type', ''))
                elif isinstance(schema, dict):
                    data.append(schema.get('@type', ''))
                else:
                    # No idea what this is but capture and figure it out later
                    data.append(schema)
            return data
        except Exception as e:
            print(e, e.args, 'jsonld')

    def structureData(self):
        '''
        A method which outputs a dictionary of values extracted through methods
        contained in this class

        :param data: Extracted information structured into a dictionary
        :return: A dictionary of parsed results
        '''
        data = {'url': self.url,
                'title': self.title(),
                'title_length': len(self.title()),
                'h1': self.h1(),
                'h1_length': len(self.h1()),
                'metaDesc': self.metaDesc(),
                'metaDesc_length': len(self.metaDesc()),
                'ogDesc': self.ogDesc(),
                'ogDesc_length': len(self.ogDesc()),
                'twitDesc': self.twitDesc(),
                'twitDesc_length': len(self.twitDesc()),
                'twitName': self.twitName(),
                'htmlLang': self.htmlLang(),
                'canonical': self.canoncial(),
                'hreflangOnPage': self.hreflangOnPage(),
                'hreflangValues': self.hreflangValues(),
                'missingImgAlts': self.missingImgAlt(),
                'preresolve': self.preresolve(),
                'preresolve_n': len(self.preresolve()),
                'preconnect': self.preconnect(),
                'preconnect_n': len(self.preconnect()),
                'prefetch': self.prefetch(),
                'prefetch_n': len(self.prefetch()),
                'prerender': self.prerender(),
                'prerender_n': len(self.prerender()),
                'schema_syntax': self.schemaSyntax(),
                'microdata_elements': self.microdataType(),
                'microdata_elements_n': len(self.microdataType()),
                'jsonld_elements': self.jsonld(),
                'jsonld_elements_n': len(self.jsonld())
                }
        return data
