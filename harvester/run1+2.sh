curl -X PUT "admin:admin@$1:5984/recent_search_tweets?q=2&n=4"
curl -X PUT "admin:admin@$1:5984/user?q=2&n=4"
curl -X PUT "admin:admin@$1:5984/clean_user?q=2&n=4"
curl -X PUT "admin:admin@$1:5984/raw_tweets_from_timeline?q=8&n=2"


STR=""

is_first=0

for j in "$@" 
do  
if [ $is_first -eq 0 ]
then
    STR="$j:1"
    is_first=1
elif [ $is_first -eq 1 ]
then
    STR="$STR,$j:1"
fi
done

mpirun -n $# -host $STR python3 harvester.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984 -location australia
mpirun -n $# -host $STR python3 user_slicemaker.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984

# mpirun -n 4 -host $1:1,$2:1,$3:1,$4:1 python3 harvester.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984 -location australia
# mpirun -n 4 -host $1:1,$2:1,$3:1,$4:1 python3 user_slicemaker.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984

                                 