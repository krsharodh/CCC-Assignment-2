import couchdb
import tweepy
import sys
import json
import time
from datetime import date
from datetime import timedelta 
import math
from mpi4py import MPI

from util import *
import requests
  
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n_tasks = comm.Get_size()

#rank = 2
#n_tasks = 4

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

print(f"Rank {rank}, address={address}")
comm.Barrier()
print("Finish!")
#res = requests.get("http://admin:admin@172.26.133.34:5984/_membership")

#print(res.text)

#db.save({'_id':"3", 'text':"こんにちは、 CouchDB!", 'User':"Jiarui"})
#db.save({'_id':"4", 'text':"你好，CouchDB!", 'User':"Jiarui"})

# Note: For urllib3 version<1.26.0, please use the line below instead.
# address = f"https://{username}:{password}@{MASTER_NODE_IP}:{couchdb_port}"
#couchdb_server = couchdb.Server(address)

#print(couchdb_server.config)

