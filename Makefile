PYTHON_VERSION=3.13
PYTHON_BIN=venv/bin/python
PIP_BIN=venv/bin/pip3
SOURCE_DIR=src

.PHONY: install

install: _setup_venv _install_hooks

uninstall: _uninstall_hooks _clean_venv

lint:
	${PYTHON_BIN} -m pylint $(SOURCE_DIR)

mypy:
	${PYTHON_BIN} -m mypy $(SOURCE_DIR) --ignore-missing-imports --strict --implicit-reexport

black:
	$(PYTHON_BIN) -m black $(SOURCE_DIR) --check --config ./pyproject.toml

flake:
	$(PYTHON_BIN) -m flake8 $(SOURCE_DIR) --config ./pyproject.toml

isort:
	$(PYTHON_BIN) -m isort $(SOURCE_DIR) --check-only --settings-file ./pyproject.toml

format:
	$(PYTHON_BIN) -m black $(SOURCE_DIR) --config ./pyproject.toml
	$(PYTHON_BIN) -m isort $(SOURCE_DIR) --settings-file ./pyproject.toml

check: black isort mypy flake lint

#####################
# PRIVATE FUNCTIONS #
#####################
_clean_venv:
	rm -rf venv

_create_venv:
	python$(PYTHON_VERSION) -m venv venv;

_install_requirements_in_venv:
	$(PIP_BIN) install -r requirements.txt --upgrade pip

_setup_venv: _clean_venv _create_venv _install_requirements_in_venv

_install_hooks:
	.hooks/install_hooks.sh -i

_uninstall_hooks:
	.hooks/install_hooks.sh -u all
