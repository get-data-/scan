'''
When Screaming Frog isn't enough and you don't have that Deep Crawl $$$
This will print out an example of data collected from one webpage

example usage:
$python extract.py 'https://wwww.example.com'
'''

__author__ = 'Kevin Tarvin'
import sys
import tldextract
from crawl import Crawler
from onpage import PageParse
from lang import utf8len
from lang import idLanguage
from lang import contentCount


def name(url):
    '''
    Extract the domain from a URL

    :return: a string of the URL's domain
    '''
    return tldextract.extract(url).domain


def webpageData(html, currentUrl, provider, url):
    '''
    Create a dictionary with information extracted from webpage.

    :param html: html rendered from Crawler.getContent()
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
        bi.update(parsed)
        bi.update({'provider': provider})
        bi.update({'website': url})
        bi.update({'title_lang': idLanguage(bi.get('title'))})
        bi.update({'h1_lang': idLanguage(bi.get('h1'))})
        bi.update({'meta_lang': idLanguage(bi.get('metaDesc'))})
        bi.update({'content_count': contentCount(content)})
        bi.update({'page_size_in_bytes': utf8len(content)})
        bi.update({'domain_name': name(url)})
        return bi
    except Exception as e:
        raise SystemExit(e, e.args, 'failed while parsing %s' % (url))


def main(url):
    '''
    Demonstrate extraction working by printing out results from one page

    :param crawler: A Selenium Crawler which renders a webpage
    :param html: the rendered html webpage as a string
    :param bi: A dictionary of extracted informaiton from the html doc
    :return: Dictionary with extracted information
    '''
    crawler = Crawler()
    crawler.startBrowser()
    html = crawler.getContent(url)
    crawler.exit()
    return webpageData(html, url, provider, url)


if __name__ == "__main__":
    try:
        while True:
            provider = input('Please describe the domain being analyze: ')
            if provider not in ('prospect', 'competitor', 'client'):
                print('Limit analysis to a prospect, competitor, or client')
                continue
            else:
                break
        url = sys.argv[1:][0]
        data = main(url)
        print(data)

    except Exception as e:
        print(type(e), e.args, e)
        print(url, type(url))
