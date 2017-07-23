from urlAnalyzer import URLAnalyzer
from textAnalyzer import TextAnalyzer
import pymysql.cursors

connection = pymysql.connect(host = '146.148.45.182', user = 'winstonl', password = '111111', db = 'arimadb',
    charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)

cursor = connection.cursor()

for i in range(1, 242895):
    sql = "SELECT * FROM reddit_posts LIMIT 1 OFFSET %s"
    cursor.execute(sql, (i-1))
    print('Currently working on batch starting: ' + str(i))
    row = cursor.fetchone()
    id = row['row_names']
    print('Currently processing: ' + str(id))
    if row['selftext'] == '':
        print('This is a link')        
        analyzer = URLAnalyzer(row['url'])
        par_count = analyzer.paragraph_counter()
        lex = analyzer.lexical_diversity()
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
        sql_update = 'UPDATE reddit_posts SET paragraph_count = %s, lexical_diversity = %s, img_count = %s, \
            descriptive_words = %s, video_count = %s, reading_time = %s, sentiment = %s, reading_difficulty = %s, \
            original_title = %s, title_nchar = %s, title_nword = %s, title_sentiment = %s WHERE row_names = %s;'
        rowUpdate = cursor.execute(sql_update, (par_count, lex, img, descriptive, vid, read_time, sentiment, grade, \
            original_title, title_nchar, title_nword, title_sentiment, id))
        connection.commit()
    else:
        print("This is self post")
        analyzer = TextAnalyzer(row['selftext'])
        par_count = analyzer.paragraph_counter()
        lex = analyzer.lexical_diversity()
        nword = analyzer.nword
        read_time = analyzer.read_time()
        grade, word_usage_freq = analyzer.reading_difficulty()
        descriptive = analyzer.descriptive_words_porp()
        sentiment = analyzer.sentiment()
        title_analyzer = TextAnalyzer(row['title'])
        title_nchar = len(row['title'])
        title_nword = title_analyzer.nword
        title_sentiment = title_analyzer.sentiment()

        sql_update = 'UPDATE reddit_posts SET paragraph_count = %s, lexical_diversity = %s, \
            descriptive_words = %s, reading_time = %s, sentiment = %s, reading_difficulty = %s, \
            title_nchar = %s, title_nword = %s, title_sentiment = %s WHERE row_names = %s;'
        rowUpdate = cursor.execute(sql_update, (par_count, lex, descriptive, read_time, sentiment, grade, \
            title_nchar, title_nword, title_sentiment, id))
        connection.commit()