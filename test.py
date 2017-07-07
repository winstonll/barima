from preprocess import RedditExtractor

myObject = RedditExtractor('http://www.cnn.com/2017/07/06/politics/trump-joins-battle-for-the-soul-of-the-west/index.html')
#a, b = myObject.word_count
d = myObject.length
c = myObject.read_time()

print(d)
print(c)