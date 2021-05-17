import couchdb
import tweepy
import sys
import json
import time
from datetime import datetime
import math

from mpi4py import MPI
from util import *

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n_tasks = comm.Get_size()
#rank = 0
#n_tasks = 1
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

node_ip = allocate_node_ip(master_node_ip, username, password, couchdb_port, rank)
address = f"http://{username}:{password}@{node_ip}:{couchdb_port}"
couchdb_server = couchdb.Server(address)

user_db_name = "user"
clean_user_db_name = "clean_user"

try:
    user_db = couchdb_server[user_db_name]
    clean_user_db = couchdb_server[clean_user_db_name]
except:
    print(f"There is no targeted database on the server.")
    exit()

# if rank == 0:
#     try:
#         clean_user_db = couchdb_server.create(clean_user_db_name)
#     except:
#         clean_user_db = couchdb_server[clean_user_db_name]

# if rank != 0:
    
#     clean_user_db = couchdb_server[clean_user_db_name]

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
