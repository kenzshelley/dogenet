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
from bs4 import BeautifulSoup, NavigableString
import random
import sys
import requests
import string

RICKROLL = "http://192.168.1.137:3000/rickroll"

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
            anchor['href'] = RICKROLL
            if randomnum < 25:
                print "changing anchor of", anchor.string, " to ", shit_site
                anchor.string = shit_site
    return soup.prettify()

def redditPhonyArticle(document):
    POSTTITLES = ["I am a nigerian prince with lots of money, AMA!",
                  "How could they make so much money so easily?",
                  "TIL Nigerian princes actually do send inheritance money",
                  "ELI5: How does a stay-at-home mom make $87k/year by doing this?",
                  "BREAKING: Every doctor always wrong, forever",
                  "A local single in your area thinks you're hot. Find out who!",
                  "OHacks at The Ohio State University deemed the best hackathon of all time"]
    soup = BeautifulSoup(document)
    divider = soup.find("div", {"class" : "clearleft"})

    #will find the last article (should find the first though?)
    articles = list(getArticles(soup))
    article = random.choice(articles)     

    #ensures we insert at a even index
    insertionIndex = random.randint(1,20)
    if (insertionIndex%2 == 1):
        insertionIndex = insertionIndex + 1
    newArticle = BeautifulSoup(str(article))
    newArticle.find("a")['href'] = RICKROLL
    articleDivs = newArticle.find_all("div")
    for div in articleDivs:
        if "entry" in div.get("class"):
            textArea = div
            break

    textArea.find("p").find("a").append(random.choice(POSTTITLES))
    textArea.find("p").find("a")['href'] = RICKROLL
    textArea.find("p").find("a").contents[0] = u''
    siteTable = soup.find("div", {"id":"siteTable"})
    siteTable.insert(insertionIndex, BeautifulSoup(str(divider)))
    siteTable.insert(insertionIndex + 1, newArticle)
    return soup.prettify()

def getArticles(soup):
    for post in soup.find_all("div"):
        postclasses = post.get("class")
        if type(postclasses) is list:
            if 'thing' in postclasses and 'link' in postclasses:
                yield post

def multiPhonyArticles(document):
    print "Multiphony!!!"
    for i in xrange(5):
        document = redditPhonyArticle(document)
    return document

def stackOverflowLinkReplacement(document):
    soup = BeautifulSoup(document)
    posts = soup.find_all("div", {'class': 'post-text'})
    comments = soup.find_all("span", {'class': 'comment-copy'})
    tags = posts + comments
    replacePercentLinks(tags, 0.5)
    return str(soup)

class WTFString(str):
    def __getitem__(self, key):
        return WTFString('{%s}' % key)
    def __getattribute__(self, key):
        return WTFString('{%s}' % key)


class WTFDict:
    def __init__(self):
        self.__dict = dict()

    def __getitem__(self, name):
        print "is this getting called"
        return self.__dict.get(name, WTFString('{%s}' % name))

    def __setitem__(self, key, value):
        value = WTFString(value)
        self.__dict[key] = value
        return self.__dict[key]

    def __missing__(self, name):
        return WTFString('{%s}' % name)

def stackOverflowPostReplacement(document):
    percent = 0.5
    soup = BeautifulSoup(document)
    broll = soup.new_tag('a', href=RICKROLL)
    RESPONSES = [("I think ", soup.new_tag('a', href=RICKROLL).append("this post"), "really covers what you're looking for."),
                 ("Here, have a look at ", soup.new_tag('a', href=RICKROLL).append("this mega enlightening thread"), ""),
                 ("Forget all of that. ", soup.new_tag('a', href=RICKROLL).append("You could be making money every month by doing nothing!"), "",),
                 ("More importantly, scientists have just discovered that Obama is ", soup.new_tag('a', href=RICKROLL).append("LITERALLY HITLER!"), ""),
                 ("", soup.new_tag('a', href=RICKROLL).append("Here's a tutorial"), " on how to do exactly what you want in Brainfuck!")]
                 # 'I think <a href="%s">this post</a> really covers what you\'re looking for.' % RICKROLL,
                 # 'Here, have a look at <a href="%s">this mega enlightening thread</a>.' % RICKROLL,
                 # 'Forget all of that. <a href="%s">You could be making money every month by doing nothing!</a>' % RICKROLL,
                 # 'More importantly, scientists have just discovered that Obama is <a href="%s">LITERALLY HITLER!</a>' % RICKROLL,
                 # '<a href="%s">Here\'s a tutorial</a> on how to do exactly what you want in Brainfuck!' % RICKROLL]
    posts = soup.find_all("div", {'class': 'post-text'})
    comments = soup.find_all("span", {'class': 'comment-copy'})
    for post in random.sample(posts, int(percent*len(posts))):
        resp = random.choice(RESPONSES)
        p = soup.new_tag('p')
        for val in resp:
            p.append(val)
        post.clear()
        post.append(p)
    for comment in random.sample(comments, int(percent*len(comments))):
        resp = random.choice(RESPONSES)
        comment.clear()
        for val in resp:
            comment.append(val)
    return str(soup)

## The dict of functions to do it
HACKS = {'www.reddit.com': multiPhonyArticles,
         'stackoverflow.com': stackOverflowLinkReplacement}

def anchors(document):
    return anchorsToRickRoll(document, 0.2)

if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    out = open("output.html", 'w')
    output = redditPhonyArticle(f.read())
    out.write(output.encode('utf-8'))

## master routing function that all html goes through
def hack(url, document):
    print "Da url: %s" % url.split("/")[2]
    return HACKS.get(url.split("/")[2], anchors)(document)
