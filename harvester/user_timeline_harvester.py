import couchdb
import tweepy
import sys
import json
import time
import math
from datetime import datetime
from mpi4py import MPI

from util import *

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n_tasks = comm.Get_size()

## load the parameters
argv = sys.argv
for i in range(len(argv)):
    if argv[i] == "-master_node_ip":
        if (i<len(argv)-1) and (argv[i+1][0] != '-'):
            master_node_ip = argv[i+1]
        else :
            print("Invalid arguments!")
            exit()
    elif argv[i] == "-username":
        if (i<len(argv)-1) and (argv[i+1][0] != '-'):
           username = argv[i+1]
        else :
            print("Invalid arguments!")
            exit()
    elif argv[i] == "-password":
        if (i<len(argv)-1) and (argv[i+1][0] != '-'):
            password = argv[i+1]
        else :
            print("Invalid arguments!")
            exit()
    elif argv[i] == "-couchdb_port":
        if (i<len(argv)-1) and (argv[i+1][0] != '-'):
            couchdb_port = int(argv[i+1])
        else :
            print("Invalid arguments!")
            exit()

## load the API key, API secret key, access token and access token secret 
f = open("auth.json", "r")
auth_dict = json.load(f)
f.close()

n_dev_account = len(auth_dict.keys())

# if rank is lower than #developer account, assign an account to this process
if rank < n_dev_account:
    dev_account = list(auth_dict.keys())[rank]
# else, end the program since there is no free developer account for this process
else :
    exit()


# load the specific API key, API secret key, access token and access token secret
API_key = auth_dict[dev_account]["API_key"]
API_secret_key = auth_dict[dev_account]["API_secret_key"]
access_token = auth_dict[dev_account]["access_token"]
access_token_secret = auth_dict[dev_account]["access_token_secret"]

auth = tweepy.OAuthHandler(API_key, API_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# check the rate limit and store it
remain_request = api.rate_limit_status("statuses")["resources"]["statuses"]["/statuses/user_timeline"]["remaining"]
if remain_request>1:
    print(f"Note: {remain_request} timeline requests remaining / 15-min window.")
else:
    print(f"Note: {remain_request} timeline request remaining / 15-min window.")
start_time = time.time()
last_check_time = time.time()

## allocate  the couchdb API
node_ip = allocate_node_ip(master_node_ip, username, password, couchdb_port, rank)
address = f"http://{username}:{password}@{node_ip}:{couchdb_port}"
couchdb_server = couchdb.Server(address)

user_db_name = "clean_user"
tweet_db_name = "raw_tweets_from_timeline"

try:
    user_db = couchdb_server[user_db_name]
    tweet_db = couchdb_server[tweet_db_name]
except:
    print(f"There is no targeted database on the server.")
    exit()

user_ids = list(user_db)
n_user = len(list(user_db))

# assign range of doc_id to each process
start_pos = round(rank*n_user/n_tasks)
end_pos = round((rank+1)*n_user/n_tasks)
assigned_user_ids = user_ids[start_pos:end_pos]

user_count = 0

for i in assigned_user_ids:
    page_cursor = tweepy.Cursor(api.user_timeline, id = i, count=200, trim_user = True, include_rts = False, tweet_mode='extended').pages()
    page_fetched = 0
    user_count += 1
    
    while (True):
        try:
            page = page_cursor.next()
        except StopIteration: # All available tweets are harvested
            print("All tweets from user's timeline are harvested.")
            break
        except: # unexpected http connnection error
            print("Something else went wrong.")
            break

        remain_request -= 1
        page_fetched += 1

        print(f"Fetch Page: {page_fetched}")
        for tweet in page:
            # here use try & except to avoid duplicated tweets
            # duplicated tweets will have the same tweet_id
            
            # save documents to tweet_db
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
                    "hashtags": tweet_formated["entities"]["hashtags"],
                    "user_location": user_db[i]["location"],
                    "user_created_at": user_db[i]["created_at"],
                    "uniform_location": user_db[i]["uniform_location"]
                })
            
            except:
                
                continue
        # if the time it is time for Twitter API to reset the rate limit count, refresh the value
        if (time.time()-last_check_time)>=15*60:
            remain_request = api.rate_limit_status("statuses")["resources"]["statuses"]["/statuses/user_timeline"]["remaining"]
            last_check_time = time.time()
            
            print(f"The request limit should be reset, now {remain_request} request(s) available")
        
        # if the requests are run out in 15 min window, wait for a while until the rate limit reset
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
print("Finish!")