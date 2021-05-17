#python3 harvester.py -keyword vaccine -location australia

#mpirun -n 4 -host $1:1,$2:1,$3:1,$4:1 python3 helloworld.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984 
#python3 helloworld.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984
curl -X PUT "admin:admin@$1:5984/recent_search_tweets3?q=2&n=4"
curl -X PUT "admin:admin@$1:5984/user3?q=2&n=4"
curl -X PUT "admin:admin@$1:5984/clean_user3?q=2&n=4"
curl -X PUT "admin:admin@$1:5984/raw_tweets_from_timeline3?q=8&n=2"

#python3 initialise_db.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984
mpirun -n 4 -host $1:1,$2:1,$3:1,$4:1 python3 harvester.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984 -location australia
mpirun -n 4 -host $1:1,$2:1,$3:1,$4:1 python3 user_slicemaker.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984
mpirun -n 4 -host $1:1,$2:1,$3:1,$4:1 python3 user_timeline_harvester.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984

#python3 harvester.py -location australia -keyword vaccine -rank $1
#python3 user_slicemaker.py
#python3 user_timeline_harvester.py -rank $1                                       