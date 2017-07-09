from urlAnalyzer import URLAnalyzer
from textAnalyzer import TextAnalyzer

myObject = URLAnalyzer('http://www.markevans.ca/2017/06/14/create-taglines/')

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