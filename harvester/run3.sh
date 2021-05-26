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


mpirun -n $# -host $STR python3 user_timeline_harvester.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984

# mpirun -n 4 -host $1:1,$2:1,$3:1,$4:1 python3 user_timeline_harvester.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984