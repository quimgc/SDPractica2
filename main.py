#https://www.trackmyhashtag.com/blog/free-twitter-datasets/
from lithops import FunctionExecutor, Storage
import json
from TwitterConnection import TwitterConnection
from Tweet import Tweet
import matplotlib.pyplot as plt



files_csv = []  #list of files .csv with prefix csv/



#return the name of file to save. 
def save_file_name(file):
   
   return (file['Key'])


def chunks(lst, n):

    for i in range(0, len(lst), n):
        yield lst[i:i + n]



def get_tweets_information(file, id):

    storage = Storage()

    data = storage.get_object(storage.bucket, file).splitlines()

    iterdata = list(chunks(data, 50000)) #create list of lists with 1000 intems each.
    

    with FunctionExecutor(runtime_memory=1024) as fexec:

        fexec.map(get_tweet_information, iterdata)
        
        compt = 0

        result = fexec.get_result()

        keys_list = []

        for tweets_information_founded in result:
       
            compt = compt+1
            
            key = 'tweet_information_'+str(id)+'_'+str(compt)
    
            storage.put_object(storage.bucket, key, json.dumps(tweets_information_founded))
            
            keys_list.append(key)
        
        return keys_list


def get_tweet_information(contentList):

    #get tweet id. 
    result = []

    connect = TwitterConnection().getConnection()
    try: 
         
        for content in contentList:

            id = content.decode('UTF-8').split(",")[0]

            #create an a Tweet object.
            tweet = Tweet(id, connect)

            # Return tweet info. 
            result.append(tweet.getInfo())

    except Exception: 
        
        pass

    return result


def create_plot_diagram(tweets_information):
    
    positive_tweets = 0
    negative_tweets = 0
    neutral_tweets = 0
    storage = Storage()

    for files in tweets_information:
        
        for file in files:
      
            data = json.loads(storage.get_object(storage.bucket, file))
            
            if len(data) > 0: 
            
                if data[0]['sentiment_is'] == "Positive":
                    positive_tweets = positive_tweets +1
                
                if data[0]['sentiment_is'] == "Negative":
                    negative_tweets = negative_tweets +1
                    
                if data[0]['sentiment_is'] == "Neutral":
                    neutral_tweets = neutral_tweets +1
        
                    
    print(positive_tweets)
    print(negative_tweets)
    print(neutral_tweets)

    counts = [positive_tweets, negative_tweets, neutral_tweets]
    
    names = ["Positive", "Negative", "Neutral"]
    
    plt.pie(counts, labels=names, autopct="%0.1f %%")
    
    plt.show()


if __name__ == '__main__':
  
    
    #get all files with the prefix is csv/.
    storage = Storage()

    files = storage.list_objects(storage.bucket, prefix = 'csv/')

    #save each filename into a list.    
    for file in files:
        
        files_csv.append(save_file_name(file))
    
    
    with FunctionExecutor(log_level='DEBUG', runtime_memory=1024) as fexec:

    
        #for each csv file, get all information about their tweet id. 
        fexec.map(get_tweets_information, files_csv)
        tweets_information = fexec.get_result()
    
      
    create_plot_diagram(tweets_information)

