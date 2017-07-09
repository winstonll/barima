library(bigrquery)
library(httr)
library(RMySQL)

#project = 'unified-sensor-173013'
project = 'phd-media-1489418588611'
sql = "SELECT created_utc, subreddit, domain, url, num_comments,
        title, selftext 
        FROM [fh-bigquery:reddit_posts.2016_01] 
        WHERE subreddit in ('todayilearned', 'science', 'worldnews', 
        'movies', 'music', 'news', 'books', 'space', 'gadgets', 
        'technology', 'politics', 'games', 'economics', )
        AND selftext <> '[removed]' 
        AND selftext <> '[deleted]'
        LIMIT 100"

data_raw = query_exec(sql, project = project, max_pages = Inf)

index = rep(1, nrow(data_raw))

for(i in 1:nrow(data_raw)){
    if(substr(data_raw$domain[i], 1, 5) == 'self.' & nchar(data_raw$selftext[i]) < 100)
        index[i] = 0
    else if(substr(data_raw$domain[i], 1, 25) != 'https://www.reddit.com/r/'){
        x = try(GET(data_raw$url[i]), silent = T)

        if(class(x) == 'try-error')
            index[i] = 0
        else if(http_status(x)$category != 'Success')
            index[i] = 0
     }
    if(i %% 10 == 0)
        print(i)
}

data = data_raw[as.logical(index), ]

con = dbConnect(MySQL(), user = 'winstonl', password = '111111', 
            host = '146.148.45.182',
            dbname = 'arimadb')

dbWriteTable(con, 'reddit_posts', data, append = T)

