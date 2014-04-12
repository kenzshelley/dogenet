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
    soup = BeautifulSoup(document)
    links = soup.find_all('a')
    for anchor in links:
        randomnum = random.randint(1,100)
        if randomnum < probability * 100:
            anchor['href'] = RICKROLL
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
    for post in soup.find_all("div"):
        postclasses = post.get("class")
        if type(postclasses) is list:
            if 'thing' in postclasses and 'link' in postclasses:
                article = post        

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

def multiPhonyArticles(document):
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

def stackOverflowPostReplacement(document):
    percent = 0.5
    RESPONSES = ['I think <a href="%s">this post</a> really covers what you\'re looking for.' % RICKROLL,
                 'Here, have a look at <a href="%s">this mega enlightening thread</a>.' % RICKROLL,
                 'Forget all of that. <a href="%s">You could be making money every month by doing nothing!</a>' % RICKROLL,
                 'More importantly, scientists have just discovered that Obama is <a href="%s">LITERALLY HITLER!</a>' % RICKROLL,
                 '<a href="%s">Here\'s a tutorial</a> on how to do exactly what you want in Brainfuck!' % RICKROLL]
    soup = BeautifulSoup(document)
    posts = soup.find_all("div", {'class': 'post-text'})
    comments = soup.find_all("span", {'class': 'comment-copy'})
    for post in random.sample(posts, int(percent*len(posts))):
        post.string = BeautifulSoup("<p>%s</p>" % random.choice(RESPONSES)).encode(formatter=None)
    for comment in random.sample(comments, int(percent*len(comments))):
        comment.string = BeautifulSoup(random.choice(RESPONSES)).encode(formatter=None)
    return str(soup)

## The dict of functions to do it
HACKS = {'reddit.com': multiPhonyArticles,
         'stackoverflow.com': stackOverflowPostReplacement}


if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    out = open("output.html", 'w')
    output = redditPhonyArticle(f.read())
    out.write(output.encode('utf-8'))

def hack(url, document):
   return HACKS.get(url.split("/")[2], anchorsToRickRoll(document, .5))(document)
