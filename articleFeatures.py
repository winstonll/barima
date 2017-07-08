from reddit import RedditExtractor


#myObject = RedditExtractor('https://naturallyella.com/tomatoes-sweet-corn-bread/')
myObject = RedditExtractor('http://www.cnn.com/2017/07/06/health/photoshopped-baby-picture-with-piercing-trnd/index.html')
#a, b = myObject.word_count
d = myObject.text
c = myObject.read_time()
e = myObject.count_img()
f, g = myObject.reading_difficulty()

print('article length:', d)
print('read time:', c)
print('Img:', e)
print('grade', f)
print('diff words', g)
