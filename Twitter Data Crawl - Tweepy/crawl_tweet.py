from tweepy import OAuthHandler
import tweepy
import json
import pandas as pd
import csv
import string
import os
import time
from datetime import datetime

def scraptweets(search_words, maxTweets):
    
    # We cannot make large API call in one go. Hence, let's try T times
    tweet_list = []
    # Define a pandas dataframe to store the date:
    db_tweets = pd.DataFrame(columns = ['user_id', 'username', 'account_desc', 'location', 'following',
                                    'followers', 'total_tweets', 'user_created_ts', 'tweet_created_ts',
                                    'retweet_count', 'text', 'hashtags', 'is_retweet', 'ori_tweet_user_id',
                                    'ori_tweet_username'
                                   ]
                                )

    authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
    authentication.set_access_token(access_token, access_secret)
    api = tweepy.API(authentication, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    maxId = -1
    tweetCount = 0
    
    start_run = time.time()
        
    newTweets = tweepy.Cursor(
        api.search, q=search_words, tweet_mode='extended', result_type="recent"
    ).items(maxTweets)

    if not newTweets:
        print("out of tweet")
        break

    new_tweet_list = [tweet for tweet in newTweets]
    tweet_list.extend(new_tweet_list)

    tweetCount += len(new_tweet_list)
        
    end_run = time.time()
    duration_run = round((end_run-start_run)/60, 2)
    
    print('Scraping has completed!')
    print('Total time taken to scrap is {} minutes.'.format(duration_run))
        
    return tweet_list
        
def store_tweets(tweet_list):
    program_start = time.time()
    
    for tweet in tweet_list:
        is_retweet = 0
        ori_tweet_user_id = None
        ori_tweet_username = None
        ori_tweet_created_ts = None
        # Pull the values
        user_id = tweet.user.id_str
        username = tweet.user.screen_name
        acctdesc = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        usercreatedts = tweet.user.created_at
        tweetcreatedts = tweet.created_at
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']
        try:
            text = tweet.retweeted_status.full_text # If not a Retweet, Error will occur here
            is_retweet = 1
            ori_tweet_user_id = tweet.retweeted_status.user.id_str
            ori_tweet_username = tweet.retweeted_status.user.screen_name
            ori_tweet_created_ts = tweet.retweeted_status.created_at
        except AttributeError:  # Not a Retweet
            text = tweet.full_text
            is_retweet = 0
        # Add the variables to the empty list - ith_tweet:
        ith_tweet = [user_id, username, acctdesc, location, following, followers, totaltweets,
                     usercreatedts, tweetcreatedts, retweetcount, text, hashtags, is_retweet,
                     ori_tweet_user_id, ori_tweet_username
                    ]
        # Append to dataframe - db_tweets
        db_tweets.loc[len(db_tweets)] = ith_tweet
        
    # Obtain timestamp in a readable format
    to_csv_timestamp = datetime.today().strftime('%Y%m%d_%H%M%S')
    path = os.getcwd()
    filename = path + '/scrap_results/' + 'pajak sembako_' + to_csv_timestamp + '.csv'
    db_tweets.to_csv(filename, index = False)

    program_end = time.time()
    print('Data saving has completed!')
    print('Total time taken to scrap is {} minutes.'.format(round(program_end - program_start)/60, 2))

If __name__ == '__main__':
    # Credentials
    consumer_key = <consumer_key>
    consumer_secret = <consumer_secret>
    access_token = <access_token>
    access_secret = <access_secret>

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    raw_tweets = scraptweets('pajak sembako', 100000)
    store_tweets(raw_tweets)