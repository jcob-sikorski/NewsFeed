def sortTweetsByLikes():
    # codecs for better performance
    import json, codecs
    from jsonLoad import jsonLoad
    from jsonSave import jsonSave

    friends = jsonLoad('friends_data.json')
    sorted_tweets_by_likes = {}
    dir_path = r'C:\Users\jmsie\Dev\Projects\NewsFeed\data'


    for screen_name in friends['friends']:
        path = ''.join(dir_path + f'\{screen_name}_tweets.json')
        user_data = jsonLoad(path)

        IDs = [*user_data]
        likes = {}

        # make dictionary with ID: likes pair
        for ID in IDs:
            likes.update({ID: user_data[ID]['favorite_count']})

        sorted_IDs_by_likes = list({
            ID: likes_count 
            for ID, likes_count in sorted(
                likes.items(), key=lambda item: int(item[1]), reverse=True)
                }.keys()
                )

        sorted_tweets_by_likes[screen_name] = {tweet_id: user_data[tweet_id] for tweet_id in sorted_IDs_by_likes}

    with open('sorted_tweets_by_likes.json', 'wb') as f:
        json.dump(sorted_tweets_by_likes, codecs.getwriter('utf-8')(f), ensure_ascii=False)