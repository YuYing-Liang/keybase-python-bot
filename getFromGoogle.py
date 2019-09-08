from itertools import combinations
from requests import *
from bs4 import BeautifulSoup

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
        r = get("https://www.google.com/search?q={}".format(sPhrase)).content
        s = BeautifulSoup(r, 'lxml')
        s.prettify()
        links = s.find_all("a")
        for link in links:
            pureLink = link.attrs['href']
            if pureLink[:7] == "/url?q=":
                pureLink = pureLink[7:]
            if pureLink[:8] == "https://" or pureLink[:7] == "http://":
                keywords = sPhrase.split(" AND ")
                inText = 1
                for word in keywords:
                    if inText == 0:
                        break
                    if word not in link.text:
                        inText = 0
                if inText == 1:
                    urlList += [pureLink]
    return(urlList)