# -*- coding: utf-8 -*-

'''
Measure the size of a website based on the number of URLs within an XML
sitemap. Sitemaps are discovered by following best practices for xml sitemap
declaration. The robots.txt is checked first. If a sitemap isn't declared,
several guesses are made using the most common xml sitemap naming conventions.

sample usage:
$python sitemap.py 'https://www.exmaple.com/'
'''

__author__ = 'Kevin Tarvin'
import sys
import requests
from bs4 import BeautifulSoup
from reppy.robots import Robots
from urllib.parse import urlparse


def findSitemap(url):
    '''
    Find the location of an xml sitemap

    :param url: a URL in string format
    :param robotUrl: The url string of the robots.txt location
    :param robots: The parsed robots.txt patterns from a website
    :param common_locations: a list of common sitemap naming conventions
    :param discoveredSitemaps: a list to store discovered XML sitemaps
    :param makeUrl: Parse input URL to create sitemap location guesses
    :param guessed_sitemap: Mutate input URL into a guessed location
    :param guess: String of sitemap guess URL
    :param r: guessed sitemap request object
    :param guessPath: String of guessed path
    :param responsePath: string of the returned path from request object
    :return: A list of discovered XML sitemap URLs
    '''
    # Website is using best practices
    robotUrl = Robots.robots_url(url)
    robots = Robots.fetch(robotUrl)
    if len(list(robots.sitemaps)) == 0:
        pass
    else:
        return list(robots.sitemaps)
    # Website is not using best practice so take some guesses
    common_locations = ['/sitemap.xml', '/sitemap_index.xml']
    discoveredSitemaps = []
    while len(common_locations) > 0:
        makeUrl = urlparse(url)
        guessed_sitemap = makeUrl._replace(path=common_locations.pop(0))
        guess = guessed_sitemap.geturl()
        r = requests.get(guess)
        # match guessed path of response to make sure page resolves
        guessPath = urlparse(guess).path
        responsePath = urlparse(r.url).path
        if r.status_code == 200 and guessPath == responsePath:
            discoveredSitemaps.append(guess)
        else:
            pass
        return [] if len(discoveredSitemaps) == 0 else discoveredSitemaps


def countSitemapLinks(sitemap):
    '''
    Count the number of URLs in an XML sitemap

    :param sitemap: a list or string of xml sitemap locations
    :param sitemapList: a list which holds nested sitemaps locations
    :param linksFound: List of integers that are sum of URLs from each sitemap
    :param s: sitemap URL location string
    :param r: request object visiting the sitemap location
    :param soup: BeautifulSoup object structuring sitemap response
    :param urlCount: Integer sum of URLs found in sitemap
    :return: Integer sum of all URLs discovered
    '''
    sitemapList = []
    # Type validation for sitemap variable
    if isinstance(sitemap, list):
        for s in sitemap:
            sitemapList.append(s)
    else:
        sitemapList.append(sitemap)
    linksFound = []
    # Sum links found within known sitemaps
    while len(sitemapList) > 0:
        s = sitemapList.pop(0)
        r = requests.get(s)
        soup = BeautifulSoup(r.text, 'lxml')
        if len(soup.find_all('sitemap')) > 0:
            # Sitemap is an index of nested sitemaps
            for eachSitemap in soup.find_all('sitemap'):
                sitemapList.append(eachSitemap.loc.text)
        else:
            # Sitemap is flat
            urlCount = len(soup.find_all('loc'))
            linksFound.append(urlCount)
    return sum(linksFound)


def main(argv):
    '''
    Count the number of URLs within a website's xml sitemap and print the
    result.

    :param known_sitemaps: a list or string of discovered xml sitemaps
    :param site_size: Integer sum of all URLs within a sitemap
    :return: None
    '''
    known_sitemaps = findSitemap(argv[0])
    site_size = countSitemapLinks(known_sitemaps)
    print('%s URLs discovered while scanning known sitemaps' % (site_size))
    return None


if __name__ == "__main__":
    main(sys.argv[1:])
