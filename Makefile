NAME=dbzr-projects-audit
VERSION=$(shell git rev-parse HEAD)
SEMVER_VERSION=$(shell git describe --abbrev=0 --tags)
REPO=quay.io/babylonhealth
DEPLOY_DEV_URL=http://dev-ai-deploy.babylontech.co.uk:5199/job/AI-deploy-dev/buildWithParameters
DEPLOY_STAGING_URL=http://dev-ai-deploy.babylontech.co.uk:5199/job/AI-deploy-staging/buildWithParameters
PYPI_URL=https://pypi.fury.io/$(INDEX_SERVER_USER)/babylonpartners/

clean:
	find . -name "*.py[cod]" -delete

install-requirements:
	pip3 install -r requirements.txt --extra-index-url $(PYPI_URL)

install-test-requirements:
	pip3 install -r requirements-test.txt --extra-index-url $(PYPI_URL)

run: build
	docker run --rm -it $(REPO)/$(NAME):$(VERSION)

build: clean 
	echo $(VERSION) > .commit-id
	docker build --build-arg pypi_url=$(PYPI_URL) -t $(REPO)/$(NAME):$(VERSION) .

lint:
	flake8 --exclude=.venv

check-format:
	black --check --diff .
	isort --recursive --check-only --diff .

format:
	black .
	isort --recursive .

mypy:
	mypy --disallow-untyped-calls --disallow-incomplete-defs --check-untyped-defs .

test:
	pytest -v --cov-config .coveragerc --cov .
	coverage xml

pull:
	docker pull $(REPO)/$(NAME):$(VERSION)

install:
	docker push $(REPO)/$(NAME):$(VERSION)

tag-latest: build
	docker tag $(REPO)/$(NAME):$(VERSION) $(REPO)/$(NAME):latest
	docker push $(REPO)/$(NAME):latest

tag-semver: build
	@if docker run -e DOCKER_REPO=babylonhealth/$(NAME) -e DOCKER_TAG=$(SEMVER_VERSION) quay.io/babylonhealth/tag-exists; \
	  then echo "Tag $(SEMVER_VERSION) already exists!" && exit 1 ; \
	else \
	  docker tag $(REPO)/$(NAME):$(VERSION) $(REPO)/$(NAME):$(SEMVER_VERSION); \
	  docker push $(REPO)/$(NAME):$(SEMVER_VERSION); \
	fi

deploy-dev:
	@curl -vvv -XPOST "${DEPLOY_DEV_URL}?token=${JENKINS_DEV_TOKEN}&APP=${NAME}&VERSION=${VERSION}"

deploy-staging:
	@curl -vvv -XPOST "${DEPLOY_STAGING_URL}?token=${JENKINS_STAGING_TOKEN}&APP=${NAME}&VERSION=${SEMVER_VERSION}"

.PHONY: lint test clean build run install install-requirements install-test-requirements tag-latest tag-semver deploy-dev deploy-staging
