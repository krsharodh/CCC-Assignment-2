import couchdb
import tweepy
import sys
import json
import time
from datetime import date
from datetime import timedelta 
import math
import requests

def get_nodes_ip(master_node_ip, username, password, couchdb_port = 5984):
    res = requests.get(f"http://{username}:{password}@{master_node_ip}:{couchdb_port}/_membership")
    #print([ip.split("@")[1] for ip in json.loads(res.text)["all_nodes"]])
    return [ip.split("@")[1] for ip in json.loads(res.text)["all_nodes"]]

def allocate_node_ip(master_node_ip, username, password, couchdb_port = 5984, rank = 0):
    
    all_nodes = get_nodes_ip(master_node_ip, username, password, couchdb_port)
    #print(rank % len(all_nodes))
    return all_nodes[(rank % len(all_nodes))]

