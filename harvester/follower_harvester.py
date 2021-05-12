import couchdb
import tweepy
import sys
import json
import time
from datetime import datetime

from var import * 

auth = tweepy.OAuthHandler(JiarChen108_API_key, JiarChen108_API_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

ids = []
remain_request = api.rate_limit_status("followers")
#/followers/list'
 
print(remain_request)