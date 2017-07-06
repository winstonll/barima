import pandas as pd
from newspaper import Article
import gensim
import collections
from urllib.request import urlopen
from PIL import ImageFile
import nltk

def getsizes(url):
	file = urlopen(url)
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

class RedditExtractor:

	def __init__(self, url):
		a = Article(url)
		a.download()
		a.parse()
		self.text = a.text
		self.tok = nltk.word_tokenize(self.text)
		self.img = list(a.images)
		self.url = url

	def paragraph_counter(self):
		linecount = 0
		for line in self.text:
			if line in ('\n', '\r\n'):
				if linecount == 0:
					self.paragraph_count += 1
					linecount += 1
				else:
					linecount = 0
		return(self.paragraph_count)
	
	def word_count(self):
		self.length = len(self.text)
		self.richness = len(set(self.text))/self.length
		return self.length, self.richness

	def word_porp(self, type):
		freq = nltk.pos_tag(self.tok)
		count = [w[1] for w in freq]
		count_length = len(count)
		table = collections.Counter(count)
		self.porp = table[type]/count_length
		return(self.porp)

#reading time = 275 wpm + 12s per img

	def count_img(self):
		self.count_img = 0
		for i in self.img:
			if getsizes(i) > 24000:
				self.img_count += 1
		return self.img_count