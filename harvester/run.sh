#python3 harvester.py -keyword vaccine -location australia
export MASTER=$1
export SLAVE1=$2
export SLAVE2=$3
export SLAVE3=$4

mpirun -n 4 -host MASTER:1,SLAVE1:1,SLAVE2:1,SLAVE3:1 python3 helloworld.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984 
#python3 helloworld.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984


#python3 harvester.py -location australia -keyword vaccine -rank $1
#python3 user_slicemaker.py
#python3 user_timeline_harvester.py -rank $1                                       