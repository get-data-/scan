'''
Identify language of a given text string.
'''

__author__ = 'Kevin Tarvin'
from bs4 import BeautifulSoup
from langdetect import detect_langs


def idLanguage(text):
    '''
    Detect language and provide a confidence level

    :param stringToCheck: a string of text to identify
    :param results: detect_langs response as string
    :param formattedResults: string sliced into list
    :param language: iso639-1 value of detected language
    :param confidence: percentage confidence in detection as string
    :return: a dictionary containing language detection values
    '''
    # Handle text arg types
    try:
        if isinstance(text, list):
            stringToCheck = text[0]
        elif isinstance(text, str):
            stringToCheck = text
        else:
            return {'language': '', 'confidence': ''}
        # Type validation check
        if isinstance(stringToCheck, str):
            # Short strings lower detection accuracy
            if len(stringToCheck) < 10:
                return {'language': '', 'confidence': ''}
            else:
                results = detect_langs(stringToCheck)
                formattedResults = str(results[0]).split(':')
                language = formattedResults[0]
                confidence = formattedResults[1]
                return {'language': language, 'confidence': confidence}
        else:
            # Identify dType which failed validation
            print('Detection Result Error: a %s object made it through' % (
                    type(results)))
            print('data object: %s came from: %s' % (results, text))
            return {'language': '', 'confidence': ''}
    except Exception as e:
        # Print exceptions to identify point of failure
        print(e, e.args,
              'failed during language detection of the following: %s' % (text))
        return {'language': '', 'confidence': ''}


def contentCount(html):
    '''
    Get a count of words within the webpage

    :param html: HTML of webpage as string
    :param soup: structured HTML into BeautifulSoup object
    :param text: text strings within soup object
    :param lines: trim whitespace from text
    :param chunks: break up multi-headlines into strings
    :param text: join text into a long string
    :param w: a dictionary of words and their frequency
    :return: integer sum of content in webpage
    '''
    soup = BeautifulSoup(html, 'html5lib')
    # kill all script and style elements
    for script in soup(["script", "style", "noscript"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = ' '.join(chunk for chunk in chunks if chunk)
    w = word_count(text)
    # uniqueContent = len(w.keys())
    return sum(w.values())


def word_count(string):
    '''
    A dictionary with the frequency of content

    :param strings: strings sliced into words
    :param content: Dictionary of words as keys and frequency as values
    :return: A dictionary of words and their frequencies
    '''
    strings = string.lower().split()
    content = {}
    for item in strings:
        content[item] = strings.count(item)
    return content


def utf8len(text):
    '''
    A measure of the html string in utf-8 encoding

    :param text: a string of text
    :return: integer measuring the length of a utf-8 encoded string
    '''
    return len(text.encode('utf-8'))
