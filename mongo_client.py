import pymongo
from pymongo import MongoClient
import pprint

class MongoTwitterClient:
  host = ""
  port = 0
  client = {}
  db = {}
  
  def __init__(self, host, port):
    self.client = MongoClient(host, port)
    self.db = self.client["tweet_miner"]
    if len(list(self.db.tweets.index_information())) < 2:
      result = self.db.tweets.create_index([('tweet_id', pymongo.DESCENDING)], unique = True)
      pprint.pprint(result)
    if len(list(self.db.users.index_information())) < 3:
      result = self.db.users.create_index([('screen_name', pymongo.ASCENDING), ('user_id', pymongo.ASCENDING)], unique = True)
      pprint.pprint(result)
  
  def insert_tweet(self, tweet):
    tweets_collection = self.db["tweets"]
    result = tweets_collection.insert_one(tweet)
    pprint.pprint(result)
    
  def insert_many_tweets(self, tweets):
    tweets_collection = self.db["tweets"]
    result = tweets_collection.insert_many(tweets)
    pprint.pprint(result)
    
  def insert_user(self, user):
    users_collection = self.db["users"]
    result = users_collection.insert_one(user)
    pprint.pprint(result)
    
  def insert_many_users(self, users):
    users_collection = self.db["users"]
    result = users_collection.insert_many(users)
    pprint.pprint(result)