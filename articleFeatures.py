from reddit import RedditExtractor

myObject = RedditExtractor('http://www.cnn.com/2017/07/06/health/photoshopped-baby-picture-with-piercing-trnd/index.html')
#a, b = myObject.word_count
d = myObject.nword
c = myObject.read_time()
e = myObject.count_img()

print('article length:', d)
print('read time:', c)
print('Img:', e)