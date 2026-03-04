#!/usr/bin/make -f

.PHONY: help clean fmt lint security spelling test types backup clean-git format-python format-shell format-toml lint-markdown lint-python lint-shell lint-workflows lint-yaml security-audit security-leaks spelling-add spelling-markdown spelling-sync test-python

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  clean-git         to run git clean"
	@echo "  clean-pycache     to clean Python cache files."
	@echo "  db-backup         to make a copy of the production db"
	@echo "  db-list           to list production db backups"
	@echo "  db-restore        to restore a backup of the production db"
	@echo "  dev               to start the dev environment"
	@echo "  dev-db            to rebuild the dev database"
	@echo "  format-python     to format Python scripts"
	@echo "  format-shell      to format shell scripts"
	@echo "  format-toml       to format TOML files"
	@echo "  lint-markdown     to lint Markdown files"
	@echo "  lint-python       to lint Python scripts"
	@echo "  lint-shell        to lint shell scripts"
	@echo "  lint-workflows    to lint GitHub workflows"
	@echo "  lint-yaml         to lint YAML files"
	@echo "  security-audit    to check for dependency vulnerabilities"
	@echo "  security-leaks    to scan for credential leaks"
	@echo "  spelling-add      to add a regex to the ignore patterns"
	@echo "  spelling-markdown to spellcheck markdown files"
	@echo "  spelling-sync     to synchronize vale packages"
	@echo "  production        to start the production environment"
	@echo "  test-python       to test the Python scripts"

clean: clean-git clean-pycache
fmt: format-shell format-toml format-python
lint: lint-markdown lint-python lint-shell lint-workflows lint-yaml
security: security-audit security-leaks
spelling: spelling-markdown security-leaks
test: test-python
types: types-python

clean-git:
	@echo "Cleaning git content ..."
	@git clean -fd
	@echo "Done."

clean-pycache:
	@echo "Cleaning __pycache__ content ..."
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	@echo "Done."

coverage:
	@echo "Running coverage ..."
	@poetry run bash -c "coverage run -m pytest cross_shopper && coverage html || (coverage report; exit 127)"
	@echo "Done."

db-backup:
	@echo "Backing up production database ..."
	@cp -vp ./cross_shopper/db.production.sqlite ~/iCloud/Databases/cross_shopper/$$(date +%s).sqlite
	@cp -vp ./cross_shopper/db.production.sqlite ~/iCloud/Databases/cross_shopper/"__latest__.sqlite"

db-list:
	@echo "List production database backups ..."
	@ls -laht ~/iCloud/Databases/cross_shopper

db-restore:
	@echo "Restoring production database ..."
	@echo "Are you sure? [Y/n] " && read ANS && [ $${ANS:-N} = Y ]
	@cp -vp ~/iCloud/Databases/cross_shopper/"__latest__.sqlite" ./cross_shopper/db.production.sqlite

dev:
	@echo "Starting Django development environment ..."
	@cd cross_shopper && poetry run ./manage.py runserver

dev-db:
	@echo "Rebuilding development database ..."
	@cp -vp ./cross_shopper/db.production.sqlite ./cross_shopper/db.development.sqlite

format-shell:
	@echo "Checking shell scripts ..."
	@poetry run bash -c "pre-commit run format-shell --all-files --verbose"
	@echo "Done."

format-toml:
	@echo "Checking TOML files ..."
	@poetry run bash -c "pre-commit run format-toml --all-files --verbose"
	@echo "Done."

format-python:
	@echo "Formatting all Python files ..."
	@poetry run bash -c "pre-commit run fmt-type-checking-coverage --verbose --all-files"
	@poetry run bash -c "pre-commit run ruff-fix --hook-stage manual --verbose --all-files"
	@poetry run bash -c "pre-commit run yapf --verbose --all-files"
	@echo "Done."

lint-markdown:
	@echo "Checking Markdown files ..."
	@poetry run bash -c "pre-commit run lint-markdown --all-files --verbose"
	@echo "Done."

lint-shell:
	@echo "Checking shell scripts ..."
	@poetry run bash -c "pre-commit run lint-shell --all-files --verbose"
	@echo "Done."

lint-python:
	@echo "Checking Python files ..."
	@poetry run bash -c "pre-commit run ruff-lint --verbose --all-files"
	@echo "Done."

lint-workflows:
	@echo "Checking workflows ..."
	@poetry run bash -c "pre-commit run lint-github-workflow --all-files --verbose"
	@poetry run bash -c "pre-commit run lint-github-workflow-header --all-files --verbose"
	@echo "Done."

lint-yaml:
	@echo "Checking YAML files ..."
	@poetry run bash -c "pre-commit run yamllint --all-files --verbose"
	@echo "Done."

spelling-add:
	@echo "Adding word ..."
	@echo "${MAKE_ARGS}" >> ".vale/Vocab/${PROJECT_NAME}/accept.txt"
	@sort -u -o ".vale/Vocab/${PROJECT_NAME}/accept.txt" ".vale/Vocab/${PROJECT_NAME}/accept.txt"

security-audit:
	@echo "Auditing dependencies ..."
	@poetry run bash -c "pre-commit run python-safety-dependencies-check --all-files --verbose"
	@echo "Done."

security-leaks:
	@echo "Scanning for credentials ..."
	@poetry run bash -c "pre-commit run security-credentials --all-files --verbose"
	@echo "Done."

spelling-markdown:
	@echo "Checking spelling ..."
	@poetry run bash -c "pre-commit run spelling-markdown --all-files --verbose"
	@echo "Done."

spelling-sync:
	@echo "Synchronizing vale ..."
	@poetry run bash -c "pre-commit run --hook-stage manual spelling-vale-sync --all-files --verbose"

production:
	@echo "Starting Django ..."
	@cd cross_shopper && DJANGO_SETTINGS_MODULE='config.production' poetry run ./manage.py collectstatic --noinput
	@cd cross_shopper && DJANGO_SETTINGS_MODULE='config.production' poetry run gunicorn --bind 0.0.0.0:8000 --workers=2 --access-logfile - --error-logfile - --log-level info root.wsgi:application

test-python:
	@echo "Testing Python scripts ..."
	@poetry run pytest cross_shopper -xvvv

types-python:
	@echo "Checking Python types ..."
	@poetry run bash -c "pre-commit run poetry-types-python --all-files --verbose"
