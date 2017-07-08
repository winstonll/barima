from newspaper import Article
import gensim
import collections
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from PIL import ImageFile
import nltk
import justext
import requests
from socket import timeout

def getsizes(url):
    req = Request(url)
    try:
        file = urlopen(req)
    except HTTPError:
        print('http')
        return 0
    except URLError:
        print('url')
        return 0
    except timeout:
        print('timeout')
        return(0)
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
        np_extract = Article(url)
        np_extract.download()
        np_extract.parse()
        np_text = np_extract.text

        jt_text = ''
        response = requests.get(url)
        paragraphs = justext.justext(response.content, justext.get_stoplist("English"))

        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                jt_text = jt_text + str(paragraph.text)

        if len(np_text) > len(jt_text):
            self.text = np_text
        else:
            self.text = jt_text

        self.tok = nltk.word_tokenize(self.text)
        self.img = list(np_extract.images)
        self.url = url
        self.nchar = len(self.text)
        self.nword = len(self.tok)

    def paragraph_counter(self):
        linecount = 0
        paragraph_count = 0
        for line in self.text:
            if line in ('\n', '\r\n'):
                if linecount == 0:
                    paragraph_count += 1
                    linecount += 1
                else:
                    linecount = 0
        return paragraph_count

    def lexical_diversity(sel):
        lex = len(set(self.text))/self.nword

    def word_porp(self, type):
        freq = nltk.pos_tag(self.tok)
        count = [w[1] for w in freq]
        count_length = len(count)
        table = collections.Counter(count)
        porp = table[type]/count_length
        return porp

    def read_time(self):
        required_time = round(self.nword/275 + 0.2*self.count_img(), 1)
        return required_time

    def count_img(self):
        img_list = self.img
        img_count = 0
        for i in img_list:
            if getsizes(i) > 500**2:
                img_count += 1
        return img_count

    def count_video(self):
        video_list = list(self.movies)
        return len(video_list)