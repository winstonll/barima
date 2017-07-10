library(bigrquery)
library(httr)
library(RMySQL)
library(SocialMediaMineR)

project = 'unified-sensor-173013'
#project = 'phd-media-1489418588611'
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
data_raw$paragraph_count = 0
data_raw$lexical_diversity = 0
data_raw$img_count = 0
data_raw$descriptive_words = 0
data_raw$video_count = 0
data_raw$reading_time = 0
data_raw$sentiment = 0
data_raw$reading_difficulty = 0
#data_raw$fb_share = 0
#data_raw$fb_comments = 0
data_raw$linkedin_shares = 0


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
        else{
            #fb_table = get_facebook(data_raw$url[i])
            linkedin_table = try(get_linkedin(data_raw$url[i]), silent = T)
            #data_raw$fb_share[i] = fb_table[2]
            #data_raw$fb_comments[i] = fb_table[1]
            if(class(linkedin_table) != 'try-error')
                data_raw$linkedin_shares[i] = linkedin_table[1]
        }
     }
    print(i)
}

data = data_raw[as.logical(index), ]

con = dbConnect(MySQL(), user = 'winstonl', password = '111111', 
            host = '146.148.45.182',
            dbname = 'arimadb')

dbWriteTable(con, 'reddit_posts', data, append = T)

