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

def hack(document):
    soup = BeautifulSoup(document)
    links = soup.find_all('a')
    for anchor in links:
        anchor['href'] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    f = open('output.html', 'w')
    f.write(soup.prettify())

if __name__ == "__main__":
    hack(html_doc)
