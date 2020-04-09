import json
from jsonLoad import jsonLoad

friends = jsonLoad('friends_data.json')

for screen_name in friends['friends']:
    dir_path = r'C:\Users\jmsie\Dev\Projects\NewsFeed\data'

    # path to new data
    path = ''.join(dir_path + f'\{screen_name}_tweets.json')

    user_data = jsonLoad(path)
    print(user_data)