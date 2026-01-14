# =========================
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
