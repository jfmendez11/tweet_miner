import pymongo
from pymongo import MongoClient
import pprint
from tweet_tokenizer import TextCleaner

class MongoTwitterClient:
  host = ""
  port = 0
  client = {}
  db = {}
  text_cleaner = {}
  # Class initialization
  def __init__(self, host, port, isTest = False):
    print(host)
    self.client = MongoClient(host, port)
    self.db = self.client["tweet_miner" if not isTest else "tweet_miner_test"]
    if len(list(self.db.tweets.index_information())) < 2:
      result = self.db.tweets.create_index([('tweet_id', pymongo.DESCENDING), ('text', pymongo.TEXT)], unique=True)
      pprint.pprint("Created tweets collection")
    if len(list(self.db.users.index_information())) < 2:
      result = self.db.users.create_index([('screen_name', pymongo.ASCENDING), ('user_id', pymongo.ASCENDING), ('last_tweet_mined', pymongo.ASCENDING)], unique=True)
      pprint.pprint("Created user colleciton")
    
    self.text_cleaner = TextCleaner()
  
  # TWEETS
  def insert_tweet(self, tweet):
    tweets_collection = self.db["tweets"]
    result = tweets_collection.insert_one(tweet)
    pprint.pprint("Successfully mined {} tweets".format(len(result.inserted_ids)))
    
  def insert_many_tweets(self, tweets):
    tweets_collection = self.db["tweets"]
    result = tweets_collection.insert_many(tweets)
    pprint.pprint("Successfully mined {} tweets".format(len(result.inserted_ids)))
  
  def tokenize_text(self):
    tweets_collection = self.db["tweets"]
    query = { "tokenized_text": { "$size": 0 } }
    tweets = tweets_collection.find(query)
    for tweet in tweets:
      tweet_to_update = { "tweet_id": tweet['tweet_id'] }
      tokenized_text = self.text_cleaner.lemmatize(tweet['text'], tweet['hashtags'])
      update_value = { "$set": { "tokenized_text": tokenized_text } }
      if not tokenized_text:
        self.db["tweets"].delete_one(tweet_to_update)
      else:
        self.db["tweets"].update_one(tweet_to_update, update_value)
  
  def delete_tokens(self):
    tweets_collection = self.db["tweets"]
    query = {"tokenized_text": {"$gt": []}}
    tweets = tweets_collection.find(query)
    for tweet in tweets:
      tweet_to_update = { "tweet_id": tweet['tweet_id'] }
      update_value = { "$set": { "tokenized_text": [] } }
      self.db["tweets"].update_one(tweet_to_update, update_value)
  
  # USERS
  def get_users(self):
    users_collection = self.db["users"]
    return users_collection.find({})
  
  def get_user(self, screen_name):
    users_collection = self.db["users"]
    return users_collection.find_one({"screen_name": screen_name})
  
  def insert_user(self, user):
    users_collection = self.db["users"]
    result = users_collection.insert_one(user)
    pprint.pprint("Successfully mined {} information".format(user["screen_name"]))
    
  def insert_many_users(self, users):
    users_collection = self.db["users"]
    result = users_collection.insert_many(users)
    pprint.pprint("Successfully mined {} users".format(len(result.inserted_ids)))
    
  def update_last_tweet_mined(self, tweet_id, user_screen_name):
    user_to_update = { "screen_name": user_screen_name }
    update_value = { "$set": { "last_tweet_mined": tweet_id } }
    self.db["users"].update_one(user_to_update, update_value)
    
  def should_insert_users(self):
    tweets_collection = self.db["users"]
    return tweets_collection.count_documents({}) == 0