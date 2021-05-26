The ansible playbooks need to be run in order to deploy the system on Melbourne Research Cloud. First the user need to be under the ansible direcotry in the project CCC-Assignment-2 folder. The ansibles playbook can be run using the folling command in the terminal:
. ./openrc.sh; ansible-playbook -i inventory/hosts.ini instance_and_couchdb.yaml other.yaml

Or alternatively ruuning the shell script which contains the line above with the follwing command:
./run_playbook.sh

The first playbook "instance_and_couchdb.yaml" will deploy the virtual instances and MRC and set up the couchDB cluster. Whereas the second playbook "other.yaml" will clone github repository, launch back-end, front-end and harvester application on the instances created. Details about the deployment process is explained later in this report in the method section.

After running the playbooks, the user can check the front end web page using the IP address of the first/masternode instance with port 3000. At the moment, the IP address of the masternode is 172.26.133.161, and the front end web application is at http://172.26.133.161:3000

Then the user will be able to interact with the front end application using the tabs and drop down list on the web page.

Apart from launching back end, front end and harvester all at once, the user can also run the playbooks that runs them individually, namely back_end.yaml, front_end.yaml, harvester.yaml.
