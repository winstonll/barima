library(bigrquery)
library(httr)
library(RMySQL)
library(R.utils)

# subs = c('todayilearned', 'science', 'worldnews', 
#         'movies', 'Music', 'news', 'books', 'space', 'gadgets', 
#         'technology', 'politics', 'Games', 'Economics', 'relationships',
#         'Fitness', 'Bitcoin', 'lgbt', 'writing', 'Android', 'PS4', 'nyc', 'LosAngeles',
#         'toronto', 'KotakuInAction')
subs = c('movies', 'Music', 'news', 'books', 'space', 'gadgets', 
        'technology', 'politics', 'Games', 'Economics', 'relationships',
        'Fitness', 'Bitcoin', 'lgbt', 'writing', 'Android', 'PS4', 'nyc', 'LosAngeles',
        'toronto', 'KotakuInAction')

# dates = c('2016_01', '2016_02', '2016_03', '2016_04', '2016_05', '2016_06', '2016_07', 
#             '2016_08', '2016_09', '2016_10', '2016_11', '2016_12', '2017_01', '2017_02', 
#             '2017_03', '2017_04', '2017_05')

dates = '2016_01'

project = 'unified-sensor-173013'

get_linkedin = function (links){
    lkn.response <- data.frame()
    lkn.call <- paste0("https://www.linkedin.com/countserv/count/share?url=", 
        links, "&format=json")
    api_scrapper <- function(x) try(RCurl::getURL(x, timeout = 240, ssl.verifypeer = FALSE))
    lkn.response <- try(data.frame(RJSONIO::fromJSON(api_scrapper(lkn.call))))
    return(lkn.response)
}

for(d in dates){
    for(s in subs){
        print(paste("Start", d, s, Sys.time(), sep = ', '))
        sql = paste("SELECT created_utc, subreddit, domain, url, num_comments,
                score, title, selftext 
                FROM [fh-bigquery:reddit_posts.", d, "] 
                WHERE subreddit in ('", s, "')
                AND selftext <> '[removed]' 
                AND selftext <> '[deleted]'
                AND score > 49", sep = '')

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

        dim = nrow(data_raw)
        index = rep(1, dim)

        for(i in 1:dim){
            if(substr(data_raw$domain[i], 1, 5) == 'self.' & nchar(data_raw$selftext[i]) < 100)
                index[i] = 0
            else{   
                shorten = strsplit(data_raw$url[i], '#')[[1]][1]
                x = evalWithTimeout(try(GET(shorten), silent = T), timeout = 10, onTimeout = "silent") 
                if(exists('x'))
                    index[i] = 0
                else if(class(x) == 'try-error')
                    index[i] = 0
                else if(x$status_code == 200){
                    linkedin_table = get_linkedin(shorten)
                    data_raw$linkedin_shares[i] = as.integer(linkedin_table[1])
                }
             }
            if(i %% 50 == 0)
                print(paste(i, dim, Sys.time(), sep = ', '))
        }

        data = data_raw[as.logical(index), ]

        con = dbConnect(MySQL(), user = 'winstonl', password = '111111', 
            host = '146.148.45.182',
            dbname = 'arimadb')
        
        dbWriteTable(con, 'reddit_posts', data, append = T)

        print(paste('End', d, s, Sys.time(), sep = ', '))
    }
}