# install only in venv, please.

TEST_PATH=./tests

install:
	pip install poetry
	poetry install
	pre-commit install

black:
	black vk/
	black tests

lint:
	flake8 vk

delete-unused-imports:
	autoflake --in-place --remove-unused-variables -r vk

reorder-imports:
	reorder-python-imports --application-directories=vk

docs:
	mkdocs serve

docs-deploy:
	mkdocs gh-deploy

test:
	py.test --verbose --color=yes $(TEST_PATH)