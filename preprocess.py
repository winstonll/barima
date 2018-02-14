from urlAnalyzer import URLAnalyzer
from textAnalyzer import TextAnalyzer
import pandas as pd
import requests
import json
import numpy as np
import gc
import time
import timeout_decorator    
pd.options.mode.chained_assignment = None

def getLinkedin(url):
    q = "https://www.linkedin.com/countserv/count/share?url=" + url + "&format=json"
    r = requests.get(q)
    try:
        json_data = json.loads(r.text)
        count = json_data['count']
    except:
        count = 0
    return count

@timeout_decorator.timeout(30)
def analyzeURL(row):
    try:
        analyzer = URLAnalyzer(row['url'])
    except:
        return(row)
    else:
        selftext = analyzer.text
        row['para_count'] = analyzer.paragraph_counter()
        row['lexical_diversity'] = analyzer.lexical_diversity()
        row['word_count'] = analyzer.nword
        row['reading_time'] = analyzer.read_time()
        try:
            row['img_count'] = analyzer.count_img()
        except:
            row['img_count'] = 0
        row['grade'], row['word_freq'] = analyzer.reading_difficulty()
        row['descriptive_words'] = analyzer.descriptive_words_porp()
        row['video_count'] = analyzer.count_video()
        row['sentiment'] = analyzer.sentiment()
        row['original_title'] = analyzer.original_title
        title_analyzer = TextAnalyzer(row['original_title'])
        row['title_nchar'] = len(row['original_title'])
        row['title_nword'] = title_analyzer.nword
        row['title_sentiment'] = title_analyzer.sentiment()
        row['linkedin_shares'] = getLinkedin(row['url'])
        row['score_rank'] = row['score']/max_score[row['subreddit']]
        row['num_comments_rank'] = row['num_comments']/max_score[row['subreddit']]
        del analyzer
        del title_analyzer
        return(row)

data = pd.read_pickle('/home/wli/dec2017')
max_score = data.groupby('subreddit').apply(lambda x: np.max((x['score'])))
max_comments = data.groupby('subreddit').apply(lambda x: np.max((x['num_comments'])))

for index in range(50101, data.shape[0]):
    row = data.iloc[index]
    if row['selftext'] == '':
        try:
            data.iloc[index] = analyzeURL(row)
        except:
            continue
    elif len(row['selftext']) > 10:
        analyzer = TextAnalyzer(row['selftext'])
        row['para_count'] = analyzer.paragraph_counter()
        row['lexical_diversity'] = analyzer.lexical_diversity()
        row['word_count'] = analyzer.nword
        row['reading_time'] = analyzer.read_time()
        row['grade'], row['word_freq'] = analyzer.reading_difficulty()
        row['descriptive_words'] = analyzer.descriptive_words_porp()
        row['sentiment'] = analyzer.sentiment()
        title_analyzer = TextAnalyzer(row['title'])
        row['title_nchar'] = len(row['title'])
        row['title_nword'] = title_analyzer.nword
        row['title_sentiment'] = title_analyzer.sentiment()
        row['score_rank'] = row['score']/max_score[row['subreddit']]
        row['num_comments_rank'] = row['num_comments']/max_score[row['subreddit']]
        data.iloc[index] = row
        del analyzer
        del title_analyzer
    print(index)
    if index % 100 == 0:
        gc.collect()
        data.to_pickle('/home/wli/dec2017')
