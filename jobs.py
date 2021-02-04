import os
from dotenv import load_dotenv
from mongo_client import MongoTwitterClient

load_dotenv()
# Twitter keys
twitter_keys = {
  "consumer_key": os.getenv("TWITTER_API_KEY"),
  "consumer_secret": os.getenv("TWITTER_API_SECRET_KEY"),
  "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
  "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
}

# MongoDB parameters
host = os.getenv("MONGO_DB_HOST")
port = int(os.getenv("MONGO_DB_PORT"))

# Initialization
mongo_client = MongoTwitterClient(host, port, isTest=True)
## Job to update database
mongo_client.tokenize_text()
