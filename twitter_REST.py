from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import time
import json
import re

def writeToJson():
    with open('USOPEN-SEP19-EN.json','a+', encoding='utf8') as json_file:
        for tweet in searched_tweets:
            json_str = json.dumps(tweet._json, ensure_ascii=False)
            json_file.write(json_str)

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



query = 'US Open' or '#djokovic' or '#wawrinka' or '#kerber' or 'Wawrinka' or 'Kerber' or '#USOpen' or '#USOpen2016' or 'Djokovic'

max_count = 9999
searched_tweets = []
last_id = -1
count_rt = 0
actual_count_rt = 0
tweet_count = 0

while len(searched_tweets) < max_count:
    count = max_count - len(searched_tweets)
    try:
        new_tweets = api.search(q=query, count=count, lang='en', max_id=(last_id-1))
        if not new_tweets:
            break
        word = "RT @"

        for current_tweet in new_tweets:
            match = re.search(word, current_tweet.text)
            #print(current_tweet.text)
            if match:
                
                continue
            else:
                #print(tweet)
                tweet_count += 1
                searched_tweets.append(current_tweet)

        last_id = new_tweets[-1].id

        if (tweet_count % 1000 == 0):
            writeToJson()
            searched_tweets = []

        if (tweet_count >= max_count):
            print("Total Number of Tweets:", tweet_count)
            print("Retweeted Count", actual_count_rt)
            exit()

        if ((tweet_count % 10000) == 0):        
            print("Total Number of Tweets:", tweet_count)
            print("Retweeted Count", actual_count_rt)
            print("Going to Sleep now. Good night!")
            time.sleep(60*15)

        print(last_id)
        print(len(new_tweets))

    except tweepy.TweepError as e:
        writeToJson()
        print(e.reason)
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break

writeToJson()
#print(last_id)
#print (searched_tweets)
print(len(searched_tweets))
print("Total Number of Tweets:", tweet_count)
print("Retweeted Count", actual_count_rt)


