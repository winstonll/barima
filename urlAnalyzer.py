from newspaper import Article
import collections
from urllib.request import Request, urlopen
from PIL import ImageFile
import nltk
import justext
import requests
from textstat.textstat import textstat
import math
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def getsizes(url):
    req = Request(url)
    try:
        file = urlopen(req, timeout = 10)
    except:
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

class URLAnalyzer:

    def __init__(self, url):
        np_extract = Article(url)
        np_extract.download()
        if np_extract.download_state == 2:
            np_extract.parse()
            np_text = np_extract.text
        else:
            np_text = ''

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

        self.original_title = np_extract.title
        self.tok = nltk.word_tokenize(self.text)
        self.img = list(np_extract.images)
        self.vid = list(np_extract.movies)
        self.url = url
        self.nchar = len(self.text)
        self.nword = len(self.tok)

    def descriptive_words_porp(self):
        if self.nword == 0:
            porp = 0
        else:
            freq = nltk.pos_tag(self.tok)
            count = [w[1] for w in freq]
            table = collections.Counter(count)
            sub_table = dict((k, table[k]) for k in ('JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS'))
            porp = sum(sub_table.values())/self.nword
        return porp

    def lexical_diversity(self):
        if self.nword == 0:
            lex = 0
        else:
            lex = len(set(self.text))/self.nword
        return lex

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

    def read_time(self):
        required_time = round(self.nword/275 + 0.2*self.count_img(), 1)
        return required_time

    def count_img(self):
        img_count = 0
        for i in self.img:
            if getsizes(i) > 500**2:
                img_count += 1
        return img_count

    def count_video(self):
        return len(self.vid)

    def reading_difficulty(self):
        if self.nword == 0:
            return 0, 0
        else:  
            diff_words = textstat.difficult_words(self.text)/self.nword
            flesch_kincaid = textstat.flesch_kincaid_grade(self.text)
            coleman_liau = textstat.coleman_liau_index(self.text)
            ari = textstat.automated_readability_index(self.text)
            dale_chall = textstat.dale_chall_readability_score(self.text)
            linsear = textstat.linsear_write_formula(self.text)
            gunning_fog = textstat.gunning_fog(self.text) - 6
            smog = textstat.smog_index(self.text)
            avg_grade = math.ceil((flesch_kincaid + coleman_liau + ari + dale_chall + linsear + gunning_fog + smog)/7)
            return avg_grade, diff_words

    def sentiment(self):
        analyser = SentimentIntensityAnalyzer()
        sent = analyser.polarity_scores(self.text)
        return sent['compound']