'''
A class that identifies social media accounts by parsing a webpage's html
'''

__author__ = 'Kevin Tarvin'
import tldextract
from bs4 import BeautifulSoup


class SocialParse(object):
    '''
    This class identifies social media account referenced on a webpage.

    :param socials: Unique strings of popular social media domains
    '''
    socials = [
            '500px',
            'abou.to',
            'about.me',
            'angel.co',
            'aviary',
            'badoo',
            'bandcamp',
            'basecamphq',
            'behance.net',
            'bitbucket.org',
            'bitly',
            'blinklist',
            'blip.fm',
            'blogspot',
            'buzzfeed',
            'cafemom',
            'canva',
            'cash.me',
            'codecademy',
            'codementor.io',
            'coinbase',
            'colourlovers',
            'community.wikia',
            'contently',
            'creativemarket',
            'crokes',
            'dailymotion',
            'designspiration.net',
            'deviantart',
            'disqus',
            'dribbble',
            'ebay',
            'edmodo',
            'ello.co',
            'en.gravatar',
            'etsy',
            'facebook',
            'fanpop',
            'fiverr',
            'flavors.me',
            'flickr',
            'flipboard',
            'fotolog',
            'foursquare',
            'geekli.st',
            'getsatisfaction',
            'github',
            'gogobot',
            'goodreads',
            'hitbox.tv',
            'houzz',
            'hubpages',
            'ifttt',
            'ifunny.co',
            'imgur',
            'instagram',
            'instructables',
            'keybase.io',
            'kongregate',
            'last.fm',
            'livejournal',
            'medium',
            'meetup',
            'mig.me',
            'miiverse.nintendo.net',
            'myspace',
            'newgrounds',
            'news.ycombinator',
            'okcupid',
            'open.spotify',
            'pandora',
            'papaly',
            'pastebin',
            'patreon',
            'paypal.me',
            'photobucket',
            'pinterest',
            'plus.google',
            'postagon',
            'producthunt',
            'reddit',
            'reverbnation',
            'roblox',
            'scribd',
            'seatwish',
            'slack',
            'slideshare.net',
            'snapchat',
            'soundcloud',
            'soup.io',
            'steamcommunity',
            'stream.me',
            'stumbleupon',
            'teamtreehouse',
            'technorati',
            'tracky',
            'trakt.tv',
            'tripadvisor',
            'tripit',
            'tsu.co',
            'tumblr',
            'twitch.tv',
            'twitter',
            'ustream.tv',
            'venmo',
            'viddler',
            'vimeo',
            'vine.co',
            'vk.com',
            'wattpad',
            'webcred.it',
            'wikia',
            'wikipedia.org',
            'wishlistr',
            'wittyprofiles',
            'wordpress',
            'world.kano.me',
            'xfire',
            'yelp',
            'youtube',
            'story.kakao',
            'cafe.naver',
            'blog.naver',
            'weibo',
            'qyer',
            'youku.com',
            'qq.com',
            'weibo.com',
            'ok.ru']

    def __init__(self, html, url):
        '''
        Pass the webpage's HTML as a string which is then turned into a
        BeautifulSoup object.

        :param html: the html string passed into this class
        :param url: the URL associated with the webpage's HTML
        :param soup: The HTML string as a BeautifulSoup Object
        '''
        self.html = html
        self.url = url
        self.soup = BeautifulSoup(html, 'html5lib')

    def gethrefs(self):
        '''
        Find and return all absolute URLs on the page

        :param hrefs: A list of extracted anchor tags with hrefs
        :param data: a list of hrefs extracted from the 'href' soup parsing
        :return: a list of all anchor tag hrefs withing the html doc
        '''
        hrefs = self.soup.find_all('a', href=True)
        data = [link['href'] for link in hrefs if 'http' in link['href']]
        return data

    def getDomain(self, href):
        '''
        Extract the domain name of a URL

        :return: A string extracted from the URL's domain
        '''
        return tldextract.extract(href).domain

    def socialmedia(self):
        '''
        String match unique fragments of known social media domains against
        the URLs extracted from a webpage.

        :param hrefs: a list of hrefs
        :param results: Filter href list against social list to find matches
        :param data: An initialized dictionary where results will be added
        :return: a dictonary of social media links found on a specific URL
        :return type: dictionary - keys = social media name, value = URL
        '''
        hrefs = self.gethrefs()
        results = [href for s in self.socials for href in hrefs if s in href]
        data = {'url': self.url}
        for result in results:
            data.update({self.getDomain(result): result})
        return data
