# Lab 7 Setup Summary

## Overview
Lab 7 has been successfully set up using a Python script that reads the PDF manual and generates all necessary files and configurations.

## Setup Method
- **Tool Used**: `pdfplumber` Python package to read and parse the PDF manual
- **Script**: `setup_lab7.py` - Automated setup script that creates complete lab structure
- **Execution**: `python3 setup_lab7.py`

## Created Structure

### Directory Layout
```
Lab7/
├── Makefile                      # Makefile for common operations
├── README.md                     # Lab documentation
├── ansible-deploy.sh             # Deployment automation script
├── group_vars/
│   └── webservers.yml           # Group variables for webservers group
├── inventories/
│   └── development.yml          # Development environment inventory
├── playbooks/
│   ├── deploy-app.yml           # Main deployment playbook
│   └── templates/
│       ├── app.conf.j2          # Application configuration template
│       └── supervisor-app.conf.j2 # Supervisor process configuration template
└── roles/                       # Directory for Ansible roles (empty)
```

## Files Created

### 1. **inventories/development.yml**
- Defines all hosts and host groups (webservers, databases, loadbalancers)
- Configures 2 web servers (web1 on port 8080, web2 on port 8081)
- Includes database (db1) and load balancer (lb1) hosts
- Sets global variables for environment, deploy user, and paths

### 2. **group_vars/webservers.yml**
- Nginx configuration (port, worker processes)
- Application configuration (debug mode, log level, max workers, timeout)
- Monitoring settings (enabled, log rotation days)
- Deployment strategy settings

### 3. **playbooks/deploy-app.yml**
- Main deployment playbook with 3 sections:
  - **pre_tasks**: Package cache update, directory creation
  - **tasks**: Package installation, Flask app creation, virtual environment setup, template generation
  - **post_tasks**: Supervisor configuration, service management, health checks, deployment summary

### 4. **playbooks/templates/app.conf.j2**
- Jinja2 template for application configuration
- Includes application settings, logging config, and monitoring settings
- Dynamically populated with Ansible variables

### 5. **playbooks/templates/supervisor-app.conf.j2**
- Jinja2 template for Supervisor process management
- Configures Flask app execution, logging, and environment variables
- Supports auto-restart and log rotation

### 6. **ansible-deploy.sh**
- Bash script for deployment automation
- Accepts environment and playbook parameters (-e, -p flags)
- Performs pre-flight checks (connectivity, syntax validation)
- Executes Ansible playbook

### 7. **Makefile**
- Provides convenient make targets for common operations:
  - `make deploy-check` - Dry-run deployment
  - `make deploy` - Execute deployment
  - `make clean` - Cleanup logs and configs
  - `make status` - Check Supervisor status
  - `make logs-web1`, `make logs-web2` - View application logs
  - `make test` - Test deployed applications

### 8. **README.md**
- Lab documentation with setup instructions
- Usage examples and troubleshooting guide
- Links to key resources and commands

## Lab 7 Objectives Covered

✅ **Write basic deployment playbooks with YAML syntax**
- Complete `deploy-app.yml` playbook with proper YAML structure
- Uses pre_tasks, tasks, and post_tasks sections
- Includes conditional statements and templating

✅ **Automate service restart and file copying operations**
- Package installation with `package` module
- File creation with `copy` module
- Service management with `service` and `supervisorctl` modules
- Template generation with `template` module

✅ **Handle errors and playbook failures gracefully**
- Uses conditional `when` statements
- Includes error handling in post_tasks
- Health check endpoints for verification
- Wait_for module for service readiness

✅ **Practice YAML structuring and modular playbook design**
- Separate inventory, variables, and playbooks
- Group variables organization
- Template modularity with Jinja2
- Configuration files separated from playbooks

## Key Features

### Multi-Host Deployment
- Supports deploying to web1 and web2 on different ports
- Local connection for testing (ansible_connection: local)
- Ready for remote hosts (change ansible_host and connection type)

### Flask Application Deployment
- Automatically creates Flask demo application
- Includes health check endpoint (/health)
- Version endpoint for tracking deployments
- Environment-aware configuration

### Process Management
- Uses Supervisor for process management
- Automatic restart on failure
- Log rotation configured
- Multiple app instances support

### Automation & Convenience
- Makefile targets for common operations
- Deployment script with pre-flight checks
- Status monitoring commands
- Log viewing utilities

## Next Steps

1. **Review the files**: Navigate to Lab7 and examine each file
2. **Check prerequisites**: Ensure Ansible is installed
   ```bash
   sudo apt install ansible -y
   pip3 install --user "jinja2==3.0.3"
   ```
3. **Test connectivity**: 
   ```bash
   cd Lab7
   make ENV=development test
   ```
4. **Run deployment check**:
   ```bash
   make deploy-check ENV=development
   ```
5. **Deploy applications**:
   ```bash
   make deploy ENV=development
   ```

## Workflow

The lab follows this workflow:

```
PDF Manual (840154_L07.pdf)
        ↓
Python Script (setup_lab7.py)
        ↓
pdfplumber (reads PDF)
        ↓
Creates Lab7 Structure:
  - Inventory files
  - Group variables
  - Playbooks
  - Templates
  - Automation scripts
  - Makefile
        ↓
Ready for Deployment
```

## Estimated Completion Time
60 minutes for full lab execution

## Support & Troubleshooting

- Check Ansible syntax: `ansible-playbook playbooks/deploy-app.yml --syntax-check`
- Test inventory: `ansible-inventory -i inventories/development.yml --list`
- View Supervisor status: `sudo supervisorctl status`
- Check application logs: `tail /home/student/deployed-apps/logs/*.log`

---
**Lab 7 Setup Completed**: All files created from PDF manual using Python automation
