#!/usr/bin/env python3
"""
Lab 7 Setup Script - Automate Remote Deployment with Ansible Playbooks
Reads the PDF manual and creates the complete lab structure
"""

import os
import sys
import subprocess
from pathlib import Path
import pdfplumber

def read_pdf_manual(pdf_path):
    """Read and extract text from the PDF manual."""
    print(f"📖 Reading PDF manual: {pdf_path}")
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def create_directory_structure(base_path):
    """Create the Lab7 directory structure."""
    print("\n📁 Creating directory structure...")
    directories = [
        "Lab7",
        "Lab7/inventories",
        "Lab7/playbooks",
        "Lab7/playbooks/templates",
        "Lab7/roles",
        "Lab7/group_vars",
    ]
    
    for dir_path in directories:
        full_path = base_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created: {dir_path}")
    
    return base_path / "Lab7"

def create_inventory_file(lab_path):
    """Create the development.yml inventory file."""
    print("\n📋 Creating inventory file...")
    inventory_content = """# Development Environment Inventory
all:
  children:
    webservers:
      hosts:
        web1:
          ansible_host: localhost
          ansible_connection: local
          ansible_user: student
          server_role: primary
          app_port: 8080
          app_name: flask-demo-web1
        web2:
          ansible_host: localhost
          ansible_connection: local
          ansible_user: student
          server_role: secondary
          app_port: 8081
          app_name: flask-demo-web2
    databases:
      hosts:
        db1:
          ansible_host: localhost
          ansible_connection: local
          ansible_user: student
          db_port: 5432
          db_name: app_database
    loadbalancers:
      hosts:
        lb1:
          ansible_host: localhost
          ansible_connection: local
          ansible_user: student
          lb_algorithm: round_robin
  vars:
    environment: development
    app_environment: development
    deploy_user: student
    app_directory: "/home/student/deployed-apps"
    ansible_python_interpreter: /usr/bin/python3
    app_version: "1.0.0"
    restart_services: true
"""
    
    inventory_file = lab_path / "inventories" / "development.yml"
    inventory_file.write_text(inventory_content)
    print(f"  ✓ Created: {inventory_file.relative_to(lab_path)}")

def create_group_variables(lab_path):
    """Create group variables for webservers."""
    print("\n🔧 Creating group variables...")
    webservers_vars = """# Variables specific to webserver group
nginx_port: 80
nginx_worker_processes: auto
app_max_memory: 512M
health_check_url: "/health"
deployment_strategy: rolling
max_failure_percentage: 20

# Application configuration
app_config:
  debug: false
  log_level: INFO
  max_workers: 4
  timeout: 30

# Monitoring
monitoring_enabled: true
log_rotation_days: 30

# Environment setting
app_environment: development
"""
    
    vars_file = lab_path / "group_vars" / "webservers.yml"
    vars_file.write_text(webservers_vars)
    print(f"  ✓ Created: {vars_file.relative_to(lab_path)}")

