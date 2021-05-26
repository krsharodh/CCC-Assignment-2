import couchdb
import tweepy
import sys
import json
import time
from datetime import date
from datetime import timedelta 
from mpi4py import MPI
import math

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
    elif argv[i] == "-location":
        if (i<len(argv)-1) and (argv[i+1][0] != '-'):
            search_location = argv[i+1]
        else :
            print("Invalid arguments!")
            exit()

# set keywords for search
keyword = "vaccin OR COVID OR COVAX OR SARS-CoV-2 OR pfizer OR astrazeneca OR az OR moderna"

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
remain_request = api.rate_limit_status("search")["resources"]["search"]["/search/tweets"]["remaining"]
if remain_request>1:
    print(f"Note: {remain_request} search requests remaining / 15-min window.")
else:
    print(f"Note: {remain_request} search request remaining / 15-min window.")

start_time = time.time()
last_check_time = time.time()

## set the couchdb API
node_ip = allocate_node_ip(master_node_ip, username, password, couchdb_port, rank)
address = f"http://{username}:{password}@{node_ip}:{couchdb_port}"
couchdb_server = couchdb.Server(address)

tweet_db_name = "recent_search_tweets"
user_db_name = "user"

tweet_db = couchdb_server[tweet_db_name]
user_db = couchdb_server[user_db_name]


geocode = {"australia": "-25.610112,134.354805,2240km", 
"sydney":"-33.63,150.89,85km", 
"melbourne":"-37.80,145.11,75km", 
"brisbane":"-27.33,152.81,109km", 
"perth":"-32.12,115.68,75km"
}

# cities we get interested in
city_list = ["melbourne", "sydney", "adelaide", "brisbane", "perth", "canberra", "darwin", "hobart"]

# assign period to each process
today = date.today()
period = math.ceil(7/(min(n_dev_account, n_tasks)))

until_date = today + timedelta(days=1-(rank*period))
since_date = today + timedelta(days=1-((rank+1)*period))

if rank == (min(n_dev_account, n_tasks)-1):
    page_cursor = tweepy.Cursor(api.search, q = keyword, until=str(until_date), lang="en", count = 100, geocode=geocode[search_location], tweet_mode='extended').pages()
    
else:
    page_cursor = tweepy.Cursor(api.search, q = keyword, since=str(since_date),until=str(until_date), lang="en", count = 100, geocode=geocode[search_location], tweet_mode='extended').pages()



page_fetched = 0

while (True):
    try:
        page = page_cursor.next()
    except StopIteration: # All available tweets are harvested
        print("All tweets in the time interval are harvested.")
        break
    except: # unexpected http connnection error
        print("Something else went wrong.")
        break

    remain_request -= 1
    
    for tweet in page:
        # here use try & except to avoid duplicated tweets
        # duplicated tweets will have the same tweet_id
        
        # save documents to tweet_db
        tweet_formated = tweet._json
        user_list = [tweet_formated["user"]]
        if "retweeted_status" in tweet_formated.keys():
            tweet_formated = tweet_formated["retweeted_status"]
            user_list.append(tweet_formated["user"])
            
        try:
            tweet_db.save({
                "_id": str(tweet_formated["id"]),
                "created_at": tweet_formated["created_at"],
                "full_text": tweet_formated["full_text"],
                "hashtags": tweet_formated["entities"]["hashtags"],
                "user": tweet_formated["user"],
                "search_location": search_location
            })
        
        except:
            
            continue
        
        # save documents to user_db
        for user_info in user_list:
            
            uniform_location = "NA"
            for c in city_list:
                if c in user_info["location"].lower():
                    uniform_location = c
                    break
            try:
                user_db.save({
                            "_id": str(user_info["id"]),
                            "name": user_info["name"],
                            "screen_name": user_info["screen_name"],
                            "location": user_info["location"],
                            "uniform_location": uniform_location,
                            "created_at": user_info["created_at"]
                        }) 

            except:
                
                pass
    
    page_fetched += 1
    
    # if the time it is time for Twitter API to reset the rate limit count, refresh the value
    if (time.time()-last_check_time)>=15*60:
        remain_request = api.rate_limit_status("search")["resources"]["search"]["/search/tweets"]["remaining"]
        last_check_time = time.time()
        print(f"The request limit should be reset, now {remain_request} request(s) available")
    
    # if the requests are run out in 15 min window, wait for a while until the rate limit reset
    if remain_request <=1:
        # recheck it with Twitter API
        remain_request = api.rate_limit_status("search")["resources"]["search"]["/search/tweets"]["remaining"]
        
        while (remain_request<=1):
            sleep_time = 15*60 - (time.time()-last_check_time)
            last_check_time = time.time()
            print(f"Start to sleep {round(sleep_time, 2)}s to wait for the limit resetting.")
            time.sleep(sleep_time)
            remain_request = api.rate_limit_status("search")["resources"]["search"]["/search/tweets"]["remaining"]

        last_check_time = time.time()


end_time = time.time()
print(f"harvest_time={round(end_time-start_time, 2)}")
print("Finish!")
