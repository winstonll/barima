import pandas as pd
from newspaper import Article
import gensim
import collections
from urllib.request import urlopen
from PIL import ImageFile

def paragraph_count(text):
    paragraphcount = 0
    linecount = 0
    for line in text:
        if line in ('\n', '\r\n'):
            if linecount == 0:
                paragraphcount = paragraphcount + 1
            linecount = linecount + 1
        else:
            linecount = 0
    return(paragraphcount)

def word_porp(text, type):
    tok = nltk.word_tokenize(text)
    freq = nltk.pos_tag(tok)
    count = [w[1] for w in freq]
    total_length = len(count)
    table = collections.Counter(count)
    porp = table[type]/total_length
    return(porp)

def get_url_content(url):
	a = Article(url)
	a.download()
	a.parse()
	text = a.text
	img = list(a.images)
	largePic = 0
	for i in img:
		if getsizes(i) > 24000:
			largePic += 1
	return text, largePic



def getsizes(uri):
    file = urlopen(uri)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return p.image.size[0]*p.image.size[1]
            break
    file.close()
    return 0
