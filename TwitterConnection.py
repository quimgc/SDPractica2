import tweepy
import os
import json

class TwitterConnection():

    parser = ""
    auth = ""
    api = ""

    #constructor
    def __init__(self):

            
        #open twitter config.
    
        twitter_conf = json.loads(os.environ['LITHOPS_CONFIG'])
        
        self.auth = tweepy.OAuthHandler(twitter_conf["twitter"]["api_key"], twitter_conf["twitter"]["api_secret_key"])
        self.auth.set_access_token(twitter_conf["twitter"]["access_token"], twitter_conf["twitter"]["access_token_secret"])
    
        self.api = tweepy.API(self.auth)

        
    
    def getConnection(self):

        return self.api
