# Lab 7: Ansible Deployment - Complete Project Index

## 📋 Project Overview

**Status**: ✅ **COMPLETE AND READY FOR DEPLOYMENT**

This project contains a complete Lab 7 setup for "Automate Remote Deployment with Ansible Playbooks" created using Python automation (pdfplumber) to read the PDF manual.

---

## 📂 File Structure

```
/workspaces/cicdlab7/
├── 840154_L07.pdf              # Original PDF manual (991 KB)
├── setup_lab7.py              # Python automation script (reads PDF, creates lab)
├── COMPLETION_REPORT.txt      # Comprehensive completion report
├── LAB7_SETUP_SUMMARY.md      # Detailed setup documentation
├── QUICK_START.md             # Quick reference guide
├── INDEX.md                   # This file
└── Lab7/                      # Main lab directory (production-ready)
    ├── Makefile               # Automation targets
    ├── README.md              # Lab documentation
    ├── ansible-deploy.sh      # Deployment script
    ├── group_vars/
    │   └── webservers.yml     # Group variables
    ├── inventories/
    │   └── development.yml    # Host inventory
    ├── playbooks/
    │   ├── deploy-app.yml     # Main playbook (163 lines)
    │   └── templates/
    │       ├── app.conf.j2    # Application config template
    │       └── supervisor-app.conf.j2  # Supervisor template
    └── roles/                 # Roles directory (for future use)
```

---

## 🚀 Quick Navigation

### For First-Time Users
1. Start here: [QUICK_START.md](QUICK_START.md)
2. Then read: [Lab7/README.md](Lab7/README.md)
3. Then navigate to: `cd Lab7`

### For Complete Details
- Full report: [COMPLETION_REPORT.txt](COMPLETION_REPORT.txt)
- Setup documentation: [LAB7_SETUP_SUMMARY.md](LAB7_SETUP_SUMMARY.md)

### To Re-run Setup
```bash
python3 setup_lab7.py
```

---

## 📊 Files Summary

| File | Size | Purpose |
|------|------|---------|
| [setup_lab7.py](setup_lab7.py) | 18 KB | Python script that reads PDF and creates lab |
| [COMPLETION_REPORT.txt](COMPLETION_REPORT.txt) | 13 KB | Full project completion report |
| [LAB7_SETUP_SUMMARY.md](LAB7_SETUP_SUMMARY.md) | 6.1 KB | Detailed setup documentation |
| [QUICK_START.md](QUICK_START.md) | 4.0 KB | Quick reference guide |
| [Lab7/Makefile](Lab7/Makefile) | 66 lines | Automation targets |
| [Lab7/README.md](Lab7/README.md) | 108 lines | Lab documentation |
| [Lab7/playbooks/deploy-app.yml](Lab7/playbooks/deploy-app.yml) | 163 lines | Main deployment playbook |
| [Lab7/group_vars/webservers.yml](Lab7/group_vars/webservers.yml) | 21 lines | Group variables |
| [Lab7/inventories/development.yml](Lab7/inventories/development.yml) | 42 lines | Host inventory |
| [Lab7/ansible-deploy.sh](Lab7/ansible-deploy.sh) | 30 lines | Deployment script |
| [Lab7/playbooks/templates/app.conf.j2](Lab7/playbooks/templates/app.conf.j2) | 21 lines | App config template |
| [Lab7/playbooks/templates/supervisor-app.conf.j2](Lab7/playbooks/templates/supervisor-app.conf.j2) | 20 lines | Supervisor template |

**Total Lab Configuration**: 471 lines across 8 files

---

## 🎯 Lab Learning Objectives

✅ Write basic deployment playbooks with YAML syntax
✅ Automate service restart and file copying operations
✅ Handle errors and playbook failures gracefully
✅ Practice YAML structuring and modular playbook design

---

## 🔧 How It Works

### Setup Method
```
PDF Manual (840154_L07.pdf)
    ↓
Python Script (setup_lab7.py)
    ↓
pdfplumber Package (reads PDF)
    ↓
Creates Complete Lab Structure:
  - Inventory files
  - Group variables
  - Playbooks
  - Jinja2 templates
  - Automation scripts
  - Makefile
    ↓
Ready for Ansible Deployment
```

### Deployment Method
```
Makefile Targets
    ↓
Ansible Playbook (deploy-app.yml)
    ↓
Pre-tasks (environment setup)
    ↓
Tasks (app deployment)
    ↓
Post-tasks (service management)
    ↓
Running Applications on Ports 8080 & 8081
```

---

## 🚀 Getting Started in 3 Steps

### Step 1: Navigate to Lab
```bash
cd /workspaces/cicdlab7/Lab7
```

### Step 2: Install Prerequisites
```bash
sudo apt update
sudo apt install ansible sshpass -y
pip3 install --user "jinja2==3.0.3"
export PATH="$HOME/.local/bin:$PATH"
```

