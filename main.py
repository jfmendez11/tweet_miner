import os
from dotenv import load_dotenv
from twitter_miner import TwittterMiner
import pprint
from mongo_client import MongoTwitterClient

screen_names = [
  "Uniandes",
  "agaviriau",
  "DEUniandes",
  "inguniandes",
  "facisouniandes",
  "UniandesDerecho",
  "MediUniandes",
  "CPolUniandes",
  "EconomiaUAndes",
  "CiderUniandes",
  "EdCoUniandes",
  "AdmonUniandes",
  "GobiernoUAndes",
  "Ceper_Uniandes",
  "CulturaUniandes",
  "CienciasUAndes",
  "CEFAUniandes",
  "_CONSEFE",
  "IEEEUniandes",
  "CEGOBUniandes",
  "CeuDerecho",
  "ceuniandino",
  "cerosetenta",
  "Rev_Ingenieria",
  "ConectaTE_U",
  "BecadosUniandes",
  "PosgradosUAndes",
  "AntrUniandes",
  "CTPUniandes",
  "UniandesCEIM",
  "admision_uandes",
  "DeportesUniande"
]

def main():
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
  miner = TwittterMiner(keys_dict=twitter_keys)
  mongo_client = MongoTwitterClient(host, port)
  
  # Get user info if necessary
  if mongo_client.should_insert_users():
    pprint.pprint("Mining users from Twitter")
    users = miner.mine_users(screen_names)
    mongo_client.insert_many_users(users)
  # If not, get user info from DB
  else:
    users = mongo_client.get_users()
  
  # Mine the user tweets
  for user in users:
    pprint.pprint("Mining from " + user["screen_name"])
    tweets = miner.mine_user_tweets(user=user["screen_name"], mongo_client=mongo_client, since_id=user["last_tweet_mined"])
    try:
      # Mine the tweets
      mongo_client.insert_many_tweets(tweets)
      mongo_client.tokenize_text()
    except Exception as e:
      # The user has no tweets
      print("Could not insert tweets from {}. Exception {}".format(user["screen_name"], e))
      continue
  
if __name__ == '__main__':
  main()
