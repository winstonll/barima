from preprocess import RedditExtractor

myObject = RedditExtractor('https://www.investing.com/news/stock-market-news/futures-lower-ahead-of-trade,-adp-jobs-data-502653')
#a, b = myObject.word_count
c = myObject.count_img()

print(c)