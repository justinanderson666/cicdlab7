#!/bin/bash
# Ansible Deployment Script
set -e

while getopts e:p: flag
do
    case "${flag}" in
        e) ENV=${OPTARG};;
        p) PLAYBOOK=${OPTARG};;
    esac
done

echo "[`date +"%Y-%m-%d %H:%M:%S"`] Ansible Deployment Plan"
echo "================================="
echo "Environment: $ENV"
echo "Inventory: $(pwd)/inventories/$ENV.yml"
echo "Playbook: $(pwd)/$PLAYBOOK"
echo "Command: ansible-playbook -i $(pwd)/inventories/$ENV.yml $(pwd)/$PLAYBOOK"
echo "================================="

echo "[`date +"%Y-%m-%d %H:%M:%S"`] Running pre-flight checks..."
echo "[`date +"%Y-%m-%d %H:%M:%S"`] Testing inventory connectivity..."
ansible -i inventories/$ENV.yml all -m ping

echo "[`date +"%Y-%m-%d %H:%M:%S"`] Checking playbook syntax..."
ansible-playbook -i inventories/$ENV.yml $PLAYBOOK --syntax-check

echo "[SUCCESS] Pre-flight checks completed"
echo "[`date +"%Y-%m-%d %H:%M:%S"`] Starting Ansible execution..."
ansible-playbook -i inventories/$ENV.yml $PLAYBOOK
