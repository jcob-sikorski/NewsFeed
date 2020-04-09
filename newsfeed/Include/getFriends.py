def getFriends(api, screen_name=None, user_id=None, write_json=False):
    # Twitter API
    import tweepy
    from jsonSave import jsonSave

    # to write date of last update of friends_data.json
    from datetime import date

    '''Save Twitter friends in a JSON file.'''
    friends = []
    try:
        for user in tweepy.Cursor(api.friends, screen_name=screen_name).items():
            friends.append(user.screen_name)
    except:
        for user in tweepy.Cursor(api.friends, screen_name=user_id).items():
            friends.append(user.screen_name)

    if write_json:
        data = {'last_update': str(date.today()), 'friends':[i for i in friends]}
        jsonSave(file_name='friends_data.json', file_content=data)