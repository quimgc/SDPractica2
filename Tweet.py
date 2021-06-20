from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Tweet:
    sid_obj = SentimentIntensityAnalyzer()
    tweet_id = 0
    user_id = 0
    content_text = ""
    location = ""
    created_at = ""
    tweet_url = ""
    connector = ""
    sentiment_dict = "" 
    sentiment_is = ""

    #constructor
    def __init__(self, tweet_id, connect):
        
        self.tweet_id = tweet_id
        
        self.connector = connect

        self.tweet_url = "https://twitter.com/anyuser/status/"+str(tweet_id)

        content = self.connector.get_status(self.tweet_id, tweet_mode="extend")

        self.created_at = str(content.created_at)
        
        self.content_text = content.text

        self.user_id = content.user.id

        self.location = content.user.location

        self.calculateSentimentAnalysis()

        
    def calculateSentimentAnalysis(self):

        self.sentiment_dict = self.sid_obj.polarity_scores(self.content_text)

        if self.sentiment_dict['compound'] >= 0.05:

            self.sentiment_is = "Positive"
        
        elif self.sentiment_dict['compound'] <= - 0.05:
        
            self.sentiment_is = "Negative"
        
        else :
        
            self.sentiment_is = "Neutral"

    def getInfo(self):
        
        return {
                'tweet_id' : self.tweet_id,
                'user_id' : self.user_id,
                'tweet_url' : self.tweet_url,
                'created_at' : self.created_at,
                'content' : self.content_text,
                'location' : self.location, 
                'sentiment_dict' : self.sentiment_dict,
                'sentiment_is' : self.sentiment_is
                }