def create_deployment_playbook(lab_path):
    """Create the main deployment playbook."""
    print("\n📜 Creating deployment playbook...")
    playbook_content = """# Main Application Deployment Playbook
- name: Deploy Flask Application
  hosts: webservers
  become: yes
  become_user: root
  gather_facts: yes
  vars:
    app_version: "1.0.0"
    restart_services: true
  vars_files:
    - ../group_vars/webservers.yml
  
  pre_tasks:
    - name: Update package cache
      apt:
        update_cache: yes
      when: ansible_os_family == "Debian"
      run_once: true
    
    - name: Create application directory
      file:
        path: "{{ app_directory }}"
        state: directory
        owner: "{{ deploy_user }}"
        group: "{{ deploy_user }}"
    
    - name: Create logs directory
      file:
        path: "{{ app_directory }}/logs"
        state: directory
        owner: "{{ deploy_user }}"
        group: "{{ deploy_user }}"
  
  tasks:
    - name: Install required system packages
      package:
        name:
          - python3
          - python3-pip
          - python3-venv
          - nginx
          - supervisor
          - curl
        state: present
      run_once: true
    
    - name: Create application files directory
      file:
        path: "{{ app_directory }}/app"
        state: directory
        owner: "{{ deploy_user }}"
        group: "{{ deploy_user }}"
    
    - name: Create simple Flask application
      copy:
        content: |
          from flask import Flask, jsonify
          import os, datetime
          app = Flask(__name__)
          
          @app.route('/')
          def home():
              return f\"\"\"
              <h1>Flask Demo Application</h1>
              <p>Environment: {os.environ.get("ENVIRONMENT", "dev")}</p>
              <p>Host: {os.environ.get("HOSTNAME", "unknown")}</p>
              <p>Version: {os.environ.get("APP_VERSION", "1.0.0")}</p>
              <p>Port: {os.environ.get("APP_PORT", "8080")}</p>
              \"\"\"
          
          @app.route('/health')
          def health():
              return jsonify({
                  "status": "healthy",
                  "environment": os.environ.get("ENVIRONMENT", "dev"),
                  "timestamp": datetime.datetime.now().isoformat(),
                  "host": os.environ.get("HOSTNAME", "unknown")
              })
          
          @app.route('/version')
          def version():
              return jsonify({
                  "app_version": os.environ.get("APP_VERSION", "1.0.0"),
                  "environment": os.environ.get("ENVIRONMENT", "dev"),
                  "port": os.environ.get("APP_PORT", "8080")
              })
          
          if __name__ == "__main__":
              port = int(os.environ.get("APP_PORT", 8080))
              app.run(host="0.0.0.0", port=port, debug=False)
        dest: "{{ app_directory }}/app/app.py"
        owner: "{{ deploy_user }}"
        group: "{{ deploy_user }}"
        mode: '0755'
    
    - name: Create requirements.txt
      copy:
        content: |
          Flask==2.3.3
          gunicorn==21.2.0
        dest: "{{ app_directory }}/app/requirements.txt"
    
    - name: Create Python virtual environment
      command: python3 -m venv {{ app_directory }}/venv
      args:
        creates: "{{ app_directory }}/venv/bin/activate"
    
    - name: Install Python dependencies into venv
      pip:
        requirements: "{{ app_directory }}/app/requirements.txt"
        virtualenv: "{{ app_directory }}/venv"
    
    - name: Generate application configuration
      template:
        src: templates/app.conf.j2
        dest: "{{ app_directory }}/app.conf"
    
    - name: Configure Supervisor for application
      template:
        src: templates/supervisor-app.conf.j2
        dest: "/etc/supervisor/conf.d/{{ app_name }}.conf"
  
  post_tasks:
    - name: Ensure Supervisor is running
      service:
        name: supervisor
        state: started
        enabled: yes
    
    - name: Reread Supervisor configs
      command: supervisorctl reread
    
    - name: Update Supervisor with new configs
      command: supervisorctl update
    
    - name: Start application
      supervisorctl:
        name: "{{ app_name }}"
        state: started
    
    - name: Wait for application to be ready
      wait_for:
        port: "{{ app_port }}"
        host: "{{ ansible_host }}"
        timeout: 30
    
    - name: Test application health endpoint
      uri:
        url: "http://{{ ansible_host }}:{{ app_port }}/health"
        method: GET
        status_code: 200
    
    - name: Display deployment summary
      debug:
        msg: |
          Deployment completed successfully!
          Application: {{ app_name }}
          Version: {{ app_version }}
          Environment: {{ app_environment }}
          Host: {{ inventory_hostname }}
          Port: {{ app_port }}
          Health Check: http://{{ ansible_host }}:{{ app_port }}/health
          Main Page: http://{{ ansible_host }}:{{ app_port }}/
"""
    
    playbook_file = lab_path / "playbooks" / "deploy-app.yml"
    playbook_file.write_text(playbook_content)
    print(f"  ✓ Created: {playbook_file.relative_to(lab_path)}")

def create_templates(lab_path):
    """Create Jinja2 templates for application and supervisor configuration."""
    print("\n🎨 Creating Jinja2 templates...")
    
    # Application configuration template
    app_conf = """# Application Configuration for {{ app_name }}
# Environment: {{ app_environment }}
# Generated by Ansible on {{ ansible_date_time.iso8601 }}

[application]
name = {{ app_name }}
environment = {{ app_environment }}
debug = {{ app_config.debug }}
log_level = {{ app_config.log_level }}
port = {{ app_port }}
workers = {{ app_config.max_workers }}
timeout = {{ app_config.timeout }}

[logging]
directory = {{ app_directory }}/logs
rotation_days = {{ log_rotation_days }}
max_size = 100MB

[monitoring]
enabled = {{ monitoring_enabled }}
health_endpoint = {{ health_check_url }}
"""
    
    app_conf_file = lab_path / "playbooks" / "templates" / "app.conf.j2"
    app_conf_file.write_text(app_conf)
    print(f"  ✓ Created: {app_conf_file.relative_to(lab_path)}")
    
    # Supervisor configuration template
    supervisor_conf = """# Supervisor configuration for {{ app_name }}
# Environment: {{ app_environment }}

[program:{{ app_name }}]
command={{ app_directory }}/venv/bin/python {{ app_directory }}/app/app.py
directory={{ app_directory }}/app
user={{ deploy_user }}
autostart=true
autorestart=true
startretries=3
redirect_stderr=true

# Logs
stdout_logfile={{ app_directory }}/logs/{{ app_name }}.out.log
stderr_logfile={{ app_directory }}/logs/{{ app_name }}.err.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=5

# Environment variables
environment=ENVIRONMENT="{{ app_environment }}",APP_VERSION="{{ app_version }}",APP_NAME="{{ app_name }}",APP_PORT="{{ app_port }}",HOSTNAME="{{ inventory_hostname }}",PYTHONPATH="{{ app_directory }}/app"
"""
    
    supervisor_conf_file = lab_path / "playbooks" / "templates" / "supervisor-app.conf.j2"
    supervisor_conf_file.write_text(supervisor_conf)
    print(f"  ✓ Created: {supervisor_conf_file.relative_to(lab_path)}")

