from connectToTwitterAPI import connectToTwitterAPI
from handleTwitterAPIRateLimit import handleTwitterAPIRateLimit
from jsonLoad import jsonLoad
from getFriends import getFriends
from getAllTweets import getAllTweets

def isEmptyFile(filename):
    # to check if file exists
    import os

    filesize = os.path.getsize(filename)

    if filesize == 0:
        return True
    return False


def sortByLikes(tweets: dict):
    NotImplemented

api = connectToTwitterAPI()
print('1')
#my user_id 1035449144473788416
getFriends(api, 'jcob_sikorski', write_json=True)
print('2')
# load json data
friends = jsonLoad('friends_data.json')
print('3')
# if last update wasn't today synch data
#if str(date.today) == friends['last_update']:
for screen_name in friends['friends']:
    print('4')
    # path to tweets
    dir_path = r'C:\Users\jmsie\Dev\Projects\NewsFeed\data'
    print('5')

    # path to new data
    path = ''.join(dir_path + f'\{screen_name}_tweets.json')
    #open(path, 'w').close()
    getAllTweets(api, screen_name=screen_name, count=100, write_json=True)
    print('6')

print('done')