class MyKeysAndAccessTokens():
    def __init__(self, consumer_key=None, consumer_secret= None, access_token= None, access_token_secret= None):
        self.consumer_key       = consumer_key
        self.consumer_secret    = consumer_secret
        self.access_token       = access_token
        self.access_token_secret= access_token_secret
        
        self.keys_and_access_tokens = {
            'consumer_key' : self.consumer_key, 
            'consumer_secret' : self.consumer_secret, 
            'access_token': self.access_token, 
            'access_token_secret': self.access_token_secret
            }


    def setKeys(self, consumer_key=None, consumer_secret=None):
        if consumer_key != None:
            self.consumer_key = consumer_key

        if consumer_secret != None:
            self.consumer_secret = consumer_secret


    def setAccessTokens(self, access_token=None, access_token_secret=None):
        if access_token != None:
            self.access_token = access_token
        
        if access_token_secret != None:
            self.access_token_secret = access_token_secret


    def getKeysAndTokens(self):
        return self.keys_and_access_tokens


    def getConsumerKey(self):
        return self.keys_and_access_tokens['consumer_key']
    

    def getConsumerSecret(self):
        return self.keys_and_access_tokens['consumer_secret']

    
    def getAccessToken(self):
        return self.keys_and_access_tokens['access_token']

    
    def getAccessTokenSecret(self):
        return self.keys_and_access_tokens['access_token_secret']

secrets = MyKeysAndAccessTokens(
    consumer_key = 'y0rlFXwfrwrDSHkqpGLoLyHhR', 
    consumer_secret = 'G6PifvEauIRCpEbnaVYakXGBbClreoHTlkozotsuFCawbN1bve', 
    access_token = '1035449144473788416-6EqHHr48p1R1IxwguQFRLLwRTVbdbn', 
    access_token_secret = '011MGkxIu2nZF7AtsQEEtXnGUY8j6pAEcgNNoMW42hVle'
    )
