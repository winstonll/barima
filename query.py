import pandas as pd
import pickle

QUERY = ('SELECT created_utc, subreddit, domain, url, num_comments, score, title, selftext FROM [fh-bigquery:reddit_posts.2017_12]' 
            'WHERE subreddit in ("todayilearned", "politics", "science", "worldnews", "new", \
                    "technology", "KotakuInAction", "movies", "books", "space", "gadgets", \
                    "Games", "Economics", "relationships", "Fitness", "Bitcoin", "lgbt", \
                    "writing", "Android", "PS4", "nyc", "LosAngeles", "toronto") AND selftext <> "[removed]" \
                    AND selftext <> "[deleted]"')
data = pd.read_gbq(QUERY, project_id='graphic-armor-194600')
data = data.loc[(data['score'] >= 10) | (data['num_comments'] >= 10)]
data.to_pickle('/home/wli/dec2017_raw')   

data['para_count'] = 0
data['lexical_diversity'] = 0
data['word_count'] = 0
data['reading_time'] = 0
data['img_count'] = 0
data['grade'] = 0
data['word_freq'] = 0
data['descriptive_words'] = 0
data['video_count'] = 0
data['sentiment'] = 0
data['original_title'] = ''
data['title_nchar'] = 0
data['title_nword'] = 0
data['title_sentiment'] = 0
data['linkedin_shares'] = 0
data['score_rank'] = 0
data['num_comments_rank'] = 0

data.to_pickle('/home/wli/dec2017')