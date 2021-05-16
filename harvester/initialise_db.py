import couchdb
import sys

# rank = 2
# n_tasks = 4

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
    

#node_ip = allocate_node_ip(master_node_ip, username, password, couchdb_port, rank)
address = f"http://{username}:{password}@{master_node_ip}:{couchdb_port}"
couchdb_server = couchdb.Server(address)

print(list(couchdb_server))
if "user" not in couchdb_server:
    user_db = couchdb_server.create("user")

if "recent_search_tweets" not in couchdb_server:
    tweet_db = couchdb_server.create("recent_search_tweets")


if "clean_user" not in couchdb_server:
    clean_user_db = couchdb_server.create("clean_user")


if "raw_tweets_from_timeline" not in couchdb_server:
    raw_tweets_db = couchdb_server.create("raw_tweets_from_timeline")
