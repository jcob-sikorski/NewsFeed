def handleTwitterAPIRateLimit(cursor, list_name):
    # Twitter API
    import tweepy

    # for catching Twitter API rate limit exception and waiting for 15 minutes
    import time

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