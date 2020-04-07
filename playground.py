# Twitter API
import tweepy

# for saving which account's I am following
import json

# for catching Twitter API rate limit exception and wait for 15 minutes
import time

# class with my keys and tokens for authentication
import MySecrets

# to read csv file with tweets data
import pandas

# to write date of last update of following_data.json
from datetime import date

# to check if file exists
import os


my_secrets = MySecrets.secrets

# path to tweets
dir_path = r'C:\Users\jmsie\Dev\Projects\NewsFeed\data'

# Connecting to tweeter API using secrets
auth = tweepy.OAuthHandler(my_secrets.getConsumerKey(), my_secrets.getConsumerSecret())
auth.set_access_token(my_secrets.getAccessToken(), my_secrets.getAccessTokenSecret())
api = tweepy.API(auth, wait_on_rate_limit=True)


def saveJson(file_name, file_content):
    '''Saves data on json file.
    
    file_name: the file name of the data

    file_content: the data you want to save
    '''

    # write to JSON
    with open(file_name, 'w', encoding="utf-8") as f:
        #json.dumps(file_content, indent=4, sort_keys=True, default=str)
        json.dump(file_content, f, ensure_ascii=False, indent=4)


def handleTwitterAPIRateLimit(cursor, list_name):
    while True:
        try:
            yield cursor.next()

        # Catch Twitter API rate limit exception and wait for 15 minutes
        except tweepy.RateLimitError:
            print(f'\nData points in list = {len(list_name)}')
            print('Hit Twitter API rate limit.')
            
            for i in range(3, 0, -1):
                print(f'Wait for {i*5} minutes.')
                time.sleep(5 * 60)

        # Catch any other exceptions
        except Exception as e:
            print(e)

def getAllTweets(screen_name, count=200, return_tweets=False, update_json=False):
    '''Gets all tweets of a specified user.'''

    all_tweepy_tweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        new_tweets = api.user_timeline(screen_name=screen_name, count=count)
        print('trying')
    except tweepy.error.TweepError:
        print('\n----------The particular user has protected tweets.------------\n')
        if update_json:
            # write in CSV
            full_path = ''.join(dir_path + f'\{screen_name}_tweets.json')

            saveJson(path, [])
            print(screen_name)
            return None

    # save most recent tweets
    all_tweepy_tweets.extend(new_tweets)

    # save the id of the oldest tweet less one to avoid duplication
    oldest = all_tweepy_tweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left
    while count > 0:
        if len(new_tweets) == 0:
            break

        print(f'getting tweets before {oldest}')

        # all subsequent requests use the max_id param to prevent
        # duplicates
        try:
            new_tweets = api.user_timeline(screen_name=screen_name, count=count)
            count -= 200
        except:
            count = 0
        
        # save most recent tweets
        all_tweepy_tweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = all_tweepy_tweets[-1].id - 1
        print(f'...{count+200} tweets downloaded so far.')

    tweets_json = {}

    for tweet in all_tweepy_tweets:
        tweets_json[tweet.id_str] = {
        'created_at': str(tweet.created_at),
        'text': str(tweet.text), 
        'favorite_count': str(tweet.favorite_count)
        }

    #tweets_json = {
    #    tweet.id_str:   {
    #    'created_at':     tweet.created_at,
    #    'text':           tweet.text, 
    #    'favorite_count': tweet.favorite_count
    #}
    #for tweet in all_tweepy_tweets}

    if update_json:
        # write in CSV
        full_path = ''.join(dir_path + f'\{screen_name}_tweets.json')

        saveJson(full_path, tweets_json)
        print('json_saved')
        #with open(full_path, 'w',encoding="utf-8") as f:
        #    writer = csv.writer(f)
        #    writer.writerow(["id", "created_at" ,"text" ,"likes" ,"in reply to" ,"retweeted"])
        #    writer.writerows(tweets_json)

        print('Data downloaded successfuly.')
    
    if return_tweets:
        return tweets_json


def getFollowing(screen_name=None, user_id=None, update_json=False):
    '''Save which accounts one's account is following in a JSON file.'''
    following = []
    try:
        for user in tweepy.Cursor(api.friends, screen_name=screen_name).items():
            following.append(user.screen_name)
    except:
        for user in tweepy.Cursor(api.friends, screen_name=user_id).items():
            following.append(user.screen_name)

    data = {'last_update': str(date.today()), 'following':[i for i in following]}

    if update_json:
        saveJson('following_data.json', data)


def loadAllTweets(filename):
    data = pandas.read_csv(filename)
    return data


def loadFollowing(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def isEmptyFile(filename):
    filesize = os.path.getsize(filename)

    if filesize == 0:
        return True
    return False


#my user_id 1035449144473788416
getFollowing('jcob_sikorski', update_json=True)

# load json data
following = loadFollowing('following_data.json')

# if last update wasn't today synch data
#if str(date.today) == following['last_update']:
for screen_name in following['following']:
    # path to new data
    path = ''.join(dir_path + f'\{screen_name}_tweets.json')

    #open(path, 'w').close()
    getAllTweets(screen_name=screen_name, count=100, update_json=True)

#tweets = getAllTweets(screen_name='jcob_sikorski', return_tweets=True)
#print(tweets)



print('done')