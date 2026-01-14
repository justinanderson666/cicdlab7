# Lab 7 Quick Start Guide

## ✅ Setup Complete
Lab 7 has been successfully created from the PDF manual using Python automation!

## 📁 What Was Created
- **8 files** with **471 total lines** of configuration
- Complete Ansible deployment infrastructure
- Flask application deployment system
- Supervisor process management configuration
- Makefile for easy automation

## 🚀 Quick Start (5 minutes)

### 1. Navigate to Lab Directory
```bash
cd /workspaces/cicdlab7/Lab7
```

### 2. View the Structure
```bash
ls -la
cat README.md
```

### 3. Review Key Files
```bash
# Inventory configuration
cat inventories/development.yml

# Group variables
cat group_vars/webservers.yml

# Main playbook (first 40 lines)
head -40 playbooks/deploy-app.yml

# Jinja2 templates
cat playbooks/templates/app.conf.j2
cat playbooks/templates/supervisor-app.conf.j2
```

## 🛠️ Installation & Deployment

### Install Prerequisites
```bash
sudo apt update
sudo apt install ansible sshpass -y
pip3 install --user "jinja2==3.0.3"
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
ansible --version
```

### Test Inventory
```bash
ansible-inventory -i inventories/development.yml --list
ansible -i inventories/development.yml all -m ping
```

### Check Playbook Syntax
```bash
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml --syntax-check
```

### Deploy Using Makefile
```bash
# Dry-run (check mode)
make deploy-check ENV=development

# Actual deployment
make deploy ENV=development

# Check status
make status

# View logs
make logs-web1
make logs-web2
```

## 🧪 Test Deployed Applications

```bash
# Test web1 (port 8080)
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/version

# Test web2 (port 8081)
curl http://localhost:8081/
curl http://localhost:8081/health
curl http://localhost:8081/version

# Check Supervisor status
sudo supervisorctl status
```

## 📊 File Breakdown

| File | Lines | Purpose |
|------|-------|---------|
| `playbooks/deploy-app.yml` | 163 | Main deployment playbook |
| `README.md` | 108 | Lab documentation |
| `Makefile` | 66 | Automation targets |
| `inventories/development.yml` | 42 | Host inventory |
| `ansible-deploy.sh` | 30 | Deployment script |
| `playbooks/templates/app.conf.j2` | 21 | App configuration template |
| `group_vars/webservers.yml` | 21 | Group variables |
| `playbooks/templates/supervisor-app.conf.j2` | 20 | Supervisor template |

## 🔧 Common Commands

```bash
# View Supervisor status
sudo supervisorctl status

# Stop all applications
sudo supervisorctl stop all

# Stop specific app
sudo supervisorctl stop flask-demo-web1

# Start applications
sudo supervisorctl start all

# Tail application logs
tail -f /home/student/deployed-apps/logs/flask-demo-web1.out.log
tail -f /home/student/deployed-apps/logs/flask-demo-web2.out.log

# Clean up deployment
make clean
```

## 📋 Lab Objectives

✅ Write basic deployment playbooks with YAML syntax
✅ Automate service restart and file copying operations
✅ Handle errors and playbook failures gracefully
✅ Practice YAML structuring and modular playbook design

## 🔍 Key Features

- **Multi-host deployment** to web1 and web2
- **Flask demo application** with health checks
- **Supervisor process management** with auto-restart
- **Jinja2 templating** for dynamic configuration
- **Makefile automation** for convenience
- **Pre-flight checks** in deployment script
- **Comprehensive logging** and monitoring

## ⏱️ Estimated Time
60 minutes to complete full deployment and testing

## 📚 Files Reference

- **Setup Script**: `/workspaces/cicdlab7/setup_lab7.py`
- **Lab Directory**: `/workspaces/cicdlab7/Lab7/`
- **PDF Manual**: `/workspaces/cicdlab7/840154_L07.pdf`
- **Summary**: `/workspaces/cicdlab7/LAB7_SETUP_SUMMARY.md`

## ✨ Python Package Used
- **pdfplumber**: For reading and parsing the PDF manual

---
**Ready to deploy! Start with**: `cd Lab7 && make deploy ENV=development`
