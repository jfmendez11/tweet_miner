import os
from dotenv import load_dotenv
from twitter_miner import TwittterMiner
import pprint
from pymongo import MongoClient

def main():
  load_dotenv()
  twitter_keys = {
    "consumer_key": os.getenv("TWITTER_API_KEY"),
    "consumer_secret": os.getenv("TWITTER_API_SECRET_KEY"),
    "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
    "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
  }

  miner = TwittterMiner(keys_dict=twitter_keys, result_limit=20)
  data = miner.mine_user_tweets(user="agaviriau", max_pages=10)
  pprint.pprint(data)
  