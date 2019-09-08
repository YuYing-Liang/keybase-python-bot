from itertools import combinations
from requests import *
import json
from bs4 import BeautifulSoup

def rSearch(SearchTerms, noComb):
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
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = get("http://www.reddit.com/search.json?q={}&type=link".format(sPhrase), headers=headers)
        jsonBody = json.loads(r.text)
        children = jsonBody["data"]["children"]
        for child in children:
            url = "reddit.com"+child["data"]["permalink"]

            keywords = sPhrase.split(" AND ")
            inText = 1
            for word in keywords:
                if inText == 0:
                    break
                if word not in url:
                    inText = 0
            if inText == 1:
                urlList += [url]
    return(urlList)