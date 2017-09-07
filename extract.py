from urlAnalyzer import URLAnalyzer
from textAnalyzer import TextAnalyzer
from sqlalchemy import create_engine
import pandas as pd

# connection = pymysql.connect(host = '146.148.45.182', user = 'winstonl', password = '111111', db = 'arimadb',
#     charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)

# cursor = connection.cursor()

engine = create_engine('mysql+pymysql://winstonl:111111@146.148.45.182:3306/arimadb')
sql_template = "SELECT * FROM reddit_posts LIMIT 1 OFFSET %s"

with engine.connect() as conn, conn.begin():
    for i in range(1, 242895):
        sql = sql_template % (i-1)
        row = pd.read_sql(sql, conn)
        if row['selftext'] == '':
            analyzer = URLAnalyzer(row['url'][0])
            selftext = analyzer.text.encode('utf-8')
            paragraph_count = analyzer.paragraph_counter()
            lexical_diversity = analyzer.lexical_diversity()
            nword = analyzer.nword
            read_time = analyzer.read_time()
            img = analyzer.count_img()
            grade, word_usage_freq = analyzer.reading_difficulty()
            descriptive = analyzer.descriptive_words_porp()
            vid = analyzer.count_video()
            sentiment = analyzer.sentiment()
            original_title = analyzer.original_title
            title_analyzer = TextAnalyzer(original_title)
            title_nchar = len(original_title)
            title_nword = title_analyzer.nword
            title_sentiment = title_analyzer.sentiment()

            d = pd.DataFrame({'created_at': row['created_utc'][0], 'subreddit': row['subreddit'][0], 
                'url': row['url'][0], 'num_comments': row['num_comments'][0], 'score': row['score'][0], 
                'title': row['title'][0], 'selftext': selftext, 'paragraph_count': paragraph_count, 'image_count': img,
                'video_count': vid, 'reading_time': read_time, 'sentiment': sentiment, 'reading_difficulty': grade, 
                'word_freq': word_usage_freq,'descriptive_words': descriptive,
                'linkedin_shares': row['linkedin_shares'][0], 'keywords': '', 'original_title': original_title,
                'title_nchar': title_nchar, 'title_nword': title_nword, 'title_sentiment': title_sentiment}, index=[0])
            d.to_sql('reddit_data', conn, if_exists = 'append', index = False)
        
        else:
            print("This is self post")
            analyzer = TextAnalyzer(row['selftext'][0])
            par_count = analyzer.paragraph_counter()
            lex = analyzer.lexical_diversity()
            nword = analyzer.nword
            read_time = analyzer.read_time()
            grade, word_usage_freq = analyzer.reading_difficulty()
            descriptive = analyzer.descriptive_words_porp()
            sentiment = analyzer.sentiment()
            title_analyzer = TextAnalyzer(row['title'][0])
            title_nchar = len(row['title'][0])
            title_nword = title_analyzer.nword
            title_sentiment = title_analyzer.sentiment()

            d = pd.DataFrame({'created_at': row['created_utc'][0], 'subreddit': row['subreddit'][0], 
                'url': row['url'][0], 'num_comments': row['num_comments'][0], 'score': row['score'][0], 
                'title': row['title'][0], 'selftext': selftext, 'paragraph_count': paragraph_count, 'image_count': 0,
                'video_count': 0, 'reading_time': read_time, 'sentiment': sentiment, 'reading_difficulty': grade, 
                'word_freq': word_usage_freq,'descriptive_words': descriptive,
                'linkedin_shares': row['linkedin_shares'][0], 'keywords': '', 'original_title': '',
                'title_nchar': title_nchar, 'title_nword': title_nword, 'title_sentiment': title_sentiment}, index=[0])

        d.to_sql('reddit_data', conn, if_exists = 'append', index = False)