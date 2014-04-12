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

    insertionIndex = random.randint(1,10)
    if (insertionIndex%2 == 1):
        insertionIndex = insertionIndex + 1
    article.find("a")['href'] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    article.find_all("div")[6].find("p").find("a").replace_with('I am a nigerian prince with lots of money, AMA!')
    siteTable = soup.find("div", {"id":"siteTable"})
    siteTable.insert(insertionIndex, BeautifulSoup(str(divider)))
    siteTable.insert(insertionIndex + 1, BeautifulSoup(str(article)))

    return soup.prettify()
if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    out = open("output.html", 'w')
    output = redditPhonyArticle(f.read())
    out.write(output.encode('utf-8'))

def hack(url, document):
   if "reddit.com" in url:
        redditPhonyArticle(document)
   else:
        anchorsToRickRoll(document, .5) 
