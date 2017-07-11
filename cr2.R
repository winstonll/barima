library(bigrquery)
library(httr)
library(RMySQL)
library(SocialMediaMineR)

project = 'unified-sensor-173013'
sql = "SELECT created_utc, subreddit, domain, url, num_comments,
        score, title, selftext 
        FROM [fh-bigquery:reddit_posts.2016_01] 
        WHERE subreddit in ('todayilearned', 'science', 'worldnews', 
        'movies', 'Music', 'news', 'books', 'space', 'gadgets', 
        'technology', 'politics', 'Games', 'Economics', 'relationships',
        'Fitness', 'Bitcoin', 'lgbt', 'writing', 'Android', 'PS4', 'nyc', 'LosAngeles',
        'toronto', 'KotakuInAction')
        AND selftext <> '[removed]' 
        AND selftext <> '[deleted]'
        LIMIT 10"

data_raw = query_exec(sql, project = project, max_pages = Inf)
data_raw$paragraph_count = 0L
data_raw$lexical_diversity = 0
data_raw$img_count = 0L
data_raw$descriptive_words = 0
data_raw$video_count = 0L
data_raw$reading_time = 0
data_raw$sentiment = 0
data_raw$reading_difficulty = 0
data_raw$linkedin_shares = 0L
data_raw$keywords = ''

input = cbind(data_raw$domain, data_raw$selftext, data_raw$url)

check = function(input){
    index = 1
    shares = 0
    if(substr(input[1], 1, 5) == 'self.' & nchar(input[2]) < 100)
        index = 0
    else if(substr(input[1], 1, 25) != 'https://www.reddit.com/r/'){
        x = try(GET(input[3]), silent = T)
        if(class(x) == 'try-error')
            index = 0
        else if(x$status_code != 200)
            index = 0
        else{
            linkedin_table = try(get_linkedin(input[3]), silent = T)
            if(class(linkedin_table) != 'try-error')
                shares = as.integer(linkedin_table[1])
        }
     }
     return(paste(index, shares, sep = ','))
}
pbapply(input, 1, check)


index = rep(1, nrow(data_raw))
linkedin_shares = rep(0, nrow(data_raw))

for(i in 1:nrow(data_raw)){


foreach(i=1:dim, .combine = 'c', .packages = 'SocialMediaMineR')%dopar% {
    if(substr(data_raw$domain[i], 1, 5) == 'self.' & nchar(data_raw$selftext[i]) < 100)
        index[i] = 0
    else if(substr(, 1, 25) != 'https://www.reddit.com/r/'){
        x = try(GET(data_raw$url[i]), silent = T)
        if(class(x) == 'try-error')
            index[i] = 0
        else if(x$status_code != 200)
            index[i] = 0
        else{
            linkedin_table = try(get_linkedin(data_raw$url[i]), silent = T)
            if(class(linkedin_table) != 'try-error')
                linkedin_shares[i] = as.integer(linkedin_table[1])
        }
     }
}
data = data_raw[as.logical(index), ]

con = dbConnect(MySQL(), user = 'winstonl', password = '111111', 
            host = '146.148.45.182',
            dbname = 'arimadb')

dbWriteTable(con, 'reddit_posts', data, append = T)