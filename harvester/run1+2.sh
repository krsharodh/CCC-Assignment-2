#python3 harvester.py -keyword vaccine -location australia

#mpirun -n 4 -host $1:1,$2:1,$3:1,$4:1 python3 helloworld.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984 
#python3 helloworld.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984

python3 initialise_db.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984
mpirun -n 4 -host $1:1,$2:1,$3:1,$4:1 python3 harvester.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984 -location australia
mpirun -n 4 -host $1:1,$2:1,$3:1,$4:1 python3 user_slicemaker.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984
#mpirun -n 4 -host $1:1,$2:1,$3:1,$4:1 python3 user_timeline_harvester.py -master_node_ip $1 -username admin -password admin -couchdb_port 5984

#python3 harvester.py -location australia -keyword vaccine -rank $1
#python3 user_slicemaker.py
#python3 user_timeline_harvester.py -rank $1                                       