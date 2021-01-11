IMAGE ?= opbeans/opbeans-loadgen
VERSION ?= latest
LTS_ALPINE ?= 12-alpine
VENV ?= ./venv
PYTHON ?= python3

.PHONY: help
.DEFAULT_GOAL := help

help: ## Display this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

all: build test

build: ## Build docker image
	@docker build --file Dockerfile --tag=${IMAGE}:${VERSION} .

bats: ## Install bats in the project itself
	@git clone https://github.com/sstephenson/bats.git

venv: requirements-dev.txt
	test -d $(VENV) || virtualenv -q --python=$(PYTHON) $(VENV);\
	. $(VENV)/bin/activate || exit 1;\
	pip install -r requirements-dev.txt;\
	touch $(VENV);\

prepare-test: bats venv ## Prepare the dependencies
	@docker pull node:${LTS_ALPINE}
	@mkdir -p target
	@git submodule sync
	@git submodule update --init --recursive

test: prepare-test ## Run the tests
	@echo "Tests are in progress, please be patient"
	@bats/bin/bats --tap tests | tee target/results.tap
	@docker run --rm -v "${PWD}":/usr/src/app -w /usr/src/app node:${LTS_ALPINE} \
					sh -c "npm install tap-xunit -g && cat target/results.tap | tap-xunit --package='co.elastic.opbeans' > target/junit-results.xml"
	@PYTHONPATH=. $(VENV)/bin/pytest

publish: build ## Publish docker image
	@docker push "${IMAGE}:${VERSION}"

clean: ## Clean autogenerated files/folders
	@rm -rf bats
	@rm -rf target
