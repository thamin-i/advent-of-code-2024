PIP_BIN=.venv/bin/pip3
PRECOMMIT_BIN=.venv/bin/pre-commit
PYTHON_BIN=.venv/bin/python3
PYTHON_VERSION=3.13
SOURCE_DIR=advent_of_code_2024

.PHONY: install

install: setup_local install_hooks

install_hooks:
	.hooks/install_hooks.sh -i

show_hooks:
	.hooks/install_hooks.sh -s

uninstall_hooks:
	.hooks/install_hooks.sh -u ${HOOKS_TO_UNINSTALL}

uninstall_all_hooks:
	.hooks/install_hooks.sh -u all

setup_local:
	poetry install --with dev

remove_venv:
	rm -rf .venv

uninstall: uninstall_all_hooks remove_venv

lint:
	export PYTHONPATH="${PYTHONPATH}:$$(pwd)/$(SOURCE_DIR)" && $(PYTHON_BIN) -m pylint $(SOURCE_DIR)

mypy:
	$(PYTHON_BIN) -m mypy $(SOURCE_DIR) --ignore-missing-imports --strict --implicit-reexport

black:
	$(PYTHON_BIN) -m black $(SOURCE_DIR) --check

flake:
	$(PYTHON_BIN) -m flake8 $(SOURCE_DIR) --config ./setup.cfg

isort:
	$(PYTHON_BIN) -m isort $(SOURCE_DIR) --check-only

format:
	$(PYTHON_BIN) -m black $(SOURCE_DIR)
	$(PYTHON_BIN) -m isort $(SOURCE_DIR)

check: black isort mypy flake lint
