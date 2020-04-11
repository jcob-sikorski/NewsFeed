def getAllTweets(api, screen_name, count=200, write_json=False):
    '''Gets x tweets from a specified user, 
    
    where x is parameter count.
    '''

    # Twitter API
    import tweepy
    from jsonSave import jsonSave

    most_recent_tweets = []

    # path to tweets
    dir_path = r'C:\Users\jmsie\Dev\Projects\NewsFeed\data'

    full_path = ''.join(dir_path + f'\{screen_name}_tweets.json')

    # make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        tweets = api.user_timeline(screen_name=screen_name, count=count)
    except tweepy.error.TweepError:
        print('\n----------The particular user has protected tweets.------------\n')
        if write_json:
            jsonSave(full_path, [])
            print(screen_name)

            return None
        
    # save most recent tweets
    most_recent_tweets.extend(tweets)

    # save the id of the oldest_tweet tweet less one to avoid duplication
    oldest_tweet = most_recent_tweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left
    while count > 0:
        if len(tweets) == 0:
            break

        print(f'getting tweets before {oldest_tweet}')

        # all subsequent requests use the max_id param to prevent
        # duplicates
        try:
            tweets = api.user_timeline(screen_name=screen_name, count=count)
            count -= 200
        except:
            count = 0
        
        # save most recent tweets
        most_recent_tweets.extend(tweets)

        # update the id of the oldest_tweet tweet less one
        oldest_tweet = most_recent_tweets[-1].id - 1
        print(f'...{count+200} tweets downloaded so far.')
    
    # tranform tweepy tweets to write them in json file
    tweets_json = {}

    for tweet in most_recent_tweets:
        tweets_json[tweet.id_str] = {
            'created_at':       str(tweet.created_at),
            'text':             str(tweet.text),
            'favorite_count':   str(tweet.favorite_count)
        }

    if write_json:
        jsonSave(full_path, tweets_json)
        print('Data downloaded successfuly.')