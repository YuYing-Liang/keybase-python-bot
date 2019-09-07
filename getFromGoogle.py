from itertools import combinations
from urllib.parse import urlencode, urlparse, parse_qs

from lxml.html import fromstring
from requests import *

def gSearch(SearchTerms, noComb):
    """
    :param SearchTerms: A list of key search strings
    :param noComb: number of search words per search
    :return: a list of links
    """
    sTuples = list(combinations(SearchTerms, noComb))
    searchList = []
    for sTuple in sTuples:
        searchPhrase = ""
        for words in sTuple[:-1]:
            searchPhrase += words + " AND "
        searchPhrase += sTuple[-1]
        searchList += [searchPhrase]

    urlList = []

    for sPhrase in searchList:
        r = get("https://www.google.com/search?q={}".format(sPhrase)).text
        while 1:
            linkIndex = r.find("<a href=")

            if linkIndex == -1:
                break

            linkEnd = r.find('>', linkIndex+8)

            link = r[linkIndex+9:linkEnd-1]
            if link.find("/url?q=") == 0:
                link = link[7:]
            if link.find("https://") == 0:
                urlList += [link]
            r = r[:linkIndex] + r[linkEnd + 1:]
    return(urlList)