import couchdb
import tweepy
import sys
import json
import time
from datetime import date
from datetime import timedelta 
from mpi4py import MPI
import math

from var import * 
from util import *

comm = MPI.COMM_WORLD
rank = comm.rank
n_tasks = comm.size
#rank = 2
#n_tasks = 4

argv = sys.argv
for i in range(len(argv)):
    if argv[i] == "-keyword":
        if (i<len(argv)-1) and (argv[i+1][0] != '-'):
            keyword = argv[i+1]
        else :
            print("Invalid arguments!")
            exit()
    elif argv[i] == "-location":
        if (i<len(argv)-1) and (argv[i+1][0] != '-'):
            search_location = argv[i+1]
        else :
            print("Invalid arguments!")
            exit()
    elif argv[i] == "-rank":
        if (i<len(argv)-1) and (argv[i+1][0] != '-'):
            rank = int(argv[i+1])
        else :
            print("Invalid arguments!")
            exit()

keyword = "vaccin OR COVID OR COVAX OR SARS-CoV-2 OR pfizer OR astrazeneca OR az OR moderna"

## load the API key, API secret key, access token and access token secret 
f = open("auth.json", "r")
auth_dict = json.load(f)

n_dev_account = len(auth_dict.keys())

# if rank is lower than #developer account, assign an account to this process
if rank < n_dev_account:
    dev_account = list(auth_dict.keys())[rank]
# else, end the program since there is no free developer account for this process
else :
    exit()

#print(rank)
#print(dev_account)
#print(search_location)


# load the specific API key, API secret key, access token and access token secret

API_key = auth_dict[dev_account]["API_key"]
API_secret_key = auth_dict[dev_account]["API_secret_key"]
access_token = auth_dict[dev_account]["access_token"]
access_token_secret = auth_dict[dev_account]["access_token_secret"]


auth = tweepy.OAuthHandler(API_key, API_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

remain_request = api.rate_limit_status("search")["resources"]["search"]["/search/tweets"]["remaining"]
if remain_request>1:
    print(f"Note: {remain_request} search requests remaining / 15-min window.")
else:
    print(f"Note: {remain_request} search request remaining / 15-min window.")

start_time = time.time()
last_check_time = time.time()

"""
val = input("Do you want to continue? [Y/n] ")
if val.lower() in ["n", "no", "false"]:
    exit(0)
"""

## set the couchdb API

#address = f"http://{username}:{password}@{MASTER_NODE_IP}:{couchdb_port}"
# Note: For urllib3 version<1.26.0, please use the line below instead.
# address = f"https://{username}:{password}@{MASTER_NODE_IP}:{couchdb_port}"

node_ip = allocate_node_ip(master_node_ip, username, password, couchdb_port, rank, n_tasks)
address = f"http://{username}:{password}@{node_ip}:{couchdb_port}"
couchdb_server = couchdb.Server(address)

tweet_db_name = "tweets_test4"
user_db_name = "user4"

if rank == 0:
    try:
        tweet_db = couchdb_server.create(tweet_db_name)
    except:
        tweet_db = couchdb_server[tweet_db_name]

    try:
        user_db = couchdb_server.create(user_db_name)
    except:
        user_db = couchdb_server[user_db_name]

comm.Barrier()

if rank != 0:
    tweet_db = couchdb_server[tweet_db_name]
    user_db = couchdb_server[user_db_name]

#testdb = couchdb_server["test"]
#db.save({'_id':"1", 'text':"Hello CouchDB!", 'User':"Jiarui"})
#db.save({'_id':"2", 'text':"My greetings to CouchDB!", 'User':"Jiarui"})
#db.save({'_id':"3", 'text':"こんにちは、 CouchDB!", 'User':"Jiarui"})
#db.save({'_id':"4", 'text':"你好，CouchDB!", 'User':"Jiarui"})

geocode = {"australia": "-25.610112,134.354805,2240km", 
"sydney":"-33.63,150.89,85km", 
"melbourne":"-37.80,145.11,75km", 
"brisbane":"-27.33,152.81,109km", 
"perth":"-32.12,115.68,75km"
}
city_list = ["melbourne", "sydney", "adelaide", "brisbane", "perth", "canberra", "darwin", "hobart"]

# until="2021-05-08",
today = date.today()
#start_date = 
print(today + timedelta(days=1))
period = math.ceil(7/(min(n_dev_account, n_tasks)))

until_date = today + timedelta(days=1-(rank*period))
since_date = today + timedelta(days=1-((rank+1)*period))

#page_cursor = tweepy.Cursor(api.search, q = keyword, since="2021-04-29", until=f"{today.year}-{today.month}-{today.day+1}", lang="en", count = 100, geocode=geocode[search_location], tweet_mode='extended').pages()
#print(f"Rank: {rank}, since={since_date}, until={until_date}")

if rank == (min(n_dev_account, n_tasks)-1):
    page_cursor = tweepy.Cursor(api.search, q = keyword, until=str(until_date), lang="en", count = 100, geocode=geocode[search_location], tweet_mode='extended').pages()
    #print(f"Rank: {rank}, until={until_date}")
else:
    page_cursor = tweepy.Cursor(api.search, q = keyword, since=str(since_date),until=str(until_date), lang="en", count = 100, geocode=geocode[search_location], tweet_mode='extended').pages()
    #print(f"Rank: {rank}, since={since_date}, until={until_date}")

#page_cursor = tweepy.Cursor(api.search, q = keyword, since="2021-05-01", lang="en", count = 100, geocode=geocode, tweet_mode='extended').pages()

page_fetched = 0
while (True):
    try:
        page = page_cursor.next()
    except StopIteration:
        print("All tweets in the time interval are harvested.")
        break

    remain_request -= 1
    print(f"Fetch Page: {page_fetched}")
    
    for tweet in page:
        # here use try & except to avoid duplicated tweets
        # duplicated tweets will have the same tweet_id
        
        tweet_formated = tweet._json
        user_list = [tweet_formated["user"]]
        if "retweeted_status" in tweet_formated.keys():
            tweet_formated = tweet_formated["retweeted_status"]
            user_list.append(tweet_formated["user"])
            #print(tweet_formated)
        try:
            tweet_db.save({
                "_id": str(tweet_formated["id"]),
                "created_at": tweet_formated["created_at"],
                "full_text": tweet_formated["full_text"],
                "user": tweet_formated["user"],
                "search_location": search_location
            })
        
        except:
            #print("One duplicated tweets caught!")
            continue
        
        for user_info in user_list:
            #user_info = tweet_formated["user"]
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
                print("Duplicated user found!")

    
    page_fetched += 1
    
    if (time.time()-last_check_time)>=15*60:
        remain_request = api.rate_limit_status("search")["resources"]["search"]["/search/tweets"]["remaining"]
        last_check_time = time.time()
        print(f"The request limit should be reset, now {remain_request} request(s) available")
    
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
print(api.rate_limit_status("search")["resources"]["search"]["/search/tweets"]["remaining"])
print("Finish!")
exit()

while (counter <2):
    
    page = page_cursor.next()
    #print(page._json.keys())
    for tweet in page:
        #print(tweet._json.keys())
        #print(tweet._json["full_text"])
        if (tweet._json["geo"] != None) or (tweet._json["coordinates"] != None) or (tweet._json["place"] != None):
            print(tweet._json["geo"])
            print(tweet._json["coordinates"])
            print(tweet._json["place"])
    
    counter += 1
    

print(api.rate_limit_status("search"))
#print(JiarChen108_API_key)

#print("This is the name of the program:", sys.argv[0])
  
print("Argument List:", str(sys.argv))
