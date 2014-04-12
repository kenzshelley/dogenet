html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
from bs4 import BeautifulSoup
import random
import sys

def anchorsToRickRoll(document, probability):
    soup = BeautifulSoup(document)
    links = soup.find_all('a')
    for anchor in links:
        randomnum = random.randint(1,100)
        if randomnum < probability * 100:
            anchor['href'] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    return soup.prettify()

def redditPhonyArticle(document):
    soup = BeautifulSoup(document)
    divider = soup.find("div", {"class" : "clearleft"})
    for post in soup.find_all("div"):
        postclasses = post.get("class")
        if type(postclasses) is list:
            if 'thing' in postclasses and 'link' in postclasses:
                article = post        
    siteTable = soup.find("div", {"id":"siteTable"})
    siteTable.insert(0, BeautifulSoup(str(divider)))
    siteTable.insert(0, BeautifulSoup(str(article)))

    return soup.prettify()
if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    out = open("output.html", 'w')
    output = redditPhonyArticle(f.read())
    out.write(output.encode('utf-8'))

hack = redditPhonyArticle
