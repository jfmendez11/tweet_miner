import tweepy
import datetime
import time
import json


def mined_object(tweet):
  mined = {
    'tweet_id': tweet.id_str,
    'name': tweet.user.name,
    'screen_name': tweet.user.screen_name,
    'retweet_count': tweet.retweet_count,
    'text': tweet._json["full_text"],
    'mined_at': datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
    'created_at': tweet._json["created_at"],
    'favourite_count': tweet.favorite_count,
    'hashtags': tweet.entities['hashtags'],
    'status_count': tweet.user.statuses_count,
  }
  return mined


class TweetMiner(object):
  result_limit = 20
  tweets = []
  api = False
  twitter_keys = {}

  def __init__(self, keys_dict=twitter_keys, api=api, result_limit=20):
    self.twitter_keys = keys_dict

    auth = tweepy.OAuthHandler(keys_dict['consumer_key'], keys_dict['consumer_secret'])
    auth.set_access_token(keys_dict['access_token'], keys_dict['access_token_secret'])

    self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    self.result_limit = result_limit

  def mine_user_tweets(self, user, max_pages=5):
    data = []
    tweets = tweepy.Cursor(self.api.user_timeline, screen_name=user, tweet_mode="extended").items(
      max_pages * self.result_limit)
    for tweet in tweets:
      if tweet.in_reply_to_status_id == None and not hasattr(tweet, 'retweeted_status'):
        mined = mined_object(tweet)
        data.append(mined)
        self.append_replies(data, user, tweet.id_str)
    return data

  def append_replies(self, data, user, since_id):
    replies = tweepy.Cursor(self.api.search, q='to:{}'.format(user), since_id=since_id, tweet_mode='extended').items(50)
    for reply in replies:
      try:
        if not hasattr(reply, 'in_reply_to_status_id_str'):
          continue
        if reply.in_reply_to_status_id_str == since_id:
          reply_mined_object = mined_object(reply)
          data.append(reply_mined_object)
          print("reply of tweet:{}".format(reply.full_text))
      except Exception as e:
        print("Failed while fetching replies {}".format(e))
        break
