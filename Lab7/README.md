# Lab 7: Automate Remote Deployment with Ansible Playbooks

This lab demonstrates automating remote deployments using Ansible playbooks.

## Lab Structure

```
Lab7/
├── inventories/
│   └── development.yml          # Inventory file with hosts and groups
├── group_vars/
│   └── webservers.yml           # Group variables for webservers
├── playbooks/
│   ├── deploy-app.yml           # Main deployment playbook
│   └── templates/
│       ├── app.conf.j2          # Application configuration template
│       └── supervisor-app.conf.j2 # Supervisor configuration template
├── roles/                       # Directory for Ansible roles
├── ansible-deploy.sh            # Deployment automation script
├── Makefile                     # Make targets for common operations
└── README.md                    # This file
```

## Prerequisites

- Ansible installed
- Python 3 with Jinja2 3.0.3
- sshpass installed
- sudo access for service management

## Setup

Run the setup script to install dependencies:

```bash
cd Lab7
sudo apt update
sudo apt install ansible sshpass -y
pip3 install --user "jinja2==3.0.3"
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
ansible --version
```

## Usage

### Test Inventory
```bash
make ENV=development test-inventory
```

### Deploy Applications
```bash
make ENV=development deploy-check  # Dry run
make ENV=development deploy         # Actual deployment
```

### Check Status
```bash
make status
```

### View Logs
```bash
make logs-web1
make logs-web2
```

### Test Applications
```bash
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/version

curl http://localhost:8081/
curl http://localhost:8081/health
curl http://localhost:8081/version
```

### Stop Applications
```bash
sudo supervisorctl stop flask-demo-web1
sudo supervisorctl stop flask-demo-web2
sudo supervisorctl stop all
```

### Cleanup
```bash
make clean
```

## Lab Objectives

- ✅ Write basic deployment playbooks with YAML syntax
- ✅ Automate service restart and file copying operations
- ✅ Handle errors and playbook failures gracefully
- ✅ Practice YAML structuring and modular playbook design

## Expected Deployment Time

60 minutes

## Support

For troubleshooting, check:
- Supervisor status: `sudo supervisorctl status`
- Ansible logs: Check the output of `ansible-playbook` command
- Application logs: `/home/student/deployed-apps/logs/`
