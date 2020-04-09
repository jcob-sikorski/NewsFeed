import json
from jsonLoad import jsonLoad
from jsonSave import jsonSave

friends = jsonLoad('friends_data.json')
sorted_ids_by_likes = []

each_user_sorted_ids={}

for screen_name in friends['friends']:
    dir_path = r'C:\Users\jmsie\Dev\Projects\NewsFeed\data'

    path = ''.join(dir_path + f'\{screen_name}_tweets.json')

    user_data = jsonLoad(path)
    print(user_data) 

    # IDs
    keys = [*user_data]

    likes = {}

    # make dictionary with ID: likes pair only
    for i in keys:
        likes.update({i: user_data[i]['favorite_count']})

    # sort IDs by likes count
    likes = {key: value for key, value in reversed(sorted(likes.items(), key=lambda item: item[1]))}

    #sorted_ids_by_likes.extend(likes.keys())
    each_user_sorted_ids[screen_name] = [key for key in likes.keys()]

jsonSave('tweetsSortedByLikes', each_user_sorted_ids)

tweetsSortedByLikes = jsonLoad('tweetsSortedByLikes')

for screen_name in friends['friends']:
    dir_path = r'C:\Users\jmsie\Dev\Projects\NewsFeed\data'

    # path to new data
    path = ''.join(dir_path + f'\{screen_name}_tweets.json')

    user_data = jsonLoad(path)

    for id in tweetsSortedByLikes[screen_name]:
        print(user_data[id])