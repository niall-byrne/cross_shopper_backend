#!/usr/bin/make -f

.PHONY: help clean fmt lint security spelling test types backup clean-git format-python format-shell format-toml lint-markdown lint-python lint-shell lint-workflows lint-yaml security-audit security-leaks spelling-add spelling-markdown spelling-sync test-python

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  backup			   to make a copy of the db"
	@echo "  clean-git         to run git clean"
	@echo "  clean-pycache     to clean Python cache files."
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
	@echo "  test-python       to test the Python scripts"

clean: clean-git clean-pycache
fmt: format-shell format-toml format-python
lint: lint-markdown lint-python lint-shell lint-workflows lint-yaml
security: security-audit security-leaks
spelling: spelling-markdown security-leaks
test: test-python
types: types-python

backup:
	@echo "Backing up database ..."
	@cp -vp ./cross_shopper/db.sqlite3 ~/iCloud/Databases/cross_shopper/$$(date +%s).sqlite
	@cp -vp ./cross_shopper/db.sqlite3 ~/iCloud/Databases/cross_shopper/"__latest__.sqlite"

restore:
	@echo "Restoring database ..."
	@echo "Are you sure? [Y/n] " && read ANS && [ $${ANS:-N} = Y ]
	@cp -vp ~/iCloud/Databases/cross_shopper/"__latest__.sqlite" ./cross_shopper/db.sqlite3

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
	@poetry run bash -c "pre-commit run yapf --verbose --all-files"
	@poetry run bash -c "pre-commit run isort --verbose --all-files"
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
	@poetry run bash -c "pre-commit run isort --verbose --all-files"
	@poetry run bash -c "pre-commit run flake8 --verbose --all-files"
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

start:
	@echo "Starting Django ..."
	@cd cross_shopper && poetry run ./manage.py runserver

test-python:
	@echo "Testing Python scripts ..."
	@poetry run pytest cross_shopper -xvvv

types-python:
	@echo "Checking Python types ..."
	@poetry run bash -c "pre-commit run poetry-types-python --all-files --verbose"
