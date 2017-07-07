import pandas as pd
from newspaper import Article
import gensim
import collections
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from PIL import ImageFile
import nltk

def getsizes(url):
	req = Request(url)
	try:
		file = urlopen(req)
	except HTTPError as e:
		print('http')
		return 0
	except URLError as e:
		print('url')
		return 0
	else:
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
		self.length = 0
		self.img_count = 0

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

	def read_time(self):
		self.required_time = round(self.length/275 + 0.2*self.count_img(), 1)
		return self.required_time

	def count_img(self):
		for i in self.img:
			if getsizes(i) > 24000:
				self.img_count += 1
		return self.img_count