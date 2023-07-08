PROJ_PATH   ?= app
TESTS_PATH  ?= tests

### linters ###

.PHONY: black
black:
	black ${PROJ_PATH} ${TESTS_PATH}

.PHONY: ruff
ruff:
	ruff ${PROJ_PATH} ${TESTS_PATH}

.PHONY: mypy
mypy:
	mypy ${PROJ_PATH}

.PHONY: bandit
bandit:
	bandit -c pyproject.toml --silent -r ${PROJ_PATH}

.PHONY: check
check: black ruff mypy bandit

### tests ###

.PHONY: tests
tests:
	pytest --cov-report term-missing --cov=app --durations=3

### setup ###

.PHONY: install
install:
	poetry install

.PHONY: update
update:
	poetry update


### local dev ###

.PHONY: up
up:
	TARGET=development docker compose up --build -d


.PHONY: down
down:
	TARGET=development docker compose down
