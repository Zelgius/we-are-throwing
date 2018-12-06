clean:
	rm -rf dist/*
	find . -type d -name __pycache__ \
		-o \( -type f -name '*.py[cod]' \) -print0 \
		| xargs -0 rm -rf

build:
	pipenv run python3 setup.py bdist_wheel

static-analysis:
	pipenv install --dev
	pipenv run pylint we_are_throwing

test:
	pipenv install --dev
	pipenv lock -r > requirements.txt
	pipenv lock -r --dev >> requirements.txt
	pipenv run tox
	rm -rf requirements.txt

install:
	docker build . -t we-are-throwing:latest

run: install
	docker run --rm -it -p 8000:8000 we-are-throwing:latest

.PHONY: clean
.PHONY: build
.PHONY: run
.PHONY: test
.PHONY: static-analysis
.PHONY: install
