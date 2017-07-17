from urlAnalyzer import URLAnalyzer
from textAnalyzer import TextAnalyzer
import pymysql.cursors

connection = pymysql.connect(host = '146.148.45.182', user = 'winstonl', password = '111111', db = 'arimadb',
                            charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)


if #Is URL:
	analyzer = URLAnalyzer('http://www.markevans.ca/2017/06/14/create-taglines/')
	
	if analyzer.download_state != 2:
		next
	else:
		par_count = analyzer.paragraph_counter()
		lex = analyzer.lexical_diversity()
		nword = analyzer.nword
		read_time = analyzer.read_time()
		img = analyzer.count_img()
		grade, word_usage_freq = analyzer.reading_difficulty()
		descriptive = analyzer.descriptive_words_porp()
		vid = analyzer.count_video()
		sentiment = analyzer.sentiment()

else:
	analyzer = TextAnalyzer(text)

	par_count = analyzer.paragraph_counter()
	lex = analyzer.lexical_diversity()
	nword = analyzer.nword
	read_time = analyzer.read_time()
	img = analyzer.count_img()
	grade, word_usage_freq = analyzer.reading_difficulty()
	descriptive = analyzer.descriptive_words_porp()
	vid = analyzer.count_video()
	sentiment = analyzer.sentiment()	