### Step 3: Deploy
```bash
# Check syntax and connectivity
ansible-playbook playbooks/deploy-app.yml --syntax-check
ansible -i inventories/development.yml all -m ping

# Deploy applications
make deploy ENV=development
```

---

## 🧪 Testing Commands

```bash
# Test web1 (port 8080)
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/version

# Test web2 (port 8081)
curl http://localhost:8081/
curl http://localhost:8081/health
curl http://localhost:8081/version

# Check status
make status

# View logs
make logs-web1
make logs-web2
```

---

## 📋 Makefile Targets

```bash
make deploy-check    # Dry-run deployment
make deploy         # Execute deployment
make status         # Check service status
make logs-web1      # View web1 logs
make logs-web2      # View web2 logs
make test           # Test applications
make clean          # Cleanup
```

---

## 🔍 Key Features

### Multi-Host Deployment
- Deploy to web1 (port 8080) and web2 (port 8081)
- Configurable via inventory
- Ready for remote hosts

### Flask Application
- Automatic Flask demo app creation
- Health check endpoint
- Version tracking
- Environment-aware configuration

### Process Management
- Supervisor for process management
- Auto-restart on failure
- Log rotation (50MB, 5 backups)
- Per-app configuration

### Automation & Convenience
- Makefile for common operations
- Pre-flight checks
- Deployment script with flags
- Status monitoring
- Log viewing utilities

---

## 📚 Documentation Files

| File | Contains |
|------|----------|
| [QUICK_START.md](QUICK_START.md) | Installation and quick commands |
| [LAB7_SETUP_SUMMARY.md](LAB7_SETUP_SUMMARY.md) | Detailed setup and features |
| [COMPLETION_REPORT.txt](COMPLETION_REPORT.txt) | Full completion report with all details |
| [Lab7/README.md](Lab7/README.md) | Lab-specific documentation |

---

## 🛠️ Troubleshooting

### Installation Issues
```bash
# Update pip
pip3 install --upgrade pip

# Fix Jinja2 compatibility
pip3 install --user "jinja2==3.0.3"

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Deployment Issues
```bash
# Check Ansible version
ansible --version

# Validate playbook syntax
ansible-playbook playbooks/deploy-app.yml --syntax-check

# Test inventory
ansible-inventory -i inventories/development.yml --list

# Check connectivity
ansible -i inventories/development.yml all -m ping
```

### Service Issues
```bash
# Check Supervisor status
sudo supervisorctl status

# View application logs
tail /home/student/deployed-apps/logs/flask-demo-web1.out.log
tail /home/student/deployed-apps/logs/flask-demo-web2.out.log

# Stop all services
sudo supervisorctl stop all

# Restart services
sudo supervisorctl restart all
```

---

## 📖 Lab Details

| Aspect | Details |
|--------|---------|
| **Lab Name** | Lab 7: Automate Remote Deployment with Ansible Playbooks |
| **Estimated Time** | 60 minutes |
| **Hosts** | web1, web2, db1, lb1 (all on localhost for testing) |
| **Ports** | 8080 (web1), 8081 (web2) |
| **Application** | Flask demo app with health checks |
| **Process Manager** | Supervisor |
| **Configuration** | YAML + Jinja2 templates |
| **Automation** | Make + Bash + Ansible |

---

## 🎓 Lab Workflow

1. **Setup** (< 1 min): Lab already created by Python script
2. **Prerequisites** (5-10 min): Install Ansible and dependencies
3. **Pre-flight** (1-2 min): Check syntax and connectivity
4. **Deployment** (10-15 min): Run playbook
5. **Verification** (5-10 min): Test applications and services
6. **Total** (30-40 min): All steps combined

---

## 📞 Support Files

- **Python Package**: pdfplumber (for reading PDF manual)
- **Automation Tool**: Python 3 with pdfplumber
- **Deployment Tool**: Ansible
- **Process Manager**: Supervisor
- **Build Tool**: Make

---

## ✅ Verification Checklist

- [x] Lab7 directory created
- [x] All 8 configuration files present
- [x] Directory structure matches specification
- [x] All YAML files have valid syntax
- [x] Jinja2 templates properly formatted
- [x] Makefile targets executable
- [x] Deployment script executable
- [x] Documentation complete
- [x] Setup automation script working
- [x] Ready for deployment

---

## 🎉 Next Steps

1. Read [QUICK_START.md](QUICK_START.md)
2. Navigate to Lab7: `cd Lab7`
3. Review [Lab7/README.md](Lab7/README.md)
4. Install prerequisites
5. Run: `make deploy ENV=development`
6. Test: `curl http://localhost:8080/health`

---

## 📄 License & Attribution

Based on Lab 7 manual (840154_L07.pdf) from Global Knowledge Training LLC

---

**Last Updated**: 2026-01-14  
**Status**: ✅ Ready for Production  
**Python Package Used**: pdfplumber  
**Automation Method**: Fully Automated from PDF

---

**Start Here**: [QUICK_START.md](QUICK_START.md)
