.DEFAULT_GOAL := help
SHELL = /bin/bash

pkg_src = {{cookiecutter.project_slug}}
tests_src = tests
all_src = $(pkg_src) $(tests_src)

isort = isort -rc $(all_src)
autoflake = autoflake -r --remove-all-unused-imports --ignore-init-module-imports $(all_src)
black = black $(all_src)
flake8 = flake8 $(all_src)
mypy_base = mypy --show-error-codes
mypy = $(mypy_base) $(all_src)
test = pytest --cov={{cookiecutter.project_slug}}

.PHONY: all  ## Run the most common rules used during development
all: static test

.PHONY: static  ## Perform all static checks (format, lint, mypy)
static: format lint mypy

.PHONY: test  ## Run tests
test:
	poetry run $(test)

.PHONY: format  ## Auto-format the source code (isort, autoflake, black)
format:
	poetry run $(isort)
	poetry run $(autoflake) -i
	poetry run $(black)

.PHONY: lint  ## Run flake8 over the application source and tests
lint:
	poetry run $(flake8)

.PHONY: mypy  ## Run mypy over the application source and tests
mypy:
	poetry run $(mypy)

.PHONY: imports  ## Check for undefined imports or package-level cyclic imports
imports:
	poetry run python {{cookiecutter.project_slug}}/util/check_imports.py {{cookiecutter.project_slug}} --display

.PHONY: testcov  ## Run tests, generate a coverage report, and open in browser
testcov:
	poetry run $(test)
	@echo "building coverage html"
	@coverage html
	@echo "A coverage report was generated at htmlcov/index.html"
	@if [ "$$(uname -s)" = "Darwin" ]; then \
		open htmlcov/index.html; \
	fi

.PHONY: ci  ## Run all CI validation steps without making any changes to code
default: test lint mypy check-format

.PHONY: check-format  ## Check the source code format without changes
check-format:
	poetry run $(isort) --check-only
	@echo poetry run $(autoflake) --check
	@( set -o pipefail; poetry run $(autoflake) --check | (grep -v "No issues detected!" || true) )
	poetry run $(black) --check

.PHONY: clean  ## Remove temporary and cache files/directories
clean:
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name .coverage`
	rm -f `find . -type f -name ".coverage.*"`
	rm -rf `find . -name __pycache__`
	rm -rf `find . -type d -name '*.egg-info' `
	rm -rf `find . -type d -name 'pip-wheel-metadata' `
	rm -rf `find . -type d -name .pytest_cache`
	rm -rf `find . -type d -name .cache`
	rm -rf `find . -type d -name .mypy_cache`
	rm -rf `find . -type d -name htmlcov`
	rm -rf `find . -type d -name "*.egg-info"`
	rm -rf `find . -type d -name build`
	rm -rf `find . -type d -name dist`

.PHONY: lock  ## Update the lockfile
lock:
	./scripts/lock.sh

.PHONY: develop  ## Set up the development environment, or reinstall from the lockfile
develop:
	./scripts/develop.sh

.PHONY: docs-build  ## Generate the docs and update README.md
docs-build:
	poetry run python -m mkdocs build
	cp ./docs/index.md ./README.md
	cp ./docs/contributing.md ./CONTRIBUTING.md

.PHONY: docs-build-ci  ## Generate the docs and check README.md is up-to-date
docs-build-ci:
	poetry run python -m mkdocs build
	cmp README.md docs/index.md
	cmp CONTRIBUTING.md docs/contributing.md

.PHONY: docs-format  ## Format the python code that is part of the docs
docs-format:
	poetry run isort -rc $(docs_src)
	poetry run autoflake -r --remove-all-unused-imports --ignore-init-module-imports $(docs_src) -i
	poetry run black -l 82 $(docs_src)

.PHONY: docs-live  ## Serve the docs with live reload as you make changes
docs-live:
	poetry run mkdocs serve --dev-addr 0.0.0.0:8008

.PHONY: version  ## Bump the version in both pyproject.toml and __init__.py (usage: `make version version=minor`)
version: poetryversion
	$(eval NEW_VERS := $(shell cat pyproject.toml | grep "^version = \"*\"" | cut -d'"' -f2))
	@sed -i "" "s/__version__ = .*/__version__ = \"$(NEW_VERS)\"/g" $(pkg_src)/__init__.py

.PHONY: poetryversion
poetryversion:
	poetry version $(version)

.PHONY: help  ## Display this message
help:
	@grep -E \
		'^.PHONY: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ".PHONY: |## "}; {printf "\033[36m%-16s\033[0m %s\n", $$2, $$3}'
