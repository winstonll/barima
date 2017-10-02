library(tm)
library(SnowballC)
library(RMySQL)
con = dbConnect(MySQL(), user = 'winstonl', password = '111111', host = '146.148.45.182', dbname = 'arimadb')
a = dbReadTable(con, 'reddit')
doc = a$selftext
corpus = Corpus(VectorSource(doc))
corpus = tm_map(corpus, content_transformer(tolower))
corpus = tm_map(corpus, removeNumbers)
corpus = tm_map(corpus, removePunctuation)
corpus = tm_map(corpus, removeWords, c("the", "and", stopwords("english")))
corpus =  tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, stemDocument)
dtm <- DocumentTermMatrix(corpus)
dtm = removeSparseTerms(dtm, 0.99)
dtm_tfidf <- DocumentTermMatrix(corpus, control = list(weighting = weightTfIdf))
dtm_tfidf = removeSparseTerms(dtm_tfidf, 0.95)
inspect(dtm_tfidf[1, ])

for(i in 1:nrow(a)){
	a$keywords[i] = paste(colnames(inspect(dtm_tfidf[i, ])), collapse = ' ')

	if(i %% 100 == 0)
		print(i)
}

df <- data.frame(as.matrix(dtm_tfidf), stringsAsFactors=FALSE)