import tweepy
import datetime
import time
import json
import pprint


def mined_tweet(tweet):
  mined = {
    'tweet_id': tweet.id_str,
    'name': tweet.user.name,
    'screen_name': tweet.user.screen_name,
    'retweet_count': tweet.retweet_count,
    'text': tweet._json["full_text"],
    'mined_at': datetime.datetime.now(),
    'created_at': tweet.created_at,
    'favorite_count': tweet.favorite_count,
    'hashtags': tweet.entities['hashtags'],
    'status_count': tweet.user.statuses_count,
  }
  return mined

def mined_user(user):
  mined = {
    'user_id': user.id_str,
    'last_tweet_mined': "",
    'name': user.name,
    'screen_name': user.screen_name,
    'profile_image_url': user.profile_image_url,
    'verified': user.verified
  }
  return mined

class TwittterMiner(object):
  result_limit = 20
  tweets = []
  api = False
  twitter_keys = {}
  db = {}

  def __init__(self, keys_dict=twitter_keys, api=api, result_limit=20):
    self.twitter_keys = keys_dict

    auth = tweepy.OAuthHandler(keys_dict['consumer_key'], keys_dict['consumer_secret'])
    auth.set_access_token(keys_dict['access_token'], keys_dict['access_token_secret'])

    self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    self.result_limit = result_limit

  def mine_user_tweets(self, user, mongo_client, max_pages=5):
    data = []
    tweets = tweepy.Cursor(self.api.user_timeline, screen_name=user, tweet_mode="extended").items(1)
    for tweet in tweets:
      if tweet.created_at < datetime.datetime(2020, 3, 3, 0, 0, 0, 0):
        break
      if tweet.in_reply_to_status_id == None and not hasattr(tweet, 'retweeted_status'):
        mined = mined_tweet(tweet)
        data.append(mined)
        user_to_update = mongo_client.get_user(user)
        if user_to_update["last_tweet_mined"] < mined["tweet_id"]:
          mongo_client.update_last_tweet_mined(mined["tweet_id"], user)
        print("Mining from user ---------------")
        pprint.pprint(mined)
        self.append_replies(data, user, tweet.id_str)
    return data

  def append_replies(self, data, user, since_id):
    replies = tweepy.Cursor(self.api.search, q='to:{}'.format(user), since_id=since_id, tweet_mode='extended').items(50)
    for reply in replies:
      try:
        if not hasattr(reply, 'in_reply_to_status_id_str'):
          continue
        if reply.in_reply_to_status_id_str == since_id:
          reply_mined_object = mined_tweet(reply)
          data.append(reply_mined_object)
          print("Mining from reply: ---------------")
          pprint.pprint(reply_mined_object)
          #print("reply of tweet:{}".format(reply.full_text))
      except Exception as e:
        print("Failed while fetching replies {}".format(e))
        break
  
  def mine_users(self, screen_names_list):
    data = []
    for screen_name in screen_names_list:
      new_user = self.api.get_user(screen_name=screen_name)
      user = mined_user(new_user)
      data.append(user)
    return data
  