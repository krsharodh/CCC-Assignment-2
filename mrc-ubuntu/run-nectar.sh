#!/bin/bash
. ./openrc.sh; ansible-playbook -i inventory/hosts.ini mrc.yaml
