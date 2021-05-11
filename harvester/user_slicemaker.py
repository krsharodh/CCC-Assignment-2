import couchdb
import tweepy
import sys
import json
import time
from datetime import datetime

from var import * 

## set the couchdb API
address = f"http://{username}:{password}@{MASTER_NODE_IP}:{couchdb_port}"
# Note: For urllib3 version<1.26.0, please use the line below instead.
# address = f"https://{username}:{password}@{MASTER_NODE_IP}:{couchdb_port}"
couchdb_server = couchdb.Server(address)

user_db_name = "user"
clean_user_db_name = "clean_user"

try:
    user_db = couchdb_server[user_db_name]
except:
    print(f"There is no database called {user_db_name} on the server.")

try:
    clean_user_db = couchdb_server.create(clean_user_db_name)
except:
    clean_user_db = couchdb_server[clean_user_db_name]


target_user_list = []
city_list = ["melbourne", "sydney", "adelaide", "brisbane", "perth", "canberra", "darwin", "hobart"]

for i in user_db:
    doc = user_db[i]
    
    if doc["uniform_location"] != "NA":
        try:
            clean_user_db.save({
                        "_id": str(i),
                        "name": doc["name"],
                        "screen_name": doc["screen_name"],
                        "location": doc["location"],
                        "uniform_location": doc["uniform_location"],
                        "created_at": doc["created_at"]
                    })
            #print(doc)
        except:
            pass
