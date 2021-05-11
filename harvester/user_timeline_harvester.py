import couchdb
import tweepy
import sys
import json
import time
from datetime import datetime

from var import * 

## set the Twitter API
auth = tweepy.OAuthHandler(JiarChen108_API_key, JiarChen108_API_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

remain_request = api.rate_limit_status("statuses")["resources"]["statuses"]["/statuses/user_timeline"]["remaining"]
if remain_request>1:
    print(f"Note: {remain_request} timeline requests remaining / 15-min window.")
else:
    print(f"Note: {remain_request} timeline request remaining / 15-min window.")
start_time = time.time()
last_check_time = time.time()

val = input("Continue? (Y/N): ")
if val.lower() in ["n", "no", "false"]:
    exit(0)


## set the couchdb API
address = f"http://{username}:{password}@{MASTER_NODE_IP}:{couchdb_port}"
# Note: For urllib3 version<1.26.0, please use the line below instead.
# address = f"https://{username}:{password}@{MASTER_NODE_IP}:{couchdb_port}"
couchdb_server = couchdb.Server(address)

user_db_name = "clean_user"
tweet_db_name = "raw_tweets_from_timeline"

try:
    tweet_db = couchdb_server.create(tweet_db_name)
except:
    tweet_db = couchdb_server[tweet_db_name]

try:
    user_db = couchdb_server[user_db_name]
except:
    print(f"There is no database called {user_db_name} on the server.")

#city_list = ["melbourne", "sydney", "adelaide", "brisbane", "perth", "canberra", "darwin", "hobart"]

for i in user_db:
    page_cursor = tweepy.Cursor(api.user_timeline, id = i, count=200, trim_user = True, include_rts = False, tweet_mode='extended').pages()
    page_fetched = 0

    while (True):
        try:
            page = page_cursor.next()
        except:
            print("All tweets from user's timeline are harvested.")
            break
        #print(api.rate_limit_status("statuses")["resources"]["statuses"]["/statuses/user_timeline"]["remaining"])
        remain_request -= 1
        page_fetched += 1

        print(f"Fetch Page: {page_fetched}")
        for tweet in page:
            # here use try & except to avoid duplicated tweets
            # duplicated tweets will have the same tweet_id
            
            tweet_formated = tweet._json
            if "retweeted_status" in tweet_formated.keys():
                continue
                #print(tweet_formated)

            if datetime.strptime(tweet_formated["created_at"],'%a %b %d %H:%M:%S +0000 %Y') < datetime(2020, 1, 1):
                break
            try:
                tweet_db.save({
                    "_id": str(tweet_formated["id"]),
                    "created_at": tweet_formated["created_at"],
                    "full_text": tweet_formated["full_text"],
                    "user_location": user_db[i]["location"],
                    "uniform_location": user_db[i]["uniform_location"]
                })
            
            except:
                #print("One duplicated tweets caught!")
                continue
           
        if (time.time()-last_check_time)>=15*60:
            remain_request = api.rate_limit_status("statuses")["resources"]["statuses"]["/statuses/user_timeline"]["remaining"]
            last_check_time = time.time()
            
            print(f"The request limit should be reset, now {remain_request} request(s) available")
        
        if remain_request <=1:
            # recheck it with Twitter API
            remain_request = api.rate_limit_status("statuses")["resources"]["statuses"]["/statuses/user_timeline"]["remaining"]
            
            while (remain_request<=1):
                sleep_time = 15*60 - (time.time()-last_check_time)
                last_check_time = time.time()
                print(f"Start to sleep {round(sleep_time, 2)}s to wait for the limit resetting.")
                time.sleep(sleep_time)
                remain_request = api.rate_limit_status("statuses")["resources"]["statuses"]["/statuses/user_timeline"]["remaining"]

            last_check_time = time.time()


end_time = time.time()
print(f"harvest_time={round(end_time-start_time, 2)}")
print(api.rate_limit_status("statuses")["resources"]["statuses"]["/statuses/user_timeline"]["remaining"])

exit()

print(api.rate_limit_status("search"))
#print(JiarChen108_API_key)

#print("This is the name of the program:", sys.argv[0])
  
print("Argument List:", str(sys.argv))