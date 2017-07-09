from reddit import RedditExtractor

myObject = RedditExtractor('https://www.reddit.com/r/technology/comments/6h82ji/pornhub_ok_cupid_imgur_duckduckgo_namecheap/')

a = myObject.paragraph_counter()
b = myObject.lexical_diversity()
d = myObject.nword
c = myObject.read_time()
e = myObject.count_img()
f, g = myObject.reading_difficulty()
h = myObject.descriptive_words_porp()
i = myObject.count_video()
j = myObject.sentiment()

print(myObject.text)
print('Paragraph Number:', a)
print('Article length (words):', d)
print('Read time:', c)
print('Img Count:', e)
print('Grade', f)
print('Diff words', g)
print('Lexical Diversity', b, 'or each word appears', 1/b)
print('Descriptive words prop', h)
print('Vid Count:', i)
print('Sentiment:', j)