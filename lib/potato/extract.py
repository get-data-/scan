'''
When Screaming Frog isn't enough and you don't have that Deep Crawl $$$
This will print out an example of data collected from one webpage
'''

__author__ = 'Kevin Tarvin'
import tldextract
from urllib.parse import urlparse
from lib.potato.onpage import PageParse
from lib.potato.lang import (
    utf8len,
    idLanguage,
    contentCount)


def websiteDomain(url):
    '''
    Extract the homepage from a URL

    :param page: urlparse object
    :return: url homepage in string format
    '''
    page = urlparse(url)
    homepage = '%s://%s' % (page.scheme, page.netloc)
    return homepage


def name(url):
    '''
    Extract the domain from a URL

    :return: a string of the URL's domain
    '''
    return tldextract.extract(url).domain


def webpageData(html, currentUrl, provider, url):
    '''
    Create a dictionary with information extracted from webpage.

    :param html: html string object
    :param currentUrl: the URL of the rendered HTML
    :param provider: a string label describing relationship to crawled domain
    :param url: The scope of the domain being crawled as a URL string
    :param content: A validation check on html that sets empty HTML if false
    :param bi: business information dictionary
    :param title_lang: the iso 369-1 code desciribing the title's language
    :param h1_lang: the iso 369-1 code desciribing the h1's language
    :param meta_lang: the iso 369-1 code desciribing the meta's language
    :param content_count: An estimate of # of words within the HTML doc
    :param page_size_in_bytes: the size of the html doc in bytes
    :param domain_name: Domain name as string outlining scope of Crawl
    :return: Dictionary with extracted information
    '''
    try:
        if isinstance(html, str) and len(html) > 10:
            content = html
        else:
            content = '<html><head></head><body></body></html>'
        bi = {}
        pageData = PageParse(content, url)
        parsed = pageData.structureData()
        homepage = websiteDomain(url)
        bi.update(parsed)
        bi.update({'provider': provider})
        bi.update({'website': homepage})
        bi.update({'title_lang': idLanguage(bi.get('title'))})
        bi.update({'h1_lang': idLanguage(bi.get('h1'))})
        bi.update({'meta_lang': idLanguage(bi.get('metaDesc'))})
        bi.update({'content_count': contentCount(content)})
        bi.update({'page_size_in_bytes': utf8len(content)})
        bi.update({'domain_name': name(url)})
        return bi
    except Exception as e:
        raise SystemExit(e, e.args, 'failed while parsing %s' % (url))
