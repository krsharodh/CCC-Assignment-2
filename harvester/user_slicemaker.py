import couchdb
import tweepy
import sys
import json
import time
from datetime import datetime
import math
from var import * 
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank
n_tasks = comm.size
#rank = 0
#n_tasks = 1

node_ip = allocate_node_ip(master_node_ip, username, password, couchdb_port, rank, n_tasks)
address = f"http://{username}:{password}@{node_ip}:{couchdb_port}"
couchdb_server = couchdb.Server(address)

user_db_name = "user4"
clean_user_db_name = "clean_user4"

try:
    user_db = couchdb_server[user_db_name]
except:
    print(f"There is no database called {user_db_name} on the server.")

if rank == 0:
    try:
        clean_user_db = couchdb_server.create(clean_user_db_name)
    except:
        clean_user_db = couchdb_server[clean_user_db_name]

comm.barrier()

if rank != 0:
    
    clean_user_db = couchdb_server[clean_user_db_name]

user_ids = list(user_db)
n_user = len(list(user_db))
#bin_width = math.ceil(n_user/n_tasks)

start_pos = round(rank*n_user/n_tasks)
end_pos = round((rank+1)*n_user/n_tasks)
assigned_user_ids = user_ids[start_pos:end_pos]

#print(n_user, start_pos, end_pos)

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
