import couchdb
import tweepy
import sys
import json

from var import * 
argv = sys.argv
for i in range(len(argv)):
    if argv[i] == "-keyword":
        if (i<len(argv)-1) and (argv[i+1][0] != '-'):
            keyword = argv[i+1]
        else :
            print("Invalid arguments!")
            exit()
    elif argv[i] == "-city":
        if (i<len(argv)-1) and (argv[i+1][0] != '-'):
            city = argv[i+1]
        else :
            print("Invalid arguments!")
            exit()

print(keyword)
print(city)
print(f'https://{username}:{password}@{MASTER_NODE_IP}:{couchdb_port}/')

couchdb_server = couchdb.Server(f'https://{username}:{password}@{MASTER_NODE_IP}:{couchdb_port}/')
print(couchdb_server.version())
db_name = "test"

testdb = couchdb_server.create(db_name)
exit()
#testdb = couchdb_server["test"]
testdb.save({'_id':1, 'text':"Hello CouchDB!", 'User':"Jiarui"})


exit()
auth = tweepy.OAuthHandler(JiarChen108_API_key, JiarChen108_API_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

print(api.rate_limit_status("search"))

geocode = "-25.610112,134.354805,2240km"
page_cursor = tweepy.Cursor(api.search, q = keyword, since="2021-04-28", until="2021-04-29", lang="en", count = 100, geocode=geocode, tweet_mode='extended').pages()


counter = 0
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
