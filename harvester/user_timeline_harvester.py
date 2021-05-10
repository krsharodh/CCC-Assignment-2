import couchdb
import tweepy
import sys
import json
import time

from var import * 

## set the Twitter API
auth = tweepy.OAuthHandler(JiarChen108_API_key, JiarChen108_API_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

remain_request = api.rate_limit_status("search")["resources"]["search"]["/search/tweets"]["remaining"]
if remain_request>1:
    print(f"Note: {remain_request} search requests remaining / 15-min window.")
else:
    print(f"Note: {remain_request} search request remaining / 15-min window.")
start_time = time.time()
print(start_time)
val = input("Continue? (Y/N): ")
if val.lower() in ["n", "no", "false"]:
    exit(0)

## set the couchdb API
address = f"http://{username}:{password}@{MASTER_NODE_IP}:{couchdb_port}"
# Note: For urllib3 version<1.26.0, please use the line below instead.
# address = f"https://{username}:{password}@{MASTER_NODE_IP}:{couchdb_port}"
couchdb_server = couchdb.Server(address)
print(couchdb_server.version())

user_db_name = "user"

try:
    user_db = couchdb_server[user_db_name]
except:
    print(f"There is no database called {user_db_name} on the server.")

target_user_list = []
city_list = ["melbourne", "sydney", "adelaide", "brisbane", "perth", "canberra", "darwin", "hobart"]

for i in user_db:
    doc = user_db[i]
    if "darwin" in doc["location"].lower():
        target_user_list.append(i)
        print(doc["location"].lower())
#print(user_db[id_list[0]]["location"])
print(len(target_user_list))
exit()
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

# until="2021-05-08",
page_cursor = tweepy.Cursor(api.search, q = keyword, since="2021-05-01", until="2021-05-11", lang="en", count = 100, geocode=geocode[search_location], tweet_mode='extended').pages()

#page_cursor = tweepy.Cursor(api.search, q = keyword, since="2021-05-01", lang="en", count = 100, geocode=geocode, tweet_mode='extended').pages()

page_fetched = 0
while (remain_request>1):
    page = page_cursor.next()
    print(f"Fetch Page: {page_fetched}")
    for tweet in page:
        # here use try & except to avoid duplicated tweets
        # duplicated tweets will have the same tweet_id
        
        try:
            tweet_formated = tweet._json
            if "retweeted_status" in tweet_formated.keys():
                tweet_formated = tweet_formated["retweeted_status"]
                #print(tweet_formated)
            tweet_db.save({
                "_id": str(tweet_formated["id"]),
                "created_at": tweet_formated["created_at"],
                "full_text": tweet_formated["full_text"],
                "user": tweet_formated["user"],
                "search_location": search_location
            })
        
        except:
            print("One dup tweets caught!")
            continue
        
        try:
            user_db.save({
                "_id": str(tweet_formated["user"]["id"]),
                "name": tweet_formated["user"]["name"],
                "screen_name": tweet_formated["user"]["screen_name"],
                "location": tweet_formated["user"]["location"],
                "created_at": tweet_formated["user"]["created_at"]
            })
        except:
            print("One dup users caught!")

        

    
    remain_request -= 1
    page_fetched += 1

    if len(page)==0:
        print("All tweets in the time interval are harvested.")
        break


end_time = time.time()
print(f"harvest_time={round(end_time-start_time, 2)}")
print(api.rate_limit_status("search")["resources"]["search"]["/search/tweets"]["remaining"])

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