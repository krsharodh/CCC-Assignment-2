import couchdb
import tweepy
import sys
import json
import time
from datetime import datetime
import math
from var import * 


#comm = MPI.COMM_WORLD
#rank = comm.rank
#n_tasks = comm.size
rank = 0
n_tasks = 1

## set the couchdb API
address = f"http://{username}:{password}@{MASTER_NODE_IP}:{couchdb_port}"
# Note: For urllib3 version<1.26.0, please use the line below instead.
# address = f"https://{username}:{password}@{MASTER_NODE_IP}:{couchdb_port}"
couchdb_server = couchdb.Server(address)

user_db_name = "user3"
clean_user_db_name = "clean_user3"

try:
    user_db = couchdb_server[user_db_name]
except:
    print(f"There is no database called {user_db_name} on the server.")

try:
    clean_user_db = couchdb_server.create(clean_user_db_name)
except:
    clean_user_db = couchdb_server[clean_user_db_name]

user_ids = list(user_db)
n_user = len(list(user_db))
#bin_width = math.ceil(n_user/n_tasks)

start_pos = round(rank*n_user/n_tasks)
end_pos = round((rank+1)*n_user/n_tasks)
assigned_user_ids = user_ids[start_pos:end_pos]

print(n_user, start_pos, end_pos)
exit()
target_user_list = []
city_list = ["melbourne", "sydney", "adelaide", "brisbane", "perth", "canberra", "darwin", "hobart"]

for i in assigned_user_ids:
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
