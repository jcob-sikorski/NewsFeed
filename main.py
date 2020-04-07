# Twitter API
import tweepy

# for saving which account's I am friends
import json

# for catching Twitter API rate limit exception and wait for 15 minutes
import time

# class with my keys and tokens for authentication
import MySecrets

# to read csv file with tweets data
import pandas

# to write date of last update of friends_data.json
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

def saveJson(file_name, file_content):
    '''Saves data on json file.
    
    file_name: the file name of the data
    file_content: the data you want to save
    '''

    # write to JSON
    with open(file_name, 'w', encoding="utf-8") as f:
        json.dump(file_content, f, ensure_ascii=False, indent=4)


def loadJson(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data


def getAllTweets(screen_name, count=200, write_json=False):
    '''Gets all tweets of a specified user.'''

    most_recent_tweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        tweets = api.user_timeline(screen_name=screen_name, count=count)
    except tweepy.error.TweepError:
        print('\n----------The particular user has protected tweets.------------\n')
        if write_json:
            full_path = ''.join(dir_path + f'\{screen_name}_tweets.json')
            saveJson(path, [])

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
        'created_at': str(tweet.created_at),
        'text': str(tweet.text), 
        'favorite_count': str(tweet.favorite_count)
        }

    if write_json:
        path_to_json_tweets = ''.join(dir_path + f'\{screen_name}_tweets.json')

        saveJson(path_to_json_tweets, tweets_json)

        print('Data downloaded successfuly.')


def getFriends(screen_name=None, user_id=None, write_json=False):
    '''Save Twitter friends in a JSON file.'''
    friends = []
    try:
        for user in tweepy.Cursor(api.friends, screen_name=screen_name).items():
            friends.append(user.screen_name)
    except:
        for user in tweepy.Cursor(api.friends, screen_name=user_id).items():
            friends.append(user.screen_name)

    data = {'last_update': str(date.today()), 'friends':[i for i in friends]}

    if write_json:
        saveJson('friends_data.json', data)


def loadAllTweets(filename):
    data = pandas.read_csv(filename)
    return data


def isEmptyFile(filename):
    filesize = os.path.getsize(filename)

    if filesize == 0:
        return True
    return False


#my user_id 1035449144473788416
getFriends('jcob_sikorski', write_json=True)

# load json data
friends = loadJson('friends_data.json')

# if last update wasn't today synch data
#if str(date.today) == friends['last_update']:
for screen_name in friends['friends']:
    # path to new data
    path = ''.join(dir_path + f'\{screen_name}_tweets.json')

    #open(path, 'w').close()
    getAllTweets(screen_name=screen_name, count=100, write_json=True)

print('done')