import pandas as pd
from newspaper import Article
import gensim
import collections

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