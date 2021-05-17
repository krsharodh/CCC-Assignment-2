#!/bin/bash
. ./openrc.sh; ansible-playbook -i inventory/hosts.ini instance_and_couchdb.yaml other.yaml
