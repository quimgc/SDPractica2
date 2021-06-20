#https://www.trackmyhashtag.com/blog/free-twitter-datasets/
from lithops import FunctionExecutor, Storage
import json
from TwitterConnection import TwitterConnection
from Tweet import Tweet


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
    #with Pool() as p:

        #enmés de return fer put_object de 1000 en 1000.
        #fexec.map(get_tweet_information, iterdata)
        fexec.map(get_tweet_information, iterdata)
        
        
        compt = 0
        #al in posar fexec.get_result()
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
    
    print(tweets_information)