def create_deployment_script(lab_path):
    """Create the ansible-deploy.sh automation script."""
    print("\n🔧 Creating deployment script...")
    script_content = """#!/bin/bash
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
"""
    
    script_file = lab_path / "ansible-deploy.sh"
    script_file.write_text(script_content)
    script_file.chmod(0o755)
    print(f"  ✓ Created: {script_file.relative_to(lab_path)}")

def create_makefile(lab_path):
    """Create Makefile for common operations."""
    print("\n📋 Creating Makefile...")
    makefile_content = """# =========================
# Makefile for Lab07 Deployments
# =========================

ENV ?= development
PLAYBOOK = playbooks/deploy-app.yml
INVENTORY = inventories/$(ENV).yml
ANSIBLE = ansible-playbook -i $(INVENTORY) $(PLAYBOOK)
DEPLOY_SCRIPT = ./ansible-deploy.sh

# Default target
all: deploy-check

# -------------------------
# Deployment targets
# -------------------------

deploy-check:
	@echo "Running deployment check for $(ENV) environment..."
	$(DEPLOY_SCRIPT) -e $(ENV) -p $(PLAYBOOK)

deploy:
	@echo "Deploying to $(ENV) environment..."
	$(DEPLOY_SCRIPT) -e $(ENV) -p $(PLAYBOOK)

# -------------------------
# Cleanup target
# -------------------------

clean:
	@echo "Cleaning up logs and supervisor configs..."
	rm -rf /home/student/deployed-apps/logs/* || true
	sudo rm -f /etc/supervisor/conf.d/flask-demo*.conf
	sudo rm -f /etc/supervisor/conf.d/flask-demo-web*.conf
	sudo supervisorctl reread || true
	sudo supervisorctl update || true
	@echo "Cleanup complete."

# -------------------------
# Helper targets
# -------------------------

status:
	@echo "Checking Supervisor status..."
	sudo supervisorctl status

logs-web1:
	@echo "Tailing logs for web1..."
	sudo tail -n 40 /home/student/deployed-apps/logs/flask-demo-web1.out.log || true
	sudo tail -n 40 /home/student/deployed-apps/logs/flask-demo-web1.err.log || true

logs-web2:
	@echo "Tailing logs for web2..."
	sudo tail -n 40 /home/student/deployed-apps/logs/flask-demo-web2.out.log || true
	sudo tail -n 40 /home/student/deployed-apps/logs/flask-demo-web2.err.log || true

test:
	@echo "Testing deployment endpoints..."
	curl http://localhost:8080/ || true
	curl http://localhost:8080/health || true
	curl http://localhost:8080/version || true
	curl http://localhost:8081/ || true
	curl http://localhost:8081/health || true
	curl http://localhost:8081/version || true

.PHONY: all deploy-check deploy clean status logs-web1 logs-web2 test
"""
    
    makefile_file = lab_path / "Makefile"
    makefile_file.write_text(makefile_content)
    print(f"  ✓ Created: {makefile_file.relative_to(lab_path)}")

def create_readme(lab_path):
    """Create a README for the lab."""
    print("\n📝 Creating README...")
    readme_content = """# Lab 7: Automate Remote Deployment with Ansible Playbooks

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
"""
    
    readme_file = lab_path / "README.md"
    readme_file.write_text(readme_content)
    print(f"  ✓ Created: {readme_file.relative_to(lab_path)}")

def main():
    """Main execution function."""
    print("=" * 60)
    print("Lab 7 Setup: Automate Remote Deployment with Ansible")
    print("=" * 60)
    
    # Path setup
    current_path = Path.cwd()
    pdf_path = current_path / "840154_L07.pdf"
    
    # Verify PDF exists
    if not pdf_path.exists():
        print(f"❌ Error: PDF manual not found at {pdf_path}")
        sys.exit(1)
    
    # Read the PDF manual
    pdf_text = read_pdf_manual(pdf_path)
    print(f"✓ Successfully read {len(pdf_text)} characters from PDF")
    
    # Create directory structure
    lab_path = create_directory_structure(current_path)
    
    # Create all lab files
    create_inventory_file(lab_path)
    create_group_variables(lab_path)
    create_deployment_playbook(lab_path)
    create_templates(lab_path)
    create_deployment_script(lab_path)
    create_makefile(lab_path)
    create_readme(lab_path)
    
    print("\n" + "=" * 60)
    print("✅ Lab 7 setup completed successfully!")
    print("=" * 60)
    print(f"\n📂 Lab created at: {lab_path}")
    print("\nNext steps:")
    print(f"  1. cd {lab_path.relative_to(current_path)}")
    print("  2. Review the files created")
    print("  3. Install Ansible (if not already installed)")
    print("  4. Run: make deploy-check ENV=development")
    print("  5. Run: make deploy ENV=development")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
