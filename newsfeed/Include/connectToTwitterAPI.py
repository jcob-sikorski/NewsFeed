def connectToTwitterAPI():
    # Twitter API
    import tweepy

    # class with my keys and tokens for authentication
    import MySecrets

    my_secrets = MySecrets.secrets

    # path to tweets
    dir_path = r'C:\Users\jmsie\Dev\Projects\NewsFeed\data'

    # Connecting to tweeter API using secrets
    auth = tweepy.OAuthHandler(my_secrets.getConsumerKey(), my_secrets.getConsumerSecret())
    auth.set_access_token(my_secrets.getAccessToken(), my_secrets.getAccessTokenSecret())
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api