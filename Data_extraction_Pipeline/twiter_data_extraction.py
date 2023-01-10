import numpy as np
import tweepy
import json
from tweepy import OAuthHandler
import csv
import re
import nltk
from textblob import TextBlob
from nltk.corpus import stopwords
from textblob import Word
from nltk.util import ngrams
from nltk.stem import PorterStemmer
from wordcloud import WordCloud, STOPWORDS
from nltk.tokenize import word_tokenize

query = "Elon musk -is:retweet"
file_name = "tweets.txt"
id = "1177659818661728257"
tweet_id = "1599470470029783040"

#credentials
consumer_key = "b6jvfgKycMKlS5JIJFCaMEe3c"
consumer_secret = "8KgvZ5gFXyou64NcoHjNo7pR1C5LHIa3Ski1ShPUjy3Hoaa2gp"
access_token = "1487368033400389632-3Kewf1UVp7GulgX994oPk0aBOou3HL"
access_token_secret = "NjdhxIWI0dlU2QkKFmzRXnyTolLZb34fuO8I816t2K68n"
Bearer_TOken = "AAAAAAAAAAAAAAAAAAAAAAk0kAEAAAAAOwS1qY%2FOmkDE2ER9m83X3OWHlFo%3D8IfbQIcYDX57qFAdl1q3GVjGhAf7IH8fkf4CSruZPH5pUUckZN"

client = tweepy.Client(Bearer_TOken,consumer_key,consumer_secret,access_token,access_token_secret)

auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth=auth,wait_on_rate_limit=True)

#create tweet
def create_tweet(text):
    client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
    response = client.create_tweet(text=text)
    print(response.data)

# create_tweet("Hello world !!")

#Fetching tweets
def fetch_and_save_tweets(query, file_name, max_results=100):
    i = 0
    response = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=['lang'],
        user_fields=['profile_image_url','location','created_at','description','public_metrics','verified','url'], expansions=['author_id'])

    users = {u['id']: u for u in response.includes['users']}
    # print(response)
    # print(users)

    with open(file_name, '+a') as fileHandlar:
        for tweet in response.data:
            if users[tweet.author_id]:
                user = users[tweet.author_id]
                fileHandlar.write("\n")
                fileHandlar.write("Tweet_No: %s.\n" % str(i))
                fileHandlar.write("User Id: %s\n" % str(user.id))
                fileHandlar.write("User_name: %s\n" % user.username)
                fileHandlar.write("Name: %s\n" % user.name)
                fileHandlar.write("User Created at: %s\n" % str(user.created_at))
                fileHandlar.write("Description: %s\n" % str(user.description))
                fileHandlar.write("Tweet: %s\n" % tweet.text)
                fileHandlar.write("Location: %s\n" % str(user.location))
                fileHandlar.write("profile_image_url: %s\n" % str(user.profile_image_url))
                fileHandlar.write("public_metrics: %s\n" % str(user.public_metrics))
                fileHandlar.write("url: %s\n" % str(user.url))
                fileHandlar.write("verified: %s\n" % str(user.verified))
                fileHandlar.write("Language: %s\n" % tweet.lang)
                fileHandlar.write("Tweet id: %s\n" % str(tweet.id))
                fileHandlar.write("\n")
                i+=1

                # print("User Id: "+str(user.id)) #The unique identifier of this user.
                # print("User_name: "+user.username)
                # print("Name: "+user.name)
                # print("User Created at: "+str(user.created_at)) #The UTC datetime that the user account was created on Twitter.
                # print("Description: "+str(user.description)) #The text of this user's profile description (also known as bio), if the user provided one.
                # print("Tweet: "+tweet.text)
                # print("Location: "+str(user.location))  #The location specified in the user's profile, if the user provided one.
                # print("profile_image_url: "+str(user.profile_image_url)) #User's profile image
                # print("public_metrics: "+str(user.public_metrics))  #Contains details about activity for this user.
                # print("url: "+str(user.url))  #The URL specified in the user's profile, if present.
                # print("verified: "+str(user.verified))  #Indicates if this user is a verified Twitter User.
                # print("Language: "+tweet.lang) 
                # print("Tweet id: "+str(tweet.id))
                # print('\n')

# fetch_and_save_tweets(query=query, file_name=file_name)


#get counts of recent tweets 
def get_recent_tweet_counts(query, granularituy="day"):
    counts = client.get_recent_tweets_count(query=query, granularity=granularituy)
    for count in counts.data:
        print(count)

# get_recent_tweet_counts(query=query)

def get_userId(user_names):
    users = client.get_users(usernames=user_names)
    for user in users.data:
        print(user.id)

# get_userId(['Daddyfromtheot2', 'deevine212'])

def get_user_tweets(id):
    tweets = client.get_users_tweets(id=id)
    for tweet in tweets.data:
        print(tweet.text)
        print('\n')

# get_user_tweets(id)

def get_users_followers(id):
    users = client.get_users_followers(id=id, user_fields=['profile_image_url'], max_results=10)
    for user in users.data:
        print(user.id)
        print(user.profile_image_url)
        print("\n")
    
# get_users_followers(id=id)

def get_users_following(id):
    users = client.get_users_following(id=id, user_fields=['profile_image_url'], max_results=10)
    for user in users.data:
        print(user.id)
        print(user.profile_image_url)
        print("\n")

# get_users_following(id=id)

def get_liking_users(tweet_id):
    client = tweepy.Client(Bearer_TOken)
    users = client.get_liking_users(id=tweet_id,user_fields=['profile_image_url'], max_results=10)
    if users.data:
        for user in users.data:
            print(user.id)
            print(user.username)
            print(user.name)
            print(user.profile_image_url)
            print('\n')

# get_liking_users(tweet_id=tweet_id)

def get_retweeters(tweet_id):
    client = tweepy.Client(Bearer_TOken)
    users = client.get_retweeters(id=tweet_id, user_fields=['profile_image_url'], max_results=10)
    if users.data:
        for user in users.data:
            print(user.id)
            print(user.username)
            print(user.name)
            print(user.profile_image_url)
            print('\n')

# get_retweeters(tweet_id=tweet_id)

def process_tweets(tweet):
    tweet = tweet.lower()

    tweet = re.sub(r'(\\u[0-9A-Fa-f]+)', r'', tweet)
    tweet = re.sub(r'[^\x00-\x7f]', r'', tweet)
    tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    tweet = re.sub('[\n]+', ' ', tweet)
    tweet = re.sub(r'[^\w]', ' ', tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = tweet.replace(':)', '')
    tweet = tweet.replace(':(', '')
    tweet = "".join(i for i in tweet if not i.isdigit())
    tweet = re.sub(r'(\!)\1+', ' ', tweet)
    tweet = re.sub(r'(\?)\1+', ' ', tweet)
    tweet = re.sub(r'(\.)\1+', ' ', tweet)
    ##lemma
    tweet = " ".join([Word(word).lemmatize() for word in tweet.split()])
    ##stemmer
    # st = PorterStemmer()
    # tweet = " ".join([st.stem(word) for word in tweet.split()])
    #Removes emoticons from text
    tweet = re.sub(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:', '', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet

tweet_sample= "How to take control of your #debt https://personal.vanguard.com/us/insights/saving-investing/debt-management.#Best advice for #family #financial #success (@PrepareToWin)"

print(process_tweets(tweet_sample))
