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
import requests

RICKROLL = "http://127.0.0.1:3000/rickroll"

def replacePercentLinks(tags, percent):
    l = list(allLinks(tags))
    links = random.sample(l, int(percent*len(l)))
    for link in links:
        link['href'] = RICKROLL

def allLinks(tags):
    for tag in tags:
        links = tag.find_all('a')
        for link in links:
            yield link

def anchorsToRickRoll(document, probability):
    print 'in anchors to rick roll'
    p = {"X-Parse-Application-Id" : "KNf3x2GGrkFOoRapY8D9y6PkrHKRPlk6FgeWblEF","X-Parse-REST-API-Key" : "NFhLdYkpllYLW2Ndw92G8jPx7PuZOgP6CjtqbaF8"}
    r = requests.get('https://api.parse.com/1/classes/Suggestion/', headers=p)
    #randomly select and element & serve it...easy
    
    
    

    soup = BeautifulSoup(document)
    links = soup.find_all('a')
    for anchor in links:
        randomnum = random.randint(1,100)
        size = len(r.json()['results'])
        sugindex = random.randint(1,size-1)
        shit_site = r.json()['results'][sugindex]['url']
        if randomnum < probability * 100:
            randomnum = random.randint(1,100)
            anchor['href'] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            if randomnum < 25:
                print "changing anchor of", anchor.string, " to ", shit_site
                anchor.string = shit_site

    return soup.prettify()

def redditPhonyArticle(document):
    soup = BeautifulSoup(document)
    divider = soup.find("div", {"class" : "clearleft"})

    #will find the last article (should find the first though?)
    for post in soup.find_all("div"):
        postclasses = post.get("class")
        if type(postclasses) is list:
            if 'thing' in postclasses and 'link' in postclasses:
                article = post        

    #ensures we insert at a even index
    insertionIndex = random.randint(1,20)
    if (insertionIndex%2 == 1):
        insertionIndex = insertionIndex + 1
    newArticle = BeautifulSoup(str(article))
    newArticle.find("a")['href'] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    articleDivs = newArticle.find_all("div")
    for div in articleDivs:
        if "entry" in div.get("class"):
            textArea = div
            break

    textArea.find("p").find("a").append("I am a nigerian prince with lots of money, AMA!")
    textArea.find("p").find("a")['href'] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    textArea.find("p").find("a").contents[0] = u''
    siteTable = soup.find("div", {"id":"siteTable"})
    siteTable.insert(insertionIndex, BeautifulSoup(str(divider)))
    siteTable.insert(insertionIndex + 1, newArticle)

    return soup.prettify()

def stackOverflow(document):
    soup = BeautifulSoup(document)
    posts = soup.find_all("div", {'class': 'post-text'})
    comments = soup.find_all("span", {'class': 'comment-copy'})
    tags = posts + comments
    replacePercentLinks(tags, 0.5)
    return str(soup)

## The dict of functions to do it
HACKS = {'reddit.com': redditPhonyArticle,
         'stackoverflow.com': stackOverflow}

def anchors(document):
    return anchorsToRickRoll(document, 0.5)

if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    out = open("output.html", 'w')
    output = redditPhonyArticle(f.read())
    out.write(output.encode('utf-8'))

## master routing function that all html goes through
def hack(url, document):
   return HACKS.get(url.split("/")[2], anchors)(document)
