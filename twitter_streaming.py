from tweepy.streaming import *
from tweepy import OAuthHandler
from tweepy import Stream
import re


access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""
count_rt = 0
count_tweets = 0
max_count=4000

class StdOutListener(StreamListener):



    def on_data(self, raw_data):
     

        data = json.loads(raw_data)
        if 'in_reply_to_status_id' in data:
            global count_tweets
            status = Status.parse(self.api, data)
            word = "RT @"
            match = re.search(word, status.text)
            if match:
                global count_rt
                count_rt = count_rt + 1
                if count_rt < 0.05*max_count:
                    #print(raw_data)
                    count_tweets += 1
                    if count_tweets >= max_count:
                        #print('Exit here')
                        exit()
                    else:
                        file_json.write(raw_data)
                
            else:
                count_tweets += 1
                if count_tweets >= 9000:
                    #print('Exit here')
                    exit()
                else:
                    file_json.write(raw_data)
                    print(raw_data)


        return True


    def on_error(self, status):
        print(status)




if __name__ == '__main__':

    file_json = open("USOPEN-SEP14-EN","a+")
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(languages=["tr"], track=['US Open' or '#djokovic' or '#wawrinka' or '#kerber' or 'Wawrinka' or 'Kerber' or '#USOpen' or '#USOpen2016' or 'Djokovic'])










